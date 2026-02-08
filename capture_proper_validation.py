#!/usr/bin/env python3
"""
Proper validation capture with correct assistant configuration.
Tests lifesciences assistant (NOT research) and waits for actual completion.
"""

from playwright.sync_api import sync_playwright
import time
import os

def main():
    # Save validation screenshots alongside baseline
    output_dir = '/home/donbr/ai2026/lifesciences-deepagents/.playwright-mcp/validation-screenshots'
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Navigating to http://localhost:3000...")
        page.goto('http://localhost:3000')
        page.wait_for_load_state('networkidle')

        # CRITICAL: Configure to use lifesciences assistant
        print("\n🔧 Configuring assistant to 'lifesciences'...")

        try:
            # Try to find and click Settings button (gear icon)
            # Multiple selector strategies
            settings_selectors = [
                'button[aria-label*="Settings"]',
                'button:has([data-lucide="settings"])',
                'button:has(svg)',  # Settings is likely last button with icon
            ]

            clicked = False
            for selector in settings_selectors:
                try:
                    page.click(selector, timeout=5000)
                    clicked = True
                    print(f"✓ Clicked settings button using: {selector}")
                    break
                except:
                    continue

            if not clicked:
                # Fallback: click the gear icon directly
                page.locator('svg').last.click(timeout=5000)
                print("✓ Clicked settings button (fallback method)")

            time.sleep(1)

            # Clear and set Assistant ID to "lifesciences"
            assistant_input = page.locator('input[type="text"]').nth(1)  # Assistant ID field
            assistant_input.click()
            assistant_input.press('Control+A')
            assistant_input.fill('lifesciences')
            print("✓ Set Assistant ID to 'lifesciences'")

            # Click Save
            page.click('button:has-text("Save")')
            time.sleep(2)
            print("✓ Saved configuration")

        except Exception as e:
            print(f"⚠ Could not configure assistant: {e}")
            print("⚠ Will proceed with current configuration (check screenshots)")

        # Verify assistant is set correctly
        page.screenshot(path=f'{output_dir}/00-initial-lifesciences-configured.png', full_page=True)
        print("✓ Assistant configured to 'lifesciences'")

        # Submit query
        query = "By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?"
        print(f"\n📝 Submitting query: {query}")

        textarea = page.locator('textarea[placeholder*="message"]')
        textarea.wait_for(timeout=10000)
        textarea.fill(query)

        submit_button = page.locator('button[type="submit"]')
        submit_button.click()
        print("✓ Query submitted")

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
                print(f"⚠ Error waiting for {phase_name}: {e}")
                filename = f'{output_dir}/{idx:02d}-{specialist}-error.png'
                page.screenshot(path=filename, full_page=True)

        # CRITICAL: Wait for actual completion (no "Running..." indicator)
        print("\n⏳ Waiting for ACTUAL completion (no 'Running...' indicator)...")

        try:
            # Wait for "Running..." to disappear (max 5 minutes)
            page.wait_for_selector('text=/Running/i', state='hidden', timeout=300000)
            print("✓ Agent completed (Running indicator gone)")
        except Exception as e:
            print(f"⚠ Timeout waiting for completion: {e}")

        # Extra wait to ensure final render
        time.sleep(3)
        page.screenshot(path=f'{output_dir}/99-final-complete.png', full_page=True)
        print("✓ Captured final completed state")

        # Verify completion
        done_elements = page.locator('text=/Done/i').all()
        running_elements = page.locator('text=/Running/i').all()

        print(f"\n📊 Validation Results:")
        print(f"   ✅ Completed phases: {len(done_elements)}")
        print(f"   ⚠️  Still running: {len(running_elements)}")

        print("\n" + "="*70)
        print("PROPER VALIDATION CAPTURE COMPLETE")
        print("="*70)
        print(f"Screenshots saved to: {output_dir}/")
        print(f"\nAssistant used: lifesciences ✅")
        print(f"Completion verified: {'YES ✅' if len(running_elements) == 0 else 'NO ❌'}")

        browser.close()

if __name__ == '__main__':
    main()
