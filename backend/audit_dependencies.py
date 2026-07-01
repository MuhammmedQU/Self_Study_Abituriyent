"""Dependency audit script to verify all packages."""
import json
import subprocess
import sys

packages = [
    "fastapi==0.115.6",
    "uvicorn[standard]==0.34.0",
    "sqlalchemy[asyncio]==2.0.51",
    "asyncpg==0.29.0",
    "alembic==1.14.0",
    "pydantic==2.10.4",
    "pydantic-settings==2.7.0",
    "python-multipart==0.0.20",
    "python-dotenv==1.0.0",
    "passlib[bcrypt]==1.7.4",
    "python-jose[cryptography]==3.3.0",
    "pyjwt==2.8.1",
    "slowapi==0.1.9",
    "reportlab==4.2.5",
    "qrcode==8.0",
    "pillow==11.0.0",
    "httpx==0.28.1",
    "aiofiles==23.2.1",
    "pytest==8.3.4",
    "pytest-asyncio==0.25.0",
    "faker==33.1.0",
]

print("Checking package versions on PyPI...\n")

issues = []
for pkg in packages:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "index", "versions", pkg.split("==")[0]],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    pkg_name = pkg.split("[")[0].split("==")[0]
    version = pkg.split("==")[1] if "==" in pkg else "latest"
    
    if result.returncode != 0:
        issues.append(f"⚠️  {pkg_name} - Cannot verify (pip error)")
    elif version.lower() != "latest" and version not in result.stdout:
        issues.append(f"❌ {pkg} - VERSION NOT FOUND")
    else:
        print(f"✅ {pkg}")

print("\n" + "="*60)
if issues:
    print("ISSUES FOUND:")
    for issue in issues:
        print(issue)
else:
    print("All packages verified!")
