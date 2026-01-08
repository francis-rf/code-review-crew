"""
Code Review Crew - AI-Powered Code Analysis System

This module implements a multi-agent system for comprehensive Python code review.
Four specialized AI agents collaborate to analyze code for bugs, security issues,
performance bottlenecks, and documentation quality.

Agents:
    - Bug Detector: Identifies logical errors and edge cases
    - Security Analyzer: Finds vulnerabilities and security risks
    - Performance Analyzer: Detects bottlenecks and optimization opportunities
    - Documentation Analyzer: Reviews code documentation and generates final report

Usage:
    crew = CodeReviewCrew(code_file_path="path/to/code.py")
    result = crew.run()
"""

# Windows compatibility patch for libraries expecting SIGHUP
import signal
import sys
if sys.platform == 'win32' and not hasattr(signal, 'SIGHUP'):
    signal.SIGHUP = 1

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Load .env explicitly from project root before importing crewai
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

import yaml
from crewai import Agent, Crew, Process, Task

class CodeReviewCrew:
    """
    Multi-agent system for comprehensive Python code review.

    This crew analyzes Python code files and generates detailed reports covering:
    - Bug detection and edge cases
    - Security vulnerabilities
    - Performance optimizations
    - Documentation quality

    Attributes:
        code_file_path (str): Path to the Python file to review
        output_dir (str): Directory for output files
        agents_config (dict): Agent configurations from YAML
        tasks_config (dict): Task configurations from YAML
    """

    def __init__(
        self,
        code_file_path: str,
        output_dir: str = "output",
        config_dir: Optional[str] = None,
        code_content: Optional[str] = None
    ):
        """
        Initialize the Code Review Crew.

        Args:
            code_file_path: Path to the Python file (or "GITHUB_REPO" for multi-file)
            output_dir: Directory for output files (default: "output")
            config_dir: Custom config directory (default: src/config)
            code_content: Optional direct code content override
        """
        self.output_dir = output_dir
        self.code_file_path = code_file_path
        self.code_file_name = os.path.basename(code_file_path)

        # Handle direct content injection (e.g. from GitHub)
        if code_content:
            self.code_content = code_content
            self.code_lines = self.code_content.splitlines()
            print(f"✓ Loaded {len(self.code_lines)} lines from direct content")
        else:
            # Validate input file
            if not os.path.exists(code_file_path):
                raise FileNotFoundError(f"Code file not found: {code_file_path}")

            if not code_file_path.endswith('.py'):
                raise ValueError(f"File must be a Python file (.py): {code_file_path}")

            self.code_file_path = os.path.abspath(code_file_path)
            
            # Read the code file content
            with open(self.code_file_path, 'r', encoding='utf-8') as f:
                self.code_content = f.read()
                self.code_lines = self.code_content.splitlines()

            print(f"✓ Loaded {len(self.code_lines)} lines of code")

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Set config directory
        if config_dir is None:
            # Default to src/config relative to this file
            current_dir = Path(__file__).parent
            config_dir = current_dir / "config"

        self.config_dir = Path(config_dir)

        # Load configurations
        self.agents_config = self._load_yaml(self.config_dir / "agents.yaml")
        self.tasks_config = self._load_yaml(self.config_dir / "tasks.yaml")

        # Initialize agents and tasks
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()

        print(f"✓ Code Review Crew initialized")
        print(f"  File: {self.code_file_name}")
        print(f"  Output: {self.output_dir}/")

    def _load_yaml(self, file_path: Path) -> dict:
        """Load and parse YAML configuration file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load {file_path}: {e}")

    def _create_agents(self) -> Dict[str, Agent]:
        """Create all agents from configuration."""
        agents = {}

        agent_names = [
            'bug_detector_agent',
            'security_analyzer_agent',
            'performance_analyzer_agent',
            'documentation_analyzer_agent'
        ]

        for agent_name in agent_names:
            if agent_name not in self.agents_config:
                raise KeyError(f"Agent '{agent_name}' not found in agents.yaml")

            config = self.agents_config[agent_name]

            agents[agent_name] = Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                verbose=config.get('verbose', True),
                allow_delegation=config.get('allow_delegation', False),
                memory=config.get('memory', True)
            )

        print(f"✓ Created {len(agents)} agents")
        return agents

    def _create_tasks(self) -> List[Task]:
        """Create all tasks from configuration with file path injection."""
        tasks = []

        task_names = [
            'bug_detection_task',
            'security_analysis_task',
            'performance_analysis_task',
            'documentation_review_task'
        ]

        agent_mapping = {
            'bug_detection_task': 'bug_detector_agent',
            'security_analysis_task': 'security_analyzer_agent',
            'performance_analysis_task': 'performance_analyzer_agent',
            'documentation_review_task': 'documentation_analyzer_agent'
        }

        task_dependencies = {
            'bug_detection_task': [],
            'security_analysis_task': ['bug_detection_task'],
            'performance_analysis_task': ['bug_detection_task', 'security_analysis_task'],
            'documentation_review_task': ['bug_detection_task', 'security_analysis_task', 'performance_analysis_task']
        }

        task_objects = {}

        for task_name in task_names:
            if task_name not in self.tasks_config:
                raise KeyError(f"Task '{task_name}' not found in tasks.yaml")

            config = self.tasks_config[task_name]
            agent_name = agent_mapping[task_name]

            # Inject file path and code content into description
            description = config['description'].format(
                code_file_path=self.code_file_path,
                code_file_name=self.code_file_name,
                code_content=self.code_content,
                total_lines=len(self.code_lines),
                datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

            expected_output = config['expected_output']

            # Build context (dependencies)
            context = []
            for dep_task_name in task_dependencies[task_name]:
                if dep_task_name in task_objects:
                    context.append(task_objects[dep_task_name])

            task = Task(
                description=description,
                expected_output=expected_output,
                agent=self.agents[agent_name],
                context=context if context else None
            )

            task_objects[task_name] = task
            tasks.append(task)

        print(f"✓ Created {len(tasks)} tasks with dependencies")
        return tasks

    def run(self) -> Any:
        """
        Execute the code review process.

        Returns:
            CrewOutput: Result containing the comprehensive code review report
        """
        print("\n" + "="*70)
        print("🔍 STARTING CODE REVIEW")
        print("="*70)
        print(f"File: {self.code_file_name}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")

        try:
            # Create crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True
            )

            # Execute review
            print("🤖 Agents are analyzing your code...\n")
            result = crew.kickoff()

            # Save results
            self._save_results(result)

            print("\n" + "="*70)
            print("✅ CODE REVIEW COMPLETE")
            print("="*70)
            print(f"Report saved to: {self.output_dir}/")
            print("="*70 + "\n")

            return result

        except Exception as e:
            print(f"\n❌ Error during code review: {e}")
            raise

    def _save_results(self, result: Any) -> None:
        """Save review results to files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = Path(self.code_file_name).stem

        # Save as markdown
        report_path = f"{self.output_dir}/{base_name}_review_{timestamp}.md"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Code Review Report\n\n")
            f.write(f"**File**: {self.code_file_name}\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            # Write result
            result_text = str(result.raw) if hasattr(result, 'raw') else str(result)
            f.write(result_text)

        print(f"\n✓ Report saved: {report_path}")

        # Also save raw output for debugging
        raw_path = f"{self.output_dir}/{base_name}_raw_{timestamp}.txt"
        with open(raw_path, 'w', encoding='utf-8') as f:
            f.write(result_text)

        print(f"✓ Raw output saved: {raw_path}")


def main():
    """CLI entry point for Code Review Crew."""
    import argparse

    parser = argparse.ArgumentParser(
        description="AI-Powered Code Review System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review a Python file
  python code_review_crew.py my_script.py

  # Review with custom output directory
  python code_review_crew.py my_script.py --output reports/

  # Review example file
  python code_review_crew.py examples/buggy_code.py
        """
    )

    parser.add_argument(
        'code_file',
        help='Path to Python file to review'
    )

    parser.add_argument(
        '--output', '-o',
        default='output',
        help='Output directory for reports (default: output)'
    )

    parser.add_argument(
        '--config',
        help='Custom config directory (default: src/config)'
    )

    args = parser.parse_args()

    try:
        # Initialize and run crew
        crew = CodeReviewCrew(
            code_file_path=args.code_file,
            output_dir=args.output,
            config_dir=args.config
        )

        result = crew.run()

        print("\n💡 Review complete! Check the output directory for the full report.")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Review cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
