#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional, List

# --- Configuración y Autenticación ---
DEFAULT_BASE_URL = "https://api.linear.app/graphql"
ENV_PATH = Path("/Users/isaacmora/.openclaw/workspace/.linear.env")

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

def resolve_api_key(cli_api_key: Optional[str]) -> str:
    env_file = load_env_file(ENV_PATH)
    api_key = cli_api_key or os.getenv("LINEAR_API_KEY") or env_file.get("LINEAR_API_KEY")

    if not api_key:
        print(json.dumps({"error": "Missing LINEAR_API_KEY. Set it in .linear.env, as an environment variable, or pass --api-key."}), file=sys.stderr)
        sys.exit(1)
    return api_key

# --- Peticiones GraphQL ---
def linear_request(api_key: str, query: str, variables: Optional[Dict[str, Any]] = None) -> Any:
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key,
    }
    payload = {"query": query, "variables": variables or {}}
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(DEFAULT_BASE_URL, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"error": {"status": e.code, "body": body}}, indent=2), file=sys.stderr)
        sys.exit(1)

def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))

# --- Consultas GraphQL ---
# Query para obtener todos los equipos
FETCH_TEAMS_QUERY = """
query {
  teams {
    nodes {
      id
      name
      key
    }
  }
}
"""

# Query para obtener todos los estados
FETCH_WORKFLOW_STATES_QUERY = """
query {
  workflowStates {
    nodes {
      id
      name
      type
      team {
        id
        name
      }
    }
  }
}
"""

# Query para obtener labels
FETCH_LABELS_QUERY = """
query {
  issueLabels {
    nodes {
      id
      name
      team {
        id
        name
      }
    }
  }
}
"""

CREATE_LABEL_MUTATION = """
mutation IssueLabelCreate($name: String!, $teamId: String) {
  issueLabelCreate(input: {
    name: $name,
    teamId: $teamId
  }) {
    success
    issueLabel {
      id
      name
      team {
        id
        name
      }
    }
  }
}
"""

# Query para obtener usuarios (asignados)
FETCH_USERS_QUERY = """
query {
  users {
    nodes {
      id
      name
      email
    }
  }
}
"""

# Query para crear un issue
CREATE_ISSUE_MUTATION = """
mutation IssueCreate($title: String!, $description: String, $teamId: String!, $priority: Int, $stateId: String, $assigneeId: String, $labelIds: [String!]) {
  issueCreate(input: {
    title: $title,
    description: $description,
    teamId: $teamId,
    priority: $priority,
    stateId: $stateId,
    assigneeId: $assigneeId,
    labelIds: $labelIds
  }) {
    success
    issue {
      id
      identifier
      title
      url
      state {
        name
      }
      priority
      assignee {
        name
      }
      labels {
        nodes {
          name
        }
      }
    }
  }
}
"""

# Query para actualizar un issue
UPDATE_ISSUE_MUTATION = """
mutation IssueUpdate($id: String!, $title: String, $description: String, $stateId: String, $priority: Int, $assigneeId: String, $labelIds: [String!]) {
  issueUpdate(id: $id, input: {
    title: $title,
    description: $description,
    stateId: $stateId,
    priority: $priority,
    assigneeId: $assigneeId,
    labelIds: $labelIds
  }) {
    success
    issue {
      id
      identifier
      title
      url
      state {
        name
      }
      priority
      assignee {
        name
      }
      labels {
        nodes {
          name
        }
      }
    }
  }
}
"""

# Query para obtener detalles de un issue
GET_ISSUE_QUERY = """
query Issue($identifier: String!) {
  issue(id: $identifier) {
    id
    identifier
    title
    description
    url
    createdAt
    updatedAt
    priority
    state {
      id
      name
      type
    }
    assignee {
      id
      name
      email
    }
    creator {
      name
    }
    team {
      id
      name
      key
    }
    labels {
      nodes {
        id
        name
      }
    }
  }
}
"""

