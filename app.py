import streamlit as st
import pandas as pd
from utils.db_loader import load_file_to_sqlite, get_table_info
from utils.chart_generator import generate_chart
from utils.insight_generator import generate_insight
from agent.sql_agent import get_sql_agent, ask_agent

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Smart Data Analyst",
    page_icon="📊",
    layout="wide"
)

# ── Session state defaults ────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "engine" not in st.session_state:
    st.session_state.engine = None
if "table_name" not in st.session_state:
    st.session_state.table_name = None
if "columns" not in st.session_state:
    st.session_state.columns = None
if "df_preview" not in st.session_state:
    st.session_state.df_preview = None
if "agent" not in st.session_state:
    st.session_state.agent = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None

# ── Helper to load any file path ─────────────────────────
def load_dataset(file_path, display_name):
    with open(file_path, "rb") as f:
        import io
        content = f.read()
    file_obj = io.BytesIO(content)
    file_obj.name = display_name
    engine, table_name = load_file_to_sqlite(file_obj)
    info = get_table_info(engine, table_name)
    st.session_state.engine = engine
    st.session_state.table_name = table_name
    st.session_state.columns = info["columns"]
    st.session_state.file_name = display_name
    st.session_state.df_preview = pd.DataFrame(
        info["sample_rows"],
        columns=info["columns"]
    )
    st.session_state.agent = get_sql_agent(
        table_name=table_name,
        columns=info["columns"]
    )
    st.session_state.messages = []

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.title("📊 Smart Data Analyst")
    st.markdown("Ask questions about your data in plain English. Get answers, charts, and insights instantly.")
    st.divider()

    # Sample datasets
    st.markdown("**Try a sample dataset:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛒 Sales", use_container_width=True):
            with st.spinner("Loading..."):
                load_dataset("data/samples/indian_sales.csv", "indian_sales.csv")
            st.rerun()
    with col2:
        if st.button("👥 HR", use_container_width=True):
            with st.spinner("Loading..."):
                load_dataset("data/samples/hr_analytics.csv", "hr_analytics.csv")
            st.rerun()
    with col3:
        if st.button("📦 Orders", use_container_width=True):
            with st.spinner("Loading..."):
                load_dataset("data/samples/ecommerce_orders.csv", "ecommerce_orders.csv")
            st.rerun()

    st.divider()

    # File upload
    st.markdown("**Or upload your own file:**")
    uploaded_file = st.file_uploader(
        "CSV or Excel",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        with st.spinner("Loading your file..."):
            engine, table_name = load_file_to_sqlite(uploaded_file)
            info = get_table_info(engine, table_name)
            st.session_state.engine = engine
            st.session_state.table_name = table_name
            st.session_state.columns = info["columns"]
            st.session_state.file_name = uploaded_file.name
            st.session_state.df_preview = pd.DataFrame(
                info["sample_rows"],
                columns=info["columns"]
            )
            st.session_state.agent = get_sql_agent(
                table_name=table_name,
                columns=info["columns"]
            )
            st.session_state.messages = []
        st.success(f"✅ Loaded: {uploaded_file.name}")

    # Show loaded dataset info
    if st.session_state.file_name:
        st.divider()
        st.markdown(f"**Loaded:** {st.session_state.file_name}")
        if st.session_state.columns:
            st.markdown(f"**Columns:** {', '.join(st.session_state.columns)}")

    st.divider()

    # Example questions
    st.markdown("**Example questions:**")
    st.markdown("- What is the total revenue?")
    st.markdown("- Show me revenue by region")
    st.markdown("- Which product performed best?")
    st.markdown("- Compare sales by city")

    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Main area ─────────────────────────────────────────────
st.title("Smart Data Analyst 📊")
st.markdown("Upload your data or try a sample dataset — then ask anything in plain English.")

if st.session_state.df_preview is not None:
    # Stats cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Dataset", st.session_state.file_name or "Uploaded file")
    with col2:
        st.metric("Columns", len(st.session_state.columns))
    with col3:
        st.metric("Preview rows", len(st.session_state.df_preview))

    st.subheader("Data Preview")
    st.dataframe(st.session_state.df_preview, use_container_width=True)
    st.divider()
else:
    st.info("👈 Click a sample dataset or upload your own file to get started.")

# ── Chat history ──────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "chart" in message and message["chart"] is not None:
            st.plotly_chart(message["chart"], use_container_width=True)
        if "insight" in message and message["insight"] is not None:
            st.success(f"💡 **Insight:** {message['insight']}")

# ── Chat input ────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about your data..."):
    if st.session_state.agent is None:
        st.warning("⚠️ Please load a dataset first.")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "chart": None,
            "insight": None
        })
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_agent(
                    st.session_state.agent,
                    prompt,
                    chat_history=st.session_state.messages[:-1]
                )
                fig = generate_chart(
                    st.session_state.engine,
                    st.session_state.table_name,
                    prompt,
                    st.session_state.columns
                )
                insight = generate_insight(prompt, answer)

            st.markdown(answer)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
            if insight is not None:
                st.success(f"💡 **Insight:** {insight}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "chart": fig,
            "insight": insight
        })