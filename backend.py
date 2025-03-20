from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
import os
import atexit
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse #Used for parsing URLs for tree graph

# Load environment variables
load_dotenv()

# Flask App Setup
app = Flask(__name__)
CORS(app)

# Validate environment variables
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([URI, USER, PASSWORD]):
    raise ValueError("❌ Missing required Neo4j credentials in environment variables")

# Neo4j Database Connection
try:
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    print("✅ Successfully connected to Neo4j database!")
except Exception as e:
    print(f"❌ Failed to connect to Neo4j: {e}")
    exit(1)

# Ensure driver is closed on exit
@atexit.register
def close_driver():
    if driver:
        driver.close()
        print("🛑 Neo4j driver closed.")

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Server is running!", "database": "Connected"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    initials = data.get("initials")
    is_lead = data.get("is_lead")
    
    if not initials:
        return jsonify({"error": "Initials required"}), 400
    
    role = "Lead" if is_lead else "Regular"
    print(f"🔑 Logging in user {initials} as {role}")
    
    with driver.session() as session:
        session.write_transaction(create_or_update_user, initials, role)
    
    return jsonify({"initials": initials, "role": role}), 200

def create_or_update_user(tx, initials, role):
    query = """
    MERGE (a:Analyst {name: $initials})
    SET a.role = $role
    RETURN a.name AS initials, a.role AS role
    """
    return tx.run(query, initials=initials, role=role).single()

# Create Project (Lead Only)
@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    project_id = data.get("project_id")
    lead_analyst = data.get("lead_analyst")
    
    if not project_id or not lead_analyst:
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"🛠 Creating project {project_id} with lead analyst {lead_analyst}")
    
    try:
        with driver.session() as session:
            result = session.write_transaction(create_project_tx, project_id, lead_analyst)
        print(f"✅ Project {project_id} created successfully!")
        return jsonify(result), 201
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        return jsonify({"error": str(e)}), 500

def create_project_tx(tx, project_id, lead_analyst):
    query = """
    MERGE (p:Project {id: $project_id})
    MERGE (a:Analyst {name: $lead_analyst})
    ON CREATE SET a.role = 'Lead'
    MERGE (a)-[:LEADS]->(p)
    RETURN p.id AS project_id, a.name AS lead_analyst
    """
    result = tx.run(query, project_id=project_id, lead_analyst=lead_analyst)
    return result.single()

# Helper: Check if project is locked
def check_project_locked(tx, project_id):
    query = """
    MATCH (p:Project {id: $project_id})
    RETURN coalesce(p.locked, false) AS locked
    """
    result = tx.run(query, project_id=project_id).single()
    return result["locked"]

# Check if analyst is lead for the project (case-insensitive)
def check_lead_analyst(tx, project_id, lead_analyst):
    query = """
    MATCH (p:Project {id: $project_id})<-[:LEADS]-(a:Analyst)
    WHERE toLower(a.name) = toLower($lead_analyst)
    RETURN COUNT(p) > 0 AS is_lead
    """
    result = tx.run(query, project_id=project_id, lead_analyst=lead_analyst).single()
    return result["is_lead"]

# Delete Project (Lead Only; allowed only if unlocked)
@app.route('/delete_project', methods=['POST'])
def delete_project():
    data = request.json
    project_id = data.get("project_id")
    lead_analyst = data.get("lead_analyst")  # Any lead can perform this action
    
    if not project_id or not lead_analyst:
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"🗑 Attempting to delete project {project_id} by lead {lead_analyst}")
    
    with driver.session() as session:
        locked = session.read_transaction(check_project_locked, project_id)
        if locked:
            return jsonify({"error": "Cannot delete a locked project"}), 403
        session.write_transaction(delete_project_tx, project_id)
    
    print(f"✅ Project {project_id} deleted successfully!")
    return jsonify({"message": f"Project {project_id} deleted"}), 200

def delete_project_tx(tx, project_id):
    query = "MATCH (p:Project {id: $project_id}) DETACH DELETE p"
    tx.run(query, project_id=project_id)

# Lock Project (Lead Only; allowed only if currently unlocked)
@app.route('/lock_project', methods=['POST'])
def lock_project():
    data = request.json
    project_id = data.get("project_id")
    lead_analyst = data.get("lead_analyst")  # Any lead can lock
    
    if not project_id or not lead_analyst:
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"🔒 Attempting to lock project {project_id} by lead {lead_analyst}")
    
    with driver.session() as session:
        locked = session.read_transaction(check_project_locked, project_id)
        if locked:
            return jsonify({"error": "Project is already locked"}), 403
        session.write_transaction(lock_project_tx, project_id)
    
    print(f"✅ Project {project_id} locked successfully!")
    return jsonify({"message": f"Project {project_id} locked"}), 200

def lock_project_tx(tx, project_id):
    query = """
    MATCH (p:Project {id: $project_id})
    SET p.locked = true
    RETURN p.id AS project_id, p.locked AS locked
    """
    result = tx.run(query, project_id=project_id)
    return result.single()

