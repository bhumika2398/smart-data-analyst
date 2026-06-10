import pandas as pd
import plotly.express as px
from sqlalchemy import text


def detect_chart_type(question):
    """
    Detects what type of chart to draw based on keywords
    in the user's question. Returns None if no chart needed.
    """
    q = question.lower()

    line_keywords = ["trend", "over time", "over months", "monthly",
                     "by month", "by year", "growth", "change over"]
    bar_keywords = ["by region", "by product", "by category", "compare",
                    "comparison", "breakdown", "each", "per region",
                    "per product", "show me", "revenue by", "sales by"]
    pie_keywords = ["share", "percentage", "proportion", "distribution",
                    "pie", "composition"]

    for kw in line_keywords:
        if kw in q:
            return "line"
    for kw in pie_keywords:
        if kw in q:
            return "pie"
    for kw in bar_keywords:
        if kw in q:
            return "bar"

    return None


def get_chart_data(engine, table_name, question, columns):
    """
    Runs a SQL query based on the question to get data
    for the chart. Returns a DataFrame or None.
    """
    q = question.lower()
    numeric_col = None
    group_col = None

    # Find the numeric column to aggregate
    for col in columns:
        if any(word in col for word in ["revenue", "sales", "amount",
                                         "price", "cost", "profit", "total"]):
            numeric_col = col
            break

    # Find the grouping column based on question keywords
    for col in columns:
        if col == numeric_col:
            continue
        if any(word in q for word in [col, col.replace("_", " ")]):
            group_col = col
            break

    # Fallback: pick first non-numeric column as group
    if not group_col:
        for col in columns:
            if col != numeric_col:
                group_col = col
                break

    if not numeric_col or not group_col:
        return None, None, None

    sql = f"""
        SELECT {group_col}, SUM({numeric_col}) as total
        FROM {table_name}
        GROUP BY {group_col}
        ORDER BY total DESC
    """

    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(sql), conn)
        return df, group_col, "total"
    except Exception:
        return None, None, None


def generate_chart(engine, table_name, question, columns):
    """
    Main function: detects chart type, gets data, returns
    a Plotly figure or None if no chart is needed.
    """
    chart_type = detect_chart_type(question)
    if not chart_type:
        return None

    df, x_col, y_col = get_chart_data(engine, table_name, question, columns)
    if df is None or df.empty:
        return None

    title = f"{y_col.replace('_', ' ').title()} by {x_col.replace('_', ' ').title()}"

    if chart_type == "bar":
        fig = px.bar(
            df, x=x_col, y=y_col,
            title=title,
            color=x_col,
            labels={x_col: x_col.replace("_", " ").title(),
                    y_col: y_col.replace("_", " ").title()}
        )
    elif chart_type == "line":
        fig = px.line(
            df, x=x_col, y=y_col,
            title=title,
            markers=True,
            labels={x_col: x_col.replace("_", " ").title(),
                    y_col: y_col.replace("_", " ").title()}
        )
    elif chart_type == "pie":
        fig = px.pie(
            df, names=x_col, values=y_col,
            title=title
        )
    else:
        return None

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13)
    )

    return fig