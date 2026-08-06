#!/usr/bin/env python3
"""Build pressbox.html from ui_data.json + pressbox_template.html."""
import json
from pathlib import Path
here = Path(__file__).parent
data = json.loads((here / "ui_data.json").read_text())  # validates JSON
tpl = (here / "pressbox_template.html").read_text()
out = tpl.replace("__DATA__", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
(here / "pressbox.html").write_text(out)
print(f"built pressbox.html ({len(out)} bytes, {len(data['rows'])} rows, updated {data['meta']['updated']})")
