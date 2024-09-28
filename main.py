from openai import OpenAI
client = OpenAI()

path1 = "./data/0a866589-0d5d-4a9f-9121-89530653f42c.json"



with open(path1, 'r') as file:
    file_contents = file.read()


completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"What do you see in this file {file_contents}"
        }
    ]
)



print(completion.choices[0].message)
