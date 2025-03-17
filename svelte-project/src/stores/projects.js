import { writable } from 'svelte/store';

export const projects = writable([]);



export async function fetchProjects() {
    try {
        const res = await fetch('http://localhost:5000/list_projects');
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        const data = await res.json();
        projects.set(data.projects);
    } catch (error) {
        console.error('Error fetching projects:', error);
    }
}


export async function createProject(projectId, leadAnalyst) {
    try {
        const res = await fetch('http://localhost:5000/create_project', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: projectId, lead_analyst: leadAnalyst })
        });

        await res.json();
        fetchProjects(); // Refresh list after creation
    } catch (error) {
        console.error('Error creating project:', error);
    }
}

export async function joinProject(projectId, analyst) {
    try {
        const res = await fetch('http://localhost:5000/join_project', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: projectId, analyst })
        });

        await res.json();
        fetchProjects(); // Refresh list after joining
    } catch (error) {
        console.error('Error joining project:', error);
    }
}

