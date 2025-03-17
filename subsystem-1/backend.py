from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for projects and users (Replace with a database in production)
projects = {}
users = {
    "lead_analyst": {"role": "lead", "projects": []},
    "analyst": {"role": "analyst", "projects": []}
}

@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    project_id = data.get("project_id")
    lead_analyst = data.get("lead_analyst")
    
    if not project_id or not lead_analyst:
        return jsonify({"error": "Missing required fields"}), 400
    
    if project_id in projects:
        return jsonify({"error": "Project ID already exists"}), 400
    
    projects[project_id] = {
        "id": project_id,
        "lead_analyst": lead_analyst,
        "clients": []
    }
    users["lead_analyst"]["projects"].append(project_id)
    
    return jsonify({"message": "Project created successfully", "project": projects[project_id]}), 201

@app.route('/list_projects', methods=['GET'])
def list_projects():
    return jsonify({"projects": list(projects.values())})

@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.json
    project_id = data.get("project_id")
    analyst = data.get("analyst")
    
    if project_id not in projects:
        return jsonify({"error": "Project not found"}), 404
    
    projects[project_id]["clients"].append(analyst)
    users["analyst"]["projects"].append(project_id)
    
    return jsonify({"message": "Joined project successfully", "project": projects[project_id]}), 200

if __name__ == '__main__':
    app.run(debug=True)
