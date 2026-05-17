import streamlit as st
import subprocess, shutil, zipfile, tempfile, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from controller.sidebar import load_css, render_sidebar

ASSETS = Path(__file__).parent.parent / "assets"

def run_fastforge_cli(args, stdin_input=None, cwd=None):
    """
    Executes a fast-stack-forge command by running the Python package module
    directly via `sys.executable -m fast_stack_forge.cli`.
    This guarantees it uses the active virtual environment package containing the latest code,
    bypassing the global system command completely to prevent PATH version conflicts.
    
    If fast_stack_forge is not installed or importable, it automatically runs
    `pip install -e` on the local package directory to register it first.
    """
    # 1. Ensure the package is installed in editable mode in this python environment
    try:
        # pyrefly: ignore [missing-import]
        import fast_stack_forge
    except ImportError:
        pkg_dir = Path(__file__).parent.parent.parent / "fastforge"
        if pkg_dir.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", str(pkg_dir)], capture_output=True)
            
    # 2. Run the command using python -m
    cmd = [sys.executable, "-m", "fast_stack_forge.cli"] + args
    
    result = subprocess.run(
        cmd,
        cwd=cwd,
        input=stdin_input,
        capture_output=True,
        text=True
    )
    
    # 3. If there is a click "No such command" or import error, try updating the package and re-run
    if result.returncode != 0 and ("No such command" in result.stderr or "ModuleNotFoundError" in result.stderr):
        pkg_dir = Path(__file__).parent.parent.parent / "fastforge"
        if pkg_dir.exists():
            # Force update/re-install
            subprocess.run([sys.executable, "-m", "pip", "install", "-U", "-e", str(pkg_dir)], capture_output=True)
            # Re-run
            result = subprocess.run(
                cmd,
                cwd=cwd,
                input=stdin_input,
                capture_output=True,
                text=True
            )
            
    return result


st.set_page_config(page_title="Generate — Fast-Stack-Forge ⚡", page_icon="⚡", layout="wide")
load_css()

# ── Sidebar ──────────────────────────────────────────
render_sidebar()

