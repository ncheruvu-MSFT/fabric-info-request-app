# Setup: Git integration + GitHub Actions for the Info Request App

## 1. Service principal (Entra app) with GitHub OIDC

1. Register an Entra application (e.g. `sp-fabric-info-request-cicd`).
2. Add a **Federated credential** for GitHub Actions:
   - Issuer: `https://token.actions.githubusercontent.com`
   - Subject (per environment), e.g. `repo:ncheruvu-MSFT/fabric-info-request-app:environment:dev`
   - Add one federated credential per environment: `dev`, `Test`, `Prod`.
3. In the **Fabric Admin portal**, enable *Service principals can use Fabric APIs* for a security group, and add the SP to it.
4. Grant the SP **workspace access** (Admin/Member) on the Dev/Test/Prod workspaces.

> No client secret is stored — GitHub OIDC exchanges a short-lived token via the federated credential.

## 2. GitHub Environments

Create three environments under **Settings → Environments**: `dev`, `Test`, `Prod`.

For each, set **Environment variables**:

| Variable | Value |
|----------|-------|
| `AZURE_CLIENT_ID` | Entra app (client) ID |
| `AZURE_TENANT_ID` | `62c0cb46-1fcc-4c79-ba1b-d7d9fdfbaa68` |
| `FABRIC_WORKSPACE_ID` | that stage's workspace GUID |

On `Test` and `Prod`, add **Required reviewers** so promotion needs approval.

## 3. Connect Fabric workspace to Git

In the **Dev** Fabric workspace → **Workspace settings → Git integration**:
- Provider: **GitHub**
- Repository: `ncheruvu-MSFT/fabric-info-request-app`
- Branch: `main`
- Folder: `workspace`

Commit the current workspace state. Fabric writes the Info Request App (and any Notebooks / pipelines / semantic models) into `workspace/`.

## 4. Development loop

1. Developer uses **branch-out to new workspace** for isolated work.
2. Open a PR into `main`; review the diff of item definitions.
3. Merge → `ci-dev.yml` publishes to the Dev workspace.
4. Run **Promote to Test/Prod** (`promote.yml`) when ready; approve the gate.

## 5. Parameterization

Update [`workspace/parameter.yml`](../workspace/parameter.yml) with the Test/Prod workspace IDs and any connection GUIDs that must be rebound per environment.
