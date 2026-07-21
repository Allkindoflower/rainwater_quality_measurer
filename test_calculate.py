import pytest
from rainwater import calculate_rainwater_quality

@pytest.mark.parametrize("param1, param2, param3, expected_status", [
    # --- SAFE (Score >= 0.75) ---
    (0, 10, 2000, "Safe"),         # Math: ~0.84
    (15, 20, 3000, "Safe"),        # Math: ~0.80
    (25, 15, 1500, "Safe"),        # Math: ~0.78

    # --- REASONABLE (0.50 <= Score < 0.75) ---
    (50, 40, 1000, "Reasonable"),  # Math: ~0.67
    (75, 50, 800, "Reasonable"),   # Math: ~0.53
    (90, 30, 500, "Reasonable"),   # Math: ~0.51

    # --- DANGER ZONE (0.25 <= Score < 0.50) ---
    (110, 60, 400, "Danger Zone"), # Math: ~0.33
    (120, 50, 300, "Danger Zone"), # Math: ~0.31
    (130, 40, 200, "Danger Zone"), # Math: ~0.26

    # --- UNSAFE (0.0 <= Score < 0.25) ---
    (140, 70, 150, "Unsafe"),      # Math: ~0.18
    (150, 60, 100, "Unsafe"),      # Math: ~0.16
    (160, 50, 50, "Unsafe"),       # Math: ~0.13

    (170, 70, 150, "Unsafe"),      # Math: ~0.18
    (180, 60, 100, "Unsafe"),      # Math: ~0.16
    (190, 50, 50, "Unsafe"),       # Math: ~0.13
])
def test_calculate_rainwater_quality_ranges(param1, param2, param3, expected_status):
    result = calculate_rainwater_quality(param1, param2, param3)
    assert result == expected_status


