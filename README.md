# Fabric Info Request App — CI/CD

Source control and CI/CD scaffold for the **Info Request App** (a Microsoft **Fabric App**, codename *Rayfin*) used for internal workflow / info-request scenarios.

This repo wires the Fabric App into an enterprise SDLC using the [Microsoft Fabric CI/CD platform](https://learn.microsoft.com/en-us/fabric/cicd/cicd-overview):

- **Git integration** — Fabric commits item definitions into [`workspace/`](workspace/).
- **GitHub Actions** — automated deploy to **Dev**, gated promotion to **Test** and **Prod**.
- **[fabric-cicd](https://github.com/microsoft/fabric-cicd)** — Python deployment library that publishes item definitions to a target workspace.
- **Parameterization** — environment-specific values swapped via [`workspace/parameter.yml`](workspace/parameter.yml).

## Source item

| Field | Value |
|-------|-------|
| App item (Dev) | `edb99392-0b5e-4319-a5a0-a04d0f4d8063` |
| Dev workspace | `d671b9e3-a688-4011-bc80-37aff6f7b856` |
| Tenant | `62c0cb46-1fcc-4c79-ba1b-d7d9fdfbaa68` |
| Portal | https://app.powerbi.com/groups/d671b9e3-a688-4011-bc80-37aff6f7b856/appbackends/edb99392-0b5e-4319-a5a0-a04d0f4d8063 |

> The **actual item JSON is not committed by hand**. Connect the Fabric workspace to this repo via Git integration (see [docs/git-integration-setup.md](docs/git-integration-setup.md)) and Fabric will populate `workspace/` on first commit.

## Repo layout

```
.
├── workspace/            # Fabric Git-integration sync folder (item defs land here)
│   └── parameter.yml     # fabric-cicd environment parameterization
├── deploy/
│   └── deploy.py         # fabric-cicd publish script (used by CI)
├── config/
│   └── environments.yml  # Dev/Test/Prod workspace mapping (reference)
├── .github/workflows/
│   ├── ci-dev.yml        # push to main -> deploy to Dev
│   └── promote.yml       # manual -> promote to Test / Prod (gated)
├── docs/
│   ├── git-integration-setup.md
│   └── architecture.md
└── requirements.txt
```

## Flow

```
Developer branch-out workspace ──PR──▶ main
        │                                 │
        │                    ci-dev.yml (auto) ──▶ Dev workspace
        │                                 │
                          promote.yml (approval) ──▶ Test ──▶ Prod
```

## Quick start

1. Create a Fabric **service principal**, grant it workspace access, and set up an Entra app with **federated credentials** for GitHub OIDC (see [docs/git-integration-setup.md](docs/git-integration-setup.md)).
2. Create three GitHub **Environments**: `dev`, `Test`, `Prod`. Add required reviewers on `Test`/`Prod`.
3. Set per-environment variables `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `FABRIC_WORKSPACE_ID`.
4. Connect the Dev Fabric workspace to this repo (`main`, folder `workspace/`) via Git integration.
5. Commit from Fabric → PR → merge → `ci-dev.yml` deploys → run `promote.yml` for Test/Prod.

## Fabric App CI/CD caveat

Fabric App is a newer item type. Confirm it appears in the **supported items** lists before relying on automated promotion:
- [Git integration supported items](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration#supported-items)
- [Deployment pipelines supported items](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines#supported-items)

If the App item is not yet supported by fabric-cicd, use Git integration for source control now and fall back to the Fabric REST API for the App item until coverage lands. Adjust `DEFAULT_ITEM_TYPES` in [`deploy/deploy.py`](deploy/deploy.py) accordingly.
