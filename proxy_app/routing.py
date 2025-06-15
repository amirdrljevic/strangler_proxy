# A simple list of routing rules for now
ROUTING_RULES = [
    {
        "match_type": "path_prefix",
        "pattern": "/legacy/",
        "target": "http://localhost:9001"
    },
    {
        "match_type": "path_prefix",
        "pattern": "/new/",
        "target": "http://localhost:9002"
    }
]

def get_target_backend(path: str) -> str | None:
    for rule in ROUTING_RULES:
        if rule["match_type"] == "path_prefix" and path.startswith(rule["pattern"]):
            return rule["target"]
    return None
