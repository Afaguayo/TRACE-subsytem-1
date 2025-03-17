import { writable } from 'svelte/store';

export const projects = writable([]);

export async function fetchProjects() {
    const res = await fetch('http://localhost:5000/list_projects');
    const data = await res.json();
    projects.set(data.projects);
}

export async function createProject(projectId, leadAnalyst) {
    const res = await fetch('http://localhost:5000/create_project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ project_id: projectId, lead_analyst: leadAnalyst })
    });
    return await res.json();
}

export async function joinProject(projectId, analyst) {
    const res = await fetch('http://localhost:5000/join_project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ project_id: projectId, analyst })
    });
    return await res.json();
}

// Svelte Component for a Blank Page
export default function BlankPage() {
    return `<div style='display: flex; justify-content: center; align-items: center; height: 100vh;'>
                <h1>Welcome to TRACE</h1>
            </div>`;
}