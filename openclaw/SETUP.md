# Hermes Agent — Gemini AI Agent Setup Guide

Turn your Hermes CLI into a full AI-powered Hedera trading agent on any messaging platform.

## What You Get

- A dedicated **Hedera wallet agent** on Telegram, Discord, WhatsApp, or any Gemini AI Agent channel
- **Twice-daily portfolio monitoring** (6 AM / 6 PM) with proactive alerts
- **Background daemons** for Power Law rebalancing and limit orders
- Full conversational trading: "swap 5 USDC for HBAR", "what's bitcoin doing?", "send 10 HBAR to 0.0.xxx"

## Prerequisites

1. **Hermes CLI** installed and working (`./launch.sh balance` returns your portfolio)
2. **Gemini AI Agent** installed
3. A **Telegram bot token** (optional — for Telegram routing)

---

## Step 1: Install Hermes

```bash
git clone https://github.com/raunet234/hermes.git
cd hermes
./launch.sh setup        # Configure wallet keys
./launch.sh doctor       # Verify system health
./launch.sh balance      # Confirm it works
```

## Step 2: Create the Hermes Agent

```bash
openclaw agents add hermes
```

Set the workspace to this `openclaw/` directory:

```bash
# Option A: Set workspace directly
openclaw agents set hermes --workspace /path/to/hermes/openclaw

# Option B: Symlink into Gemini AI Agent's workspace directory
ln -s /path/to/hermes/openclaw ~/.openclaw/workspace-hermes
```

## Step 3: Link the Skill & Copy Defaults

```bash
# Link the skill
cd /path/to/hermes/openclaw/skills/hermes-hedera
ln -s ../../../SKILL.md SKILL.md

# Copy default user files (customize these for your setup)
cp /path/to/hermes/openclaw/defaults/USER.md /path/to/hermes/openclaw/USER.md
cp /path/to/hermes/openclaw/defaults/MEMORY.md /path/to/hermes/openclaw/MEMORY.md
```

The symlink means SKILL.md updates automatically when the Hermes repo is updated. USER.md and MEMORY.md are gitignored — they're personal to each operator.

## Step 4: Configure Gemini AI Agent

Edit `~/.openclaw/openclaw.json`. Choose a configuration below based on your setup.

### A) Hermes Only (Simplest)

One agent, one channel. Everything goes to Hermes.

```json5
{
  agents: {
    list: [
      {
        id: "hermes",
        default: true,
        name: "Hermes",
        workspace: "/path/to/hermes/openclaw"
      }
    ]
  }
}
```

### B) Hermes + Your Existing Agent

Keep your default Gemini AI Agent for general tasks. Route a specific Telegram bot to Hermes.

```json5
{
  agents: {
    list: [
      {
        id: "default",
        default: true,
        name: "Assistant",
        workspace: "~/.openclaw/workspace-default"
      },
      {
        id: "hermes",
        name: "Hermes",
        workspace: "/path/to/hermes/openclaw"
      }
    ]
  },
  bindings: [
    // Route a dedicated Telegram bot to Hermes
    {
      agentId: "hermes",
      match: { channel: "telegram", accountId: "hermes-bot" }
    },
    // Everything else goes to default
    {
      agentId: "default",
      match: {}
    }
  ],
  channels: {
    telegram: {
      accounts: {
        default: {
          botToken: "YOUR_MAIN_BOT_TOKEN"
        },
        "hermes-bot": {
          botToken: "YOUR_HERMES_BOT_TOKEN",
          dmPolicy: "pairing"
        }
      }
    }
  }
}
```

**How to get a second Telegram bot:**
1. Open Telegram, find **@BotFather**
2. Send `/newbot`, name it "Hermes Wallet" (or similar)
3. Copy the bot token into `YOUR_HERMES_BOT_TOKEN`

### C) Route by Chat (Single Bot, Multiple Agents)

Use one Telegram bot but route specific group chats to Hermes.

```json5
{
  agents: {
    list: [
      { id: "default", default: true, workspace: "~/.openclaw/workspace-default" },
      { id: "hermes", name: "Hermes", workspace: "/path/to/hermes/openclaw" }
    ]
  },
  bindings: [
    // This specific group chat goes to Hermes
    {
      agentId: "hermes",
      match: {
        channel: "telegram",
        peer: { kind: "group", id: "-1001234567890" }
      }
    },
    // Everything else stays default
    { agentId: "default", match: {} }
  ]
}
```

To find a Telegram group chat ID: add your bot to the group, send a message, then check `https://api.telegram.org/bot<TOKEN>/getUpdates`.

### D) Multi-Channel (Telegram + Discord)

Same Hermes agent, reachable from multiple platforms.

