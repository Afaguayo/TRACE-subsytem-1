<script>
    import { onMount } from "svelte";

    let projects = [];
    let analystName = "";
    let selectedProject = "";

    async function fetchProjects() {
        try {
            const response = await fetch("/list_projects");
            const data = await response.json();
            projects = data.projects;
        } catch (error) {
            console.error("Error fetching projects:", error);
        }
    }

    async function joinProject() {
        if (!analystName || !selectedProject) {
            alert("Please enter your initials and select a project.");
            return;
        }

        try {
            const response = await fetch("/join_project", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ project_id: selectedProject, analyst: analystName }),
            });

            if (response.ok) {
                alert(`Successfully joined project: ${selectedProject}`);
                fetchProjects();
            } else {
                alert("Failed to join project.");
            }
        } catch (error) {
            console.error("Error joining project:", error);
        }
    }

    onMount(fetchProjects);
</script>

<h1> Regular Analyst Dashboard</h1>

<label>
    Your Initials:
    <input type="text" bind:value={analystName} placeholder="Enter your initials" />
</label>

<label>
    Select Project:
    <select bind:value={selectedProject}>
        <option value="" disabled selected>Select a project</option>
        {#each projects as project}
            <option value={project.project_id}>{project.project_id} - {project.lead_analyst}</option>
        {/each}
    </select>
</label>

<button on:click={joinProject}>Join</button>
