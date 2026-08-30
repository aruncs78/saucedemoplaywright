# SauceDemo Playwright Test Suite

Automated end-to-end UI test suite for [SauceDemo](https://www.saucedemo.com) using **Playwright for Python** with **pytest-playwright**.

## What this repository contains

- Authentication tests
- Negative login validation tests
- Inventory and product detail tests
- Sorting checks
- Cart tests
- Checkout flow tests
- Navigation and menu tests
- A polished local HTML dashboard summarizing one sample execution
- An automatically generated screenshot evidence dashboard in CI

## Project structure

```text
.
├── dashboard/
│   └── saucedemo-test-dashboard.html
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_cart_checkout.py
│   ├── test_inventory.py
│   └── test_navigation.py
├── scripts_generate_evidence_dashboard.py
├── pytest.ini
├── requirements.txt
└── run_playwright_pytest.py
```

## Prerequisites

- Python 3.10+
- pip

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

## Run the tests

### Option 1: Simple runner

```bash
python run_playwright_pytest.py
```

### Option 2: Direct pytest command

```bash
pytest tests --browser chromium --base-url https://www.saucedemo.com
```

## Generate HTML and JSON reports

```bash
pytest tests --browser chromium --base-url https://www.saucedemo.com --html=playwright-report/index.html --self-contained-html --json-report --json-report-file=artifacts/test-results/results.json
```

## Covered scenarios

### Authentication
- Standard user login
- Locked out user validation
- Empty login submission validation
- Missing password validation
- Invalid credential validation

### Inventory
- Product list rendering
- Product details page validation
- Sorting low-to-high behavior
- Problem user inventory visibility
- Performance glitch user login/inventory access
- Cart badge state after add-to-cart

### Cart and checkout
- Add multiple items to cart
- Remove item from cart
- Checkout validation for required first name
- Successful checkout completion flow

### Navigation
- Open/close burger menu
- About link navigation
- Logout behavior
- Continue shopping navigation

## Standard test users used

- `standard_user`
- `locked_out_user`
- `problem_user`
- `performance_glitch_user`

Password for all supported users:

```text
secret_sauce
```

## Latest known sample execution

- Total tests: 19
- Passed: 19
- Failed: 0
- Pass rate: 100%

Dashboard:
- `dashboard/saucedemo-test-dashboard.html`

## CI automation

This repository is CI-ready with GitHub Actions.

Workflow file:
- `.github/workflows/playwright-python.yml`

It currently runs only by manual trigger (`workflow_dispatch`).

It automatically:
- checks out the repository
- installs Python dependencies
- installs Playwright Chromium
- runs the full test suite when manually started from GitHub Actions
- uploads HTML and JSON test artifacts
- uploads one screenshot for each successful test
- uploads an HTML screenshot evidence dashboard generated from the latest run
- retains screenshots, videos, and traces on failure

You can view and start runs in the **Actions** tab of the repository.

### Viewing screenshots for successful tests

For every successful test, the workflow uploads a screenshot artifact:
- download `playwright-success-screenshots`
- extract the zip locally
- open the generated `.png` files for each test case

### Viewing the HTML screenshot evidence dashboard

For each CI run, the workflow now also uploads:
- `playwright-evidence-dashboard`

This artifact contains an HTML file that visually presents:
- each executed test
- pass/fail outcome
- execution time
- screenshot evidence thumbnail for successful runs

To view it:
- open the completed GitHub Actions run
- download the `playwright-evidence-dashboard` artifact
- extract it locally
- open `index.html`

Note:
- keep the extracted artifact folder structure intact
- the downloaded evidence dashboard artifact now includes both `index.html` and the packaged `screenshots/` folder, so it should open correctly as-is

### Viewing screenshots, videos, and traces for failed tests

When a workflow run has failures:
- open the completed run in the **Actions** tab
- download the `playwright-failure-evidence` artifact
- extract the downloaded zip locally

Common files you may find:
- `*.png` → screenshot captured on failure
- `*.webm` → video captured for failed test execution
- `trace.zip` → Playwright trace bundle

To open a trace locally:

```bash
python -m playwright show-trace trace.zip
```

If the trace file is inside a nested folder, point the command to that exact `trace.zip` path.

## Notes

- This repository uses Playwright Python with pytest-playwright for execution.
- The included dashboard is a static report-style artifact summarizing a successful run.
- The CI-generated evidence dashboard is the best artifact for visual proof that tests were executed.
