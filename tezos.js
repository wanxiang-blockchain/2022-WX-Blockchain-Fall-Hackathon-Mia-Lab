import { BeaconWallet } from '@taquito/beacon-wallet';
import { TezosToolkit } from '@taquito/taquito';

// Update CONTRACT_ADDRESS and other constants below as required
const DAPP_NAME = "Tezos Developer Hub";
const RPC_URL = "https://rpc.ghostnet.teztnets.xyz/";
// const RPC_URL = "https://hangzhounet.smartpy.io";
const NETWORK = "teztnets";
// const NETWORK = "hangzhounet"
const CONTRACT_ADDRESS = "KT1FXAkRDjSxhQE7mUpKjX22rinx8dHw9aZa";
//const CONTRACT_ADDRESS = "KT1TF9L8MwcKm6CZu8V9Se2LbmtHR3iQSa5P";


// Initialize TezosToolkit
// 启动taquito的TezosToolkit
const Tezos = new TezosToolkit(RPC_URL);


// Initialize BeaconWallet
const wallet = new BeaconWallet({
    name: DAPP_NAME,
    preferredNetwork: NETWORK,
    rpcUrl: RPC_URL,
    colorMode: "light"
});

// Setting the wallet as the wallet provider for Taquito.
Tezos.setWalletProvider(wallet)

// Create getActiveAccount function to connect with wallet
const getActiveAccount = async() => {
    const activeAccount = await wallet.client.getActiveAccount();
    console.log(activeAccount);
    // no active account, we need permission first
    if (!activeAccount){
        await wallet.requestPermissions({
            type: NETWORK,
            rpcUrl: RPC_URL
        });
        return getActiveAccount();
    }

    return activeAccount;
};

// Create clearActiveAccount function to disconnect the wallet
const clearActiveAccount = async () => {
    return wallet.client.clearActiveAccount();
};

// Fetching contract
const getContract = async() => {
    return Tezos.wallet.at(CONTRACT_ADDRESS);
};

// Fetching Contract's storage
const getContractStorage = async() => {
    return (await getContract()).storage();
};

export {
    Tezos,
    wallet,
    getActiveAccount,
    clearActiveAccount,
    getContract,
    getContractStorage
};
