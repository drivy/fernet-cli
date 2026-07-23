# Publishing a new release

Releases are built and published to [PyPI](https://pypi.org/project/fernet-cli/) with [uv](https://docs.astral.sh/uv/).

## Prerequisites

- A PyPI account with the *Maintainer* (or *Owner*) role on the `fernet-cli` project.
- A PyPI API token, ideally scoped to the `fernet-cli` project only:
  <https://pypi.org/manage/account/token/>

## Steps

### 1. Bump the version

Edit `version` in `pyproject.toml`:

```toml
[project]
version = "0.0.4"
```

PyPI rejects re-uploads of an existing version (even after deleting it), so every
release needs a new version number.

Commit the bump:

```sh
git add pyproject.toml
git commit -m "Bump version to 0.0.4"
git tag v0.0.4
git push --follow-tags
```

### 2. Build

```sh
rm -rf dist/
uv build
```

The `rm` matters: `uv publish` uploads **everything** in `dist/`, including stale
artifacts from previous builds.

This produces two files:

- `dist/fernet_cli-0.0.4.tar.gz` (sdist)
- `dist/fernet_cli-0.0.4-py3-none-any.whl` (wheel)

### 3. Publish

```sh
uv publish --token pypi-...
```

Alternatively, export the token as `UV_PUBLISH_TOKEN` to keep it out of your
shell history:

```sh
export UV_PUBLISH_TOKEN=pypi-...
uv publish
```

### 4. Verify

Pull the freshly published package from PyPI into a throwaway environment and
run it:

```sh
uv run --no-project --with fernet-cli --refresh-package fernet-cli -- fernet --help
```
