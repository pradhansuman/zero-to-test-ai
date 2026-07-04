# Interactive Test Wizard Guide

## 🎯 Overview

The **Interactive Test Wizard** is a user-friendly guide that walks you through selecting:
1. ✅ Your use case (development, CI/CD, load testing, etc.)
2. ✅ Execution environment (local, Docker, AWS, GCP, Azure)
3. ✅ Report format (HTML, JSON, JUnit, or all)
4. ✅ Browser & worker configuration
5. ✅ Confirmation & execution

**No more guessing. No more complex commands. Just answer a few questions.**

---

## 🚀 Quick Start

```bash
# Make it executable (one-time)
chmod +x scripts/interactive-test-wizard.sh

# Run the wizard
./scripts/interactive-test-wizard.sh
```

That's it! The wizard will guide you through everything.

---

## 📋 Step-by-Step Walkthrough

### Step 1: Use Case Selection

The wizard asks: **"What are you trying to do?"**

**7 Use Case Options:**

1. **👨‍💻 Local Development**
   - For developers writing/debugging tests
   - Recommended environment: LOCAL
   - Best for: Immediate feedback, fast iteration

2. **🔄 CI/CD Pipeline**
   - For automated testing in GitHub/GitLab
   - Recommended environment: DOCKER
   - Best for: Consistent, reproducible builds

3. **📊 Load Testing**
   - Scale across multiple instances
   - Recommended environment: AWS
   - Best for: Performance under load

4. **🌍 Multi-Region Testing**
   - Test across geographic regions
   - Recommended environment: AWS
   - Best for: Global coverage validation

5. **🚀 Production Deployment**
   - Pre-production validation
   - Recommended environment: AWS
   - Best for: Enterprise-grade reliability

6. **📈 Performance Testing**
   - Measure and compare metrics
   - Recommended environment: DOCKER
   - Best for: Benchmark comparisons

7. **🧪 Quick Smoke Test**
   - Quick sanity check
   - Recommended environment: LOCAL
   - Best for: Rapid validation

**Example:**
```
What are you trying to do?

1) 👨‍💻 Local Development
2) 🔄 CI/CD Pipeline
3) 📊 Load Testing
4) 🌍 Multi-Region Testing
5) 🚀 Production Deployment
6) 📈 Performance Testing
7) 🧪 Quick Smoke Test

Select your use case (1-7): 1

✅ Use Case Selected: development

📋 Development Mode Selected
   • Fast feedback loop
   • Local browser execution
   • Easy debugging
   • Recommended: LOCAL
```

---

### Step 2: Environment Selection

The wizard shows: **"Where do you want to run tests?"**

**5 Environment Options with Details:**

1. **💻 LOCAL** (Your machine)
   - Setup: 5 minutes
   - Cost: $0
   - Speed: ⭐⭐⭐⭐⭐
   - Best for: Development, quick testing

2. **🐳 DOCKER** (Containerized)
   - Setup: 2 minutes
   - Cost: $0
   - Speed: ⭐⭐⭐⭐
   - Best for: CI/CD, consistency

3. **☁️ AWS** (Amazon EC2)
   - Setup: 20 minutes
   - Cost: $0.10/run
   - Speed: ⭐⭐⭐
   - Best for: Enterprise, scaling

4. **☁️ GOOGLE CLOUD** (Google Compute)
   - Setup: 15 minutes
   - Cost: $0.08/run
   - Speed: ⭐⭐⭐
   - Best for: Google ecosystem

5. **☁️ AZURE** (Microsoft)
   - Setup: 15 minutes
   - Cost: $0.13/run
   - Speed: ⭐⭐
   - Best for: Microsoft ecosystem

**Smart Feature:** You can press Enter to accept the recommended environment for your use case!

**Example:**
```
Where do you want to run tests?

Based on your use case (development), we recommend: LOCAL

OPTIONS:

1) 💻 LOCAL (Your machine)
   • Setup: 5 minutes | Cost: $0 | Speed: ⭐⭐⭐⭐⭐
   ...

Select environment (1-5) or press Enter for recommended (local): [Enter]

✅ Environment Selected: local

💻 LOCAL EXECUTION
   • Runs on your machine
   • Requires: Node.js 20+, Playwright
   • Results stored in: ./playwright-report/
```

---

### Step 3: Report Format Selection

The wizard asks: **"What report format do you prefer?"**

**4 Format Options:**

