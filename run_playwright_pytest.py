import pytest

args = [
    'tests',
    '--browser', 'chromium',
    '--base-url', 'https://www.saucedemo.com',
]

raise SystemExit(pytest.main(args))
