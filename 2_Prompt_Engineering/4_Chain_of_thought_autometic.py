# Few short Prompting is a technique where you provide the model with a few examples of the task or question you want it to perform. This helps the model understand the context and the expected format of the response, which can lead to more accurate and relevant outputs.

from openai import OpenAI
import json
client = OpenAI(
    api_key="AIzaSyACuIywxG4epmg9ncNnlJFCNtYnLFJRSfI",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)
SYSTEM_PROMPT = """
you're an expert AI assistant in resolving user queries using chain of thought.
you work on START, PLAN, and OUTPUT steps.
you need to first PLAN what needs to be done . the PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an output.

Rules:
- Strictly follow the given JSON Output format
- Onlu run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN(That can be multiple times) and finally OUTPUT(which is going to be displayed to the user).

Output JSON Format:
{ "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

Example:
START: Hey, you can solve 2+3*5/10
PLAN: {"step": "PLAN": "content": "Seems like user is intrested in solving a math problem. I need to follow BODMAS rule to solve this problem."}
PLAN:{"STEP": "PLAN" "content" "yes, The BODMAS is correct thing to be done here"}
PLAN: {"step": "PLAN", "content": "first we must multiply 3*5 which is 15"}
PLAN: {"step": "PLAN", "content": "Now the new equation is 2+15/10"}
PLAN: {"step": "PLAN", "content": "we must perform divide that is 15/10 = 1.5."}
pLAN: {"step": "PLAN", "content": "Now our new equation is 2+1.5."}
PLAN: {"step": "PLAN", "content": "now finally lets perform the addition and we get 3.5"}
OUTPUT: {"step": "OUTPUT", "content": "The answer to the problem 2+3*5/10 is 3.5"}
"""
print("\n\n\n")
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
user_query = input("👉 ")
message_history.append({"role": "user", "content": user_query})
while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("User Query:", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "PLAN":
        print("Planning:", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "OUTPUT":
        print("Final Output:", parsed_result.get("content"))
        break


