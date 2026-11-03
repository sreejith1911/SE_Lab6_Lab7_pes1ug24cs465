"""Test suite for Laundry Service Application."""

import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status
from BranchCoverageTest_PES1UG24CS465_application import *


# Example test cases from starter template:
def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True
