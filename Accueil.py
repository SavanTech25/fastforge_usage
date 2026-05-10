import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from controller.sidebar import load_css, render_sidebar

ASSETS = Path(__file__).parent / "assets"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fast-Stack-Forge ⚡",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_css()


# ── Sidebar ───────────────────────────────────────────────────────────────────
render_sidebar()






st.markdown("""
<div class="hero-section">
  <div class="hero-title">Fast-Stack-Forge ⚡</div>
  <div class="hero-sub">A powerful, Symfony-style CLI scaffolder for FastAPI — built for speed, built for scale.</div>
  <span class="badge">🚀 FastAPI</span>
  <span class="badge">🐍 Python</span>
  <span class="badge">⚡ uv</span>
  <span class="badge">🌿 dbt</span>
  <span class="badge">🤖 AI Services</span>
  <span class="badge">🔗 LangChain</span>
  <span class="badge">🗄️ SQLAlchemy</span>
  <span class="badge">🍃 MongoDB</span>
</div>
""", unsafe_allow_html=True)


# ── What is Fast-Stack-Forge ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🧰 What is Fast-Stack-Forge?</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="large")
with col1:
    st.markdown("""
    **Fast-Stack-Forge** is a CLI tool inspired by Symfony's MakerBundle that bootstraps and accelerates FastAPI development.  
    Instead of spending hours creating boilerplate, you run a single command and get a **production-ready project structure** complete with:

    - 🔐 JWT Authentication middleware
    - ⚡ Rate limiting with `slowapi`
    - 📆 Background scheduling with `apscheduler`
    - 🔌 WebSocket connection manager
    - 📦 Dependency management via `uv`
    - 🤖 AI Services (RAG, Agents, OCR) ready to go
    - 🌿 dbt ETL pipelines for analytics
    """)

with col2:
    st.markdown("""
        <div class="arch-box" style="margin-bottom:10px;">
            <div class="arch-box-title">🏗️ fast-stack-forge init my_project</div>
            <div class="arch-box-sub">Scaffolds a full FastAPI project in seconds</div>
        </div>
        <div class="arch-box" style="margin-bottom:10px;">
            <div class="arch-box-title">🧩 fast-stack-forge make:entity User</div>
            <div class="arch-box-sub">Generates model + schema + controller + router</div>
        </div>
        <div class="arch-box" style="margin-bottom:10px;">
            <div class="arch-box-title">🤖 fast-stack-forge make:service Bot --type rag</div>
            <div class="arch-box-sub">Scaffolds a production-ready RAG service</div>
        </div>
        <div class="arch-box">
            <div class="arch-box-title">🌿 fast-stack-forge init:etl my_dbt --archi medallion</div>
            <div class="arch-box-sub">Full dbt project with bronze/silver/gold layers</div>
        </div>
    """, unsafe_allow_html=True)


# ── Commands Overview ─────────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 All Commands</div>', unsafe_allow_html=True)

