# Flask dependencies
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# LangChain Dependencies
from langchain_ollama.chat_models import ChatOllama

# Python Dependency
import os
import time

# Local Dependency
from tool_registry import ToolRegistry
# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# Setup Flask App
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

tool_registry = ToolRegistry()

print(tool_registry.get_tools())
# Initialize Ollama model
model = ChatOllama(
    model="llama3.2", 
    base_url="http://192.168.2.17:11434",
    verbose=True,
    temperature=0
).bind_tools(list(tool_registry.get_tools().values()))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.form.get('message', '')
        files = request.files.getlist('files')
        
        # Handle file uploads
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files.append(filepath)

        # Prepare the context with files if present
        context = message
        if uploaded_files:
            context += "\n\nAttached files: " + ", ".join(uploaded_files)

        # Create messages for the model
        messages = [
            ("system", "You are a helpful AI assistant that can process text and analyze uploaded files."),
            ("human", context)
        ]

        # Get response from model
        response = model.invoke(messages)

        # Process tool calls
        for tool_call in response.tool_calls:
            print(tool_call)
            selected_tool = tool_registry.get_tools()[tool_call["name"]]
            tool_message =  selected_tool.invoke(tool_call)
            messages.append(tool_message)

        response = model.invoke(messages)
        return jsonify({
            'response': str(response.content),
            'files_processed': len(uploaded_files)
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)