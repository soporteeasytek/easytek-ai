#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

BASE_DOCS_PATH = Path("/Users/isaacmora/.openclaw/workspace/memory/empresas")

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def cmd_document_company_info(args):
    company_dir = BASE_DOCS_PATH / args.company_name.replace(" ", "_")
    ensure_dir(company_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.{args.format}"
    file_path = company_dir / filename

    content_to_write = args.info
    if args.format == "json":
        try:
            json_data = json.loads(args.info)
            content_to_write = json.dumps(json_data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON format provided for --info."}, indent=2), file=sys.stderr)
            sys.exit(1)

    try:
        file_path.write_text(content_to_write)
        print(json.dumps({"status": "success", "path": str(file_path)}, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"Failed to write file: {e}"}, indent=2), file=sys.stderr)
        sys.exit(1)

def build_parser():
    parser = argparse.ArgumentParser(description="Company documentation helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("document-company-info")
    p.add_argument("--company-name", required=True, help="Name of the company.")
    p.add_argument("--info", required=True, help="Information to document (text or JSON string).")
    p.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Format of the information.")
    p.set_defaults(func=cmd_document_company_info)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
