import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from controller.sidebar import load_css, render_sidebar
from controller import forge

st.set_page_config(page_title="Generate · fast-stack-forge", page_icon="⚡", layout="wide")
load_css()
render_sidebar()
forge.require_package()

forge.page_header(
    "Generate a project",
    "Fill in the options and download the project the CLI builds, or copy the command and run it yourself.",
)


def lead(text: str) -> None:
    st.markdown(f'<p class="lead">{text}</p>', unsafe_allow_html=True)


def label(text: str) -> None:
    st.markdown(f'<div class="panel-label">{text}</div>', unsafe_allow_html=True)


def note(text: str) -> None:
    st.markdown(f'<div class="note">{text}</div>', unsafe_allow_html=True)


# How the answers (keyed by a fragment of the CLI question) are shown in the terminal
QUESTION_NAMES = {
    "companion FastAPI backend": "Separate FastAPI project",
    "Database for the FastAPI project": "Its database",
    "open source": "Open source",
    "License": "Licence",
    "Short description": "Description",
    "Project description": "Description",
    "Author name": "Author",
    "SQL warehouse name": "SQL warehouse",
    "dbt model architecture": "dbt model layout",
}


def command_panel(args: list, answers: dict = None, then: list = None) -> None:
    """Terminal with the command, the answers to the questions it asks, and what to run next."""
    lines = [f"$ {forge.command_line(args)}"]
    for question, reply in (answers or {}).items():
        if isinstance(reply, bool):
            reply = "yes" if reply else "no"
        lines.append((f"? {QUESTION_NAMES.get(question, question)}: ", str(reply) or "(blank)"))
    lines += [f"$ {cmd}" for cmd in then or []]
    forge.show_terminal(lines)


mode = st.segmented_control(
    "What are you doing?", ["Start a new project", "Add to an existing project"],
    default="Start a new project", key="mode", label_visibility="collapsed",
) or "Start a new project"


