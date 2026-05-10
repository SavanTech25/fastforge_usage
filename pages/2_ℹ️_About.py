import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from controller.sidebar import load_css, render_sidebar

ASSETS = Path(__file__).parent.parent / "assets"

st.set_page_config(page_title="About — Fast-Stack-Forge ⚡", page_icon="⚡", layout="wide")
load_css()

# ── Sidebar ───────────────────────────────────────────────────────────────────
render_sidebar()


# ── Header ────────────────────────────────────────────────────────────────────

st.markdown('<div class="page-title">About SavanTech</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">We build open-source developer tools that accelerate AI-powered backend development.</div>', unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4)
for col, val, lbl in [
    (s1, "1.0.0", "Fast-Stack-Forge Version"),
    (s2, "8+",    "CLI Commands"),
    (s3, "2025",  "Founded"),
    (s4, "🌍 BF", "Based in Burkina Faso"),
]:
    with col:
        st.markdown(f"""
        <div style='background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:12px;padding:20px;text-align:center;'>
            <div class="stat-val">{val}</div>
            <div class="stat-lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ── Mission ───────────────────────────────────────────────────────────────────
mc1, mc2 = st.columns(2, gap="large")

with mc1:
    st.markdown("""
    <div class="about-card">
        <h3>🎯 Our Mission</h3>
        <p>
        SavanTech was born from a simple frustration: setting up a production-ready FastAPI project
        takes hours of repetitive boilerplate. We believe developers should focus on <b>business logic</b>,
        not infrastructure wiring.
        </p>
        <p>
        Fast-Stack-Forge is our answer — a Symfony-inspired scaffolding CLI that generates everything from
        entities and AI services to full ETL pipelines in seconds. We ship tools that empower developers
        in Francophone Africa and beyond to build at the speed of thought.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card">
        <h3>⚡ Fast-Stack-Forge — Our Flagship Tool</h3>
        <p>
        Fast-Stack-Forge is an open-source CLI scaffolder for FastAPI inspired by Symfony's MakerBundle.
        With a single command you get a structured project with JWT auth, rate limiting, background tasks,
        WebSocket management, and optional AI services (RAG, Agents, OCR) all wired together.
        </p>
        <p>
        We built Fast-Stack-Forge to work seamlessly with <code>uv</code> for ultra-fast package management
        and <code>dbt</code> for analytics engineering — making it the ideal foundation for any
        AI-powered backend project.
        </p>
    </div>
    """, unsafe_allow_html=True)

with mc2:
    st.markdown("""
    <div class="about-card">
        <h3>🛠️ Our Tech Stack</h3>
        <p>Tools and technologies we use and build with:</p>
    </div>
    """, unsafe_allow_html=True)

    skills = [
        "FastAPI", "Python", "uv", "dbt", "LangChain", "LangGraph",
        "OpenAI", "Anthropic", "Mistral", "Gemini",
        "PostgreSQL", "MongoDB", "SQLite", "Redis",
        "Streamlit", "Docker", "Supabase", "Upstash",
        "Chroma", "Qdrant", "Pinecone", "APScheduler",
        "Pydantic", "SQLAlchemy", "Motor", "JWT",
    ]
    badges = "".join(f'<span class="skill-badge">{s}</span>' for s in skills)
    st.markdown(f'<div style="margin-top:-12px">{badges}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card" style="margin-top:20px">
        <h3>🗺️ Roadmap</h3>
    </div>
    """, unsafe_allow_html=True)

    timeline = [
        ("2025 Q1", "🚀 Fast-Stack-Forge v1.0 — init, make:entity, JWT, rate limiting"),
        ("2025 Q2", "🤖 make:service — RAG, Agent, Agentic, OCR AI services"),
        ("2025 Q2", "🌿 init:etl & make:dbt — full dbt scaffolding"),
        ("2025 Q3", "📊 make:dashboard — Streamlit multi-page generator"),
        ("2025 Q3", "🔄 make:sync — ELT Python sync scripts"),
        ("2025 Q4", "☁️ Fast-Stack-Forge Cloud — hosted scaffolding & templates (coming soon)"),
        ("2026",    "🌍 Fast-Stack-Forge Hub — community template marketplace"),
    ]
    for date, text in timeline:
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-text">
                <div class="timeline-date">{date}</div>
                {text}
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ── Team ──────────────────────────────────────────────────────────────────────
st.markdown("### 👥 Team")
t1, t2, t3, _ = st.columns([1, 1, 1, 1], gap="medium")

for col, name, role, emoji in [
    (t1, "Wendyam A. Yameogo", "Founder & Lead Engineer", "👨‍💻"),
    (t2, "SavanTech Team",     "Backend & AI Engineers",  "🤖"),
    (t3, "Open Source",        "Community Contributors",  "🌍"),
]:
    with col:
        st.markdown(f"""
        <div class="team-card">
            <div style="font-size:2.5rem">{emoji}</div>
            <div class="team-name">{name}</div>
            <div class="team-role">{role}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ── Contact & Links ───────────────────────────────────────────────────────────
st.markdown("### 📬 Get in Touch")
lk1, lk2, lk3, lk4, lk5 = st.columns(5)

for col, icon, label, href in [
    (lk1, "🐙", "GitHub",    "https://github.com/SavanTech25"),
    (lk2, "📦", "Fast-Stack-Forge", "https://github.com/SavanTech25/fast-stack-forge"),
    (lk3, "🐍", "PyPI",      "https://pypi.org/project/fast-stack-forge/"),
    (lk4, "📧", "Email",     "mailto:savantech25@gmail.com"),
    (lk5, "🌐", "Website",   "https://savantech.org"),
]:
    with col:
        st.markdown(f"""
        <div style='background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:12px;padding:18px;text-align:center;'>
            <div style='font-size:1.8rem'>{icon}</div>
            <div style='margin-top:8px'><a href='{href}' target='_blank' class='ext-link'>{label}</a></div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;color:#4a5568;font-size:0.82rem;padding:8px 0'>
    ⚡ Fast-Stack-Forge v1.0.0 · Built with ❤️ by <a href='https://savantech.org' style='color:#06b6d4'>SavanTech</a> · Burkina Faso 🇧🇫 ·
    <a href='mailto:savantech25@gmail.com' style='color:#06b6d4'>savantech25@gmail.com</a>
</div>""", unsafe_allow_html=True)
