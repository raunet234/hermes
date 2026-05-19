# Hermes Tools — Environment-Specific Configuration

## Entry Point
All CLI commands: `./launch.sh <command>`
Working directory: The hermes repository root (where launch.sh lives)

## Accounts
- **Main**: `0.0.8995674` — user trading wallet
- **Robot**: `None` — autonomous rebalancer (nickname: "Bitcoin Rebalancer Daemon")
- Switch with: `./launch.sh account switch <id_or_nickname>`

## Daemons
- Start: `./launch.sh daemon-start`
- Stop: `./launch.sh daemon-stop`
- Status: `./launch.sh daemon-status`
- Dashboard: http://127.0.0.1:8088

## HCS Topics
- Signal topic: `0.0.10371598` — Power Law signals broadcast here
- Feedback topic: check with `./launch.sh hcs status`
- Check: `./launch.sh hcs status`

## Cross-Agent Feedback (HCS)
Submit bugs, suggestions, and successes to a shared HCS topic that all Hermes agents can read.
```
./launch.sh hcs feedback submit bug "description of the issue"
./launch.sh hcs feedback submit suggestion "improvement idea"
./launch.sh hcs feedback submit success "what worked well"
./launch.sh hcs feedback submit warning "potential concern"
./launch.sh hcs feedback read                    # read recent feedback
./launch.sh hcs feedback-setup                   # create a new feedback topic
```
**Rules**: Only submit genuine feedback. Each message costs ~$0.0008.
Never include private keys, passwords, or sensitive data — HCS messages are permanent and public.
Reference transaction IDs or hashscan URLs when reporting bugs so others can investigate.

## Network
- Network: Hedera Mainnet
- DEX: SaucerSwap V2
- RPC: https://mainnet.hashio.io/v1

## Key Commands for Quick Reference
```
./launch.sh balance --all --json  # ALL accounts in one call (main + robot + totals)
./launch.sh balance --json        # Active account only
./launch.sh status --json         # Full portfolio + account info
./launch.sh robot status --json   # Rebalancer state + Power Law signal
./launch.sh doctor                # System health check
./launch.sh daemon-status         # Check running daemons
./launch.sh history               # Recent transactions
./launch.sh price bitcoin         # Live BTC price + model
./launch.sh agent-sync            # Sync this workspace with codebase changes
```

## Full Command List
ALL COMMANDS
  ────────────────────────────────────────────────────────

  TRADING
  swap <amt> <A> for <B>                 Exact-in swap — spend exact amount, get best rate
  swap <A> for <amt> <B>                 Exact-out swap — receive exact amount, spend minimum
  swap-v1 <amt> <A> <B>                  SaucerSwap V1 (legacy AMM) swap
  price [token]                          Token prices from SaucerSwap V2
  slippage [%]                           View or set max slippage tolerance (default: 2%)

  PORTFOLIO
  balance [token]                        All token balances + USD values (or single token)
  status                                 Account + portfolio + robot snapshot
  history                                Recent execution history (swaps, transfers, staking)
  tokens                                 Supported token list with Hedera IDs & aliases
  nfts                                   View NFT inventory
  sources                                Price source breakdown (pool/contract IDs)

  TRANSFERS
  send <amt> <tk> to <rcp>               Transfer HBAR or any HTS token to an account
  receive [token]                        Show your address + check token association
  whitelist [add|remove]                 Manage trusted recipient addresses

  ACCOUNT
  account                                Show active wallet + known accounts
  account switch <name|id>               Switch active wallet
  associate <token|id>                   Link a token to your account
  setup                                  Create or import a wallet (guided wizard)
  fund                                   MoonPay/faucet link for funding
  backup-keys                            Export private key backup

  STAKING
  stake [node_id]                        Stake HBAR to a consensus node (default: Google)
  unstake                                Stop staking and clear node preference

  LIQUIDITY
  lp                                     View active LP positions (V2 NFTs)
  pool-deposit <amt> <A> <B> range <pct> Add liquidity (agent-friendly)
  pool-withdraw <nft> [amt|%|all]        Remove liquidity
  pools [list|search|approve]            Pool registry management

  LIMIT ORDERS
  order buy <tk> at <$> size N           Buy when price drops to target
  order sell <tk> at <$> size N          Sell when price rises to target
  order list                             View all open orders
  order cancel <id>                      Cancel an open order
  order on / off                         Start or stop the monitoring daemon

  ROBOT
  robot signal                           Show today's BTC Power Law signal
  robot status                           Show bot status, portfolio, and signal
  robot start                            Start the autonomous rebalancing daemon
  robot stop                             Stop the daemon

  MESSAGING (HCS)
  hcs status                             Show active signal topic
  hcs signals                            View recent investment signals
  hcs feedback submit <s> <d>            Report bug/suggestion to shared topic
  hcs feedback read                      Read recent cross-agent feedback
  hcs feedback-setup                     Create a feedback topic
  hcs10 setup                            Create public inbound topic
  hcs10 connect <topic_id>               Connect to another agent
  hcs10 send <id> <msg>                  Send message to connected agent

  SYSTEM
  doctor                                 Run system health diagnostics
  refresh                                Refresh pool & price data
  logs                                   View agent interaction log
  docs [name]                            Read reference docs (security, limits, readme, changelog)
  verbose [on/off]                       Toggle debug logging
  help [topic]                           Command help (help how <task> for workflows)

  EXAMPLES
  ────────────────────────────────────────────────────────
  swap 100 HBAR for USDC                 Exact-in: spend 100 HBAR, get best USDC rate
  swap HBAR for 10 USDC                  Exact-out: receive exactly 10 USDC, spend minimum HBAR
  swap 100 USDC for HBAR                 Spend 100 USDC, receive HBAR
  swap-v1 50 PACK HBAR                   Swap 50 PACK to HBAR via V1 legacy pool
  send 100 USDC to 0.0.1234              Transfer USDC to another Hedera account
  send 5 HBAR to 0.0.9876 memo Rent      Transfer with an on-chain memo
  associate USDC                         Link USDC to your account so you can receive it
  associate 0.0.456858                   Associate by Hedera token ID directly
  receive USDC                           Show your address + confirm USDC association status
  balance SAUCE                          Check SAUCE token balance
  price WBTC                             Get WBTC price from SaucerSwap
  stake 5                                Stake to consensus node 5 (Google)
  whitelist add 0.0.1234 Exchange        Whitelist an address with a label
  account --new                          Create a sub-account using your current key
  pools search PACK                      Find liquidity pools containing PACK
  pools approve 0.0.123456               Add a pool to your routing registry
  pool-deposit                           Start the interactive V2 liquidity wizard
  order buy HBAR at 0.08 size 100        Buy HBAR when price dips to $0.08
  order sell HBAR at 0.12 size 50        Sell HBAR when price reaches $0.12
  robot start                            Start the autonomous BTC rebalancer
  robot signal                           Check the model without trading
  doctor                                 Scan for environment bugs and AI-confusing issues
  hcs signals                            View recent investment signals from the swarm
  hcs topic create                       Create your own signal topic

---
*Auto-generated by `./launch.sh agent-sync` on 2026-05-18 10:29*
