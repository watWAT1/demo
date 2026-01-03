import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import plotly.graph_objects as go

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
    
    # 绘制比例柱状图 - 使用Plotly
    fig = go.Figure()
    
    # 添加男性柱状图
    fig.add_trace(go.Bar(
        name='男',
        x=gender_ratio.index,
        y=gender_ratio['男'],
        marker_color='#3498db',
        yaxis='y1'
    ))
    
    # 添加女性柱状图
    fig.add_trace(go.Bar(
        name='女',
        x=gender_ratio.index,
        y=gender_ratio['女'],
        marker_color='#e74c3c',
        yaxis='y1'
    ))
    
    # 更新布局
    fig.update_layout(
        title='各专业男女比例',
        xaxis_title='专业',
        yaxis_title='比例 (%)',
        yaxis=dict(range=[0, 100], color='white'),
        xaxis=dict(color='white'),
        legend=dict(title='性别', title_font_color='white', font_color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        barmode='group'
    )
    
    # 创建两列，将图表和数据显示在同一行
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
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

    # 创建图表 - 使用Plotly
    fig = go.Figure()
    
    # 添加平均学习时长柱状图（左侧y轴）
    fig.add_trace(go.Bar(
        name='平均学习时长',
        x=study_performance.index,
        y=study_performance['平均学习时长'],
        marker_color='#1f77b4',
        yaxis='y1'
    ))
    
    # 添加平均期中成绩折线图（右侧y轴）
    fig.add_trace(go.Scatter(
        name='平均期中成绩',
        x=study_performance.index,
        y=study_performance['平均期中成绩'],
        mode='lines+markers',
        marker_color='#ff7f0e',
        line=dict(width=2),
        marker=dict(size=6),
        yaxis='y2'
    ))
    
    # 添加平均期末成绩折线图（右侧y轴）
    fig.add_trace(go.Scatter(
        name='平均期末成绩',
        x=study_performance.index,
        y=study_performance['平均期末成绩'],
        mode='lines+markers',
        marker_color='#2ca02c',
        line=dict(width=2),
        marker=dict(size=6),
        yaxis='y2'
    ))
    
    # 更新布局
    fig.update_layout(
        title='各专业平均学习时间与成绩对比',
        xaxis_title='专业',
        xaxis=dict(color='white'),
        yaxis=dict(
            title='平均学习时长（小时）',
            color='white',
            range=[20, 21],
            showgrid=False
        ),
        yaxis2=dict(
            title='平均成绩',
            color='white',
            range=[70, 80],
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(font_color='white', bgcolor='rgba(0,0,0,0)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # 创建两列，将图表和详细数据显示在同一行
    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(fig, use_container_width=True)

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
        # 创建图表 - 使用Plotly
        fig = go.Figure()
        
        # 计算颜色值（基于出勤率）
        max_attendance = max(attendance_data.values)
        normalized_attendance = attendance_data.values / max_attendance
        
        # 添加柱状图
        fig.add_trace(go.Bar(
            x=attendance_data.index,
            y=attendance_data.values * 100,
            marker=dict(
                color=attendance_data.values * 100,
                colorscale='Viridis'
            ),
            yaxis='y1'
        ))
        
        # 更新布局
        fig.update_layout(
            title='各专业出勤率分析',
            xaxis_title='专业',
            xaxis=dict(color='white'),
            yaxis_title='出勤率 (%)',
            yaxis=dict(color='white', range=[0, 100], showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        # 显示图表
        st.plotly_chart(fig, use_container_width=True)

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
        
        # 合并期中考试和期末考试成绩
        all_scores = pd.concat([db_major_data['期中考试分数'], db_major_data['期末考试分数']])
        
        # 创建直方图 - 使用Plotly
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=all_scores,
            nbinsx=20,
            marker_color='#4CAF50',
            opacity=0.8
        ))
        
        # 设置图表布局
        fig.update_layout(
            title='大数据管理专业学生成绩分布',
            xaxis_title='成绩',
            yaxis_title='学生人数',
            xaxis=dict(color='white'),
            yaxis=dict(color='white'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        # 显示图表
        st.plotly_chart(fig, use_container_width=True)
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