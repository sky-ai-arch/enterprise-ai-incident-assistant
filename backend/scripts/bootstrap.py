from pathlib import Path

PROJECT_STRUCTURE = {
    ".github": {
        "workflows": {
            "ci.yml": "",
            "release.yml": "",
        },
        "ISSUE_TEMPLATE": {},
        "PULL_REQUEST_TEMPLATE.md": "",
    },

    "backend": {
        "src": {
            "incident_assistant": {

                "__init__.py": "",
                "main.py": "",

                "api": {
                    "__init__.py": "",
                    "dependencies.py": "",
                    "routers": {
                        "__init__.py": "",
                    },
                    "v1": {
                        "__init__.py": "",
                    },
                },

                "domain": {
                    "__init__.py": "",
                    "entities": {
                        "__init__.py": "",
                    },
                    "value_objects": {
                        "__init__.py": "",
                    },
                    "interfaces": {
                        "__init__.py": "",
                    },
                    "exceptions": {
                        "__init__.py": "",
                    },
                },

                "application": {
                    "__init__.py": "",
                    "services": {
                        "__init__.py": "",
                    },
                    "use_cases": {
                        "__init__.py": "",
                    },
                    "dto": {
                        "__init__.py": "",
                    },
                },

                "agents": {
                    "__init__.py": "",
                    "base.py": "",
                    "planner.py": "",
                    "metrics.py": "",
                    "logs.py": "",
                    "reporter.py": "",
                },

                "workflows": {
                    "__init__.py": "",
                },

                "infrastructure": {
                    "__init__.py": "",

                    "database": {
                        "__init__.py": "",
                        "base.py": "",
                        "session.py": "",
                    },

                    "llm": {
                        "__init__.py": "",
                        "factory.py": "",
                    },

                    "providers": {
                        "__init__.py": "",
                    },

                    "persistence": {
                        "__init__.py": "",
                    },

                    "tools": {
                        "__init__.py": "",
                    },

                    "memory": {
                        "__init__.py": "",
                    },

                    "telemetry": {
                        "__init__.py": "",
                    },
                },

                "shared": {
                    "__init__.py": "",

                    "config": {
                        "__init__.py": "",
                        "settings.py": "",
                    },

                    "logging": {
                        "__init__.py": "",
                        "logger.py": "",
                    },

                    "constants": {
                        "__init__.py": "",
                    },

                    "exceptions": {
                        "__init__.py": "",
                        "base.py": "",
                    },

                    "utils": {
                        "__init__.py": "",
                    },
                },
            },
        },

        "tests": {
            "unit": {},
            "integration": {},
            "e2e": {},
        },

        "scripts": {},

        "pyproject.toml": "",
        "Dockerfile": "",
    },

    "docs": {
        "architecture": {},
        "adr": {},
        "api": {},
        "diagrams": {},
        "runbooks": {},
    },

    "infra": {
        "docker": {},
        "compose": {},
        "kubernetes": {},
    },

    "examples": {},

    "datasets": {},

    ".env.example": "",
    "docker-compose.yml": "",
    "Makefile": "",
}


created_dirs = 0
created_files = 0


def create_structure(base: Path, structure: dict):
    global created_dirs, created_files

    for name, content in structure.items():
        path = base / name

        # File
        if isinstance(content, str):
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
                created_files += 1
            continue

        # Directory
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created_dirs += 1

        create_structure(path, content)


def main():
    project_root = Path.cwd()

    print("=" * 60)
    print(" Enterprise AI Incident Assistant Bootstrap")
    print("=" * 60)

    create_structure(project_root, PROJECT_STRUCTURE)

    print("\nBootstrap completed successfully.\n")
    print(f"Directories created : {created_dirs}")
    print(f"Files created       : {created_files}")
    print(f"Project root        : {project_root}")


if __name__ == "__main__":
    main()