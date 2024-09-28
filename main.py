from openai import OpenAI
client = OpenAI()


completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Give me a list of all openai models"
        }
    ]
)

print(completion.choices[0].message)