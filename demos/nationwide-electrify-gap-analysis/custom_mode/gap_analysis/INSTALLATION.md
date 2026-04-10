# Gap Analysis Mode - Installation Guide

**Version:** 1.0.0  
**Last Updated:** 2026-03-03

---

## Quick Start

```bash
# 1. Install dependencies
pip install PyPDF2>=3.0.0

# 2. Copy mode to Bob's modes directory
cp -r custom_mode/gap_analysis /path/to/bob/modes/

# 3. Restart Bob
bob restart

# 4. Verify installation
bob --mode gap-analysis --version
```

---

## Detailed Installation

### Step 1: Prerequisites

#### Required Dependencies

```bash
# Core requirement
pip install PyPDF2>=3.0.0
```

#### Optional Dependencies

```bash
# For DOCX support
pip install python-docx>=0.8.11

# For advanced PDF processing
pip install docling>=1.0.0

# For OCR capabilities
pip install pytesseract>=0.3.10
pip install Pillow>=9.0.0
```

#### System Requirements

- **Python:** 3.8 or higher
- **Bob:** v2.0.0 or higher
- **OS:** macOS, Linux, Windows
- **Memory:** 512MB minimum
- **Disk Space:** 50MB

---

### Step 2: Download Mode Package

#### Option A: From Repository

```bash
git clone https://github.com/bob-ai/modes.git
cd modes/gap_analysis
```

#### Option B: From Release

```bash
wget https://github.com/bob-ai/modes/releases/download/v1.0.0/gap-analysis-mode.zip
unzip gap-analysis-mode.zip
```

#### Option C: Manual Copy

Copy the entire `custom_mode/gap_analysis` directory from this project.

---

### Step 3: Install Mode

#### Automatic Installation

```bash
# Run installation script
python install_mode.py --mode gap-analysis

# Or use Bob's CLI
bob install-mode ./gap_analysis
```

#### Manual Installation

```bash
# 1. Locate Bob's modes directory
BOB_MODES_DIR=$(bob --config-dir)/modes

# 2. Copy mode files
cp -r gap_analysis $BOB_MODES_DIR/

# 3. Set permissions
chmod -R 755 $BOB_MODES_DIR/gap_analysis

# 4. Verify structure
ls -la $BOB_MODES_DIR/gap_analysis
```

---

### Step 4: Register Mode

#### Option A: Automatic Registration

```bash
# Bob will auto-discover modes on restart
bob restart
```

#### Option B: Manual Registration

Edit Bob's configuration file (`~/.bob/config.yaml`):

```yaml
modes:
  # ... existing modes
  gap-analysis:
    enabled: true
    path: modes/gap_analysis
    config: modes/gap_analysis/config/mode_config.json
```

---

### Step 5: Verify Installation

#### Check Mode List

```bash
bob --list-modes
```

Expected output:
```
Available Modes:
  📝 Plan
  💻 Code
  🔍 Gap Analysis  ← Should appear here
  ...
```

#### Test Mode Activation

```bash
# Start Bob
bob

# Switch to mode
> switch to gap analysis mode

# Verify
> which mode am I in?
```

Expected response:
```
You are currently in Gap Analysis mode (🔍).
```

#### Run Test Analysis

```bash
# Create test file
echo "# Test Design Document" > test_design.md
echo "The system must use PostgreSQL database." >> test_design.md

# Run analysis
bob --mode gap-analysis analyze test_design.md
```

---

## Configuration

### Basic Configuration

Edit `config/mode_config.json`:

```json
{
  "settings": {
    "pdf_processing": {
      "default_method": "pypdf2"
    },
    "discrepancy_detection": {
      "confidence_threshold": 0.7
    }
  }
}
```

### Advanced Configuration

```json
{
  "settings": {
    "pdf_processing": {
      "default_method": "docling",
      "fallback_method": "pypdf2",
      "ocr_enabled": true,
      "ocr_language": "eng"
    },
    "baseline_creation": {
      "auto_categorize": true,
      "priority_scoring": true,
      "version_tracking": true,
      "categories": [
        "database",
        "security",
        "architecture",
        "cicd",
        "dependencies"
      ]
    },
    "discrepancy_detection": {
      "severity_levels": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
      "auto_categorize": true,
      "confidence_threshold": 0.7,
      "min_severity": "LOW",
      "detection_rules": {
        "database": true,
        "security": true,
        "architecture": true,
        "cicd": true,
        "dependencies": true,
        "configuration": true
      }
    },
    "reporting": {
      "default_formats": ["markdown", "json"],
      "include_recommendations": true,
      "include_traceability": true,
      "include_metrics": true,
      "include_charts": false
    },
    "remediation": {
      "prioritization_method": "severity_impact",
      "effort_estimation": true,
      "dependency_tracking": true,
      "timeline_suggestions": true
    }
  }
}
```

---

## Integration with Bob

### Mode Registration Code

If you need to manually register the mode in Bob's code:

```python
# In bob/modes/__init__.py

from .gap_analysis import GapAnalysisMode

AVAILABLE_MODES = {
    'plan': PlanMode(),
    'code': CodeMode(),
    'gap-analysis': GapAnalysisMode(),  # Add this line
    # ... other modes
}
```

### Tool Registration

