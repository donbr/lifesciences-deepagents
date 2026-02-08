#!/usr/bin/env python3
"""
Validation capture that handles the configuration dialog.
Changes assistant from 'research' to 'lifesciences'.
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
        time.sleep(2)

        # Configuration dialog should be open
        page.screenshot(path=f'{output_dir}/00-initial-config-dialog.png', full_page=True)
        print("✓ Captured initial state (config dialog)")

        print("\n🔧 Changing Assistant ID from 'research' to 'lifesciences'...")

        try:
            # Find the Assistant ID input field by ID
            assistant_input = page.locator('#assistantId')

            # Check current value
            current_value = assistant_input.input_value()
            print(f"   Current Assistant ID: '{current_value}'")

            if current_value != 'lifesciences':
                # Clear and set to 'lifesciences'
                assistant_input.click()
                assistant_input.press('Control+A')  # Select all
                assistant_input.fill('lifesciences')
                print("✓ Changed Assistant ID to 'lifesciences'")
            else:
                print("✓ Assistant ID already set to 'lifesciences'")

            time.sleep(1)
            page.screenshot(path=f'{output_dir}/00-config-lifesciences-set.png', full_page=True)

            # Click Save button
            save_button = page.locator('button:has-text("Save")')
            save_button.click()
            print("✓ Saved configuration")

            time.sleep(2)

        except Exception as e:
            print(f"❌ Error configuring assistant: {e}")
            page.screenshot(path=f'{output_dir}/error-config.png', full_page=True)
            browser.close()
            return

        # Now the main UI should be visible
        page.screenshot(path=f'{output_dir}/00-initial.png', full_page=True)
        print("✓ Captured main UI (after config)")

        # Find message input
        print("\n📝 Submitting query...")
        query = "By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?"

        try:
            # Wait for textarea to be visible
            page.wait_for_selector('textarea', timeout=10000)
            textarea = page.locator('textarea').first
            textarea.fill(query)
            print(f"✓ Entered query: {query}")

            time.sleep(1)

            # Submit
            submit_button = page.locator('button[type="submit"]').first
            submit_button.click()
            print("✓ Submitted query")

            time.sleep(2)
            page.screenshot(path=f'{output_dir}/01-query-submitted.png', full_page=True)

        except Exception as e:
            print(f"❌ Error submitting query: {e}")
            page.screenshot(path=f'{output_dir}/error-submit.png', full_page=True)
            browser.close()
            return

        # Monitor phases
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
                print(f"⚠️  Timeout for {phase_name}: {e}")
                filename = f'{output_dir}/{idx:02d}-{specialist}-timeout.png'
                page.screenshot(path=filename, full_page=True)
                # Continue anyway - might still complete

        # Wait for completion
        print("\n⏳ Waiting for completion (no 'Running...' indicator)...")

        max_wait = 300  # 5 minutes
        waited = 0
        while waited < max_wait:
            try:
                running = page.locator('text=/Running/i').count()
                if running == 0:
                    print("✓ Agent completed (no Running indicator)")
                    break
            except:
                pass

            time.sleep(5)
            waited += 5

            if waited % 30 == 0:  # Progress update every 30 seconds
                print(f"   ... still waiting ({waited}s / {max_wait}s)")

        time.sleep(3)
        page.screenshot(path=f'{output_dir}/99-final-complete.png', full_page=True)
        print("✓ Captured final state")

        # Check results
        try:
            done_count = page.locator('text=/Done/i').count()
            running_count = page.locator('text=/Running/i').count()

            print(f"\n📊 Results:")
            print(f"   ✅ Completed phases: {done_count}")
            print(f"   ⚠️  Still running: {running_count}")

            if running_count == 0:
                print("\n✅ VALIDATION SUCCESSFUL - Agent completed!")
            else:
                print("\n⚠️  VALIDATION INCOMPLETE - Agent still running")

        except Exception as e:
            print(f"⚠️  Could not check status: {e}")

        print("\n" + "="*70)
        print("VALIDATION CAPTURE COMPLETE")
        print("="*70)
        print(f"Screenshots: {output_dir}/")
        print(f"\nAssistant used: lifesciences ✅")

        browser.close()

if __name__ == '__main__':
    main()
