import * as vscode from 'vscode';
import axios from 'axios';
import * as WebSocket from 'ws';

export interface MCPTool {
    group: string;
    name: string;
    schema: any;
}

export class MCPClient {
    private config: vscode.WorkspaceConfiguration;
    private wsConnection: WebSocket | undefined;
    private connected: boolean = false;

    constructor() {
        this.config = vscode.workspace.getConfiguration('darbotChia');
    }

    private getBaseUrl(): string {
        const host = this.config.get<string>('mcpServer.host', 'localhost');
        const port = this.config.get<number>('mcpServer.port', 8550);
        const useSSL = this.config.get<boolean>('mcpServer.useSSL', false);
        const protocol = useSSL ? 'https' : 'http';
        return `${protocol}://${host}:${port}`;
    }

    private getWebSocketUrl(): string {
        const host = this.config.get<string>('mcpServer.host', 'localhost');
        const port = this.config.get<number>('mcpServer.port', 8550);
        const useSSL = this.config.get<boolean>('mcpServer.useSSL', false);
        const protocol = useSSL ? 'wss' : 'ws';
        return `${protocol}://${host}:${port}/mcp/ws`;
    }

    async connect(): Promise<void> {
        if (this.connected) {
            return;
        }

        try {
            // Test connection with ping
            const response = await axios.get(`${this.getBaseUrl()}/mcp/ping`, {
                timeout: 5000
            });
            
            if (response.data.ping === 'pong') {
                this.connected = true;
                
                // Optionally establish WebSocket connection
                this.connectWebSocket();
            } else {
                throw new Error('Invalid response from MCP server');
            }
        } catch (error) {
            throw new Error(`Cannot connect to MCP server: ${error}`);
        }
    }

    private connectWebSocket(): void {
        try {
            this.wsConnection = new WebSocket(this.getWebSocketUrl());
            
            this.wsConnection.on('open', () => {
                console.log('WebSocket connection established');
            });

            this.wsConnection.on('error', (error) => {
                console.error('WebSocket error:', error);
            });

            this.wsConnection.on('close', () => {
                console.log('WebSocket connection closed');
                this.wsConnection = undefined;
            });
        } catch (error) {
            console.error('Failed to establish WebSocket connection:', error);
        }
    }

    async disconnect(): Promise<void> {
        this.connected = false;
        if (this.wsConnection) {
            this.wsConnection.close();
            this.wsConnection = undefined;
        }
    }

    async callTool(group: string, name: string, params: any = {}): Promise<any> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await axios.post(
                `${this.getBaseUrl()}/mcp/${group}/${name}`,
                params,
                {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    timeout: 30000
                }
            );
            return response.data;
        } catch (error: any) {
            if (error.response) {
                throw new Error(`MCP Error: ${error.response.data.detail || error.response.statusText}`);
            } else {
                throw new Error(`Network Error: ${error.message}`);
            }
        }
    }

    async getAvailableTools(): Promise<MCPTool[]> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await axios.get(`${this.getBaseUrl()}/mcp/schema.json`);
            return response.data;
        } catch (error: any) {
            if (error.response) {
                throw new Error(`MCP Error: ${error.response.data.detail || error.response.statusText}`);
            } else {
                throw new Error(`Network Error: ${error.message}`);
            }
        }
    }

    isConnected(): boolean {
        return this.connected;
    }

    async callToolViaWebSocket(group: string, name: string, params: any = {}): Promise<any> {
        return new Promise((resolve, reject) => {
            if (!this.wsConnection || this.wsConnection.readyState !== WebSocket.OPEN) {
                reject(new Error('WebSocket not connected'));
                return;
            }

            const message = {
                group,
                name,
                params
            };

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

            this.wsConnection.on('message', onMessage);
            this.wsConnection.send(JSON.stringify(message));

            // Timeout after 30 seconds
            setTimeout(() => {
                this.wsConnection?.removeListener('message', onMessage);
                reject(new Error('WebSocket call timeout'));
            }, 30000);
        });
    }
}