st.markdown('<div class="page-title">⚡ Project Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Fill in the form, preview the commands, then download your generated project.</div>', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab_ds_data, tab_ds_make, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🚀 Init Project",
    "🔬 Init DS Project",
    "🧬 Add DS Backend",
    "🧩 Entity",
    "🌿 Init ETL",
    "📐 dbt Model",
    "🤖 AI Service",
    "🔄 Sync Script",
    "📊 Dashboard",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — fast-stack-forge init
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="info-box">🚀 <b>fast-stack-forge init</b> bootstraps a full FastAPI project with JWT auth, rate limiting, background scheduler, WebSocket manager, and a production-ready Makefile. Choose your database engine below.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        proj_name = st.text_input("Project name", value="my_project", key="init_name", help="Snake_case name for your project folder")
        db_engine = st.selectbox("Database engine", ["sqlite", "postgresql", "mysql", "mongodb"], key="init_db",
            help="sqlite → no server needed | postgresql/mysql → SQL | mongodb → NoSQL/Motor")
    with c2:
        st.markdown("### What gets generated")
        st.markdown("""
            - `app/main.py` — FastAPI entry point with lifecycle hooks
            - `src/<name>/entity/` — DB models
            - `src/<name>/schema/` — Pydantic models
            - `src/<name>/controller/` — Business logic
            - `src/<name>/router/` — API routes
            - `src/<name>/middleware/` — JWTBearer
            - `src/<name>/utils/` — limiter, scheduler, CRUD factory, WS manager
            - `pyproject.toml`, `Makefile`, `.env`
        """)

    cmd_init = f"fast-stack-forge init {proj_name} --db {db_engine}"
    st.markdown("**Generated command:**")
    st.markdown(f'<div class="cmd-box">{cmd_init}</div>', unsafe_allow_html=True)
    st.markdown("**After running:**")
    st.code(f"cd {proj_name}\nmake install\nsource .venv/bin/activate\nmake run", language="bash")

    if st.button("🚀 Generate & Download Project", key="btn_init", type="primary"):
        with st.spinner("Generating project..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                result = run_fastforge_cli(["init", proj_name, "--db", db_engine], cwd=tmpdir)
                proj_path = Path(tmpdir) / proj_name
                if result.returncode == 0 and proj_path.exists():
                    zip_path = Path(tmpdir) / f"{proj_name}.zip"
                    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                        for fp in proj_path.rglob("*"):
                            if fp.is_file():
                                zf.write(fp, fp.relative_to(tmpdir))
                    st.success(f"✅ Project `{proj_name}` generated!")
                    st.download_button("⬇️ Download ZIP", zip_path.read_bytes(),
                                       file_name=f"{proj_name}.zip", mime="application/zip")
                    with st.expander("📋 CLI output"):
                        st.code(result.stdout)
                else:
                    st.error("❌ Generation failed. Make sure Fast-Stack-Forge is installed globally via `uv tool install fast-stack-forge`")
                    st.code(result.stderr)


# ─────────────────────────────────────────────────────────────────────────────
# TAB DS DATA — fast-stack-forge init:ds-data
# ─────────────────────────────────────────────────────────────────────────────
with tab_ds_data:
    st.markdown('<div class="info-box">🔬 <b>fast-stack-forge init:ds-data</b> scaffolds a structured AstroData data science repository. Includes environment config via python-decouple and logging via loguru.</div>', unsafe_allow_html=True)
    dsc1, dsc2 = st.columns(2, gap="large")
    with dsc1:
        ds_name = st.text_input("Project name", value="my_ds_project", key="ds_name", help="Data science repository name (will be auto-sanitized)")
        
        # Flags
        ds_api = st.checkbox("Include FastAPI skeleton inside package (--api)", value=True, key="ds_api",
            help="Creates a FastAPI app inside src/<package>/api/")
        ds_data = st.checkbox("Include ETL raw/processed data folders (--data)", value=True, key="ds_data",
            help="Creates data/raw, data/interim, data/processed, and data/external folders")
        
        # Companion project
        ds_companion = st.checkbox("Create separate companion FastAPI project", value=False, key="ds_companion",
            help="Asks you to bootstrap a separate backend project alongside (named <name>_api)")
        ds_companion_db = st.selectbox("Companion DB", ["sqlite", "postgresql", "mysql", "mongodb"], key="ds_companion_db", disabled=not ds_companion)
        
        # Stdin interactive selections
        c_pymajor = sys.version_info
        py_versions = [f"{c_pymajor.major}.{c_pymajor.minor}", f"{c_pymajor.major}.{c_pymajor.minor - 1}", f"{c_pymajor.major}.{c_pymajor.minor - 2}"]
        ds_pyver = st.selectbox("Python version", py_versions, index=0, key="ds_pyver")
        
        ds_os = st.checkbox("Is this project open source?", value=True, key="ds_os")
        ds_license = st.selectbox("License", ["MIT", "BSD-3-Clause", "Apache-2.0", "GPL-3.0"], key="ds_license", disabled=not ds_os)
        
        ds_desc = st.text_input("Project description", value="", placeholder="A data science project...", key="ds_desc")
        ds_author = st.text_input("Author name", value="", key="ds_author")
        ds_email = st.text_input("Author email", value="", key="ds_email", disabled=not ds_author.strip())
        
    with dsc2:
        st.markdown("### What gets generated")
        st.markdown("""
            - `src/<package_name>/` — Package root
                - `data/`, `features/`, `models/`, `visualization/`, `front/`
                - `api/` — FastAPI skeleton (if enabled)
            - `notebooks/`, `scripts/`, `docs/`
            - `tests/` — Pytest suite
            - `app/<package_name>_app.py` — Streamlit app
            - `pyproject.toml`, `Makefile`, `.env.example`, `.pre-commit-config.yaml`
            - `docker-compose.yml`, `dockerfiles/` (if API enabled)
        """)
        
    # Build generated command representation
    api_flag = " --api" if ds_api else ""
    data_flag = " --data" if ds_data else ""
    cmd_ds_data = f"fast-stack-forge init:ds-data {ds_name}{api_flag}{data_flag}"
    
    st.markdown("**Generated CLI command (will trigger interactive prompts):**")
    st.markdown(f'<div class="cmd-box">{cmd_ds_data}</div>', unsafe_allow_html=True)
    st.markdown("**Interactive Prompts Configured:**")
    st.code(f"""Companion FastAPI project? {'Yes' if ds_companion else 'No'}
Selected DB (if companion): {ds_companion_db}
Python version: {ds_pyver}
Open Source: {'Yes' if ds_os else 'No'} (License: {ds_license if ds_os else 'Proprietary'})
Description: {ds_desc or 'A data science project: ' + ds_name}
Author: {ds_author or 'None'} (Email: {ds_email or 'None'})""", language="text")

    if st.button("🚀 Generate & Download DS Project", key="btn_ds_data", type="primary"):
        with st.spinner("Generating AstroData project..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                # Build the interactive input sequence
                stdin_lines = []
                
                # 1. Companion API
                if ds_companion:
                    stdin_lines.append("y")
                    db_idx = ["sqlite", "postgresql", "mysql", "mongodb"].index(ds_companion_db) + 1
                    stdin_lines.append(str(db_idx))
                else:
                    stdin_lines.append("n")
                
                # 2. Python version choice
                py_idx = py_versions.index(ds_pyver) + 1
                stdin_lines.append(str(py_idx))
                
                # 3. Open source
                if ds_os:
                    stdin_lines.append("y")
                    stdin_lines.append(ds_license)
                else:
                    stdin_lines.append("n")
                
                # 4. Description
                stdin_lines.append(ds_desc.strip())
                
                # 5. Author name
                stdin_lines.append(ds_author.strip())
                
                # 6. Author email
                if ds_author.strip():
                    stdin_lines.append(ds_email.strip())
                
                stdin_input_str = "\n".join(stdin_lines) + "\n"
                
                # Let's run
                args = ["init:ds-data", ds_name]
                if ds_api:
                    args.append("--api")
                if ds_data:
                    args.append("--data")
                    
                result = run_fastforge_cli(args, stdin_input=stdin_input_str, cwd=tmpdir)
                
                # Check for output folders (sanitized name)
                san_name = ds_name.strip().lower().replace(" ", "_").replace("-", "_")
                zip_path = Path(tmpdir) / f"{san_name}_ds.zip"
                
                if result.returncode == 0:
                    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                        for fp in Path(tmpdir).rglob("*"):
                            if fp.is_file() and fp != zip_path:
                                zf.write(fp, fp.relative_to(tmpdir))
                                
                    if zip_path.exists() and zip_path.stat().st_size > 100:
                        st.success(f"✅ AstroData project `{ds_name}` successfully generated!")
                        st.download_button("⬇️ Download ZIP", zip_path.read_bytes(),
                                           file_name=f"{san_name}_ds.zip", mime="application/zip")
                        with st.expander("📋 CLI output"):
                            st.code(result.stdout)
                    else:
                        st.error("❌ Generation succeeded but no files were written.")
                else:
                    st.error("❌ Generation failed. Make sure Fast-Stack-Forge is installed globally.")
                    st.code(result.stderr)


# ─────────────────────────────────────────────────────────────────────────────
# TAB DS MAKE — fast-stack-forge init:ds-make
# ─────────────────────────────────────────────────────────────────────────────
with tab_ds_make:
    st.markdown('<div class="info-box">🧬 <b>fast-stack-forge init:ds-make</b> upgrades an existing AstroData data science project by automatically injecting a FastAPI and a Streamlit dashboard skeleton, plus Docker files.</div>', unsafe_allow_html=True)
    dmc1, dmc2 = st.columns(2, gap="large")
    with dmc1:
        ds_make_dir = st.text_input("Project directory path", value=".", key="ds_make_dir",
            help="Path to the existing AstroData project root (containing src/)")
    with dmc2:
        st.markdown("### What gets added/updated")
        st.markdown("""
            - `src/<package_name>/api/` — FastAPI REST API (main, upload middleware, routes: base, system, greetings)
            - `app/<package_name>_app.py` — Pre-wired Streamlit dashboard
            - `.streamlit/config.toml` — Theme & port configuration
            - `docker-compose.yml` — Container architecture
            - `dockerfiles/Dockerfile.api` & `Dockerfile.app`
            - `tests/test_api.py` — Endpoint test suite
            - `pyproject.toml` — Appends `fastapi`, `uvicorn`, `pydantic` etc. and adds entrypoints
            - `Makefile` — Injects running targets (`run_api` and `run`)
        """)
        
    cmd_ds_make = f"fast-stack-forge init:ds-make {ds_make_dir}".strip()
    st.markdown("**Generated command:**")
    st.markdown(f'<div class="cmd-box">{cmd_ds_make}</div>', unsafe_allow_html=True)
    st.info("⚠️ Run this command inside your existing AstroData project folder where `src/` lives.")



# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — fast-stack-forge make:entity
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="info-box">🧩 <b>fast-stack-forge make:entity</b> generates the Model, Pydantic Schema, Controller, and Router for a given entity. Run this from inside a Fast-Stack-Forge project.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        ent_name = st.text_input("Entity name (PascalCase)", value="User", key="ent_name")
        no_router = st.checkbox("Skip router generation (--no-router)", key="ent_no_router")
        no_ctrl   = st.checkbox("Skip controller generation (--no-controller)", key="ent_no_ctrl")
    with c2:
        st.markdown("**Field syntax:** `name:type[:modifier]`")
        st.markdown("""
| Type | Description |
|------|-------------|
| `string` | VARCHAR / str |
| `int` | Integer |
| `float` | Float |
| `bool` | Boolean |
| `text` | Long text |
| `date` | Date only |
| `datetime` | Full timestamp |

**Modifiers:** `hash` · `encrypt` · `nullable` · `fk=ModelName`
""")

    st.markdown("**Add fields:**")
    if "ent_fields" not in st.session_state:
        st.session_state.ent_fields = [{"name": "email", "type": "string", "modifier": "hash"},
                                        {"name": "is_active", "type": "bool", "modifier": ""}]
    
    field_types = ["string","int","float","bool","text","date","datetime"]
    field_mods  = ["","hash","encrypt","nullable"]

    for i, f in enumerate(st.session_state.ent_fields):
        fc1, fc2, fc3, fc4 = st.columns([3,2,2,1])
        with fc1:
            st.session_state.ent_fields[i]["name"] = st.text_input("Name", value=f["name"], key=f"fn_{i}", label_visibility="collapsed")
        with fc2:
            idx = field_types.index(f["type"]) if f["type"] in field_types else 0
            st.session_state.ent_fields[i]["type"] = st.selectbox("Type", field_types, index=idx, key=f"ft_{i}", label_visibility="collapsed")
        with fc3:
            mod_idx = field_mods.index(f["modifier"]) if f["modifier"] in field_mods else 0
            st.session_state.ent_fields[i]["modifier"] = st.selectbox("Modifier", field_mods, index=mod_idx, key=f"fm_{i}", label_visibility="collapsed")
        with fc4:
            if st.button("🗑️", key=f"fdel_{i}") and len(st.session_state.ent_fields) > 1:
                st.session_state.ent_fields.pop(i); st.rerun()

    if st.button("➕ Add field", key="add_field"):
        st.session_state.ent_fields.append({"name": "field", "type": "string", "modifier": ""}); st.rerun()

    fields_str = " ".join(
        f"{f['name']}:{f['type']}" + (f":{f['modifier']}" if f['modifier'] else "")
        for f in st.session_state.ent_fields if f["name"]
    )
    flags = ("--no-router " if no_router else "") + ("--no-controller" if no_ctrl else "")
    cmd_ent = f"fast-stack-forge make:entity {ent_name} {fields_str} {flags}".strip()
    st.markdown("**Generated command:**")
    st.markdown(f'<div class="cmd-box">{cmd_ent}</div>', unsafe_allow_html=True)
    st.info("⚠️ Run this command from the **root of your Fast-Stack-Forge project** (where `src/` lives).")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — fast-stack-forge init:etl
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="info-box">🌿 <b>fast-stack-forge init:etl</b> scaffolds a complete dbt project inside your Fast-Stack-Forge project, with your chosen architecture and data warehouse connector.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        etl_name = st.text_input("dbt project name", value="my_project_etl", key="etl_name")
        etl_archi = st.selectbox("Architecture style", ["medallion","default","star"], key="etl_archi",
            help="medallion → bronze/silver/gold | default → stg/int/mart | star → raw/dim/fact")
        etl_conn  = st.selectbox("Warehouse connector", ["postgres","local","snowflake","bigquery"], key="etl_conn",
            help="local → DuckDB (no server) | postgres → Supabase/RDS | snowflake/bigquery → cloud DWH")
    with c2:
        layers = {"medallion": ["bronze","silver","gold"], "default": ["stg","int","mart"], "star": ["raw","dim","fact"]}
        lyr = layers[etl_archi]
        st.markdown(f"**Layers generated for `{etl_archi}`:**")
        for l in lyr:
            st.markdown(f"- `models/{l}/`")
        st.markdown("**Also includes:** `dbt_project.yml`, `profiles.yml`, `packages.yml`, `schema.yml`, `exposures.yml`, snapshots, seeds, macros")
        if etl_conn == "local":
            st.markdown("📦 **Install:** `uv pip install dbt-duckdb`")
        elif etl_conn == "postgres":
            st.markdown("📦 **Install:** `uv pip install dbt-postgres`")
        elif etl_conn == "snowflake":
            st.markdown("📦 **Install:** `uv pip install dbt-snowflake`")
        elif etl_conn == "bigquery":
            st.markdown("📦 **Install:** `uv pip install dbt-bigquery`")

    cmd_etl = f"fast-stack-forge init:etl {etl_name} --archi {etl_archi} --connector {etl_conn}"
    st.markdown("**Generated command:**")
    st.markdown(f'<div class="cmd-box">{cmd_etl}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — fast-stack-forge make:dbt
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="info-box">📐 <b>fast-stack-forge make:dbt</b> quickly scaffolds a single dbt model (SQL or Python) inside an existing ETL project.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        dbt_model = st.text_input("Model name (snake_case)", value="fact_orders", key="dbt_model")
        dbt_layer = st.text_input("Layer (e.g. bronze, silver, mart)", value="silver", key="dbt_layer")
        dbt_view  = st.checkbox("Materialize as view (--view)", key="dbt_view")
        dbt_incr  = st.checkbox("Incremental model (--incremental)", key="dbt_incr")
        dbt_py    = st.checkbox("Python model (--python)", key="dbt_py")
    with c2:
        st.markdown("**Examples:**")
        st.code("fast-stack-forge make:dbt stg_users --layer stg\nfast-stack-forge make:dbt fact_revenue --view --layer mart\nfast-stack-forge make:dbt ml_features --python --incremental --layer gold", language="bash")

    flags_dbt = []
    if dbt_view: flags_dbt.append("--view")
    if dbt_incr: flags_dbt.append("--incremental")
    if dbt_py:   flags_dbt.append("--python")
    if dbt_layer: flags_dbt.append(f"--layer {dbt_layer}")
    cmd_dbt = f"fast-stack-forge make:dbt {dbt_model} {' '.join(flags_dbt)}".strip()
    st.markdown("**Generated command:**")
    st.markdown(f'<div class="cmd-box">{cmd_dbt}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — fast-stack-forge make:service
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="info-box">🤖 <b>fast-stack-forge make:service</b> generates a production-ready AI service and its FastAPI router. It auto-installs provider/vector-store hints.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        svc_name = st.text_input("Service name (PascalCase)", value="HelpdeskBot", key="svc_name")
        svc_type = st.selectbox("Service type", ["rag","agent","agentic","ocr"], key="svc_type",
            help="rag → RAG with vector store | agent → tool-calling | agentic → LangGraph | ocr → Vision/extraction")
        svc_prov = st.selectbox("AI Provider", ["openai","anthropic","mistral","gemini","azure"], key="svc_prov")
        svc_vec  = st.selectbox("Vector store (RAG only)", ["chroma","qdrant","supabase","upstash"], key="svc_vec",
            disabled=(svc_type != "rag"))
    with c2:
        st.markdown("**What gets generated:**")
        st.markdown(f"""
- `src/<project>/service/{svc_name.lower()}.py` — AI service class
- `src/<project>/router/r_{svc_name.lower()}.py` — FastAPI router with `POST /{svc_name.lower()}` endpoint (JWT protected)
- `app/main.py` updated with the new router import

**Required packages will be shown after generation.**
""")
        type_desc = {
            "rag": "Retrieval-Augmented Generation — chunks documents, embeds them in a vector store, retrieves context for LLM answers.",
            "agent": "Tool-calling agent — LLM with access to defined tools/functions.",
            "agentic": "LangGraph workflow — stateful multi-step agent with a state graph.",
            "ocr": "Vision/OCR extraction — send images or PDFs, extract structured data.",
        }
        st.info(type_desc.get(svc_type, ""))

    vs_part = f" --vector-store {svc_vec}" if svc_type == "rag" else ""
    cmd_svc = f"fast-stack-forge make:service {svc_name} --type {svc_type} --provider {svc_prov}{vs_part}"
    st.markdown("**Generated command:**")
    st.markdown(f'<div class="cmd-box">{cmd_svc}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — fast-stack-forge make:sync
# ─────────────────────────────────────────────────────────────────────────────
with tab6:
    st.markdown('<div class="info-box">🔄 <b>fast-stack-forge make:sync</b> scaffolds a Python ELT script that replicates data from a source DB to a destination. Includes APScheduler for continuous execution.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        sync_name = st.text_input("Sync script name (PascalCase)", value="MongoToPg", key="sync_name")
        sync_src  = st.selectbox("Source database", ["mongodb","postgresql","mysql","sqlite"], key="sync_src")
        sync_dst  = st.selectbox("Destination database", ["postgres","mysql","sqlite","bigquery"], key="sync_dst")
    with c2:
        st.markdown("**Generated files:**")
        st.markdown(f"""
- `src/<project>/sync/{sync_name.lower()}.py` — Sync script with APScheduler
- `src/<project>/sync/requirements.txt` — pymongo, pandas, sqlalchemy, apscheduler…
""")
        st.markdown("**Install and run:**")
        st.code(f"cd src/<project>/sync\nuv pip install -r requirements.txt\npython {sync_name.lower()}.py", language="bash")

    cmd_sync = f"fast-stack-forge make:sync {sync_name} --source {sync_src} --dest {sync_dst}"
    st.markdown("**Generated command:**")
    st.markdown(f'<div class="cmd-box">{cmd_sync}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — fast-stack-forge make:dashboard
# ─────────────────────────────────────────────────────────────────────────────
with tab7:
    st.markdown('<div class="info-box">📊 <b>fast-stack-forge make:dashboard</b> generates a multi-page Streamlit dashboard inside <code>app/dashboard/</code> and updates your Makefile with <code>make dashboard</code>.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("**Add dashboard pages:**")
        preset_pages = st.multiselect(
            "Choose preset pages",
            ["Atelier","Analytics","Chatbot"],
            default=["Atelier","Analytics"],
            key="dash_pages",
            help="Atelier → entity/service manager | Analytics → charts | Chatbot → AI chat UI"
        )
        custom_pages = st.text_input("Additional custom pages (comma-separated)", value="", key="dash_custom",
            help="e.g. Reports, Settings, Users")
        all_pages = list(preset_pages)
        if custom_pages.strip():
            all_pages += [p.strip() for p in custom_pages.split(",") if p.strip()]
    with c2:
        st.markdown("**Pages that will be generated:**")
        for i, p in enumerate(all_pages, 1):
            st.markdown(f"- `{i}_{p}.py`")
        st.markdown("**Launch after generation:**")
        st.code("make dashboard", language="bash")

    pages_str = " ".join(all_pages)
    cmd_dash = f"fast-stack-forge make:dashboard {pages_str}"
    st.markdown("**Generated command:**")
    st.markdown(f'<div class="cmd-box">{cmd_dash}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#4a5568;font-size:0.82rem'>⚡ Fast-Stack-Forge · by <a href='https://savantech.org' style='color:#06b6d4'>SavanTech</a> · <a href='mailto:savantech25@gmail.com' style='color:#06b6d4'>savantech25@gmail.com</a></div>", unsafe_allow_html=True)
