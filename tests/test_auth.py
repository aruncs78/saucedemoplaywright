import re
from playwright.sync_api import expect
from conftest import USERS, goto_login, login


def test_smoke_standard_user_can_log_in_successfully(page, base_url):
    username, password = USERS['standard']
    login(page, base_url, username, password)
    expect(page).to_have_url(re.compile(r'/inventory'))
    expect(page.locator('[data-test="title"]')).to_have_text('Products')
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(6)


def test_locked_out_user_sees_access_error(page, base_url):
    username, password = USERS['locked_out']
    login(page, base_url, username, password)
    expect(page.locator('[data-test="error"]')).to_contain_text('Sorry, this user has been locked out.')
    expect(page).to_have_url(re.compile(r'saucedemo\.com/?$'))


def test_required_error_appears_for_empty_login_submission(page, base_url):
    goto_login(page, base_url)
    page.locator('[data-test="login-button"]').click()
    expect(page.locator('[data-test="error"]')).to_contain_text('Username is required')


def test_password_required_after_entering_only_username(page, base_url):
    goto_login(page, base_url)
    page.locator('[data-test="username"]').fill(USERS['standard'][0])
    page.locator('[data-test="login-button"]').click()
    expect(page.locator('[data-test="error"]')).to_contain_text('Password is required')


def test_invalid_credentials_show_matching_error_message(page, base_url):
    login(page, base_url, 'invalid_user', 'wrong_password')
    expect(page.locator('[data-test="error"]')).to_contain_text('Username and password do not match')
