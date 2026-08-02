import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from edition import render_chinese_daily


class ChineseDailyCoreLayoutTests(unittest.TestCase):
    def test_core_section_uses_card_grid_layout(self):
        text = render_chinese_daily(
            edition_date="2026-08-03",
            coverage_start="2026-08-02T06:00:00+09:00",
            coverage_end="2026-08-03T05:59:59+09:00",
            published_at="2026-08-03 06:00:00 +0900",
            counts={"core": 6, "social": 8, "other": 10},
        )

        self.assertIn('<div class="core-grid">', text)
        self.assertIn('<article class="core-card">', text)
        self.assertIn('<span class="core-card__number">', text)
        self.assertNotIn('<ol class="daily-list">', text)


if __name__ == "__main__":
    unittest.main()
