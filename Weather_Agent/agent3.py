import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize the client with the Gemini-OpenAI bridge
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"The Weather in {city} is {response.text}"
    except Exception:
        pass
    return "Error: Unable to fetch weather data."


available_tools = {"get_weather": get_weather,
                   "run_command": run_command
                   }

SYSTEM_PROMPT = """
you're an expert AI assistant in resolving user queries using chain of thought.
you work on START, PLAN, and OUTPUT steps.
you need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an output.
you can also call a tool if required from the list of available tools.
for every tool call wait for the observe step which is the output from the called tool.

Rules:
- Strictly follow the given JSON Output format.
- Only run one step at a time.
- The sequence of steps is START, PLAN, and finally OUTPUT.

Output JSON Format:
{ "step": "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool":"string", "input":"string" }

Available Tools:
- get_weather(city: str): Takes city name as an input string and returns the weather info about the city.
- run_command(cmd: str): Takes a system linux command as string and executes the command on user's system and return the system output.


Example 1:
START: Hey, you can solve 2+3*5/10
PLAN: {"step": "PLAN", "content": "Seems like user is intrested in solving a math problem. I need to follow BODMAS rule to solve this problem."}
PLAN: {"step": "PLAN", "content": "yes, The BODMAS is correct thing to be done here"}
PLAN: {"step": "PLAN", "content": "first we must multiply 3*5 which is 15"}
PLAN: {"step": "PLAN", "content": "Now the new equation is 2+15/10"}
PLAN: {"step": "PLAN", "content": "we must perform divide that is 15/10 = 1.5."}
PLAN: {"step": "PLAN", "content": "Now our new equation is 2+1.5."}
PLAN: {"step": "PLAN", "content": "now finally lets perform the addition and we get 3.5"}
OUTPUT: {"step": "OUTPUT", "content": "The answer to the problem 2+3*5/10 is 3.5"}

Example 2:
START: what is the weather of Delhi?
PLAN: {"step": "PLAN", "content": "Seems like user intrested to know about the weather of delhi india"}
PLAN: {"step": "PLAN", "content": "Lets see if we have any available tool from the list of avalable tools"}
PLAN: {"step": "PLAN", "content": "Great we have get_weather tool available for this query."}
PLAN: {"step": "PLAN", "content": "I need to call get_weather tool for delhi as input in city"}
TOOL: {"step": "TOOL", "tool": "get_weather", "input": "delhi"}
OBSERVE: {"step": "OBSERVE", "tool": "get-weather", "output": "The temp of delhi is cloudy with 20C"}
PLAN: {"step": "PLAN", "content": "Great, I got the weather of delhi"}
OUTPUT: {"step": "OUTPUT", "content": "The Weather of delhi is 20C with some cloudy sky."}

"""


class MyOutputFormat(BaseModel):
    step: str = Field(
        ..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc"
    )
    content: Optional[str] = Field(
        None, description="The Optional String content for the step"
    )
    tool: Optional[str] = Field(None, description="the ID of the tool to call.")
    input: Optional[str] = Field(None, description="the input params for the tool")


def main():
    print("\n--- Agentic Weather Assistant ---\n")
    message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    user_query = input("👉 ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        try:
            response = client.chat.completions.parse(
                model="gemini-2.5-flash",
                response_format=MyOutputFormat,
                messages=message_history,
            )

            raw_result = response.choices[0].message.content
            message_history.append({"role": "assistant", "content": raw_result})

            
            parsed_result = response.choices[0].message.parsed

            if parsed_result.step == "PLAN":
                print(f"🧠 [PLANNING]: {parsed_result.content}")
                continue

            elif parsed_result.step == "TOOL":
                tool_to_call = parsed_result.tool
                tool_input = parsed_result.input

                if not tool_to_call or not tool_input:
                    print("❌ Error: Tool name or input is missing.")
                    break

                print(f"🔨 [TOOL]: Calling {tool_to_call} for {tool_input}...")

                if tool_to_call in available_tools:
                    tool_response = available_tools[tool_to_call](tool_input)
                    observation_data = {
                        "step": "OBSERVE",
                        "tool": tool_to_call,
                        "output": tool_response,
                    }
                    message_history.append(
                        {"role": "user", "content": json.dumps(observation_data)}
                    )
                    print(f"👁️  [OBSERVE]: {tool_response}")
                else:
                    print(f"❌ Error: Tool '{tool_to_call}' not found.")
                    error_data = {
                        "step": "OBSERVE",
                        "tool": tool_to_call,
                        "output": f"Tool '{tool_to_call}' is not available.",
                    }
                    message_history.append(
                        {"role": "user", "content": json.dumps(error_data)}
                    )
                continue

            elif parsed_result.step == "OUTPUT":
                print(f"\n🤖 [RESULT]: {parsed_result.content}")
                break

            else:
                print(f"⚠️  Unknown step '{parsed_result.step}', skipping...")
                continue

        except Exception as e:
            print(f"❌ Critical Loop Error: {e}")
            break

main()
