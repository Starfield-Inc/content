---
title: "OpenClaw AI Agent Tutorial: Autonomous Wallets on Base and Solana - Part 1"
seo_title: "OpenClaw Agent Wallets on Base and Solana, Part 1"
meta_description: "Set up an AI hackathon agent with OpenClaw, give it test wallets on Base and Solana, and send a test transaction on each network."
level: "Not stated in the original tutorial"
time: "Not stated in the original tutorial"
prerequisites:
  - "A Hostinger account (to host the OpenClaw instance)"
  - "A Google AI Studio API key (Gemini API key)"
  - "A Telegram account (optional, for the messaging channel)"
  - "A Coinbase Developer Platform account (for the Base Sepolia faucet)"
  - "A wallet such as MetaMask for Base Sepolia and Phantom for Solana devnet"
---

# OpenClaw AI Agent Tutorial: Autonomous Wallets on Base and Solana - Part 1

## Introduction

This tutorial provides a guide to setting up and using OpenClaw AI agents for managing autonomous cryptocurrency wallets on both the Base and Solana networks. You will learn how to deploy OpenClaw on a Hostinger instance, configure messaging channels for interaction, and perform secure transactions on testnets before transitioning to mainnets. This part focuses on the initial setup and wallet creation on the Base network, followed by a brief overview of Solana wallet setup.

An agent that can hold and send test tokens is a useful building block for an AI hackathon project. Practising on testnets, as this tutorial does, lets you rehearse a payment demo without spending real funds. When you have a working agent, see the [upcoming AI hackathons](/ai-hackathons/).

## Setting Up OpenClaw and Messaging Channels

### Hostinger Instance and OpenClaw Installation

