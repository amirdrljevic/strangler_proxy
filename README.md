## Loading Routing Rules into Redis

We store our routing configuration in `routing_rules.json`.  
After starting Redis, populate it with:

```bash
python manage.py load_rules