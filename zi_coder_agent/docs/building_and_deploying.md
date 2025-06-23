# Building and Deploying Zi Coder Agent Documentation

## Building the Documentation
To build the documentation site for deployment, use the following command from the `zi_coder_agent` directory:

```bash
python -m mkdocs build
```

This will generate the static site in the `site` directory, which can be hosted on any static web server.

## Running the Development Server
To preview the documentation locally during development, run:

```bash
python -m mkdocs serve
```

This starts a local server at `http://127.0.0.1:8000/` where you can view the documentation in real-time with automatic reloading on file changes.

## Deploying to GitHub Pages
If you wish to deploy the documentation to GitHub Pages, ensure your repository is set up with a `gh-pages` branch. Then, use the following command:

```bash
python -m mkdocs gh-deploy
```

This command builds the site and pushes it to the `gh-pages` branch of your repository, making it available at `https://<username>.github.io/<repository-name>/`.

*Note: Ensure that the `repo_url` in `mkdocs.yml` is correctly set to your repository URL for proper deployment configuration.*

## Custom Deployment
For deployment to other hosting services, build the site using the `build` command and upload the contents of the `site` directory to your hosting provider.

*Note: This document provides basic instructions for building and deploying the documentation. Additional configurations or steps may be required based on specific hosting environments or project needs.*
