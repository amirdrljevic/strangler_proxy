import json
from pathlib import Path
import redis
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Load routing_rules.json into Redis under key 'routing_rules'"

    def handle(self, *args, **options):
        # Connect to local Redis
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

        # Locate the JSON file at project root
        repo_root = Path(__file__).resolve().parents[3]  # up from commands/ to project root
        rules_path = repo_root / 'routing_rules.json'

        # Read & parse JSON
        with open(rules_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Write to Redis
        r.set("routing_rules", json.dumps(data))
        self.stdout.write(self.style.SUCCESS("✅ Loaded routing_rules.json into Redis"))
