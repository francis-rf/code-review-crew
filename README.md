# 🤖 Code Review Crew

**AI-Powered Multi-Agent Code Review System**

An intelligent code analysis tool powered by 4 specialized AI agents that collaboratively review Python code for bugs, security vulnerabilities, performance issues, and documentation quality.

---

## 🎯 Features

### Four Specialized AI Agents

1. **🐛 Bug Detector Agent**
   - Identifies logical errors and edge cases
   - Detects exception handling issues
   - Finds resource leaks and None-handling problems
   - Catches off-by-one errors and type mismatches

2. **🔒 Security Analyzer Agent**
   - Scans for OWASP Top 10 vulnerabilities
   - Detects SQL/Command injection risks
   - Identifies hardcoded secrets and weak cryptography
   - Flags insecure file operations

3. **⚡ Performance Analyzer Agent**
   - Analyzes algorithmic complexity (Big O)
   - Identifies inefficient loops and data structures
   - Detects redundant computations
   - Suggests memory optimizations

4. **📝 Documentation Analyzer Agent**
   - Reviews docstring coverage
   - Checks type hints
   - Evaluates code clarity and naming
   - Generates comprehensive final report

---

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to project
cd code_review_crew

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="your-api-key-here"
# OR
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Basic Usage

```bash
# Review a Python file
python src/code_review_crew.py examples/buggy_code.py

# Specify custom output directory
python src/code_review_crew.py my_script.py --output reports/

# Get help
python src/code_review_crew.py --help
```

### Python API

```python
from src.code_review_crew import CodeReviewCrew

# Initialize crew
crew = CodeReviewCrew(code_file_path="examples/buggy_code.py")

# Run review
result = crew.run()

# Result is saved to output/ directory
```

---

## 📊 Sample Output

```markdown
# Code Review Report

**File**: buggy_code.py
**Date**: 2025-01-07
**Overall Score**: 42/100

## Executive Summary

### Key Findings
- 🐛 **Bugs**: 12 issues found (3 critical)
- 🔒 **Security**: 7 vulnerabilities (4 critical)
- ⚡ **Performance**: 5 bottlenecks identified
- 📝 **Documentation**: 35% coverage

### Risk Assessment
**Overall Risk Level**: CRITICAL

### Critical Actions Required
1. [IMMEDIATE] Fix SQL injection (Line 27)
2. [IMMEDIATE] Handle division by zero (Line 19)
3. [IMMEDIATE] Remove hardcoded API key (Line 12)

---

## 🐛 Bug Detection Results

### [CRITICAL] Division by Zero Risk (Line 19)

**Issue**: Variable `ages` used as divisor without validation

**Current Code**:
```python
19: average = total / len(ages)
```

**Suggested Fix**:
```python
if len(ages) > 0:
    average = total / len(ages)
else:
    raise ValueError("Cannot calculate average of empty list")
```

...
```

---

## 📁 Project Structure

```
code_review_crew/
├── src/
│   ├── code_review_crew.py    # Main crew implementation
│   ├── config/
│   │   ├── agents.yaml         # Agent configurations
│   │   └── tasks.yaml          # Task definitions
│   └── tools/                  # Custom tools (future)
├── examples/
│   └── buggy_code.py           # Example file with intentional bugs
├── output/                     # Generated reports
├── tests/                      # Unit tests (future)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔧 Configuration

### Agent Configuration (`src/config/agents.yaml`)

Customize agent behaviors, roles, and backstories.

```yaml
bug_detector_agent:
  role: "Senior Bug Detective & Logic Analyzer"
  goal: "Identify logical errors and edge cases..."
  backstory: "You are a veteran software engineer..."
  verbose: true
  memory: true
```

### Task Configuration (`src/config/tasks.yaml`)

Define analysis tasks and expected outputs.

```yaml
bug_detection_task:
  description: "Analyze the Python code file for bugs..."
  expected_output: "A comprehensive bug detection report..."
  agent: bug_detector_agent
