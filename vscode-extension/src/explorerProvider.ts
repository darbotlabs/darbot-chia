import * as vscode from 'vscode';
import { MCPClient } from './mcpClient';

export class ChiaExplorerProvider implements vscode.TreeDataProvider<ChiaItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<ChiaItem | undefined | null | void> = new vscode.EventEmitter<ChiaItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<ChiaItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private mcpClient: MCPClient) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: ChiaItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: ChiaItem): Promise<ChiaItem[]> {
        if (!this.mcpClient.isConnected()) {
            return [new ChiaItem('Not connected', vscode.TreeItemCollapsibleState.None, 'status')];
        }

        if (!element) {
            // Root level
            return [
                new ChiaItem('Blockchain', vscode.TreeItemCollapsibleState.Collapsed, 'blockchain'),
                new ChiaItem('Wallets', vscode.TreeItemCollapsibleState.Collapsed, 'wallets'),
                new ChiaItem('Farmer', vscode.TreeItemCollapsibleState.Collapsed, 'farmer'),
                new ChiaItem('Harvester', vscode.TreeItemCollapsibleState.Collapsed, 'harvester'),
                new ChiaItem('Offers', vscode.TreeItemCollapsibleState.Collapsed, 'offers'),
                new ChiaItem('CATs', vscode.TreeItemCollapsibleState.Collapsed, 'cats'),
                new ChiaItem('Data Layer', vscode.TreeItemCollapsibleState.Collapsed, 'datalayer'),
                new ChiaItem('DIDs & VCs', vscode.TreeItemCollapsibleState.Collapsed, 'didvc')
            ];
        }