commands = [
    {
        "icon": "🚀",
        "title": "fast-stack-forge init <name> --db <engine>",
        "desc": "Bootstrap a new FastAPI project with the complete directory structure, Makefile, pyproject.toml, JWT middleware, rate limiting, scheduling, WebSocket manager, and a CRUD utility router. Choose between sqlite, postgresql, mysql, or mongodb as your database engine."
    },
    {
        "icon": "🧩",
        "title": "fast-stack-forge make:entity <Name> <fields>",
        "desc": "Auto-generate the Entity (model), Schema (Pydantic), Controller (business logic), and Router (API routes) for a given entity. Supports field types: string, int, float, bool, text, date, datetime — and modifiers: hash, encrypt, nullable, fk=ModelName."
    },
    {
        "icon": "🌿",
        "title": "fast-stack-forge init:etl <name> --archi <style> --connector <db>",
        "desc": "Initialize a complete dbt project inside your project's src/ directory. Choose an architecture style: default (stg/int/mart), medallion (bronze/silver/gold), or star (raw/dim/fact). Supports DuckDB, Snowflake, BigQuery, and PostgreSQL connectors."
    },
    {
        "icon": "📐",
        "title": "fast-stack-forge make:dbt <model> [--view] [--incremental] [--layer]",
        "desc": "Quickly scaffold a dbt SQL or Python model in the correct layer. Use --view for view materialization, --incremental to add incremental logic, --python for a Python-based model, and --layer to place it in a specific architecture layer (e.g., bronze, silver, gold)."
    },
    {
        "icon": "🤖",
        "title": "fast-stack-forge make:service <Name> --type <t> --provider <p>",
        "desc": "Generate a production-ready AI service and its FastAPI router. Types: rag (Retrieval-Augmented Generation), agent (tool-calling), agentic (LangGraph workflow), ocr (Vision extraction). Providers: openai, anthropic, mistral, gemini, azure. For RAG, choose a vector store: chroma, qdrant, supabase, or upstash."
    },
    {
        "icon": "🔄",
        "title": "fast-stack-forge make:sync <Name> --source <db> --dest <db>",
        "desc": "Scaffold a Python ELT sync script that replicates data from an operational database (MongoDB, PostgreSQL, etc.) to an analytical warehouse. Includes APScheduler boilerplate for continuous execution and pandas-based document flattening."
    },
    {
        "icon": "📊",
        "title": "fast-stack-forge make:dashboard [pages...]",
        "desc": "Generate a multi-page Streamlit dashboard inside your project's app/dashboard/ directory. Specify page names like Atelier, Analytics, Chatbot. Automatically updates your Makefile with a 'make dashboard' target to launch the dashboard with uv."
    },
    {
        "icon": "🗑️",
        "title": "fast-stack-forge make:discard <EntityName>",
        "desc": "Remove a previously generated entity along with its associated schema, controller, and router files. Safely cleans up the scaffolded boilerplate without affecting the rest of your project."
    },
]

