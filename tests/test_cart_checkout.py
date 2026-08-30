from playwright.sync_api import expect
from conftest import add_item_to_cart, login_as_standard_user, open_cart


def test_user_can_add_multiple_items_to_cart_and_see_correct_badge_count(page, base_url):
    login_as_standard_user(page, base_url)
    add_item_to_cart(page, 'Sauce Labs Backpack')
    add_item_to_cart(page, 'Sauce Labs Bike Light')
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text('2')
    open_cart(page)
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(2)


def test_user_can_remove_item_from_cart(page, base_url):
    login_as_standard_user(page, base_url)
    add_item_to_cart(page, 'Sauce Labs Backpack')
    open_cart(page)
    page.get_by_role('button', name='Remove').click()
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(0)
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_count(0)


def test_checkout_validation_requires_first_name(page, base_url):
    login_as_standard_user(page, base_url)
    add_item_to_cart(page, 'Sauce Labs Backpack')
    open_cart(page)
    page.locator('[data-test="checkout"]').click()
    page.locator('[data-test="continue"]').click()
    expect(page.locator('[data-test="error"]')).to_contain_text('First Name is required')


def test_user_can_complete_checkout_successfully(page, base_url):
    login_as_standard_user(page, base_url)
    add_item_to_cart(page, 'Sauce Labs Backpack')
    add_item_to_cart(page, 'Sauce Labs Bike Light')
    open_cart(page)
    page.locator('[data-test="checkout"]').click()
    page.locator('[data-test="firstName"]').fill('Arun')
    page.locator('[data-test="lastName"]').fill('Sane')
    page.locator('[data-test="postalCode"]').fill('10001')
    page.locator('[data-test="continue"]').click()
    expect(page.locator('[data-test="payment-info-value"]')).to_contain_text('SauceCard')
    expect(page.locator('[data-test="shipping-info-value"]')).to_contain_text('Free Pony Express Delivery')
    expect(page.locator('[data-test="total-label"]')).to_contain_text('$')
    page.locator('[data-test="finish"]').click()
    expect(page.locator('[data-test="complete-header"]')).to_have_text('Thank you for your order!')
    expect(page.locator('[data-test="back-to-products"]')).to_be_visible()
