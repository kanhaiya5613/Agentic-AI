# Few short Prompting is a technique where you provide the model with a few examples of the task or question you want it to perform. This helps the model understand the context and the expected format of the response, which can lead to more accurate and relevant outputs.

from openai import OpenAI
import json
client = OpenAI(
    api_key="AIzaSyCIlotwaRVzZs1TUwEBo3l4ZqIROxrE7lU",
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
PLAN: {"step": "PLAN", "content": "Seems like user is intrested in solving a math problem. I need to follow BODMAS rule to solve this problem. First I will solve 3*5, then divide the result by 10 and then add 2 to the result."
PLAN: {"step": "PLAN", "content": "3*5 is 15. Now I will divide 15 by 10, which is 1.5. Finally I will add 2 to 1.5, which gives me 3.5"
pLAN: {"step": "PLAN", "content": "I have solved the problem and the final answer is 3.5. Now I will give the output to the user."}
OUTPUT: {"step": "OUTPUT", "content": "The answer to the problem 2+3*5/10 is 3.5"}
"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "write a code of factorial in python"}
    ]
)
print(response.choices[0].message.content)