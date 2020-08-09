# prevent-submodule-regression

Pre-commit hook to prevent accidental submodule regressions

## Description

Do you find yourself (or your collaborators) constantly rolling back submodule
SHAs because someone forgot to `git submodule update` before running `git add
.` or `git commit -a …`?

This pre-commit plugin will prevent those nasty surprises from making their
way into your repositories.

## Installation

### As a git hook

The simplest way to use this package is as a plugin to [pre-commit](https://pre-commit.com/).

A sample configuration:

```yaml
repos:
  # […]
  - repo: https://github.com/erikogan/prevent-submodule-regression
    rev: v0.1.1
    hooks:
      - id: prevent-submodule-regression
        # By default hooks only operat on plain files, which do not include
        # submodules. This setting has been added to the hook configuration,
        # but it is not consistently honored. The safest approach is to be
        # explicit in your configuration.
        types: [directory]
```

Example failure output:

![submodule_example](https://user-images.githubusercontent.com/60583/89809067-ec04d500-daef-11ea-9d43-7e990ea21234.png)


### As a standalone script

```
pip install prevent-submodule-regression [path…]
```

If you run the script with no arguments, it will automatically find all the
configured submodules. You can also pass it a list of files to check.

It will currently ignore any path that is not staged to be commit. A future
version of the script will have an argument to override that behavior.

## TODO

In no particular order:

* Actual tests
* Ways to override the error and allow you to commit a regression.
  * Command-line
  * Environment variables
* Ways to override (or disable) colorization codes
  * Command-line
  * Environment variables
* Usage information via `--help`
* Actual command-line flag parsing
