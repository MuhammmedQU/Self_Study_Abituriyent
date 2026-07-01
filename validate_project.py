"""
Advanced Project Validation Script

Tests:
1. FastAPI app initialization
2. Database configuration
3. All service imports
4. All repository imports
5. All model imports
6. Middleware and exception handlers
7. API router configuration
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_fastapi_app():
    """Test FastAPI app initialization."""
    try:
        from app.main import app
        assert app is not None
        assert app.title == "LMS API"
        print("[OK] FastAPI app initializes successfully")
        return True
    except Exception as e:
        print(f"[ERROR] FastAPI app initialization failed: {e}")
        return False

def test_database_config():
    """Test database configuration."""
    try:
        from app.core.config import settings
        assert settings.database_url
        assert "postgresql+asyncpg" in settings.database_url
        print(f"[OK] Database config valid: {settings.database_url[:50]}...")
        return True
    except Exception as e:
        print(f"[ERROR] Database config failed: {e}")
        return False

def test_models():
    """Test all model imports."""
    models = [
        "user", "refresh_token", "course", "module", "lesson",
        "resource", "quiz", "question", "option", "quiz_attempt",
        "progress", "certificate", "notification", "announcement",
        "activity_log"
    ]
    
    failed = []
    for model in models:
        try:
            __import__(f"app.models.{model}")
        except Exception as e:
            failed.append(f"{model}: {e}")
    
    if failed:
        for error in failed:
            print(f"[ERROR] Model import failed: {error}")
        return False
    else:
        print(f"[OK] All {len(models)} models import successfully")
        return True

def test_repositories():
    """Test all repository imports."""
    repos = [
        "base", "user", "refresh_token", "course", "module", "lesson",
        "resource", "quiz", "question", "option", "quiz_attempt",
        "progress", "certificate", "notification", "announcement",
        "activity_log"
    ]
    
    failed = []
    for repo in repos:
        try:
            __import__(f"app.repositories.{repo}")
        except Exception as e:
            failed.append(f"{repo}: {e}")
    
    if failed:
        for error in failed:
            print(f"[ERROR] Repository import failed: {error}")
        return False
    else:
        print(f"[OK] All {len(repos)} repositories import successfully")
        return True

def test_services():
    """Test all service imports."""
    services = [
        "auth_service", "admin_service", "student_service", 
        "quiz_service", "progress_service", "certificate_service"
    ]
    
    failed = []
    for service in services:
        try:
            __import__(f"app.services.{service}")
        except Exception as e:
            failed.append(f"{service}: {e}")
    
    if failed:
        for error in failed:
            print(f"[ERROR] Service import failed: {error}")
        return False
    else:
        print(f"[OK] All {len(services)} services import successfully")
        return True

def test_api_routers():
    """Test API router imports."""
    try:
        from app.api.v1.router import api_router
        assert api_router is not None
        print("[OK] API routers initialized successfully")
        return True
    except Exception as e:
        print(f"[ERROR] API router initialization failed: {e}")
        return False

def test_middleware_exception_handlers():
    """Test middleware and exception handlers."""
    try:
        from app.middleware.logging import request_logging_middleware
        from app.exceptions.handlers import register_exception_handlers
        assert request_logging_middleware is not None
        assert register_exception_handlers is not None
        print("[OK] Middleware and exception handlers import successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Middleware/exception handlers failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("\n" + "=" * 70)
    print("ADVANCED PROJECT VALIDATION")
    print("=" * 70 + "\n")
    
    tests = [
        ("FastAPI App", test_fastapi_app),
        ("Database Config", test_database_config),
        ("Models", test_models),
        ("Repositories", test_repositories),
        ("Services", test_services),
        ("API Routers", test_api_routers),
        ("Middleware/Handlers", test_middleware_exception_handlers),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"[ERROR] {name} test crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")
    
    print("\n" + "=" * 70)
    print(f"RESULT: {passed}/{total} tests passed")
    if passed == total:
        print("Status: READY FOR DEPLOYMENT")
    else:
        print("Status: NEEDS FIXES")
    print("=" * 70 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
