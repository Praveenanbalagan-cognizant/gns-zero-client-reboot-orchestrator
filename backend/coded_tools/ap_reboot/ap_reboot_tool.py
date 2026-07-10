from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from neuro_san.interfaces.coded_tool import CodedTool
except ImportError:
    class CodedTool:  # type: ignore[no-redef]
        """Fallback so the tool can be imported in standalone demos."""


try:
    from backend.ap_reboot_tools import (
        build_reboot_plan,
        load_inventory,
        render_report,
        simulate_reboot,
        split_candidates,
        validate_recovery,
    )
except ImportError:
    from ap_reboot_tools import (
        build_reboot_plan,
        load_inventory,
        render_report,
        simulate_reboot,
        split_candidates,
        validate_recovery,
    )


class APRebootTool(CodedTool):
    """Neuro SAN coded tool for AP reboot planning and validation."""

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any] | str:
        repo_root = Path(__file__).resolve().parents[3]
        inventory_path = Path(args.get("inventory_path", repo_root / "data" / "sample_ap_inventory.csv"))
        site_tag = args.get("site_tag")
        min_uptime_days = int(args.get("min_uptime_days", 100))
        batch_size = int(args.get("batch_size", 5))
        dry_run = bool(args.get("dry_run", True))
        action = str(args.get("action", "full_report")).lower()

        inventory = load_inventory(inventory_path)
        eligible, blocked = split_candidates(inventory, site_tag=site_tag, min_uptime_days=min_uptime_days)
        reboot_plan = build_reboot_plan(eligible, batch_size=batch_size)
        reboot_results = simulate_reboot(eligible, dry_run=dry_run)
        validation = validate_recovery(reboot_results, dry_run=dry_run)

        response = {
            "site_tag": site_tag or "ALL",
            "min_uptime_days": min_uptime_days,
            "dry_run": dry_run,
            "eligible_aps": [ap.ap_name for ap in eligible],
            "blocked_aps": blocked,
            "reboot_plan": reboot_plan,
            "reboot_results": reboot_results,
            "validation": validation,
        }

        if action in {"report", "full_report"}:
            response["report"] = render_report(
                inventory=inventory,
                eligible=eligible,
                blocked=blocked,
                reboot_results=reboot_results,
                validation=validation,
                site_tag=site_tag,
                min_uptime_days=min_uptime_days,
                dry_run=dry_run,
            )

        return response