```python
# In bob/tools/registry.py

from modes.gap_analysis.tools import (
    IngestDesignDocumentTool,
    CreateBaselineTool,
    ScanImplementationTool,
    DetectDiscrepanciesTool,
    GenerateGapReportTool,
    CreateRemediationPlanTool,
    TrackProgressTool
)

# Register tools
TOOL_REGISTRY = {
    # ... existing tools
    'ingest_design_document': IngestDesignDocumentTool(),
    'create_baseline': CreateBaselineTool(),
    'scan_implementation': ScanImplementationTool(),
    'detect_discrepancies': DetectDiscrepanciesTool(),
    'generate_gap_report': GenerateGapReportTool(),
    'create_remediation_plan': CreateRemediationPlanTool(),
    'track_progress': TrackProgressTool(),
}
```

---

## Troubleshooting

### Issue: Mode Not Found

**Symptoms:**
```
Error: Mode 'gap-analysis' not found
```

**Solutions:**
```bash
# 1. Check mode directory exists
ls -la ~/.bob/modes/gap_analysis

# 2. Check permissions
chmod -R 755 ~/.bob/modes/gap_analysis

# 3. Restart Bob
bob restart

# 4. Clear cache
bob clear-cache
```

### Issue: Import Errors

**Symptoms:**
```
ImportError: No module named 'PyPDF2'
```

**Solutions:**
```bash
# Install missing dependencies
pip install PyPDF2>=3.0.0

# Verify installation
python -c "import PyPDF2; print(PyPDF2.__version__)"

# Use virtual environment
python -m venv bob_env
source bob_env/bin/activate
pip install -r requirements.txt
```

### Issue: PDF Processing Fails

**Symptoms:**
```
Error: Failed to process PDF document
```

**Solutions:**
```bash
# 1. Check PDF file
file document.pdf

# 2. Try alternative method
# Edit config/mode_config.json:
"pdf_processing": {
  "default_method": "docling"  # Change from pypdf2
}

# 3. Enable OCR for scanned PDFs
pip install pytesseract
# Edit config:
"ocr_enabled": true
```

### Issue: Low Detection Accuracy

**Symptoms:**
```
Only 30% of discrepancies detected
```

**Solutions:**
```bash
# 1. Lower confidence threshold
# Edit config/mode_config.json:
"confidence_threshold": 0.5  # Lower from 0.7

# 2. Enable all detection rules
"detection_rules": {
  "database": true,
  "security": true,
  "architecture": true,
  "cicd": true,
  "dependencies": true,
  "configuration": true
}

# 3. Use semantic analysis (Phase 2)
pip install transformers
"semantic_analysis": true
```

---

## Uninstallation

### Remove Mode

```bash
# 1. Deactivate mode
bob deactivate-mode gap-analysis

# 2. Remove files
rm -rf ~/.bob/modes/gap_analysis

# 3. Clean configuration
bob config remove modes.gap-analysis

# 4. Restart Bob
bob restart
```

### Remove Dependencies

```bash
# Only if not used by other modes
pip uninstall PyPDF2 python-docx docling
```

---

## Upgrading

### From v1.0.0 to v1.1.0

```bash
# 1. Backup current configuration
cp ~/.bob/modes/gap_analysis/config/mode_config.json ~/gap_analysis_config_backup.json

# 2. Download new version
wget https://github.com/bob-ai/modes/releases/download/v1.1.0/gap-analysis-mode.zip

# 3. Extract and replace
unzip gap-analysis-mode.zip
cp -r gap_analysis ~/.bob/modes/

# 4. Restore configuration
cp ~/gap_analysis_config_backup.json ~/.bob/modes/gap_analysis/config/mode_config.json

# 5. Restart Bob
bob restart
```

---

## Docker Installation

### Using Docker

```dockerfile
FROM bob-ai/bob:latest

# Install dependencies
RUN pip install PyPDF2>=3.0.0 python-docx>=0.8.11

# Copy mode
COPY gap_analysis /app/bob/modes/gap_analysis

# Set permissions
RUN chmod -R 755 /app/bob/modes/gap_analysis

# Expose port
EXPOSE 8080

# Start Bob
CMD ["bob", "serve"]
```

### Build and Run

```bash
# Build image
docker build -t bob-gap-analysis .

# Run container
docker run -d -p 8080:8080 \
  -v $(pwd)/workspace:/workspace \
  bob-gap-analysis

# Access Bob
curl http://localhost:8080/modes
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Gap Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Bob
        run: |
          pip install bob-ai
          bob install-mode gap-analysis
      
      - name: Run Gap Analysis
        run: |
          bob --mode gap-analysis analyze \
            --design docs/design.pdf \
            --implementation ./src \
            --output gap_report.md
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: gap-analysis-report
          path: gap_report.md
```

---

## Support

### Getting Help

- **Documentation:** https://docs.bob.ai/modes/gap-analysis
- **Issues:** https://github.com/bob-ai/modes/issues
- **Discussions:** https://github.com/bob-ai/modes/discussions
- **Email:** support@bob.ai

### Reporting Bugs

```bash
# Generate diagnostic report
bob diagnose --mode gap-analysis > diagnostic.txt

# Submit issue with diagnostic report
# https://github.com/bob-ai/modes/issues/new
```

---

## Next Steps

After installation:

1. ✅ Read the [User Guide](docs/user_guide.md)
2. ✅ Try the [Examples](docs/examples.md)
3. ✅ Review the [API Reference](docs/api_reference.md)
4. ✅ Join the [Community](https://community.bob.ai)

---

**Installation Complete!** 🎉

You're ready to start using Gap Analysis mode. Try:
```
bob --mode gap-analysis
> analyze my_design.pdf