# Query para listar issues
LIST_ISSUES_QUERY = """
query Issues($teamId: ID, $priority: Int, $stateType: String, $assigneeId: ID, $first: Int = 25) {
  issues(
    filter: {
      team: { id: { eq: $teamId } },
      priority: { eq: $priority },
      state: { type: { eq: $stateType } },
      assignee: { id: { eq: $assigneeId } }
    },
    first: $first
  ) {
    nodes {
      id
      identifier
      title
      url
      state {
        name
      }
      priority
      assignee {
        name
      }
      labels {
        nodes {
          name
        }
      }
    }
  }
}
"""

# Query para añadir un comentario
ADD_COMMENT_MUTATION = """
mutation CommentCreate($issueId: String!, $body: String!) {
  commentCreate(input: {
    issueId: $issueId,
    body: $body
  }) {
    success
    comment {
      id
      body
      issue {
        identifier
      }
      user {
        name
      }
    }
  }
}
"""

# --- Ayudantes de mapeo ---
def map_priority_to_linear(priority_name: str) -> Optional[int]:
    mapping = {
        "sin prioridad": 0,
        "urgente": 1,
        "alta": 2,
        "media": 3,
        "baja": 4,
    }
    return mapping.get(priority_name.lower())

def map_linear_priority_to_name(priority_value: int) -> str:
    mapping = {
        0: "Sin Prioridad",
        1: "Urgente",
        2: "Alta",
        3: "Media",
        4: "Baja",
    }
    return mapping.get(priority_value, "Desconocida")

def map_state_name_to_id(states: List[Dict[str, Any]], state_name: str, team_id: Optional[str] = None) -> Optional[str]:
    for state in states:
        if state["name"].lower() == state_name.lower():
            if team_id is None or state["team"]["id"] == team_id:
                return state["id"]
    return None

def map_label_name_to_id(labels: List[Dict[str, Any]], label_name: str, team_id: Optional[str] = None) -> Optional[str]:
    fallback = None
    for label in labels:
        if label["name"].lower() == label_name.lower():
            if label.get("team") is None:
                fallback = label["id"]
            if team_id is None:
                return label["id"]
            if label.get("team") and label["team"]["id"] == team_id:
                return label["id"]
    return fallback

def map_user_name_to_id(users: List[Dict[str, Any]], user_name: str) -> Optional[str]:
    for user in users:
        if user["name"].lower() == user_name.lower():
            return user["id"]
    return None

# --- Comandos CLI ---

def cmd_list_teams(args):
    api_key = resolve_api_key(args.api_key)
    result = linear_request(api_key, FETCH_TEAMS_QUERY)
    print_json(result)


def cmd_list_workflow_states(args):
    api_key = resolve_api_key(args.api_key)
    result = linear_request(api_key, FETCH_WORKFLOW_STATES_QUERY)
    print_json(result)


def cmd_list_labels(args):
    api_key = resolve_api_key(args.api_key)
    result = linear_request(api_key, FETCH_LABELS_QUERY)
    print_json(result)


def cmd_list_users(args):
    api_key = resolve_api_key(args.api_key)
    result = linear_request(api_key, FETCH_USERS_QUERY)
    print_json(result)


def cmd_create_label(args):
    api_key = resolve_api_key(args.api_key)

    team_id = None
    if args.team_id:
        team_id = args.team_id
    elif args.team_name or args.team_key:
        teams_data = linear_request(api_key, FETCH_TEAMS_QUERY)
        teams = teams_data["data"]["teams"]["nodes"]
        if args.team_name:
            for team in teams:
                if team["name"].lower() == args.team_name.lower():
                    team_id = team["id"]
                    break
        elif args.team_key:
            for team in teams:
                if team["key"].lower() == args.team_key.lower():
                    team_id = team["id"]
                    break
        if (args.team_name or args.team_key) and not team_id:
            print_json({"error": "Team not found."})
            sys.exit(1)

    result = linear_request(api_key, CREATE_LABEL_MUTATION, {"name": args.name, "teamId": team_id})
    print_json(result)


