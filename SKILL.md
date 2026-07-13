---
name: advanced-schedule
description: >-
  Schedule background alarms using natural language (e.g. 'in 6 hours', '9:30 AM') that bypass the 15-minute native cap.
---

# Advanced Schedule Skill

## Overview
This skill allows you to schedule background timers for massively long durations (e.g. "6 hours", "3 days") or for exact calendar times (e.g. "9:30 AM", "tomorrow at noon"). It uses a lightweight background python daemon that parses the natural language time, sleeps silently, and then wakes you up by printing a message to standard output.

## When to Use
- When the user asks you to wait for **more than 15 minutes** (which breaks the native scheduling limits).
- When the user specifies an exact clock time (e.g. "Wake me up at 2:00 PM").

## Usage Instructions

To use this skill, use the `run_command` tool to launch the background daemon. 

### Critical Execution Rules
1. **Always ensure `dateparser` is available.** Use `uv run --with dateparser` or your environment's equivalent.
2. **Always send to background:** Set `WaitMsBeforeAsync` to `500` or `1000` in the `run_command` tool. This ensures the script is pushed to the background immediately so your execution is not blocked while it sleeps!
3. **Format `--time` carefully**: It should be wrapped in quotes.
4. **Format `--message` carefully**: This is the literal text you will receive when you wake up. Make it a clear instruction for yourself (e.g., "Check the build status").

### Command Syntax
```bash
uv run --with dateparser advanced_timer.py --time "[Time String]" --message "[Your Wake-up Prompt]"
```

### Examples

**Example 1: Specific Duration (6 hours)**
```bash
uv run --with dateparser advanced_timer.py --time "in 6 hours" --message "6 hours have passed. Check the metrics."
```

**Example 2: Specific Time (9:30 AM)**
```bash
uv run --with dateparser advanced_timer.py --time "9:30 AM" --message "It is 9:30 AM. Send the daily report."
```

## Troubleshooting
If you receive an immediate output message saying `[ADVANCED-SCHEDULE-ERROR]`, it means the time string was invalid or in the past. Do not go to sleep; fix the time string and launch the command again.
