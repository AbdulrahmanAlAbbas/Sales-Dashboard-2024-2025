import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="2024-2025 Sales Dashboard", layout="wide")

# ---- Title with Logo ----
col1, col2 = st.columns([7, 1])  # العنوان أوسع، الشعار أصغر

with col1:
    st.markdown(
        """
        <h1 style="color:#000000; font-size:36px; margin-top:15px; margin-bottom:5px;">
            📊 2024-2025 Sales Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThAsJgb1nN-XLqXMsXh6DYAE-qTUf1lEG2tw&s",
        width=100
    )

# Load data
df = pd.read_csv("Sales_24_and_25_cleaned.csv")
df["Month"] = pd.to_datetime(df["Month"], errors="coerce")

# Tabs
tabs = st.tabs(["📊 Overview", "📅 2024", "📅 2025", "⚖ Comparison"])

# ---- CSS for cards ----
st.markdown("""
    <style>
        .metric-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            text-align: center;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .metric-card h4 {
            font-size: 16px;
            color: #666;
            margin-bottom: 6px;
        }
        .metric-card h2 {
            font-size: 28px;
            margin: 0;
            color: #222;
        }
        .metric-card p {
            font-size: 13px;
            margin-top: 4px;
        }
        .positive { color: green; }
        .negative { color: red; }
        .neutral { color: gray; }
        .main-container {
            max-width: 90%;
            margin: auto;
        }
        [data-testid="stPlotlyChart"] > div {
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            padding: 10px;
            margin: 10px 0;
            overflow: hidden;
        }
                
        [data-testid="stSelectbox"] {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        padding: 10px;
        margin: 10px 0;
        }
        
         /* ✅ هنا إضافة التحكم بالمسافة بين الفلتر والتشارت */
        [data-testid="stSelectbox"] {
            margin-bottom: 2px !important;  /* قللتها من 20px إلى 8px */
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Tab 1 ----------------
with tabs[0]:

    # ---- Start Container ----
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # KPIs
    total_net = df["Net_Sales"].sum()
    total_discount = df["Discount_Amount"].sum()
    total_orders = df["Orders"].sum()
    
    # ---- First row: 4 KPIs ----
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <h4>Total Net Sales</h4>
            <h2 style="display:flex;align-items:center;justify-content:center;gap:6px;">
                {total_net:,.0f}
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Saudi_Riyal_Symbol.svg/500px-Saudi_Riyal_Symbol.svg.png" 
                     alt="SAR" width="25" height="25">
            </h2>
        </div>
        """, unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Total Discounts</h4>
                <h2 style="display:flex;align-items:center;justify-content:center;gap:6px;">
                {total_discount:,.0f}
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Saudi_Riyal_Symbol.svg/500px-Saudi_Riyal_Symbol.svg.png" 
                     alt="SAR" width="25" height="25">
            </h2>
        </div>
        """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Total Orders</h4>
                <h2>{total_orders:,}</h2>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    
    # ---- Branch filter ----
    branches = sorted(df["Branch"].unique())
    selected_branch = st.selectbox("Select Branch", branches)

    df["Month"] = pd.to_datetime(df["Month"], errors="coerce")
    # إنشاء عمود نصي للعرض (سنة-شهر فقط)
    df["Month_Label"] = df["Month"].dt.strftime("%b %Y")
    
    # ---- Filter data ----
    branch_df = df[df["Branch"] == selected_branch]

    # ---- Charts ----
    fig = go.Figure()

    # Add Net Sales
    fig.add_trace(go.Scatter(
        x=branch_df["Month_Label"],
        y=branch_df["Net_Sales"],
        mode="lines+markers",
        name="Net Sales",
        line=dict(color="#2ecc71"),   # ✅ اللون أخضر
        visible=True
    ))

    # Add Discounts
    fig.add_trace(go.Scatter(
        x=branch_df["Month_Label"],
        y=branch_df["Discount_Amount"],
        mode="lines+markers",
        name="Discounts",
        line=dict(color="red"),     # ✅ اللون أحمر
        visible=False
    ))

    # Add Orders
    fig.add_trace(go.Scatter(
        x=branch_df["Month_Label"],
        y=branch_df["Orders"],
        mode="lines+markers",
        name="Orders",
        visible=False
    ))

    # Buttons menu
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(label="Net Sales",
                        method="update",
                        args=[{"visible": [True, False, False]},
                            {"title": {"text": "Net Sales by Month"}}]),
                    dict(label="Discounts",
                        method="update",
                        args=[{"visible": [False, True, False]},
                            {"title":{"text": "Discounts by Month"}}]),
                    dict(label="Orders",
                        method="update",
                        args=[{"visible": [False, False, True]},
                            {"title":{"text": "Orders by Month"}}]),
                ]),
                x=0.5,
                y=1.15,
                xanchor="center",
                yanchor="top"
            )
        ]
    )

    # Layout style
    fig.update_layout(
        title="Net Sales by Month",
        showlegend=False
    )

    fig.update_yaxes(
        tickformat="d"   # ✅ يعرض أعداد صحيحة فقط بدون كسور
    )

    st.plotly_chart(fig, use_container_width=True)


    # ---- End Container ----
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Tab 2 ----------------
with tabs[1]:

    # ✅ Start main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # ---- فلترة بيانات 2024 ----
    df["Year"] = df["Month"].dt.year
    df_2024 = df[df["Year"] == 2024]

    # ---- KPIs (2024 فقط) ----
    total_net_2024 = df_2024["Net_Sales"].sum()
    total_discount_2024 = df_2024["Discount_Amount"].sum()
    total_orders_2024 = df_2024["Orders"].sum()

    # ---- First row: 3 KPIs ----
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Total Net Sales</h4>
                <h2 style="display:flex;align-items:center;justify-content:center;gap:6px;">
                {total_net_2024:,.0f}
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Saudi_Riyal_Symbol.svg/500px-Saudi_Riyal_Symbol.svg.png" 
                     alt="SAR" width="25" height="25">
            </h2>
        </div>
        """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Total Discounts</h4>
                <h2 style="display:flex;align-items:center;justify-content:center;gap:6px;">
                {total_discount_2024:,.0f}
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Saudi_Riyal_Symbol.svg/500px-Saudi_Riyal_Symbol.svg.png" 
                     alt="SAR" width="25" height="25">
            </h2>
        </div>
        """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Total Orders</h4>
                <h2>{total_orders_2024:,}</h2>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # ---- Branch filter (2024 فقط) ----
    branches_2024 = sorted(df_2024["Branch"].unique())
    selected_branch_2024 = st.selectbox("Select Branch (2024)", branches_2024)

    # Filtered data
    branch_df_2024 = df_2024[df_2024["Branch"] == selected_branch_2024]

    # ---- Chart (2024 فقط) ----
    fig2024 = go.Figure()

    # Add Net Sales
    fig2024.add_trace(go.Scatter(
        x=branch_df_2024["Month_Label"],
        y=branch_df_2024["Net_Sales"],
        mode="lines+markers",
        name="Net Sales",
        line=dict(color="#2ecc71"),   # أخضر فاتح
        visible=True
    ))

    # Add Discounts
    fig2024.add_trace(go.Scatter(
        x=branch_df_2024["Month_Label"],
        y=branch_df_2024["Discount_Amount"],
        mode="lines+markers",
        name="Discounts",
        line=dict(color="red"),       # أحمر
        visible=False
    ))

    # Add Orders
    fig2024.add_trace(go.Scatter(
        x=branch_df_2024["Month_Label"],
        y=branch_df_2024["Orders"],
        mode="lines+markers",
        name="Orders",
        line=dict(color="blue"),      # أزرق
        visible=False
    ))

    # Buttons menu
    fig2024.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(label="Net Sales",
                        method="update",
                        args=[{"visible": [True, False, False]},
                            {"title": {"text": "Net Sales by Month (2024)"}}]),
                    dict(label="Discounts",
                        method="update",
                        args=[{"visible": [False, True, False]},
                            {"title":{"text": "Discounts by Month (2024)"}}]),
                    dict(label="Orders",
                        method="update",
                        args=[{"visible": [False, False, True]},
                            {"title":{"text": "Orders by Month (2024)"}}]),
                ]),
                x=0.5,
                y=1.15,
                xanchor="center",
                yanchor="top"
            )
        ]
    )

    # Layout style
    fig2024.update_layout(
        title={"text": "Net Sales by Month (2024)"},
        showlegend=False
    )

    fig2024.update_yaxes(
        tickformat="d"   # ✅ أعداد صحيحة فقط
    )

    st.plotly_chart(fig2024, use_container_width=True)

    # ✅ End main container
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Tab 3 ----------------
with tabs[2]:

    # ✅ Start main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # ---- فلترة بيانات 2025 ----
    df["Year"] = df["Month"].dt.year
    df_2025 = df[df["Year"] == 2025]

    # ---- KPIs (2025 فقط) ----
    total_net_2025 = df_2025["Net_Sales"].sum()
    total_discount_2025 = df_2025["Discount_Amount"].sum()
    total_orders_2025 = df_2025["Orders"].sum()

    # ---- First row: 3 KPIs ----
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Total Net Sales</h4>
                <h2 style="display:flex;align-items:center;justify-content:center;gap:6px;">
                {total_net_2025:,.0f}
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Saudi_Riyal_Symbol.svg/500px-Saudi_Riyal_Symbol.svg.png" 
                     alt="SAR" width="25" height="25">
            </h2>
        </div>
        """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Total Discounts</h4>
                <h2 style="display:flex;align-items:center;justify-content:center;gap:6px;">
                {total_discount_2025:,.0f}
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Saudi_Riyal_Symbol.svg/500px-Saudi_Riyal_Symbol.svg.png" 
                     alt="SAR" width="25" height="25">
            </h2>
        </div>
        """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Total Orders</h4>
                <h2>{total_orders_2025:,}</h2>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # ---- Branch filter (2025 فقط) ----
    branches_2025 = sorted(df_2025["Branch"].unique())
    selected_branch_2025 = st.selectbox("Select Branch (2025)", branches_2025)

    # Filtered data
    branch_df_2025 = df_2025[df_2025["Branch"] == selected_branch_2025]

    # ---- Chart (2025 فقط) ----
    fig2025 = go.Figure()

    # Add Net Sales
    fig2025.add_trace(go.Scatter(
        x=branch_df_2025["Month_Label"],
        y=branch_df_2025["Net_Sales"],
        mode="lines+markers",
        name="Net Sales",
        line=dict(color="#2ecc71"),   # أخضر فاتح
        visible=True
    ))

    # Add Discounts
    fig2025.add_trace(go.Scatter(
        x=branch_df_2025["Month_Label"],
        y=branch_df_2025["Discount_Amount"],
        mode="lines+markers",
        name="Discounts",
        line=dict(color="red"),       # أحمر
        visible=False
    ))

    # Add Orders
    fig2025.add_trace(go.Scatter(
        x=branch_df_2025["Month_Label"],
        y=branch_df_2025["Orders"],
        mode="lines+markers",
        name="Orders",
        line=dict(color="blue"),      # أزرق
        visible=False
    ))

    # Buttons menu
    fig2025.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(label="Net Sales",
                        method="update",
                        args=[{"visible": [True, False, False]},
                            {"title": {"text": "Net Sales by Month (2025)"}}]),
                    dict(label="Discounts",
                        method="update",
                        args=[{"visible": [False, True, False]},
                            {"title":{"text": "Discounts by Month (2025)"}}]),
                    dict(label="Orders",
                        method="update",
                        args=[{"visible": [False, False, True]},
                            {"title":{"text": "Orders by Month (2025)"}}]),
                ]),
                x=0.5,
                y=1.15,
                xanchor="center",
                yanchor="top"
            )
        ]
    )

    # Layout style
    fig2025.update_layout(
        title={"text": "Net Sales by Month (2025)"},
        showlegend=False
    )

    fig2025.update_yaxes(
        tickformat="d"   # ✅ أعداد صحيحة فقط
    )

    st.plotly_chart(fig2025, use_container_width=True)

    # ✅ End main container
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Tab 4 ----------------
with tabs[3]:

    # ✅ Start main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # ---- فلترة البيانات ----
    df_2024 = df[df["Year"] == 2024]
    df_2025 = df[df["Year"] == 2025]

    # ---- إجماليات ----
    net_2024, net_2025 = df_2024["Net_Sales"].sum(), df_2025["Net_Sales"].sum()
    disc_2024, disc_2025 = df_2024["Discount_Amount"].sum(), df_2025["Discount_Amount"].sum()
    orders_2024, orders_2025 = df_2024["Orders"].sum(), df_2025["Orders"].sum()

    # ---- النسب ----
    net_growth = ((net_2025 - net_2024) / net_2024) * 100 if net_2024 != 0 else 0
    disc_growth = ((disc_2025 - disc_2024) / disc_2024) * 100 if disc_2024 != 0 else 0
    orders_growth = ((orders_2025 - orders_2024) / orders_2024) * 100 if orders_2024 != 0 else 0

    # ---- First row: 3 KPIs ----
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Net Sales Growth</h4>
                <h2>{net_growth:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Discounts Growth</h4>
                <h2>{disc_growth:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Orders Growth</h4>
                <h2>{orders_growth:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # ---- Branch filter ----
    branches_comp = sorted(df["Branch"].unique())
    selected_branch_comp = st.selectbox("Select Branch (Comparison)", branches_comp)

    # Filtered data
    branch_2024 = df_2024[df_2024["Branch"] == selected_branch_comp]
    branch_2025 = df_2025[df_2025["Branch"] == selected_branch_comp]

    # ---- Bar Chart ----
import calendar
available_months = sorted(
    set(branch_2024["Month"].dt.month.dropna().unique()) |
    set(branch_2025["Month"].dt.month.dropna().unique())
)
selected_month = st.selectbox("Select Month", available_months, format_func=lambda m: calendar.month_name[m])

# تصفية الشهر المختار
m24 = branch_2024[branch_2024["Month"].dt.month == selected_month]
m25 = branch_2025[branch_2025["Month"].dt.month == selected_month]

# قيم كل مقياس لذلك الشهر
net24, net25   = m24["Net_Sales"].sum(),        m25["Net_Sales"].sum()
disc24, disc25 = m24["Discount_Amount"].sum(),  m25["Discount_Amount"].sum()
ord24, ord25   = m24["Orders"].sum(),           m25["Orders"].sum()

# ---- Bar Chart: فقط بارين (2024 vs 2025) للشهر المختار ----
fig_comp = go.Figure()

# Net Sales
fig_comp.add_trace(go.Bar(
    x=["2024"], y=[net24],
    name="Net Sales 2024",
    marker_color="#27ae60",
    width=0.35, visible=True,
    texttemplate="%{y:,.0f}", 
    textposition="inside",
    textfont=dict(size=20, color="white")
))
fig_comp.add_trace(go.Bar(
    x=["2025"], y=[net25],
    name="Net Sales 2025",
    marker_color="#2ecc71",
    width=0.35, visible=True,
    texttemplate="%{y:,.0f}", 
    textposition="inside",
    textfont=dict(size=20, color="white")
))

# Discounts
fig_comp.add_trace(go.Bar(
    x=["2024"], y=[disc24],
    name="Discounts 2024",
    marker_color="darkred",
    width=0.35, visible=False,
    texttemplate="%{y:,.0f}", 
    textposition="inside",
    textfont=dict(size=20, color="white")
))

fig_comp.add_trace(go.Bar(
    x=["2025"], y=[disc25],
    name="Discounts 2025",
    marker_color="red",
    width=0.35, visible=False,
    texttemplate="%{y:,.0f}", 
    textposition="inside",
    textfont=dict(size=20, color="white")
))

# Orders
fig_comp.add_trace(go.Bar(
    x=["2024"], y=[ord24],
    name="Orders 2024",
    marker_color="navy",
    width=0.35, visible=False,
    texttemplate="%{y:,.0f}", 
    textposition="inside",
    textfont=dict(size=20, color="white")
))

fig_comp.add_trace(go.Bar(
    x=["2025"], y=[ord25],
    name="Orders 2025",
    marker_color="blue",
    width=0.35, visible=False,
    texttemplate="%{y:,.0f}", 
    textposition="inside",
    textfont=dict(size=20, color="white")
))

# اجعل محور X تصنيفيًا (فقط 2024 و 2025)
fig_comp.update_xaxes(type="category")

# Buttons menu
fig_comp.update_layout(
    barmode="group",
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=[
                dict(label="Net Sales",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False]},
                           {"title": {"text": f"Net Sales in {calendar.month_name[selected_month]} (2024 vs 2025)"}}]),
                dict(label="Discounts",
                     method="update",
                     args=[{"visible": [False, False, True, True, False, False]},
                           {"title": {"text": f"Discounts in {calendar.month_name[selected_month]} (2024 vs 2025)"}}]),
                dict(label="Orders",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, True]},
                           {"title": {"text": f"Orders in {calendar.month_name[selected_month]} (2024 vs 2025)"}}]),
            ],
            x=0.5, y=1.15, xanchor="center", yanchor="top"
        )
    ],
    title={"text": f"Net Sales in {calendar.month_name[selected_month]} (2024 vs 2025)"},
    showlegend=True
)

# أرقام صحيحة فقط على محور Y
fig_comp.update_yaxes(tickformat="d")

st.plotly_chart(fig_comp, use_container_width=True)