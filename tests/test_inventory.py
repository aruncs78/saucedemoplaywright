from playwright.sync_api import expect
from conftest import USERS, add_item_to_cart, login, login_as_standard_user


def test_inventory_page_shows_all_products_with_core_details(page, base_url):
    login_as_standard_user(page, base_url)
    items = page.locator('[data-test="inventory-item"]')
    expect(items).to_have_count(6)
    for i in range(6):
        item = items.nth(i)
        expect(item.locator('[data-test="inventory-item-name"]')).to_be_visible()
        expect(item.locator('[data-test="inventory-item-price"]')).to_contain_text('$')
        expect(item.locator('img.inventory_item_img')).to_be_visible()
        expect(item.locator('button')).to_be_visible()


def test_product_details_page_displays_selected_item_information(page, base_url):
    login_as_standard_user(page, base_url)
    page.locator('[data-test="inventory-item"]').filter(
        has=page.locator('[data-test="inventory-item-name"]', has_text='Sauce Labs Backpack')
    ).locator('[data-test="inventory-item-name"]').click()
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text('Sauce Labs Backpack')
    expect(page.locator('[data-test="inventory-item-desc"]')).to_contain_text('carry.allTheThings()')
    expect(page.locator('[data-test="inventory-item-price"]')).to_have_text('$29.99')
    expect(page.locator('[data-test="back-to-products"]')).to_be_visible()


def test_sorting_changes_order_from_default_to_low_to_high(page, base_url):
    login_as_standard_user(page, base_url)
    sort = page.locator('[data-test="product-sort-container"]')
    expect(sort).to_have_value('az')
    expect(page.locator('[data-test="inventory-item-name"]').first).to_have_text('Sauce Labs Backpack')
    sort.select_option('lohi')
    expect(page.locator('[data-test="inventory-item-price"]').first).to_have_text('$7.99')
    expect(page.locator('[data-test="inventory-item-name"]').first).to_have_text('Sauce Labs Onesie')


def test_problem_user_inventory_loads_products_and_visible_images(page, base_url):
    username, password = USERS['problem']
    login(page, base_url, username, password)
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(6)
    expect(page.locator('img.inventory_item_img').first).to_be_visible()


def test_performance_glitch_user_reaches_inventory(page, base_url):
    username, password = USERS['performance']
    login(page, base_url, username, password)
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(6)


def test_cart_badge_updates_when_adding_product_from_inventory(page, base_url):
    login_as_standard_user(page, base_url)
    add_item_to_cart(page, 'Sauce Labs Backpack')
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text('1')
