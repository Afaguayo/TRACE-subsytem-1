<script lang="ts">
    import { ProxyServer, HTTPClient } from '../../lib/ProxyServer';

    let proxyServer = new ProxyServer();
    let httpClient = new HTTPClient(proxyServer);
    
    let requestUrl = '';
    let response = '';
    let history = { requests: [], responses: [] };
    let loading = false;

    async function sendRequest() {
        loading = true;
        response = await httpClient.sendRequestToProxy(requestUrl);
        history = proxyServer.getHistory();
        loading = false;
    }
</script>

<main>
    <h1>HTTP Proxy Client</h1>

    <input bind:value={requestUrl} placeholder="Enter URL (e.g., https://example.com)" />
    <button on:click={sendRequest} disabled={loading}>
        {loading ? "Loading..." : "Send Request"}
    </button>

    {#if response}
        <h2>Response</h2>
        {#if response.startsWith("{") || response.startsWith("[")}
            <pre>{response}</pre> <!-- JSON is formatted -->
        {:else}
            {@html response} <!-- HTML content is displayed -->
        {/if}
    {/if}

    <h2>Request History</h2>
    <ul>
        {#each history.requests as req, i}
            <li>{i + 1}: {req}</li>
        {/each}
    </ul>

    <h2>Response History</h2>
    <ul>
        {#each history.responses as res, i}
            <li>{i + 1}: {res}</li>
        {/each}
    </ul>
</main>

<style>
    input {
        width: 400px;
        padding: 5px;
        margin-right: 10px;
    }
    button {
        padding: 5px 10px;
    }
    h2 {
        margin-top: 20px;
    }
    pre {
        background: #f4f4f4;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
    }
</style>