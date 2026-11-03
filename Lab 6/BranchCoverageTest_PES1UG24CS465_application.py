"""Branch and Boundary Coverage Test Suite for Laundry Service Application
SRN: PES1UG24CS465
Course: Software Engineering Lab 6 (Code and Branch Coverage Analysis)
"""

import pytest
from laundry_service import dropoff_status, extra_weight_charge, order_acceptable


# ============================================================================
# Branch & Boundary Coverage Tests: extra_weight_charge
# ============================================================================

def test_extra_weight_charge_invalid_garments():
    """Branch True for `garment_type not in INCLUDED_KG` with various invalid inputs."""
    for invalid_type in ["silk", "curtains", "UNKNOWN", ""]:
        with pytest.raises(ValueError, match="unknown garment type"):
            extra_weight_charge(invalid_type, 5, "standard", False)


def test_extra_weight_charge_negative_weights():
    """Branch True for `weight_kg < 0` with negative boundary values."""
    for invalid_weight in [-0.01, -1, -50]:
        with pytest.raises(ValueError, match="invalid weight"):
            extra_weight_charge("regular", invalid_weight, "standard", False)


def test_extra_weight_charge_zero_weight():
    """Boundary test for weight_kg = 0 (valid, non-negative, extra <= 0)."""
    assert extra_weight_charge("delicate", 0, "standard", False) == 0


def test_extra_weight_charge_exact_included_weight():
    """Boundary test where weight == included (extra == 0)."""
    # regular: included = 5; weight = 5 -> extra = 0 -> charge = 0
    assert extra_weight_charge("regular", 5, "standard", False) == 0
    # delicate: included = 3; weight = 3 -> extra = 0 -> charge = 0
    assert extra_weight_charge("delicate", 3, "standard", False) == 0
    # bedding: included = 8; weight = 8 -> extra = 0 -> charge = 0
    assert extra_weight_charge("bedding", 8, "standard", False) == 0


def test_extra_weight_charge_membership_branches():
    """Test compound decision `is_member and garment_type != 'bedding'`:
    - is_member False: condition evaluates to False
    - is_member True, garment 'regular': both True -> included + 2
    - is_member True, garment 'delicate': both True -> included + 2
    - is_member True, garment 'bedding': first True, second False -> condition False (bedding excluded)
    """
    # Non-member regular: included stays 5; weight 6 -> extra 1 * 30 = 30
    assert extra_weight_charge("regular", 6, "standard", False) == 30

    # Member regular: included becomes 5 + 2 = 7; weight 7 -> extra 0 -> 0
    assert extra_weight_charge("regular", 7, "standard", True) == 0
    # Member regular: weight 8 -> extra 1 * 30 = 30
    assert extra_weight_charge("regular", 8, "standard", True) == 30

    # Member delicate: included becomes 3 + 2 = 5; weight 5 -> extra 0 -> 0
    assert extra_weight_charge("delicate", 5, "standard", True) == 0
    # Member delicate: weight 6 -> extra 1 * 30 = 30
    assert extra_weight_charge("delicate", 6, "standard", True) == 30

    # Member bedding: included stays 8 (bedding gets no member bonus); weight 8 -> extra 0 -> 0
    assert extra_weight_charge("bedding", 8, "standard", True) == 0
    # Member bedding: weight 9 -> extra 1 * 30 = 30
    assert extra_weight_charge("bedding", 9, "standard", True) == 30


def test_extra_weight_charge_speed_rates_and_extra_boundaries():
    """Test speed rates ('standard' vs non-standard) and `extra > 10` boundary branches:
    - extra <= 10, speed standard (rate 30)
    - extra <= 10, speed express (rate 50)
    - extra exactly 10 (boundary: extra > 10 is False)
    - extra > 10, speed standard (rate 30 + 15 = 45, express False)
    - extra > 10, speed express (rate 50 + 15 + 10 = 75, express True)
    - extra > 10, non-standard non-express speed (rate 50 + 15 = 65, express False)
    """
    # extra = 2, standard -> 2 * 30 = 60
    assert extra_weight_charge("regular", 7, "standard", False) == 60

    # extra = 2, express -> 2 * 50 = 100
    assert extra_weight_charge("regular", 7, "express", False) == 100

    # Boundary: extra == 10 (weight 15, included 5) -> extra > 10 is False -> rate 30 -> 10 * 30 = 300
    assert extra_weight_charge("regular", 15, "standard", False) == 300

    # Boundary: extra == 10 with express -> rate 50 -> 10 * 50 = 500
    assert extra_weight_charge("regular", 15, "express", False) == 500

    # Boundary: extra == 11 (> 10) with standard -> rate 30 + 15 = 45 -> 11 * 45 = 495
    assert extra_weight_charge("regular", 16, "standard", False) == 495

    # Boundary: extra == 11 (> 10) with express -> rate 50 + 15 + 10 = 75 -> 11 * 75 = 825
    assert extra_weight_charge("regular", 16, "express", False) == 825

    # extra == 11 (> 10) with custom speed -> rate 50 + 15 = 65 -> 11 * 65 = 715
    assert extra_weight_charge("regular", 16, "overnight", False) == 715


