import { test, expect } from '@playwright/test';

test('baseline progressive disclosure - Palovarotene FOP mechanism', async ({ page }) => {
  // Navigate to app
  await page.goto('http://localhost:3000');

  // Enter competency question
  const query = 'By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?';

  // Find and fill the textarea
  const textarea = page.locator('textarea').first();
  await textarea.fill(query);

  // Submit the query
  await page.keyboard.press('Enter');

  // Wait for first phase indicator (anchor specialist)
  console.log('Waiting for ANCHOR phase...');
  await page.waitForSelector('text=/anchor_specialist|Phase 1|ANCHOR/i', { timeout: 30000 });
  await page.screenshot({
    path: 'baseline-screenshots/phase1-anchor.png',
    fullPage: true
  });

  // Wait for enrichment phase
  console.log('Waiting for ENRICH phase...');
  await page.waitForSelector('text=/enrichment_specialist|Phase 2|ENRICH/i', { timeout: 30000 });
  await page.screenshot({
    path: 'baseline-screenshots/phase2-enrich.png',
    fullPage: true
  });

  // Wait for expansion phase
  console.log('Waiting for EXPAND phase...');
  await page.waitForSelector('text=/expansion_specialist|Phase 3|EXPAND/i', { timeout: 30000 });
  await page.screenshot({
    path: 'baseline-screenshots/phase3-expand.png',
    fullPage: true
  });

  // Wait for traversal drugs phase
  console.log('Waiting for TRAVERSE_DRUGS phase...');
  await page.waitForSelector('text=/traversal_drugs_specialist|Phase 4a|DRUGS/i', { timeout: 30000 });
  await page.screenshot({
    path: 'baseline-screenshots/phase4a-drugs.png',
    fullPage: true
  });

  // Wait for traversal trials phase
  console.log('Waiting for TRAVERSE_TRIALS phase...');
  await page.waitForSelector('text=/traversal_trials_specialist|Phase 4b|TRIALS/i', { timeout: 30000 });
  await page.screenshot({
    path: 'baseline-screenshots/phase4b-trials.png',
    fullPage: true
  });

  // Wait for validation phase
  console.log('Waiting for VALIDATE phase...');
  await page.waitForSelector('text=/validation_specialist|Phase 5|VALIDATE/i', { timeout: 30000 });
  await page.screenshot({
    path: 'baseline-screenshots/phase5-validate.png',
    fullPage: true
  });

  // Wait for persistence phase (final)
  console.log('Waiting for PERSIST phase...');
  await page.waitForSelector('text=/persistence_specialist|Phase 6|PERSIST/i', { timeout: 60000 });
  await page.screenshot({
    path: 'baseline-screenshots/phase6-persist.png',
    fullPage: true
  });

  // Wait a bit more for final response to render
  await page.waitForTimeout(3000);
  await page.screenshot({
    path: 'baseline-screenshots/final-complete.png',
    fullPage: true
  });

  // Verify we have completed phases
  const completedPhases = await page.locator('text=/Done/i').count();
  console.log(`Found ${completedPhases} completed phases`);
  expect(completedPhases).toBeGreaterThanOrEqual(6);

  console.log('✅ Baseline capture complete!');
});
