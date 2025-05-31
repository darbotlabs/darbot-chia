import axios, { AxiosInstance } from 'axios';
import * as WebSocket from 'ws';
import { MCPTool, MCPClientOptions, MCPError } from './types';

export class DarbotChiaMCPClient {
    private httpClient: AxiosInstance;
    private wsConnection: WebSocket | undefined;
    private connected: boolean = false;
    private baseUrl: string;
    private wsUrl: string;

    constructor(options: MCPClientOptions = {}) {
        const {
            host = 'localhost',
            port = 8550,
            useSSL = false,
            timeout = 30000
        } = options;

        const protocol = useSSL ? 'https' : 'http';
        const wsProtocol = useSSL ? 'wss' : 'ws';
        
        this.baseUrl = `${protocol}://${host}:${port}`;
        this.wsUrl = `${wsProtocol}://${host}:${port}/mcp/ws`;

        this.httpClient = axios.create({
            baseURL: this.baseUrl,
            timeout,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    /**
     * Connect to the MCP server
     */
    async connect(): Promise<void> {
        if (this.connected) {
            return;
        }

        try {
            const response = await this.httpClient.get('/mcp/ping');
            if (response.data.ping === 'pong') {
                this.connected = true;
            } else {
                throw new Error('Invalid response from MCP server');
            }
        } catch (error: any) {
            throw new Error(`Cannot connect to MCP server: ${error.message}`);
        }
    }

    /**
     * Disconnect from the MCP server
     */
    async disconnect(): Promise<void> {
        this.connected = false;
        if (this.wsConnection) {
            this.wsConnection.close();
            this.wsConnection = undefined;
        }
    }

    /**
     * Check if connected to the MCP server
     */
    isConnected(): boolean {
        return this.connected;
    }

    /**
     * Get all available MCP tools
     */
    async getAvailableTools(): Promise<MCPTool[]> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await this.httpClient.get('/mcp/schema.json');
            return response.data;
        } catch (error: any) {
            this.handleHttpError(error);
        }
    }

    /**
     * Call an MCP tool via HTTP
     */
    async callTool(group: string, name: string, params: any = {}): Promise<any> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await this.httpClient.post(`/mcp/${group}/${name}`, params);
            return response.data;
        } catch (error: any) {
            this.handleHttpError(error);
        }
    }

    /**
     * Establish WebSocket connection
     */
    async connectWebSocket(): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                this.wsConnection = new WebSocket(this.wsUrl);

                this.wsConnection.on('open', () => {
                    resolve();
                });

                this.wsConnection.on('error', (error) => {
                    reject(error);
                });

                this.wsConnection.on('close', () => {
                    this.wsConnection = undefined;
                });
            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Call an MCP tool via WebSocket
     */
    async callToolViaWebSocket(group: string, name: string, params: any = {}): Promise<any> {
        if (!this.wsConnection || this.wsConnection.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket not connected');
        }

        return new Promise((resolve, reject) => {
            const message = { group, name, params };

            const onMessage = (data: WebSocket.Data) => {
                try {
                    const response = JSON.parse(data.toString());
                    this.wsConnection?.removeListener('message', onMessage);

                    if (response.error) {
                        reject(new Error(response.error));
                    } else {
                        resolve(response.result);
                    }
                } catch (error) {
                    reject(error);
                }
            };

            const timeout = setTimeout(() => {
                this.wsConnection?.removeListener('message', onMessage);
                reject(new Error('WebSocket call timeout'));
            }, 30000);

            this.wsConnection.on('message', onMessage);
            this.wsConnection.send(JSON.stringify(message));

            // Clear timeout when done
            this.wsConnection.once('message', () => clearTimeout(timeout));
        });
    }

    private handleHttpError(error: any): never {
        if (error.response) {
            const mcpError: MCPError = {
                error: error.response.data.detail || error.response.statusText,
                code: error.response.status,
                details: error.response.data
            };
            throw new Error(`MCP Error (${mcpError.code}): ${mcpError.error}`);
        } else {
            throw new Error(`Network Error: ${error.message}`);
        }
    }
}