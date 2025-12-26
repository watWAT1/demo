import streamlit as st
import pandas as pd

# 页面配置
st.set_page_config(page_title="商场销售仪表板", layout="wide")

# ---------------------- 数据加载（指定表头行，适配你的表格结构） ----------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel(
            "supermarket_sales.xlsx",
            engine="openpyxl",
            header=1
        )
        return df
    except FileNotFoundError:
        st.error("未找到文件：supermarket_sales.xlsx，请确认文件与py脚本同目录！")
        return None
    except Exception as e:
        st.error(f"读取异常：{str(e)}")
        return None

# 加载Excel数据
df = load_data()

# 仅当数据加载成功后执行后续逻辑
if df is not None:
    # ---------------------- 侧边栏筛选（完全适配你的表格列名） ----------------------
    st.sidebar.header("筛选条件")

    # 1. 城市筛选
    cities = df["城市"].unique()
    selected_cities = st.sidebar.multiselect(
        "选择城市",
        options=cities,
        default=cities
    )

    # 2. 顾客类型筛选
    customer_types = df["顾客类型"].unique()
    selected_customers = st.sidebar.multiselect(
        "选择顾客类型",
        options=customer_types,
        default=customer_types
    )

    # 3. 性别筛选
    genders = df["性别"].unique()
    selected_genders = st.sidebar.multiselect(
        "选择性别",
        options=genders,
        default=genders
    )

    # 应用筛选条件
    filtered_df = df[
        (df["城市"].isin(selected_cities)) &
        (df["顾客类型"].isin(selected_customers)) &
        (df["性别"].isin(selected_genders))
    ]

    # ---------------------- 核心指标计算 ----------------------
    if not filtered_df.empty:
        total_sales = filtered_df["总价"].sum()
        avg_rating = filtered_df["评分"].mean()
        order_count = filtered_df["订单号"].nunique()
        avg_per_order = total_sales / order_count if order_count != 0 else 0
        avg_price = filtered_df["单价"].mean()
    else:
        total_sales = 0
        avg_rating = 0.0
        order_count = 0
        avg_per_order = 0.0
        avg_price = 0.0

    # ---------------------- 主页面展示 ----------------------
    st.title("📊 2022年前3个月销售仪表板")

    # 四列展示核心指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总销售额", f"RMB ¥ {total_sales:,.2f}")
    with col2:
        stars = "⭐" * int(avg_rating)
        st.metric("顾客评分平均值", f"{avg_rating:.1f} {stars}")
    with col3:
        st.metric("每单平均销售额", f"RMB ¥ {avg_per_order:,.2f}")
    with col4:
        st.metric("商品平均单价", f"RMB ¥ {avg_price:.2f}")

    st.divider()

    # ---------------------- 数据可视化（两个图表同一行显示，核心修改） ----------------------
    if not filtered_df.empty:
        # 提取纯时间类型的小时数
        filtered_df["小时"] = filtered_df["时间"].apply(lambda x: x.hour if hasattr(x, 'hour') else None)
        hourly_sales = filtered_df.groupby("小时")["总价"].sum().reset_index()
        hourly_sales = hourly_sales.dropna(subset=["小时"])
        product_sales = filtered_df.groupby("产品类型")["总价"].sum().sort_values(ascending=False).reset_index()

        # 核心修改：创建两列布局，实现两个图表同一行显示
        chart_col1, chart_col2 = st.columns(2)

        # 左列：按下单小时划分的纵向柱状图
        with chart_col1:
            st.subheader("按小时划分的销售额分布")
            st.bar_chart(hourly_sales.set_index("小时")["总价"], color="#1f77b4", height=300)

        # 右列：按产品类型划分的横向柱状图
        with chart_col2:
            st.subheader("按产品类型划分的销售额分布")
            st.bar_chart(product_sales.set_index("产品类型")["总价"], color="#ff7f0e", height=400, horizontal=True)

