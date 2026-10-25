"""
Shared sidebar renderer and CSS loader for all Fast-Stack-Forge Streamlit pages.
Call load_css() then render_sidebar() at the top of each page.
"""
import streamlit as st
from pathlib import Path

from controller.forge import PYPI_URL, version

ASSETS = Path(__file__).parent.parent / "assets"

LINKEDIN_URL = "https://www.linkedin.com/in/wendyam-yameogo"
GITHUB_URL   = "https://github.com/SavanTech25/fast-stack-forge"
WEBSITE_URL  = "https://savantech.org"
EMAIL        = "savantech25@gmail.com"


def load_css() -> None:
    """Inject the shared stylesheet from assets/style.css."""
    css_file = ASSETS / "style.css"
    if css_file.exists():
        st.markdown(f"<style>{css_file.read_text()}</style>", unsafe_allow_html=True)


def render_sidebar() -> None:
    """
    Render the shared sidebar under Streamlit's automatic page navigation:
      1. Product name and installed CLI version
      2. Documentation links
      3. Credits, SavanTech / Wendyam YAMEOGO
    """
    st.logo(str(ASSETS / "savantech_logo.png"), link=WEBSITE_URL)
    with st.sidebar:
        st.markdown(
            f"""
<div class="side-brand">fast-stack-forge</div>
<div class="side-version">v{version()} installed</div>
<div class="side-links">
  <a href="{GITHUB_URL}" target="_blank">Source on GitHub</a>
  <a href="{PYPI_URL}" target="_blank">Package on PyPI</a>
  <a href="https://docs.astral.sh/uv/" target="_blank">uv docs</a>
  <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI docs</a>
  <a href="https://docs.getdbt.com/" target="_blank">dbt docs</a>
  <a href="https://docs.databricks.com/dev-tools/bundles/" target="_blank">Databricks Asset Bundles</a>
  <a href="https://python.langchain.com/" target="_blank">LangChain docs</a>
</div>
""",
            unsafe_allow_html=True,
        )
        st.divider()
        st.markdown(
            f"""
<div class="side-credit">
  Built by <a href="{WEBSITE_URL}" target="_blank">SavanTech</a><br>
  Wendyam YAMEOGO<br>
  <a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a> · <a href="mailto:{EMAIL}">{EMAIL}</a>
</div>
""",
            unsafe_allow_html=True,
        )
