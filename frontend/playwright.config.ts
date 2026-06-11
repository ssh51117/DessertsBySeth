import { defineConfig, devices } from '@playwright/test'
import path from 'path'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  webServer: [
    {
      command: 'pnpm dev',
      url: 'http://localhost:3000',
      reuseExistingServer: true,
      timeout: 60000,
    },
    {
      // Starts the Django dev server when it isn't already running.
      // Requires the dessertsbyseth conda env to be active (or python on PATH).
      command: 'python manage.py runserver --noreload',
      cwd: path.join(__dirname, '../backend'),
      url: 'http://localhost:8000/products/',
      reuseExistingServer: true,
      timeout: 30000,
      env: {
        DJANGO_SETTINGS_MODULE: 'dessertsbyseth.settings',
      },
    },
  ],
})
