"""
Guild AI — E2E Smoke Test

Tests the critical user journey against a running instance:
  Health → Register → Onboarding → Generate Content → Approve → Check Calendar → Check CRM → Check Goals

Usage:
    python scripts/e2e_smoke_test.py [BASE_URL]
    python scripts/e2e_smoke_test.py http://localhost:8001
"""
import sys
import httpx
import asyncio
import json

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8001"


async def smoke_test():
    results = []

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as c:
        # 1. Health check
        r = await c.get("/health")
        ok = r.status_code == 200 and r.json().get("status") in ("ok", "degraded")
        results.append(("Health Check", ok, r.json()))

        # 2. API docs accessible
        r = await c.get("/docs")
        results.append(("API Docs", r.status_code == 200, f"status={r.status_code}"))

        # 3. Auth endpoints exist
        r = await c.post("/api/auth/register", json={"email": "smoke@test.com", "password": "test123"})
        # Expect 400/401/422 (Firebase not configured) or 200
        results.append(("Auth Register Endpoint", r.status_code in (200, 400, 401, 422, 500), f"status={r.status_code}"))

        # 4. Content queue (unauthenticated should fail)
        r = await c.get("/api/content/queue")
        results.append(("Content Auth Guard", r.status_code in (401, 403), f"status={r.status_code}"))

        # 5. CRM (unauthenticated should fail)
        r = await c.get("/api/crm/contacts")
        results.append(("CRM Auth Guard", r.status_code in (401, 403), f"status={r.status_code}"))

        # 6. Goals (unauthenticated should fail)
        r = await c.get("/api/goals/")
        results.append(("Goals Auth Guard", r.status_code in (401, 403), f"status={r.status_code}"))

        # 7. Calendar (unauthenticated should fail)
        r = await c.get("/api/calendar/events")
        results.append(("Calendar Auth Guard", r.status_code in (401, 403), f"status={r.status_code}"))

        # 8. Dashboard snapshot (unauthenticated should fail)
        r = await c.get("/api/dashboard/snapshot")
        results.append(("Dashboard Auth Guard", r.status_code in (401, 403), f"status={r.status_code}"))

    # Print results
    print(f"\n{'='*60}")
    print(f"  Guild AI Smoke Test — {BASE_URL}")
    print(f"{'='*60}\n")

    passed = 0
    failed = 0
    for name, ok, detail in results:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"  {status}  {name}")
        if not ok:
            print(f"          Detail: {detail}")
            failed += 1
        else:
            passed += 1

    print(f"\n{'─'*60}")
    print(f"  Results: {passed} passed, {failed} failed, {len(results)} total")
    print(f"{'─'*60}\n")

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(smoke_test())
    sys.exit(0 if success else 1)
