# Project Summary

## GNS Zero-Client Reboot Orchestrator

GNS Zero-Client Reboot Orchestrator is an agentic wireless operations assistant built for the Neuro SAN hackathon. The project focuses on a real operational problem: safely rebooting wireless access points that have very high uptime while avoiding user impact. In large wireless environments, APs may remain online for more than 100 days. Periodic maintenance can help reduce instability, but manual selection is time-consuming and bulk reboot actions can be risky if an AP still has connected users or if the device is part of a critical site.

This project improves the AP reboot process by adding a Neuro SAN multi-agent orchestration layer over a deterministic Python tool. The Python tool performs the actual operational checks, while the agents reason through the workflow, explain decisions, and produce a clear report. The repository includes a live Neuro SAN direct-agent run path using NVIDIA/NVAPI, plus a deterministic dry-run path for safe fallback demonstration. The goal is not to replace the wireless engineer; the goal is to give the engineer a safer and faster decision-support workflow.

## Problem Statement

Traditional AP reboot automation usually works like a script: collect APs, filter by a few fields, run a reboot command, and export a result. That approach is useful, but it does not clearly explain why a device was selected or skipped. It also does not naturally separate responsibilities such as inventory review, risk validation, execution, and post-check reporting.

For a hackathon project, this is a strong fit for Neuro SAN because the AP reboot process can be represented as a network of specialist agents. Each agent has a focused responsibility, and the overall system produces an operator-friendly answer instead of only raw command output.

## Solution

The system uses a front agent called `Wireless Reboot Copilot`. This agent coordinates six specialist agents:

- Inventory Agent
- Eligibility Agent
- Risk Agent
- Execution Agent
- Validation Agent
- Report Agent

The workflow begins when the engineer asks for safe AP reboot candidates, usually with a site tag and maintenance rule. The inventory agent reads the AP inventory. The eligibility agent checks whether AP uptime is above the configured threshold and whether active client count is zero. The risk agent blocks unsafe APs, such as APs that are unreachable, not joined to the controller, outside the maintenance window, or marked as critical. The execution agent defaults to dry-run mode for safety. The validation agent checks recovery state after the reboot action. Finally, the report agent produces a concise Markdown report.

## Agentic Value

The agentic design is the main differentiator. A normal automation script can reboot APs, but this project creates a reviewable decision process:

- It decomposes the request into multiple operational responsibilities.
- It uses specialist agents instead of one monolithic prompt.
- It combines agent reasoning with deterministic Python guardrails.
- It creates a clear audit trail for selected and blocked APs.
- It supports safe demonstration through synthetic data and dry-run mode.

This design directly supports the hackathon scoring areas:

- Novelty: agentic closed-loop wireless maintenance, not only chatbot Q&A.
- Neuro SAN features: multi-agent network, coded tool integration, task delegation, and final synthesis.
- Code quality: clean separation between agent orchestration, safety logic, sample data, and reporting.

## Safety and Compliance

The hackathon version uses only synthetic AP inventory. The sample AP names, site tags, and controller fields are not real client data. The tool defaults to dry-run mode and does not connect to a live controller. This makes the demo safe and compliant while still showing the full operational workflow.

For production use, the live reboot function should be connected only to approved wireless controller APIs and protected with operator approval, change ticket reference, controller allowlist, batch limit, and post-reboot stop conditions.

## Demo Scenario

The demo shows an engineer asking:

`Find APs that are safe to reboot for site tag BLR-CAMPUS. Use uptime greater than 100 days, zero clients only, dry-run mode, and generate the validation report.`

The system then:

1. Sends the prompt to the Neuro SAN front agent.
2. Delegates the request across the inventory, eligibility, risk, execution, validation, and report agents.
3. Calls the coded AP reboot tool against synthetic AP inventory.
4. Finds APs matching the site tag.
5. Selects APs with uptime greater than 100 days and zero clients.
6. Blocks APs that fail safety checks.
7. Creates a dry-run reboot plan.
8. Simulates validation.
9. Generates a final report.

## Expected Impact

The project can reduce manual AP review time, reduce user-impact risk, and give wireless engineers a repeatable maintenance workflow. It also gives managers and reviewers a readable summary of why specific APs were selected or skipped.

The final result is a practical agentic AI project grounded in real wireless operations: a safe AP reboot copilot that is useful, explainable, and demo-ready.
