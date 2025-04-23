const HDWalletProvider = require('@truffle/hdwallet-provider');
require('dotenv').config();

console.log("INFURA_PROJECT_ID:", process.env.INFURA_PROJECT_ID);
console.log("MNEMONIC:", process.env.MNEMONIC ? '✅ Loaded' : '❌ Not loaded');

module.exports = {
  networks: {
    sepolia: {
      provider: () =>
        new HDWalletProvider(
          process.env.MNEMONIC,
          `https://sepolia.infura.io/v3/${process.env.INFURA_PROJECT_ID}`
        ),
        network_id: 11155111, // Sepolia's network ID
        gas: 4000000, // Adjust the gas limit as per your requirements
        gasPrice: 10000000000, // Set the gas price to an appropriate value
        confirmations: 2, // Set the number of confirmations needed for a transaction
        disableConfirmationListener: true,
        timeoutBlocks: 200, // Set the timeout for transactions
        skipDryRun: true // Skip the dry run option
    },
  },

  compilers: {
    solc: {
      version: '0.8.19',
    },
  },
};