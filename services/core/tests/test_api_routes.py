"""Integration-style tests for API infrastructure — tier enforcement, rate limiting."""
import pytest


class TestTierEnforcement:
    def test_tier_limits_structure(self):
        """Verify tier limits are defined for all plans."""
        from services.api.middleware.tier_enforcement import TIER_LIMITS
        assert "free" in TIER_LIMITS
        assert "starter" in TIER_LIMITS
        assert "growth" in TIER_LIMITS
        assert "scale" in TIER_LIMITS
        for limits in TIER_LIMITS.values():
            assert "content_per_month" in limits
            assert "videos_per_month" in limits
            assert isinstance(limits["content_per_month"], int)

    def test_starter_has_lower_limit_than_growth(self):
        from services.api.middleware.tier_enforcement import TIER_LIMITS
        assert TIER_LIMITS["starter"]["content_per_month"] < TIER_LIMITS["growth"]["content_per_month"]

    def test_scale_has_highest_limit(self):
        from services.api.middleware.tier_enforcement import TIER_LIMITS
        assert TIER_LIMITS["scale"]["content_per_month"] >= TIER_LIMITS["growth"]["content_per_month"]


class TestRateLimiter:
    def test_rate_limiter_allows_requests_under_limit(self):
        from services.core.security.rate_limiter import RateLimiter
        rl = RateLimiter()
        assert rl.is_rate_limited("user-1", max_requests=5, window_minutes=1) is False

    def test_rate_limiter_blocks_over_limit(self):
        from services.core.security.rate_limiter import RateLimiter
        rl = RateLimiter()
        for _ in range(10):
            rl.is_rate_limited("user-2", max_requests=5, window_minutes=1)
        assert rl.is_rate_limited("user-2", max_requests=5, window_minutes=1) is True

    def test_remaining_requests_decreases(self):
        from services.core.security.rate_limiter import RateLimiter
        rl = RateLimiter()
        initial = rl.get_remaining_requests("user-3", max_requests=10)
        rl.is_rate_limited("user-3", max_requests=10, window_minutes=1)
        after = rl.get_remaining_requests("user-3", max_requests=10)
        assert after < initial

    def test_clear_rate_limit(self):
        from services.core.security.rate_limiter import RateLimiter
        rl = RateLimiter()
        for _ in range(10):
            rl.is_rate_limited("user-4", max_requests=5, window_minutes=1)
        rl.clear_rate_limit("user-4")
        assert rl.is_rate_limited("user-4", max_requests=5, window_minutes=1) is False