        try {
            switch (element.contextValue) {
                case 'blockchain':
                    return await this.getBlockchainItems();
                case 'wallets':
                    return await this.getWalletItems();
                case 'farmer':
                    return await this.getFarmerItems();
                case 'harvester':
                    return await this.getHarvesterItems();
                case 'offers':
                    return await this.getOfferItems();
                case 'cats':
                    return await this.getCATItems();
                case 'datalayer':
                    return await this.getDataLayerItems();
                case 'didvc':
                    return await this.getDIDVCItems();
                default:
                    return [];
            }
        } catch (error) {
            return [new ChiaItem(`Error: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getBlockchainItems(): Promise<ChiaItem[]> {
        try {
            const state = await this.mcpClient.callTool('full_node', 'get_blockchain_state', {});
            const items = [];
            
            if (state.blockchain_state) {
                const blockchain = state.blockchain_state;
                items.push(new ChiaItem(`Height: ${blockchain.peak?.height || 'Unknown'}`, vscode.TreeItemCollapsibleState.None, 'info'));
                items.push(new ChiaItem(`Difficulty: ${blockchain.difficulty || 'Unknown'}`, vscode.TreeItemCollapsibleState.None, 'info'));
                items.push(new ChiaItem(`Space: ${blockchain.space || 'Unknown'}`, vscode.TreeItemCollapsibleState.None, 'info'));
                items.push(new ChiaItem(`Sync Status: ${blockchain.sync?.synced ? 'Synced' : 'Syncing'}`, vscode.TreeItemCollapsibleState.None, 'info'));
            }
            
            return items;
        } catch (error) {
            return [new ChiaItem(`Failed to load: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getWalletItems(): Promise<ChiaItem[]> {
        try {
            const wallets = await this.mcpClient.callTool('wallet', 'get_wallets', {});
            const items = [];
            
            if (wallets.wallets) {
                for (const wallet of wallets.wallets) {
                    const item = new ChiaItem(
                        `${wallet.name} (ID: ${wallet.id})`,
                        vscode.TreeItemCollapsibleState.None,
                        'wallet'
                    );
                    item.description = `Type: ${wallet.type}`;
                    items.push(item);
                }
            }
            
            return items;
        } catch (error) {
            return [new ChiaItem(`Failed to load: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getFarmerItems(): Promise<ChiaItem[]> {
        try {
            const harvesters = await this.mcpClient.callTool('farmer', 'get_harvesters', {});
            const items = [];
            
            if (harvesters.harvesters) {
                for (const harvester of harvesters.harvesters) {
                    const item = new ChiaItem(
                        `Harvester: ${harvester.connection?.host || 'Unknown'}`,
                        vscode.TreeItemCollapsibleState.None,
                        'harvester'
                    );
                    item.description = `Plots: ${harvester.plots || 0}`;
                    items.push(item);
                }
            }
            
            return items;
        } catch (error) {
            return [new ChiaItem(`Failed to load: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getHarvesterItems(): Promise<ChiaItem[]> {
        try {
            const plots = await this.mcpClient.callTool('harvester', 'get_plots', {});
            const items = [];
            
            if (plots.plots) {
                items.push(new ChiaItem(`Total Plots: ${plots.plots.length}`, vscode.TreeItemCollapsibleState.None, 'info'));
                
                // Group by directory
                const dirMap = new Map<string, number>();
                for (const plot of plots.plots) {
                    const dir = plot.filename?.split('/').slice(0, -1).join('/') || 'Unknown';
                    dirMap.set(dir, (dirMap.get(dir) || 0) + 1);
                }
                
                for (const [dir, count] of dirMap) {
                    items.push(new ChiaItem(`${dir}: ${count} plots`, vscode.TreeItemCollapsibleState.None, 'directory'));
                }
            }
            
            return items;
        } catch (error) {
            return [new ChiaItem(`Failed to load: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getOfferItems(): Promise<ChiaItem[]> {
        try {
            const offers = await this.mcpClient.callTool('offers', 'get_all_offers', { start: 0, end: 10 });
            const items = [];
            
            if (offers.trade_records) {
                items.push(new ChiaItem(`Total Offers: ${offers.trade_records.length}`, vscode.TreeItemCollapsibleState.None, 'info'));
                
                for (const offer of offers.trade_records.slice(0, 5)) {
                    const item = new ChiaItem(
                        `Offer: ${offer.trade_id?.slice(0, 8)}...`,
                        vscode.TreeItemCollapsibleState.None,
                        'offer'
                    );
                    item.description = `Status: ${offer.status}`;
                    items.push(item);
                }
            }
            
            return items;
        } catch (error) {
            return [new ChiaItem(`Failed to load: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getCATItems(): Promise<ChiaItem[]> {
        try {
            const cats = await this.mcpClient.callTool('cat', 'get_cat_list', {});
            const items = [];
            
            if (cats.cat_list) {
                for (const cat of cats.cat_list.slice(0, 10)) {
                    const item = new ChiaItem(
                        `${cat.name || 'Unknown CAT'}`,
                        vscode.TreeItemCollapsibleState.None,
                        'cat'
                    );
                    item.description = cat.symbol || cat.asset_id?.slice(0, 8);
                    items.push(item);
                }
            }
            
            return items;
        } catch (error) {
            return [new ChiaItem(`Failed to load: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getDataLayerItems(): Promise<ChiaItem[]> {
        try {
            const stores = await this.mcpClient.callTool('data_layer', 'get_owned_stores', {});
            const items = [];
            
            if (stores.store_ids) {
                items.push(new ChiaItem(`Owned Stores: ${stores.store_ids.length}`, vscode.TreeItemCollapsibleState.None, 'info'));
                
                for (const storeId of stores.store_ids.slice(0, 5)) {
                    const item = new ChiaItem(
                        `Store: ${storeId.slice(0, 8)}...`,
                        vscode.TreeItemCollapsibleState.None,
                        'datastore'
                    );
                    items.push(item);
                }
            }
            
            return items;
        } catch (error) {
            return [new ChiaItem(`Failed to load: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getDIDVCItems(): Promise<ChiaItem[]> {
        return [
            new ChiaItem('DID Wallets: Click to create', vscode.TreeItemCollapsibleState.None, 'did'),
            new ChiaItem('Verifiable Credentials: Click to manage', vscode.TreeItemCollapsibleState.None, 'vc')
        ];
    }
}

export class ChiaItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly contextValue: string
    ) {
        super(label, collapsibleState);
        this.tooltip = `${this.label}`;
        
        // Set appropriate icons
        switch (contextValue) {
            case 'blockchain':
                this.iconPath = new vscode.ThemeIcon('server-process');
                break;
            case 'wallets':
            case 'wallet':
                this.iconPath = new vscode.ThemeIcon('account');
                break;
            case 'farmer':
            case 'harvester':
                this.iconPath = new vscode.ThemeIcon('vm');
                break;
            case 'offers':
            case 'offer':
                this.iconPath = new vscode.ThemeIcon('symbol-event');
                break;
            case 'cats':
            case 'cat':
                this.iconPath = new vscode.ThemeIcon('symbol-property');
                break;
            case 'datalayer':
            case 'datastore':
                this.iconPath = new vscode.ThemeIcon('database');
                break;
            case 'didvc':
            case 'did':
            case 'vc':
                this.iconPath = new vscode.ThemeIcon('key');
                break;
            case 'info':
                this.iconPath = new vscode.ThemeIcon('info');
                break;
            case 'error':
                this.iconPath = new vscode.ThemeIcon('error');
                break;
            default:
                this.iconPath = new vscode.ThemeIcon('circle-outline');
        }
    }
}