```

---

## 📈 Use Cases

### 1. Pre-Commit Code Review
```bash
# Add to pre-commit hook
python src/code_review_crew.py $(git diff --name-only --cached | grep .py$)
```

### 2. CI/CD Integration
```yaml
# .github/workflows/code-review.yml
- name: AI Code Review
  run: |
    python src/code_review_crew.py src/**/*.py --output reports/
```

### 3. Learning Tool
```bash
# Review your own code to learn best practices
python src/code_review_crew.py my_learning_project.py
```

### 4. Legacy Code Assessment
```bash
# Assess technical debt in old codebases
python src/code_review_crew.py legacy_system.py
```

---

## 🎓 What This Project Demonstrates

**For Portfolio/Interviews:**

✅ **AI Agent Orchestration** - Multi-agent collaboration with CrewAI
✅ **LLM Application Development** - Practical use of language models
✅ **Software Engineering** - Clean code architecture, error handling
✅ **Security Awareness** - OWASP Top 10, secure coding practices
✅ **Performance Optimization** - Algorithm complexity analysis
✅ **Production Readiness** - CLI interface, configuration management

**Technical Skills Shown:**
- Python best practices
- YAML configuration
- Static code analysis concepts
- Report generation
- File I/O and path handling
- Exception handling
- Type hints and documentation

---

## 🧪 Testing

### Run on Example File
```bash
python src/code_review_crew.py examples/buggy_code.py
```

Expected: Report with ~25 issues found across all categories.

### Create Your Own Test File
```python
# test_me.py
def divide(a, b):
    return a / b  # Missing zero check!

result = divide(10, 0)  # Boom!
```

```bash
python src/code_review_crew.py test_me.py
```

---

## 📝 Requirements

- Python 3.8+
- OpenAI API key OR Anthropic API key
- Internet connection (for LLM API calls)

See `requirements.txt` for full dependencies.

---

## 🚧 Limitations & Future Enhancements

### Current Limitations
- Only supports Python files
- Requires LLM API (costs money)
- Analysis time depends on file size (1-5 minutes)
- English-only reports

### Planned Features
- [ ] Support for JavaScript, TypeScript, Go, Java
- [ ] PDF report generation
- [ ] Integration with GitHub Actions
- [ ] Custom rule definitions
- [ ] Batch file processing
- [ ] Diff-based analysis (only review changes)
- [ ] VS Code extension
- [ ] Local LLM support (Ollama)

---

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

1. Test the tool on your code
2. Open issues for bugs found
3. Suggest new features
4. Share interesting use cases

---

## 📄 License

MIT License - Feel free to use this project for learning and portfolio purposes.

---

## 👤 Author

**Your Name**
AI Engineer | Python Developer | LLM Enthusiast

- Portfolio: [your-portfolio.com]
- LinkedIn: [linkedin.com/in/yourprofile]
- GitHub: [github.com/yourusername]

---

## 🙏 Acknowledgments

- **CrewAI** - Multi-agent framework
- **Anthropic/OpenAI** - LLM providers
- **OWASP** - Security guidelines
- **Python Community** - Best practices and patterns

---

## 📞 Support

Having issues? Want to discuss the project?

1. Check `examples/buggy_code.py` for expected behavior
2. Verify your API key is set correctly
3. Ensure Python 3.8+ is installed
4. Check `output/` for generated reports

---

## 🎯 Interview Talking Points

**"Tell me about a project you built":**

> "I built an AI-powered code review system using multi-agent orchestration. Four specialized AI agents collaborate to analyze Python code for bugs, security vulnerabilities, performance issues, and documentation quality.
>
> The system uses CrewAI for agent coordination and LLMs for analysis. Each agent is an expert in their domain - bugs, security, performance, or documentation.
>
> **Tech stack**: Python, CrewAI, LangChain, OpenAI/Anthropic APIs
>
> **Key challenges solved**:
> - Designing agent roles that don't overlap
> - Passing context between agents
> - Generating actionable, specific recommendations
> - Creating a clean CLI interface
>
> **Business value**: Catches bugs before code review, teaches best practices, identifies security risks early."

---

**Built with ❤️ and 🤖 AI**
