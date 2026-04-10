#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

ENV_PATH = Path("/Users/isaacmora/.openclaw/workspace/.paperclip.env")


def load_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def resolve_settings(cli_api_url: Optional[str], cli_api_key: Optional[str], cli_company_id: Optional[str], cli_agent_id: Optional[str]) -> tuple[str, str, str, str]:
    env_file = load_env_file(ENV_PATH)
    api_url = cli_api_url or os.getenv("PAPERCLIP_API_URL") or env_file.get("PAPERCLIP_API_URL")
    api_key = cli_api_key or os.getenv("PAPERCLIP_AGENT_API_KEY") or env_file.get("PAPERCLIP_AGENT_API_KEY")
    company_id = cli_company_id or os.getenv("PAPERCLIP_COMPANY_ID") or env_file.get("PAPERCLIP_COMPANY_ID")
    agent_id = cli_agent_id or os.getenv("PAPERCLIP_AGENT_ID") or env_file.get("PAPERCLIP_AGENT_ID")

    if not api_url:
        print(json.dumps({"error": "Missing PAPERCLIP_API_URL. Set it in .paperclip.env or pass --api-url."}, indent=2), file=sys.stderr)
        sys.exit(1)
    if not api_key:
        print(json.dumps({"error": "Missing PAPERCLIP_AGENT_API_KEY. Set it in .paperclip.env or pass --api-key."}, indent=2), file=sys.stderr)
        sys.exit(1)
    if not company_id:
        print(json.dumps({"error": "Missing PAPERCLIP_COMPANY_ID. Set it in .paperclip.env or pass --company-id."}, indent=2), file=sys.stderr)
        sys.exit(1)
    if not agent_id:
        print(json.dumps({"error": "Missing PAPERCLIP_AGENT_ID. Set it in .paperclip.env or pass --agent-id."}, indent=2), file=sys.stderr)
        sys.exit(1)

    return api_url.rstrip("/"), api_key, company_id, agent_id


def request_json(api_url: str, path: str, api_key: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> Any:
    url = api_url + path
    data = None
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"error": {"status": e.code, "body": body}}, indent=2), file=sys.stderr)
        sys.exit(1)


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_create_issue(args):
    api_url, api_key, company_id, current_agent_id = resolve_settings(args.api_url, args.api_key, args.company_id, args.agent_id)
    assignee_agent_id = args.assignee_agent_id if args.assignee_agent_id else current_agent_id

    payload = {
        "title": args.title,
        "description": args.description,
        "companyId": company_id,
        "assigneeAgentId": assignee_agent_id,
        "status": args.status,
        "metadata": json.loads(args.metadata) if args.metadata else None,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    data = request_json(api_url, f"/api/companies/{company_id}/issues", api_key, method="POST", payload=payload)
    print_json(data)

def cmd_list_agents(args):
    api_url, api_key, company_id, _ = resolve_settings(args.api_url, args.api_key, args.company_id, None)
    data = request_json(api_url, f"/api/companies/{company_id}/agents", api_key)
    print_json(data)


def build_parser():
    parser = argparse.ArgumentParser(description="Paperclip helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create-issue")
    p.add_argument("--api-url")
    p.add_argument("--api-key")
    p.add_argument("--company-id")
    p.add_argument("--agent-id") # Current agent making the request
    p.add_argument("--title", required=True)
    p.add_argument("--description", required=True)
    p.add_argument("--status", default="todo")
    p.add_argument("--assignee-agent-id", type=str) # Agent to assign the issue to
    p.add_argument("--metadata")
    p.set_defaults(func=cmd_create_issue)

    p = sub.add_parser("list-agents")
    p.add_argument("--api-url")
    p.add_argument("--api-key")
    p.add_argument("--company-id")
    p.set_defaults(func=cmd_list_agents)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
