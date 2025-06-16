import json
import redis
from django.test import SimpleTestCase
from proxy_app.routing import get_target_backend, REDIS_RULES_KEY

class RoutingUnitTests(SimpleTestCase):
    def setUp(self):
        # Connect to Redis and seed it with test rules
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.rules = [
            {"match_type": "path_prefix", "pattern": "/foo/", "target": "http://foo.test"},
            {"match_type": "path_prefix", "pattern": "/bar/", "target": "http://bar.test"}
        ]
        self.r.set(REDIS_RULES_KEY, json.dumps(self.rules))

    def tearDown(self):
        # Clean up after each test
        self.r.delete(REDIS_RULES_KEY)

    def test_get_target_backend_foo(self):
        self.assertEqual(
            get_target_backend("/foo/baz"),
            "http://foo.test"
        )

    def test_get_target_backend_bar(self):
        self.assertEqual(
            get_target_backend("/bar/qux"),
            "http://bar.test"
        )

    def test_get_target_backend_no_match(self):
        self.assertIsNone(
            get_target_backend("/unknown/path")
        )
