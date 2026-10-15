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