# ============================================================================
# Branch & Boundary Coverage Tests: order_acceptable
# ============================================================================

def test_order_acceptable_delicate_branches():
    """Test `is_delicate` decision branches and boundaries:
    - is_delicate True, items <= 5 (boundary: items = 5 -> True; items = 4 -> True)
    - is_delicate True, items > 5 (boundary: items = 6 -> False)
    """
    assert order_acceptable(5, 5, True) is True
    assert order_acceptable(5, 4, True) is True
    assert order_acceptable(5, 6, True) is False
    assert order_acceptable(30, 5, True) is True  # weight ignored when delicate


def test_order_acceptable_weight_and_item_boundaries():
    """Test non-delicate branches and boundary conditions:
    - weight_kg > 25 (boundary: 25.0 -> continues; 25.1 -> False; 26 -> False)
    - items <= 40 (boundary: 40 -> True; 41 -> False)
    - Both limits simultaneously at boundary
    """
    # Weight exactly at upper limit (25 kg) and items at limit (40) -> True
    assert order_acceptable(25, 40, False) is True

    # Weight strictly exceeding limit (25.1 kg) -> False
    assert order_acceptable(25.1, 10, False) is False
    assert order_acceptable(26, 10, False) is False

    # Weight valid (25 kg), but items exceeding limit (41) -> False
    assert order_acceptable(25, 41, False) is False

    # Typical valid order
    assert order_acceptable(15, 25, False) is True


# ============================================================================
# Branch & Boundary Coverage Tests: dropoff_status
# ============================================================================

def test_dropoff_status_all_branch_combinations_and_boundaries():
    """Test all combinations of `has_bedding` and `is_express` cutoffs,
    and all boundary intervals for minutes_before_closing:
    
    1) has_bedding=False, is_express=False -> cutoff = 60
       - accepted: >= 60 (boundaries: 61, 60)
       - late: 40 <= minutes < 60 (boundaries: 59, 40)
       - rejected: < 40 (boundaries: 39, 0)
    
    2) has_bedding=True, is_express=False -> cutoff = 90
       - accepted: >= 90 (boundaries: 91, 90)
       - late: 70 <= minutes < 90 (boundaries: 89, 70)
       - rejected: < 70 (boundaries: 69, 10)
    
    3) has_bedding=False, is_express=True -> cutoff = 90
       - accepted: >= 90 (boundaries: 90)
       - late: 70 <= minutes < 90 (boundaries: 89, 70)
       - rejected: < 70 (boundaries: 69)
    
    4) has_bedding=True, is_express=True -> cutoff = 120
       - accepted: >= 120 (boundaries: 121, 120)
       - late: 100 <= minutes < 120 (boundaries: 119, 100)
       - rejected: < 100 (boundaries: 99, 50)
    """
    # 1) Standard (cutoff = 60)
    assert dropoff_status(61, False, False) == "accepted"
    assert dropoff_status(60, False, False) == "accepted"
    assert dropoff_status(59, False, False) == "late"
    assert dropoff_status(40, False, False) == "late"
    assert dropoff_status(39, False, False) == "rejected"
    assert dropoff_status(0, False, False) == "rejected"

    # 2) Bedding standard (cutoff = 90)
    assert dropoff_status(91, True, False) == "accepted"
    assert dropoff_status(90, True, False) == "accepted"
    assert dropoff_status(89, True, False) == "late"
    assert dropoff_status(70, True, False) == "late"
    assert dropoff_status(69, True, False) == "rejected"

    # 3) Express without bedding (cutoff = 90)
    assert dropoff_status(90, False, True) == "accepted"
    assert dropoff_status(89, False, True) == "late"
    assert dropoff_status(70, False, True) == "late"
    assert dropoff_status(69, False, True) == "rejected"

    # 4) Bedding express (cutoff = 120)
    assert dropoff_status(121, True, True) == "accepted"
    assert dropoff_status(120, True, True) == "accepted"
    assert dropoff_status(119, True, True) == "late"
    assert dropoff_status(100, True, True) == "late"
    assert dropoff_status(99, True, True) == "rejected"
