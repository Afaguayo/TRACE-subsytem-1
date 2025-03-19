export class ProxyServer {
    //This should be sent to a Request and Response Manager which keeps track
    requestHistory: string[] = [];
    responseHistory: string[] = [];

    //Takes in only URL for now, should expand to take in a specific request
    async sendRequest(requestUrl: string): Promise<string> {
        this.requestHistory.push(requestUrl);
    
        try {
            //This connects to our backend
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

    //Sends URL to Server, should also send request type
    async sendRequestToProxy(requestUrl: string): Promise<string> {
        return await this.proxy.sendRequest(requestUrl);
    }
}