#!/usr/bin/env python3
"""
Capture baseline screenshots of UI progressive disclosure.
Servers must already be running on ports 2024 (backend) and 3000 (frontend).
"""

from playwright.sync_api import sync_playwright
import time
import os

def main():
    # Create output directory
    os.makedirs('test-screenshots', exist_ok=True)

    with sync_playwright() as p:
        # Launch browser in headless mode as per skill guidelines
        browser = p.chromium.launch(headless=False)  # Using headed to see progress
        page = browser.new_page()

        print("Navigating to http://localhost:3000...")
        page.goto('http://localhost:3000')
        page.wait_for_load_state('networkidle')  # CRITICAL per skill guidelines

        # Capture initial state
        page.screenshot(path='test-screenshots/00-initial.png', full_page=True)
        print("✓ Captured initial state")

        # Find textarea by placeholder and enter query
        query = "By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?"
        print(f"\nSubmitting query: {query}")

        # Use placeholder selector
        textarea = page.locator('textarea[placeholder*="message"]')
        textarea.wait_for(timeout=10000)
        textarea.fill(query)

        # Find and click submit button
        submit_button = page.locator('button[type="submit"]')
        submit_button.click()
        print("✓ Clicked submit button")

        # Wait for submission
        time.sleep(2)
        page.screenshot(path='test-screenshots/01-query-submitted.png', full_page=True)
        print("✓ Query submitted")

        # Monitor each phase with reconnaissance approach
        phases = [
            ('anchor_specialist', 'Phase 1: ANCHOR'),
            ('enrichment_specialist', 'Phase 2: ENRICH'),
            ('expansion_specialist', 'Phase 3: EXPAND'),
            ('traversal_drugs_specialist', 'Phase 4a: TRAVERSE_DRUGS'),
            ('traversal_trials_specialist', 'Phase 4b: TRAVERSE_TRIALS'),
            ('validation_specialist', 'Phase 5: VALIDATE'),
            ('persistence_specialist', 'Phase 6: PERSIST'),
        ]

        for idx, (specialist, phase_name) in enumerate(phases, start=2):
            print(f"\nWaiting for {phase_name} ({specialist})...")

            try:
                # Wait for specialist name to appear (case insensitive text match)
                page.wait_for_selector(f'text=/{specialist}/i', timeout=60000)

                # Wait for content to render
                time.sleep(3)

                # Capture screenshot
                filename = f'test-screenshots/{idx:02d}-{specialist}.png'
                page.screenshot(path=filename, full_page=True)
                print(f"✓ Captured {phase_name}")

            except Exception as e:
                print(f"⚠ Error waiting for {phase_name}: {e}")
                # Capture anyway
                filename = f'test-screenshots/{idx:02d}-{specialist}-error.png'
                page.screenshot(path=filename, full_page=True)

        # Final complete state
        print("\nWaiting for completion...")
        time.sleep(5)
        page.screenshot(path='test-screenshots/99-final-complete.png', full_page=True)
        print("✓ Captured final state")

        # Count completed phases
        done_elements = page.locator('text=/Done/i').all()
        print(f"\n✅ Found {len(done_elements)} completed phases")

        print("\n" + "="*70)
        print("BASELINE CAPTURE COMPLETE")
        print("="*70)
        print(f"Screenshots saved to: test-screenshots/")

        browser.close()

if __name__ == '__main__':
    main()
