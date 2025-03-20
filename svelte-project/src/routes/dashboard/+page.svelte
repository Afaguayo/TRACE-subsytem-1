<script>
  import { onMount } from "svelte";
  import { goto } from '$app/navigation'; // SvelteKit navigation function
  
  let initials = "";
  let isLead = false;
  let user = null;
  let projects = [];
  let newProjectId = "";
  let showDeletePrompt = false;
  let projectToDelete = null;
  
  // Login Function
  async function login() {
    const response = await fetch("http://localhost:5001/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initials, is_lead: isLead }),
    });
  
    if (response.ok) {
      user = await response.json();
      localStorage.setItem("user", JSON.stringify(user));
      fetchProjects();
    }
  }
  
  // Logout Function
  function logout() {
    user = null;
    projects = [];
    localStorage.removeItem("user");
  }
  
  // Fetch Projects
  async function fetchProjects() {
    const response = await fetch("http://localhost:5001/list_projects");
    if (response.ok) {
      const data = await response.json();
      projects = data.projects;
    }
  }
  
  // Create New Project (Lead Only)
  async function createProject() {
    if (!newProjectId.trim()) return;
  
    const response = await fetch("http://localhost:5001/create_project", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: newProjectId, lead_analyst: user.initials }),
    });
  
    if (response.ok) {
      newProjectId = "";
      fetchProjects();
    }
  }
  
  // Join Project (for analysts who are not yet members)
  async function joinProject(projectId) {
    const response = await fetch("http://localhost:5001/join_project", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: projectId, analyst: user.initials }),
    });
    if (response.ok) {
      fetchProjects();
    }
  }
  
  // Leave Project (for non-lead analysts)
  async function leaveProject(projectId) {
    const response = await fetch("http://localhost:5001/leave_project", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: projectId, analyst: user.initials }),
    });
    if (response.ok) {
      fetchProjects();
    }
  }
  
  // Open Project – redirect to the projectDashboard page with the project ID as a query parameter
  function openProject(projectId) {
    goto(`/projectDashboard?projectId=${projectId}`);
  }
  
  // Lock Project (Lead Only)
  async function lockProject(projectId) {
    const response = await fetch("http://localhost:5001/lock_project", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: projectId, lead_analyst: user.initials }),
    });
    if (response.ok) {
      fetchProjects();
    }
  }
  
  // Unlock Project (Lead Only)
  async function unlockProject(projectId) {
    const response = await fetch("http://localhost:5001/unlock_project", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: projectId, lead_analyst: user.initials }),
    });
    if (response.ok) {
      fetchProjects();
    }
  }
  
  // Confirm Delete Project
  function confirmDelete(projectId) {
    projectToDelete = projectId;
    showDeletePrompt = true;
  }
  
  // Delete Project (Lead Only)
  async function deleteProject() {
    if (!projectToDelete) return;
  
    const response = await fetch("http://localhost:5001/delete_project", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: projectToDelete, lead_analyst: user.initials }),
    });
  
    if (response.ok) {
      showDeletePrompt = false;
      projectToDelete = null;
      fetchProjects();
    }
  }
  
  // Cancel Delete Project
  function cancelDelete() {
    showDeletePrompt = false;
    projectToDelete = null;
  }
  
  // Helper: Check if the user is already a member of the project
  function isMember(project) {
    const userInitial = user.initials.toLowerCase();
    const lead = project.lead_analyst.toLowerCase();
    const regulars = project.regular_analysts.map(a => a.toLowerCase());
    return userInitial === lead || regulars.includes(userInitial);
  }
  
  onMount(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      user = JSON.parse(savedUser);
      fetchProjects();
    }
  });
</script>
  
<style>
  .container {
    padding: 40px;
    max-width: 800px;
    margin: 0 auto;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  }
  .login, .projects, .create-project {
    margin-top: 30px;
    background: #f7f7f7;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  .login input, .create-project input {
    padding: 10px;
    font-size: 16px;
    margin-right: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  button {
    padding: 10px 15px;
    font-size: 16px;
    border: none;
    background-color: #1e90ff;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  button:hover {
    background-color: #0d6efd;
  }
  .project {
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #fff;
  }
  .project-info {
    flex-grow: 1;
  }
  .project-actions {
    display: flex;
    gap: 10px;
  }
  .lead {
    font-weight: bold;
    color: #1e90ff;
  }
  .delete-button, .lock-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-size: 16px;
  }
  .delete-button {
    color: red;
  }
  .lock-button {
    color: #555;
  }
  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    z-index: 100;
  }
  .modal button {
    margin: 10px;
  }
  .locked-status {
    font-size: 14px;
    color: #d9534f;
    margin-left: 10px;
  }
  .button-logout {
    padding: 10px 15px;
    font-size: 16px;
    border: none;
    background-color: #d61515;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 20px;
  }
  .button-logout:hover {
    background-color: #c93939;
  }
</style>
  
<div class="container">
  {#if !user}
    <!-- Login Form -->
    <div class="login">
      <h2>🔑 Login</h2>
      <input type="text" bind:value={initials} placeholder="Enter Initials" />
      <label>
        <input type="checkbox" bind:checked={isLead} />
        Lead Analyst?
      </label>
      <button on:click={login}>Login</button>
    </div>
  {:else}
    <!-- User Info & Logout -->
    <p>Welcome, <span class="lead">{user.initials}</span> ({user.role})!</p>
    <button on:click={logout} class="button-logout">Logout</button>
  
    <!-- Project Creation (Only for Lead Analysts) -->
    {#if user.role === "Lead"}
      <div class="create-project">
        <h3>Create a New Project</h3>
        <input type="text" bind:value={newProjectId} placeholder="Project ID" />
        <button on:click={createProject}>Create Project</button>
      </div>
    {/if}
  
    <!-- Project List -->
    <div class="projects">
      <h2>📋 Projects</h2>
      {#each projects as project}
        <div class="project">
          <div class="project-info">
            <p class="lead">
              📌 {project.project_id} (Lead: {project.lead_analyst})
              {#if project.locked}
                <span class="locked-status">🔒 Locked</span>
              {/if}
            </p>
            {#each project.regular_analysts as analyst}
              <p>👤 {analyst} (Regular Analyst)</p>
            {/each}
          </div>
          <div class="project-actions">
            {#if project.locked}
              <!-- For locked projects, only leads get an unlock option -->
              {#if user.role === "Lead"}
                <button class="lock-button" on:click={() => unlockProject(project.project_id)}>Unlock</button>
              {/if}
            {:else}
              {#if isMember(project)}
                <button on:click={() => openProject(project.project_id)}>Open</button>
                {#if user.role !== "Lead"}
                  <button on:click={() => leaveProject(project.project_id)}>Leave</button>
                {/if}
              {:else}
                <button on:click={() => joinProject(project.project_id)}>Join</button>
              {/if}
              {#if user.role === "Lead"}
                <button class="lock-button" on:click={() => lockProject(project.project_id)}>Lock</button>
                <button class="delete-button" on:click={() => confirmDelete(project.project_id)}>🗑 Delete</button>
              {/if}
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
  
  <!-- Delete Confirmation Modal -->
  {#if showDeletePrompt}
    <div class="modal">
      <p>Are you sure you want to delete this project?</p>
      <button on:click={deleteProject}>Yes</button>
      <button on:click={cancelDelete}>No</button>
    </div>
  {/if}
</div>
