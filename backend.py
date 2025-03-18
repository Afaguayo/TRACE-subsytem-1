from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
import os
import atexit
from dotenv import load_dotenv

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

# Create Project (Lead Analyst Only)
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


# Join Project (Regular Analyst)
@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.json
    project_id = data.get("project_id")
    analyst = data.get("analyst")

    if not project_id or not analyst:
        return jsonify({"error": "Missing required fields"}), 400

    print(f"🔗 Analyst {analyst} joining project {project_id}")

    try:
        with driver.session() as session:
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

# List All Projects with Analysts
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
    RETURN p.id AS project_id, l.name AS lead_analyst, COLLECT(a.name) AS regular_analysts
    """
    result = tx.run(query)
    return [record.data() for record in result]

# Start Flask Server
if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True, port=5001)
