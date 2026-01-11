git-actions
========================================================================


Introducción a GitHub Actions
-----------------------------

You can write individual tasks, called **actions**, and combine them to
create a custom workflow. Workflows are custom automated processes that
you can set up in your repository to build, test, package, release, or
deploy any code project on GitHub.

With GitHub Actions you can build end-to-end continuous integration (CI)
and continuous deployment (CD) capabilities directly in your repository.

Workflows run in Linux, macOS, Windows, and containers on GitHub-hosted
machines, called **runners**. Alternatively, you can also host your own
runners to run workflows on machines you own or manage.

You can create workflows using actions defined in your repository, open
source actions in a public repository on GitHub, or a published Docker
container image. Workflows in forked repositories don’t run by default.

You can discover actions to use in your workflow on GitHub and build
actions to share with the GitHub community. Discovering actions in the
`GitHub community GitHub
Marketplace <https://github.com/marketplace?type=actions>`__ is a
central location for you to find, share, and use actions built by t

Límites de uso
--------------

There are some limits on GitHub Actions usage, and will vary depending
on whether you use GitHub-hosted or self-hosted runners. Here we only
consider the limitations for GutHub Hosted.

-  **Job execution time:** A job in a workflow can run for up to **6
hours** of execution time.

-  **Workflow run time**: The workflow run is limited to **72 hours**.

-  **API requests**: You can execute up to **1000 API requests in an
hour** across all actions **within a repository**.

-  **Concurrent jobs**: The number of concurrent jobs you can run in
your account depends on your GitHub plan, as indicated in the
following table.

| GitHub plan \| Total concurrent jobs \| Maximum concurrent macOS jobs
\|

\|————-:———————-:\|——————————:\| \| Free \| 20 \| 5 \| \| Pro \| 40 \| 5
\| \| Team \| 60 \| 5 \| \| Enterprise \| 180 \| 50 \|

-  **Job matrix**: A job matrix can generate a maximum of **256 jobs per
workflow run**.
