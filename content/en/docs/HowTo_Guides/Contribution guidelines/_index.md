---
title: "Contribution Guidelines"
linkTitle: "Contribution Guidelines"
weight: 10
description: >
  How to contribute to the docs
---

{{% pageinfo %}}
These guidelines assume that you're familiar with the GitHub workflow.
{{% /pageinfo %}}

## How to Contribute

We use [Hugo](https://gohugo.io/) to format and generate our website, the
[Docsy](https://github.com/google/docsy) theme for styling and site structure, 
and [GitHub Actions for GitHub Pages](https://github.com/peaceiris/actions-gh-pages) to manage the deployment of the site. 
Hugo is an open-source static site generator that provides us with templates, 
content organisation in a standard directory structure, and a website generation 
engine. You write the pages in Markdown (or HTML if you want), and Hugo wraps them up into a website.

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## How to write good documentation

There are four types of documentation: [Tutorials](https://documentation.divio.com/tutorials), [How-To Guides](https://documentation.divio.com/how-to-guides/), [References](https://documentation.divio.com/reference/), and [Explanations](https://documentation.divio.com/explanation/#). 
Consult the [The Documentation System](https://documentation.divio.com/) for:
* [How to write good tutorials](https://documentation.divio.com/tutorials/#how-to-write-good-tutorials)
* [How to write good how-to guides](https://documentation.divio.com/how-to-guides/#how-to-write-good-how-to-guides)
* [How to write good reference guides](https://documentation.divio.com/reference/#how-to-write-good-reference-guides)
* [How to write good explanation](https://documentation.divio.com/explanation/#how-to-write-good-explanation)

## Updating the site

Here's a quick guide to updating the site:

1. Fork the [Project Tetra repo](https://github.com/helpfulengineering/project-tetra) on GitHub.
1. Make your changes and create a pull request (PR).
1. If you're not yet ready for a review, add "WIP" to the PR name to indicate 
  it's a work in progress.
1. Continue updating your doc and pushing your changes until you're happy with 
  the content.
1. When you're ready for a review, add a comment to the PR, and remove any
  "WIP" markers.

## Updating a single page

If you've just spotted something you'd like to change while using the docs, Docsy has a shortcut for you:

1. Click **Edit this page** in the top right hand corner of the page.
1. If you don't already have an up to date fork of the project repo, you are prompted to get one - click **Fork this repository and propose changes** or **Update your Fork** to get an up to date version of the project to edit. The appropriate page in your fork is displayed in edit mode.
1. Follow the rest of the [Updating the site](#updating-the-site) process to propose your changes.

## Previewing your changes

If you want to preview your changes as you work, you'll need to run your own local Hugo server:

1. Follow the instructions in [Getting started](https://gohugo.io/getting-started/installing/) to install Hugo and any other tools you need. You'll need at least **Hugo version 0.68.3**.
  If you install from the [release page](https://github.com/gohugoio/hugo/releases),
  make sure you download the `_extended` version which supports SCSS.
1. Fork the [Project Tetra repo](https://github.com/helpfulengineering/project-tetra) into your own project, then create a local copy using `git clone`. Don’t forget to use `--recurse-submodules` or you won’t pull down some of the code you need to generate a working site.

    ```
    git clone --recurse-submodules --depth 1 https://github.com/<your_github_username>/project-tetra.git
    ```

1. Run `hugo server` in the site root directory. By default your site will be available at `http://localhost:1313/project-tetra`. Now that you're serving your site locally, Hugo will watch for changes to the content and automatically refresh your site.

    ```
    hugo server
    ```

1. Follow the rest of the [Updating the site](#updating-the-site) process to propose your changes.

## Creating an issue

If you've found a problem in the docs, but you're not sure how to fix it yourself, please create an issue in the [Project Tetra repo](https://github.com/helpfulengineering/project-tetra/issues). You can also create an issue about a specific page by clicking the **Create Issue** button in the top right hand corner of the page.

## Useful resources

* [Docsy user guide](wherever it goes): All about Docsy, including how it manages navigation, look and feel, and multi-language support.
* [Hugo documentation](https://gohugo.io/documentation/): Comprehensive reference for Hugo.
* [Github Hello World!](https://guides.github.com/activities/hello-world/): A basic introduction to GitHub concepts and workflow.
