from flask import Flask, request, jsonify, render_template
import os
import json
from openai import OpenAI
import threading

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI()

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

@app.route('/api/files', methods=['GET'])
def get_files():
    files = os.listdir('data')
    return jsonify(files)

def chunk_data(data, chunk_size=20000):
    """Divide data into chunks of specified size."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def chunk_messages(content, max_length=4000):  # Adjust max_length as per API limits
    """Split messages into smaller parts based on length."""
    chunks = []
    current_chunk = ""

    for message in content.split(" "):  # Split by space for better chunking
        if len(current_chunk) + len(message) + 1 > max_length:  # +1 for space
            chunks.append(current_chunk)
            current_chunk = message
        else:
            current_chunk += " " + message if current_chunk else message
    
    if current_chunk:  # Append any remaining content
        chunks.append(current_chunk)

    return chunks

@app.route('/api/read_files', methods=['POST'])
def read_files():
    data = request.get_json()
    selected_files = data.get('files', [])
    
    combined_content = []
    
    for filename in selected_files:
        try:
            file_path = os.path.join('data', filename)
            content = read_json_file(file_path)
            if content is not None:
                combined_content.append(content)
            else:
                print(f"Failed to read content from: {filename}")
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")
    
    if combined_content:
        # Combine all content into a string and chunk it
        json_content = json.dumps(combined_content)
        chunks = chunk_data(json_content, chunk_size=20000)  # Adjust size as needed

        responses = []
        threads = []

        # Process each chunk in a separate thread
        for chunk in chunks:
            thread = threading.Thread(target=lambda c=chunk: responses.append(process_data_with_openai(c)))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()  # Wait for all threads to finish

        # Aggregate responses
        final_statistics = process_data_with_openai(" ".join(responses), is_final_call=True)
        return jsonify({"response": final_statistics})
    
    return jsonify({"response": "No valid files selected."})


def read_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        print(f"File not found: {filepath}")
        return None

def process_data_with_openai(data_content, is_final_call=False):
    try:
        prompt = "Generate a general statistics about user happiness: " if not is_final_call else "Generate a general summary based on the following responses: "
        message_chunks = chunk_messages(data_content)

        responses = []
        for message_chunk in message_chunks:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}{message_chunk}"}
                ]
            )
            response_message = completion.choices[0].message.content
            responses.append(response_message)

        final_response = " ".join(responses)
        print(f"OpenAI Response: {final_response}")  # Log response for debugging
        return final_response

    except Exception as e:
        print(f"Error while calling OpenAI API: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
