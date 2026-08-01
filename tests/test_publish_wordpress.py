import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from publish_wordpress import exact_term_id, make_post_payload, normalize_password, post_lookup_action


class PublisherTests(unittest.TestCase):
    def test_normalize_password_removes_grouping_spaces(self):
        self.assertEqual(normalize_password("abcd efgh ijkl"), "abcdefghijkl")

    def test_exact_term_id_ignores_partial_matches(self):
        terms = [{"id": 1, "name": "日本経済"}, {"id": 2, "name": "日本"}]
        self.assertEqual(exact_term_id(terms, "日本"), 2)
        self.assertIsNone(exact_term_id(terms, "社会"))

    def test_make_post_payload_maps_wordpress_fields(self):
        data = {
            "title": "見出し",
            "slug": "sample-story",
            "excerpt": "要約",
            "date": "2026-08-01 09:00:00 +0900",
            "wordpress": {"status": "draft", "comment_status": "closed"},
        }
        payload = make_post_payload(data, "<p>本文</p>", [10], [20, 21])
        self.assertEqual(payload["title"], "見出し")
        self.assertEqual(payload["slug"], "sample-story")
        self.assertEqual(payload["status"], "draft")
        self.assertEqual(payload["comment_status"], "closed")
        self.assertEqual(payload["categories"], [10])
        self.assertEqual(payload["tags"], [20, 21])
        self.assertEqual(payload["date"], "2026-08-01T09:00:00+09:00")

    def test_post_lookup_action_is_idempotent(self):
        self.assertEqual(post_lookup_action([]), ("create", None))
        self.assertEqual(post_lookup_action([{"id": 77}]), ("update", 77))
        with self.assertRaisesRegex(RuntimeError, "multiple posts"):
            post_lookup_action([{"id": 1}, {"id": 2}])


if __name__ == "__main__":
    unittest.main()
