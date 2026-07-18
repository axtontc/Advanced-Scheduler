import argparse
import sys
import time
from datetime import datetime
from typing import Optional

try:
    import dateparser
except ImportError:
    print(
        "[ERROR]: The 'dateparser' library is not installed. "
        "Please install it with 'pip install dateparser' or use 'uv run --with dateparser'.",
        file=sys.stderr,
    )
    sys.exit(1)


def parse_time(time_str: str) -> Optional[datetime]:
    """
    Parses a natural language time string into a datetime object.
    Enforces PREFER_DATES_FROM=future to handle ambiguous times (e.g. '9:30 AM').
    """
    return dateparser.parse(time_str, settings={"PREFER_DATES_FROM": "future"})


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Advanced-Schedule: A natural language timer daemon designed for background execution.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--time", required=True, help="Natural language time (e.g. 'in 6 hours', '9:30 AM', 'tomorrow at noon')"
    )
    parser.add_argument(
        "--message", required=True, help="The message to print to stdout when the time is up to wake the agent"
    )

    args = parser.parse_args()

    target_time = parse_time(args.time)

    if not target_time:
        print(
            f"\n[ADVANCED-SCHEDULE-ERROR]: Could not parse time string '{args.time}'. Please try a different format.",
            flush=True,
            file=sys.stderr,
        )
        sys.exit(1)

    now = datetime.now()
    if target_time < now:
        print(
            f"\n[ADVANCED-SCHEDULE-ERROR]: The parsed time '{target_time}' is in the past! Current time is {now}.",
            flush=True,
            file=sys.stderr,
        )
        sys.exit(1)

    sleep_seconds = (target_time - now).total_seconds()

    # We sleep silently. No initial output ensures the console remains clean for the background daemon.
    try:
        time.sleep(sleep_seconds)
    except KeyboardInterrupt:
        print("\n[ADVANCED-SCHEDULE-ERROR]: Timer interrupted manually.", flush=True, file=sys.stderr)
        sys.exit(1)

    # Print the final message to standard output to wake the agent.
    # The newlines help the message stand out in a stream of logs.
    print(f"\n[ADVANCED-SCHEDULE ALARM]: {args.message}\n", flush=True)


if __name__ == "__main__":
    main()
