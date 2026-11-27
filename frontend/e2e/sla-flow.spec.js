import { test, expect } from '@playwright/test';

test('support agent creates a high-priority ticket and resolves it', async ({ page }) => {
  const ticketTitle = `E2E: build agent cannot connect ${Date.now()}`;

  await page.goto('/');
  await expect(page.getByRole('heading', { name: /ticket overview/i })).toBeVisible();
  await page.getByRole('button', { name: 'Create ticket', exact: true }).click();
  const dialog = page.getByRole('dialog');
  await dialog.getByLabel('Ticket title').fill(ticketTitle);
  await dialog.getByLabel('Description').fill('The build agent cannot connect to the internal service.');
  await dialog.getByLabel('Requester').fill('Taylor Quinn');
  await dialog.locator('select[name="priority"]').selectOption('High');
  await dialog.getByRole('button', { name: 'Create ticket', exact: true }).click();
  const row = page.getByRole('row').filter({ hasText: ticketTitle });
  await expect(row).toHaveCount(1);
  await expect(row).toBeVisible();
  await row.click();
  const details = page.getByRole('complementary').filter({
    has: page.getByRole('heading', { name: ticketTitle, exact: true }),
  });
  await details.getByLabel('UPDATE STATUS').selectOption('Resolved');
  await expect(row.getByText('Resolved', { exact: true })).toBeVisible();
});
