from flask import Flask, request, jsonify, render_template
import os
import json
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI()

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

@app.route('/api/files', methods=['GET'])
def get_files():
    # List files in the 'data' directory
    files = os.listdir('data')
    return jsonify(files)

@app.route('/api/read_files', methods=['POST'])
def read_files():
    data = request.get_json()
    selected_files = data.get('files', [])
    
    combined_content = []
    
    for filename in selected_files:
        try:
            # Construct the file path
            file_path = os.path.join('data', filename)  # Adjust the path as necessary
            content = read_json_file(file_path)
            if content is not None:
                combined_content.append(content)  # Append content to the list
            else:
                print(f"Failed to read content from: {filename}")  # Debug log
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")  # Capture any errors
    
    # Send the combined content to OpenAI
    if combined_content:
        json_content = json.dumps(combined_content)  # Convert list of dicts to JSON string
        print(f"Sending the following JSON to OpenAI: {json_content}")  # Debug log
        response_content = process_data_with_openai(json_content)
        return jsonify({"response": response_content if response_content else "No response from OpenAI."})
    
    return jsonify({"response": "No valid files selected."})


# Function to read JSON file and return its content
def read_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        print(f"File not found: {filepath}")
        return None

# Function to process data with OpenAI
def process_data_with_openai(data_content):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  # Specify your desired model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a general statistics about user hapiness: {data_content}"}
            ]
        )
        response_message = completion.choices[0].message.content  # Corrected line
        print(f"OpenAI Response: {response_message}")  # Log response for debugging
        return response_message  # Return the response content
    except Exception as e:
        print(f"Error while calling OpenAI API: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
