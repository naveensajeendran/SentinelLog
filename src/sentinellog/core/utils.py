import os


def project_root() -> str:
    """Returns project root based on current file path."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../..")
    )


def resolve_path(*parts) -> str:
    """Safely joins paths relative to project root."""
    return os.path.join(project_root(), *parts)