def cmd_create_issue(args):
    api_key = resolve_api_key(args.api_key)
    
    # Obtener IDs necesarios
    teams_data = linear_request(api_key, FETCH_TEAMS_QUERY)
    teams = teams_data["data"]["teams"]["nodes"]
    
    # Asumimos un team por ahora, o buscamos por nombre/key
    team_id = None
    if args.team_id:
        team_id = args.team_id
    elif args.team_name:
        for team in teams:
            if team["name"].lower() == args.team_name.lower():
                team_id = team["id"]
                break
    elif args.team_key:
        for team in teams:
            if team["key"].lower() == args.team_key.lower():
                team_id = team["id"]
                break

    if not team_id:
        print_json({"error": "Team ID, name or key is required to create an issue."})
        sys.exit(1)

    priority_value = map_priority_to_linear(args.priority) if args.priority else None
    
    state_id = None
    if args.status:
        workflow_states_data = linear_request(api_key, FETCH_WORKFLOW_STATES_QUERY)
        workflow_states = workflow_states_data["data"]["workflowStates"]["nodes"]
        state_id = map_state_name_to_id(workflow_states, args.status, team_id)
        if not state_id:
            print_json({"error": f"Workflow state '{args.status}' not found for team."})
            sys.exit(1)

    assignee_id = None
    if args.assignee:
        users_data = linear_request(api_key, FETCH_USERS_QUERY)
        users = users_data["data"]["users"]["nodes"]
        assignee_id = map_user_name_to_id(users, args.assignee)
        if not assignee_id:
            print_json({"error": f"Assignee '{args.assignee}' not found."})
            sys.exit(1)

    label_ids = []
    if args.label:
        labels_data = linear_request(api_key, FETCH_LABELS_QUERY)
        labels = labels_data["data"]["issueLabels"]["nodes"]
        label_id = map_label_name_to_id(labels, args.label, team_id)
        if not label_id:
            print_json({"error": f"Label '{args.label}' not found for team."})
            sys.exit(1)
        label_ids.append(label_id)

    variables = {
        "title": args.title,
        "description": args.description,
        "teamId": team_id,
        "priority": priority_value,
        "stateId": state_id,
        "assigneeId": assignee_id,
        "labelIds": label_ids if label_ids else None
    }
    result = linear_request(api_key, CREATE_ISSUE_MUTATION, variables)
    print_json(result)

def cmd_update_issue(args):
    api_key = resolve_api_key(args.api_key)

    variables = {"id": args.issue_id}

    if args.title:
        variables["title"] = args.title
    if args.description:
        variables["description"] = args.description
    if args.priority:
        variables["priority"] = map_priority_to_linear(args.priority)
    
    if args.status:
        # Necesitamos el teamId del issue para buscar el state correcto
        get_issue_data = linear_request(api_key, GET_ISSUE_QUERY, {"identifier": args.issue_id})
        if not get_issue_data["data"]["issue"]:
            print_json({"error": f"Issue with ID '{args.issue_id}' not found."})
            sys.exit(1)
        issue_team_id = get_issue_data["data"]["issue"]["team"]["id"]

        workflow_states_data = linear_request(api_key, FETCH_WORKFLOW_STATES_QUERY)
        workflow_states = workflow_states_data["data"]["workflowStates"]["nodes"]
        state_id = map_state_name_to_id(workflow_states, args.status, issue_team_id)
        if not state_id:
            print_json({"error": f"Workflow state '{args.status}' not found for issue's team."})
            sys.exit(1)
        variables["stateId"] = state_id

    if args.assignee:
        users_data = linear_request(api_key, FETCH_USERS_QUERY)
        users = users_data["data"]["users"]["nodes"]
        assignee_id = map_user_name_to_id(users, args.assignee)
        if not assignee_id:
            print_json({"error": f"Assignee '{args.assignee}' not found."})
            sys.exit(1)
        variables["assigneeId"] = assignee_id

    label_ids = []
    if args.label:
        get_issue_data = linear_request(api_key, GET_ISSUE_QUERY, {"identifier": args.issue_id})
        if not get_issue_data["data"]["issue"]:
            print_json({"error": f"Issue with ID '{args.issue_id}' not found."})
            sys.exit(1)
        issue_team_id = get_issue_data["data"]["issue"]["team"]["id"]

        labels_data = linear_request(api_key, FETCH_LABELS_QUERY)
        labels = labels_data["data"]["issueLabels"]["nodes"]
        label_id = map_label_name_to_id(labels, args.label, issue_team_id)
        if not label_id:
            print_json({"error": f"Label '{args.label}' not found for team."})
            sys.exit(1)
        label_ids.append(label_id)
        variables["labelIds"] = label_ids

    result = linear_request(api_key, UPDATE_ISSUE_MUTATION, variables)
    print_json(result)

