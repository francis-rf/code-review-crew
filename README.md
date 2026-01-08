# Code Review Crew

Multi-agent code review system I built to catch bugs and security issues before they hit production.

I wanted to see if I could get AI agents to work together on a real problem - turns out they're pretty good at finding things I miss when reviewing my own code.

---

## How It Works

I set up 4 different agents, each focused on a specific aspect of code review:

**Bug Detector** - Looks for logical errors, edge cases, exception handling issues. Basically catches the stuff that would blow up in production at 2am.

**Security Analyzer** - Scans for common vulnerabilities (SQL injection, hardcoded secrets, etc.). I based this on OWASP guidelines since that's what most companies care about.

**Performance Analyzer** - Checks algorithmic complexity and inefficient patterns. Won't catch everything a profiler would, but finds obvious bottlenecks.

**Documentation Analyzer** - Reviews docstrings and type hints, then puts together the final report. I gave this one the summarizer role since it sees all the other findings.

---

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# You'll need an API key from OpenAI or Anthropic
export OPENAI_API_KEY="your-key-here"

# Run it on any Python file
python src/code_review_crew.py examples/buggy_code.py
```

You can also use it in your own Python code:

```python
from src.code_review_crew import CodeReviewCrew

crew = CodeReviewCrew(code_file_path="my_script.py")
result = crew.run()
# Check the output/ folder for your report
```

---

## What the Reports Look Like

When you run it, you get a markdown report that breaks down everything:

- Overall risk score
- Specific issues grouped by severity (critical, high, medium)
- Line numbers where problems are
- Suggested fixes with code examples

For example, it caught a division by zero bug I had where I forgot to check if a list was empty before calculating the average. Gave me the exact fix too.

The agents also summarize the findings at the top, so you know immediately if there's something critical to fix.

---

## Project Structure

```
code_review_crew/
├── src/
│   ├── code_review_crew.py    # Main orchestration logic
│   ├── config/
│   │   ├── agents.yaml         # Where I defined each agent's role
│   │   └── tasks.yaml          # What each agent is supposed to do
├── examples/
│   └── buggy_code.py           # Test file with intentional bugs
├── output/                     # Reports get saved here
└── requirements.txt
```

---

## Configuration

All the agent behavior is defined in YAML files:

**agents.yaml** - Each agent's role, goals, and "personality". I spent some time tuning these to make sure they don't overlap.

**tasks.yaml** - What each agent analyzes and what format they should output.

You can tweak these if you want different focus areas or reporting styles.

---

## Ways I've Used This

**Learning** - I run it on my old code to see what I missed. It's humbling but helpful.

**Pre-commit checks** - Sometimes I'll run it before pushing code to catch obvious issues.

**Legacy code** - Helped me assess some old scripts I inherited. Found several SQL injection risks I didn't notice on first read.

You could probably integrate this into CI/CD, but keep in mind the API calls cost money and take time (couple minutes per file).

---

## What I Learned Building This

This project taught me a lot about working with AI agents:

- How to coordinate multiple LLM agents without them stepping on each other
- Designing prompts that give consistent, useful output
- Managing context between agents (they need to pass info to each other)
- The tradeoffs between agent autonomy and control

Also got deeper into:
- CrewAI framework
- YAML-based configuration
- Building CLI tools that people might actually use
- OWASP security patterns

---

## Testing

I included `examples/buggy_code.py` which has intentional bugs. Run the crew on that to see what kind of output you get - should find around 25 issues.

Or create your own buggy file and see what it catches.

---

## Requirements

- Python 3.8 or higher
- API key from OpenAI or Anthropic (this costs a bit to run)
- Internet connection

Full dependencies are in `requirements.txt`.

---

## Limitations

Right now this only works with Python files. I'd like to add support for JavaScript/TypeScript eventually.

The API calls cost money - not a lot, but something to be aware of if you're running it on huge files.

Takes a few minutes per file since each agent has to make LLM calls.

## Ideas for Future Improvements

- Support other languages (JavaScript, Go, Java)
- Batch processing for multiple files
- Only analyze git diffs instead of entire files
- Local LLM support so you don't need API keys
- Custom rules that you can define yourself

---

## Contributing

This is mainly a learning project for me, but if you find bugs or have ideas, feel free to open an issue.

---

## License

MIT - use it however you want.

---

## Tech Stack

- Python
- CrewAI for agent orchestration
- OpenAI/Anthropic LLMs
- YAML for configuration
- Markdown for reports

---

## Troubleshooting

**Nothing's happening** - Check that your API key is set correctly as an environment variable.

**Reports look weird** - Make sure you're running it on Python files, not other languages.

**Taking forever** - Yeah, LLM calls are slow. Larger files take longer. Grab a coffee.
