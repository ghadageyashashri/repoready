from repoready.checks import check_dependency_file, check_readme
from repoready.models import Status


def test_readme_found(tmp_path):
    (tmp_path / "README.md").write_text("# Hello")
    assert check_readme(tmp_path).status == Status.PASS


def test_readme_missing(tmp_path):
    assert check_readme(tmp_path).status == Status.FAIL


def test_dependency_file_found(tmp_path):
    (tmp_path / "requirements.txt").write_text("requests")
    assert check_dependency_file(tmp_path).status == Status.PASS


def test_dependency_file_missing(tmp_path):
    assert check_dependency_file(tmp_path).status == Status.FAIL