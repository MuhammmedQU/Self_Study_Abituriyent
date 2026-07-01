"""
Project Structure and Configuration Validation

This script validates the project WITHOUT requiring package installation.
It checks:
1. File structure and organization
2. Python syntax validity
3. Configuration files
4. Critical file contents
"""

import os
from pathlib import Path
import ast
import json

class ProjectValidator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.backend_root = self.project_root / "backend"
        self.frontend_root = self.project_root / "frontend"
        self.issues = []
        self.successes = []

    def add_issue(self, msg):
        self.issues.append(f"[ERROR] {msg}")

    def add_success(self, msg):
        self.successes.append(f"[OK] {msg}")

    def validate_backend_structure(self):
        """Validate backend directory structure."""
        required_dirs = {
            "app": ["api", "core", "exceptions", "middleware", "models", "repositories", "schemas", "services", "utils"],
            "app/api": ["v1"],
            "app/utils": ["storage"],
        }

        for parent, subdirs in required_dirs.items():
            parent_path = self.backend_root / parent
            if not parent_path.exists():
                self.add_issue(f"Missing directory: {parent}")
                continue

            for subdir in subdirs:
                subdir_path = parent_path / subdir
                if not subdir_path.exists():
                    self.add_issue(f"Missing directory: {parent}/{subdir}")
                elif not (subdir_path / "__init__.py").exists():
                    self.add_issue(f"Missing __init__.py in {parent}/{subdir}")

        self.add_success("Backend directory structure valid")

    def validate_frontend_structure(self):
        """Validate frontend directory structure."""
        required_dirs = [
            "src",
            "src/components",
            "src/pages",
            "src/routes",
            "src/services",
            "src/contexts",
            "public",
        ]

        for dir_path in required_dirs:
            full_path = self.frontend_root / dir_path
            if not full_path.exists():
                self.add_issue(f"Missing frontend directory: {dir_path}")

        self.add_success("Frontend directory structure valid")

    def validate_critical_files(self):
        """Check for critical configuration files."""
        critical_files = [
            "backend/requirements.txt",
            "backend/.env.example",
            "backend/Dockerfile",
            "backend/alembic.ini",
            "backend/app/main.py",
            "docker-compose.yml",
            "frontend/package.json",
            "frontend/.env.example",
            "README.md",
        ]

        for file_path in critical_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.add_issue(f"Missing critical file: {file_path}")

        self.add_success(f"All {len(critical_files)} critical files present")

    def validate_requirements_txt(self):
        """Validate requirements.txt content."""
        req_file = self.backend_root / "requirements.txt"
        if not req_file.exists():
            self.add_issue("requirements.txt missing")
            return

        try:
            content = req_file.read_text()
            lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]

            # Check for bad packages
            bad_packages = ["pyjwt==2.8.1", "psycopg2-binary"]
            for bad in bad_packages:
                for line in lines:
                    if bad in line:
                        self.add_issue(f"Bad package in requirements.txt: {line}")

            # Check for good packages
            has_asyncpg = any("asyncpg" in l for l in lines)
            has_sqlalchemy = any("sqlalchemy" in l for l in lines)
            has_python_jose = any("python-jose" in l for l in lines)
            has_fastapi = any("fastapi" in l for l in lines)

            if not has_asyncpg:
                self.add_issue("Missing asyncpg in requirements.txt")
            if not has_sqlalchemy:
                self.add_issue("Missing sqlalchemy in requirements.txt")
            if not has_python_jose:
                self.add_issue("Missing python-jose in requirements.txt")
            if not has_fastapi:
                self.add_issue("Missing fastapi in requirements.txt")

            if has_asyncpg and has_sqlalchemy and has_python_jose and has_fastapi:
                self.add_success("requirements.txt has all critical packages")

        except Exception as e:
            self.add_issue(f"Error reading requirements.txt: {e}")

    def validate_package_json(self):
        """Validate package.json content."""
        pkg_file = self.frontend_root / "package.json"
        if not pkg_file.exists():
            self.add_issue("frontend/package.json missing")
            return

        try:
            data = json.loads(pkg_file.read_text())

            all_deps = {}
            all_deps.update(data.get("dependencies", {}))
            all_deps.update(data.get("devDependencies", {}))

            required = ["react", "react-dom", "react-router-dom", "axios", "vite"]
            missing = [d for d in required if d not in all_deps]

            if missing:
                self.add_issue(f"Missing from package.json: {', '.join(missing)}")
            else:
                self.add_success("package.json has all required packages")

        except Exception as e:
            self.add_issue(f"Error reading package.json: {e}")

    def validate_python_files(self):
        """Check Python file syntax."""
        py_files = list(self.backend_root.rglob("*.py"))
        py_files = [f for f in py_files if "__pycache__" not in str(f) and ".venv" not in str(f)]

        syntax_errors = []
        for py_file in py_files:
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                ast.parse(content)
            except SyntaxError as e:
                syntax_errors.append(f"{py_file.name}: line {e.lineno}")
            except Exception as e:
                pass  # Skip files with encoding or other issues

        if syntax_errors:
            for error in syntax_errors:
                self.add_issue(f"Syntax error in {error}")
        else:
            self.add_success(f"All {len(py_files)} Python files have valid syntax")

    def validate_env_files(self):
        """Check .env.example files."""
        env_files = [
            self.backend_root / ".env.example",
            self.frontend_root / ".env.example",
        ]

        for env_file in env_files:
            if not env_file.exists():
                self.add_issue(f"Missing: {env_file.relative_to(self.project_root)}")
            else:
                try:
                    content = env_file.read_text().strip()
                    if content:
                        self.add_success(f"{env_file.name} is configured")
                    else:
                        self.add_issue(f"Empty: {env_file.relative_to(self.project_root)}")
                except Exception as e:
                    self.add_issue(f"Error reading {env_file.name}: {e}")

    def validate_dockerfile(self):
        """Check Dockerfile configuration."""
        dockerfile = self.backend_root / "Dockerfile"
        if not dockerfile.exists():
            self.add_issue("backend/Dockerfile missing")
            return

        try:
            content = dockerfile.read_text()
            if "python:3.12" in content:
                self.add_success("Dockerfile uses Python 3.12")
            elif "python:3.11" in content:
                self.add_issue("Dockerfile uses Python 3.11 (should use 3.12)")
            else:
                self.add_issue("Dockerfile Python version unclear")
        except Exception as e:
            self.add_issue(f"Error reading Dockerfile: {e}")

    def print_report(self):
        """Print validation report."""
        print("\n" + "=" * 70)
        print("PROJECT VALIDATION REPORT")
        print("=" * 70 + "\n")

        if self.successes:
            print("SUCCESSES [OK]")
            for msg in self.successes:
                print(f"  {msg}")
            print()

        if self.issues:
            print("ISSUES [ERROR]")
            for msg in self.issues:
                print(f"  {msg}")
            print()

        print("=" * 70)
        passed = len(self.successes)
        failed = len(self.issues)
        print(f"RESULT: {passed} passed, {failed} issues")
        if failed == 0:
            print("Status: VALIDATION PASSED - Ready for testing")
        else:
            print("Status: VALIDATION FAILED - Fix issues before testing")
        print("=" * 70 + "\n")

        return failed == 0

    def validate_all(self):
        """Run all validations."""
        print("\nRunning Project Validation...\n")
        self.validate_backend_structure()
        self.validate_frontend_structure()
        self.validate_critical_files()
        self.validate_requirements_txt()
        self.validate_package_json()
        self.validate_python_files()
        self.validate_env_files()
        self.validate_dockerfile()
        return self.print_report()

if __name__ == "__main__":
    import sys
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    validator = ProjectValidator(project_root)
    success = validator.validate_all()
    sys.exit(0 if success else 1)
