<script>
    import { onMount } from 'svelte';
    import { Network } from 'vis-network';
    import { DataSet } from 'vis-data';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
  
    let treeData = {}; 
    let container; 
    let projectId = "";
    
    onMount(() => {
      const urlParams = new URLSearchParams($page.url.search);
      projectId = urlParams.get("projectId") || "Unknown";
    });
  
    async function fetchTree() {
        try {
            console.log("Fetching tree data...");
            const response = await fetch("http://127.0.0.1:5001/api/tree", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    urls: [
                        "https://example.com/",
                        "https://example.com/about.html",
                        "https://example.com/subdir/post1",
                        "https://example.com/subdir/post2",
                        "https://example.com/subdir/subdir2/post1"
                    ]
                })
            });
  
            treeData = await response.json();
            console.log("Tree Data:", treeData);
  
            const rootDomain = extractDomain("https://example.com/");
            createGraph(treeData, rootDomain);
        } catch (error) {
            console.error("Error fetching tree:", error);
        }
    }
  
    function extractDomain(url) {
        return new URL(url).hostname; // Extracts "example.com"
    }
  
    function createGraph(data, rootDomain) {
        if (!container) {
            console.error("Container not found!");
            return;
        }
  
        let nodes = [];
        let edges = [];
        let nodeId = 1;
        let nodeMap = { "index": nodeId }; 
  
        function processTree(obj, parentId) {
            Object.entries(obj).forEach(([key, value]) => {
                const id = ++nodeId;
                nodeMap[key] = id;
                nodes.push({ id, label: key });
  
                if (parentId !== null) {
                    edges.push({ from: parentId, to: id });
                }
  
                if (typeof value === "object" && Object.keys(value).length > 0) {
                    processTree(value, id);
                }
            });
        }
  
        // Set the root node to the domain name
        nodes.push({ id: 1, label: rootDomain });
        processTree(data, 1);
  
        const networkData = {
            nodes: new DataSet(nodes),
            edges: new DataSet(edges),
        };
  
        const options = {
            layout: {
                hierarchical: {
                    direction: "UD", 
                    sortMethod: "directed",
                }
            },
            physics: false,
        };
  
        new Network(container, networkData, options);
    }
  
    onMount(fetchTree);

    function navigateToDashboard() {
      goto(`/projectDashboard?projectId=${projectId}`);
    }
</script>
<style>
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

  <h1>Tree Graph</h1>
  <!-- <p>Project ID: {projectId}</p> -->
  <div id="tree-graph" bind:this={container} style="width: 100%; height: 500px; border: 1px solid black;"></div>
  <button on:click={navigateToDashboard} class="button-back"> Dashboard </button>


  