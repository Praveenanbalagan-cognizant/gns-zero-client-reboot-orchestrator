from __future__ import annotations

import os
import sys
from pathlib import Path


DEMO_PROMPT = (
    "Find APs that are safe to reboot for site tag BLR-CAMPUS. "
    "Use uptime greater than 100 days, zero clients only, dry-run mode, "
    "and generate the validation report."
)


def invoke_live_agent(prompt: str = DEMO_PROMPT) -> str:
    """Call the Neuro SAN agent network directly with the user's prompt."""
    repo_root = Path(__file__).resolve().parents[1]
    backend_path = repo_root / "backend"
    agent_path = repo_root / "backend" / "registries" / "ap_reboot_orchestrator.hocon"

    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

    if not os.getenv("NVIDIA_API_KEY"):
        raise RuntimeError(
            "NVIDIA_API_KEY is missing. Set it in PowerShell before running the live Neuro SAN agent."
        )

    from neuro_san.client.simple_one_shot import SimpleOneShot

    previous_cwd = Path.cwd()
    try:
        os.chdir(repo_root)
        return SimpleOneShot(
            agent=str(agent_path),
            connection_type="direct",
        ).get_answer_for(prompt)
    finally:
        os.chdir(previous_cwd)


if __name__ == "__main__":
    user_prompt = " ".join(sys.argv[1:]).strip() or DEMO_PROMPT
    print(invoke_live_agent(user_prompt))
