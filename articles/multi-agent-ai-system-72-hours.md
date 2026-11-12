---
title: "Building a Multi-Agent AI System in 72 Hours: My AI Hackathon Experience"
summary: "A first-person build log of a five-agent system made with LangGraph, Claude and Gemini in 72 hours, with the architecture and lessons for AI hackathon builders."
byline: "Starfield Labs"
seo_title: "Multi-Agent AI System in 72 Hours: AI Hackathon Build"
meta_description: "AI hackathon build log: five agents with LangGraph, Claude and Gemini plus on-chain settlement, and lessons for your next project."
---

# Building a Multi-Agent AI System in 72 Hours: My AI Hackathon Experience

## TL;DR

I recently took part in an **AI hackathon** project called "**AI Agents on Arc with USDC**". This **artificial intelligence hackathon** challenged participants to build multi-agent systems. My project, **Arc Mind Collective**, brings AI-powered intelligence to blockchain intent coordination using 5 specialized agents (supported by Claude Sonnet 4.5 + Gemini 2.5 Pro) orchestrated with LangGraph, deployed on the Arc L1 testnet with smart contract settlement.

For those exploring **AI hackathon ideas** or wondering **how AI hackathons work**, this article provides a detailed breakdown of building a production-ready multi-agent system within the tight timeframe typical of **online AI hackathons**.

## The Problem: Why Blockchain Needs to Get Smarter

I've been fascinated by intent-based architectures ever since Uniswap X and CoW Protocol started gaining traction. The idea is simple but powerful: instead of manually crafting complex transactions, users express their _intent_ ("I want to buy 1 BTC with USDC at the best price") and let the protocol figure out the execution.

But here's the thing that kept bothering me: **these systems can't actually think**.

Current intent coordination platforms are basically sophisticated matching engines - they can compare numbers and execute predefined rules, but they fundamentally lack:

1. **Semantic understanding** - They can't understand context or nuanced requirements
2. **Risk awareness** - No built-in fraud detection or counterparty risk assessment
3. **Market intelligence** - No real-time validation of whether prices make sense
4. **Explainability** - Decisions are opaque black boxes

This is where AI and blockchain should merge. Smart contracts are perfect for trustless execution, but they need intelligence for coordination, analysis, and decision-making.

## The Idea: Five AI Agents Working as a Team

During the Arc L1 hackathon, I set out to build a **multi-agent AI system for decentralized intent coordination**. The architecture is inspired by how humans work in trading desks - different specialists handling different aspects:

### The Five Agents

**🎯 Matching Agent** (Claude Sonnet 4.5)

- Semantic understanding of buy/sell intents
- Finds optimal counterparties with confidence scoring
- Can handle complex requirements like "verified sellers only" or "must settle within 1 hour"

**📈 Market Agent** (Gemini 2.5 Pro)

- Real-time price validation against market conditions
- Volatility analysis and sentiment scoring
- Ensures users aren't getting ripped off

**🛡️ Fraud Agent** (Claude Sonnet 4.5)

- Pattern detection for wash trading, pump-and-dump schemes
- Historical behavior analysis
- Flags suspicious activity before settlement

**⚠️ Risk Agent** (Claude Sonnet 4.5)

- Comprehensive risk scoring across multiple dimensions
- Counterparty risk, liquidity risk, market risk, operational risk
- Explainable decisions with reasoning

**💳 Settlement Agent** (Claude Sonnet 4.5)

- Plans atomic escrow settlement on Arc L1
- Gas estimation and optimization
- Coordinates with PaymentRouter for AP2 (Stripe) integration

## The Build: From Concept to Production in 72 Hours

### Night 1: Architecture & Smart Contracts

I started with the blockchain layer - three Solidity contracts that would handle the on-chain settlement:

```text
Core contracts deployed to Arc testnet
IntentRegistry.sol - Stores all trading intents (182 LOC)
AuctionEscrow.sol - Manages matching and settlement (348 LOC)
PaymentRouter.sol - Handles payments via AP2 protocol (210 LOC)
```

The key insight was to keep the blockchain minimal - just the trustless settlement layer. All the AI reasoning happens off-chain for speed and cost efficiency.

By 2 AM, I had all contracts compiling and 27 Foundry tests passing. There's something deeply satisfying about seeing that green checkmark wall.

### Day 2: The Agent Swarm

The real magic happened when I started building the agent coordination layer using **LangGraph**. This framework is perfect for multi-agent systems because it gives you:

- Type-safe state management across agents
- Conditional routing (different paths based on agent decisions)
- Streaming outputs for real-time visualization
- Full observability and debugging

Each agent is built with a consistent pattern:

1. Receive intent + context from shared state
2. Use LLM API (Claude or Gemini) for analysis
3. Return structured output with reasoning and confidence scores
4. Update shared state for next agent

