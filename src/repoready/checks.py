from pathlib import Path
from .models import CheckResult,Status
def check_readme(folder: Path)->CheckResult:
    for name in ("README.md", "README.rst", "README.txt", "README"):
        if(folder / name).is_file():
            return CheckResult("README",Status.PASS,f"Found{name}")
    return CheckResult("README", Status.FAIL,"No README file found")

def check_dependency_file(folder:Path)->CheckResult:
    candidates=[
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "Pipfile",
        "package.json",
    ]
    found=[name for name in candidates if(folder / name).is_file()]
    if found:
        return CheckResult("Dependencies",Status.PASS, "Found: "+ ", ".join(found))
    return CheckResult("Dependencies", Status.FAIL, "No dependency file found")

def check_gitignore(folder: Path) -> CheckResult:
    if (folder / ".gitignore").is_file():
        return CheckResult(".gitignore", Status.PASS, "Found .gitignore")
    return CheckResult(
        ".gitignore", Status.WARNING, "No .gitignore found (junk files may get committed)"
    )


def check_env_example(folder: Path) -> CheckResult:
    has_env = (folder / ".env").is_file()
    has_example = (folder / ".env.example").is_file()

    if has_example:
        return CheckResult(".env.example", Status.PASS, "Found .env.example")
    if has_env:
        return CheckResult(
            ".env.example",
            Status.WARNING,
            ".env exists but .env.example is missing; new developers won't know which settings to create",
        )
    return CheckResult(".env.example", Status.PASS, "No .env file in use, nothing to document")