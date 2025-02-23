from flask import Flask, request, jsonify, Response, session, make_response
from werkzeug.utils import secure_filename
import os
import json
import uuid
from flask_cors import CORS
from flask import request, jsonify
from db_manager import DBManager

#Local Imports
from ingest import condensed_metadata, initialize_vector_store, ingest_file, return_chunk_by_id, return_documents_summary, search_documents_with_score
from quiz import create_quiz
from roadmap import create_roadmap
from chat_with_chunk import chat_with_chunk
from chat import chat_with_docs

# Initialize database manager
db_manager = DBManager()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')  # Set a secret key for sessions
CORS(app, supports_credentials=True)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

def sanitize_collection_name(name):
    """Sanitize the collection name to meet Chroma requirements."""
    import re
    # Remove any characters that aren't alphanumeric, underscore, or hyphen
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    # Replace consecutive underscores with a single one
    sanitized = re.sub(r'_+', '_', sanitized)
    # Ensure it starts and ends with alphanumeric
    sanitized = re.sub(r'^[^a-zA-Z0-9]+', '', sanitized)
    sanitized = re.sub(r'[^a-zA-Z0-9]+$', '', sanitized)
    # Limit length to 63 characters
    sanitized = sanitized[:63]
    # Ensure minimum length of 3 characters by padding if necessary
    while len(sanitized) < 3:
        sanitized += '0'
    return sanitized

@app.route('/ingest', methods=['POST'])
def ingest_file_endpoint():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    print(file.filename)
    # Check if the file is empty
    if file.filename == '':
        return jsonify({"error": "Empty file provided"}), 400
    
    # Validate the file
    if file and allowed_file(file.filename):
        # Generate a unique session ID if not exists

        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        
        # Create user-specific collection name
        filename = secure_filename(file.filename)
        user_collection = sanitize_collection_name(filename)
        
        # Check if file already exists in uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            # If file exists, return success with existing file info
            response = make_response(jsonify({
                "message": "File already exists and has been processed",
                "filename": filename,
                "file_path": file_path,
                "collection_name": user_collection
            }))
            
            # Set cookie with filename and collection name
            response.set_cookie('current_file', filename, samesite='Strict', secure=True)
            response.set_cookie('collection_name', user_collection, samesite='Strict', secure=True)
            
            return response, 200
        
        try:
            # Create a vector store with the user-specific collection name
            vector_store = initialize_vector_store(collection_name=user_collection)
            
            # Save the file
            file.save(file_path)
            
            # Ingest the file with the dedicated vector store
            ingest_file(file_path, vector_store=vector_store)
            
            # Create response with cookie
            response = make_response(jsonify({
                "message": "File uploaded and ingested successfully",
                "filename": filename,
                "file_path": file_path,
                "collection_name": user_collection
            }))
            
            # Set cookie with filename and collection name
            response.set_cookie('current_file', filename, samesite='Strict', secure=True)
            response.set_cookie('collection_name', user_collection, samesite='Strict', secure=True)
            
            return response, 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400



@app.route('/roadmap', methods=['GET'])
def get_roadmap():
    # Get the current file from cookie
    current_filename = request.cookies.get('current_file')
    if not current_filename:
        return jsonify({"error": "No file selected"}), 400

    # Try to get roadmap from database first
    stored_roadmap = db_manager.get_roadmap(current_filename)
    if stored_roadmap:
        return jsonify(stored_roadmap), 200

    try:
        roadmap = create_roadmap(filename=current_filename)
        if roadmap:
            # Store the roadmap in database
            db_manager.store_roadmap(current_filename, roadmap)
            return jsonify(roadmap), 200
        else:
            return jsonify({"error": "Failed to create roadmap"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/quiz', methods=['POST'])
def get_quiz():
    # Get the current file from cookie
    print("Creating Quiz...")
    current_filename = request.cookies.get('current_file')
    if not current_filename:
        return jsonify({"error": "No file selected"}), 400

    # Get the node data from request body
    node_data = request.get_json()
    node_data = node_data.get('node_data')
    # print(type(node_data), node_data)
    if not node_data:
        return jsonify({"error": "No node data provided"}), 400

    try:
        # Try to get quiz from database first
        stored_quiz = db_manager.get_quiz(current_filename, node_data['node_id'])
        if stored_quiz:
            return jsonify(stored_quiz), 200

        # If not in database, create new quiz
        quiz = create_quiz(node_data, current_filename)
        if quiz:
            # Store the quiz in database
            db_manager.store_quiz(current_filename, node_data['node_id'], quiz)
            return jsonify(quiz), 200
        else:
            return jsonify({"error": "Failed to create quiz"}), 500
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/chat-with-chunk', methods=['POST'])
def chat_endpoint():
    # Get the current file from cookie
    current_filename = request.cookies.get('current_file')
    if not current_filename:
        return jsonify({"error": "No file selected"}), 400

    # Get the request data
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "No request data provided"}), 400

    # Extract required fields
    node_data = data.get('node_data')
    user_query = data.get('query')

    if not node_data:
        return jsonify({"error": "No node data provided"}), 400
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Call the chat function from chat_with_chunk
        response = chat_with_chunk(user_query, node_data, current_filename)
        return jsonify({"response": response}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def global_chat_endpoint():
    # Get the current file from cookie
    current_filename = request.cookies.get('current_file')
    if not current_filename:
        return jsonify({"error": "No file selected"}), 400

    # Get the request data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No request data provided"}), 400

    # Extract user query
    user_query = data.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Call the chat function from chat module
        response = chat_with_docs(user_query, collection_name=current_filename)
        print(response)
        return jsonify({"response": response}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)