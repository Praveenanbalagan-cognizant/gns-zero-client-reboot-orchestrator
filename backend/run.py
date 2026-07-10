from __future__ import annotations

from pathlib import Path

from ap_reboot_tools import (
    build_reboot_plan,
    load_inventory,
    render_report,
    simulate_reboot,
    split_candidates,
    validate_recovery,
)


def invoke_agent(
    site_tag: str = "BLR-CAMPUS",
    min_uptime_days: int = 100,
    dry_run: bool = True,
) -> str:
    repo_root = Path(__file__).resolve().parents[1]
    inventory_path = repo_root / "data" / "sample_ap_inventory.csv"

    inventory = load_inventory(inventory_path)
    eligible, blocked = split_candidates(
        inventory=inventory,
        site_tag=site_tag,
        min_uptime_days=min_uptime_days,
    )
    reboot_plan = build_reboot_plan(eligible)
    reboot_results = simulate_reboot(eligible, dry_run=dry_run)
    validation = validate_recovery(reboot_results, dry_run=dry_run)

    header = [
        "GNS Zero-Client Reboot Orchestrator",
        "===================================",
        f"Site tag: {site_tag}",
        f"Eligible APs: {', '.join(ap.ap_name for ap in eligible) or 'None'}",
        f"Blocked AP count: {len(blocked)}",
        f"Reboot batches: {reboot_plan}",
        "",
    ]

    report = render_report(
        inventory=inventory,
        eligible=eligible,
        blocked=blocked,
        reboot_results=reboot_results,
        validation=validation,
        site_tag=site_tag,
        min_uptime_days=min_uptime_days,
        dry_run=dry_run,
    )
    return "\n".join(header) + report


if __name__ == "__main__":
    print(invoke_agent())