# ═════════════════════════════════════════════════════════════════════════════
# New projects: generated here and downloaded as a ZIP
# ═════════════════════════════════════════════════════════════════════════════
if mode == "Start a new project":
    t_api, t_dbt, t_dbx, t_ds = st.tabs(["FastAPI backend", "dbt project", "Databricks bundle", "Data science repo"])

    # ── fast-stack-forge init ────────────────────────────────────────────────
    with t_api:
        lead("<b>init</b> creates a FastAPI backend with JWT middleware, rate limiting, a background scheduler, "
             "a WebSocket manager and a generic CRUD router.")
        form, out = st.columns([5, 6], gap="large")
        with form:
            api_name = st.text_input("Project name", "my_api", key="api_name", help="Turned into a valid Python package name")
            api_db = st.radio("Database", list(forge.DB_HELP), key="api_db", horizontal=True)
            st.caption(forge.DB_HELP[api_db])
        with out:
            name = forge.sanitize_name(api_name) or "my_api"
            args = ["init", name, "--db", api_db]
            label("Command")
            command_panel(args, then=[f"cd {name} && make install && make run"])
            forge.generate_section("api", args, {}, name, "Generate FastAPI project")

    # ── fast-stack-forge init:dbt ────────────────────────────────────────────
    with t_dbt:
        lead("<b>init:dbt</b> creates a standalone dbt project with a <code>profiles.yml</code> that reads its secrets "
             "from environment variables. With the examples, <code>make build</code> passes on the first run.")
        form, out = st.columns([5, 6], gap="large")
        with form:
            dbt_name = st.text_input("Project name", "analytics", key="dbt_name")
            c1, c2 = st.columns(2)
            with c1:
                dbt_archi = st.selectbox("Model layout", list(forge.ARCHITECTURES), key="dbt_archi",
                                         format_func=lambda k: f"{k} · {' → '.join(forge.ARCHITECTURES[k]['layers'])}")
            with c2:
                dbt_adapter = st.selectbox("Warehouse adapter", list(forge.ADAPTERS), key="dbt_adapter",
                                           format_func=lambda k: f"{k} · {forge.ADAPTERS[k]['help']}")
            dbt_examples = st.checkbox("Example seeds, models, tests and snapshot", True, key="dbt_examples")
            py_ok = forge.ADAPTERS[dbt_adapter]["python_models"] and dbt_examples
            dbt_python = st.checkbox(
                "Example dbt Python model", dbt_adapter == "duckdb", key="dbt_python", disabled=not py_ok,
                help="Available with the examples on DuckDB, Snowflake and Databricks",
            )
            c1, c2 = st.columns([1, 2])
            with c1:
                dbt_py = st.selectbox("Python version", forge.DBT_PYTHON_VERSIONS, key="dbt_py")
            with c2:
                dbt_desc = st.text_input("Description", "", key="dbt_desc", placeholder="Optional")
        with out:
            name = forge.sanitize_name(dbt_name) or "my_dbt_project"
            args = ["init:dbt", name, "--archi", dbt_archi, "--adapter", dbt_adapter,
                    "--examples" if dbt_examples else "--no-examples",
                    "--python-model" if dbt_python and py_ok else "--no-python-model"]
            answers = {"Python version": dbt_py, "Short description": dbt_desc}
            label("Command")
            command_panel(args, answers, then=[f"cd {name} && make install && make build"])
            layers = forge.ARCHITECTURES[dbt_archi]["layers"]
            st.caption(f"Models go in {', '.join(f'models/{l}/' for l in layers)}. "
                       f"Installs dbt-core and {forge.ADAPTERS[dbt_adapter]['package']}.")
            forge.generate_section("dbt", args, answers, name, "Generate dbt project")

    # ── fast-stack-forge init:databricks ─────────────────────────────────────
    with t_dbx:
        lead("<b>init:databricks</b> creates a Databricks Asset Bundle: dev and prod targets, a Unity Catalog schema "
             "and a daily job made of the tasks you pick. Tests run locally through Databricks Connect.")
        form, out = st.columns([5, 6], gap="large")
        with form:
            dbx_name = st.text_input("Project name", "lakehouse", key="dbx_name")
            dbx_host = st.text_input("Workspace URL", "https://<your-workspace>.cloud.databricks.com", key="dbx_host")
            c1, c2 = st.columns(2)
            with c1:
                dbx_catalog = st.text_input("Unity Catalog catalog", "main", key="dbx_catalog")
            with c2:
                dbx_runtime = st.selectbox(
                    "Runtime", list(forge.RUNTIMES), key="dbx_runtime",
                    format_func=lambda k: f"{forge.RUNTIMES[k]['label']} · Python {forge.RUNTIMES[k]['python']}",
                )
            c1, c2 = st.columns(2)
            with c1:
                dbx_compute = st.radio("Compute", ["serverless", "classic"], key="dbx_compute", horizontal=True,
                                       help="Serverless needs no cluster. Classic uses a job cluster.")
            with c2:
                dbx_cloud = st.selectbox("Cloud", list(forge.NODE_TYPES), key="dbx_cloud",
                                         disabled=dbx_compute != "classic",
                                         format_func=lambda k: f"{k} · {forge.NODE_TYPES[k]}")
            dbx_with = st.multiselect(
                "Job tasks", list(forge.COMPONENTS), default=["wheel", "notebook"], key="dbx_with",
                format_func=lambda k: f"{k}: {forge.COMPONENTS[k]}",
            )
            if not dbx_with:
                st.caption("Nothing picked: the CLI adds the Python wheel task.")
            if "dbt" in dbx_with:
                c1, c2 = st.columns(2)
                with c1:
                    dbx_wh = st.text_input("SQL warehouse for dbt", "Serverless Starter Warehouse", key="dbx_wh")
                with c2:
                    dbx_archi = st.selectbox("dbt model layout", list(forge.ARCHITECTURES), index=1, key="dbx_archi")
            dbx_desc = st.text_input("Description", "", key="dbx_desc", placeholder="Optional")
        with out:
            name = forge.sanitize_name(dbx_name) or "my_databricks_project"
            args = ["init:databricks", name, "--host", dbx_host.strip(), "--catalog", dbx_catalog.strip() or "main",
                    "--compute", dbx_compute, "--runtime", dbx_runtime]
            if dbx_compute == "classic":
                args += ["--cloud", dbx_cloud]
            for component in dbx_with or ["wheel"]:
                args += ["--with", component]
            answers = {"Short description": dbx_desc}
            if "dbt" in dbx_with:
                answers = {"SQL warehouse name": dbx_wh, "dbt model architecture": dbx_archi, **answers}
            label("Command")
            command_panel(args, answers, then=[f"cd {name}", "make login && make install", "make deploy && make run"])
            forge.generate_section("dbx", args, answers, name, "Generate Databricks bundle")

    # ── fast-stack-forge init:ds-data ────────────────────────────────────────
    with t_ds:
        lead("<b>init:ds-data</b> creates an AstroData data science repo: notebooks, a Streamlit app, "
             "config with python-decouple and logging with loguru.")
        form, out = st.columns([5, 6], gap="large")
        with form:
            ds_name = st.text_input("Project name", "churn_study", key="ds_name")
            ds_api = st.checkbox("FastAPI service inside the package (src/<name>/api)", True, key="ds_api")
            ds_data = st.checkbox("Data folders: raw, interim, processed, external", True, key="ds_data")
            c1, c2 = st.columns(2)
            with c1:
                ds_companion = st.checkbox("Separate API project", False, key="ds_companion",
                                           help="Creates <name>_api next to the repo, with its own database")
            with c2:
                ds_companion_db = st.selectbox("Its database", forge.DB_CHOICES, key="ds_companion_db",
                                               disabled=not ds_companion)
            py_versions = forge.get_python_versions()
            c1, c2 = st.columns(2)
            with c1:
                ds_pyver = st.selectbox("Python version", py_versions, key="ds_pyver")
            with c2:
                ds_license = st.selectbox("Licence", [*forge.LICENSES, "Proprietary"], key="ds_license")
            ds_desc = st.text_input("Description", "", key="ds_desc", placeholder="Optional")
            c1, c2 = st.columns(2)
            with c1:
                ds_author = st.text_input("Author", "", key="ds_author", placeholder="Optional")
            with c2:
                ds_email = st.text_input("Author email", "", key="ds_email", disabled=not ds_author.strip())
        with out:
            name = forge.sanitize_name(ds_name) or "my_ds_project"
            args = ["init:ds-data", name, "--api" if ds_api else "--no-api", "--data" if ds_data else "--no-data"]
            open_source = ds_license != "Proprietary"
            answers = {"companion FastAPI backend": ds_companion}
            if ds_companion:
                answers["Database for the FastAPI project"] = ds_companion_db
            answers |= {"Python version": ds_pyver, "open source": open_source}
            if open_source:
                answers["License"] = ds_license
            answers |= {"Project description": ds_desc.strip(), "Author name": ds_author.strip()}
            if ds_author.strip():
                answers["Author email"] = ds_email.strip()
            label("Command")
            command_panel(args, answers, then=[f"cd {name} && make install"])
            forge.generate_section("ds", args, answers, name, "Generate data science repo")


