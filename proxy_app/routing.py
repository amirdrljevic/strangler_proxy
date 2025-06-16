import json
import redis
from typing import Optional, List, Dict

# 1️⃣ Connect to Redis:
#    - host, port, db match your local Redis setup
#    - decode_responses=True returns Python strings instead of bytes
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 2️⃣ The Redis key where rules are stored
REDIS_RULES_KEY = "routing_rules"

def load_rules() -> List[Dict]:
    """
    Fetch the JSON blob from Redis and parse into Python list of dicts.
    Returns [] if no rules are set.
    """
    raw = r.get(REDIS_RULES_KEY)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # In case the JSON is malformed
        return []

def get_target_backend(path: str) -> Optional[str]:
    """
    Determine the backend base URL for a given request path
    by iterating through the loaded Redis rules.
    """
    for rule in load_rules():
        if rule.get("match_type") == "path_prefix" and path.startswith(rule.get("pattern", "")):
            return rule.get("target")
    return None