# Unlock Project (Lead Only; allowed only if currently locked)
@app.route('/unlock_project', methods=['POST'])
def unlock_project():
    data = request.json
    project_id = data.get("project_id")
    lead_analyst = data.get("lead_analyst")  # Any lead can unlock
    
    if not project_id or not lead_analyst:
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"🔓 Attempting to unlock project {project_id} by lead {lead_analyst}")
    
    with driver.session() as session:
        locked = session.read_transaction(check_project_locked, project_id)
        if not locked:
            return jsonify({"error": "Project is already unlocked"}), 400
        session.write_transaction(unlock_project_tx, project_id)
    
    print(f"✅ Project {project_id} unlocked successfully!")
    return jsonify({"message": f"Project {project_id} unlocked"}), 200

def unlock_project_tx(tx, project_id):
    query = """
    MATCH (p:Project {id: $project_id})
    SET p.locked = false
    RETURN p.id AS project_id, p.locked AS locked
    """
    result = tx.run(query, project_id=project_id)
    return result.single()

# Join Project (Regular Analyst; cannot join if locked)
@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.json
    project_id = data.get("project_id")
    analyst = data.get("analyst")
    
    if not project_id or not analyst:
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"🔗 Analyst {analyst} joining project {project_id}")
    
    with driver.session() as session:
        locked = session.read_transaction(check_project_locked, project_id)
        if locked:
            return jsonify({"error": "Project is locked, cannot join"}), 403
        try:
            result = session.write_transaction(join_project_tx, project_id, analyst)
            print(f"✅ {analyst} successfully joined project {project_id}!")
            return jsonify(result), 200
        except Exception as e:
            print(f"❌ Error joining project: {e}")
            return jsonify({"error": str(e)}), 500

def join_project_tx(tx, project_id, analyst):
    query = """
    MATCH (p:Project {id: $project_id})
    MERGE (a:Analyst {name: $analyst})
    ON CREATE SET a.role = 'Regular'
    MERGE (a)-[:WORKS_ON]->(p)
    RETURN a.name AS analyst, a.role AS role, p.id AS project_id
    """
    result = tx.run(query, project_id=project_id, analyst=analyst)
    return result.single()

# Leave Project (Regular Analyst only; leads cannot leave)
@app.route('/leave_project', methods=['POST'])
def leave_project():
    data = request.json
    project_id = data.get("project_id")
    analyst = data.get("analyst")
    
    if not project_id or not analyst:
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"🔗 Analyst {analyst} attempting to leave project {project_id}")
    
    with driver.session() as session:
        # Disallow leaving if the analyst is the lead
        is_lead = session.read_transaction(check_lead_analyst, project_id, analyst)
        if is_lead:
            return jsonify({"error": "Lead cannot leave the project"}), 403
        session.write_transaction(leave_project_tx, project_id, analyst)
    
    return jsonify({"message": f"{analyst} left project {project_id}"}), 200

def leave_project_tx(tx, project_id, analyst):
    query = """
    MATCH (p:Project {id: $project_id})<-[r:WORKS_ON]-(a:Analyst {name: $analyst})
    DELETE r
    """
    tx.run(query, project_id=project_id, analyst=analyst)

# List All Projects with Analysts and Lock Status
@app.route('/list_projects', methods=['GET'])
def list_projects():
    print("📋 Fetching all projects with analysts...")
    try:
        with driver.session() as session:
            projects = session.read_transaction(list_projects_tx)
        print(f"✅ Found {len(projects)} projects!")
        return jsonify({"projects": projects})
    except Exception as e:
        print(f"❌ Error fetching projects: {e}")
        return jsonify({"error": str(e)}), 500

def list_projects_tx(tx):
    query = """
    MATCH (p:Project)<-[:LEADS]-(l:Analyst)
    OPTIONAL MATCH (p)<-[:WORKS_ON]-(a:Analyst)
    RETURN p.id AS project_id, l.name AS lead_analyst, p.locked AS locked, COLLECT(a.name) AS regular_analysts
    """
    result = tx.run(query)
    return [record.data() for record in result]

@app.route('/proxy', methods=['GET'])
def proxy_request():
    external_url = request.args.get("url")
    if not external_url:
        return jsonify({"error": "Missing URL parameter"}), 400
    
    try:
        response = requests.get(external_url, headers={"User-Agent": "Mozilla/5.0"})
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Proxy request error: {e}")
        return jsonify({"error": "Failed to fetch data from the requested URL"}), 500
# Tree Graph

def build_tree(urls):
    tree = {}

    for url in urls:
        parsed = urlparse(url)
        print(f"Processing URL: {url}, Path: {parsed.path}")  # Debugging print

        path_parts = parsed.path.strip("/").split("/")
        
        # Handle root path explicitly
        if parsed.path == "/":
            path_parts = ["index"]  # or use "root" instead of "index"
        
        node = tree
        for part in path_parts:
            if part not in node:
                node[part] = {}
            node = node[part]

    return tree


@app.route('/api/tree', methods=['POST'])
def generate_tree():
    print("Raw Data:", request.data)  # Debugging: Print raw request data
    print("Content-Type:", request.content_type)  # Debugging: Print Content-Type
    
    if request.content_type != "application/json":
        return jsonify({"error": "Invalid Content-Type"}), 415

    data = request.get_json()
    print(request.json)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    urls = data.get("urls", [])
    tree = build_tree(urls)
    return jsonify(tree)

# End Tree Graph


if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True, port=5001)
