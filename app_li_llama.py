from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.llms.groq import Groq
from llama_index.core.readers.file.base import SimpleDirectoryReader
from getpass import getpass


# Load environment variables from .env
def load_env_variables():
    if os.path.exists('.env'):
        load_dotenv()
    else:
        print("No .env file found. You can create one to store your API keys. Prompting for keys.")

# Prompt for API keys if not set or empty
def set_api_keys():
    if "GROQ_API_KEY" not in os.environ or not os.environ["GROQ_API_KEY"].strip():
        os.environ["GROQ_API_KEY"] = getpass("Enter your Groq API key: ")
    if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"].strip():
        os.environ["OPENAI_API_KEY"] = getpass("Enter your OpenAI API key: ")

# Initialize environment
def initialize_environment():
    load_env_variables()
    set_api_keys()

# Initialize environment at startup
initialize_environment()

# Initialize Flask app
app = Flask(__name__)
CORS(app)


# Define the index globally
index = None

def load_index():
    global index
    if os.path.exists("./index_data/index.json"):
        storage_context = StorageContext.from_defaults(persist_dir="./index_data")
        index = VectorStoreIndex.from_documents([], storage_context=storage_context)
    else:
        index = None

load_index()

def create_index_from_files(files_directory):
    global index
    documents = SimpleDirectoryReader(files_directory).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir="./index_data")

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('files')
    upload_folder = './uploaded_files'

    if os.path.exists(upload_folder):
        for file in os.listdir(upload_folder):
            os.remove(os.path.join(upload_folder, file))
    else:
        os.makedirs(upload_folder)

    for file in files:
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

    create_index_from_files(upload_folder)
    return jsonify({"message": "Files uploaded and indexed successfully"}), 200

@app.route('/query', methods=['POST'])
def query_data():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({"error": "Query is missing."}), 400

    if not index:
        return jsonify({"error": "No index available. Upload files first."}), 400

    llm = Groq(model="llama3-70b-8192")
    #llm = Groq(model="llama3-3-70b")
    #llm = Groq(model="llama3-2-11b-instruct")
    query_engine = index.as_query_engine(llm=llm)
    response = query_engine.query(query)
    return jsonify({"response": str(response)}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
