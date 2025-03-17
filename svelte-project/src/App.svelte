<script>
	import { onMount } from 'svelte';
	import { projects, fetchProjects, createProject, joinProject } from './stores/projects.js';
  
	let newProjectId = '';
	let leadAnalyst = '';
	let joinProjectId = '';
	let analyst = '';
  
	onMount(fetchProjects);
  
	async function handleCreateProject() {
	  if (!newProjectId || !leadAnalyst) return;
	  await createProject(newProjectId, leadAnalyst);
	  newProjectId = '';
	  leadAnalyst = '';
	}
  
	async function handleJoinProject() {
	  if (!joinProjectId || !analyst) return;
	  await joinProject(joinProjectId, analyst);
	  joinProjectId = '';
	  analyst = '';
	}
  </script>
  
  <main>
	<h1>Project Management</h1>
  
	<section>
	  <h2>All Projects</h2>
	  <button on:click={fetchProjects}>Refresh</button>
	  <ul>
		{#each $projects as project}
		  <li>
			<strong>{project.id}</strong> - Lead: {project.lead_analyst}
			<p>Clients: {project.clients.length ? project.clients.join(', ') : 'None'}</p>
		  </li>
		{/each}
	  </ul>
	</section>
  
	<section>
	  <h2>Create a New Project</h2>
	  <input type="text" bind:value={newProjectId} placeholder="Project ID" />
	  <input type="text" bind:value={leadAnalyst} placeholder="Lead Analyst" />
	  <button on:click={handleCreateProject}>Create Project</button>
	</section>
  
	<section>
	  <h2>Join a Project</h2>
	  <input type="text" bind:value={joinProjectId} placeholder="Project ID" />
	  <input type="text" bind:value={analyst} placeholder="Your Name" />
	  <button on:click={handleJoinProject}>Join Project</button>
	</section>
  </main>
  
  <style>
	main {
	  max-width: 600px;
	  margin: auto;
	  font-family: Arial, sans-serif;
	}
	section {
	  margin-bottom: 20px;
	}
	input {
	  display: block;
	  margin: 5px 0;
	  padding: 8px;
	}
	button {
	  padding: 8px;
	  background: blue;
	  color: white;
	  border: none;
	  cursor: pointer;
	}
	button:hover {
	  background: darkblue;
	}
  </style>
  