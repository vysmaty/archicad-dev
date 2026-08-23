from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cpp_build_uses_visual_studio_2022_runner() -> None:
    workflow = (ROOT / ".github" / "workflows" / "build.yml").read_text(encoding="utf-8")

    assert "runs-on: windows-2022" in workflow
    assert "runs-on: windows-latest" not in workflow


def test_ci_runs_python_quality_and_all_six_cpp_builds() -> None:
    workflow = (ROOT / ".github" / "workflows" / "build.yml").read_text(encoding="utf-8")

    assert "uv run ruff check ." in workflow
    assert "uv run ty check" in workflow
    assert "uv run pytest" in workflow
    assert workflow.count("configuration: Debug") == 3
    assert workflow.count("configuration: Release") == 3


def test_scheduled_updates_only_open_a_review_pr() -> None:
    workflow = (ROOT / ".github" / "workflows" / "upstream-updates.yml").read_text(encoding="utf-8")

    assert "schedule:" in workflow
    assert "tools/check_updates.py --apply" in workflow
    assert "create-pull-request" in workflow
    assert "gh pr merge" not in workflow.lower()
