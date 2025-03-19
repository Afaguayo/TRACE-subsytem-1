<script lang="ts">
    //Gets classes for ProxyServer and HTTPClients from lib
    import { ProxyServer, HTTPClient } from '../../lib/ProxyServer';

    let proxyServer = new ProxyServer();
    let httpClient = new HTTPClient(proxyServer);
    
    let requestUrl = '';
    let response = '';

    // TODO: Replace storing into Request and ResponseManager
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

    <input bind:value={requestUrl} placeholder="Enter URL (ex: https://test.com)" />
    <button on:click={sendRequest} disabled={loading}>
        {loading ? "Loading..." : "Send Request"}
    </button>

    <!-- Determines if we're getting a JSON or HTTP Format -->
    {#if response}
        <h2>Response</h2>
        {#if response.startsWith("{") || response.startsWith("[")}
            <pre>{response}</pre> <!-- JSON is formatted -->
        {:else}
            {@html response} <!-- HTML content is displayed -->
        {/if}
    {/if}

    <!-- Displays current history of requests -->
    <h2>Request History</h2>
    <ul>
        {#each history.requests as req, i}
            <li>{i + 1}: {req}</li>
        {/each}
    </ul>

    <!-- Displays current history of responses -->
    <h2>Response History</h2>
    <ul>
        {#each history.responses as res, i}
            <li>{i + 1}: {res}</li>
        {/each}
    </ul>
</main>

<!-- Base style found online, I don't know how to style -->
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