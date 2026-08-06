#!/usr/bin/env python3
"""Build the PressBox app from ui_data.json + pressbox_template.html.

Outputs:
- pressbox.html      (gitignored; used for republishing the Claude artifact)
- docs/index.html    (committed; served publicly via GitHub Pages)

The Pages copy gets a full HTML shell around the same content the artifact
publisher wraps automatically.
"""
import json
from pathlib import Path

here = Path(__file__).parent
data = json.loads((here / "ui_data.json").read_text())  # validates JSON
tpl = (here / "pressbox_template.html").read_text()
body = tpl.replace("__DATA__", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))

(here / "pressbox.html").write_text(body)

page = "<!doctype html>\n<html lang=\"en\">\n" + body + "\n</html>\n"
(here / "docs").mkdir(exist_ok=True)
(here / "docs" / "index.html").write_text(page)

print(f"built pressbox.html + docs/index.html ({len(body)} bytes, "
      f"{len(data['rows'])} rows, updated {data['meta']['updated']})")