for i in range(0, len(commands), 2):
    cols = st.columns(2, gap="medium")
    for j, col in enumerate(cols):
        if i + j < len(commands):
            cmd = commands[i + j]
            with col:
                st.markdown(f"""
                <div class="cmd-card">
                    <div class="cmd-icon">{cmd['icon']}</div>
                    <div class="cmd-title">{cmd['title']}</div>
                    <div class="cmd-desc">{cmd['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ── Minimum Requirements ──────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">✅ Minimum Requirements</div>', unsafe_allow_html=True)

req_col1, req_col2 = st.columns(2, gap="large")

with req_col1:
    st.markdown("""
    <div class="req-card">
        <div class="req-title">🐍 Python ≥ 3.11</div>
        <div class="req-desc">Fast-Stack-Forge uses modern Python features. Python 3.11+ is required.</div>
    </div>
    <div class="req-card">
        <div class="req-title">⚡ uv (Astral)</div>
        <div class="req-desc">Fast-Stack-Forge uses uv for virtual environment management and ultra-fast dependency installation. Install via: <code>curl -LsSf https://astral.sh/uv/install.sh | sh</code></div>
    </div>
    <div class="req-card">
        <div class="req-title">🗄️ Database (optional)</div>
        <div class="req-desc">For PostgreSQL or MySQL projects, you'll need a running server. MongoDB projects need a running MongoDB instance or Atlas URI. SQLite requires no setup.</div>
    </div>
    """, unsafe_allow_html=True)

with req_col2:
    st.markdown("""
    <div class="req-card">
        <div class="req-title">📦 Fast-Stack-Forge itself</div>
        <div class="req-desc">Install globally via pip or uv tool — no virtual env needed for the CLI itself.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="code-block"><span class="code-comment"># Install Fast-Stack-Forge globally</span>
<span class="code-cmd">pip install</span> <span class="code-arg">fast-stack-forge</span>
<span class="code-comment"># Or with uv: uv tool install fast-stack-forge</span>

<span class="code-comment"># Verify installation</span>
<span class="code-cmd">fast-stack-forge</span> <span class="code-flag">--version</span>

<span class="code-comment"># Bootstrap your first project</span>
<span class="code-cmd">fast-stack-forge init</span> <span class="code-arg">my_project</span> <span class="code-flag">--db postgresql</span>

<span class="code-comment"># Install dependencies & run</span>
<span class="code-cmd">cd</span> <span class="code-arg">my_project</span>
<span class="code-cmd">make</span> <span class="code-arg">install</span>
<span class="code-cmd">make</span> <span class="code-arg">run</span></div>
    """, unsafe_allow_html=True)


# ── Quick Start Workflow ───────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚡ Quick Start Workflow</div>', unsafe_allow_html=True)

steps = [
    ("1️⃣", "Install Fast-Stack-Forge", "pip install fast-stack-forge"),
    ("2️⃣", "Init your project", "fast-stack-forge init my_api --db postgresql"),
    ("3️⃣", "Install deps & run", "cd my_api && make install && make run"),
    ("4️⃣", "Generate an entity", "fast-stack-forge make:entity User name:string email:string:hash role:string"),
    ("5️⃣", "Add an AI service", "fast-stack-forge make:service ChatBot --type rag --provider openai --vector-store qdrant"),
    ("6️⃣", "Add analytics (ETL)", "fast-stack-forge init:etl my_api_etl --archi medallion --connector postgres"),
    ("7️⃣", "Generate dashboard", "fast-stack-forge make:dashboard Analytics Chatbot"),
]

for icon, title, cmd in steps:
    col_i, col_t, col_c = st.columns([0.5, 2, 4], gap="small")
    with col_i:
        st.markdown(f"<div style='font-size:1.4rem;padding-top:8px'>{icon}</div>", unsafe_allow_html=True)
    with col_t:
        st.markdown(f"<div style='font-weight:600;color:#a5b4fc;padding-top:12px'>{title}</div>", unsafe_allow_html=True)
    with col_c:
        st.code(cmd, language="bash")

# ── Project Architecture ───────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏗️ Generated Project Architecture</div>', unsafe_allow_html=True)

arc_col1, arc_col2 = st.columns([2, 3], gap="large")
with arc_col1:
    st.markdown("When you run `fast-stack-forge init my_project`, here is the complete structure generated for you:")
    st.code("""my_project/
├── app/
│   ├── main.py              ← FastAPI entrypoint
│   └── dashboard/           ← Streamlit pages (make:dashboard)
├── src/
│   └── my_project/
│       ├── entity/          ← Database models
│       ├── schema/          ← Pydantic schemas
│       ├── controller/      ← Business logic
│       ├── router/          ← API routes
│       ├── service/         ← AI services
│       ├── data/            ← DB connection
│       ├── middleware/      ← JWT middleware
│       └── utils/
│           ├── limiter.py   ← Rate limiting
│           ├── scheduling.py← Background tasks
│           ├── crud_router.py← CRUD factory
│           └── connection_manager.py
├── Makefile
├── pyproject.toml
└── .env""", language="text")

with arc_col2:
    st.markdown("### 🧩 Key Components")
    st.markdown("""
| Component | File | Description |
|-----------|------|-------------|
| 🚀 **App Entry** | `app/main.py` | FastAPI app with lifecycle hooks, rate limiter, scheduler |
| 🗄️ **Database** | `src/*/data/database.py` | Connection setup for your chosen DB engine |
| 🔐 **Auth** | `src/*/middleware/middleware.py` | Pre-configured `JWTBearer` for route protection |
| ⚡ **Rate Limiter** | `src/*/utils/limiter.py` | `slowapi` integration, ready to use |
| 📆 **Scheduler** | `src/*/utils/scheduling.py` | `apscheduler` background jobs |
| 🔌 **WebSocket** | `src/*/utils/connection_manager.py` | Generic WS manager |
| 🛣️ **CRUD Router** | `src/*/utils/crud_router.py` | Generic factory for standard CRUD routes |
| 🤖 **AI Service** | `src/*/service/*.py` | Generated by `make:service` |
""")

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;color:#4a5568;font-size:0.85rem;padding:16px 0'>
    ⚡ Fast-Stack-Forge · by <a href="https://savantech.org" class="ext-link">SavanTech</a> ·
    <a href="https://github.com/SavanTech25/fast-stack-forge" class="ext-link">GitHub</a> ·
    <a href="mailto:savantech25@gmail.com" class="ext-link">savantech25@gmail.com</a>
</div>
""", unsafe_allow_html=True)
