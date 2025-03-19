export class ProxyServer {
    requestHistory: string[] = [];
    responseHistory: string[] = [];

    async sendRequest(requestUrl: string): Promise<string> {
        this.requestHistory.push(requestUrl);
    
        try {
            const proxyUrl = `http://localhost:5001/proxy?url=${encodeURIComponent(requestUrl)}`;
            const response = await fetch(proxyUrl);
            const data = await response.text();
    
            this.responseHistory.push(data);
            return data;
        } catch (error) {
            console.error("Error fetching data:", error);
            this.responseHistory.push("Error fetching data.");
            return "Error fetching data.";
        }
    }

    getHistory() {
        return {
            requests: this.requestHistory,
            responses: this.responseHistory
        };
    }
}

export class HTTPClient {
    proxy: ProxyServer;

    constructor(proxy: ProxyServer) {
        this.proxy = proxy;
    }

    async sendRequestToProxy(requestUrl: string): Promise<string> {
        return await this.proxy.sendRequest(requestUrl);
    }
}