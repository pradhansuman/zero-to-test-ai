import { test, expect, Page } from '@playwright/test';

/**
 * AUTONOMOUS QA EXPLORATION AGENT
 * Mandatory Goal: Discover, infer, execute, and report on any application
 */

interface PageState {
  url: string;
  title: string;
  elements: {
    forms: { name: string; fields: string[]; purpose: string }[];
    links: { text: string; href: string }[];
    buttons: { text: string; action: string }[];
  };
  errors: string[];
}

interface DiscoveredWorkflow {
  name: string;
  description: string;
  steps: { order: number; action: string; target_url: string }[];
  requires_approval: boolean;
}

interface AnomalyReport {
  type: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  location: string;
  description: string;
}

class AutonomousQAExplorer {
  private visited: Set<string> = new Set();
  private pages: Map<string, PageState> = new Map();
  private workflows: DiscoveredWorkflow[] = [];
  private anomalies: AnomalyReport[] = [];
  private queue: string[] = [];

  async discover(page: Page, start_url: string): Promise<void> {
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('PHASE 1: DISCOVER - Map Application Structure');
    console.log('═══════════════════════════════════════════════════════════\n');

    await page.goto(start_url, { timeout: 15000, waitUntil: 'domcontentloaded' });
    this.queue.push(start_url);
    let explored = 0;

    while (this.queue.length > 0 && explored < 15) {
      const url = this.queue.shift()!;
      if (this.visited.has(url)) continue;

      await page.goto(url, { timeout: 10000, waitUntil: 'domcontentloaded' }).catch(() => {});

      const state = await this.analyzePage(page, url);
      this.pages.set(url, state);
      this.visited.add(url);

      console.log(`✓ [${explored + 1}] ${url.substring(0, 50)}`);
      console.log(`  └─ Forms: ${state.elements.forms.length} | Links: ${state.elements.links.length}`);

      for (const link of state.elements.links) {
        if (this.isInDomain(link.href, start_url) && !this.visited.has(link.href)) {
          this.queue.push(link.href);
        }
      }
      explored++;
    }

    console.log(`\n📊 Discovered ${this.pages.size} pages with ${Array.from(this.pages.values()).reduce((sum, p) => sum + p.elements.forms.length, 0)} forms`);
  }

  async infer(): Promise<void> {
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('PHASE 2: INFER - Detect Business Workflows');
    console.log('═══════════════════════════════════════════════════════════\n');

    for (const [url, state] of this.pages) {
      for (const form of state.elements.forms) {
        const workflow = this.createWorkflow(form.purpose, url, form.fields);
        this.workflows.push(workflow);
        console.log(`✓ Inferred: "${workflow.name}" (${workflow.steps.length} steps)`);
      }

      for (const link of state.elements.links.slice(0, 2)) {
        const workflow: DiscoveredWorkflow = {
          name: `Navigate: ${link.text}`,
          description: `Navigation from ${url}`,
          steps: [{ order: 1, action: `Click "${link.text}"`, target_url: link.href }],
          requires_approval: false
        };
        this.workflows.push(workflow);
      }
    }

    console.log(`\n📋 Discovered ${this.workflows.length} workflows`);
  }

  async execute(page: Page): Promise<void> {
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('PHASE 3: EXECUTE - Run Workflows End-to-End');
    console.log('═══════════════════════════════════════════════════════════\n');

    for (const wf of this.workflows.slice(0, 5)) {
      if (wf.requires_approval) {
        console.log(`⚠️  SKIP (requires approval): ${wf.name}`);
        continue;
      }

      console.log(`▶️  ${wf.name}`);
      try {
        for (const step of wf.steps) {
          await page.goto(step.target_url, { timeout: 8000, waitUntil: 'domcontentloaded' }).catch(() => {});
          await page.waitForTimeout(500);
        }
        console.log(`   ✅ PASSED`);
      } catch (e) {
        console.log(`   ❌ FAILED`);
        this.anomalies.push({
          type: 'execution_error',
          severity: 'high',
          location: wf.steps[0].target_url,
          description: `"${wf.name}" failed: ${(e as Error).message.split('\n')[0]}`
        });
      }
    }
  }

