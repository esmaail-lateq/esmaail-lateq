#!/usr/bin/env python3
"""
GitHub Contribution Graph Populator
------------------------------------
This script generates authentic commits over a specified date range
with custom author dates to populate your GitHub contribution graph.

Usage:
  python3 scripts/populate_contributions.py --days 365 --max-commits 4
"""

import os
import sys
import random
import argparse
import subprocess
from datetime import datetime, timedelta

def run_command(cmd, env=None):
    result = subprocess.run(cmd, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error executing: {cmd}\n{result.stderr}")
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Populate GitHub contributions")
    parser.add_argument("--days", type=int, default=365, help="Number of past days to generate commits for (default: 365)")
    parser.add_argument("--max-commits", type=int, default=4, help="Maximum commits per day (default: 4)")
    parser.add_argument("--author-name", type=str, default="esmaail-lateq", help="Git author name")
    parser.add_argument("--author-email", type=str, default="asmailalmaori@gmail.com", help="Git author email (must match GitHub account)")
    args = parser.parse_args()

    log_file = "activity.log"
    today = datetime.now()

    print(f"🚀 Starting contribution generator for the past {args.days} days...")
    print(f"👤 Author: {args.author_name} <{args.author_email}>")

    total_commits = 0
    env = os.environ.copy()

    for day_offset in range(args.days, -1, -1):
        target_date = today - timedelta(days=day_offset)
        
        # Skip random days (e.g. 10% chance) to make activity look organic and natural
        if random.random() < 0.12:
            continue

        # Random number of commits for this day (1 to max-commits)
        commits_today = random.randint(1, args.max_commits)

        for i in range(commits_today):
            # Pick a realistic time during the day (between 09:00 and 23:00)
            hour = random.randint(9, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = target_date.replace(hour=hour, minute=minute, second=second)
            date_str = commit_time.strftime("%Y-%m-%d %H:%M:%S")

            # Update activity log
            with open(log_file, "a") as f:
                f.write(f"Activity entry on {date_str} - build #{total_commits + 1}\n")

            env["GIT_AUTHOR_NAME"] = args.author_name
            env["GIT_AUTHOR_EMAIL"] = args.author_email
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_NAME"] = args.author_name
            env["GIT_COMMITTER_EMAIL"] = args.author_email
            env["GIT_COMMITTER_DATE"] = date_str

            run_command(f'git add {log_file}', env=env)
            commit_msg = f"chore(activity): record update for {commit_time.strftime('%Y-%m-%d')}"
            run_command(f'git commit -m "{commit_msg}" --quiet', env=env)
            total_commits += 1

    print(f"✅ Successfully generated {total_commits} commits over {args.days} days!")
    print("\n👉 To push them to GitHub and fill your contribution graph, run:")
    print("   git push origin main")

if __name__ == "__main__":
    main()
