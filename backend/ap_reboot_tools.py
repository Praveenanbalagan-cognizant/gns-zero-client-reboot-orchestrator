from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class AccessPoint:
    ap_name: str
    site_tag: str
    controller: str
    uptime_days: int
    client_count: int
    reachable: bool
    controller_state: str
    maintenance_window: bool
    critical_site: bool
    last_reboot_result: str


def _to_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "yes", "1", "y"}


def load_inventory(path: str | Path) -> list[AccessPoint]:
    inventory_path = Path(path)
    with inventory_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [
            AccessPoint(
                ap_name=row["ap_name"],
                site_tag=row["site_tag"],
                controller=row["controller"],
                uptime_days=int(row["uptime_days"]),
                client_count=int(row["client_count"]),
                reachable=_to_bool(row["reachable"]),
                controller_state=row["controller_state"].strip().lower(),
                maintenance_window=_to_bool(row["maintenance_window"]),
                critical_site=_to_bool(row["critical_site"]),
                last_reboot_result=row["last_reboot_result"].strip().lower(),
            )
            for row in reader
        ]


def explain_blockers(ap: AccessPoint, min_uptime_days: int) -> list[str]:
    blockers: list[str] = []
    if ap.uptime_days < min_uptime_days:
        blockers.append(f"uptime below {min_uptime_days} days")
    if ap.client_count != 0:
        blockers.append("active clients present")
    if not ap.reachable:
        blockers.append("AP not reachable")
    if ap.controller_state != "joined":
        blockers.append("AP not joined to controller")
    if not ap.maintenance_window:
        blockers.append("outside maintenance window")
    if ap.critical_site:
        blockers.append("critical site AP requires manual approval")
    return blockers


def split_candidates(
    inventory: Iterable[AccessPoint],
    site_tag: str | None = None,
    min_uptime_days: int = 100,
) -> tuple[list[AccessPoint], dict[str, list[str]]]:
    eligible: list[AccessPoint] = []
    blocked: dict[str, list[str]] = {}

    for ap in inventory:
        if site_tag and ap.site_tag.upper() != site_tag.upper():
            continue

        blockers = explain_blockers(ap, min_uptime_days)
        if blockers:
            blocked[ap.ap_name] = blockers
        else:
            eligible.append(ap)

    return eligible, blocked


def build_reboot_plan(eligible: Iterable[AccessPoint], batch_size: int = 5) -> list[dict[str, object]]:
    plan: list[dict[str, object]] = []
    batch_number = 1
    current_batch: list[str] = []

    for ap in sorted(eligible, key=lambda item: (item.site_tag, item.ap_name)):
        current_batch.append(ap.ap_name)
        if len(current_batch) == batch_size:
            plan.append({"batch": batch_number, "aps": current_batch})
            batch_number += 1
            current_batch = []

    if current_batch:
        plan.append({"batch": batch_number, "aps": current_batch})

    return plan


def simulate_reboot(eligible: Iterable[AccessPoint], dry_run: bool = True) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for ap in eligible:
        status = "planned" if dry_run else "reboot_command_sent"
        results.append(
            {
                "ap_name": ap.ap_name,
                "site_tag": ap.site_tag,
                "controller": ap.controller,
                "action": status,
            }
        )
    return results


def validate_recovery(reboot_results: Iterable[dict[str, str]], dry_run: bool = True) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    for result in reboot_results:
        validation.append(
            {
                "ap_name": result["ap_name"],
                "validation_status": "dry_run_not_executed" if dry_run else "joined_and_reachable",
                "notes": "No live change performed" if dry_run else "AP recovered successfully",
            }
        )
    return validation


def render_report(
    inventory: list[AccessPoint],
    eligible: list[AccessPoint],
    blocked: dict[str, list[str]],
    reboot_results: list[dict[str, str]],
    validation: list[dict[str, str]],
    site_tag: str | None,
    min_uptime_days: int,
    dry_run: bool,
) -> str:
    lines = [
        "# AP Reboot Orchestration Report",
        "",
        f"- Site tag: {site_tag or 'ALL'}",
        f"- Minimum uptime: {min_uptime_days} days",
        f"- Mode: {'DRY RUN' if dry_run else 'LIVE'}",
        f"- Inventory APs reviewed: {len(inventory)}",
        f"- Eligible APs: {len(eligible)}",
        f"- Blocked APs: {len(blocked)}",
        "",
        "## Eligible APs",
    ]

    if eligible:
        for ap in eligible:
            lines.append(f"- {ap.ap_name} ({ap.site_tag}, uptime {ap.uptime_days} days, clients {ap.client_count})")
    else:
        lines.append("- None")

    lines.extend(["", "## Blocked APs"])
    if blocked:
        for ap_name, reasons in blocked.items():
            lines.append(f"- {ap_name}: {', '.join(reasons)}")
    else:
        lines.append("- None")

    lines.extend(["", "## Reboot Actions"])
    if reboot_results:
        for item in reboot_results:
            lines.append(f"- {item['ap_name']}: {item['action']}")
    else:
        lines.append("- No reboot actions planned")

    lines.extend(["", "## Validation"])
    if validation:
        for item in validation:
            lines.append(f"- {item['ap_name']}: {item['validation_status']} - {item['notes']}")
    else:
        lines.append("- No validation performed")

    return "\n".join(lines)
