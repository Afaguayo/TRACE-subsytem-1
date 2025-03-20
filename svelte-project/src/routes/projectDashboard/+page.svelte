<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    
    let projectId = "";
    
    // Read the projectId from the URL query parameters when the page loads
    onMount(() => {
      const urlParams = new URLSearchParams($page.url.search);
      projectId = urlParams.get("projectId") || "Unknown";
    });
    
    // Navigate to the Webtree page, carrying the projectId as a query parameter
    function navigateToWebtree() {
      goto(`/webtree?projectId=${projectId}`);
    }

    function navigateToProjects() {
      goto(`/dashboard`);
    }
  </script>
  
  <style>
.dashboard {
  padding: 40px;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
button {
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  background-color: #1e90ff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}
button:hover {
  background-color: #0d6efd;  
}
.button-back {
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  background-color: #d61515;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}
.button-back:hover {
  background-color: #c93939;
}
  </style>
  
  <div class="dashboard">
    <h1>Project Dashboard</h1>
    <p>Project ID: {projectId}</p>
    
    <!-- Webtree button navigates to the new webtree page -->
    <button on:click={navigateToWebtree}>Webtree</button>
    <button on:click={navigateToProjects} class="button-back">Projects</button>
    <!-- Add additional project dashboard functionality here -->
  </div>
  