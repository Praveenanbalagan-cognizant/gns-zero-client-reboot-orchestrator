# GNS Zero-Client Reboot Orchestrator

A Neuro SAN based wireless operations assistant that identifies APs with high uptime, confirms zero-client status, applies safety guardrails, creates a dry-run reboot plan, validates recovery, and generates an audit-ready report.

This project uses synthetic AP data only. No client data, production AP inventory, controller credentials, or internal logs are included.

## Prerequisites

- Python 3.13
- NVIDIA/NVAPI key for the full Neuro SAN agent run

The standalone dry-run backend works without an API key.

## Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If package metadata downloads are blocked by network policy, the standalone backend can still be demonstrated without installing Neuro SAN or Streamlit.

### 3. Set NVIDIA/NVAPI key for full agent run

Set the key only in your local PowerShell session:

```powershell
$env:NVIDIA_API_KEY="paste-your-nvapi-key-here"
```

Confirm it is set without printing the key:

```powershell
python -c "import os; print('NVIDIA_API_KEY is set' if os.getenv('NVIDIA_API_KEY') else 'missing')"
```

Do not commit API keys or `.env` files.

## Running the Project

### Standalone backend dry run

This path does not require an API key:

```powershell
python backend\run.py
```

Expected result:

```text
Eligible APs: AP-BLR-01, AP-BLR-03
Blocked AP count: 4
Mode: DRY RUN
```

### Live Neuro SAN agent run

This path talks to the Neuro SAN agent network through the NVIDIA/NVAPI-backed LLM:

```powershell
python backend\live_agent.py
```

### Browser dry-run demo

This path is the fastest demo option and does not require Streamlit, an API key, or a controller connection:

```powershell
python -m http.server 8765
```

Then open:

```text
http://localhost:8765/frontend/browser_demo.html
```

### Optional Streamlit frontend

```powershell
python -m streamlit run frontend\run.py
```

### Optional Neuro SAN registry validation

```powershell
python -m neuro_san.client.hocon_validator_cli backend/registries/ap_reboot_orchestrator.hocon
```

## Project Structure

```text
gns-zero-client-reboot-orchestrator/
|-- backend/
|   |-- run.py
|   |-- ap_reboot_tools.py
|   |-- registries/
|   |   |-- manifest.hocon
|   |   |-- ap_reboot_orchestrator.hocon
|   |   |-- llm_config.hocon
|   |   `-- aaosa.hocon
|   `-- coded_tools/
|       `-- ap_reboot/
|           |-- __init__.py
|           `-- ap_reboot_tool.py
|-- frontend/
|   `-- run.py
|-- data/
|   `-- sample_ap_inventory.csv
|-- requirements.txt
|-- architecture.md
|-- summary.md
`-- README.md
```

## How It Works

The project is designed as a multi-agent wireless maintenance workflow:

| Agent | Role |
|---|---|
| `Wireless_Reboot_Copilot` | Front agent that coordinates the AP reboot workflow |
| `Inventory_Agent` | Reviews AP inventory by site tag, uptime, clients, reachability, and controller state |
| `Eligibility_Agent` | Selects APs with uptime above threshold and zero active clients |
| `Risk_Agent` | Blocks APs that are unsafe to reboot |
| `Execution_Agent` | Creates dry-run or approved reboot batches |
| `Validation_Agent` | Validates AP recovery state |
| `Report_Agent` | Generates the final report |
| `APRebootTool` | Python coded tool that performs deterministic checks and reporting |

The browser demo mirrors this workflow visually for recording and fallback demonstration.

## Demo Prompt

```text
Find APs that are safe to reboot for site tag BLR-CAMPUS. Use uptime greater than 100 days, zero clients only, dry-run mode, and generate the validation report.
```

## Safety Notes

- Dry-run mode is the default.
- The demo uses synthetic AP data.
- The project does not connect to a real wireless controller.
- A production version should require operator approval, maintenance window validation, controller allowlist, batch limits, and post-reboot stop conditions.
