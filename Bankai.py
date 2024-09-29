import os
import json
from openai import OpenAI

# Input JSON data (simulating the paths you provided)
data = [
{"name": "path0", "value": "/home/mrdine/darkmen/data/042236c5-a686-41de-bc03-ebc81e07a7e1.json"},
{"name": "path1", "value": "/home/mrdine/darkmen/data/047d6909-b9a4-410f-83d3-7137c9d5101c.json"},
{"name": "path2", "value": "/home/mrdine/darkmen/data/04d3bffe-7394-4397-b545-779bdd0a7201.json"},
{"name": "path3", "value": "/home/mrdine/darkmen/data/0a866589-0d5d-4a9f-9121-89530653f42c.json"},
{"name": "path4", "value": "/home/mrdine/darkmen/data/13f12c58-dbaa-47ae-a091-0bf5445b0c66.json"},
{"name": "path5", "value": "/home/mrdine/darkmen/data/162d2502-9b6d-4cbb-b98b-42d29d66b913.json"},
{"name": "path6", "value": "/home/mrdine/darkmen/data/1a9dfff8-9baa-4202-8364-1660b9641c60.json"},
{"name": "path7", "value": "/home/mrdine/darkmen/data/1cb88c13-26a6-4771-a260-444b50808394.json"},
{"name": "path8", "value": "/home/mrdine/darkmen/data/1d040883-9009-4dc7-9acc-5a3fc069532d.json"},
{"name": "path9", "value": "/home/mrdine/darkmen/data/2049c529-8a1f-471d-9511-44ca46add579.json"},
{"name": "path10", "value": "/home/mrdine/darkmen/data/21687314-3b24-4f58-a239-2bd236667807.json"},
{"name": "path11", "value": "/home/mrdine/darkmen/data/238987b5-7148-4185-b11e-a332013c6f4d.json"},
{"name": "path12", "value": "/home/mrdine/darkmen/data/2525106f-baf5-48e8-94f0-f26e449481f2.json"},
{"name": "path13", "value": "/home/mrdine/darkmen/data/2697500b-bcad-4e53-9879-45e94313181a.json"},
{"name": "path14", "value": "/home/mrdine/darkmen/data/2a990775-661a-4fed-a590-46e4f9cdaf54.json"},
{"name": "path15", "value": "/home/mrdine/darkmen/data/2d3a1607-300f-4c7c-bbe0-880e1ac418fb.json"},
{"name": "path16", "value": "/home/mrdine/darkmen/data/2d6fc25e-fd06-4080-89a0-fc2cb823f904.json"},
{"name": "path17", "value": "/home/mrdine/darkmen/data/31f0f196-485a-44c0-8bcf-43227ced2d14.json"},
{"name": "path18", "value": "/home/mrdine/darkmen/data/3c3d20b8-aa88-4daa-8ba0-c94ab8fc5c76.json"},
{"name": "path19", "value": "/home/mrdine/darkmen/data/3d73efca-77d1-4361-82b7-4bc5f8668533.json"},
{"name": "path20", "value": "/home/mrdine/darkmen/data/3ee81e59-7bf5-4a3e-a036-d9faf26e9ab4.json"},
{"name": "path21", "value": "/home/mrdine/darkmen/data/3f3f7a59-7303-4908-8ff7-c1a6824396c5.json"},
{"name": "path22", "value": "/home/mrdine/darkmen/data/3f7b3ef7-12d6-4c15-9a90-87811681dec1.json"},
{"name": "path23", "value": "/home/mrdine/darkmen/data/40b71a01-1b61-411a-a09b-bc5f18978120.json"},
{"name": "path24", "value": "/home/mrdine/darkmen/data/41610f67-77a7-4480-8930-40dc0ae84a39.json"},
{"name": "path25", "value": "/home/mrdine/darkmen/data/424e9e3f-9a81-4c0b-9ad8-e3da0f215f18.json"},
{"name": "path26", "value": "/home/mrdine/darkmen/data/4323289a-337e-469a-8e76-d99cbb5432c0.json"},
{"name": "path27", "value": "/home/mrdine/darkmen/data/43236081-09ec-426f-ac59-17710cb38614.json"},
{"name": "path28", "value": "/home/mrdine/darkmen/data/436a59ae-9a57-4bee-a5d2-02c3115756e3.json"},
{"name": "path29", "value": "/home/mrdine/darkmen/data/439cddbd-ffe7-46ab-bd70-c5c3a2989edf.json"},
{"name": "path30", "value": "/home/mrdine/darkmen/data/4455bc62-10d2-40d4-b717-fcff4c2a704d.json"},
{"name": "path31", "value": "/home/mrdine/darkmen/data/469ea43e-fdde-400b-8979-a058d56c6ee6.json"},
{"name": "path32", "value": "/home/mrdine/darkmen/data/475052dc-3597-485c-a32b-b44e05c5739f.json"},
{"name": "path33", "value": "/home/mrdine/darkmen/data/4c62706c-e244-40ab-8042-20a235bdbd2e.json"},
{"name": "path34", "value": "/home/mrdine/darkmen/data/4cd9475c-5888-47bb-9d20-24cb3fe4d03d.json"},
{"name": "path35", "value": "/home/mrdine/darkmen/data/50519cb4-116b-4392-b69a-dde04be10eea.json"},
{"name": "path36", "value": "/home/mrdine/darkmen/data/5600d1f3-0a59-40ec-a26c-5d8e28390b9d.json"},
{"name": "path37", "value": "/home/mrdine/darkmen/data/58268d95-6a22-4a53-9bde-a33f2b2ec29a.json"},
{"name": "path38", "value": "/home/mrdine/darkmen/data/59e902c0-3c01-47aa-bb2f-2ed8da895ef6.json"},
{"name": "path39", "value": "/home/mrdine/darkmen/data/5a4adf78-3a26-4cda-92a1-7bfe89386fab.json"},
{"name": "path40", "value": "/home/mrdine/darkmen/data/5e39b13e-fb59-4370-b9ec-9870bc893097.json"},
{"name": "path41", "value": "/home/mrdine/darkmen/data/628ebc66-6e45-4648-9059-baa37424eaf9.json"},
{"name": "path42", "value": "/home/mrdine/darkmen/data/6434515b-8541-4861-bb24-8acd6e77e8c4.json"},
{"name": "path43", "value": "/home/mrdine/darkmen/data/6578e7ed-534a-458e-a406-267fe76a413f.json"},
{"name": "path44", "value": "/home/mrdine/darkmen/data/66274262-859c-4d79-9a16-46ee698e637a.json"},
{"name": "path45", "value": "/home/mrdine/darkmen/data/66c4a5d1-71d7-4cdd-8326-80af1ff1b933.json"},
{"name": "path46", "value": "/home/mrdine/darkmen/data/6b220ec4-0c2f-4c9a-8dd7-18acd57e7cf1.json"},
{"name": "path47", "value": "/home/mrdine/darkmen/data/6c4e0cb8-1ff1-4b6e-a670-106af4d1080f.json"},
{"name": "path48", "value": "/home/mrdine/darkmen/data/6fe38fbc-5078-41b1-b3c8-a15388d5f4c3.json"},
{"name": "path49", "value": "/home/mrdine/darkmen/data/71ca6dda-ed74-4c4a-a2da-043f682ab8eb.json"},
{"name": "path50", "value": "/home/mrdine/darkmen/data/737e38f1-2c44-469d-bed9-9d2f16d6da10.json"},
{"name": "path51", "value": "/home/mrdine/darkmen/data/7bf96f00-3f46-4863-8afb-38d2bf0a864f.json"},
{"name": "path52", "value": "/home/mrdine/darkmen/data/81a1a951-6283-4e53-ae51-5248064a773a.json"},
{"name": "path53", "value": "/home/mrdine/darkmen/data/8be8885f-9d5f-4750-b30e-9b5f719d9819.json"},
{"name": "path54", "value": "/home/mrdine/darkmen/data/8da51681-6f88-4c94-b2cb-3e75f668e23d.json"},
{"name": "path55", "value": "/home/mrdine/darkmen/data/914daeb5-747d-40b6-a588-d5439e4d5f26.json"},
{"name": "path56", "value": "/home/mrdine/darkmen/data/91bf13e1-e86e-4788-927d-7cb8af862e24.json"},
{"name": "path57", "value": "/home/mrdine/darkmen/data/92326c47-4d4a-4c3b-94ce-82cc5b47c126.json"},
{"name": "path58", "value": "/home/mrdine/darkmen/data/96e395eb-d25c-4814-bbf8-9116d0faa19b.json"},
{"name": "path59", "value": "/home/mrdine/darkmen/data/979feeb2-ad11-4729-bc76-4783c2901a33.json"},
{"name": "path60", "value": "/home/mrdine/darkmen/data/996c4933-513c-4e7e-8ba6-1b47349b46bc.json"},
{"name": "path61", "value": "/home/mrdine/darkmen/data/9f1e8e44-3977-4978-8f63-149d3b2241d8.json"},
{"name": "path62", "value": "/home/mrdine/darkmen/data/a2701246-11b6-44a9-8f09-0cdc28bd5f95.json"},
{"name": "path63", "value": "/home/mrdine/darkmen/data/a41b3bd1-dd17-4d1f-abfd-7c60710e3248.json"},
{"name": "path64", "value": "/home/mrdine/darkmen/data/a80447f4-0bbb-40f9-a052-bd469aef7748.json"},
{"name": "path65", "value": "/home/mrdine/darkmen/data/a986c29d-27df-4dac-a895-1e399f3e2830.json"},
{"name": "path66", "value": "/home/mrdine/darkmen/data/ab759b51-8ccb-4e4b-bc87-8ab7400210d4.json"},
{"name": "path67", "value": "/home/mrdine/darkmen/data/ac1e298b-7a6d-413e-b4c7-5256350a017a.json"},
{"name": "path68", "value": "/home/mrdine/darkmen/data/ae502579-a5b6-44fd-8fba-1b6a54b06717.json"},
{"name": "path69", "value": "/home/mrdine/darkmen/data/af580ef8-5bf1-49fc-9f85-cf53fac3afb8.json"},
{"name": "path70", "value": "/home/mrdine/darkmen/data/b0b13609-7166-409b-b553-d02388064bbf.json"},
{"name": "path71", "value": "/home/mrdine/darkmen/data/b186ea7e-f174-4401-8fd6-061854d9bdc1.json"},
{"name": "path72", "value": "/home/mrdine/darkmen/data/b2ddb519-334b-4a1e-9e51-319dc367b4bb.json"},
{"name": "path73", "value": "/home/mrdine/darkmen/data/b9453c68-06d0-4c33-a111-4c9abe4b3d10.json"},
{"name": "path74", "value": "/home/mrdine/darkmen/data/bb88cf6f-28e1-4968-abca-04386ec6c506.json"},
{"name": "path75", "value": "/home/mrdine/darkmen/data/bff8fb8a-0af2-4779-93d4-04787a9ece31.json"},
{"name": "path76", "value": "/home/mrdine/darkmen/data/c07ca95d-c96f-4926-a42a-5dcb76637d94.json"},
{"name": "path77", "value": "/home/mrdine/darkmen/data/c0ec3393-9e27-45f3-8852-e3a4037ac191.json"},
{"name": "path78", "value": "/home/mrdine/darkmen/data/c219ab47-093d-4bd5-a06c-36c3c6ed9e6f.json"},
{"name": "path79", "value": "/home/mrdine/darkmen/data/c3470b06-297f-4a96-bddb-9c7edebfaebb.json"},
{"name": "path80", "value": "/home/mrdine/darkmen/data/c35a3e4d-5867-4d0b-8f9b-8783c0c136a7.json"},
{"name": "path81", "value": "/home/mrdine/darkmen/data/c4b6fe42-8e8e-4c1d-8f36-b9f6b13a094e.json"},
{"name": "path82", "value": "/home/mrdine/darkmen/data/c4fec310-2512-457d-ba8a-79de5c3d122c.json"},
{"name": "path83", "value": "/home/mrdine/darkmen/data/c80ebffe-21ca-4f08-abfa-db7e03ce7c62.json"},
{"name": "path84", "value": "/home/mrdine/darkmen/data/cbc2ed0d-017f-4d44-8a67-4cf78ab07062.json"},
{"name": "path85", "value": "/home/mrdine/darkmen/data/d0520667-c128-44e7-9912-413ef84ed45d.json"},
{"name": "path86", "value": "/home/mrdine/darkmen/data/d0732bf8-ccc3-49d8-b6eb-852833d30fca.json"},
{"name": "path87", "value": "/home/mrdine/darkmen/data/d084ada7-43f0-49fb-b410-fe2c9eaa7869.json"},
{"name": "path88", "value": "/home/mrdine/darkmen/data/d5234b3a-687c-4b9d-8399-50f9b02516a2.json"},
{"name": "path89", "value": "/home/mrdine/darkmen/data/d5c7be0d-66fb-48e2-b4ae-00b3dc41c3b3.json"},
{"name": "path90", "value": "/home/mrdine/darkmen/data/de9832dd-f1cb-4276-ad63-ff4f5a078dc5.json"},
{"name": "path91", "value": "/home/mrdine/darkmen/data/df49fe03-5e50-4053-8469-9a73cea045e4.json"},
{"name": "path92", "value": "/home/mrdine/darkmen/data/e09f9bbf-f586-4d2c-b162-87c79cc4617f.json"},
{"name": "path93", "value": "/home/mrdine/darkmen/data/e1e2accd-5626-4475-a258-f8a337b76fd5.json"},
{"name": "path94", "value": "/home/mrdine/darkmen/data/e5644068-7fc7-4f8d-ac1e-6f626d643bfa.json"},
{"name": "path95", "value": "/home/mrdine/darkmen/data/e87caac6-1917-46b8-9636-0535bebec092.json"},
{"name": "path96", "value": "/home/mrdine/darkmen/data/f0c667dd-0020-4c0e-9fff-6aa215843f84.json"},
{"name": "path97", "value": "/home/mrdine/darkmen/data/f1de77bf-e28f-4884-8d18-c16702fd20c3.json"},
{"name": "path98", "value": "/home/mrdine/darkmen/data/f35dadf6-2e1d-422f-941f-ac2744ff3f80.json"},
{"name": "path99", "value": "/home/mrdine/darkmen/data/f846074f-a47e-4ad0-acf4-b1b2a170896e.json"},
{"name": "path100", "value": "/home/mrdine/darkmen/data/f94a8a09-a9d3-460c-9a64-52bbb0a0f3c4.json"},
{"name": "path101", "value": "/home/mrdine/darkmen/data/f9587c93-287b-4ad7-adf7-f50148a14b82.json"},
{"name": "path102", "value": "/home/mrdine/darkmen/data/fa09c786-3299-4179-a631-8fb0d12e9636.json"},
{"name": "path103", "value": "/home/mrdine/darkmen/data/fb43ed1d-26f9-4e44-81cd-f1b02060e4d8.json"}
]

OPENAI_API_KEY = "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"

client=OpenAI()
# Function to read JSON file and return its content
def read_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        print(f"File not found: {filepath}")
        return None

# Loop through the data to read each JSON file
for item in data:
    json_file_path = item["value"]
    json_content = read_json_file(json_file_path)
    
def process_data_with_openai(data_content):
    
    response = client.ChatCompletion.create(
        model="gpt-4o",  # or your desired model
        messages=[
            {"role": "user", "content": data_content}
        ]
    )
    return response['choices'][0]['message']['content']


# Loop through each path and process the JSON files
for entry in data:
    file_path = entry['value']
    if os.path.exists(file_path):
        try:
            content = read_json_file(file_path)
            json_content = json.dumps(content)  # Convert dict to string if needed
            response = process_data_with_openai(json_content)
            print(f"Response from OpenAI for {entry['name']}: {response}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    else:
        print(f"File not found: {file_path}")