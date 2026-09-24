# workspace/

This folder is the **Fabric Git integration sync directory**. Do not author files here by hand.

When you connect the Fabric workspace to this repo (Git integration → *Connect* → branch `main`, folder `workspace/`), Fabric serializes each item — including the **Info Request App** — into subfolders here as `.platform` + item definition files, and commits them.

`parameter.yml` in this folder is read by [fabric-cicd](https://microsoft.github.io/fabric-cicd/) to swap environment-specific values during deployment.