def cmd_get_issue(args):
    api_key = resolve_api_key(args.api_key)
    variables = {"identifier": args.issue_id}
    result = linear_request(api_key, GET_ISSUE_QUERY, variables)
    print_json(result)

def cmd_list_issues(args):
    api_key = resolve_api_key(args.api_key)

    team_id = None
    if args.team_id:
        team_id = args.team_id
    elif args.team_name or args.team_key:
        teams_data = linear_request(api_key, FETCH_TEAMS_QUERY)
        teams = teams_data["data"]["teams"]["nodes"]
        if args.team_name:
            for team in teams:
                if team["name"].lower() == args.team_name.lower():
                    team_id = team["id"]
                    break
        elif args.team_key:
            for team in teams:
                if team["key"].lower() == args.team_key.lower():
                    team_id = team["id"]
                    break
        if not team_id:
            print_json({"error": "Team not found."})
            sys.exit(1)
            
    priority_value = map_priority_to_linear(args.priority) if args.priority else None

    assignee_id = None
    if args.assignee:
        users_data = linear_request(api_key, FETCH_USERS_QUERY)
        users = users_data["data"]["users"]["nodes"]
        assignee_id = map_user_name_to_id(users, args.assignee)
        if not assignee_id:
            print_json({"error": f"Assignee '{args.assignee}' not found."})
            sys.exit(1)

    variables = {
        "teamId": team_id,
        "priority": priority_value,
        "stateType": args.status,
        "assigneeId": assignee_id,
        "first": args.limit
    }
    result = linear_request(api_key, LIST_ISSUES_QUERY, variables)
    print_json(result)

def cmd_add_comment(args):
    api_key = resolve_api_key(args.api_key)
    comment_body = None

    if args.comment_file:
        try:
            comment_body = Path(args.comment_file).read_text()
        except FileNotFoundError:
            print(json.dumps({"error": f"Comment file not found: {args.comment_file}"}), file=sys.stderr)
            sys.exit(1)
    elif args.comment:
        comment_body = args.comment

    if not comment_body:
        print(json.dumps({"error": "Comment body or comment file is required."}), file=sys.stderr)
        sys.exit(1)

    variables = {
        "issueId": args.issue_id,
        "body": comment_body
    }
    result = linear_request(api_key, ADD_COMMENT_MUTATION, variables)
    print_json(result)

