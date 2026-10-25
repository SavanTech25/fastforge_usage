import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from controller.sidebar import load_css, render_sidebar
from controller import forge

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="fast-stack-forge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto",
)
load_css()
render_sidebar()
forge.require_package()


def section(title: str, intro: str = "") -> None:
    st.markdown(f'<div class="sec"><h2>{title}</h2>{f"<p>{intro}</p>" if intro else ""}</div>', unsafe_allow_html=True)


# ── Hero: the wizard ──────────────────────────────────────────────────────────
hero_text, hero_term = st.columns([5, 6], gap="large")
with hero_text:
    st.markdown(
        """
<div class="hero">
  <div class="name">fast-stack-forge</div>
  <h1>Answer a few questions. Get a project that runs.</h1>
  <p>A Symfony-style scaffolder for FastAPI backends, dbt projects, Databricks bundles,
  AI services and data science repos. Every project comes managed with <code>uv</code>
  and a <code>Makefile</code>, ready for <code>make install</code>.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    b1, b2 = st.columns([1, 1])
    with b1:
        st.page_link("pages/1_⚡_Generate.py", label="Generate a project", icon=":material/bolt:")
    with b2:
        st.page_link("https://github.com/SavanTech25/fast-stack-forge", label="Read the source", icon=":material/code:")

with hero_term:
    st.markdown(
        forge.terminal(
            [
                "$ fast-stack-forge new",
                "What do you want to create?",
                "  [1] fastapi     FastAPI backend",
                "  [2] dbt         dbt project",
                "  [3] databricks  Databricks Asset Bundle",
                "  [4] ds          Data science project",
                ("Choice [1]: ", "2"),
                ("dbt project name [my_dbt_project]: ", "analytics"),
                ("Model architecture [1]: ", "2  medallion"),
                ("Warehouse adapter [1]: ", "1  duckdb"),
                "",
                "     created  analytics/dbt_project.yml",
                "     created  analytics/models/gold/gld_customers.sql",
                "     created  analytics/Makefile",
                "$ cd analytics && make install && make build",
            ],
            title="~/code",
            animate=True,
        ),
        unsafe_allow_html=True,
    )

st.markdown('<p class="lead">Install it once, globally. <b>Python 3.11+</b> and <b>uv</b> are the only requirements.</p>', unsafe_allow_html=True)
st.code("uv tool install fast-stack-forge", language="bash")


# ── What it builds ────────────────────────────────────────────────────────────
section(
    "Four kinds of project",
    "Each <code>init</code> command asks only for what you leave out. Pass every option as a flag, "
    "or add <code>-y</code> to accept the defaults, and it runs unattended in CI.",
)


def opts(values) -> str:
    return ", ".join(f"<span>{v}</span>" for v in values)


kinds = [
    ("FastAPI backend", "Entities, JWT middleware, rate limiting, a background scheduler and a WebSocket manager.",
     "init", "my_api", f"Databases: {opts(forge.DB_HELP)}"),
    ("dbt project", "Seeds, models, tests and a snapshot that pass <code>dbt build</code> out of the box.",
     "init:dbt", "analytics", f"Adapters: {opts(forge.ADAPTERS)}<br>Layouts: {opts(forge.ARCHITECTURES)}"),
    ("Databricks bundle", "An Asset Bundle with dev and prod targets, a Unity Catalog schema and a daily job.",
     "init:databricks", "lakehouse", f"Runtimes: {opts(f'{r} LTS' for r in forge.RUNTIMES)}<br>Tasks: {opts(forge.COMPONENTS)}"),
    ("Data science repo", "AstroData layout with notebooks, a Streamlit app and an optional FastAPI service.",
     "init:ds-data", "churn_study", "Options: <span>--api</span>, <span>--data</span>, licence, companion API"),
]
for col, (title, desc, cmd, example, options) in zip(st.columns(4, gap="medium"), kinds):
    with col:
        st.markdown(
            f"""<div class="kind"><h3>{title}</h3><p>{desc}</p>
<span class="cmd"><b>$</b> fast-stack-forge {cmd} {example}</span>
<div class="opts">{options}</div></div>""",
            unsafe_allow_html=True,
        )


# ── Grow an existing project ──────────────────────────────────────────────────
section("Add to an existing project", "Run these from anywhere inside a generated project. They find the project root on their own.")

grow = [
    ("make:entity", "Model, Pydantic schema, controller and router for an entity. Fields use <code>name:type[:modifier]</code>, with <code>hash</code>, <code>encrypt</code>, <code>nullable</code> and <code>fk=Model</code> modifiers."),
    ("make:service", f"An AI service and its JWT-protected router: {', '.join(f'<code>{t}</code>' for t in forge.SERVICE_TYPES)}. Providers: {', '.join(forge.PROVIDERS)}."),
    ("make:dbt", "A SQL or Python dbt model in the layer you choose, as a table, view or incremental model."),
    ("make:dashboard", "A multi-page Streamlit dashboard in <code>app/dashboard/</code>, launched with <code>make dashboard</code>."),
    ("make:sync", "An ELT script that copies MongoDB or an HTTP API into PostgreSQL or Upstash, on a schedule."),
    ("init:ds-make", "Adds a FastAPI service, a Streamlit app and Docker files to an existing data science repo."),
    ("make:discard", "Removes an entity's model, schema, controller and router."),
]
rows = "".join(f'<div class="cmd-row"><code>{name}</code><div>{desc}</div></div>' for name, desc in grow)
st.markdown(f'<div class="cmd-list">{rows}</div>', unsafe_allow_html=True)


# ── Quick start ───────────────────────────────────────────────────────────────
section("From zero to a running API")

steps = [
    ("Install the CLI", "uv tool install fast-stack-forge"),
    ("Create the backend", "fast-stack-forge init my_api --db postgresql"),
    ("Install and run it", "cd my_api && make install && make run"),
    ("Add an entity", "fast-stack-forge make:entity User name:string email:string:hash is_active:bool"),
    ("Add an AI service", "fast-stack-forge make:service HelpdeskBot --type rag --provider anthropic --vector-store qdrant"),
    ("Add analytics", "fast-stack-forge init:dbt analytics --archi medallion --adapter postgres -y"),
]
for i, (title, cmd) in enumerate(steps, 1):
    c_title, c_cmd = st.columns([2, 5], gap="small")
    with c_title:
        st.markdown(f'<div class="step"><b>{i}</b><span>{title}</span></div>', unsafe_allow_html=True)
    with c_cmd:
        st.code(cmd, language="bash")


# ── Generated structure ───────────────────────────────────────────────────────
section("What lands on disk")

trees = {
    "FastAPI": """my_api/
├── app/
│   └── main.py              FastAPI entry point, lifecycle, rate limiter
├── src/my_api/
│   ├── entity/              ORM models (SQLAlchemy or Motor)
│   ├── schema/              Pydantic models
│   ├── controller/          business logic
│   ├── router/              API routes
│   ├── service/             AI services (make:service)
│   ├── data/                database.py
│   ├── middleware/          JWTBearer
│   └── utils/               limiter, scheduling, crud_router, connection_manager
├── Makefile
├── pyproject.toml
└── .env""",
    "dbt": """analytics/                   --archi medallion --adapter duckdb
├── dbt_project.yml
├── profiles.yml             secrets read from environment variables
├── packages.yml             dbt_utils
├── models/
│   ├── bronze/              brz_customers, brz_orders, _sources.yml
│   ├── silver/              slv_customer_orders
│   ├── gold/                gld_customers
│   ├── schema.yml
│   └── exposures.yml
├── seeds/  snapshots/  tests/  macros/
├── pyproject.toml  Makefile  .env.example""",
    "Databricks": """lakehouse/
├── databricks.yml              dev (default) and prod targets
├── resources/
│   ├── schema.yml              Unity Catalog schema
│   ├── lakehouse_pipeline.yml  Lakeflow pipeline (--with pipeline)
│   └── lakehouse_job.yml       ingest → refresh_pipeline → transform → dbt
├── src/
│   ├── notebooks/ingest.py     (--with notebook)
│   ├── pipelines/              bronze / silver / gold tables
│   └── lakehouse/main.py       Python wheel (--with wheel)
├── dbt_project/                (--with dbt)
├── tests/                      pytest through Databricks Connect
├── pyproject.toml  Makefile  .env.example""",
    "Data science": """churn_study/
├── src/churn_study/
│   ├── data/  features/  models/  visualization/
│   └── api/                 FastAPI service (--api)
├── app/churn_study_app.py   Streamlit app
├── notebooks/  scripts/  docs/  tests/
├── data/                    raw, interim, processed, external (--data)
├── pyproject.toml  Makefile  .env.example
└── .pre-commit-config.yaml""",
}
for tab, (label, tree) in zip(st.tabs(list(trees)), trees.items()):
    with tab:
        st.code(tree, language="text")


# ── Requirements ──────────────────────────────────────────────────────────────
section("What you need")

reqs = [
    ("Python 3.11 or newer", "The CLI and the generated projects use modern typing."),
    ("uv", "Creates the virtual environments and installs dependencies. <code>curl -LsSf https://astral.sh/uv/install.sh | sh</code>"),
    ("A database, sometimes", "SQLite and DuckDB need nothing. PostgreSQL, MySQL and MongoDB need a running server or a cloud URI."),
    ("Databricks CLI, for bundles", "<code>make login</code> runs <code>databricks auth login</code> before you deploy."),
]
for col, (title, desc) in zip(st.columns(4, gap="medium"), reqs):
    with col:
        st.markdown(f'<div class="req"><strong>{title}</strong><span>{desc}</span></div>', unsafe_allow_html=True)

forge.footer()
