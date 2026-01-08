# 🚀 Get Started with Code Review Crew

## Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd d:\1.Crew_AI_projects\code_review_crew
pip install -r requirements.txt
```

### Step 2: Set Up API Key

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   # OR
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

### Step 3: Run Your First Review

```bash
python src\code_review_crew.py examples\buggy_code.py
```

Wait 2-3 minutes while the 4 AI agents analyze the code...

### Step 4: Check the Results

Open the generated report in `output/` folder:
- `buggy_code_review_TIMESTAMP.md` - Main report
- `buggy_code_raw_TIMESTAMP.txt` - Raw output

---

## What to Expect

The report will show:
- 🐛 **~12 bugs** (division by zero, None handling, etc.)
- 🔒 **~7 security issues** (SQL injection, hardcoded secrets)
- ⚡ **~5 performance problems** (nested loops, string concatenation)
- 📝 **Documentation issues** (missing docstrings, type hints)

Each finding includes:
- Specific line numbers
- Explanation of the issue
- Suggested fix with code
- Severity level (CRITICAL/HIGH/MEDIUM/LOW)

---

## Try It On Your Own Code

```bash
python src\code_review_crew.py path\to\your\script.py
```

---

## Common Issues

### "API key not found"
- Make sure you created `.env` file (not `.env.example`)
- Check that your API key is correct

### "Module not found: crewai"
- Run: `pip install -r requirements.txt`

### "File not found"
- Use full path or navigate to the project directory first

### Takes too long
- Normal for first run (downloads models)
- Subsequent runs are faster
- Large files (>500 lines) take 3-5 minutes

---

## Next Steps

1. ✅ Test on `examples/buggy_code.py`
2. ✅ Try on your own Python files
3. ✅ Read `README.md` for full documentation
4. ✅ Read `PORTFOLIO_SUMMARY.md` for interview prep
5. ✅ Upload to GitHub (see below)

---

## Upload to GitHub

```bash
cd d:\1.Crew_AI_projects\code_review_crew
git init
git add .
git commit -m "Initial commit: AI-powered code review system"
git remote add origin https://github.com/YOUR_USERNAME/code-review-crew.git
git push -u origin main
```

Then:
- Add a good description
- Add topics: `ai`, `crewai`, `code-review`, `python`, `llm`
- Pin the repo on your profile
- Add screenshot or GIF to README

---

## Demo for Interviews

**Setup (before interview):**
1. Have project open in VS Code
2. Terminal ready in project directory
3. Example file open: `examples/buggy_code.py`

**Demo script (30 seconds):**
```
"Let me show you my AI code reviewer.

[Open buggy_code.py]
Here's a file with some bugs. Watch this:

[Run command]
python src\code_review_crew.py examples\buggy_code.py

[While it runs]
Four AI agents are analyzing this - Bug Detector, Security Analyzer,
Performance Optimizer, and Documentation Reviewer.

[Show report]
Look - it found SQL injection on line 27, hardcoded API keys,
division by zero bugs, and even suggests fixes.

Built with CrewAI and Claude. Each agent specializes in their domain."
```

---

**You're ready to go! 🎉**

Questions? Check:
- `README.md` - Full documentation
- `PORTFOLIO_SUMMARY.md` - Interview prep
- `examples/buggy_code.py` - Sample with bugs
