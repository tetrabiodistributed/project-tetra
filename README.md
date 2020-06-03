# Project Tetra - Project Repository
This repository contains the content and source code for generating the Project Tetra site.
For more information about Project Tetra, please visit https://helpfulengineering.github.io/project-tetra/docs/

This Project is hosted at https://helpfulengineering.github.io/project-tetra (soon to be migrated to https://helpfulengineering.github.io/project-tetra)

## Prerequisites

The following are basic prerequisites for previewing the Project Tetra site on your local machine:

- [Install Hugo](https://gohugo.io/getting-started/installing/) for your specific platform.
  If you install from the [release page](https://github.com/gohugoio/hugo/releases),
  make sure you download the `_extended` version which supports SCSS.

## Cloning the Project Tetra Project

The following will clone the project repository onto your local machine.
This will allow you to edit and preview changes to the project site
(don't forget to use `--recurse-submodules` or you won't pull down some of the code you need to generate a working site).

```bash
git clone --recurse-submodules --depth 1 https://github.com/helpfulengineering/project-tetra.git
cd project-tetra
```

## Running the website locally

Once you've cloned the project repo, from the `project-tetra` root directory, run:

```bash
hugo server
```

The `hugo server` command builds and serves the site.
If you just want to build the site, run `hugo` instead.