One of the breakthrough moments was getting the fraud agent working. I gave it examples of wash trading patterns and pump-and-dump schemes, and it started catching suspicious behavior with scary accuracy. In testing, it flagged a fake intent I created where the same address was both buyer and seller.

### Day 3: UI, Integration & Deployment

The final day was all about making it usable. I built a Streamlit dashboard that shows:

- Real-time agent execution with color-coded status (🟡 running → 🟢 complete)
- Live intermediate results from each agent
- Confidence scores and reasoning for every decision
- Transaction links to Arc testnet explorer

The coolest feature: you can watch the agents "think" in real-time. When the Matching Agent analyzes intents, you see its reasoning appear live:

🎯 Matching Agent: "Found 3 potential matches for BUY intent..."

Match #1: score 0.92 - "High compatibility, price within 2% of market"

Match #2: score 0.78 - "Good match but 4% price spread"

...reasoning continues...

### Deployment to Arc Testnet

Getting everything on Arc L1 was surprisingly smooth. Circle's infrastructure is solid - the testnet is fast, the faucet is generous with USDC, and the block explorer is clean.

I used Foundry's deployment scripts:

```bash
forge script script/Deploy.s.sol:Deploy \
  --rpc-url https://rpc.testnet.arc.network \
  --broadcast \
  --legacy
```

Within minutes, all three contracts were live and verified. You can actually see them on Arc testnet explorer - real contracts with real code.

The moment when I created the first intent through the UI and saw it appear on the Arc explorer... that's the hackathon high right there.

## Why I Used Arc L1

Here are some benefits with Circle's Arc Chain

### 1. Native USDC Integration

Arc uses USDC as its native gas token. This is brilliant for a DeFi intent system because:

- No need for users to hold separate gas tokens
- All payments are already in USDC
- Seamless integration with traditional finance via AP2

### 2. EVM Compatibility with Modern Features

Arc is EVM-compatible but built from scratch with modern standards. I could use familiar Solidity patterns while leveraging:

- Faster block times (2-second finality)
- Lower gas costs
- Better tooling support

### 3. The Google's AP2 Protocol

Using Google's Agent Payments Protocol (AP2) on Arc Chain is game-changing. It lets you verify off-chain payments (like Stripe) on-chain. In Arc AI Agents, the PaymentRouter contract can:

- Accept traditional credit card payments via Stripe
- Verify the payment happened using Circle's oracle
- Release escrow atomically

This bridges TradFi and DeFi in a way that's actually usable.

### 4. Early Ecosystem Opportunity

Arc is brand new (testnet launched recently). Being an early builder means:

- Early presence in the ecosystem
- Direct feedback from the Arc team
- Potential for future grants/support
- Chance to define standards

## The Numbers: What We Achieved

After 72 hours of focused building, here's what shipped:

**Smart Contracts:**

- 3 production contracts (740 LOC total)
- 27 Foundry tests (100% passing)
- Deployed and verified on Arc testnet

**AI Agents:**

- 5 specialized agents with distinct roles
- LangGraph orchestration with conditional routing
- Real-time streaming outputs
- Structured outputs with confidence scores

**Full Stack:**

- FastAPI backend with async endpoints
- Streamlit UI with live agent visualization
- Arc L1 integration with contract calls
- Real-time transaction tracking

**Performance:**

