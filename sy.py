import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# 定义一个设置中文字体的函数
def setup_chinese_fonts():
    try:
        # 尝试加载多种字体，确保在不同环境下都能工作
        fonts = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Noto Sans CJK SC', 'Noto Sans SC', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
        plt.rcParams['font.sans-serif'] = fonts
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.family'] = 'sans-serif'
    except Exception as e:
        # 如果设置字体失败，使用默认字体
        pass

# 设置页面配置
st.set_page_config(
    page_title="学生成绩分析与预测系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置暗色主题样式
st.markdown("""
    <style>
        /* 重置默认样式 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* 页面背景 */
        body {
            background-color: #0a0a0a;
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
        
        /* 侧边栏样式 */
        .css-1d391kg {
            background-color: #0a0a0a;
            border-right: 1px solid #1e1e1e;
            padding-top: 2rem;
            padding-left: 1.5rem;
        }
        
        /* 主内容区域 */
        .css-18e3th9 {
            padding-top: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }
        
        /* 标题样式 */
        h1 {
            color: #ffffff;
            font-size: 2.2rem;
            font-weight: 600;
            margin-bottom: 2rem;
        }
        
        h2 {
            color: #ffffff;
            font-size: 1.5rem;
            font-weight: 500;
            margin-top: 2.5rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* 侧边栏标题 */
        .sidebar .css-1v0mbdj {
            color: #ffffff;
            font-size: 1.2rem;
        }
        
        /* 单选按钮样式 */
        .stRadio > div {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .stRadio label {
            color: #e0e0e0;
            font-size: 0.95rem;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .stRadio label:hover {
            background-color: #1e1e1e;
        }
        
        .stRadio input[type="radio"]:checked + label {
            background-color: #2a2a2a;
            color: #ffffff;
            font-weight: 500;
        }
        
        /* 分栏样式 */
        .css-1kyxreq {
            gap: 1.5rem;
        }
        
        /* 卡片样式 */
        .css-1aumxhk {
            background-color: #121212;
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid #1e1e1e;
        }
        
        /* 列表样式 */
        ul {
            margin-left: 1.5rem;
        }
        
        li {
            margin-bottom: 0.5rem;
        }
        
        /* 数据可视化区域 */
        .chart-container {
            background-color: #121212;
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid #1e1e1e;
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* 图片切换按钮样式 */
        .stButton > button {
            width: 100%;
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: #2a2a2a;
            border-color: #444444;
        }
        
        .stButton > button:active {
            background-color: #333333;
        }
        
        /* 图片样式 */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        
        /* 表单容器样式 */
        .stForm {
            background-color: #121212;
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid #1e1e1e;
        }
        
        /* 输入字段样式 */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            color: #e0e0e0;
            border-radius: 4px;
            padding: 0.5rem;
        }
        
        /* 表单标签样式 */
        .stForm label {
            color: #e0e0e0;
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        /* 提交按钮样式 */
        .stFormSubmitButton > button {
            width: 100%;
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .stFormSubmitButton > button:hover {
            background-color: #c0392b;
        }
        
        .stFormSubmitButton > button:active {
            background-color: #a93226;
        }
    </style>
""", unsafe_allow_html=True)

# 左侧导航栏
with st.sidebar:
    st.title("学生成绩分析与预测系统")
    menu_options = ["项目介绍", "专业数据分析", "成绩预测"]
    selected_menu = st.radio(" ", menu_options, index=0)

# 主内容区域
if selected_menu == "项目介绍":
    # 页面标题
    st.title("学生成绩分析与预测系统")
    
    st.markdown("---")
    
    # 左右两列布局：左侧包含项目概述和主要特点（上下排列），右侧包含系统展示
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # 项目概述
        st.header("项目概述")
        st.markdown("""
        本系统基于学生的学习数据，利用机器学习算法进行成绩分析与预测。通过收集学生的学习行为数据，我们可以深入了解学生的学习情况，并预测其未来的学习成绩，为教育教学提供科学依据。
        """)
        
        # 主要特点
        st.header("主要特点")
        st.markdown("""
        - **数据分析**：对学生学习数据进行多维度分析
        - **成绩预测**：基于机器学习算法预测学生成绩
        - **实时更新**：数据实时更新，保证分析结果准确性
        - **可视化展示**：直观的图表展示，便于理解和决策
        """)
    
    with right_col:
        # 系统展示 - 图片切换器
        st.subheader("系统展示")
        
        # 初始化会话状态来跟踪当前图片
        if 'current_image' not in st.session_state:
            st.session_state.current_image = 1
        
        # 显示当前图片
        st.image(f"images/{st.session_state.current_image}.png", width="stretch")
        
        # 按钮布局
        col1, col2 = st.columns(2)
        with col1:
            # 上一张按钮
            if st.button("上一张"):
                if st.session_state.current_image > 1:
                    st.session_state.current_image -= 1
        
        with col2:
            # 下一张按钮
            if st.button("下一张"):
                if st.session_state.current_image < 3:
                    st.session_state.current_image += 1
    
    st.markdown("---")
    
    # 项目目标
    st.header("项目目标")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**目标一**")
        st.markdown("- 建立学生成绩预测模型")
        st.markdown("- 提高预测准确率")
        st.markdown("- 为教学提供参考")
    with col2:
        st.markdown("**目标二**")
        st.markdown("- 优化学习资源分配")
        st.markdown("- 提升教学质量")
        st.markdown("- 促进学生发展")
    with col3:
        st.markdown("**目标三**")
        st.markdown("- 形成智能教育体系")
        st.markdown("- 个性化学习推荐")
        st.markdown("- 教育决策支持")
    
    st.markdown("---")
    
    # 技术架构
    st.header("技术架构")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**前端框架**")
        st.markdown("Streamlit")
    with col2:
        st.markdown("**数据处理**")
        st.markdown("Pandas")
        st.markdown("NumPy")
    with col3:
        st.markdown("**可视化**")
        st.markdown("Matplotlib")
        st.markdown("Seaborn")
    with col4:
        st.markdown("**机器学习**")
        st.markdown("Scikit-learn")
    
    st.markdown("---")

# 其他页面内容可以在这里继续添加
elif selected_menu == "专业数据分析":
    # 页面标题
    st.title("专业数据分析")
    
    # 添加横线分割
    st.markdown("---")
    
    # 1. 各专业男女比例
    st.header("1. 各专业男女比例")
    
    # 设置样式
    plt.style.use('default')
    sns.set_theme(style="white")
    
    # 设置中文字体支持（适用于本地和Cloud环境）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Noto Sans CJK SC', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.family'] = 'sans-serif'
    
    # 读取数据
    df = pd.read_csv('student.csv')
    
    # 计算男女人数
    gender_counts = df.groupby(['专业', '性别']).size().unstack(fill_value=0)
    
    # 计算每个专业的总人数
    total_counts = gender_counts.sum(axis=1)
    
    # 计算男女比例（百分比）
    gender_ratio = gender_counts.div(total_counts, axis=0) * 100
    
    # 绘制比例柱状图
    setup_chinese_fonts()
    fig, ax = plt.subplots(figsize=(12, 6))
    gender_ratio.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c'])
    ax.set_title('各专业男女比例', color='white')
    ax.set_xlabel('专业', color='white')
    ax.set_ylabel('比例 (%)', color='white')
    ax.tick_params(axis='x', colors='white', rotation=0)
    ax.tick_params(axis='y', colors='white')
    
    # 调整x轴标签为横向显示
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
    ax.legend(title='性别', labels=['男', '女'], frameon=False)
    for text in ax.get_legend().get_texts():
        text.set_color('white')
    ax.get_legend().get_title().set_color('white')
    
    # 去掉背景色
    ax.set_facecolor('none')
    fig.patch.set_facecolor('none')
    
    # 设置y轴范围为0-100%
    ax.set_ylim(0, 100)
    
    # 移除边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # 去掉所有网格线
    ax.grid(False)
    
    # 创建两列，将图表和数据显示在同一行
    col1, col2 = st.columns(2)
    
    with col1:
        st.pyplot(fig)
    
    with col2:
        # 显示详细比例数据
        st.subheader("性别比例数据")
        # 保留1位小数显示
        st.dataframe(gender_ratio.round(1))

    # 2. 各专业平均学习时间与成绩对比
    st.markdown("---")
    st.header("2. 各专业平均学习时间与成绩对比")

    # 设置中文字体支持（适用于本地和Cloud环境）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Arial Unicode MS', 'WenQuanYi Micro Hei', 'STXihei', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    # 计算各专业的平均学习时长、平均期中成绩和平均期末成绩
    study_performance = df.groupby('专业')[['每周学习时长（小时）', '期中考试分数', '期末考试分数']].mean()
    study_performance.columns = ['平均学习时长', '平均期中成绩', '平均期末成绩']

    # 创建图表
    setup_chinese_fonts()
    fig2, ax2 = plt.subplots(figsize=(12, 6))

    # 设置图表样式
    fig2.patch.set_facecolor('none')
    ax2.set_facecolor('none')

    # 绘制柱状图（平均学习时长）
    bars = ax2.bar(study_performance.index, study_performance['平均学习时长'], color='#1f77b4', alpha=0.8, label='平均学习时长')

    # 设置y轴标签（左侧）
    ax2.set_ylabel('平均学习时长（小时）', color='white')
    ax2.tick_params(axis='x', colors='white', rotation=0)
    ax2.tick_params(axis='y', colors='white')

    # 创建第二个y轴（右侧）用于显示成绩
    ax3 = ax2.twinx()
    ax3.set_facecolor('none')

    # 绘制折线图（平均期中成绩）
    line_mid = ax3.plot(study_performance.index, study_performance['平均期中成绩'], 'o-', color='#ff7f0e', linewidth=2, markersize=6, label='平均期中成绩')

    # 绘制折线图（平均期末成绩）
    line_final = ax3.plot(study_performance.index, study_performance['平均期末成绩'], 'o-', color='#2ca02c', linewidth=2, markersize=6, label='平均期末成绩')

    # 设置第二个y轴标签
    ax3.set_ylabel('平均成绩', color='white')
    ax3.tick_params(axis='y', colors='white')

    # 设置图表标题
    ax2.set_title('各专业平均学习时间与成绩对比', color='white')
    ax2.set_xlabel('专业', color='white')

    # 调整x轴标签为横向显示
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0, ha='center')

    # 设置图例（只显示三个指标）
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D

    # 创建自定义图例元素
    legend_elements = [
        Patch(facecolor='#1f77b4', edgecolor='#1f77b4', alpha=0.8, label='平均学习时长'),
        Line2D([0], [0], marker='o', color='#ff7f0e', linestyle='-', linewidth=2, markersize=6, label='平均期中成绩'),
        Line2D([0], [0], marker='o', color='#2ca02c', linestyle='-', linewidth=2, markersize=6, label='平均期末成绩')
    ]

    ax2.legend(handles=legend_elements, frameon=False, labelcolor='white', loc='upper left')

    # 移除边框
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)

    # 去掉所有网格线
    ax2.grid(False)
    ax3.grid(False)

    # 设置y轴范围
    ax2.set_ylim(20, 21)  # 平均学习时长范围设置为20-21小时
    ax3.set_ylim(70, 80)  # 平均期中成绩和平均期末成绩范围设置为70-80分

    # 创建两列，将图表和详细数据显示在同一行
    col3, col4 = st.columns(2)

    with col3:
        st.pyplot(fig2)

    with col4:
        # 显示详细数据
        st.subheader("详细数据")
        # 显示原始平均值数据，保留1位小数
        st.dataframe(study_performance.round(1))

    # 3. 各专业出勤率分析
    st.markdown("---")
    st.header("3. 各专业出勤率分析")

    # 设置中文字体支持（适用于本地和Cloud环境）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Arial Unicode MS', 'WenQuanYi Micro Hei', 'STXihei', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    # 计算各专业的平均出勤率
    attendance_data = df.groupby('专业')['上课出勤率'].mean()
    attendance_data = attendance_data.sort_values(ascending=False)

    # 创建两列布局
    col5, col6 = st.columns(2)

    with col5:
        # 创建图表
        setup_chinese_fonts()
        fig3, ax4 = plt.subplots(figsize=(12, 6))
        
        # 设置图表样式
        fig3.patch.set_facecolor('none')
        ax4.set_facecolor('none')
        
        # 生成颜色渐变
        from matplotlib import cm
        colors = cm.viridis(attendance_data.values / max(attendance_data.values))
        
        # 绘制柱状图
        bars = ax4.bar(attendance_data.index, attendance_data.values * 100, color=colors)
        
        # 设置标题和标签
        ax4.set_title('各专业平均出勤率', color='white')
        ax4.set_xlabel('专业', color='white')
        ax4.set_ylabel('出勤率 (%)', color='white')
        
        # 设置坐标轴样式
        ax4.tick_params(axis='x', colors='white', rotation=0)
        ax4.tick_params(axis='y', colors='white')
        
        # 移除边框
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        ax4.spines['left'].set_visible(False)
        ax4.spines['bottom'].set_visible(False)
        
        # 去掉网格线
        ax4.grid(False)
        
        # 设置y轴范围
        ax4.set_ylim(0, 100)
        
        # 显示图表
        st.pyplot(fig3)

    with col6:
        # 显示出勤率排名
        st.subheader("出勤率排名")
        
        # 创建排名数据框
        attendance_rank = pd.DataFrame({
            '专业': attendance_data.index,
            '平均出勤率': (attendance_data.values * 100).round(1)
        })
        
        # 添加排名列
        attendance_rank['排名'] = range(1, len(attendance_rank) + 1)
        
        # 重新排列列顺序
        attendance_rank = attendance_rank[['排名', '专业', '平均出勤率']]
        
        # 显示排名表
        st.dataframe(attendance_rank, hide_index=True)

    # 4. 大数据管理专业专项分析
    st.markdown("---")
    st.header("4. 大数据管理专业专项分析")

    # 设置中文字体支持（适用于本地和Cloud环境）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Arial Unicode MS', 'WenQuanYi Micro Hei', 'STXihei', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    # 筛选大数据管理专业的数据
    db_major_data = df[df['专业'] == '大数据管理'].copy()

    # 计算关键指标
    if not db_major_data.empty:
        # 计算平均出勤率
        avg_attendance = db_major_data['上课出勤率'].mean() * 100
        
        # 计算平均成绩（期中考试和期末考试的平均值）
        avg_score = (db_major_data['期中考试分数'].mean() + db_major_data['期末考试分数'].mean()) / 2
        
        # 计算及格率（期中考试和期末考试都及格的学生比例）
        passed_students = db_major_data[(db_major_data['期中考试分数'] >= 60) & (db_major_data['期末考试分数'] >= 60)]
        pass_rate = (len(passed_students) / len(db_major_data)) * 100
        
        # 计算平均学习时长
        avg_study_time = db_major_data['每周学习时长（小时）'].mean()

        # 创建概览卡片
        col_overview1, col_overview2, col_overview3, col_overview4 = st.columns(4)
        
        with col_overview1:
            st.markdown(f"<div style='background-color: #1e1e1e; border-radius: 8px; padding: 16px; text-align: center;'><div style='font-size: 18px; color: #e0e0e0; margin-bottom: 8px;'>平均出勤率</div><div style='font-size: 24px; color: #4CAF50; font-weight: bold;'>{avg_attendance:.1f}%</div></div>", unsafe_allow_html=True)
        
        with col_overview2:
            st.markdown(f"<div style='background-color: #1e1e1e; border-radius: 8px; padding: 16px; text-align: center;'><div style='font-size: 18px; color: #e0e0e0; margin-bottom: 8px;'>平均成绩</div><div style='font-size: 24px; color: #2196F3; font-weight: bold;'>{avg_score:.1f}分</div></div>", unsafe_allow_html=True)
        
        with col_overview3:
            st.markdown(f"<div style='background-color: #1e1e1e; border-radius: 8px; padding: 16px; text-align: center;'><div style='font-size: 18px; color: #e0e0e0; margin-bottom: 8px;'>及格率</div><div style='font-size: 24px; color: #FFC107; font-weight: bold;'>{pass_rate:.1f}%</div></div>", unsafe_allow_html=True)
        
        with col_overview4:
            st.markdown(f"<div style='background-color: #1e1e1e; border-radius: 8px; padding: 16px; text-align: center;'><div style='font-size: 18px; color: #e0e0e0; margin-bottom: 8px;'>平均学习时间</div><div style='font-size: 24px; color: #9C27B0; font-weight: bold;'>{avg_study_time:.1f}小时</div></div>", unsafe_allow_html=True)

        # 创建图表区域
        st.subheader("大数据管理专业学生数据分析")
        
        # 创建图表
        setup_chinese_fonts()
        fig4, ax5 = plt.subplots(figsize=(12, 6))
        
        # 设置图表样式
        fig4.patch.set_facecolor('none')
        ax5.set_facecolor('none')
        
        # 合并期中考试和期末考试成绩
        all_scores = pd.concat([db_major_data['期中考试分数'], db_major_data['期末考试分数']])
        
        # 绘制直方图
        n, bins, patches = ax5.hist(all_scores, bins=20, color='#4CAF50', alpha=0.8)
        
        # 设置标题和标签
        ax5.set_title('大数据管理专业学生成绩分布', color='white')
        ax5.set_xlabel('成绩', color='white')
        ax5.set_ylabel('学生人数', color='white')
        
        # 设置坐标轴样式
        ax5.tick_params(axis='x', colors='white')
        ax5.tick_params(axis='y', colors='white')
        
        # 移除边框
        ax5.spines['top'].set_visible(False)
        ax5.spines['right'].set_visible(False)
        ax5.spines['left'].set_visible(False)
        ax5.spines['bottom'].set_visible(False)
        
        # 去掉网格线
        ax5.grid(False)
        
        # 显示图表
        st.pyplot(fig4)
    else:
        st.info("暂无大数据管理专业学生数据")