```json5
{
  agents: {
    list: [
      {
        id: "hermes",
        default: true,
        name: "Hermes",
        workspace: "/path/to/hermes/openclaw"
      }
    ]
  },
  channels: {
    telegram: {
      accounts: {
        default: {
          botToken: "YOUR_TELEGRAM_BOT_TOKEN",
          dmPolicy: "pairing"
        }
      }
    },
    discord: {
      accounts: {
        default: {
          botToken: "YOUR_DISCORD_BOT_TOKEN"
        }
      }
    }
  }
}
```

### E) WhatsApp Setup

WhatsApp uses QR pairing instead of a bot token.

```json5
{
  agents: {
    list: [
      {
        id: "hermes",
        default: true,
        workspace: "/path/to/hermes/openclaw"
      }
    ]
  },
  channels: {
    whatsapp: {
      accounts: {
        default: {
          dmPolicy: "pairing"
        }
      }
    }
  }
}
```

Then run `openclaw channels pair whatsapp` and scan the QR code with your phone.

## Step 5: Set Up the Heartbeat (Cron)

The heartbeat checks your portfolio, daemons, and orders twice daily.

```bash
# 6 AM daily check
openclaw cron add \
  --name "hermes-morning" \
  --cron "0 6 * * *" \
  --agent hermes \
  --session isolated \
  --announce telegram:default \
  --message "Run the HEARTBEAT.md checklist"

# 6 PM daily check
openclaw cron add \
  --name "hermes-evening" \
  --cron "0 18 * * *" \
  --agent hermes \
  --session isolated \
  --announce telegram:default \
  --message "Run the HEARTBEAT.md checklist"
```

Adjust the `--announce` channel to match your setup (e.g., `discord:default`, `whatsapp:default`).

## Step 6: Start Daemons & Verify

```bash
# Start Hermes background services
cd /path/to/hermes
./launch.sh daemon-start

# Verify agent is loaded
openclaw agents list --bindings

# Restart the gateway to pick up config changes
openclaw gateway restart

# Test with a chat
openclaw chat hermes
> hi
# Should see: portfolio overview, daemon status, action menu
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Skill not found" | Check symlink: `ls -la openclaw/skills/hermes-hedera/SKILL.md` |
| "exec failed" | Verify Hermes works standalone: `cd /path/to/hermes && ./launch.sh balance` |
| "daemon not running" | Run `./launch.sh daemon-start` from the Hermes repo |
| Agent suggests MoonPay with tokens available | SOUL.md rule — check it's loaded (`/context list` in chat) |
| "No route found" for a swap | Run `./launch.sh pools search <TOKEN>` to discover pools |
| Agent modifying config files | SOUL.md violation — check `openclaw agents list` shows correct workspace |

## Architecture

```
┌──────────────────────────────────────────────────┐
│  Gemini AI Agent Gateway                         │
│  ┌────────────┐  ┌───────────┐  ┌────────────┐  │
│  │  Telegram   │  │  Discord  │  │  WhatsApp  │  │
│  └─────┬──────┘  └─────┬─────┘  └─────┬──────┘  │
│        └───────────────┼───────────────┘         │
│                        ▼                         │
│              ┌─────────────────┐                 │
│              │  Hermes Agent   │                 │
│              │  (openclaw/)    │                 │
│              │                 │                 │
│              │  SOUL.md ◄──── loaded every turn  │
│              │  SKILL.md ◄─── loaded on demand   │
│              │  HEARTBEAT.md   ◄── 6AM + 6PM     │
│              └────────┬────────┘                 │
│                       ▼                          │
│              ./launch.sh <cmd>                   │
│                       ▼                          │
│              ┌─────────────────┐                 │
│              │  Hermes CLI     │                 │
│              │  (Python app)   │                 │
│              │                 │                 │
│              │  Daemon ──► PowerLaw rebalancer   │
│              │           ──► Limit order engine  │
│              │           ──► HCS signals         │
│              │           ──► Web dashboard       │
│              └─────────────────┘                 │
└──────────────────────────────────────────────────┘
```

## Files in This Workspace

| File | Loaded | Purpose |
|------|--------|---------|
| `SOUL.md` | Every turn | Core identity + unbreakable rules (~370 words) |
| `IDENTITY.md` | Every turn | Name and role (3 lines) |
| `BOOTSTRAP.md` | Every turn | Channel format table + safety limits |
| `USER.md` | Every turn | Your personal preferences |
| `AGENTS.md` | Every turn | Architecture guide for the agent |
| `MEMORY.md` | Private sessions | Long-term memory index |
| `HEARTBEAT.md` | Cron (2x/day) | Portfolio monitoring checklist |
| `skills/hermes-hedera/SKILL.md` | On demand | Full 965-line command reference |
