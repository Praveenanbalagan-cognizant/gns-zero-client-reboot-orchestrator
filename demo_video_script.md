# Demo Video Script

Target length: 4 to 5 minutes.

## 0:00 - 0:30 - Opening

Say:

`Hi, this is GNS Zero-Client Reboot Orchestrator. It is a Neuro SAN based wireless operations assistant that helps engineers safely identify APs with high uptime, confirm zero-client status, run a dry-run reboot plan, validate recovery, and generate an audit-ready report.`

Show:

- Repo root.
- `README.md`.
- `architecture.md`.
- Synthetic sample inventory.

## 0:30 - 1:20 - Problem

Say:

`In wireless operations, APs with uptime greater than 100 days may need maintenance. The risk is that a direct bulk reboot can impact users if the AP still has clients or is part of a critical site. The project solves this by adding an agentic review layer before execution.`

Show:

- `data/sample_ap_inventory.csv`.
- Columns: site tag, uptime, clients, reachability, controller state, maintenance window.

## 1:20 - 2:20 - Architecture

Say:

`The Neuro SAN front agent is the Wireless Reboot Copilot. It delegates work to inventory, eligibility, risk, execution, validation, and reporting agents. These agents call a Python coded tool that performs deterministic checks. This keeps the LLM responsible for coordination and explanation, while Python handles safety-critical rules.`

Show:

- `architecture.md` diagram.
- `registries/ap_reboot_orchestrator.hocon`.
- `coded_tools/ap_reboot/ap_reboot_tool.py`.

## 2:20 - 3:30 - Live Demo

Run:

```powershell
python .\src\orchestrator_demo.py --inventory .\data\sample_ap_inventory.csv --site-tag BLR-CAMPUS --dry-run
```

Say:

`The system found candidate APs, blocked unsafe devices, created a dry-run plan, and generated a validation report. Notice that APs with active clients or failed safety checks are skipped with reasons.`

Show:

- Eligible APs.
- Blocked AP reasons.
- Dry-run plan.
- Final report.

## 3:30 - 4:20 - Neuro SAN Fit

Say:

`This is not just a script. The agent network decomposes wireless maintenance into specialist roles. It uses tool integration, task delegation, guardrails, and final report synthesis. That is why this project fits the hackathon scoring for novelty, Neuro SAN features, and code quality.`

Show:

- Agent roles in `architecture.md`.
- HOCON agent network.

## 4:20 - 5:00 - Closing

Say:

`The current demo uses synthetic data and dry-run mode for safety. In production, the same coded tool layer can be connected to approved controller APIs with operator approval, change ticket reference, batch limits, and post-reboot stop conditions. Thank you.`

Final screen:

- Final generated report.
- Repo file list.
