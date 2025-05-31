import { DarbotChiaMCPClient } from './mcpClient';
import { ChiaWallet, ChiaBlockchainState, ChiaPlot, ChiaOffer, ChiaCAT } from './types';

/**
 * High-level wrapper for common Chia operations
 */
export class ChiaTools {
    constructor(private client: DarbotChiaMCPClient) {}

    // Wallet Tools
    async getWallets(): Promise<{ wallets: ChiaWallet[] }> {
        return this.client.callTool('wallet', 'get_wallets');
    }

    async getWalletBalance(walletId: number): Promise<any> {
        return this.client.callTool('wallet', 'get_wallet_balance', { wallet_id: walletId });
    }

    async getPublicKeys(): Promise<any> {
        return this.client.callTool('wallet', 'get_public_keys');
    }

    async loginWallet(fingerprint: number): Promise<any> {
        return this.client.callTool('wallet', 'log_in', { fingerprint });
    }

    // Full Node Tools
    async getBlockchainState(): Promise<ChiaBlockchainState> {
        return this.client.callTool('full_node', 'get_blockchain_state');
    }

    async getBlock(headerHash: string): Promise<any> {
        return this.client.callTool('full_node', 'get_block', { header_hash: headerHash });
    }

    async getNetworkInfo(): Promise<any> {
        return this.client.callTool('full_node', 'get_network_info');
    }

    // Farmer Tools
    async getHarvesters(): Promise<any> {
        return this.client.callTool('farmer', 'get_harvesters');
    }

    async getSignagePoints(): Promise<any> {
        return this.client.callTool('farmer', 'get_signage_points');
    }

    // Harvester Tools
    async getPlots(): Promise<{ plots: ChiaPlot[] }> {
        return this.client.callTool('harvester', 'get_plots');
    }

    async getPlotDirectories(): Promise<any> {
        return this.client.callTool('harvester', 'get_plot_directories');
    }

    // Offer Tools
    async getAllOffers(start: number = 0, end: number = 50): Promise<{ trade_records: ChiaOffer[] }> {
        return this.client.callTool('offers', 'get_all_offers', { start, end });
    }

    async createOfferForIds(offer: any, requestedPayments: any[], fee: number = 0): Promise<any> {
        return this.client.callTool('offers', 'create_offer_for_ids', {
            offer,
            requested_payments: requestedPayments,
            fee
        });
    }

    async takeOffer(offer: string, fee: number = 0): Promise<any> {
        return this.client.callTool('offers', 'take_offer', { offer, fee });
    }

    // CAT Tools
    async getCATList(): Promise<{ cat_list: ChiaCAT[] }> {
        return this.client.callTool('cat', 'get_cat_list');
    }

    async createNewCATWallet(amount: number, fee: number = 0): Promise<any> {
        return this.client.callTool('cat', 'create_new_cat_and_wallet', { amount, fee });
    }

    async getStrayCats(): Promise<any> {
        return this.client.callTool('cat', 'get_stray_cats');
    }

    // Data Layer Tools
    async getOwnedStores(): Promise<any> {
        return this.client.callTool('data_layer', 'get_owned_stores');
    }

    async createDataStore(fee: number = 0): Promise<any> {
        return this.client.callTool('data_layer', 'create_data_store', { fee });
    }

    async getValue(storeId: string, key: string): Promise<any> {
        return this.client.callTool('data_layer', 'get_value', { 
            store_id: storeId, 
            key 
        });
    }

    // DID Tools
    async createNewDIDWallet(amount: number = 1, fee: number = 0): Promise<any> {
        return this.client.callTool('did', 'create_new_did_wallet', { amount, fee });
    }

    // VC Tools
    async mintVC(didId: string, targetAddress: string, fee: number = 0): Promise<any> {
        return this.client.callTool('vc', 'vc_mint', {
            did_id: didId,
            target_address: targetAddress,
            fee
        });
    }

    async getVC(launcherId: string): Promise<any> {
        return this.client.callTool('vc', 'vc_get', { launcher_id: launcherId });
    }
}