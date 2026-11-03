"""Code Coverage Test Suite for Laundry Service Application
SRN: PES1UG24CS465
Course: Software Engineering Lab 6 (Code and Branch Coverage Analysis)
"""

import pytest
from laundry_service import dropoff_status, extra_weight_charge, order_acceptable


# ============================================================================
# Code / Statement Coverage Tests for extra_weight_charge
# ============================================================================

def test_extra_weight_charge_within_included_weight():
    """Test charge when weight is within included allowance (extra <= 0)."""
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_extra_weight_charge_unknown_garment():
    """Test exception when garment type is unknown."""
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("leather", 5, "standard", False)


def test_extra_weight_charge_negative_weight():
    """Test exception when weight is negative."""
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -3, "standard", False)


def test_extra_weight_charge_member_allowance():
    """Test member receives extra 2 kg allowance for non-bedding."""
    # regular included: 5 + 2 = 7; weight: 8; extra: 1; rate: 30
    assert extra_weight_charge("regular", 8, "standard", True) == 30


def test_extra_weight_charge_express_rate():
    """Test express rate calculation when extra <= 10."""
    # delicate included: 3; weight: 5; extra: 2; express rate: 50
    assert extra_weight_charge("delicate", 5, "express", False) == 100


def test_extra_weight_charge_extra_above_10_standard():
    """Test extra > 10 kg with standard speed."""
    # regular included: 5; weight: 16; extra: 11; rate: 30 + 15 = 45 -> 11 * 45 = 495
    assert extra_weight_charge("regular", 16, "standard", False) == 495


def test_extra_weight_charge_extra_above_10_express():
    """Test extra > 10 kg with express speed."""
    # regular included: 5; weight: 16; extra: 11; rate: 50 + 15 + 10 = 75 -> 11 * 75 = 825
    assert extra_weight_charge("regular", 16, "express", False) == 825


# ============================================================================
# Code / Statement Coverage Tests for order_acceptable
# ============================================================================

def test_order_acceptable_delicate_valid():
    """Test delicate order within item limit (<= 5)."""
    assert order_acceptable(2, 5, True) is True


def test_order_acceptable_delicate_invalid():
    """Test delicate order exceeding item limit (> 5)."""
    assert order_acceptable(2, 6, True) is False


def test_order_acceptable_overweight():
    """Test non-delicate order exceeding max weight (> 25 kg)."""
    assert order_acceptable(28, 10, False) is False


def test_order_acceptable_valid():
    """Test valid non-delicate order within weight and item limit."""
    assert order_acceptable(10, 20, False) is True


def test_order_acceptable_too_many_items():
    """Test non-delicate order exceeding item limit (> 40)."""
    assert order_acceptable(10, 42, False) is False


# ============================================================================
# Code / Statement Coverage Tests for dropoff_status
# ============================================================================

def test_dropoff_status_accepted_standard():
    """Test accepted status for standard order without bedding."""
    # cutoff = 60; minutes = 65 -> accepted
    assert dropoff_status(65, False, False) == "accepted"


def test_dropoff_status_accepted_bedding_express():
    """Test accepted status with bedding and express cutoff."""
    # cutoff = 90 + 30 = 120; minutes = 125 -> accepted
    assert dropoff_status(125, True, True) == "accepted"


def test_dropoff_status_late():
    """Test late status when minutes between cutoff - 20 and cutoff."""
    # cutoff = 60; minutes = 45 (cutoff - 15) -> late
    assert dropoff_status(45, False, False) == "late"


def test_dropoff_status_rejected():
    """Test rejected status when minutes < cutoff - 20."""
    # cutoff = 60; minutes = 30 -> rejected
    assert dropoff_status(30, False, False) == "rejected"
