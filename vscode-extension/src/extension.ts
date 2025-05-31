import * as vscode from 'vscode';
import { MCPClient } from './mcpClient';
import { ChiaExplorerProvider } from './explorerProvider';

let mcpClient: MCPClient | undefined;
let explorerProvider: ChiaExplorerProvider | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('Darbot Chia extension is now active!');

    // Initialize MCP client
    mcpClient = new MCPClient();
    explorerProvider = new ChiaExplorerProvider(mcpClient);

    // Register tree data provider
    vscode.window.registerTreeDataProvider('darbotChiaExplorer', explorerProvider);

    // Register commands
    const commands = [
        vscode.commands.registerCommand('darbotChia.connect', async () => {
            try {
                await mcpClient?.connect();
                vscode.commands.executeCommand('setContext', 'darbotChia.connected', true);
                vscode.window.showInformationMessage('Connected to Chia MCP server');
                explorerProvider?.refresh();
            } catch (error) {
                vscode.window.showErrorMessage(`Failed to connect: ${error}`);
            }
        }),

        vscode.commands.registerCommand('darbotChia.disconnect', async () => {
            await mcpClient?.disconnect();
            vscode.commands.executeCommand('setContext', 'darbotChia.connected', false);
            vscode.window.showInformationMessage('Disconnected from Chia MCP server');
            explorerProvider?.refresh();
        }),

        vscode.commands.registerCommand('darbotChia.getBlockchainState', async () => {
            try {
                const state = await mcpClient?.callTool('full_node', 'get_blockchain_state', {});
                if (state) {
                    const channel = vscode.window.createOutputChannel('Chia Blockchain State');
                    channel.clear();
                    channel.appendLine(JSON.stringify(state, null, 2));
                    channel.show();
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Failed to get blockchain state: ${error}`);
            }
        }),

        vscode.commands.registerCommand('darbotChia.getWallets', async () => {
            try {
                const wallets = await mcpClient?.callTool('wallet', 'get_wallets', {});
                if (wallets) {
                    const channel = vscode.window.createOutputChannel('Chia Wallets');
                    channel.clear();
                    channel.appendLine(JSON.stringify(wallets, null, 2));
                    channel.show();
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Failed to get wallets: ${error}`);
            }
        }),

        vscode.commands.registerCommand('darbotChia.showTools', async () => {
            try {
                const tools = await mcpClient?.getAvailableTools();
                if (tools) {
                    const quickPick = vscode.window.createQuickPick();
                    quickPick.items = tools.map(tool => ({
                        label: `${tool.group}.${tool.name}`,
                        description: tool.schema.description || 'No description'
                    }));
                    quickPick.placeholder = 'Select a tool to view details';
                    quickPick.onDidChangeSelection(selection => {
                        if (selection[0]) {
                            const selectedTool = tools.find(t => 
                                `${t.group}.${t.name}` === selection[0].label
                            );
                            if (selectedTool) {
                                const channel = vscode.window.createOutputChannel('MCP Tool Details');
                                channel.clear();
                                channel.appendLine(`Tool: ${selectedTool.group}.${selectedTool.name}`);
                                channel.appendLine(`Description: ${selectedTool.schema.description || 'No description'}`);
                                channel.appendLine(`Schema: ${JSON.stringify(selectedTool.schema, null, 2)}`);
                                channel.show();
                            }
                        }
                        quickPick.hide();
                    });
                    quickPick.show();
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Failed to get tools: ${error}`);
            }
        })
    ];

    context.subscriptions.push(...commands);

    // Auto-connect if enabled
    const config = vscode.workspace.getConfiguration('darbotChia');
    if (config.get('autoConnect')) {
        vscode.commands.executeCommand('darbotChia.connect');
    }
}

export function deactivate() {
    mcpClient?.disconnect();
}