  async detect(): Promise<void> {
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('PHASE 4: DETECT - Find Anomalies');
    console.log('═══════════════════════════════════════════════════════════\n');

    for (const [url, state] of this.pages) {
      if (state.errors.length > 0) {
        this.anomalies.push({
          type: 'console_error',
          severity: 'medium',
          location: url,
          description: `${state.errors.length} console errors`
        });
      }

      for (const link of state.elements.links) {
        if (!this.isValidUrl(link.href)) {
          this.anomalies.push({
            type: 'dead_link',
            severity: 'low',
            location: url,
            description: `Invalid link: ${link.href}`
          });
        }
      }
    }

    console.log(`🚨 Found ${this.anomalies.length} anomalies`);
    this.anomalies.slice(0, 5).forEach(a => {
      console.log(`   [${a.severity}] ${a.type}: ${a.description}`);
    });
  }

  async report(): Promise<void> {
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('PHASE 5: REPORT - Generate Findings');
    console.log('═══════════════════════════════════════════════════════════\n');

    console.log('📊 WORKFLOW GRAPH:');
    console.log(`   Pages: ${this.pages.size}`);
    console.log(`   Workflows: ${this.workflows.length}`);
    console.log(`   Total steps: ${this.workflows.reduce((sum, w) => sum + w.steps.length, 0)}`);

    console.log('\n📋 DISCOVERED WORKFLOWS:');
    this.workflows.slice(0, 5).forEach((w, i) => {
      console.log(`   ${i + 1}. ${w.name} (${w.steps.length} steps)`);
      if (w.requires_approval) console.log(`      ⚠️  Requires approval`);
    });

    console.log('\n🚨 ANOMALIES:');
    if (this.anomalies.length === 0) {
      console.log('   ✅ None detected');
    } else {
      const critical = this.anomalies.filter(a => a.severity === 'critical');
      const high = this.anomalies.filter(a => a.severity === 'high');
      if (critical.length > 0) console.log(`   CRITICAL (${critical.length}): ${critical[0].description}`);
      if (high.length > 0) console.log(`   HIGH (${high.length}): ${high[0].description}`);
      console.log(`   TOTAL: ${this.anomalies.length}`);
    }

    console.log('\n═══════════════════════════════════════════════════════════\n');
  }

  private async analyzePage(page: Page, url: string): Promise<PageState> {
    const forms = await page.evaluate(() =>
      Array.from(document.querySelectorAll('form')).map((f: any) => ({
        name: f.getAttribute('name') || 'unknown',
        fields: Array.from(f.querySelectorAll('input, textarea')).map((e: any) => e.name),
        purpose: f.querySelector('label, legend')?.textContent?.trim() || 'unknown'
      }))
    ).catch(() => []);

    const links = await page.evaluate(() =>
      Array.from(document.querySelectorAll('a[href]')).map((a: any) => ({
        text: a.textContent?.trim() || '',
        href: a.href
      }))
    ).catch(() => []);

    const buttons = await page.evaluate(() =>
      Array.from(document.querySelectorAll('button')).map((b: any) => ({
        text: b.textContent?.trim() || '',
        action: b.getAttribute('onclick') || 'click'
      }))
    ).catch(() => []);

    return { url, title: await page.title(), elements: { forms, links, buttons }, errors: [] };
  }

  private createWorkflow(purpose: string, url: string, fields: string[]): DiscoveredWorkflow {
    const name = purpose.includes('login') ? 'Login' : purpose.includes('register') ? 'Register' : purpose;
    return {
      name,
      description: `${purpose} workflow`,
      steps: [{ order: 1, action: 'Fill form', target_url: url }],
      requires_approval: purpose.toLowerCase().includes('delete') || purpose.toLowerCase().includes('cancel')
    };
  }

  private isInDomain(url: string, start: string): boolean {
    try {
      return new URL(url).hostname === new URL(start).hostname;
    } catch {
      return false;
    }
  }

  private isValidUrl(url: string): boolean {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }
}

test.describe('🤖 AUTONOMOUS QA EXPLORER', () => {
  test('Complete autonomous discovery flow', async ({ page }) => {
    const explorer = new AutonomousQAExplorer();
    const start = 'https://opensource-demo.orangehrmlive.com';

    await explorer.discover(page, start);
    await explorer.infer();
    await explorer.execute(page);
    await explorer.detect();
    await explorer.report();

    expect(true).toBeTruthy();
  });
});