1. **📊 HTML** (Interactive web report - DEFAULT)
   - Visual dashboards
   - Screenshots & videos
   - Timeline analysis
   - Best for: Presentations, sharing

2. **📋 JSON** (Structured data)
   - Machine-readable format
   - API-friendly
   - Detailed metrics
   - Best for: Integration, automation

3. **🔧 JUNIT** (XML format)
   - CI/CD standard
   - Jenkins compatible
   - Maven/Gradle integration
   - Best for: Enterprise CI/CD

4. **📦 ALL** (HTML + JSON + JUNIT)
   - Comprehensive output
   - Multiple use cases
   - All formats generated
   - Best for: Complete documentation

**Smart Feature:** Press Enter to default to HTML (most popular)!

**Example:**
```
What report format do you prefer?

1) 📊 HTML (Interactive web report - DEFAULT)
   • Visual dashboards
   ...

Select report format (1-4) or press Enter for HTML: [Enter]
```

---

### Step 4: Fine-Tune Settings

The wizard asks: **"Fine-tune execution settings?"**

**Configuration Options:**

1. **Browser Selection**
   - chromium (default)
   - firefox
   - webkit
   - Press Enter to keep default

2. **Worker Count** (Parallel Execution)
   - 1-16 workers available
   - Default: 4
   - Press Enter to keep default

3. **Smoke Test Mode**
   - Run SMOKE TESTS ONLY? (y/n)
   - Only executes tests tagged with @smoke
   - Perfect for quick validation

**Example:**
```
Fine-tune execution settings?

Current settings:
  • Browser: chromium
  • Parallel workers: 4

Change browser? (chromium/firefox/webkit) [Enter to skip]: [Enter]

Change worker count? (1-16) [Enter to skip]: 8

Run SMOKE TESTS ONLY? (y/n) [Default: n]: n
```

---

### Step 5: Review & Confirm

The wizard shows: **"Execution Configuration Summary"**

**Summary Display:**

```
═════════════════════════════════════════════════════════
               EXECUTION CONFIGURATION SUMMARY
═════════════════════════════════════════════════════════

Use Case:          development
Environment:       local
Report Format:     html
Browser:           chromium
Workers:           4

═════════════════════════════════════════════════════════

📊 Estimated Cost & Duration:

   • Duration: ~10-15 minutes
   • Cost: $0
   • Setup: Already done

═════════════════════════════════════════════════════════

Do you want to run tests with these settings? (y/n):
```

**You can:**
- ✅ Press 'y' to start tests immediately
- ❌ Press 'n' to cancel and start over

---

## 🎯 Real-World Examples

### Example 1: Developer's Quick Test

```bash
$ ./scripts/interactive-test-wizard.sh

Step 1: Select "1) Local Development"
Step 2: Press Enter for LOCAL (recommended)
Step 3: Press Enter for HTML (default)
Step 4: Keep defaults, no smoke test
Step 5: Confirm and run

Result: Tests run in 10-15 minutes on your machine
```

### Example 2: CI/CD Integration

```bash
$ ./scripts/interactive-test-wizard.sh

Step 1: Select "2) CI/CD Pipeline"
Step 2: Press Enter for DOCKER (recommended)
Step 3: Select "4) ALL" (comprehensive results)
Step 4: Set workers to 8, no smoke test
Step 5: Confirm and run

Result: Container-based tests with full reporting
```

### Example 3: Load Testing on AWS

```bash
$ ./scripts/interactive-test-wizard.sh

Step 1: Select "3) Load Testing"
Step 2: Press Enter for AWS (recommended)
Step 3: Select "2) JSON" (for metrics)
Step 4: Set workers to 16 (max parallelization)
Step 5: Confirm and run

Result: Scalable cloud execution with detailed metrics
```

### Example 4: Quick Smoke Test

```bash
$ ./scripts/interactive-test-wizard.sh

Step 1: Select "7) Quick Smoke Test"
Step 2: Press Enter for LOCAL (recommended)
Step 3: Press Enter for HTML (default)
Step 4: Answer 'y' to "Run SMOKE TESTS ONLY?"
Step 5: Confirm and run

Result: Smoke tests complete in 2-3 minutes
```

---

## 📊 Smart Recommendations

The wizard **automatically recommends** the best environment based on your use case:

| Use Case | Recommended | Why? |
|----------|-------------|------|
| Local Development | LOCAL | Fastest, no cost, immediate feedback |
| CI/CD Pipeline | DOCKER | Consistent, containerized, reproducible |
| Load Testing | AWS | Scalable, auto-terminating instances |
| Multi-Region | AWS | Multi-region support, geographic distribution |
| Production | AWS | Enterprise-grade, most reliable |
| Performance | DOCKER | Controlled environment, no cloud latency |
| Smoke Test | LOCAL | Fastest execution, no overhead |

---

## 💰 Cost & Duration Estimates

The wizard shows realistic estimates for each environment:

### LOCAL
```
Duration: ~10-15 minutes
Cost: $0
Setup: Already done
```

### DOCKER
```
Duration: ~12-18 minutes
Cost: $0
Setup: 2 minutes (if not built)
```

### AWS
```
Duration: ~20-30 minutes (including provisioning)
Cost: ~$0.10-$0.20 per run
Setup: Instance provisioning + initialization
```

### GOOGLE CLOUD
```
Duration: ~15-25 minutes (including provisioning)
Cost: ~$0.08-$0.15 per run
Setup: VM creation + initialization
```

### AZURE
```
Duration: ~15-25 minutes (including provisioning)
Cost: ~$0.13-$0.20 per run
Setup: VM creation + initialization
```

---

## 📂 Results & Reports

After tests complete, the wizard shows where to find results:

```
✅ TESTS COMPLETED SUCCESSFULLY!

📊 View Your Results:

📈 HTML Report:
   open ./playwright-report/index.html

📋 JSON Results:
   cat ./test-results-store/results.json

📁 All Artifacts:
   ls -la ./test-results-store/
```

---

## 🛡️ Safety Features

The wizard includes several safety mechanisms:

✅ **Input Validation**
- Validates all user inputs
- Re-prompts on invalid selections
- Range checking for workers (1-16)

✅ **Confirmation Before Execution**
- Shows complete summary
- Requires explicit confirmation
- Easy to cancel and restart

✅ **Logging**
- Records all executions
- Timestamps each run
- Saves results/failures to log file

✅ **Error Handling**
- Graceful error messages
- Never silent failures
- Clear guidance on fixes

---

## 🔧 Troubleshooting

### "Command not found"
```bash
# Make the script executable
chmod +x scripts/interactive-test-wizard.sh

# Then run it
./scripts/interactive-test-wizard.sh
```

### "Node.js not found" (when selecting LOCAL)
```bash
# Install Node.js
brew install node@20

# Verify installation
node --version
```

### "Docker not found" (when selecting DOCKER)
```bash
# Install Docker Desktop
brew install --cask docker

# Verify installation
docker --version
```

### "AWS CLI not found" (when selecting AWS)
```bash
# Install AWS CLI
brew install awscli

# Configure credentials
aws configure

# Verify installation
aws sts get-caller-identity
```

---

## 📞 Support

### Getting Help
```bash
# Run the wizard
./scripts/interactive-test-wizard.sh

# It will guide you through every step

# Or read the full documentation
cat MULTI_ENV_DEPLOYMENT.md
```

### Common Issues

1. **"Invalid choice. Please select..."**
   - You entered an invalid number
   - Select from the shown options (1-7, 1-5, etc.)

2. **"Docker image not found"**
   - Build it first: `docker build -f Dockerfile.test -t qa_agents-test:latest .`
   - Or select LOCAL instead

3. **"AWS credentials not configured"**
   - Run: `aws configure`
   - Enter your AWS Access Key ID and Secret Access Key

---

## ✨ Key Benefits

🎯 **No Complex Commands**
- Forget about command-line flags
- Just answer simple questions

🎯 **Smart Recommendations**
- Get the best environment for your use case
- But still have full control

🎯 **Cost Transparency**
- Know exactly what it will cost
- Understand the duration

🎯 **User-Friendly**
- Clear descriptions
- Progress indicators
- Helpful error messages

🎯 **Quick Results**
- Guided execution
- Automatic report generation
- Results shown immediately

---

## 🚀 Next Steps

1. **First Time?**
   - Run: `./scripts/interactive-test-wizard.sh`
   - Answer the questions
   - Watch your tests run

2. **Regular Use?**
   - Bookmark the wizard in your terminal
   - Use it for every test run
   - Enjoy consistent, guided execution

3. **CI/CD Integration?**
   - Use Docker environment
   - Select "ALL" reports
   - Archive results automatically

---

**Happy Testing with the Interactive Wizard! 🎉**

The wizard makes testing accessible to everyone, from developers to QA engineers to DevOps specialists.
