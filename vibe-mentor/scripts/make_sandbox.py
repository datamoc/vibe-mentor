#!/usr/bin/env python3
"""Prepare the Initiation-mode exercises in .sandbox/ (throwaway Git repository).

Usage: python make_sandbox.py {1|2|3} [--dest .sandbox]
  1 = AI vs Script : 50 badly formatted JSON files
  2 = The Split    : one monolithic file of more than 500 lines
  3 = Duplicates   : 3 near-identical functions under different names
"""
import argparse
import json
import random
import subprocess
import sys
import zipfile
from pathlib import Path

ENTITIES = ["user", "order", "invoice", "product", "cart", "coupon", "review", "shipment",
            "address", "payment", "refund", "supplier", "category", "wishlist", "ticket", "newsletter"]


def kata1(dest: Path) -> None:
    """50 configs: varied indentation, minified JSON, trailing commas (invalid)."""
    rnd = random.Random(1)
    (dest / "configs").mkdir(parents=True)
    for i in range(50):
        cfg = {"service": f"svc-{i:02d}", "port": 3000 + i, "debug": rnd.random() < .5,
               "retries": rnd.randint(1, 5), "tags": ["a", "b"]}
        style = i % 4
        text = (json.dumps(cfg) if style == 0 else
                json.dumps(cfg, indent="\t") if style == 1 else
                json.dumps(cfg, indent=7) if style == 2 else
                json.dumps(cfg, indent=2).replace('"b"\n  ]', '"b",\n  ]'))  # trailing comma
        (dest / "configs" / f"svc-{i:02d}.json").write_text(text, encoding="utf-8")


def kata2(dest: Path) -> None:
    """Node.js monolith: data access + business logic + HTML in a single file."""
    dest.mkdir(parents=True)
    out = ["// server.js: everything is mixed together here", "const http = require('http');", "const db = {};", ""]
    for e in ENTITIES:
        out += [f"// ---- {e}: data ----",
                f"function load_{e}(id) {{", f"  const row = db['{e}:' + id];",
                f"  if (!row) throw new Error('{e} not found');", "  return row;", "}",
                f"function save_{e}(id, data) {{", f"  db['{e}:' + id] = {{ ...data, updated: Date.now() }};", "}",
                f"// ---- {e}: business logic ----",
                f"function validate_{e}(data) {{", "  const errors = [];",
                f"  if (!data.name) errors.push('name required for {e}');",
                f"  if (data.name && data.name.length > 80) errors.push('name too long');",
                "  if (data.price !== undefined && data.price < 0) errors.push('negative price');",
                "  return errors;", "}",
                f"function compute_{e}_total(items) {{", "  let total = 0;",
                "  for (const it of items) {", "    total += it.price * it.qty;", "    if (it.discount) total -= it.discount;", "  }",
                "  return Math.round(total * 100) / 100;", "}",
                f"// ---- {e}: HTML rendering ----",
                f"function render_{e}(data) {{",
                "  return `<div class=\"card\">", f"    <h2>${{data.name}}</h2>", f"    <p>{e} #${{data.id}}</p>",
                "    <span class=\"price\">${data.price} €</span>", "  </div>`;", "}",
                f"function handle_{e}(req, res) {{", f"  const data = load_{e}(req.url.split('/').pop());",
                "  res.writeHead(200, { 'Content-Type': 'text/html' });", f"  res.end(render_{e}(data));", "}", ""]
    out += ["http.createServer((req, res) => {"]
    out += [f"  if (req.url.startsWith('/{e}')) return handle_{e}(req, res);" for e in ENTITIES]
    out += ["  res.writeHead(404); res.end('?');", "}).listen(3000);"]
    (dest / "server.js").write_text("\n".join(out) + "\n", encoding="utf-8")


def kata3(dest: Path) -> None:
    """Three functions doing the same thing: format a price in euros."""
    (dest / "src").mkdir(parents=True)
    # Identical body (typical AI copy-paste), only the name changes.
    body = ("  const rounded = Math.round(value * 100) / 100;\n"
            "  const fixed = rounded.toFixed(2);\n"
            "  const parts = fixed.split('.');\n"
            "  const intPart = parts[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, ' ');\n"
            "  const decimals = parts[1];\n"
            "  const sign = value < 0 ? '-' : '';\n"
            "  return sign + intPart + ',' + decimals + ' €';\n")
    for file, fn in (("cart.js", "formatPrice"), ("invoice.js", "euroString"), ("report.js", "toEuros")):
        text = f"function {fn}(value) {{\n{body}}}\nmodule.exports = {{ {fn} }};\n"
        (dest / "src" / file).write_text(text, encoding="utf-8")


README = """Practice exercise: {name}

What this is: a small, safe folder made for practising. Nothing here is a real
project, so you cannot break anything. Open the folder in your editor or give it
to your AI assistant, and follow the steps it proposes.

Tip: keep this folder separate from your real projects, and keep a copy of the
original zip so you can start the exercise again.
"""


def make_zip(target: Path) -> Path:
    """Downloadable copy of the exercise: files plus a README, without the Git history."""
    archive = target.with_suffix(".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{target.name}/README.txt", README.format(name=target.name))
        for f in sorted(target.rglob("*")):
            if f.is_file() and ".git" not in f.relative_to(target).parts:
                z.write(f, f"{target.name}/{f.relative_to(target).as_posix()}")
    return archive


KATAS = {"1": ("kata1-ia-vs-script", kata1), "2": ("kata2-decoupe", kata2), "3": ("kata3-doublons", kata3)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("kata", choices=KATAS)
    ap.add_argument("--dest", default=".sandbox")
    ap.add_argument("--zip", action="store_true", help="also create a downloadable .zip of the exercise")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    name, build = KATAS[args.kata]
    target = Path(args.dest) / name
    if target.exists():
        print(f"{target} already exists: delete it to restart the exercise.")
        return 1
    build(target)
    subprocess.run(["git", "init", "-q", str(target)], check=False)
    subprocess.run(["git", "-C", str(target), "add", "-A"], check=False)
    subprocess.run(["git", "-C", str(target), "commit", "-qm", "Initial state of the exercise"], check=False)
    if args.zip:
        print(f"Download: {make_zip(target)}")
    print(f"Exercise ready in {target} (local Git repository, isolated from production code).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
