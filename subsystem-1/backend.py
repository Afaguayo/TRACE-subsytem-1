from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




# Flask App Setup
app = Flask(__name__)
CORS(app)

# Neo4j Database Connection
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

try:
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    print("✅ Successfully connected to Neo4j database!")
except Exception as e:
    print(f"❌ Failed to connect to Neo4j: {e}")

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Server is running!", "database": "Connected"}), 200

# Create Project
@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    project_id = data.get("project_id")
    lead_analyst = data.get("lead_analyst")

    if not project_id or not lead_analyst:
        return jsonify({"error": "Missing required fields"}), 400

    print(f"🛠 Creating project {project_id} with lead analyst {lead_analyst}")

    with driver.session() as session:
        result = session.write_transaction(create_project_tx, project_id, lead_analyst)

    print(f"✅ Project {project_id} created successfully!")
    return jsonify(result), 201

def create_project_tx(tx, project_id, lead_analyst):
    query = """
    MERGE (p:Project {id: $project_id})
    ON CREATE SET p.lead_analyst = $lead_analyst
    RETURN p.id AS project_id, p.lead_analyst AS lead_analyst
    """
    result = tx.run(query, project_id=project_id, lead_analyst=lead_analyst)
    return result.single()

# List All Projects
@app.route('/list_projects', methods=['GET'])
def list_projects():
    print("📋 Fetching all projects...")

    with driver.session() as session:
        projects = session.read_transaction(list_projects_tx)

    print(f"✅ Found {len(projects)} projects!")
    return jsonify({"projects": projects})

def list_projects_tx(tx):
    query = "MATCH (p:Project) RETURN p.id AS project_id, p.lead_analyst AS lead_analyst"
    result = tx.run(query)
    return [record.data() for record in result]

# Join Project
@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.json
    project_id = data.get("project_id")
    analyst = data.get("analyst")

    if not project_id or not analyst:
        return jsonify({"error": "Missing required fields"}), 400

    print(f"🔗 Analyst {analyst} joining project {project_id}")

    with driver.session() as session:
        result = session.write_transaction(join_project_tx, project_id, analyst)

    print(f"✅ {analyst} successfully joined project {project_id}!")
    return jsonify(result), 200

def join_project_tx(tx, project_id, analyst):
    query = """
    MATCH (p:Project {id: $project_id})
    MERGE (a:Analyst {name: $analyst})
    MERGE (a)-[:WORKS_ON]->(p)
    RETURN a.name AS analyst, p.id AS project_id
    """
    result = tx.run(query, project_id=project_id, analyst=analyst)
    return result.single()

# Function to insert a test object
def insert_test_project():
    test_project_id = "test_project_001"
    test_lead_analyst = "test_lead"

    print(f"🛠 Inserting test project {test_project_id} into the database...")

    with driver.session() as session:
        session.write_transaction(create_project_tx, test_project_id, test_lead_analyst)

    print(f"✅ Test project {test_project_id} successfully inserted!")

if __name__ == '__main__':
    print("🚀 Starting Flask server...")

    # Insert a test project on startup
    #insert_test_project() this is a test function to see if everything worked do not uncomment unless you need to debug

    app.run(debug=True)