- Intent matching: 2-5 seconds end-to-end
- Agent reasoning: 1-3 seconds per agent
- On-chain settlement: < 10 seconds (Arc's 2s block time)
- Cost per intent: ~$0.10 (LLM API calls)

## The Architecture: Hybrid Intelligence

The key architectural decision was to keep AI off-chain and settlement on-chain. Here's why this hybrid approach works:

### Off-Chain: AI Coordination Layer

All the "thinking" happens off-chain using LangGraph:

```
Intent → Matching Agent → Market Agent → Fraud Agent → Risk Agent → Settlement Agent → On-Chain Settlement
```

Each agent:

1. Receives shared state (intent data, previous agent outputs)
2. Calls LLM API (Claude or Gemini)
3. Returns structured decision with reasoning
4. Updates state for next agent

This gives us:

- **Speed**: LLM inference in seconds (not minutes)
- **Cost**: $0.05-0.10 per intent (not $10-50 on-chain)
- **Flexibility**: Update prompts without contract upgrades
- **Explainability**: Full reasoning chain visible

### On-Chain: Trustless Settlement

The settlement flow on Arc L1:

1. **Intent Registration**
```solidity
function registerIntent(
    IntentType intentType,
    address asset,
    uint256 price,
    uint256 quantity
) external returns (bytes32 intentId);
```
2. **Escrow Creation** (when match found)
```solidity
function createEscrow(
    bytes32 buyIntentId,
    bytes32 sellIntentId,
    uint256 amount
) external returns (uint256 escrowId);
```
3. **Atomic Settlement**
```solidity
function settleEscrow(uint256 escrowId) external {
    // Verify both parties deposited
    // Transfer assets atomically
    // Emit settlement event
}
```
### Why This Architecture Scales

**Off-Chain Advantages:**

- LLM inference: 1-5 seconds per agent (vs minutes on-chain)
- Cost: $0.10 per intent (vs $10-50 on-chain computation)
- Flexibility: Update agent prompts without contract upgrades

**On-Chain Advantages:**

- Trustless settlement: No one can rug pull
- Composability: Other contracts can read intent data
- Transparency: All settlements verifiable

The hybrid approach combines the strengths of both.

## For Builders: Key Takeaways for AI Hackathons

If you're building at the intersection of AI and blockchain for your next **AI hackathon**, here's what I learned from this **artificial intelligence hackathon**:

### 1. Use the Right Tool for Each Layer

- **AI Layer**: LangGraph for orchestration, Claude/Gemini for reasoning
- **API Layer**: FastAPI for Python (fast, async, auto-docs)
- **Blockchain Layer**: Foundry for contracts (good testing experience)
- **UI Layer**: Streamlit for MVPs (insanely fast to build)

### 2. Start with the Contract Tests

Write your smart contract tests first. It forces you to think through edge cases and gives you confidence to build the rest of the stack.

### 3. Make AI Decisions Explainable

Always include reasoning and confidence scores in LLM outputs. Users need to understand why the system made a decision, especially in finance.

### 4. Stream Everything

Use server-sent events or WebSockets to stream agent progress to the UI. Real-time feedback makes the experience magical.

### 5. Deploy Early and Often

I deployed to Arc testnet on day 2. Having real on-chain contracts motivated me and caught integration bugs early.

## The Business Case: Why This Could Be Big

Let's talk market opportunity (because judges and investors care):

### The Intent Economy is Exploding

**Market Size:**

- Global DeFi TVL: $50B+ (2024)
- Intent-based protocols: Growing 300% YoY
- OTC trading: $500B+ annually

**Adoption Drivers:**

- Uniswap X (UniswapX), CoW Protocol, 1inch Fusion all betting on intents
- Users prefer "I want to buy BTC" over manual DEX interactions
- Professional traders need sophisticated execution strategies

### Revenue Model

**Transaction Fees** (Primary)

- 0.1-0.3% fee per matched intent
- At 1M intents/month averaging $1,000 each → $1-3M/month revenue
- 95% gross margins (LLM costs: $0.05/transaction)

**Enterprise API** (Secondary)

- $500-$5,000/month per protocol integration
- Custom agents, SLA guarantees, dedicated support
- Target: 50 protocols in year 1 → $300K-$3M ARR

**White-Label Solutions** (High-Margin)

- One-time deployment: $50K-$200K per protocol
- Custom agent development for specific verticals
- Target: 5-10 deployments in year 1 → $500K-$2M

## Final Thoughts: Why This Matters

We're at an inflection point in technology. For the first time, we have:

1. **Smart contracts** that can enforce trustless execution
2. **LLMs** that can understand context and reason
3. **Fast L1s like Arc** that can handle real-time settlement
4. **TradFi bridges like AP2** that connect to existing finance

These pieces weren't ready 2 years ago. They are now.

The future of finance isn't purely decentralized (too rigid) or purely centralized (too risky). It's **agentic and hybrid** - AI agents handling intelligent coordination, smart contracts handling trustless settlement, and bridges connecting both worlds.

Arc AI Agents is my bet on that future. I built it in 72 hours during this **AI hackathon** to prove it's possible. This experience demonstrates what's achievable in **online AI hackathons** when you combine the right tools, clear architecture, and focused execution.

## Build it at an AI hackathon

If this build gives you ideas, an AI hackathon is a good place to try them under a deadline. A short time limit pushes you to keep the scope small and to deploy early, as this project did on day 2. See the list of [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

### What is an AI hackathon?

An **AI hackathon** (also called an artificial intelligence hackathon) is a time-limited competitive event where developers, data scientists, and AI engineers collaborate to build innovative AI solutions. These events, whether **online AI hackathons**, **virtual AI hackathons**, or hybrid formats, bring together global teams to solve real-world problems using AI technologies.

### How do AI hackathons work?

**AI hackathons** typically follow this structure:

1. **Registration**: Teams or individuals sign up for the event
2. **Kickoff**: Organizers present challenges, APIs, and resources
3. **Development**: Teams have 24-72 hours to build their solutions
4. **Submission**: Projects are submitted with demos and documentation
5. **Judging**: Judges evaluate projects on innovation, technical merit, and impact
6. **Awards**: Winners receive prizes, recognition, and sometimes job opportunities

### How long do AI hackathons last?

Most **AI hackathons** last between 24-72 hours, though some extended events can span a week. The AI Agents on Arc hackathon was a 72-hour event, which is typical for **online AI hackathons** that allow participants to work from anywhere in the world.
