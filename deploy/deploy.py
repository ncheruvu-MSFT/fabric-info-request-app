"""Publish Fabric item definitions from workspace/ to a target Fabric workspace.

Used by GitHub Actions. Authentication is handled by DefaultAzureCredential,
which picks up the Azure CLI login performed by azure/login (GitHub OIDC).

Requires fabric-cicd >= 1.3.0. New capabilities you can opt into:
  - Bulk publish (single API call) for faster deploys.
  - Dynamic replacement variables in parameter.yml (e.g. $sqlendpoint,
    $workspace.$name) and case-insensitive find_replace.
  - Private-link workspaces via configure_fabric_fqdn.
  - FABRIC_CICD_RETRY_API_MAX_DURATION_SECONDS to tune long-running polling.

Env vars:
  FABRIC_WORKSPACE_ID  target workspace GUID
  FABRIC_ENVIRONMENT   Dev | Test | Prod  (selects parameter.yml replace values)
  FABRIC_REPO_DIR      path to the Git-synced item folder (default: workspace)
  FABRIC_ITEM_TYPES    optional comma-separated override of item types in scope
"""
import os

from azure.identity import DefaultAzureCredential
from fabric_cicd import (
    FabricWorkspace,
    publish_all_items,
    unpublish_all_orphan_items,
)

# Item types managed by fabric-cicd for this solution.
# These are all in fabric-cicd's supported item list (v1.3.0):
# https://microsoft.github.io/fabric-cicd/latest/  -> Supported Item Types
#
# NOTE: the Fabric "App" (Info Request App / Rayfin) item is NOT yet in the
# fabric-cicd supported list, because it does not yet expose the public
# create/update + source-control APIs fabric-cicd requires. Source-control the
# App via Git integration now; promote it with Git-based deployment pipelines /
# REST API until fabric-cicd adds coverage. See docs/sdlc.md.
DEFAULT_ITEM_TYPES = [
    "VariableLibrary",
    "Notebook",
    "DataPipeline",
    "SemanticModel",
    "Report",
    "DataAgent",   # supported since fabric-cicd added Data Agent items
    # "App",       # not yet supported by fabric-cicd (see note above)
]


def main() -> None:
    workspace_id = os.environ["FABRIC_WORKSPACE_ID"]
    environment = os.environ.get("FABRIC_ENVIRONMENT", "Dev")
    repo_dir = os.environ.get("FABRIC_REPO_DIR", "workspace")
    item_types_env = os.environ.get("FABRIC_ITEM_TYPES")
    item_types = (
        [t.strip() for t in item_types_env.split(",") if t.strip()]
        if item_types_env
        else DEFAULT_ITEM_TYPES
    )

    print(f"Deploying to workspace={workspace_id} environment={environment} dir={repo_dir}")
    print(f"Item types in scope: {item_types}")

    target = FabricWorkspace(
        workspace_id=workspace_id,
        environment=environment,
        repository_directory=repo_dir,
        item_type_in_scope=item_types,
        token_credential=DefaultAzureCredential(),
    )

    publish_all_items(target)
    unpublish_all_orphan_items(target)
    print("Deployment complete.")


if __name__ == "__main__":
    main()
