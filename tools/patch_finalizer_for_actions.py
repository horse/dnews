#!/usr/bin/env python3
from pathlib import Path

self_path = Path(__file__)
finalizer = self_path.with_name("finalize_expanded_daily.py")
text = finalizer.read_text(encoding="utf-8")

start = text.index('# Restore a permanent, read-only PR test workflow.')
end = text.index('for relative in [', start)
text = text[:start] + text[end:]
text = text.replace('    ".github/workflows/generate-expanded-daily.yml",\n', '')
finalizer.write_text(text, encoding="utf-8")
self_path.unlink()
