# SDLC & CI/CD for the Fabric Info Request App

Refined application lifecycle guide for the **Info Request App** (a Microsoft **Fabric App**, codename *Rayfin*), aligned to the current Microsoft Fabric CI/CD platform. Tracks the CI/CD updates released through **September 2026**.

---

## 1. What changed recently (track these)

| Update | Why it matters here | Reference |
|--------|--------------------|-----------|
| **fabric-cicd v1.3.0** — bulk publish (single API call), dynamic replacement variables (`$sqlendpoint`, `$workspace.$name`), case-insensitive `find_replace`, private-link FQDN support, configurable API retry duration, feature-flag controls | Faster, more robust deploys; parameterize by endpoint/name instead of hard-coded GUIDs | [Releases](https://github.com/microsoft/fabric-cicd/releases) · [Docs](https://microsoft.github.io/fabric-cicd/) |
| **Deployment pipelines — new UI (preview)** and a much broader supported-items list (Data Agents, User Data Functions, Variable Library, Cosmos DB, Graph Model/QuerySet, Ontology/Plan, dbt/Airflow) | More of the solution can be promoted natively across Dev/Test/Prod | [Deployment pipelines overview](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines) |
| **Network security for CI/CD** — workspace-level inbound/outbound controls integrated with Git integration | Keeps app + data inside trusted network boundaries during CI/CD | [CI/CD network security](https://learn.microsoft.com/en-us/fabric/cicd/cicd-security) |
| **Data Agent** is now a first-class CI/CD item (Git + pipelines + fabric-cicd) | Directly supports the companion Fabric Data Agent scenario | [Create a Data Agent](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent) |
| **Semantic model retirement (Feb 12, 2026)** — deployment pipelines drop support for models not on Enhanced Metadata | Upgrade any semantic model the app depends on before that date | [Retirement notice](https://learn.microsoft.com/en-us/fabric/cicd/troubleshoot-cicd#retirement-of-semantic-model-support-for-deployment-pipelines) |

---

## 2. SDLC model

```
Developer branch-out workspace  ── PR + review ──▶  main
        │                                              │
        │                          ci-dev.yml (auto)  ──▶  Dev workspace
        │                                              │
                           promote.yml (approval gate) ──▶ Test ──▶ Prod
```

- **Branch strategy:** trunk-based on `main`; developers use Fabric **branch-out to a new workspace** for isolated work, then PR back. Diffs of item definitions are reviewed in GitHub.
- **Environments:** three Fabric workspaces (Dev / Test / Prod), each on its own capacity, mapped to GitHub Environments `dev` / `Test` / `Prod`.
- **Promotion:** auto-deploy to Dev on merge; manual, approval-gated promotion to Test then Prod.
- **Config as code:** environment-specific values (workspace IDs, connection GUIDs, SQL endpoints) resolved by the **Variable library** and `workspace/parameter.yml`.

---

## 3. Reference architecture (maps to the Fabric CI/CD platform)

| Platform layer | This solution | Docs |
|----------------|---------------|------|
| Source control | GitHub `main`; item defs under `workspace/` via **Git integration** | [Git integration](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration) |
| Delivery | **Deployment pipelines** and/or GitHub Actions + fabric-cicd | [Deployment pipelines](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines) |
| Config as code | **Variable library** + `parameter.yml` | [Variable library](https://learn.microsoft.com/en-us/fabric/cicd/variable-library/variable-library-overview) |
| Automation | GitHub Actions (`ci-dev.yml`, `promote.yml`) with OIDC | — |
| Deployment engine | **fabric-cicd** `publish_all_items` | [fabric-cicd](https://microsoft.github.io/fabric-cicd/) |
| Foundation API | **Fabric REST APIs** | [Using Fabric APIs](https://learn.microsoft.com/en-us/rest/api/fabric/articles/get-started/using-fabric-apis) |
| Scripting / IaC | **Fabric CLI** (`fab`), **Terraform** provider | [Fabric CLI](https://learn.microsoft.com/en-us/rest/api/fabric/articles/fabric-command-line-interface) · [Terraform](https://registry.terraform.io/providers/microsoft/fabric/latest/docs) |

---

## 4. Item coverage for this app

| Item | Git integration | Deployment pipelines | fabric-cicd (v1.3.0) |
|------|:---:|:---:|:---:|
| Info Request **App** (Rayfin) | ✅ source control | ⚠️ verify in [supported items](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines#supported-items) | ❌ not yet listed |
| Notebook | ✅ | ✅ | ✅ |
| Data Pipeline | ✅ | ✅ | ✅ |
| Semantic model | ✅ | ✅ (Enhanced Metadata only) | ✅ |
| Report | ✅ | ✅ (preview) | ✅ |
| Variable library | ✅ | ✅ | ✅ |
| Data Agent | ✅ | ✅ | ✅ |

> **fabric-cicd base rule:** it only supports items that expose source control **and** public create/update APIs. The Fabric App item isn't there yet — see the gap below.

---

## 5. The Fabric App gap — recommended handling

The **App** item is newer than the surrounding items. Until it appears in the fabric-cicd supported list and/or deployment-pipeline supported items:

1. **Source control now** — Git integration versions the App definition in `workspace/` for backup, review, and rollback.
2. **Promote supporting items** with fabric-cicd (Notebooks, Pipelines, Semantic models, Variable library, Data Agent).
3. **Promote the App** via Git-based deployment pipelines when the item type is supported, otherwise via the **Fabric REST API** as a scripted step in `promote.yml`.
4. **Re-check monthly** — add `"App"` to `DEFAULT_ITEM_TYPES` in `deploy/deploy.py` as soon as fabric-cicd lists it.

---

## 6. Security & governance

- **Identity:** Entra **service principal** + GitHub **OIDC federated credentials** (no stored secrets). Enable *Service principals can use Fabric APIs* and grant workspace access.
- **Network:** apply **[CI/CD network security](https://learn.microsoft.com/en-us/fabric/cicd/cicd-security)** (workspace inbound/outbound) so deploys stay inside trusted boundaries; use fabric-cicd private-link FQDN config for private workspaces.
- **Approvals:** GitHub Environment **required reviewers** on Test/Prod; branch protection + required PR review on `main`.
- **Capacity isolation:** separate capacities per stage so Prod is never starved by Dev/Test.

---

## 7. Staying current

Track these sources (they change monthly):

- Fabric **What's New**: https://learn.microsoft.com/en-us/fabric/fundamentals/whats-new
- Fabric **Updates Blog**: https://blog.fabric.microsoft.com/
- **fabric-cicd releases**: https://github.com/microsoft/fabric-cicd/releases
- **Git integration supported items**: https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration#supported-items
- **Deployment pipelines supported items**: https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines#supported-items

---

## Links index

- CI/CD overview: https://learn.microsoft.com/en-us/fabric/cicd/cicd-overview
- Git integration: https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration
- Deployment pipelines: https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines
- Variable library: https://learn.microsoft.com/en-us/fabric/cicd/variable-library/variable-library-overview
- CI/CD network security: https://learn.microsoft.com/en-us/fabric/cicd/cicd-security
- Fabric REST APIs: https://learn.microsoft.com/en-us/rest/api/fabric/articles/get-started/using-fabric-apis
- Fabric CLI: https://learn.microsoft.com/en-us/rest/api/fabric/articles/fabric-command-line-interface
- fabric-cicd: https://microsoft.github.io/fabric-cicd/ · https://github.com/microsoft/fabric-cicd
- Terraform provider for Fabric: https://registry.terraform.io/providers/microsoft/fabric/latest/docs
