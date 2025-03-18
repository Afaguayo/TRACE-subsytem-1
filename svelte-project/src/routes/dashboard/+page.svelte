<script>
    import { onMount } from "svelte";
   
  
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
  
    // Create New Project
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
  
    // Confirm Delete Project
    function confirmDelete(projectId) {
      projectToDelete = projectId;
      showDeletePrompt = true;
    }
  
    // Delete Project
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
  
    onMount(() => {
      const savedUser = localStorage.getItem("user");
      if (savedUser) {
        user = JSON.parse(savedUser);
        fetchProjects();
      }
    });
  </script>
  
  <style>
    .container { padding: 20px; }
    .login, .projects, .create-project { margin-top: 20px; }
    button { margin-top: 10px; }
    .project { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
    .lead { font-weight: bold; color: #1e90ff; }
    .delete-button { color: red; cursor: pointer; margin-left: 10px; }
    .modal { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border-radius: 5px; box-shadow: 0px 0px 10px #00000050; }
    .modal button { margin: 10px; }
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
      <p>Welcome, {user.initials} ({user.role})!</p>
      <button on:click={logout}>Logout</button>
  
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
            <p class="lead">
              📌 {project.project_id} (Lead: {project.lead_analyst}) 
              {#if user.role === "Lead" && user.initials === project.lead_analyst}
                <span class="delete-button" on:click={() => confirmDelete(project.project_id)}>🗑 Delete</span>
              {/if}
            </p>
            {#each project.regular_analysts as analyst}
              <p>👤 {analyst} (Regular Analyst)</p>
            {/each}
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
  