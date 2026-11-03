# Software Engineering Lab 6: Code and Branch Coverage Analysis

- **Student SRN:** PES1UG24CS465
- **Problem Statement:** 41 - Laundry Service
- **Repository:** SE_Lab6_Lab7_pes1ug24cs465
- **Course:** Software Engineering Lab (SE Lab 6)

---

## 1. Executive Summary

This report documents the coverage analysis, test suite design, and verification process for the **Laundry Service** application (`laundry_service.py`). The analysis compares statement (line) coverage against decision (branch) coverage, highlighting why 100% line coverage does not ensure logical completeness.

### Results Overview

| Metric | Initial Starter Suite | Code Coverage Suite (`CodeCoverageTest_*`) | Branch Coverage Suite (`BranchCoverageTest_*`) |
| :--- | :---: | :---: | :---: |
| **Statements Covered** | 14 / 37 (38%) | **37 / 37 (100%)** | **37 / 37 (100%)** |
| **Decision Branches Covered** | 8 / 26 (32%) | 26 / 26 (100%) | **26 / 26 (100%)** |
| **Tests Passed** | 2 passed | **16 passed** | **9 passed** (multi-assertion) |
| **Missing Lines** | 23 statements | **0** | **0** |
| **Partial Branches** | 6 branches | **0** | **0** |
| **Target Requirement** | >= 90% | **>= 90% (Achieved 100%)** | **>= 90% (Achieved 100%)** |

---

## 2. Theoretical Concepts: Line vs. Branch Coverage

### What is Code (Line) Coverage?
Line coverage measures the percentage of executable statements executed during test runs:
$$\text{Line Coverage} = \frac{\text{Executed Statements}}{\text{Total Statements}} \times 100\%$$

While line coverage guarantees that every line was executed at least once, it can create a false sense of security because single statements often contain multiple evaluation paths.

### What is Branch Coverage?
Branch coverage measures whether every control flow decision point (e.g., `if`, `elif`, `else`, boolean compounds) has evaluated to both `True` and `False`:
$$\text{Branch Coverage} = \frac{\text{Exercised Branches}}{\text{Total Branches}} \times 100\%$$

### Concrete Example from `laundry_service.py`

Consider line 10 in `laundry_service.py`:
```python
if is_member and garment_type != "bedding":
    included += 2
```
- **Line Coverage View:** If we test with `is_member = True` and `garment_type = "regular"`, line 11 (`included += 2`) executes. Statement coverage reports this line as **100% covered**.
- **Branch Coverage View:** Branch coverage requires testing:
  1. `is_member = True` and `garment_type != "bedding"` $\rightarrow$ **True** (allowance increased)
  2. `is_member = False` $\rightarrow$ **False** (short-circuit, no allowance)
  3. `is_member = True` and `garment_type == "bedding"` $\rightarrow$ **False** (bedding exception verified)

Without testing condition (3), a regression allowing bedding members extra weight would slip through unnoticed even with 100% line coverage.

---

## 3. Analysis of Target Module (`laundry_service.py`)

The application consists of three primary functions:

### 3.1 `extra_weight_charge(garment_type, weight_kg, speed, is_member)`
1. **Garment validation:** `garment_type not in INCLUDED_KG` raises `ValueError("unknown garment type")`.
2. **Weight validation:** `weight_kg < 0` raises `ValueError("invalid weight")`.
3. **Membership bonus:** `is_member and garment_type != "bedding"` adds $2\text{ kg}$ to included allowance.
4. **Extra weight threshold:** `extra <= 0` returns $0$ charge.
5. **Speed rate base:** `speed == "standard"` sets base rate $30$, else $50$.
6. **Heavy order surcharge:** If `extra > 10`, adds $+15$ to rate; if `speed == "express"`, adds another $+10$.
7. **Final calculation:** Returns `extra * rate`.

### 3.2 `order_acceptable(weight_kg, items, is_delicate)`
1. **Delicate items branch:** If `is_delicate` is `True`, returns `items <= 5`.
2. **Weight limit branch:** If `weight_kg > 25`, returns `False`.
3. **Item limit branch:** Returns `items <= 40`.

### 3.3 `dropoff_status(minutes_before_closing, has_bedding, is_express)`
1. **Cutoff determination:**
   - Base cutoff: $90\text{ min}$ if bedding else $60\text{ min}$.
   - Express surcharge: $+30\text{ min}$ if express.
   - Possible cutoffs: $60$, $90$, $120\text{ min}$.
2. **Status evaluation:**
   - $\ge \text{cutoff} \rightarrow \text{"accepted"}$
   - $\ge \text{cutoff} - 20 \rightarrow \text{"late"}$
   - $< \text{cutoff} - 20 \rightarrow \text{"rejected"}$

