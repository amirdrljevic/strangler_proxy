# Strangler Proxy Service

## Explanation

A Django-based reverse proxy implementing the “strangler” pattern:

- **Proxy**: intercepts incoming HTTP requests and forwards them to the appropriate backend  
- **Strangler Pattern**: gradually migrate from a monolith by routing some endpoints to new microservices  
- **Dynamic Rules**: routing rules live in `routing_rules.json` (under version control) and are loaded into Redis  
- **Graceful Reload**: atomic swapping of rules ensures in-flight requests finish under old rules while new requests use updated rules immediately  

## Requirements

- Python 3.11 or higher  
- Redis server (listening on localhost:6379)  
- Git  

## Setup & Installation

### Clone the repo

```bash
git clone https://github.com/amirdrljevic/strangler_proxy.git
cd strangler_proxy
```

### Create & activate virtualenv

```bash
python -m venv venv
```

**Windows CMD:**
```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply initial migrations (creates db.sqlite3)

```bash
python manage.py migrate
```

## 🔄 Loading & Hot-Swapping Rules

Define your routing in `routing_rules.json`. To push those rules into Redis:

### Initial load (first time)

```bash
python manage.py load_rules
# → ✅ Loaded routing_rules.json into Redis key 'routing_rules'
```

### Hot-swap after editing routing_rules.json

```bash
python manage.py load_rules
# → ✅ Swapped routing_rules.json into Redis key 'routing_rules'
```

Under the hood, this writes to a temporary Redis key and atomically renames it over `routing_rules`, so in-flight requests continue under the old rules and new requests immediately pick up the updated rules.

## Running the Proxy

```bash
python manage.py runserver
```

**Health check:**
```bash
curl http://127.0.0.1:8000/health/
# → Proxy service is up and healthy.
```


## Testing

### Run all tests
```bash
python manage.py test
```

### Run unit tests only
```bash
python manage.py test proxy_app.tests.unit
```

### Run integration tests only
```bash
python manage.py test proxy_app.tests.integration
```

### Run tests with verbose output
```bash
python manage.py test -v 2
```

## Quick Command Summary

```bash
git clone https://github.com/youruser/strangler_proxy.git
cd strangler_proxy
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_rules
python manage.py runserver
python manage.py test
python manage.py test proxy_app.tests.unit
python manage.py test proxy_app.tests.integration
python manage.py test -v 2
```
