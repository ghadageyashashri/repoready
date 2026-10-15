from pathlib import Path
from .models import CheckResult,Status
import os 
CODE_SUFFIXES = {".py", ".js", ".ts", ".java", ".go", ".rs", ".rb", ".php", ".c", ".cpp", ".cs"}
SKIP_FOLDERS = {".git", ".venv", "node_modules", "__pycache__"}


def _has_code_files(folder: Path) -> bool:
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS]
        if any(Path(f).suffix in CODE_SUFFIXES for f in files):
            return True
    return False
def check_readme(folder: Path)->CheckResult:
    for name in ("README.md", "README.rst", "README.txt", "README"):
        if(folder / name).is_file():
            return CheckResult("README",Status.PASS,f"Found {name}")
    return CheckResult("README", Status.FAIL,"No README file found")

def check_dependency_file(folder: Path) -> CheckResult:
    candidates = [
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "Pipfile",
        "package.json",
    ]
    found = [name for name in candidates if (folder / name).is_file()]
    if found:
        return CheckResult("Dependencies", Status.PASS, "Found: " + ", ".join(found))
    if not _has_code_files(folder):
        return CheckResult(
            "Dependencies",
            Status.UNKNOWN,
            "No code files found, so a dependency file may not be needed",
        )
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

def run_all_checks(folder: Path) -> list[CheckResult]:
    checks = [
        check_readme,
        check_dependency_file,
        check_gitignore,
        check_env_example,
    ]
    return [check(folder) for check in checks]