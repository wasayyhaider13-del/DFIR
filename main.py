"""
main.py — DFIR System Entry Point
===================================
DFIR Module 8: Command-line orchestrator for all system modes.
"""

import sys
import argparse
import datetime

from colorama import Fore, Style, init

init(autoreset=True)

# ── Banner ─────────────────────────────────────────────────────────────────────

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
║  🔍  DFIR Real-Time Browser Forensics System         ║
║      AI-Driven Incident Response Platform            ║
╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

def _print_banner() -> None:
    print(BANNER)
    print(f"  Start time : {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print()


# ── Mode handlers ──────────────────────────────────────────────────────────────

def run_scan() -> None:
    from extractor      import extract_chrome_history
    from timeline       import reconstruct_timeline
    from ioc_detector   import detect_iocs
    from llm_classifier import classify_all_events
    from alerter        import send_alerts

    print(f"{Fore.CYAN}[MAIN] Mode: SCAN{Style.RESET_ALL}\n")

    records = extract_chrome_history()
    if not records:
        print(f"{Fore.YELLOW}[MAIN] No browser history found. Exiting.{Style.RESET_ALL}")
        return

    timeline = reconstruct_timeline(records)
    flagged = detect_iocs(timeline)
    classified = classify_all_events(flagged) if flagged else []
    alerts_sent = send_alerts(classified)

    print(f"\n{Fore.GREEN}[MAIN] Scan complete.{Style.RESET_ALL}")
    print(f"  Events extracted : {len(records)}")
    print(f"  Timeline events  : {len(timeline)}")
    print(f"  Flagged IOCs     : {len(flagged)}")
    print(f"  LLM classified   : {len(classified)}")
    print(f"  Alerts sent      : {alerts_sent}")


def run_live(interval: int) -> None:
    from monitor import start_monitor

    print(f"{Fore.CYAN}[MAIN] Mode: LIVE MONITOR (interval: {interval}s){Style.RESET_ALL}\n")
    start_monitor(interval_seconds=interval)


def run_report() -> None:
    from reporter import generate_report

    print(f"{Fore.CYAN}[MAIN] Mode: REPORT{Style.RESET_ALL}\n")
    report_path = generate_report()
    print(f"\n{Fore.GREEN}[MAIN] Report generated: {report_path}{Style.RESET_ALL}")


# ── CLI parser ────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dfir",
        description="DFIR Real-Time Browser Forensics & AI Incident Response System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--mode",
        choices=["live", "scan", "report"],
        default="scan",  # ✅ Default mode added
        help="Operation mode (default: scan)",
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=None,
        metavar="SECONDS",
        help="Interval for live mode",
    )

    return parser


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    _print_banner()

    parser = _build_parser()
    args = parser.parse_args()  # ✅ FIXED

    import config
    interval = args.interval or config.SCAN_INTERVAL_SECONDS

    try:
        if args.mode == "scan":
            run_scan()
        elif args.mode == "live":
            run_live(interval=interval)
        elif args.mode == "report":
            run_report()

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[MAIN] Interrupted by user.{Style.RESET_ALL}")
        sys.exit(0)

    except Exception as exc:
        print(f"\n{Fore.RED}[MAIN] Fatal error: {exc}{Style.RESET_ALL}")
        raise


if __name__ == "__main__":
    main()

    from utils import save_logs

def run_scan():
    from extractor import extract_chrome_history
    from timeline import reconstruct_timeline
    from ioc_detector import detect_iocs
    from llm_classifier import classify_all_events
    from alerter import send_alerts

    records = extract_chrome_history()
    timeline = reconstruct_timeline(records)
    flagged = detect_iocs(timeline)
    classified = classify_all_events(flagged)

    save_logs(classified)
    send_alerts(classified)