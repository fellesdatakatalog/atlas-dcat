"""Nox sessions."""

import os
import sys
from typing import List

import nox
from nox_poetry import Session, session

python_versions = ["3.11"]
nox.options.envdir = ".cache"  # To run consecutive nox sessions faster.
locations = ["fdk_atlas_dcat_service", "tests"]
nox.options.sessions = ("lint", "format", "mypy", "tests")

ENV_VARS = {"API_KEY": "test-key"}


@session(python=python_versions[0])
def cache(session: Session) -> None:
    """Clear cache."""
    session.run(
        "bash",
        "-c",
        "for f in $(find . -maxdepth 1 -name '*cache*'); do rm -rf $f; done",
        external=True,
    )
    session.run(
        "bash",
        "-c",
        "for f in $(find . -maxdepth 4 -name '__pycache__'); do rm -rf $f; done",
        external=True,
    )


@session(python=python_versions[0])
def openapi(session: Session) -> None:
    """Generate API spec from code."""
    session.install(".")
    session.install("PyYAML")
    session.run("python", "openapi.py")


@session(python=python_versions[0])
def ruff(session: Session) -> None:
    """Run ruff code linter and formatter."""
    session.notify("lint")
    session.notify("format")


@session(python=python_versions[0])
def lint(session: Session) -> None:
    """Run ruff linter."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", *args)


@session(python=python_versions[0])
def format(session: Session) -> None:
    """Run ruff code formatter."""
    if os.getenv("CI"):
        print("Skipping ruff in CI")
        return
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "format", *args)


@session(python=python_versions[0])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or [
        "--install-types",
        "--non-interactive",
        "--no-namespace-packages",
        *locations,
    ]
    session.install(".", "mypy", "pytest")
    session.run("mypy", *args)
    # --python-executable to get nox/nox_poetry type information without installing in virtualenv.
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")
