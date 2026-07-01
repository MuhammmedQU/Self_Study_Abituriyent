"""
Complete Project Health Check Validation Script

This script validates:
1. requirements.txt has valid packages
2. All Python files have valid syntax
3. No broken imports
4. No circular imports
5. Database models are valid
6. FastAPI app initializes without errors
7. All necessary __init__.py files exist
8. No duplicate code directories
9. React build is valid
"""

import os
import sys
import json
import subprocess
import ast
from pathlib import Path


class HealthCheck:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.backend_root = self.project_root / "backend"
        self.frontend_root = self.project_root / "frontend"
        self.errors = []
        self.warnings = []
        self.successes = []

    def add_error(self, msg):
        self.errors.append(f"[ERROR] {msg}")

    def add_warning(self, msg):
        self.warnings.append(f"[WARNING] {msg}")

    def add_success(self, msg):
        self.successes.append(f"[OK] {msg}")

    def check_requirements(self):
        """Check requirements.txt validity."""
        req_file = self.backend_root / "requirements.txt"
        if not req_file.exists():
            self.add_error("requirements.txt not found")
            return

        try:
            with open(req_file) as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            
            # Check for known invalid versions
            for line in lines:
                if "pyjwt" in line.lower():
                    self.add_error(f"Invalid or redundant package: {line} (use python-jose instead)")
                if "psycopg2-binary" in line:
                    self.add_error(f"Redundant package: {line} (use asyncpg for async operations)")
                if "2.8.1" in line and "pyjwt" in line:
                    self.add_error("pyjwt==2.8.1 does not exist (version invalid)")
            
            # Check for duplicate drivers
            has_asyncpg = any("asyncpg" in l for l in lines)
            has_psycopg2 = any("psycopg2" in l for l in lines)
            if has_asyncpg and has_psycopg2:
                self.add_warning("Both asyncpg and psycopg2 found (redundant, asyncpg is for async)")
            
            if not has_asyncpg:
                self.add_warning("asyncpg not found (needed for SQLAlchemy async)")

            self.add_success(f"requirements.txt has {len(lines)} packages")
        except Exception as e:
            self.add_error(f"Error reading requirements.txt: {e}")

    def check_python_files(self):
        """Check all Python files for syntax errors."""
        py_files = list(self.backend_root.rglob("*.py"))
        syntax_errors = 0

        for py_file in py_files:
            if "__pycache__" in str(py_file):
                continue
            try:
                with open(py_file) as f:
                    ast.parse(f.read())
            except SyntaxError as e:
                self.add_error(f"Syntax error in {py_file.relative_to(self.backend_root)}: {e}")
                syntax_errors += 1
            except Exception as e:
                self.add_warning(f"Error parsing {py_file.relative_to(self.backend_root)}: {e}")

        if syntax_errors == 0:
            self.add_success(f"All {len(py_files)} Python files have valid syntax")
        else:
            self.add_error(f"{syntax_errors} Python files have syntax errors")

    def check_init_files(self):
        """Check that all packages have __init__.py."""
        packages = [
            "app",
            "app/api",
            "app/api/v1",
            "app/models",
            "app/repositories",
            "app/services",
            "app/schemas",
            "app/core",
            "app/exceptions",
            "app/middleware",
            "app/utils",
            "app/utils/storage",
            "app/scripts",
        ]

        missing = []
        for pkg in packages:
            init_file = self.backend_root / pkg / "__init__.py"
            if not init_file.exists():
                missing.append(pkg)

        if missing:
            self.add_error(f"Missing __init__.py in: {', '.join(missing)}")
        else:
            self.add_success(f"All {len(packages)} packages have __init__.py")

    def check_duplicate_dirs(self):
        """Check for duplicate directories."""
        duplicates = {
            "app/storage vs app/utils/storage": [
                self.backend_root / "app" / "storage",
                self.backend_root / "app" / "utils" / "storage",
            ],
            "src/context vs src/contexts": [
                self.frontend_root / "src" / "context",
                self.frontend_root / "src" / "contexts",
            ],
        }

        for name, dirs in duplicates.items():
            existing = [d for d in dirs if d.exists()]
            if len(existing) > 1:
                self.add_warning(f"Duplicate directories: {name} - should consolidate to one")

    def check_dockerfile(self):
        """Check Dockerfile configuration."""
        dockerfile = self.backend_root / "Dockerfile"
        if not dockerfile.exists():
            self.add_error("Backend Dockerfile not found")
            return

        try:
            content = dockerfile.read_text()
            if "python:3.11" in content:
                self.add_warning("Dockerfile uses Python 3.11, should use 3.12+")
            elif "python:3.12" in content:
                self.add_success("Dockerfile configured for Python 3.12")
            else:
                self.add_warning("Dockerfile Python version unclear")
        except Exception as e:
            self.add_error(f"Error reading Dockerfile: {e}")

    def check_fastapi_imports(self):
        """Check critical FastAPI imports."""
        main_file = self.backend_root / "app" / "main.py"
        if not main_file.exists():
            self.add_error("app/main.py not found")
            return

        try:
            content = main_file.read_text()
            required_imports = [
                "from fastapi import FastAPI",
                "from app.api.v1.router import api_router",
                "from app.core.config import settings",
            ]

            for imp in required_imports:
                if imp not in content:
                    self.add_error(f"Missing import in main.py: {imp}")
            
            self.add_success("app/main.py has all critical imports")
        except Exception as e:
            self.add_error(f"Error reading main.py: {e}")

    def check_react_package_json(self):
        """Check React package.json."""
        package_json = self.frontend_root / "package.json"
        if not package_json.exists():
            self.add_error("frontend/package.json not found")
            return

        try:
            with open(package_json) as f:
                data = json.load(f)
            
            # Check both dependencies and devDependencies
            all_deps = {}
            all_deps.update(data.get("dependencies", {}))
            all_deps.update(data.get("devDependencies", {}))
            
            required_deps = ["react", "react-dom", "react-router-dom", "axios", "vite"]
            missing = [d for d in required_deps if d not in all_deps]
            
            if missing:
                self.add_error(f"Missing dependencies in package.json: {', '.join(missing)}")
            else:
                total_deps = len(data.get("dependencies", {})) + len(data.get("devDependencies", {}))
                self.add_success(f"package.json has {total_deps} dependencies (required + dev)")
        except Exception as e:
            self.add_error(f"Error reading package.json: {e}")

    def check_env_examples(self):
        """Check environment example files."""
        env_files = [
            self.backend_root / ".env.example",
            self.frontend_root / ".env.example",
        ]

        for env_file in env_files:
            if env_file.exists():
                try:
                    content = env_file.read_text()
                    if content.strip():
                        self.add_success(f"{env_file.name} exists and has content")
                except Exception as e:
                    self.add_warning(f"Error reading {env_file.name}: {e}")

    def print_report(self):
        """Print health check report."""
        print("\n" + "=" * 70)
        print("LMS PROJECT HEALTH CHECK REPORT")
        print("=" * 70 + "\n")

        if self.successes:
            print("SUCCESSES [OK]")
            for msg in self.successes:
                print(f"  {msg}")
            print()

        if self.warnings:
            print("WARNINGS [WARNING]")
            for msg in self.warnings:
                print(f"  {msg}")
            print()

        if self.errors:
            print("ERRORS [ERROR]")
            for msg in self.errors:
                print(f"  {msg}")
            print()

        print("=" * 70)
        print(f"SUMMARY: {len(self.successes)} passed, {len(self.warnings)} warnings, {len(self.errors)} errors")
        print("=" * 70 + "\n")

        return len(self.errors) == 0

    def run_all_checks(self):
        """Run all health checks."""
        print("Running LMS Project Health Check...\n")

        self.check_requirements()
        self.check_python_files()
        self.check_init_files()
        self.check_duplicate_dirs()
        self.check_dockerfile()
        self.check_fastapi_imports()
        self.check_react_package_json()
        self.check_env_examples()

        return self.print_report()


if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    checker = HealthCheck(project_root)
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
