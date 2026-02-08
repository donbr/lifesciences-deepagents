#!/usr/bin/env python3
"""
Capture baseline screenshots of UI progressive disclosure.

This script navigates to the lifesciences deep agents UI, submits the Palovarotene/FOP
competency question, and captures screenshots as each phase executes.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import os

def capture_baseline():
    """Capture screenshots of baseline UI behavior."""

    # Create output directory
    os.makedirs('baseline-screenshots', exist_ok=True)

    with sync_playwright() as p:
        # Launch browser in headed mode to see what's happening
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to app
        print("Navigating to http://localhost:3000...")
        page.goto('http://localhost:3000')
        page.wait_for_load_state('networkidle')

        # Take initial screenshot
        page.screenshot(path='baseline-screenshots/00-initial.png', full_page=True)
        print("✓ Captured initial state")

        # Find textarea and enter query
        query = "By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?"
        print(f"\nEntering query: {query}")

        textarea = page.locator('textarea').first
        textarea.fill(query)

        # Submit (press Enter)
        textarea.press('Enter')
        print("✓ Submitted query")

        # Wait a moment for initial response
        time.sleep(2)
        page.screenshot(path='baseline-screenshots/01-query-submitted.png', full_page=True)
        print("✓ Captured query submitted state")

        # Monitor for each phase
        phases = [
            ('anchor_specialist', 'ANCHOR', '02-phase1-anchor'),
            ('enrichment_specialist', 'ENRICH', '03-phase2-enrich'),
            ('expansion_specialist', 'EXPAND', '04-phase3-expand'),
            ('traversal_drugs_specialist', 'TRAVERSE_DRUGS', '05-phase4a-drugs'),
            ('traversal_trials_specialist', 'TRAVERSE_TRIALS', '06-phase4b-trials'),
            ('validation_specialist', 'VALIDATE', '07-phase5-validate'),
            ('persistence_specialist', 'PERSIST', '08-phase6-persist'),
        ]

        for specialist_name, phase_name, filename in phases:
            try:
                print(f"\nWaiting for {phase_name} phase ({specialist_name})...")

                # Wait for phase text to appear (with generous timeout)
                page.wait_for_selector(
                    f'text=/{specialist_name}|{phase_name}/i',
                    timeout=60000  # 60 second timeout per phase
                )

                # Wait a bit for content to render
                time.sleep(2)

                # Capture screenshot
                page.screenshot(path=f'baseline-screenshots/{filename}.png', full_page=True)
                print(f"✓ Captured {phase_name} phase screenshot")

            except PlaywrightTimeout:
                print(f"⚠ Timeout waiting for {phase_name} - continuing anyway")
                page.screenshot(path=f'baseline-screenshots/{filename}-timeout.png', full_page=True)

        # Wait for final completion
        print("\nWaiting for final completion...")
        time.sleep(5)
        page.screenshot(path='baseline-screenshots/09-final-complete.png', full_page=True)
        print("✓ Captured final complete state")

        # Count completed phases
        try:
            done_elements = page.locator('text=/Done/i').all()
            print(f"\n✅ Found {len(done_elements)} completed phases")
        except:
            print("\n⚠ Could not count completed phases")

        print("\n" + "="*60)
        print("BASELINE CAPTURE COMPLETE")
        print("="*60)
        print(f"Screenshots saved to: baseline-screenshots/")
        print("\nFiles captured:")
        for f in sorted(os.listdir('baseline-screenshots')):
            print(f"  - {f}")

        browser.close()

if __name__ == '__main__':
    capture_baseline()
