export interface MCPTool {
    group: string;
    name: string;
    schema: MCPToolSchema;
}

export interface MCPToolSchema {
    description?: string;
    properties?: Record<string, any>;
    required?: string[];
    type?: string;
}

export interface MCPClientOptions {
    host?: string;
    port?: number;
    useSSL?: boolean;
    timeout?: number;
}

export interface ChiaWallet {
    id: number;
    name: string;
    type: number;
    data?: any;
}

export interface ChiaBlockchainState {
    blockchain_state: {
        peak?: {
            height: number;
            header_hash: string;
            prev_header_hash: string;
            timestamp: number;
        };
        difficulty?: number;
        space?: string;
        sync?: {
            synced: boolean;
            sync_mode: boolean;
            sync_progress_height: number;
            sync_tip_height: number;
        };
        mempool_size?: number;
    };
}

export interface ChiaPlot {
    filename: string;
    plot_id: string;
    pool_public_key?: string;
    pool_contract_puzzle_hash?: string;
    plot_public_key: string;
    file_size: number;
    time_modified: number;
}

export interface ChiaOffer {
    trade_id: string;
    status: string;
    offer: string;
    requested_payments: any[];
    created_at_time: number;
    confirmed_at_index?: number;
}

export interface ChiaCAT {
    asset_id: string;
    name: string;
    symbol: string;
}

export interface MCPError {
    error: string;
    code?: number;
    details?: any;
}