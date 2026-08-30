import re
from playwright.sync_api import expect
from conftest import login_as_standard_user


def test_burger_menu_can_be_opened_and_closed(page, base_url):
    login_as_standard_user(page, base_url)
    page.locator('#react-burger-menu-btn').click()
    expect(page.locator('[data-test="inventory-sidebar-link"]')).to_be_visible()
    page.locator('#react-burger-cross-btn').click()
    expect(page.locator('[data-test="inventory-sidebar-link"]')).not_to_be_visible()


def test_about_link_navigates_to_sauce_labs_marketing_site(page, base_url):
    login_as_standard_user(page, base_url)
    page.locator('#react-burger-menu-btn').click()
    page.locator('[data-test="about-sidebar-link"]').click()
    expect(page).to_have_url(re.compile(r'saucelabs\.com'))


def test_logout_returns_user_to_login_page(page, base_url):
    login_as_standard_user(page, base_url)
    page.locator('#react-burger-menu-btn').click()
    page.locator('[data-test="logout-sidebar-link"]').click()
    expect(page).to_have_url(re.compile(r'saucedemo\.com/?$'))
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


def test_continue_shopping_from_cart_returns_to_inventory(page, base_url):
    login_as_standard_user(page, base_url)
    page.locator('[data-test="shopping-cart-link"]').click()
    page.locator('[data-test="continue-shopping"]').click()
    expect(page).to_have_url(re.compile(r'/inventory'))
    expect(page.locator('[data-test="title"]')).to_have_text('Products')
