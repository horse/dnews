#!/usr/bin/env python3
from __future__ import annotations

import base64
import io
import itertools
import re
import string
import tarfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("generate_expanded_daily.py")
source = SCRIPT.read_text(encoding="utf-8")
match = re.search(r'PAYLOAD = """([A-Za-z0-9+/=\r\n]+)"""', source)
if not match:
    raise RuntimeError("PAYLOAD block not found")

payload = "".join(match.group(1).split())
alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
expected = {
    "_posts/2026-08-01-kumamoto-water-heat-evacuation.md",
    "_posts/2026-08-01-kumamoto-red-cross-emergency-care.md",
    "_posts/2026-08-01-kumamoto-public-facility-closures.md",
    "_posts/2026-08-01-tomoiku-end-solo-parenting.md",
    "_posts/2026-08-01-tokyo-skilled-trades-succession.md",
    "_posts/2026-08-01-tokyo-art-accessibility-exhibition.md",
    "_posts/2026-08-01-japan-environment-plan-review.md",
    "_posts/2026-08-01-tokyo-life-opinion-survey.md",
    "_posts/2026-08-01-kahaku-human-earth-exhibition.md",
    "_posts/2026-08-01-conrad-nagoya-opening.md",
    "_posts/2026-08-01-national-art-center-family-week.md",
    "_posts/2026-08-01-yoshimura-akira-yuonki.md",
    "_posts/2026-08-01-okayama-ponpon-boat-exhibition.md",
    "_posts/2026-08-01-japan-medical-education-conference.md",
    "_posts/2026-08-01-medical-physics-summer-seminar.md",
    "_posts/2026-08-01-japan-cinema-july31.md",
    "_posts/2026-08-01-npb-july31-roundup.md",
    "_posts/2026-08-01-kasai-sunflower-lighting.md",
}


def archive_names(candidate: str) -> set[str] | None:
    try:
        data = base64.b64decode(candidate, validate=True)
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            names = {member.name for member in archive.getmembers() if member.isfile()}
        return names
    except (ValueError, OSError, EOFError, tarfile.TarError):
        return None


candidates: list[str] = []
if len(payload) % 4 == 0:
    candidates.append(payload)

# The captured payload is two data characters short. Try the only bounded,
# auditable repair: insert two Base64 characters immediately before padding.
if payload.endswith("="):
    stem = payload[:-1]
    candidates.extend(stem + a + b + "=" for a, b in itertools.product(alphabet, repeat=2))

# Also test whether one accidental trailing character was introduced.
for cut in range(1, 4):
    stem = payload[:-cut]
    padded = stem + "=" * ((-len(stem)) % 4)
    candidates.append(padded)

fixed = None
for candidate in candidates:
    names = archive_names(candidate)
    if names == expected:
        fixed = candidate
        break

if fixed is None:
    raise RuntimeError(
        f"No validated payload repair found; payload_length={len(payload)}, "
        f"data_mod4={len(payload.rstrip('=')) % 4}"
    )

print(f"Validated payload repair: {len(fixed)} Base64 characters, {len(expected)} files")
repaired = source[: match.start(1)] + fixed + source[match.end(1) :]
exec(compile(repaired, str(SCRIPT), "exec"), {"__file__": str(SCRIPT), "__name__": "__main__"})
