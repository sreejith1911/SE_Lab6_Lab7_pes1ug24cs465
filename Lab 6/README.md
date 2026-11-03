# L6_L7_41 — Laundry Service

**Student SRN:** PES1UG24CS465  
**Course:** Software Engineering Lab  
**Lab 6:** Code and Branch Coverage Analysis  

---

## Overview

This repository contains the test suites and coverage analysis for the Laundry Service application (`laundry_service.py`), fulfilling all requirements specified in the Lab 6 handout:
- Achieving **100% Code Coverage** (Requirement: $\ge 90\%$)
- Achieving **100% Branch Coverage** (Requirement: $\ge 90\%$)
- Providing terminal output analysis and screenshots
- Maintaining distinct test suites for Code Coverage and Branch Coverage

---

## Deliverables & File Mapping

| File | Description | Status |
| :--- | :--- | :---: |
| `laundry_service.py` | Source application module under test | Original |
| `CodeCoverageTest_PES1UG24CS465_application.py` | Primary test suite for statement/code coverage | **100% Line Coverage** |
| `CodeCoverageTest_laundry_service.py` | Standard named alias suite for code coverage | **100% Line Coverage** |
| `BranchCoverageTest_PES1UG24CS465_application.py` | Primary test suite for branch & boundary coverage | **100% Branch Coverage** |
| `BranchCoverageTest_laundry_service.py` | Standard named alias suite for branch coverage | **100% Branch Coverage** |
| `test_laundry_service.py` | Comprehensive test file covering all test cases | **100% Coverage** |
| `screenshots/code_coverage_report.png` | Terminal output screenshot for code coverage | $\ge 90\%$ verified |
| `screenshots/branch_coverage_report.png` | Terminal output screenshot for branch coverage | $\ge 90\%$ verified |
| `COVERAGE_ANALYSIS.md` | Comprehensive coverage analysis report | Complete |

---

## Test Execution & Verification

### 1. Run Code Coverage Suite
```bash
cd "Lab 6"
python -m coverage erase
python -m coverage run -m pytest CodeCoverageTest_PES1UG24CS465_application.py
python -m coverage report -m
```
**Output:**
```
============================= 16 passed in 0.05s ==============================
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
laundry_service.py      37      0   100%
--------------------------------------------------
TOTAL                   37      0   100%
```

### 2. Run Branch Coverage Suite
```bash
cd "Lab 6"
python -m coverage erase
python -m coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS465_application.py
python -m coverage report -m
```
**Output:**
```
============================== 9 passed in 0.04s ==============================
Name                 Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------
laundry_service.py      37      0     26      0   100%
----------------------------------------------------------------
TOTAL                   37      0     26      0   100%
```

---

## Summary of Results

| Suite | Stmts | Miss | Branch | BrPart | Coverage | Target |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Code Coverage** | 37 | 0 | - | - | **100%** | $\ge 90\%$ |
| **Branch Coverage** | 37 | 0 | 26 | 0 | **100%** | $\ge 90\%$ |