# ═════════════════════════════════════════════════════════════════════════════
# Existing projects: the command to run from the project root
# ═════════════════════════════════════════════════════════════════════════════
else:
    note("These commands change files in a project you already have, so copy them and run them "
         "from anywhere inside that project.")
    t_ent, t_svc, t_mdl, t_dash, t_sync, t_dsm, t_rm = st.tabs(
        ["Entity", "AI service", "dbt model", "Dashboard", "Sync script", "DS backend", "Remove an entity"]
    )

    # ── make:entity ──────────────────────────────────────────────────────────
    with t_ent:
        lead("<b>make:entity</b> writes the model, the Pydantic schema, the controller and the router for an entity, "
             "and registers the router in <code>app/main.py</code>.")
        form, out = st.columns([6, 5], gap="large")
        with form:
            ent_name = st.text_input("Entity name", "User", key="ent_name", help="PascalCase, e.g. Invoice")
            fields = st.data_editor(
                [
                    {"name": "name", "type": "string", "modifier": None, "fk": None},
                    {"name": "email", "type": "string", "modifier": "hash", "fk": None},
                    {"name": "is_active", "type": "bool", "modifier": None, "fk": None},
                ],
                key="ent_fields", num_rows="dynamic",
                column_config={
                    "name": st.column_config.TextColumn("Field", required=True),
                    "type": st.column_config.SelectboxColumn(
                        "Type", options=["string", "int", "float", "bool", "text", "date", "datetime"],
                        default="string", required=True),
                    "modifier": st.column_config.SelectboxColumn(
                        "Modifier", options=["hash", "encrypt", "nullable"]),
                    "fk": st.column_config.TextColumn("Foreign key to", help="Model name, e.g. Role"),
                },
            )
            c1, c2 = st.columns(2)
            with c1:
                no_router = st.checkbox("Skip the router", key="ent_no_router")
            with c2:
                no_ctrl = st.checkbox("Skip the controller", key="ent_no_ctrl")
        with out:
            tokens = []
            for f in fields:
                if not (f.get("name") or "").strip():
                    continue
                parts = [f["name"].strip(), f.get("type") or "string"]
                if f.get("modifier"):
                    parts.append(f["modifier"])
                if (f.get("fk") or "").strip():
                    parts.append(f"fk={f['fk'].strip()}")
                tokens.append(":".join(parts))
            args = ["make:entity", ent_name.strip() or "Entity", *tokens]
            args += ["--no-router"] if no_router else []
            args += ["--no-controller"] if no_ctrl else []
            label("Command")
            command_panel(args)
            st.caption("Hashed fields are stored with bcrypt; encrypted fields with Fernet, using FERNET_KEY from .env.")

    # ── make:service ─────────────────────────────────────────────────────────
    with t_svc:
        lead("<b>make:service</b> adds an AI service and its JWT-protected router, puts the dependencies in "
             "<code>pyproject.toml</code> and the settings in <code>.env</code>.")
        svc_info = {
            "rag": ("Answers from your documents: chunking, vector search, sources in the answer.",
                    "POST /{n}  {query}   ·   POST /{n}/ingest   ·   POST /{n}/refresh"),
            "agent": ("Tool-calling agent (LangChain create_agent) with memory per session.",
                      "POST /{n}  {query, session_id}"),
            "agentic": ("An explicit LangGraph workflow, an LLM ↔ tools loop you extend with your own nodes.",
                        "POST /{n}  {query, session_id}"),
            "ocr": ("Text extraction from an uploaded image or PDF, returned as Markdown.",
                    "POST /{n}  multipart field 'file'"),
        }
        form, out = st.columns([5, 6], gap="large")
        with form:
            svc_name = st.text_input("Service name", "HelpdeskBot", key="svc_name")
            svc_type = st.radio("Type", forge.SERVICE_TYPES, key="svc_type", horizontal=True)
            st.caption(svc_info[svc_type][0])
            c1, c2 = st.columns(2)
            with c1:
                svc_prov = st.selectbox("Provider", forge.PROVIDERS, key="svc_prov")
            with c2:
                svc_vec = st.selectbox("Vector store", forge.VECTOR_STORES, key="svc_vec",
                                       disabled=svc_type != "rag", help="RAG services only")
            if svc_type == "rag" and svc_prov == "anthropic":
                note("Anthropic has no embeddings API, so this RAG service embeds with Voyage AI (VOYAGE_API_KEY).")
        with out:
            args = ["make:service", svc_name.strip() or "Service", "--type", svc_type, "--provider", svc_prov]
            if svc_type == "rag":
                args += ["--vector-store", svc_vec]
            label("Command")
            command_panel(args, then=["uv sync"])
            st.caption(f"Endpoint: {svc_info[svc_type][1].replace('{n}', (svc_name.strip() or 'service').lower())}. "
                       "Fill in the API keys in .env; models are set there too.")

    # ── make:dbt ─────────────────────────────────────────────────────────────
    with t_mdl:
        lead("<b>make:dbt</b> adds one model to a dbt project, in the layer folder you name.")
        form, out = st.columns([5, 6], gap="large")
        with form:
            mdl_name = st.text_input("Model name", "fct_orders", key="mdl_name")
            mdl_layer = st.text_input("Layer folder", "gold", key="mdl_layer", help="e.g. staging, silver, marts")
            mdl_lang = st.radio("Language", ["SQL", "Python"], key="mdl_lang", horizontal=True)
            mdl_mat = st.radio("Materialization", ["table", "view", "incremental"], key="mdl_mat", horizontal=True,
                               help="Python models can't be views; the CLI uses a table instead")
        with out:
            args = ["make:dbt", mdl_name.strip() or "model"]
            if mdl_mat == "view":
                args.append("--view")
            if mdl_mat == "incremental":
                args.append("--incremental")
            if mdl_lang == "Python":
                args.append("--python")
            if mdl_layer.strip():
                args += ["--layer", mdl_layer.strip()]
            label("Command")
            command_panel(args, then=["uv run dbt build --select " + (mdl_name.strip() or "model")])

    # ── make:dashboard ───────────────────────────────────────────────────────
    with t_dash:
        lead("<b>make:dashboard</b> writes a multi-page Streamlit dashboard in <code>app/dashboard/</code> "
             "and adds a <code>dashboard</code> target to the Makefile.")
        page_icons = {"Atelier": "🏗️", "Analytics": "📊", "Chatbot": "🤖"}
        form, out = st.columns([5, 6], gap="large")
        with form:
            dash_presets = st.multiselect("Ready-made pages", list(page_icons), default=["Atelier", "Analytics"],
                                          key="dash_pages", help="Atelier manages entities, services and dbt models")
            dash_custom = st.text_input("More pages", "", key="dash_custom", placeholder="Reports, Settings")
            pages = dash_presets + [p.strip() for p in dash_custom.split(",") if p.strip()]
        with out:
            args = ["make:dashboard", *pages]
            label("Command")
            command_panel(args, then=["make dashboard"])
            files = [f"{i}_{page_icons.get(p, '📄')}_{p}.py" for i, p in enumerate(pages or ["Atelier"], 1)]
            st.caption("Pages: " + ", ".join(files))

    # ── make:sync ────────────────────────────────────────────────────────────
    with t_sync:
        lead("<b>make:sync</b> writes an ELT script that copies data into your analytics store on a schedule "
             "(APScheduler), flattening nested documents with pandas.")
        form, out = st.columns([5, 6], gap="large")
        with form:
            sync_name = st.text_input("Script name", "MongoToPg", key="sync_name")
            c1, c2 = st.columns(2)
            with c1:
                sync_src = st.selectbox("Source", ["mongodb", "api"], key="sync_src")
            with c2:
                sync_dst = st.selectbox("Destination", ["postgres", "upstash"], key="sync_dst")
        with out:
            name = sync_name.strip() or "Sync"
            args = ["make:sync", name, "--source", sync_src, "--dest", sync_dst]
            label("Command")
            command_panel(args, then=[f"cd src/<package>/sync && uv pip install -r requirements.txt",
                                      f"python {name.lower()}.py"])

    # ── init:ds-make ─────────────────────────────────────────────────────────
    with t_dsm:
        lead("<b>init:ds-make</b> adds a FastAPI service, a Streamlit app, Docker files and API tests to an "
             "existing AstroData repo. It finds the package in <code>src/</code> by itself.")
        form, out = st.columns([5, 6], gap="large")
        with form:
            dsm_dir = st.text_input("Project folder", ".", key="dsm_dir", help="Leave '.' when you run it from the repo root")
        with out:
            args = ["init:ds-make"] + ([dsm_dir.strip()] if dsm_dir.strip() not in ("", ".") else [])
            label("Command")
            command_panel(args, then=["make install"])
            st.caption("Adds src/<package>/api/, app/<package>_app.py, .streamlit/config.toml, docker-compose.yml, "
                       "dockerfiles/ and tests/test_api.py, and new Makefile targets.")

    # ── make:discard ─────────────────────────────────────────────────────────
    with t_rm:
        lead("<b>make:discard</b> deletes an entity's model, schema, controller and router.")
        form, out = st.columns([5, 6], gap="large")
        with form:
            rm_name = st.text_input("Entity name", "User", key="rm_name")
        with out:
            label("Command")
            command_panel(["make:discard", rm_name.strip() or "Entity"])
            note("Commit your work first: the files are deleted, not moved.")

forge.footer()
