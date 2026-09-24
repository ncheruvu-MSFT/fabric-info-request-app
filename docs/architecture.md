# Architecture — Info Request App CI/CD

## Layers (maps to the Fabric CI/CD platform)

| Layer | This repo |
|-------|-----------|
| Source control | GitHub `main`, item defs under `workspace/` via Fabric Git integration |
| CI automation | GitHub Actions (`ci-dev.yml`, `promote.yml`) |
| Deployment | [fabric-cicd](https://github.com/microsoft/fabric-cicd) `publish_all_items` in `deploy/deploy.py` |
| Config as code | `workspace/parameter.yml` (per-stage value swaps) |
| Identity | Entra service principal + GitHub OIDC federated credentials |

## Promotion flow

```
              branch-out workspace (per dev)
                        │  PR + review
                        ▼
  GitHub main ──push──▶ ci-dev.yml ──fabric-cicd──▶ Dev workspace
                        │
                        ▼ (manual dispatch + approval)
                  promote.yml ──fabric-cicd──▶ Test workspace
                        │  (approval)
                        ▼
                  promote.yml ──fabric-cicd──▶ Prod workspace
```

Each stage is a separate Fabric workspace on its own capacity. `parameter.yml`
rebinds workspace IDs and connection references so a promoted app points at the
correct stage resources.

## References

- Fabric CI/CD overview: https://learn.microsoft.com/en-us/fabric/cicd/cicd-overview
- Git integration supported items: https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration#supported-items
- Deployment pipelines supported items: https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines#supported-items
- fabric-cicd docs: https://microsoft.github.io/fabric-cicd/