Begin by signing up for a Hostinger account.
Set up OpenClaw on Hostinger using this tutorial: [https://www.hostinger.com/support/how-to-install-openclaw-on-hostinger-vps/](https://www.hostinger.com/support/how-to-install-openclaw-on-hostinger-vps/)

This offers a cost-effective and secure environment for deploying OpenClaw, suited to users seeking alternatives to local hardware solutions like a Mac Mini.

### Messaging Channels and Onboarding

Navigate to **Docker Manager** > **Projects** > **Terminal**.

Once the terminal is open, you can install OpenClaw by running the command:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Then run the onboarding command

```bash
openclaw onboard --install-daemon
```

Complete the setup steps according to your preferences.

> Carefully read the security warning to understand the repercussions of installation. Once you have a clear understanding, proceed by clicking "Yes."

For **Onboarding Mode**, select "Quickstart."

**Model/Auth Provider**:
Select your preferred model provider. We recommend **Google/Gemini** for this tutorial.

Then select *Gemini API Key*.

1. Go to [Google AI Studio](https://aistudio.google.com/u/1/api-keys) and get your API key there

Then insert it.

On the *Default model* choose your preferred model, but you can select "Keep Current"

**Communication Channel**:
For the communication channel, we will select Telegram due to its widespread use, but you are free to choose any of your preferred communication channels.

Go to [@BotFather](https://web.telegram.org/k/#@BotFather) on telegram, then create a new bot by running the command ``/newbot``

Follow the prompts then copy the bot token.

Then, configure the allowed username(s) that can direct message your bot.

For more info, you can check [this documentation](https://docs.openclaw.ai/telegram)

**Completing Setup**:
Upon successful setup, you can begin interacting with the bot via Telegram or the terminal. This tutorial will proceed using the terminal interface.

The bot will then prompt you to:
1. Give it a name
2. Give it your name (what it will be calling you)
3. Give it the personality it will be portraying as

Feel free to customize these settings to align with your preferences.

## Creating a Wallet on Base

### Wallet Creation

In this straightforward step, you will instruct the agent to set up a new wallet on the Base network for token transactions.

This is the prompt we will use:

```bash
Create a new wallet on Base that you will use to receive and send USDC stablecoins. Start by setting it up on the Base Sepolia testnet so you can receive test tokens and practice transactions safely. After confirming everything works on testnet, prepare the same setup for use on Base mainnet.
```

Wallet creation may take some time, so expect a progress response from the agent before the result. Once it is done, the agent replies with a final response that includes the new wallet details.

### Obtaining USDC Test Funds

The next step involves acquiring test USDC funds for your newly created wallet.

Go to [Coinbase Developer Platform Faucet](https://portal.cdp.coinbase.com/products/faucet), sign up and select:
1. Network as *sepolia*
2. Token as *USDC*
3. Send to address: *insert your address*

Then click on **Claim 1 USDC**.

Afterward, send a prompt to confirm the receipt of 1 USDC:
```bash
I have just sent 1 test USDC to your Base Sepolia wallet from the Coinbase Developer Faucet. Please verify that you have received it by checking the USDC balance on Base Sepolia and confirm:
1) whether the 1 USDC has arrived,
2) your current USDC balance,
3) the hash, block number, and timestamp of the latest incoming USDC transaction.
```

The expected response confirms the deposit, with the balance, hash, block number and timestamp you asked for.

### Testing a Transaction

The next step is to test the transaction functionality.

Open your MetaMask wallet (or any other wallet you use) and ensure it's connected to the Base Sepolia network.

Then, select the receiving address for Base Sepolia USDC.

Copy the address and tell the agent to send 0.3 USDC to that address:

```bash
Send 0.3 USDC from your Base Sepolia wallet to the following recipient address on Base Sepolia: <your_wallet_address>. After sending, confirm that the transaction was successful by sharing the transaction hash and your updated USDC balance.
```

> You also need to ensure you have enough ETH for gas fees, you can get more eth at the [Coinbase Developer Platform Faucet](https://portal.cdp.coinbase.com/products/faucet)

Once the transaction successfully completes, the agent replies with the transaction hash and the updated balance.

And you can also confirm it in the [Block Explorer](https://sepolia-explorer.base.org)

You can see the balance goes from 1 USDC to 0.7 USDC.

This concludes the setup and testing of your AI Agent's autonomous wallet on the Base network. Next, we will explore practical solutions that can be built using this functionality.

### Resources

- [Official Base documentation](https://docs.base.org/base-chain/quickstart/why-base)
- [Base Sepolia block explorer](https://sepolia-explorer.base.org)
- [Coinbase Developer Platform Faucet](https://portal.cdp.coinbase.com/products/faucet)

## Creating a Wallet on Solana

### Wallet Creation

Similar to the Base network, this step involves instructing the agent to set up a Solana wallet for token transactions.

This is the prompt we will use:

```bash
Create a new wallet on Solana that you will use to receive and send USDC, and hold SOL for transaction fees. Start by setting it up on the Solana devnet so you can receive test tokens and practice transactions safely. After confirming everything works on devnet, prepare the same setup for use on Solana mainnet.
```

The agent replies with the new Solana wallet details.

### Obtaining USDC/SOL Test Funds

The next step is to acquire test funds for your Solana wallet.

Go to a [Solana devnet faucet](https://faucet.solana.com) such as the official Solana Faucet, then:
1. Select **Devnet** as the network
2. Request **SOL** to the agent's Solana devnet address (for gas fees)
3. Optionally, use a devnet USDC faucet or test-token mint (if available) to send **USDC** to the same address

Afterward, send a prompt to confirm the receipt of the test funds:

```bash
I have just sent you test SOL (and USDC if available) on Solana devnet to your wallet address. Please verify that you have received them by checking your balances on Solana devnet and confirm:
1) whether the new funds have arrived,
2) your current SOL and USDC balances,
3) the signature, slot, and timestamp of the latest incoming transaction.
```

The expected response confirms the deposit.

### Testing a Transaction

If you haven't already, download the Phantom wallet [here](https://phantom.com/download).

Open your Solana wallet (for example, Phantom) and switch it to the Devnet network.

Then, click on the ``SOL`` address to receive funds from your OpenClaw agent.

Copy your wallet's Solana devnet receiving address.

Then tell the agent to send a small amount to that address:
```bash
Send 0.3 USDC (or an equivalent small amount of SOL if USDC is not available) from your Solana devnet wallet to the following recipient address: <your_solana_wallet_address>. After sending, confirm that the transaction was successful by sharing the transaction signature and your updated token balance.
```

> You also need to ensure the agent's wallet has enough SOL to pay for transaction fees; you can always request more SOL from the Solana Faucet on devnet.

Upon successful completion, the agent confirms the transfer with the transaction signature.

## Frequently asked questions

### Why create the wallet on a testnet before mainnet?

The prompts ask the agent to set up the wallet on the Base Sepolia testnet (or Solana devnet) before mainnet, so it can receive test tokens and practise transactions safely. Only after confirming everything works on testnet does the agent prepare the same setup for mainnet.

### What do I need besides the agent to test a transaction?

You need a wallet that can receive funds on the test network, such as MetaMask on Base Sepolia or Phantom on Solana devnet. The agent's wallet also needs enough ETH (Base) or SOL (Solana) to pay transaction fees, which you can request from the faucets linked above.

### How do I confirm that a transaction went through?

Ask the agent for the transaction hash (Base) or signature (Solana) and its updated balance, as the prompts do. On Base Sepolia you can also check the Block Explorer, where the balance in this example goes from 1 USDC to 0.7 USDC after sending 0.3 USDC.

## Conclusion

This tutorial has demonstrated the capability of OpenClaw AI agents to manage autonomous wallets on both Base and Solana networks. The ability to perform blockchain transactions by simply providing instructions, without writing a single line of code, is a notable step for decentralized application development. This approach lets users interact with blockchain ecosystems more intuitively and efficiently, and opens doors to solutions that use AI-driven automation in the web3 space.

We encourage you to explore the potential of autonomous agents further and discover how they can streamline your interactions with various blockchain platforms.

## How this tutorial was tested

This content is carried over from Steve's earlier tutorial and updated for Starfield Labs. It was not re-run in this build. The prompts and expected outcomes described above are the author's original results, and the author's screenshots were not carried over.

The following were not run here: the Hostinger account and OpenClaw installation, onboarding with a Gemini API key, the Telegram bot setup, wallet creation on Base and Solana, the faucet requests (these need accounts), and the test transactions with MetaMask and Phantom.
