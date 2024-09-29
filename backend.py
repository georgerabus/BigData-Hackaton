from flask import Flask, request, jsonify, render_template, send_from_directory
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
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def chunk_messages(content, max_length=4000):
    chunks = []
    current_chunk = ""

    for message in content.split(" "):
        if len(current_chunk) + len(message) + 1 > max_length:  # +1 for space
            chunks.append(current_chunk)
            current_chunk = message
        else:
            current_chunk += " " + message if current_chunk else message
    
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def build_prompt(options):
    # Use a simple prompt for initial analysis
    prompts = {
        "Basic Statistics": "Please extract basic statistics from the conversation like number of conversations, lengths, frequency, etc.",
        "Emotional Patterns": "Identify emotional patterns such as user sentiment, satisfaction, and frustration from the conversation.",
        "Trends of Interest": "Identify trends and frequently asked questions from the conversation.",
        "Hallucination Detection": "Detect instances of hallucination in chatbot responses.",
        "all": "Please extract basic statistics from the conversation like number of conversations, lengths, frequency, etc, Identify emotional patterns such as user sentiment, satisfaction, and frustration from the conversation, Identify trends and frequently asked questions from the conversation and see if there are any hallucinations."
    }

    selected_prompts = [prompts[option] for option in options if option in prompts]
    return " ".join(selected_prompts) if selected_prompts else "Generate a basic summary of the data."

@app.route('/api/read_files', methods=['POST'])
def read_files():
    data = request.get_json()
    selected_files = data.get('files', [])
    selected_options = data.get('options', [])

    combined_content = []  # To hold content from all selected files

    for filename in selected_files:
        try:
            file_path = os.path.join('data', filename)
            content = read_json_file(file_path)  # Read the JSON content from each file
            if content is not None:
                combined_content.append({
                    "filename": filename,
                    "content": content
                })  # Add content along with the filename for context
            else:
                print(f"Failed to read content from: {filename}")
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")

    if combined_content:
        # Combine all content into a single string (JSON serialized) and chunk it
        json_content = json.dumps([item['content'] for item in combined_content])
        chunks = chunk_data(json_content, chunk_size=20000)

        responses = []  # To hold OpenAI responses
        threads = []

        # Build the OpenAI prompt based on the selected options
        prompt = build_prompt(selected_options)

        # Process each chunk in a separate thread
        for chunk in chunks:
            thread = threading.Thread(target=lambda c=chunk: responses.append(process_data_with_openai(c, prompt)))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Combine all the OpenAI responses into a final aggregated result
        final_statistics = process_data_with_openai(" ".join(responses), prompt, is_final_call=True)

        # Generate a human-readable report without JSON content
        formatted_report = generate_human_readable_report(combined_content, final_statistics, selected_options)

        # Save the formatted report as a text file or PDF
        report_filename = 'combined_report.txt'
        report_path = os.path.join('reports', report_filename)
        os.makedirs('reports', exist_ok=True)

        with open(report_path, 'w') as report_file:
            report_file.write(formatted_report)

        # Return the report URL to the frontend for download
        report_url = f"/api/download_report/{report_filename}"
        return jsonify({"response": formatted_report, "reportUrl": report_url})

    return jsonify({"response": "No valid files selected."})

def generate_human_readable_report(files_data, statistics, options):
    """Generate a human-readable report in plain text format without JSON content."""
    report = []

    report.append("=== Combined Report ===\n\n")

    # Loop through each file's data and append the report for it
    for idx, file_data in enumerate(files_data):
        filename = file_data['filename']
        
        report.append(f"==== Report for {filename} ====\n")
        report.append("File Content Summary:\n")

        # Create a descriptive summary of the content without showing JSON
        content_summary = f"The file contains {len(file_data['content'])} entries with various topics discussed."
        report.append(content_summary + "\n")

        report.append("\nSelected Options:\n")
        for option in options:
            report.append(f"- {option}\n")

        report.append("--- Analysis Results ---\n")
        report.append(f"{statistics}\n")  # Use the aggregated statistics directly

        # Add a separator between reports
        report.append("\n==================================================\n\n")

    # Return the final stacked and formatted report
    return "".join(report)

def read_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        print(f"File not found: {filepath}")
        return None

def process_data_with_openai(data_content, prompt, is_final_call=False):
    try:
        # Check if we are generating the final report
        if is_final_call:
            prompt = "Create a detailed, plain text report based on the following data:"

        message_chunks = chunk_messages(data_content)

        responses = []
        for message_chunk in message_chunks:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt} {message_chunk}"}
                ]
            )
            response_message = completion.choices[0].message.content.strip()
            responses.append(response_message)

        final_response = " ".join(responses)
        return final_response

    except Exception as e:
        print(f"Error while calling OpenAI API: {e}")
        return None

@app.route('/api/download_report/<filename>', methods=['GET'])
def download_report(filename):
    return send_from_directory('reports', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
