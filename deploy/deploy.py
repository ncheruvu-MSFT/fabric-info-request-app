"""Publish Fabric item definitions from workspace/ to a target Fabric workspace.

Used by GitHub Actions. Authentication is handled by DefaultAzureCredential,
which picks up the Azure CLI login performed by azure/login (GitHub OIDC).

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

# Item types to manage. Extend as the app grows (Notebook, DataPipeline, etc.).
# NOTE: "App" (Fabric App / Info Request App) — confirm fabric-cicd support before
# relying on automated promotion. See README "Fabric App CI/CD caveat".
DEFAULT_ITEM_TYPES = [
    "VariableLibrary",
    "Notebook",
    "DataPipeline",
    "SemanticModel",
    "Report",
    # "App",
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
