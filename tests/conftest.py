import re
from pathlib import Path

import pytest
from playwright.sync_api import expect

USERS = {
    'standard': ('standard_user', 'secret_sauce'),
    'locked_out': ('locked_out_user', 'secret_sauce'),
    'problem': ('problem_user', 'secret_sauce'),
    'performance': ('performance_glitch_user', 'secret_sauce'),
}


def goto_login(page, base_url: str):
    page.goto(base_url)
    expect(page).to_have_url(re.compile(r'saucedemo\.com/?$'))
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


def login(page, base_url: str, username: str, password: str = 'secret_sauce'):
    goto_login(page, base_url)
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def login_as_standard_user(page, base_url: str):
    username, password = USERS['standard']
    login(page, base_url, username, password)
    expect(page).to_have_url(re.compile(r'/inventory'))
    expect(page.locator('[data-test="title"]')).to_have_text('Products')


def add_item_to_cart(page, item_name: str):
    item = page.locator('[data-test="inventory-item"]').filter(
        has=page.get_by_role('link', name=item_name)
    )
    expect(item).to_have_count(1)
    item.locator('button').click()


def open_cart(page):
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(re.compile(r'/cart'))
    expect(page.locator('[data-test="title"]')).to_have_text('Your Cart')