---

## 4. Phase 1: Code Coverage Analysis

### Initial Run (Starter Test Case)
- **File:** `test_laundry_service.py`
- **Output:** 2 passed
- **Coverage:** 38% line coverage (23 statements missed: 6, 8, 11, 15-23, 28, 30, 35-45)

### Targeted Test Suite Design (`CodeCoverageTest_PES1UG24CS465_application.py`)
To achieve $\ge 90\%$ code coverage, 16 targeted test cases were implemented:

| Test Name | Target Statement / Function | Outcome |
| :--- | :--- | :---: |
| `test_extra_weight_charge_within_included_weight` | Lines 13-14 (extra <= 0 return 0) | PASS |
| `test_extra_weight_charge_unknown_garment` | Line 6 (garment ValueError) | PASS |
| `test_extra_weight_charge_negative_weight` | Line 8 (weight ValueError) | PASS |
| `test_extra_weight_charge_member_allowance` | Line 11 (membership included += 2) | PASS |
| `test_extra_weight_charge_express_rate` | Line 18 (speed != 'standard' rate=50) | PASS |
| `test_extra_weight_charge_extra_above_10_standard` | Line 20 (extra > 10, rate += 15) | PASS |
| `test_extra_weight_charge_extra_above_10_express` | Line 22 (extra > 10 and express, rate += 10) | PASS |
| `test_order_acceptable_delicate_valid` | Line 28 (delicate items <= 5 -> True) | PASS |
| `test_order_acceptable_delicate_invalid` | Line 28 (delicate items > 5 -> False) | PASS |
| `test_order_acceptable_overweight` | Line 30 (weight > 25 -> False) | PASS |
| `test_order_acceptable_valid` | Line 31 (items <= 40 -> True) | PASS |
| `test_order_acceptable_too_many_items` | Line 31 (items > 40 -> False) | PASS |
| `test_dropoff_status_accepted_standard` | Lines 38, 41 (cutoff=60, accepted) | PASS |
| `test_dropoff_status_accepted_bedding_express` | Lines 36, 40 (cutoff=120, accepted) | PASS |
| `test_dropoff_status_late` | Line 43 (late status) | PASS |
| `test_dropoff_status_rejected` | Line 44 (rejected status) | PASS |

### Statement Coverage Result
- **Statements:** 37 / 37
- **Missed:** 0
- **Coverage:** **100%** (Exceeds 90% requirement)

Screenshot reference: `screenshots/code_coverage_report.png` / `code_coverage.png`

---

## 5. Phase 2: Branch Coverage Analysis

### Targeted Branch Suite Design (`BranchCoverageTest_PES1UG24CS465_application.py`)
Branch coverage requires evaluating all conditional decisions and boundaries to both `True` and `False`:

1. **Compound Decisions:**
   - Tested `is_member=True` with `garment_type="bedding"` to verify that bedding is strictly excluded from member bonus.
   - Tested `is_member=False` to verify immediate evaluation to False.
   - Tested all 3 valid garment types ("regular", "delicate", "bedding").

2. **Boundary Value Testing:**
   - `extra == 0` (boundary: zero charge)
   - `extra == 10` (boundary: exactly 10, no surcharge)
   - `extra == 11` (boundary: strictly greater than 10, surcharge applies)
   - `weight_kg == 25.0` (acceptable) vs `weight_kg == 25.1` (rejected)
   - `items == 40` (acceptable) vs `items == 41` (rejected)
   - `items == 5` (delicate acceptable) vs `items == 6` (delicate rejected)

3. **Cutoff Timing Interval Testing:**
   - All 4 cutoff permutations: $(60, 90, 90, 120)\text{ minutes}$.
   - Boundaries evaluated: $\text{cutoff}$, $\text{cutoff}-1$, $\text{cutoff}-20$, $\text{cutoff}-21$.

### Branch Coverage Result
- **Statements:** 37 / 37 (100%)
- **Branches:** 26 / 26 (100%)
- **Partial Branches:** 0
- **Branch Coverage:** **100%** (Exceeds 90% requirement)

Screenshot reference: `screenshots/branch_coverage_report.png` / `branch_coverage.png`

---

## 6. How to Reproduce

### Prerequisites
```bash
python -m pip install coverage pytest
```

### Run Code Coverage
```bash
cd "Lab 6"
python -m coverage erase
python -m coverage run -m pytest CodeCoverageTest_PES1UG24CS465_application.py
python -m coverage report -m
```

### Run Branch Coverage
```bash
cd "Lab 6"
python -m coverage erase
python -m coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS465_application.py
python -m coverage report -m
```
