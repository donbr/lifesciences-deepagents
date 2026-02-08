#!/usr/bin/env python3
"""
Simplified validation capture - just capture the UI as-is.
Manually verify assistant configuration from screenshots.
"""

from playwright.sync_api import sync_playwright
import time
import os

def main():
    output_dir = '/home/donbr/ai2026/lifesciences-deepagents/.playwright-mcp/validation-screenshots'
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Navigating to http://localhost:3000...")
        page.goto('http://localhost:3000')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(3)  # Let UI fully render

        # Capture initial state
        page.screenshot(path=f'{output_dir}/00-initial.png', full_page=True)
        print("✓ Captured initial state")
        print("⚠️  IMPORTANT: Check this screenshot to verify 'lifesciences' assistant is selected!")

        # Wait for and click textarea
        print("\n📝 Looking for message input...")
        time.sleep(2)

        # Try multiple selectors for textarea
        textarea = None
        selectors = [
            'textarea[placeholder*="message"]',
            'textarea[placeholder*="Message"]',
            'textarea',
            '[contenteditable="true"]',
        ]

        for selector in selectors:
            try:
                textarea = page.locator(selector).first
                if textarea.is_visible(timeout=2000):
                    print(f"✓ Found input using: {selector}")
                    break
            except:
                continue

        if textarea is None:
            print("❌ Could not find message input")
            page.screenshot(path=f'{output_dir}/error-no-textarea.png', full_page=True)
            browser.close()
            return

        # Submit query
        query = "By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?"
        print(f"\n📝 Submitting query: {query}")

        textarea.click()
        textarea.fill(query)
        time.sleep(1)

        # Find and click submit
        try:
            submit = page.locator('button[type="submit"]').first
            submit.click()
            print("✓ Query submitted")
        except:
            print("⚠️  Trying Enter key fallback...")
            textarea.press('Enter')

        time.sleep(2)
        page.screenshot(path=f'{output_dir}/01-query-submitted.png', full_page=True)

        # Monitor each phase
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
            print(f"\n⏳ Waiting for {phase_name} ({specialist})...")

            try:
                page.wait_for_selector(f'text=/{specialist}/i', timeout=90000)
                time.sleep(3)

                filename = f'{output_dir}/{idx:02d}-{specialist}.png'
                page.screenshot(path=filename, full_page=True)
                print(f"✓ Captured {phase_name}")

            except Exception as e:
                print(f"⚠️  Error waiting for {phase_name}: {e}")
                filename = f'{output_dir}/{idx:02d}-{specialist}-error.png'
                page.screenshot(path=filename, full_page=True)

        # Wait for completion
        print("\n⏳ Waiting for completion (no 'Running...' indicator)...")

        try:
            page.wait_for_selector('text=/Running/i', state='hidden', timeout=300000)
            print("✓ Agent completed")
        except Exception as e:
            print(f"⚠️  Timeout or error: {e}")

        time.sleep(3)
        page.screenshot(path=f'{output_dir}/99-final-complete.png', full_page=True)
        print("✓ Captured final state")

        # Check results
        try:
            done_elements = page.locator('text=/Done/i').all()
            running_elements = page.locator('text=/Running/i').all()

            print(f"\n📊 Results:")
            print(f"   ✅ Completed phases: {len(done_elements)}")
            print(f"   ⚠️  Still running: {len(running_elements)}")
        except:
            print("⚠️  Could not count completion status")

        print("\n" + "="*70)
        print("VALIDATION CAPTURE COMPLETE")
        print("="*70)
        print(f"Screenshots: {output_dir}/")
        print("\n⚠️  MANUAL VERIFICATION REQUIRED:")
        print("   1. Check 00-initial.png - is 'lifesciences' assistant selected?")
        print("   2. Check 99-final-complete.png - is 'Running...' gone?")

        browser.close()

if __name__ == '__main__':
    main()
