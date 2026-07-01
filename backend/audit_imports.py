"""
Complete dependency audit - scans all Python files for imports.
"""
import ast
import os
from pathlib import Path
from collections import defaultdict

# Standard library modules
STDLIB = {
    'abc', 'collections', 'datetime', 'functools', 'hashlib', 'io', 'json', 'logging', 
    'os', 'pathlib', 'sys', 'time', 'typing', 'uuid', 'asyncio', 'inspect', 're',
    'tempfile', 'shutil', 'subprocess', 'base64', 'hmac', 'secrets', 'stat', 'gzip'
}

def extract_imports(file_path):
    """Extract all imports from a Python file."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split('.')[0]
                    if module not in STDLIB:
                        imports.add(module)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module.split('.')[0]
                    if module not in STDLIB:
                        imports.add(module)
    except:
        pass
    return imports

backend_path = Path("backend")
all_imports = set()

for py_file in backend_path.rglob("*.py"):
    if "__pycache__" not in str(py_file) and ".venv" not in str(py_file):
        imports = extract_imports(py_file)
        all_imports.update(imports)

print("All third-party packages used in the project:")
print("=" * 50)
for imp in sorted(all_imports):
    print(f"  {imp}")

print("\n\nPackages currently in requirements.txt:")
print("=" * 50)
with open("requirements.txt") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            pkg_name = line.split("[")[0].split("==")[0].split(">=")[0].split("<")[0].lower()
            print(f"  {pkg_name}")

print("\n\nAnalyzing coverage...")
current_packages = set()
with open("requirements.txt") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            pkg_name = line.split("[")[0].split("==")[0].split(">=")[0].split("<")[0].lower()
            current_packages.add(pkg_name)

# Map package names to their import names
package_map = {
    'python-jose': 'jose',
    'python-multipart': 'multipart',
    'python-dotenv': 'dotenv',
    'pydantic-settings': 'pydantic_settings',
    'passlib': 'passlib',
    'sqlalchemy': 'sqlalchemy',
    'asyncpg': 'asyncpg',
    'email-validator': 'email_validator',
}

missing = []
for imp in sorted(all_imports):
    imp_lower = imp.lower().replace('-', '_')
    found = False
    
    # Check direct match
    if imp_lower in current_packages:
        found = True
    # Check mapped names
    for pkg, name in package_map.items():
        pkg_lower = pkg.lower().replace('-', '_')
        if name == imp_lower or pkg_lower == imp_lower:
            found = True
            break
    # Check if it's part of a larger package
    for pkg in current_packages:
        if imp_lower.startswith(pkg.replace('-', '_')):
            found = True
            break
    
    if not found and imp not in ['starlette']:  # starlette is included in fastapi
        missing.append(imp)

if missing:
    print("\n\nMISSING PACKAGES:")
    print("=" * 50)
    for pkg in sorted(missing):
        print(f"  {pkg}")
else:
    print("\n\nAll required packages are covered!")
