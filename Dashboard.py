import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar

st.set_page_config(page_title="2024-2025 Sales Dashboard", layout="wide")

# ---- Title with Logo ----
col1, col2 = st.columns([7, 1]) 

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
@st.cache_data
def load_data():
    df = pd.read_csv("Sales_2024_2025_up.csv")
    df["Month"] = pd.to_datetime(df["Month"], errors="coerce")
    return df
df = load_data()

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
        
        [data-testid="stSelectbox"] {
            margin-bottom: 2px !important;  
        }
        
        [data-testid="stPlotlyChart"] > div,
            .stPlotlyChart > div,
            .plot-card {
            background: #fff !important;
            border-radius: 15px !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
            padding: 10px !important;
            margin: 10px 0 !important;            
            overflow: hidden !important;
            max-width: 98.4% !important;      
        }

        .plot-card .js-plotly-plot,
        .stPlotlyChart .js-plotly-plot {
        border-radius: 15px !important;
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
    
    st.subheader("📊 Total Numbers for Branchs Performance in 2024 + 2025")
    st.write("")

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
    st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

    st.subheader("📊 Performance of the Selected Branch in 2024 + 2025")

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
    st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)
    
    # ---- Branch Contribution ----
    st.markdown("### 🏬 Percentage of Contribution of Each Branch to Total Sales 2024 + 2025")

    # ---- حساب مساهمة كل فرع ----
    totals_by_branch = df.groupby("Branch").agg({
        "Net_Sales": "sum"
    }).reset_index()

    # إجمالي المبيعات لكل الفروع
    total_sales = totals_by_branch["Net_Sales"].sum()

    # حساب نسبة المساهمة
    totals_by_branch["Contribution %"] = (totals_by_branch["Net_Sales"] / total_sales * 100).round(2)

    # ترتيب من الأعلى إلى الأقل
    totals_by_branch = totals_by_branch.sort_values("Net_Sales", ascending=False).reset_index(drop=True)

    # عرض في ستريم ليت كجدول
    st.dataframe(
    totals_by_branch.style.format({
        "Net_Sales": "{:,.0f}",
        "Contribution %": "{:.2f}%"
    }),
    use_container_width=True
    )

    # ---- End Container ----
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Tab 2 ----------------
with tabs[1]:

    # ✅ Start main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.subheader("📊 KPIs for Branchs Performance in 2024")

    # ---- فلترة بيانات 2024 ----
    df["Year"] = df["Month"].dt.year
    df_2024 = df[df["Year"] == 2024]
    
    # ---- Branch Filter ----
    branches = ["All Branches"] + sorted(df["Branch"].unique())
    selected_branch_2024 = st.selectbox("🏬 Select Branch (2024)", branches, index=0)

    # ---- فلترة بناءً على الاختيار ----
    if selected_branch_2024 != "All Branches":
        df_2024 = df_2024[df_2024["Branch"] == selected_branch_2024]

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

    st.subheader("📊 KPIs for Branchs Performance in 2025")

    # ---- فلترة بيانات 2025 ----
    df["Year"] = df["Month"].dt.year
    df_2025 = df[df["Year"] == 2025]

    # ---- Branch Filter ----
    branches = ["All Branches"] + sorted(df["Branch"].unique())
    selected_branch = st.selectbox("🏬 Select Branch", branches, index=0)

    # ---- فلترة بناءً على الاختيار ----
    if selected_branch != "All Branches":
        df_2025 = df_2025[df_2025["Branch"] == selected_branch]

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

    # Filtered data
    branch_df_2025 = df_2025[df_2025["Branch"] == selected_branch]

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

    st.subheader("📊 Total of Year-over-Year Growth Between 2024 → 2025")
    st.write("")

    # ---- First row: 3 KPIs ----
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Net Sales Growth</h4>
                <h2 style="color:{'green' if net_growth > 0 else 'red' if net_growth < 0 else 'orange'};">
                    {net_growth:.1f}%
                </h2>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Discounts Growth</h4>
                <h2 style="color:{'green' if disc_growth > 0 else 'red' if disc_growth < 0 else 'orange'};">
                    {disc_growth:.1f}%
                </h2>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Orders Growth</h4>
                <h2 style="color:{'green' if orders_growth > 0 else 'red' if orders_growth < 0 else 'orange'};">
                    {orders_growth:.1f}%
                </h2>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)
    
    # ---- عنوان ----
    st.subheader("📊 Year-over-Year Growth for Selected Branches Between 2024 → 2025")
    st.write("")

    # ---- Branch filter ----
    branches = sorted(df["Branch"].unique())
    selected_branches = st.multiselect(
        "🏬 Select Branches",
        branches,
        default=[branches[0]] 
    )

    if selected_branches:
        # ---- فلترة الداتا على الفروع المختارة ----
        df_selected = df[df["Branch"].isin(selected_branches)]

        # ---- تقسيم حسب السنوات ----
        df_2024 = df_selected[df_selected["Year"] == 2024]
        df_2025 = df_selected[df_selected["Year"] == 2025]

        # ---- إجماليات ----
        net_2024, net_2025 = df_2024["Net_Sales"].sum(), df_2025["Net_Sales"].sum()
        disc_2024, disc_2025 = df_2024["Discount_Amount"].sum(), df_2025["Discount_Amount"].sum()
        orders_2024, orders_2025 = df_2024["Orders"].sum(), df_2025["Orders"].sum()

        # ---- دالة تحسب النمو ----
        def safe_growth(v2024, v2025):
            if v2024 == 0 and v2025 == 0:
                return "N/A"
            elif v2024 == 0 and v2025 != 0:
                return "N/A"
            else:
                return round(((v2025 - v2024) / v2024) * 100, 1)

        net_growth = safe_growth(net_2024, net_2025)
        disc_growth = safe_growth(disc_2024, disc_2025)
        orders_growth = safe_growth(orders_2024, orders_2025)

        # ---- دالة تحدد اللون ----
        def growth_color(val):
            if isinstance(val, str):  # N/A
                return "#6c757d"  # رمادي
            elif val > 0:
                return "green"
            elif val < 0:
                return "red"
            else:
                return "orange"  # صفر

        # ---- عرض الكاردز ----
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align:center;">
                    <h4>Net Sales Growth</h4>
                    <h2 style="color:{growth_color(net_growth)};">{net_growth if isinstance(net_growth,str) else str(net_growth)+'%'}</h2>
                </div>
                """, unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align:center;">
                    <h4>Discounts Growth</h4>
                    <h2 style="color:{growth_color(disc_growth)};">{disc_growth if isinstance(disc_growth,str) else str(disc_growth)+'%'}</h2>
                </div>
                """, unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align:center;">
                    <h4>Orders Growth</h4>
                    <h2 style="color:{growth_color(orders_growth)};">{orders_growth if isinstance(orders_growth,str) else str(orders_growth)+'%'}</h2>
                </div>
                """, unsafe_allow_html=True
            )

    else:
        st.info("Please select at least one branch to calculate growth.")

    # ---- خط فاصل ----
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

        
    # ---- تجهيز العمود Month ----
    df["Month"] = pd.to_datetime(df["Month"], errors="coerce")   # ✅ التحويل مرة وحدة في البداية
    df["Month_Label"] = df["Month"].dt.strftime("%b %Y")

    st.subheader(f"📊 Average Order Value per Month - {selected_branch}")

    # ---- Branch filter ----
    branches = sorted(df["Branch"].unique())
    selected_branch = st.selectbox("🏬 Select Branch", branches)

    # ---- فلترة الداتا على الفرع المختار ----
    df_branch = df[df["Branch"] == selected_branch].copy()

    # ---- حساب متوسط قيمة الطلب ----
    df_branch["Avg_Order_Value"] = df_branch.apply(
        lambda row: row["Net_Sales"] / row["Orders"] if row["Orders"] > 0 else 0,
        axis=1
    )

    # ---- تجهيز الجدول ----
    avg_table = df_branch.sort_values("Month")[["Month_Label", "Avg_Order_Value"]]

    # ---- عرض لاين تشارت ----
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=avg_table["Month_Label"],
        y=avg_table["Avg_Order_Value"],
        mode="lines+markers",
        line=dict(color="#007BFF", width=3),
        marker=dict(size=8),
        name="Avg Order Value"
    ))

    fig.update_layout(
        title=f"📈 Average Order Value per Month - {selected_branch}",
        xaxis_title="Month",
        yaxis_title="Average Order Value (SAR)",
        hovermode="x unified",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---- خط فاصل ----
    st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

    st.subheader("📊 Comparing the Performance of a Specific Branch Between Two Different Periods")

    # ---- Branch filter ----
    branches_comp = sorted(df["Branch"].unique())
    selected_branch_comp = st.selectbox("Select Branch (Comparison)", branches_comp, key="branch_comp")

    branch_data = df[df["Branch"] == selected_branch_comp]

    # ------------------ الفترة الأولى ------------------
    st.markdown("<h5>📅 Select the First Period</h5>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3, col4 = st.columns([1,1,1,1])

        with col1:
            start_month1 = st.selectbox("Start Month", list(range(1, 13)),
                                        format_func=lambda m: calendar.month_name[m], key="start_month1")
        with col2:
            start_year1 = st.selectbox("Start Year", sorted(df["Year"].unique()), key="start_year1")

        with col3:
            end_month1 = st.selectbox("End Month", list(range(1, 13)),
                                    format_func=lambda m: calendar.month_name[m], key="end_month1")
        with col4:
            end_year1 = st.selectbox("End Year", sorted(df["Year"].unique()), key="end_year1")

    # ------------------ الفترة الثانية ------------------
    st.markdown("<h5>📅 Select the Second Period</h5>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3, col4 = st.columns([1,1,1,1])

        with col1:
            start_month2 = st.selectbox("Start Month", list(range(1, 13)),
                                        format_func=lambda m: calendar.month_name[m], key="start_month2")
        with col2:
            start_year2 = st.selectbox("Start Year", sorted(df["Year"].unique()), key="start_year2")

        with col3:
            end_month2 = st.selectbox("End Month", list(range(1, 13)),
                                    format_func=lambda m: calendar.month_name[m], key="end_month2")
        with col4:
            end_year2 = st.selectbox("End Year", sorted(df["Year"].unique()), key="end_year2")

    # ------------------ فلترة البيانات ------------------
    # تحويل إلى تواريخ بداية ونهاية
    start_date1 = pd.to_datetime(f"{start_year1}-{start_month1}-01")
    end_date1   = pd.to_datetime(f"{end_year1}-{end_month1}-28")
    start_date2 = pd.to_datetime(f"{start_year2}-{start_month2}-01")
    end_date2   = pd.to_datetime(f"{end_year2}-{end_month2}-28")

    # فلترة
    period1 = branch_data[(branch_data["Month"] >= start_date1) & (branch_data["Month"] <= end_date1)]
    period2 = branch_data[(branch_data["Month"] >= start_date2) & (branch_data["Month"] <= end_date2)]

    # القيم
    net1, net2   = period1["Net_Sales"].sum(),       period2["Net_Sales"].sum()
    disc1, disc2 = period1["Discount_Amount"].sum(), period2["Discount_Amount"].sum()
    ord1, ord2   = period1["Orders"].sum(),          period2["Orders"].sum()

    # ------------------ التشارت ------------------
    fig_comp = go.Figure()

    # Net Sales
    fig_comp.add_trace(go.Bar(
        x=["Period 1"], y=[net1],
        name=f"Net Sales {start_date1:%b %Y} - {end_date1:%b %Y}",
        marker_color="#27ae60",
        texttemplate="%{y:,.0f}", textposition="inside",
        textfont=dict(size=20, color="white")
    ))
    fig_comp.add_trace(go.Bar(
        x=["Period 2"], y=[net2],
        name=f"Net Sales {start_date2:%b %Y} - {end_date2:%b %Y}",
        marker_color="#2ecc71",
        texttemplate="%{y:,.0f}", textposition="inside",
        textfont=dict(size=20, color="white")
    ))

    # Discounts
    fig_comp.add_trace(go.Bar(
        x=["Period 1"], y=[disc1],
        name=f"Discounts {start_date1:%b %Y} - {end_date1:%b %Y}",
        marker_color="darkred", visible=False,
        texttemplate="%{y:,.0f}", textposition="inside",
        textfont=dict(size=20, color="white")
    ))
    fig_comp.add_trace(go.Bar(
        x=["Period 2"], y=[disc2],
        name=f"Discounts {start_date2:%b %Y} - {end_date2:%b %Y}",
        marker_color="red", visible=False,
        texttemplate="%{y:,.0f}", textposition="inside",
        textfont=dict(size=20, color="white")
    ))

    # Orders
    fig_comp.add_trace(go.Bar(
        x=["Period 1"], y=[ord1],
        name=f"Orders {start_date1:%b %Y} - {end_date1:%b %Y}",
        marker_color="navy", visible=False,
        texttemplate="%{y:,.0f}", textposition="inside",
        textfont=dict(size=20, color="white")
    ))
    fig_comp.add_trace(go.Bar(
        x=["Period 2"], y=[ord2],
        name=f"Orders {start_date2:%b %Y} - {end_date2:%b %Y}",
        marker_color="blue", visible=False,
        texttemplate="%{y:,.0f}", textposition="inside",
        textfont=dict(size=20, color="white")
    ))

    fig_comp.update_xaxes(type="category")
    fig_comp.update_layout(
        barmode="group",
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(label="Net Sales", method="update",
                        args=[{"visible": [True, True, False, False, False, False]},
                            {"title": {"text": f"Net Sales Comparison"}}]),
                    dict(label="Discounts", method="update",
                        args=[{"visible": [False, False, True, True, False, False]},
                            {"title": {"text": f"Discounts Comparison"}}]),
                    dict(label="Orders", method="update",
                        args=[{"visible": [False, False, False, False, True, True]},
                            {"title": {"text": f"Orders Comparison"}}]),
                ],
                x=0.5, y=1.15, xanchor="center", yanchor="top"
            )
        ],
        title={"text": f"Comparison: {start_date1:%b %Y}-{end_date1:%b %Y} vs {start_date2:%b %Y}-{end_date2:%b %Y}"},
        showlegend=True
    )
    fig_comp.update_yaxes(tickformat="d")

    st.plotly_chart(fig_comp, use_container_width=True)
    st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

    st.subheader("📊 Comparing Two or More Branches in a Specific Period")

    # ---- Aggregated by Branch with Date Range ----

    # فلتر لاختيار أكثر من فرع
    selected_branches_total = st.multiselect(
        "Select Branches", 
        branches_comp, 
        default=branches_comp[:2]
    )

    # ------------------ اختيار الفترة ------------------
    st.markdown("<h5>📅 Select Period</h5>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        start_month = st.selectbox(
            "Start Month",
            list(range(1, 13)),
            format_func=lambda m: calendar.month_name[m],
            key="start_month",
            index=0
        )
    with col2:
        start_year = st.selectbox(
            "Start Year",
            sorted(df["Year"].unique()),
            key="start_year",
            index=0
        )
    with col3:
        end_month = st.selectbox(
            "End Month",
            list(range(1, 13)),
            format_func=lambda m: calendar.month_name[m],
            key="end_month",
            index=11   
        )
    with col4:
        end_year = st.selectbox(
            "End Year",
            sorted(df["Year"].unique()),
            key="end_year",
            index=1
        )

    # ------------------ فلترة البيانات ------------------
    start_date = pd.to_datetime(f"{start_year}-{start_month}-01")
    end_date = pd.to_datetime(f"{end_year}-{end_month}-28")  # نهاية الشهر كافية

    if selected_branches_total:
        # فلترة البيانات حسب الفروع والفترة
        branch_multi = df[
            (df["Branch"].isin(selected_branches_total)) &
            (df["Month"] >= start_date) & 
            (df["Month"] <= end_date)
        ]

        # حساب الإجماليات لكل فرع
        totals_by_branch = branch_multi.groupby("Branch").agg({
            "Net_Sales": "sum",
            "Discount_Amount": "sum",
            "Orders": "sum"
        }).reset_index()

        # ---- Bar Chart ----
        fig_total = go.Figure()

        # Net Sales
        fig_total.add_trace(go.Bar(
            x=totals_by_branch["Branch"], 
            y=totals_by_branch["Net_Sales"],
            name="Net Sales",
            marker_color="#2ecc71",
            texttemplate="%{y:,.0f}",
            textposition="inside",
            textfont=dict(size=18, color="white")
        ))

        # Discounts
        fig_total.add_trace(go.Bar(
            x=totals_by_branch["Branch"], 
            y=totals_by_branch["Discount_Amount"],
            name="Discounts",
            marker_color="red",
            visible=False,
            texttemplate="%{y:,.0f}",
            textposition="inside",
            textfont=dict(size=18, color="white")
        ))

        # Orders
        fig_total.add_trace(go.Bar(
            x=totals_by_branch["Branch"], 
            y=totals_by_branch["Orders"],
            name="Orders",
            marker_color="blue",
            visible=False,
            texttemplate="%{y:,.0f}",
            textposition="inside",
            textfont=dict(size=18, color="white")
        ))

        # إعداد الأزرار
        fig_total.update_layout(
            barmode="group",
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=[
                        dict(label="Net Sales",
                            method="update",
                            args=[{"visible": [True, False, False]},
                                {"title": {"text": f"Net Sales {start_date:%b %Y} → {end_date:%b %Y}"}}]),
                        dict(label="Discounts",
                            method="update",
                            args=[{"visible": [False, True, False]},
                                {"title": {"text": f"Discounts {start_date:%b %Y} → {end_date:%b %Y}"}}]),
                        dict(label="Orders",
                            method="update",
                            args=[{"visible": [False, False, True]},
                                {"title": {"text": f"Orders {start_date:%b %Y} → {end_date:%b %Y}"}}]),
                    ],
                    x=0.5, y=1.15, xanchor="center", yanchor="top"
                )
            ],
            title={"text": f"Net Sales {start_date:%b %Y} → {end_date:%b %Y}"},
            showlegend=True
        )

        fig_total.update_yaxes(tickformat="d")

        st.plotly_chart(fig_total, use_container_width=True)

    else:
        st.info("Please select at least one branch to display the chart.")