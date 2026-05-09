"""
Shared sidebar renderer and CSS loader for all FastForge Streamlit pages.
Call load_css() then render_sidebar() at the top of each page.
"""
import streamlit as st
from pathlib import Path

ASSETS = Path(__file__).parent.parent / "assets"

LINKEDIN_URL = "https://www.linkedin.com/in/wendyam-yameogo"
GITHUB_URL   = "https://github.com/SavanTech25/fastforge"
WEBSITE_URL  = "https://savantech.org"
EMAIL        = "savantech25@gmail.com"


def load_css() -> None:
    """Inject the shared stylesheet from assets/style.css."""
    css_file = ASSETS / "style.css"
    if css_file.exists():
        st.markdown(f"<style>{css_file.read_text()}</style>", unsafe_allow_html=True)


def render_sidebar() -> None:
    """
    Render the shared sidebar:
      1. SavanTech logo (small, top)
      2. Resources links
      3. Credits — Propulsé par SavanTech / Wendyam YAMEOGO
    Note: Streamlit already renders the page navigation automatically above
    the sidebar content, so we do NOT add page links manually here.
    """
    with st.sidebar:
        # ── 1. Resources ──────────────────────────────────────────────────────
        st.markdown("### 🔗 Resources")
        st.markdown(f"""
- [📦 FastForge GitHub]({GITHUB_URL})
- [🌐 SavanTech]({WEBSITE_URL})
- [📖 FastAPI Docs](https://fastapi.tiangolo.com/)
- [⚡ uv Docs](https://docs.astral.sh/uv/)
- [🌿 dbt Docs](https://docs.getdbt.com/)
- [🤖 LangChain](https://python.langchain.com/)
""")

        st.markdown("---")

        # ── 2. Credits ────────────────────────────────────────────────────────
        st.markdown(
            f"""
<div style="font-size:0.78rem;color:#64748b;line-height:1.9;padding-bottom:8px">
    <div style="color:#a5b4fc;font-weight:700;font-size:0.85rem;margin-bottom:6px">
        ⚡ FastForge <span style="color:#4a5568;font-weight:400">v1.0.0</span>
    </div>
    Propulsé par&nbsp;
    <a href="{WEBSITE_URL}" target="_blank"
       style="color:#06b6d4;text-decoration:none;font-weight:600">SavanTech</a>
    <br>
    <span style="color:#94a3b8">👨‍💻 <strong>Wendyam YAMEOGO</strong></span>
    <br>
    <a href="{LINKEDIN_URL}" target="_blank"
       style="color:#0a66c2;text-decoration:none;font-weight:500">🔗 LinkedIn</a>
    &nbsp;·&nbsp;
    <a href="mailto:{EMAIL}"
       style="color:#06b6d4;text-decoration:none">✉️ {EMAIL}</a>
</div>
""",
            unsafe_allow_html=True,
        )
