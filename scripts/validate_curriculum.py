from __future__ import annotations

from app.data.curriculum import validate_curriculum_content


def main() -> int:
    issues = validate_curriculum_content()
    if issues:
        print("Curriculum validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Curriculum validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
