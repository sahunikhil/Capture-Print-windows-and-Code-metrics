# from openai import OpenAI
# client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)


# import os

# # os.environ["OPENAI_API_KEY"] = "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"

# api_key = os.getenv("OPENAI_API_KEY")
# print("API Key:", api_key)



# import os

# # Set the environment variable
# os.environ["OPENAI_API_KEY"] = "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"

# # Print the environment variable to verify
# print(os.environ["OPENAI_API_KEY"])

# # Now you can access the environment variable in your code
# client = OpenAI()



import pathlib
import textwrap
import json

import google.generativeai as genai

with open('final_capture_print.py') as f:
    code_in_text = f.read()

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(f"""I will give you code in text format you have to give output only in json with no other text apart from json.
                                  The keys for json will be  Time Complexity, Space Complexity, Cyclomatic complexity, Code Smells and Security vulnerabilities.
                                  You have to provide values to the keys.
                                  Here's code: {code_in_text}""")
print(response.text)
print()

res = response.text
json_res = json.loads(res[res.find("{") : res.find("}")+1])
print(json_res)