elif selected_menu == "成绩预测":
    # 加载数据和模型
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(current_dir, 'student.csv'))
    with open(os.path.join(current_dir, 'student_rf_model.pkl'), 'rb') as f:
        model = pickle.load(f)
    
    # 获取专业列表
    majors = df['专业'].unique().tolist()
    
    st.title("期末成绩预测")
    st.markdown("---")
    
    # 添加提示文本
    st.markdown("输入学生学习信息，系统将预测期末考试成绩并提供学习建议")
    
    # 创建预测表单
    with st.form(key='prediction_form'):
        # 左右两列布局
        col1, col2 = st.columns(2)
        
        with col1:
            # 左侧输入字段
            student_id = st.text_input("学号")
            gender = st.selectbox("性别", ['男', '女'])
            major = st.selectbox("专业", majors)
        
        with col2:
            # 右侧输入字段
            study_hours = st.number_input("每周学习时长（小时）", min_value=0.0, max_value=50.0, value=15.0)
            attendance_rate = st.number_input("上课出勤率", min_value=0.0, max_value=1.0, value=0.85)
            midterm_score = st.number_input("期中考试分数", min_value=0.0, max_value=100.0, value=80.0)
            homework_rate = st.number_input("作业完成率", min_value=0.0, max_value=1.0, value=0.85)
        
        # 提交按钮
        submit_button = st.form_submit_button(label='预测成绩')
    
    # 处理预测请求
    if submit_button:
        # 构建基础输入数据
        base_data = {
            '每周学习时长（小时）': [study_hours],
            '上课出勤率': [attendance_rate],
            '期中考试分数': [midterm_score],
            '作业完成率': [homework_rate]
        }
        
        # 添加性别独热编码
        base_data['性别_女'] = [1 if gender == '女' else 0]
        base_data['性别_男'] = [1 if gender == '男' else 0]
        
        # 添加专业独热编码
        for m in ['人工智能', '大数据管理', '工商管理', '电子商务', '财务管理']:
            base_data[f'专业_{m}'] = [1 if major == m else 0]
        
        # 构建完整输入数据
        input_data = pd.DataFrame(base_data)
        
        # 进行预测
        prediction = model.predict(input_data)
        predicted_score = prediction[0]
        
        # 显示结果
        st.markdown("---")
        st.header("预测结果")
        
        if predicted_score >= 60:
            st.success(f"预测期末成绩: {predicted_score:.2f} 分")
            try:
                image_path = os.path.join(current_dir, "images/4.png")
                st.image(image_path, width="content")
            except Exception as e:
                st.balloons()
        else:
            st.warning(f"预测期末成绩: {predicted_score:.2f} 分")
            try:
                image_path = os.path.join(current_dir, "images/5.png")
                st.image(image_path, width="content")
            except Exception as e:
                pass