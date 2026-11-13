import csv
import re
from collections import defaultdict
from datetime import datetime


# --------------------------------------------------
# TBL scoring rules
# --------------------------------------------------

RESULT_RULES = {
    "W - Decision": {
        "score": 1,
        "rounds_won": 1,
        "rounds_lost": 0,
        "knockdowns": 0,
        "knockouts": 0,
    },
    "W - Knockdown": {
        "score": 2,
        "rounds_won": 1,
        "rounds_lost": 0,
        "knockdowns": 1,
        "knockouts": 0,
    },
    "W - 2x Knockdown": {
        "score": 3,
        "rounds_won": 1,
        "rounds_lost": 0,
        "knockdowns": 2,
        "knockouts": 0,
    },
    "W - KO": {
        "score": 4,
        "rounds_won": 1,
        "rounds_lost": 0,
        "knockdowns": 0,
        "knockouts": 1,
    },
    "W - TKO": {
        "score": 4,
        "rounds_won": 1,
        "rounds_lost": 0,
        "knockdowns": 0,
        "knockouts": 1,
    },

    "L - Decision": {
        "score": -1,
        "rounds_won": 0,
        "rounds_lost": 1,
        "knockdowns": 0,
        "knockouts": 0,
    },
    "L - Knockdown": {
        "score": -2,
        "rounds_won": 0,
        "rounds_lost": 1,
        "knockdowns": 0,
        "knockouts": 0,
    },
    "L - 2x Knockdown": {
        "score": -3,
        "rounds_won": 0,
        "rounds_lost": 1,
        "knockdowns": 0,
        "knockouts": 0,
    },
    "L - KO": {
        "score": -4,
        "rounds_won": 0,
        "rounds_lost": 1,
        "knockdowns": 0,
        "knockouts": 0,
    },
    "L - TKO": {
        "score": -4,
        "rounds_won": 0,
        "rounds_lost": 1,
        "knockdowns": 0,
        "knockouts": 0,
    },

    "No Contest": {
        "score": 0,
        "rounds_won": 0,
        "rounds_lost": 0,
        "knockdowns": 0,
        "knockouts": 0,
    },
}


# --------------------------------------------------
# Read source CSV
# --------------------------------------------------

CSV_FILE = "stats-test.csv"

aggregated = defaultdict(
    lambda: {
        "score": 0,
        "rounds_won": 0,
        "rounds_lost": 0,
        "knockdowns": 0,
        "knockouts": 0,
        "rounds": 0,
    }
)


with open(CSV_FILE, newline="", encoding="utf-8-sig") as file:

    reader = csv.DictReader(file)
    print("CSV headers:", reader.fieldnames)

    for row_number, row in enumerate(reader, start=2):

        fighter = row["Fighter Name"].strip()
        fighter_id = row["Fighter ID"].strip()
        team = row["Team"].strip()
        match_id = row["Match ID"].strip()
        result = row["Result"].strip()

        # Generate a unique ID for this fighter's
        # performance in this competition.
        fight_date = datetime.strptime(
            row["Date of Fight"].strip(), "%m/%d/%Y"
        )
        formatted_date = fight_date.strftime("%Y%m%d")

        # Normalize fighter name for a consistent identifier.
        fighter_key = re.sub(
            r"[^a-z0-9]+", "-",
            fighter.lower()
            ).strip("-")

        # One unique ID per fighter per competition.
        source_stat_id = f"{fighter_key}-{formatted_date}-{match_id}" 

        if result not in RESULT_RULES:
            print(
                f"WARNING row {row_number}: "
                f"Unknown result '{result}' for {fighter}"
            )
            continue

        # Group all rounds for this fighter and match.
        key = source_stat_id

        stats = aggregated[key]

        # Save identifying information.
        stats["fighter"] = fighter
        stats["fighter_id"] = fighter_id
        stats["source_stat_id"] = source_stat_id
        stats["team"] = team
        stats["match_id"] = match_id
        stats["date"] = row["Date of Fight"].strip()

        # Apply TBL scoring rules.
        rule = RESULT_RULES[result]

        stats["score"] += rule["score"]
        stats["rounds_won"] += rule["rounds_won"]
        stats["rounds_lost"] += rule["rounds_lost"]
        stats["knockdowns"] += rule["knockdowns"]
        stats["knockouts"] += rule["knockouts"]

        stats["rounds"] += 1


# --------------------------------------------------
# Dry-run output
# --------------------------------------------------

print("\n====================================")
print("TBL PLAYER STAT IMPORT — DRY RUN")
print("NO SHOPIFY DATA WILL BE CHANGED")
print("====================================\n")


for stats in aggregated.values():

    print(stats["fighter"])
    print("------------------------------------")

    print(f"Fighter ID:   {stats['fighter_id']}")
    print(f"Team:         {stats['team']}")
    print(f"source id:    {stats['source_stat_id']}")
    print(f"Match ID:     {stats['match_id']}")
    print(f"Date:         {stats['date']}")

    print()

    print(f"Score:        {stats['score']}")
    print(f"Rounds Won:   {stats['rounds_won']}")
    print(f"Rounds Lost:  {stats['rounds_lost']}")
    print(f"Knockdowns:   {stats['knockdowns']}")
    print(f"Knockouts:    {stats['knockouts']}")

    print()
