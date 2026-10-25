import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from controller.sidebar import load_css, render_sidebar
from controller import forge

st.set_page_config(page_title="About · fast-stack-forge", page_icon="⚡", layout="wide")
load_css()
render_sidebar()

forge.page_header(
    "About SavanTech",
    "We build open-source developer tools that take the boilerplate out of backend, data and AI projects.",
)

# ── Facts ─────────────────────────────────────────────────────────────────────
facts = [
    (forge.version(), "fast-stack-forge version"),
    (str(len(forge.public_commands())), "CLI commands"),
    ("2025", "Founded"),
    ("Burkina Faso", "Where we're based"),
]
st.markdown(
    '<div class="facts">' + "".join(f'<div class="fact"><b>{v}</b><span>{l}</span></div>' for v, l in facts) + "</div>",
    unsafe_allow_html=True,
)
st.divider()

# ── Mission and roadmap ───────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown(
        """
<div class="prose">
  <h3>Why we built it</h3>
  <p>SavanTech started from a simple frustration: setting up a production-ready FastAPI project
  took hours of the same wiring every time. Developers should spend that time on business logic.</p>
  <p>fast-stack-forge is our answer, a scaffolder inspired by Symfony's MakerBundle. It now covers the
  whole path from an API to analytics: FastAPI backends, AI services, dbt projects, Databricks bundles
  and data science repos, all managed with <code>uv</code>. We build it for developers in Francophone
  Africa and everywhere else.</p>
  <h3>How it works</h3>
  <p>Run <code>fast-stack-forge new</code> and answer a few questions, or pass every option as a flag
  and add <code>-y</code> to run it in CI. The generated projects use your choices for everything:
  database driver, dbt adapter, Databricks runtime, AI provider and vector store.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="panel-label">What we work with</div>', unsafe_allow_html=True)
    stack = [
        "FastAPI", "Pydantic", "SQLAlchemy", "Motor", "uv", "dbt", "DuckDB", "Snowflake", "BigQuery",
        "Databricks", "Lakeflow", "LangChain", "LangGraph", "OpenAI", "Anthropic", "Mistral", "Gemini",
        "Azure OpenAI", "Chroma", "Qdrant", "Supabase", "Upstash", "PostgreSQL", "MongoDB", "Streamlit",
        "Docker", "APScheduler",
    ]
    st.markdown('<div class="chips">' + "".join(f"<span>{s}</span>" for s in stack) + "</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="prose"><h3>Roadmap</h3></div>', unsafe_allow_html=True)
    timeline = [
        ("2025 Q1", "v1.0: init, make:entity, JWT, rate limiting", False),
        ("2025 Q2", "make:service: RAG, agent, agentic and OCR services", False),
        ("2025 Q2", "init:etl and make:dbt: dbt scaffolding", False),
        ("2025 Q3", "make:dashboard and make:sync", False),
        ("2026 Q1", "AstroData: init:ds-data and init:ds-make for data science", False),
        ("2026 Q4", "v1.1: the new wizard, init:dbt with five adapters, init:databricks, rewritten AI services", False),
        ("Next", "fast-stack-forge Cloud: hosted scaffolding and templates", True),
        ("Next", "fast-stack-forge Hub: a community template marketplace", True),
    ]
    st.markdown(
        '<div class="timeline">'
        + "".join(
            f'<div class="tl-item{" next" if upcoming else ""}"><div class="tl-date">{date}</div>'
            f'<div class="tl-text">{text}</div></div>'
            for date, text, upcoming in timeline
        )
        + "</div>",
        unsafe_allow_html=True,
    )

st.divider()

# ── Team ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="prose"><h3>Team</h3></div>', unsafe_allow_html=True)
team = [
    ("Wendyam A. Yameogo", "Founder and lead engineer"),
    ("SavanTech team", "Backend and AI engineers"),
    ("Open-source contributors", "Issues, ideas and pull requests"),
]
for col, (name, role) in zip(st.columns(4, gap="medium"), team):
    with col:
        st.markdown(f'<div class="person"><b>{name}</b><span>{role}</span></div>', unsafe_allow_html=True)

st.divider()

# ── Contact ───────────────────────────────────────────────────────────────────
st.markdown('<div class="prose"><h3>Get in touch</h3></div>', unsafe_allow_html=True)
links = [
    ("SavanTech on GitHub", "https://github.com/SavanTech25"),
    ("fast-stack-forge source", "https://github.com/SavanTech25/fast-stack-forge"),
    ("Package on PyPI", forge.PYPI_URL),
    ("savantech25@gmail.com", "mailto:savantech25@gmail.com"),
    ("savantech.org", "https://savantech.org"),
]
st.markdown(
    '<div class="contact">' + "".join(f'<a href="{href}" target="_blank">{text}</a>' for text, href in links) + "</div>",
    unsafe_allow_html=True,
)

forge.footer()