# --- Argument Parser ---
def main():
    parser = argparse.ArgumentParser(description="Linear.app CLI for OpenClaw.")
    parser.add_argument("--api-key", help="Linear API key (overrides env var/file)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # List Teams
    list_teams_parser = subparsers.add_parser("list-teams", help="List Linear teams.")
    list_teams_parser.set_defaults(func=cmd_list_teams)

    # List Workflow States
    list_states_parser = subparsers.add_parser("list-workflow-states", help="List Linear workflow states.")
    list_states_parser.set_defaults(func=cmd_list_workflow_states)

    # List Labels
    list_labels_parser = subparsers.add_parser("list-labels", help="List Linear labels.")
    list_labels_parser.set_defaults(func=cmd_list_labels)

    # List Users
    list_users_parser = subparsers.add_parser("list-users", help="List Linear users.")
    list_users_parser.set_defaults(func=cmd_list_users)

    # Create Label
    create_label_parser = subparsers.add_parser("create-label", help="Create a Linear label.")
    create_label_parser.add_argument("--name", required=True, help="Name of the label.")
    create_label_parser.add_argument("--team-id", help="Optional team ID for team-scoped label.")
    create_label_parser.add_argument("--team-name", help="Optional team name for team-scoped label.")
    create_label_parser.add_argument("--team-key", help="Optional team key for team-scoped label.")
    create_label_parser.set_defaults(func=cmd_create_label)

    # Create Issue
    create_parser = subparsers.add_parser("create-issue", help="Create a new Linear issue.")
    create_parser.add_argument("--title", required=True, help="Title of the issue.")
    create_parser.add_argument("--description", help="Description of the issue.")
    create_parser.add_argument("--team-id", help="ID of the team to create the issue in.")
    create_parser.add_argument("--team-name", help="Name of the team to create the issue in (e.g., 'EasyTEK').")
    create_parser.add_argument("--team-key", help="Key of the team to create the issue in (e.g., 'EASY').")
    create_parser.add_argument("--priority", choices=["sin prioridad", "urgente", "alta", "media", "baja"], help="Priority of the issue.")
    create_parser.add_argument("--status", help="Initial status of the issue (e.g., 'Todo', 'In Progress').")
    create_parser.add_argument("--assignee", help="Name of the assignee.")
    create_parser.add_argument("--label", help="Label to apply to the issue (e.g., 'development', 'client').")
    create_parser.set_defaults(func=cmd_create_issue)

    # Update Issue
    update_parser = subparsers.add_parser("update-issue", help="Update an existing Linear issue.")
    update_parser.add_argument("--issue-id", required=True, help="ID of the issue to update (e.g., 'EASY-123').")
    update_parser.add_argument("--title", help="New title of the issue.")
    update_parser.add_argument("--description", help="New description of the issue.")
    update_parser.add_argument("--priority", choices=["sin prioridad", "urgente", "alta", "media", "baja"], help="New priority of the issue.")
    update_parser.add_argument("--status", help="New status of the issue (e.g., 'Todo', 'In Progress').")
    update_parser.add_argument("--assignee", help="Name of the new assignee.")
    update_parser.add_argument("--label", help="New label to apply.")
    update_parser.set_defaults(func=cmd_update_issue)

    # Get Issue
    get_parser = subparsers.add_parser("get-issue", help="Get details of a Linear issue.")
    get_parser.add_argument("--issue-id", required=True, help="ID of the issue (e.g., 'EASY-123').")
    get_parser.set_defaults(func=cmd_get_issue)

    # List Issues
    list_parser = subparsers.add_parser("list-issues", help="List Linear issues.")
    list_parser.add_argument("--team-id", help="ID of the team to filter issues by.")
    list_parser.add_argument("--team-name", help="Name of the team to filter issues by (e.g., 'EasyTEK').")
    list_parser.add_argument("--team-key", help="Key of the team to filter issues by (e.g., 'EASY').")
    list_parser.add_argument("--priority", choices=["sin prioridad", "urgente", "alta", "media", "baja"], help="Filter by priority.")
    list_parser.add_argument("--status", help="Filter by status type (e.g., 'backlog', 'unstarted', 'started', 'completed', 'canceled').")
    list_parser.add_argument("--assignee", help="Filter by assignee name.")
    list_parser.add_argument("--limit", type=int, default=25, help="Maximum number of issues to retrieve.")
    list_parser.set_defaults(func=cmd_list_issues)

    # Add Comment
    add_comment_parser = subparsers.add_parser("add-comment", help="Add a comment to a Linear issue.")
    add_comment_parser.add_argument("--issue-id", required=True, help="ID of the issue to comment on (e.g., 'EASY-123').")
    add_comment_parser.add_argument("--comment", help="The comment body (use with --comment-file for large content).")
    add_comment_parser.add_argument("--comment-file", help="Path to a file containing the comment body.")
    add_comment_parser.set_defaults(func=cmd_add_comment)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
