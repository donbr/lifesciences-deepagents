#!/usr/bin/env python3
"""Reconnaissance script to inspect UI and find correct selectors."""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("Navigating to http://localhost:3000...")
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')

    # Take screenshot
    page.screenshot(path='inspect.png', full_page=True)
    print("✓ Screenshot saved to inspect.png")

    # Find all textareas
    textareas = page.locator('textarea').all()
    print(f"\nFound {len(textareas)} textarea elements")

    # Find all inputs
    inputs = page.locator('input').all()
    print(f"Found {len(inputs)} input elements")

    # Look for contenteditable
    contenteditable = page.locator('[contenteditable]').all()
    print(f"Found {len(contenteditable)} contenteditable elements")

    # Get page content snippet
    content = page.content()
    print(f"\nPage content length: {len(content)} characters")

    # Look for form elements
    forms = page.locator('form').all()
    print(f"Found {len(forms)} form elements")

    # Look for buttons
    buttons = page.locator('button').all()
    print(f"Found {len(buttons)} button elements")

    # Try to find input by placeholder
    placeholder_inputs = page.locator('[placeholder*="question" i], [placeholder*="ask" i], [placeholder*="query" i]').all()
    print(f"Found {len(placeholder_inputs)} inputs with question/ask/query placeholder")

    # Wait for user to inspect
    print("\nBrowser window is open - inspect the page manually")
    print("Press Ctrl+C when done")

    try:
        import time
        time.sleep(300)  # Wait 5 minutes
    except KeyboardInterrupt:
        print("\nClosing browser...")

    browser.close()
