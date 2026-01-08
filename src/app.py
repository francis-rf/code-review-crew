import streamlit as st
import os
import tempfile
import time
import shutil
import git
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables explicitly from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

from code_review_crew import CodeReviewCrew

# Page Config
st.set_page_config(
    page_title="Code Review Crew AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Custom CSS
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    load_css(css_path)

# Header
st.title("🤖 AI Code Review Crew")

# Sidebar
with st.sidebar:
    st.header("Mode Selection")
    mode = st.radio("Choose Input Source", ["Upload File", "GitHub Repository"])

# Main Content
if mode == "Upload File":
    st.markdown("### 📤 Upload Single File")
    uploaded_file = st.file_uploader("Drop your Python file here", type=['py'])

    if uploaded_file is not None:
        if st.button("🚀 Start Code Review", type="primary"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                src_dir = Path(__file__).parent
                config_dir = src_dir / "config"
                
                with st.spinner("Initializing Agents..."):
                    crew = CodeReviewCrew(
                        code_file_path=tmp_path,
                        output_dir="output",
                        config_dir=str(config_dir)
                    )
                
                with st.status("🔍 Analyzing Code...", expanded=True) as status:
                    st.write("🐛 Senior Bug Detective is checking logic...")
                    result = crew.run()
                    status.update(label="✅ Review Complete!", state="complete", expanded=False)
                
                final_report = str(result.raw) if hasattr(result, 'raw') else str(result)
                st.markdown(final_report)
                
                st.download_button(
                    label="📥 Download Report",
                    data=final_report,
                    file_name=f"{uploaded_file.name}_review.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

elif mode == "GitHub Repository":
    st.markdown("### 🐙 Analyze GitHub Repo")
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/username/repo")
    
    if "repo_path" not in st.session_state:
        st.session_state.repo_path = None

    if st.button("Fetch Repository"):
        if repo_url:
            try:
                temp_dir = tempfile.mkdtemp()
                with st.spinner(f"Cloning {repo_url}..."):
                    git.Repo.clone_from(repo_url, temp_dir)
                    st.session_state.repo_path = temp_dir
                    st.success("✅ Repository Cloned!")
            except Exception as e:
                st.error(f"Failed to clone: {e}")
    
    if st.session_state.repo_path:
        # List Python files
        py_files = []
        for root, dirs, files in os.walk(st.session_state.repo_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, st.session_state.repo_path)
                    py_files.append(rel_path)
        
        selected_files = st.multiselect("Select files to analyze", py_files, default=py_files[:5])
        
        if st.button("🚀 Analyze Selected Files", type="primary"):
            if selected_files:
                combined_content = ""
                for file_rel in selected_files:
                    full_path = os.path.join(st.session_state.repo_path, file_rel)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            combined_content += f"\n\n=== FILE: {file_rel} ===\n{content}\n"
                    except Exception as e:
                        st.warning(f"Skipping {file_rel}: {e}")
                
                try:
                    src_dir = Path(__file__).parent
                    config_dir = src_dir / "config"
                    
                    with st.spinner("Agents are analyzing the selected files..."):
                        crew = CodeReviewCrew(
                            code_file_path="GITHUB_REPO",
                            code_content=combined_content,
                            output_dir="output",
                            config_dir=str(config_dir)
                        )
                        result = crew.run()
                    
                    final_report = str(result.raw) if hasattr(result, 'raw') else str(result)
                    st.markdown(final_report)
                    
                    st.download_button(
                        label="📥 Download Report",
                        data=final_report,
                        file_name="github_repo_review.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Analysis Failed: {e}")
            else:
                st.warning("Please select at least one file.")
