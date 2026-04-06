#!/usr/bin/env python3
"""
⛓️ Blockchain-Agent
Blockchain Developer агент

Создаёт:
- Smart contracts
- Web3 интеграции
- Token contracts
- DApps
"""

import argparse
from pathlib import Path
from typing import Dict


class BlockchainAgent:
    """
    ⛓️ Blockchain-Agent
    
    Специализация: Blockchain Development
    Стек: Solidity, Web3.js, Ethereum, Smart Contracts
    """
    
    NAME = "⛓️ Blockchain-Agent"
    ROLE = "Blockchain Developer"
    EXPERTISE = ["Solidity", "Web3", "Ethereum", "Smart Contracts", "DeFi"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["Token.sol"] = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MyToken
 * @dev ERC20 Token with burnable and mintable functionality
 */
contract MyToken is ERC20, ERC20Burnable, Ownable {
    uint256 public constant MAX_SUPPLY = 1000000000 * 10**18; // 1 billion tokens
    uint256 public constant INITIAL_SUPPLY = 100000000 * 10**18; // 100 million tokens
    
    mapping(address => bool) public minters;
    
    event MinterAdded(address indexed minter);
    event MinterRemoved(address indexed minter);
    
    modifier onlyMinter() {
        require(minters[msg.sender] || msg.sender == owner(), "Not authorized to mint");
        _;
    }
    
    constructor() ERC20("MyToken", "MTK") {
        _mint(msg.sender, INITIAL_SUPPLY);
    }
    
    /**
     * @dev Mint new tokens
     * @param to Address to mint tokens to
     * @param amount Amount of tokens to mint
     */
    function mint(address to, uint256 amount) public onlyMinter {
        require(totalSupply() + amount <= MAX_SUPPLY, "Max supply exceeded");
        _mint(to, amount);
    }
    
    /**
     * @dev Add a new minter
     */
    function addMinter(address minter) public onlyOwner {
        minters[minter] = true;
        emit MinterAdded(minter);
    }
    
    /**
     * @dev Remove a minter
     */
    function removeMinter(address minter) public onlyOwner {
        minters[minter] = false;
        emit MinterRemoved(minter);
    }
    
    /**
     * @dev Batch transfer tokens
     */
    function batchTransfer(address[] calldata recipients, uint256[] calldata amounts) external {
        require(recipients.length == amounts.length, "Arrays length mismatch");
        
        for (uint256 i = 0; i < recipients.length; i++) {
            _transfer(msg.sender, recipients[i], amounts[i]);
        }
    }
}
"""
        
        files["Web3Integration.js"] = """import { ethers } from 'ethers';

class Web3Integration {
    constructor() {
        this.provider = null;
        this.signer = null;
        this.contract = null;
    }
    
    /**
     * Connect to MetaMask wallet
     */
    async connectWallet() {
        if (typeof window.ethereum === 'undefined') {
            throw new Error('MetaMask not installed');
        }
        
        try {
            // Request account access
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            
            // Create provider and signer
            this.provider = new ethers.providers.Web3Provider(window.ethereum);
            this.signer = this.provider.getSigner();
            
            const address = await this.signer.getAddress();
            console.log('Connected:', address);
            
            return address;
        } catch (error) {
            console.error('Connection failed:', error);
            throw error;
        }
    }
    
    /**
     * Initialize contract instance
     */
    async initContract(contractAddress, abi) {
        if (!this.signer) {
            await this.connectWallet();
        }
        
        this.contract = new ethers.Contract(contractAddress, abi, this.signer);
        return this.contract;
    }
    
    /**
     * Get token balance
     */
    async getBalance(address) {
        if (!this.contract) throw new Error('Contract not initialized');
        
        const balance = await this.contract.balanceOf(address);
        return ethers.utils.formatEther(balance);
    }
    
    /**
     * Transfer tokens
     */
    async transfer(to, amount) {
        if (!this.contract) throw new Error('Contract not initialized');
        
        const tx = await this.contract.transfer(to, ethers.utils.parseEther(amount));
        await tx.wait();
        return tx.hash;
    }
    
    /**
     * Listen for events
     */
    listenForEvents(eventName, callback) {
        if (!this.contract) throw new Error('Contract not initialized');
        
        this.contract.on(eventName, (...args) => {
            callback(args);
        });
    }
    
    /**
     * Get transaction history
     */
    async getTransactionHistory(address) {
        const filter = this.contract.filters.Transfer(null, address);
        const events = await this.contract.queryFilter(filter, -10000);
        
        return events.map(event => ({
            from: event.args.from,
            to: event.args.to,
            value: ethers.utils.formatEther(event.args.value),
            transactionHash: event.transactionHash,
            blockNumber: event.blockNumber
        }));
    }
}

export default Web3Integration;
"""
        
        files["hardhat.config.js"] = """require('@nomicfoundation/hardhat-toolbox');
require('@nomicfoundation/hardhat-verify');
require('dotenv').config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
    solidity: {
        version: '0.8.19',
        settings: {
            optimizer: {
                enabled: true,
                runs: 200
            }
        }
    },
    networks: {
        hardhat: {
            chainId: 1337
        },
        localhost: {
            url: 'http://127.0.0.1:8545'
        },
        goerli: {
            url: process.env.GOERLI_RPC || '',
            accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : []
        },
        mainnet: {
            url: process.env.MAINNET_RPC || '',
            accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : []
        }
    },
    etherscan: {
        apiKey: process.env.ETHERSCAN_API_KEY
    },
    gasReporter: {
        enabled: process.env.REPORT_GAS !== undefined,
        currency: 'USD'
    }
};
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="⛓️ Blockchain-Agent — Smart Contracts")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = BlockchainAgent()
    
    if args.request:
        print(f"⛓️ {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"⛓️ {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
