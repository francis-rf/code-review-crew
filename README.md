# Code Review Crew 🤖🔎

I built this multi-agent system to solve a problem I constantly face: catching subtle bugs and security flaws _before_ they become production nightmares.

Originally, this was just a CLI tool, but **I recently overhauled it** to include a full **Streamlit Web UI** and **GitHub Repository Integration**. Now, instead of manually running scripts, I can just paste a repo URL or upload a file and let the agents go to work.

---

## 🚀 Why I Built This

I wanted to see if specialized AI agents could work together like a real code review team. Turns out, they're surprisingly good at it.

- **The Problem**: I often miss things like checking for empty lists or subtle SQL injection risks when I'm tired.
- **The Solution**: A "crew" of agents where each one wears a specific hat (Security, Performance, Bug Hunting).

---

## ✨ New Features I Added

### 🖥️ Interactive Web UI

I realized running CLI commands wasn't the best experience effectively, so I built a **Streamlit interface**.

- **Upload Files Directly**: Drag and drop python files for instant analysis.
- **Visual Reports**: See risk scores and issues formatted nicely, not just raw text.

### 🔗 GitHub Integration

I added a feature to **pull code directly from GitHub**.

- Paste any public repository URL.
- The system clones it, analyzes the structure, and lets you pick specific files to review.
- Saves me the hassle of manually downloading files just to check them.

---

## 🧠 The Crew (My Agents)

I set up 4 different agents to mimic a human review process:

1.  **Bug Detector**: Looks for logical errors, edge cases, and exception handling issues. Basically looks for things that will crash the app.
2.  **Security Analyzer**: Scans for vulnerabilities like SQL injection, hardcoded secrets, and XSS. I based its rules on OWASP guidelines.
3.  **Performance Analyzer**: Checks for algorithmic bottlenecks and inefficient loops.
4.  **Documentation Analyzer**: Reviews docstrings and then compiles the final "Senior Engineer" style report.

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- An API key (OpenAI or Anthropic)

### Installation

```bash
# Clone the repo
git clone https://github.com/francis-rf/code-review-crew.git
cd code_review_crew

# Install dependencies
pip install -r requirements.txt
```

### Running the App

I made it super easy to start. Just run the Streamlit app:

```bash
streamlit run src/app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📂 Project Structure

Here's how I organized the code:

```
code_review_crew/
├── src/
│   ├── app.py                  # The new Streamlit Web UI entry point
│   ├── crew.py                 # The core CrewAI orchestration logic
│   ├── config/
│       ├── agents.yaml         # Where I define the agent "personalities"
│       └── tasks.yaml          # The specific instructions for each agent
├── examples/                   # Test files I use to verify the agents
├── output/                     # Generated reports go here
└── requirements.txt
```

---

## 💡 What I Learned

Building this taught me a lot about **Agentic Workflows**:

- **Context is King**: Agents need clear, specific goals (YAML config) or they get sidetracked.
- **UI Matters**: Moving from CLI to Streamlit made the tool 10x more usable for quick checks.
- **Handling Large Codebases**: Integrating GitHub cloning was tricky (keeping it efficient), but having agents read directly from repo files is a game changer.

---

## 🛡️ License

MIT. Feel free to use this code, break it, and learn from it!
