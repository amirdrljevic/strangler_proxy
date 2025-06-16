import json
from pathlib import Path

import redis
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Atomically load routing_rules.json into Redis under key 'routing_rules'"

    def handle(self, *args, **options):
        # 1️⃣ Connect to Redis
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

        # 2️⃣ Locate the JSON file at the project root
        repo_root = Path(__file__).resolve().parents[3]
        rules_path = repo_root / 'routing_rules.json'

        # 3️⃣ Read & parse the JSON
        data = json.loads(rules_path.read_text(encoding='utf-8'))

        # 4️⃣ Check if the live key exists before overwrite
        live_exists = r.exists("routing_rules")

        # 5️⃣ Write the new rules to a temporary key
        tmp_key = "routing_rules_tmp"
        r.set(tmp_key, json.dumps(data))

        # 6️⃣ Atomically rename the temp key over the live key
        #    RENAME will replace the old key if it exists
        r.rename(tmp_key, "routing_rules")

        # 7️⃣ Decide if this was a first-time load or a swap
        action = "swapped" if live_exists else "loaded"

        # 8️⃣ Output a clear success message
        self.stdout.write(self.style.SUCCESS(
            f"✅ {action.capitalize()} routing_rules.json into Redis key 'routing_rules'"
        ))
