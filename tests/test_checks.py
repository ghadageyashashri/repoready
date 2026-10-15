from repoready.checks import check_dependency_file, check_readme
from repoready.models import Status 
from repoready.checks import (
    check_dependency_file,
    check_env_example,
    check_gitignore,
    check_readme,
    run_all_checks,
)


def test_readme_found(tmp_path):
    (tmp_path / "README.md").write_text("# Hello")
    assert check_readme(tmp_path).status == Status.PASS


def test_readme_missing(tmp_path):
    assert check_readme(tmp_path).status == Status.FAIL


def test_dependency_file_found(tmp_path):
    (tmp_path / "requirements.txt").write_text("requests")
    assert check_dependency_file(tmp_path).status == Status.PASS


def test_dependency_file_missing_with_code_fails(tmp_path):
    (tmp_path / "main.py").write_text("print('hi')")
    assert check_dependency_file(tmp_path).status == Status.FAIL


def test_dependency_file_missing_without_code_is_unknown(tmp_path):
    assert check_dependency_file(tmp_path).status == Status.UNKNOWN

from repoready.checks import (
    check_dependency_file,
    check_env_example,
    check_gitignore,
    check_readme,
)

def test_gitignore_found(tmp_path):
    (tmp_path / ".gitignore").write_text(".venv/")
    assert check_gitignore(tmp_path).status == Status.PASS


def test_gitignore_missing(tmp_path):
    assert check_gitignore(tmp_path).status == Status.WARNING


def test_env_example_found(tmp_path):
    (tmp_path / ".env").write_text("KEY=1")
    (tmp_path / ".env.example").write_text("KEY=")
    assert check_env_example(tmp_path).status == Status.PASS


def test_env_without_example_warns(tmp_path):
    (tmp_path / ".env").write_text("KEY=1")
    assert check_env_example(tmp_path).status == Status.WARNING


def test_no_env_files_is_fine(tmp_path):
    assert check_env_example(tmp_path).status == Status.PASS

def test_run_all_checks_returns_every_result(tmp_path):
    results = run_all_checks(tmp_path)
    assert len(results) == 4