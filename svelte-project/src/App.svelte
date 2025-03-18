<script>
	import { onMount } from "svelte";
	let projects = [];
  
	async function fetchProjects() {
	  const response = await fetch("http://localhost:5001/list_projects");
	  const data = await response.json();
	  projects = data.projects;
	}
  
	onMount(fetchProjects);
  </script>
  
  <style>
	.tree-container {
	  padding: 20px;
	}
	.project {
	  margin-bottom: 20px;
	  border: 1px solid #ddd;
	  padding: 10px;
	  border-radius: 5px;
	  background-color: #f9f9f9;
	}
	.lead {
	  font-weight: bold;
	  color: #1e90ff;
	}
	.analyst {
	  margin-left: 20px;
	  color: #555;
	}
  </style>
  
  <div class="tree-container">
	{#each projects as project}
	  <div class="project">
		<p class="lead">📌 {project.project_id} (Lead: {project.lead_analyst})</p>
		{#each project.regular_analysts as analyst}
		  <p class="analyst">👤 {analyst} (Regular Analyst)</p>
		{/each}
	  </div>
	{/each}
  </div>
  