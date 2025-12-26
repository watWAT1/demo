import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# 设置页面配置
st.set_page_config(
    page_title="多功能应用平台", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化session state用于页面导航
if 'current_page' not in st.session_state:
    st.session_state.current_page = "美食数据仪表盘"

# 创建顶部导航栏
st.markdown("""
<style>
    .top-nav {
        display: flex;
        justify-content: center;
        background-color: #f0f2f6;
        padding: 10px 0;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    .nav-item {
        padding: 10px 20px;
        margin: 0 5px;
        border-radius: 5px;
        cursor: pointer;
        text-align: center;
        flex: 1;
        max-width: 200px;
    }
    .nav-item:hover {
        background-color: #e6f3ff;
    }
    .nav-item.active {
        background-color: #02ab21;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 创建顶部导航菜单
pages = ["🍜 美食数据", "📄 简历生成", "⚔️ 亚索介绍", "🐒 动物园相册", "🎵 音乐播放", "📺 视频中心"]
page_mapping = {
    "🍜 美食数据": "美食数据仪表盘",
    "📄 简历生成": "个人简历生成器", 
    "⚔️ 亚索介绍": "亚索英雄介绍",
    "🐒 动物园相册": "动物园轮播相册",
    "🎵 音乐播放": "音乐播放器",
    "📺 视频中心": "视频中心"
}

# 创建导航按钮
cols = st.columns(len(pages))
for i, page in enumerate(pages):
    with cols[i]:
        if st.button(page, use_container_width=True, key=f"nav_{i}"):
            st.session_state.current_page = page_mapping[page]
            st.rerun()

# 显示当前页面标题
st.markdown(f"## {st.session_state.current_page}")

# 根据选择显示不同页面
if st.session_state.current_page == "美食数据仪表盘":
    # === 美食数据仪表盘页面 ===
    st.title("🍜 南宁美食数据分析仪表盘")
    st.markdown("展示南宁本地美食信息，包括餐厅评分、价格走势和地理位置分布")

    # 1. 南宁餐厅基本信息数据框
    restaurants_data = {
        "餐厅名称": ["舒记老友粉（七星路店）", "桂小厨广西菜（万象城店）", "乌布花园餐厅（青山店）", 
                  "甘家界柠檬鸭(春晖店)", "米马河（竹塘路总店）", "海底捞火锅(航洋店)", 
                  "丫丫厨娘·柠檬鸭（西关店）", "南湖名都大饭店·景湖轩", "鱼上·黑豆花烤鱼（万象城店）"],
        "菜系类型": ["小吃快餐", "广西菜", "东南亚料理", "广西菜", "广西菜", "火锅", 
                  "广西菜", "自助餐", "川菜烤鱼"],
        "评分": [4.4, 4.6, 4.6, 5.0, 4.3, 4.6, 4.5, 4.8, 4.2],
        "人均价格(元)": [25, 85, 120, 80, 60, 110, 75, 180, 70],
        "评论数量": [840, 839, 183, 54, 224, 1200, 48, 56, 247],
        "区域": ["青秀区", "青秀区", "青秀区", "青秀区", "青秀区", "青秀区", "西乡塘区", "青秀区", "青秀区"],
        "latitude": [22.815, 22.812, 22.806, 22.817, 22.819, 22.811, 22.824, 22.802, 22.812],
        "longitude": [108.321, 108.372, 108.366, 108.369, 108.351, 108.375, 108.319, 108.358, 108.372]
    }

    # 创建餐厅数据框
    restaurants_df = pd.DataFrame(restaurants_data)
    restaurants_df.index = pd.Series(range(1, len(restaurants_df)+1), name='序号')

    # 2. 创建5家餐厅12个月的价格走势数据
    months = [f'{i}月' for i in range(1, 13)]
    price_trend_data = {
        "月份": months * 5,
        "餐厅": (["舒记老友粉"]*12 + ["桂小厨广西菜"]*12 + ["乌布花园餐厅"]*12 + 
               ["甘家界柠檬鸭"]*12 + ["海底捞火锅"]*12),
        "人均价格": [25, 24, 26, 25, 26, 27, 28, 27, 26, 25, 26, 24,
                  85, 82, 84, 86, 88, 90, 92, 91, 89, 87, 85, 83,
                  120, 125, 130, 128, 132, 135, 140, 138, 142, 145, 148, 150,
                  80, 78, 82, 85, 83, 80, 78, 82, 85, 88, 86, 84,
                  110, 112, 115, 118, 120, 122, 125, 123, 121, 119, 117, 115]
    }

    # 创建价格走势数据框
    price_trend_df = pd.DataFrame(price_trend_data)
    pivot_df = price_trend_df.pivot(index='月份', columns='餐厅', values='人均价格')
    pivot_df = pivot_df.reindex(months)

    # 3. 开始创建仪表盘界面
    # 展示关键指标
    st.header("📊 南宁美食关键指标")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("餐厅数量", len(restaurants_df))

    with col2:
        avg_price = restaurants_df['人均价格(元)'].mean()
        st.metric("平均人均价格", f"¥{avg_price:.1f}")

    with col3:
        avg_rating = restaurants_df['评分'].mean()
        st.metric("平均评分", f"{avg_rating:.1f}/5.0")

    with col4:
        total_reviews = restaurants_df['评论数量'].sum()
        st.metric("总评论数", f"{total_reviews}")

    # 展示餐厅数据表格
    st.header("📋 南宁餐厅详细信息")
    st.dataframe(
        restaurants_df[['餐厅名称', '菜系类型', '评分', '人均价格(元)', '评论数量', '区域']],
        use_container_width=True
    )

    # 创建多列布局
    col1, col2 = st.columns(2)

    # 左侧列：条形图和面积图
    with col1:
        st.header("📈 餐厅数据分析")
        
        # 条形图：各菜系平均评分对比
        st.subheader("各菜系平均评分对比（条形图）")
        cuisine_rating = restaurants_df.groupby('菜系类型')['评分'].mean().reset_index()
        cuisine_rating = cuisine_rating.sort_values('评分', ascending=False)
        st.bar_chart(cuisine_rating.set_index('菜系类型'))
        
        # 面积图：各区域餐厅数量分布
        st.subheader("各区域餐厅数量分布（面积图）")
        area_counts = restaurants_df['区域'].value_counts().reset_index()
        area_counts.columns = ['区域', '餐厅数量']
        area_counts = area_counts.sort_values('区域')
        st.area_chart(area_counts.set_index('区域'))

    # 右侧列：折线图和地图
    with col2:
        st.header("📊 价格趋势与地理位置")
        
        # 折线图：5家餐厅12个月价格走势
        st.subheader("5家餐厅12个月价格走势（折线图）")
        st.line_chart(pivot_df)
        
        # 地图：展示餐厅地理位置
        st.subheader("🗺️ 餐厅地理位置分布（地图）")
        
        # 准备地图数据
        map_data = restaurants_df[['latitude', 'longitude']].copy()
        map_data.columns = ['lat', 'lon']
        
        # 显示地图
        st.map(map_data)
        
        # 在地图下方显示对应的餐厅名称
        st.caption("地图标记对应的餐厅：")
        for idx, row in restaurants_df.iterrows():
            st.markdown(f"📍 **{row['餐厅名称']}** - {row['菜系类型']} (评分: {row['评分']}, 人均: ¥{row['人均价格(元)']})")

    # 价格趋势详细数据表格
    st.header("💰 价格趋势详细数据")
    st.write("以下是5家餐厅12个月的人均价格变化数据（单位：元）")
    st.dataframe(pivot_df, use_container_width=True)

elif st.session_state.current_page == "个人简历生成器":
    # === 个人简历生成器页面 ===
    # 初始化session state
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {
            'user_id': '231231231',
            'name': '',
            'phone': '',
            'birth_date': date(2025, 12, 25),
            'gender': '男',
            'education': '本科',
            'language': '中文',
            'skill': 'Python',
            'experience': 8,
            'salary_range': [10000, 20000],
            'introduction': '这个人很神秘，没有留下任何介绍...',
            'contact_time': '01:00'
        }

    # 应用标题
    st.title("📄 个人简历生成器")

    # 创建两列布局
    left_col, right_col = st.columns([1, 2])

    # 左侧输入区域
    with left_col:
        # 身份标识
        user_id = st.text_input(
            "身份标识",
            value=st.session_state.resume_data['user_id'],
            key="user_id_input"
        )
        
        # 出生日期 - 日历选择器
        st.write("出生日期")
        birth_date = st.date_input(
            "选择出生日期",
            value=st.session_state.resume_data['birth_date'],
            format="YYYY/MM/DD",
            label_visibility="collapsed"
        )
        
        # 性别选择 - 单选框
        gender = st.radio(
            "性别",
            options=["男", "女"],
            index=0,
            key="gender_input"
        )
        
        # 学历选择
        education = st.selectbox(
            "学历",
            options=["高中", "专科", "本科", "硕士", "博士", "其他"],
            index=2,
            key="education_input"
        )
        
        # 语言能力
        language = st.selectbox(
            "语言能力",
            options=["中文", "英语", "西班牙语", "法语", "德语", "日语", "韩语"],
            index=0,
            key="language_input"
        )
        
        # 班级信息
        class_info = st.text_input(
            "班级信息",
            value="22中本信管2班-python数据采",
            placeholder="请输入班级信息",
            key="class_info_input"
        )
        
        # 姓名输入
        name = st.text_input(
            "姓名",
            value=st.session_state.resume_data['name'],
            placeholder="请输入您的姓名",
            key="name_input"
        )
        
        # 手机号输入
        phone = st.text_input(
            "手机号",
            value=st.session_state.resume_data['phone'],
            placeholder="请输入您的手机号",
            key="phone_input"
        )
        
        # 技能选择
        skill = st.selectbox(
            "技能",
            options=["Python", "JavaScript", "HTML/CSS", "Java", "C++", "Go", "React", "Vue", "Node.js", "Docker", "Kubernetes", "AWS"],
            index=0,
            key="skill_input"
        )
        
        # 工作经验滑块
        experience = st.slider(
            "工作经验（年）",
            min_value=0,
            max_value=30,
            value=st.session_state.resume_data['experience'],
            key="experience_input"
        )
        
        # 期望薪资范围滑块
        salary_range = st.slider(
            "期望薪资范围（元）",
            min_value=5000,
            max_value=50000,
            value=st.session_state.resume_data['salary_range'],
            key="salary_input"
        )
        
        # 个人简介
        introduction = st.text_area(
            "个人简介",
            value=st.session_state.resume_data['introduction'],
            height=100,
            placeholder="请简要介绍您的专业背景、职业目标和个人特点...",
            key="introduction_input"
        )
        
        # 每日最佳联系时间段
        st.write("每日最佳联系时间段")
        contact_time = st.text_input(
            "输入时间（HH:MM格式）",
            value=st.session_state.resume_data['contact_time'],
            placeholder="01:00",
            label_visibility="collapsed",
            key="contact_time_input"
        )
        
        # 上传个人照片
        st.write("上传个人照片")
        uploaded_file = st.file_uploader(
            "Drag and drop file here\nLimit 200MB per file·JPG,JPEG,PNG",
            type=['png', 'jpg', 'jpeg'],
            label_visibility="collapsed",
            key="file_uploader"
        )
        
        # 保存按钮
        if st.button("保存信息", type="primary", key="save_button"):
            # 更新session state数据
            st.session_state.resume_data = {
                'user_id': user_id,
                'name': name,
                'phone': phone,
                'birth_date': birth_date,
                'gender': gender,
                'education': education,
                'language': language,
                'class_info': class_info,
                'skill': skill,
                'experience': experience,
                'salary_range': salary_range,
                'introduction': introduction if introduction else '这个人很神秘，没有留下任何介绍...',
                'contact_time': contact_time
            }
            
            st.success("信息已保存！")

    # 右侧信息显示区域
    with right_col:
        # 显示班级信息
        st.write(f"班级：{class_info}")
        
        # 显示姓名和手机号
        if st.session_state.resume_data['name']:
            st.header(st.session_state.resume_data['name'])
        
        if st.session_state.resume_data['phone']:
            st.write(f"手机号：{st.session_state.resume_data['phone']}")
        
        # 显示个人简历
        st.subheader("个人简历")
        st.write(st.session_state.resume_data['introduction'])
        
        # 显示上传的照片
        if uploaded_file is not None:
            st.image(uploaded_file, caption="个人照片", width=200)
        
        # 分隔线
        st.divider()
        
        # 显示专业技能
        st.subheader("专业技能")
        st.write(f"- {st.session_state.resume_data['skill']}")
        
        # 显示其他信息
        st.subheader("其他信息")
        
        # 身份标识
        st.write(f"身份标识：{st.session_state.resume_data['user_id']}")
        
        # 出生日期
        birth_date_str = st.session_state.resume_data['birth_date'].strftime("%Y/%m/%d")
        st.write(f"出生日期：{birth_date_str}")
        
        # 性别
        st.write(f"性别：{st.session_state.resume_data['gender']}")
        
        # 学历
        st.write(f"学历：{st.session_state.resume_data['education']}")
        
        # 语言能力
        st.write(f"语言能力：{st.session_state.resume_data['language']}")
        
        # 工作经验
        st.write(f"工作经验：{st.session_state.resume_data['experience']}年")
        
        # 期望薪资
        salary_min, salary_max = st.session_state.resume_data['salary_range']
        st.write(f"期望薪资：{salary_min:,} - {salary_max:,}元")
        
        # 每日最佳联系时间段
        st.write(f"每日最佳联系时间段：{st.session_state.resume_data['contact_time']}")

elif st.session_state.current_page == "亚索英雄介绍":
    # === 亚索英雄介绍页面 ===
    # 自定义CSS样式
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        
        body {
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            font-family: 'Orbitron', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
        }
        
        .hero-card {
            background: rgba(30, 30, 50, 0.8);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid #3498db;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
        }
        
        .skill-card {
            background: rgba(20, 20, 40, 0.9);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #3498db;
            margin-bottom: 15px;
        }
        
        .title-gradient {
            background: linear-gradient(90deg, #3498db, #f39c12);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 2.5rem;
        }
        
        .section-title {
            color: #3498db;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 15px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        
        .stat-box {
            background: rgba(40, 40, 60, 0.8);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            border: 1px solid #3498db;
        }
        
        .code-block {
            background: rgba(20, 20, 40, 0.9);
            border-radius: 8px;
            padding: 15px;
            font-family: monospace;
            border: 1px solid #3498db;
        }
        
        .highlight {
            color: #f39c12;
            font-weight: bold;
        }
        
        .mastery-display {
            text-align: center;
            font-size: 3rem;
            color: #ffffff;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # 标题
    st.markdown("<h1 class='title-gradient'>⚔️ 亚索 - 疾风剑豪</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>来自艾欧尼亚的流浪剑客</p>", unsafe_allow_html=True)

    # 英雄背景故事
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>📖 英雄背景</h2>", unsafe_allow_html=True)
    st.markdown("""
    亚索，一位追求极致速度的剑客，他的一生都在追寻自己的兄长——永恩。在故乡艾欧尼亚，亚索被指控杀害了自己的哥哥，为了洗清罪名，他踏上了流浪的旅程。

    > "死亡，如同生时一样，我行我素，没有意义。"

    亚索手持一把名为"铁脊"的剑，身披飘逸的斗篷，他的剑术如风一般迅捷，每一次出剑都带着致命的精准。他相信命运，但更相信自己的剑技，在艾欧尼亚的各个角落，他都在寻找真相，也在寻找自己的归宿。
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 英雄数据
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>📊 英雄数据</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='stat-box'><h3>攻击</h3><p class='highlight'>8</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stat-box'><h3>防御</h3><p class='highlight'>3</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='stat-box'><h3>法术</h3><p class='highlight'>2</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='stat-box'><h3>难度</h3><p class='highlight'>7</p></div>", unsafe_allow_html=True)

    # 英雄熟练度
    st.markdown("<h3 style='margin-top: 20px; color: #3498db; text-align: center;'>英雄熟练度</h3>", unsafe_allow_html=True)
    st.metric(label="总体熟练度", value="114514", delta="↑ 100%")
    st.markdown("</div>", unsafe_allow_html=True)

    # 技能数据表格
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>⚔️ 技能数据</h2>", unsafe_allow_html=True)

    # 创建技能数据表格
    skill_data = {
        '技能名称': ['斩钢闪 (Q)', '风之障壁 (W)', '踏前斩 (E)', '狂风绝息斩 (R)'],
        '冷却时间': ['1.5秒', '22/20.5/19/17.5/16秒', '38/34/30/26/22秒', '80/65/50秒'],
        '法力消耗': ['30', '50', '40', '100'],
        '范围': ['400', '指定位置', '475', '目标']
    }

    skill_df = pd.DataFrame(skill_data)
    st.table(skill_df)
    st.markdown("</div>", unsafe_allow_html=True)

    # 技能介绍
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>⚔️ 技能介绍</h2>", unsafe_allow_html=True)

    # 技能1 - 斩钢闪
    st.markdown("<div class='skill-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #3498db;'>🗡️ 斩钢闪 (Q)</h3>", unsafe_allow_html=True)
    st.markdown("""
    一次无目标锁定的普通攻击，命中后可获得旋风烈斩效果，积攒两层后会形成击飞敌人的旋风。

    **冷却时间**: 1.5秒  
    **消耗**: 30法力  
    **范围**: 400
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 技能2 - 风之障壁 (W)
    st.markdown("<div class='skill-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #3498db;'>🛡️ 风之障壁 (W)</h3>", unsafe_allow_html=True)
    st.markdown("""
    形成一个气流之墙，阻挡敌方的飞行道具。

    **冷却时间**: 22/20.5/19/17.5/16秒  
    **消耗**: 50法力
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 技能3 - 踏前斩 (E)
    st.markdown("<div class='skill-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #3498db;'>⚡ 踏前斩 (E)</h3>", unsafe_allow_html=True)
    st.markdown("""
    突进到一个单位身边，造成逐步提升的魔法伤害。

    **冷却时间**: 38/34/30/26/22秒  
    **消耗**: 40法力  
    **范围**: 475
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 技能4 - 狂风绝息斩 (R)
    st.markdown("<div class='skill-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #3498db;'>🌪️ 狂风绝息斩 (R)</h3>", unsafe_allow_html=True)
    st.markdown("""
    突进到一个单位身边并进行多次击打，造成重度伤害，仅对被击飞的单位施放。

    **冷却时间**: 80/65/50秒  
    **消耗**: 100法力
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 装备推荐
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>🛡️ 装备推荐</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 核心装备")
        st.markdown("""
        - 幽梦之灵
        - 黑色切割者
        - 死亡之舞
        """)
    with col2:
        st.markdown("#### 防御装备")
        st.markdown("""
        - 水银之靴
        - 狂徒铠甲
        - 挺进破坏者
        """)
    with col3:
        st.markdown("#### 奢华装备")
        st.markdown("""
        - 灵巧披风
        - 饮血剑
        - 狂热
        """)
    st.markdown("</div>", unsafe_allow_html=True)

    # 对战技巧
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>💡 对战技巧</h2>", unsafe_allow_html=True)
    st.markdown("""
    **前期**: 利用Q技能的快速冷却进行补刀和骚扰，注意不要过度消耗法力。

    **中期**: 积极游走，利用E技能的位移和R技能的击飞来配合队友。

    **后期**: 作为团队的前排刺客，利用风墙保护队友，寻找敌方C位进行击杀。

    **小贴士**: 
    - 风墙可以阻挡很多关键技能，如寒冰的箭、卡特的飞镖等
    - E技能的击飞可以打断敌方技能
    - R技能命中后，亚索会获得大量攻击速度，适合追击
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 代码示例
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>💻 亚索技能逻辑</h2>", unsafe_allow_html=True)
    st.code("""
    def yaso_skill():
        while True:
            if detect_enemy():
                use_q()  # 斩钢闪
                use_e()  # 踏前斩
                if enemy_low_hp():
                    use_r()  # 狂风绝息斩
                return "ENEMY ELIMINATED"
            else:
                use_w()  # 风之障壁
                dash()

    # SYSTEM MESSAGE: 目标已锁定...
    # TARGET: 敌方ADC
    # COUNTDOWN: 2025-06-03 15:24:58
    # 系统状态: 在线 | 连接状态: 已加密
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # 底部信息
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #888;'>亚索 - 疾风剑豪 | 艾欧尼亚的流浪剑客</p>", unsafe_allow_html=True)

elif st.session_state.current_page == "动物园轮播相册":
    # === 动物园轮播相册页面 ===
    st.title("🐒 动物园轮播相册")
    st.markdown("---")

    # 图片数组
    images = [
        'https://www.allaboutbirds.org/guide/assets/og/75712701-1200px.jpg',
        'https://image.petmd.com/files/styles/863x625/public/CANS_dogsmiling_379727605.jpg',
        'https://images2.alphacoders.com/716/71660.jpg'
    ]

    # 图片标题
    captions = ['小鸟', '小狗', '大猫']

    # 初始化 session_state
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    # 计算总图片数
    total_images = len(images)

    # 显示当前图片信息
    st.subheader(f"图片 {st.session_state.current_index + 1} / {total_images}")

    # 显示当前图片
    current_image = images[st.session_state.current_index]
    current_caption = captions[st.session_state.current_index]

    st.image(current_image, caption=current_caption, use_column_width=True)

    # 控制按钮
    st.markdown("### 控制按钮")

    # 创建控制按钮行
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("◀️ 上一张", use_container_width=True):
            st.session_state.current_index = (st.session_state.current_index - 1) % total_images
            st.rerun()

    with col2:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 20px;'>第 {st.session_state.current_index + 1} 张</div>", unsafe_allow_html=True)

    with col3:
        if st.button("下一张 ▶️", use_container_width=True):
            st.session_state.current_index = (st.session_state.current_index + 1) % total_images
            st.rerun()

    # 添加图片选择滑块
    st.markdown("### 快速选择")
    selected_idx = st.slider(
        "选择图片", 
        min_value=1, 
        max_value=total_images, 
        value=st.session_state.current_index+1,
        key="image_slider"
    )
    
    if selected_idx != st.session_state.current_index + 1:
        st.session_state.current_index = selected_idx - 1
        st.rerun()

elif st.session_state.current_page == "音乐播放器":
    # === 音乐播放器页面 ===
    st.title("🎵 音乐播放器")
    
    # 歌库
    SONGS = {
        "1": {
            "name": "罗生门（Follow）",
            "artist": "梨冻紧 / Wiz_H张子豪",
            "album": "罗生门（Follow）",
            "url": "https://music.163.com/song/media/outer/url?id=1456890009.mp3",
            "pic": "http://p2.music.126.net/yN1ke1xYMJ718FiHaDWtYQ==/109951165076380471.jpg",
        },
        "2": {
            "name": "如果呢",
            "artist": "郑润泽",
            "album": "如果呢",
            "url": "https://music.163.com/song/media/outer/url?id=1842728629.mp3",
            "pic": "http://p2.music.126.net/-xMsNLpquZTmMZlIztTgHg==/109951165953469081.jpg",
        },
        "3": {
            "name": "苦茶子",
            "artist": "Starling8 / MoreLearn 27 / FIVESTAR",
            "album": "埋汰",
            "url": "https://music.163.com/song/media/outer/url?id=1922888354.mp3",
            "pic": "http://p1.music.126.net/VjXYNoGC3lXajZDs0r35XQ==/109951167852652412.jpg",
        },
    }

    # session 状态
    if "sid" not in st.session_state:
        st.session_state.sid = "1"  # 默认第一首

    if "pick" not in st.session_state:
        st.session_state.pick = "1"

    def switch_song():
        st.session_state.sid = st.session_state.pick
        st.rerun()

    def prev_song():
        song_ids = list(SONGS.keys())
        current_idx = song_ids.index(st.session_state.sid)
        prev_idx = (current_idx - 1) % len(song_ids)
        st.session_state.sid = song_ids[prev_idx]
        st.session_state.pick = st.session_state.sid
        st.rerun()

    def next_song():
        song_ids = list(SONGS.keys())
        current_idx = song_ids.index(st.session_state.sid)
        next_idx = (current_idx + 1) % len(song_ids)
        st.session_state.sid = song_ids[next_idx]
        st.session_state.pick = st.session_state.sid
        st.rerun()

    # 页面布局
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(SONGS[st.session_state.sid]["pic"], width=240)
        
        # 添加播放列表
        st.markdown("### 播放列表")
        for song_id, song_info in SONGS.items():
            is_current = song_id == st.session_state.sid
            if is_current:
                st.markdown(f"▶️ **{song_info['name']}**")
            else:
                if st.button(f"🎵 {song_info['name']}", key=f"play_{song_id}", use_container_width=True):
                    st.session_state.sid = song_id
                    st.session_state.pick = song_id
                    st.rerun()

    with col2:
        st.markdown("### 正在播放")
        st.markdown(f"**歌曲：** {SONGS[st.session_state.sid]['name']}")
        st.markdown(f"**歌手：** {SONGS[st.session_state.sid]['artist']}")
        st.markdown(f"**专辑：** {SONGS[st.session_state.sid]['album']}")
        
        # 歌曲进度模拟
        st.markdown("### 播放进度")
        st.progress(0.5)  # 模拟50%播放进度
        
        col_time1, col_time2, col_time3 = st.columns(3)
        with col_time1:
            st.markdown("**2:30**")
        with col_time2:
            st.markdown("<div style='text-align: center;'>播放中</div>", unsafe_allow_html=True)
        with col_time3:
            st.markdown("<div style='text-align: right;'>5:00</div>", unsafe_allow_html=True)

        # 歌曲选择下拉框
        options = {k: f"{v['name']} - {v['artist']}" for k, v in SONGS.items()}
        st.selectbox(
            "切换歌曲",
            options.keys(),
            format_func=lambda x: options[x],
            key="pick",
            on_change=switch_song,
        )

        # 播放控制按钮
        st.markdown("### 播放控制")
        col_control1, col_control2, col_control3 = st.columns([1, 1, 1])
        
        with col_control1:
            st.button("⏮️ 上一首", on_click=prev_song, use_container_width=True)
        with col_control2:
            st.button("⏸️ 暂停/播放", use_container_width=True)
        with col_control3:
            st.button("⏭️ 下一首", on_click=next_song, use_container_width=True)

        # 音量控制
        st.markdown("### 音量控制")
        st.slider("音量", 0, 100, 80, key="volume")

        # 音频播放器
        st.markdown("### 音频播放器")
        st.audio(SONGS[st.session_state.sid]["url"], format="audio/mp3")

else:
    # === 视频中心页面 ===
    st.title("📺 视频中心")
    
    video_arr = [
        {
            'url': 'http://upos-sz-mirrorcos.bilivideo.com/upgcxcode/51/70/25642407051/25642407051-1-192.mp4?e=ig8euxZM2rNcNbRB7zdVhwdlhWUahwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&platform=html5&og=ali&trid=6bdc59c2e99f4c4fafa11112fbe396dO&mid=0&gen=playurlv3&os=estgoss&oi=2067284620&deadline=1766567924&uipk=5&nbs=1&upsig=f2d7c34000fb702b0f4a72205410a1b8&uparams=e,platform,og,trid,mid,gen,os,oi,deadline,uipk,nbs&bvc=vod&nettype=1&bw=1263404&dl=0&f=O_0_0&agrr=1&buvid=&build=7330300&orderid=0,3',
            'title': '熊出没之夏日连连看第一集：纳凉地争夺战'
        },
        {
            'url': 'http://upos-sz-mirrorcos.bilivideo.com/upgcxcode/40/71/25642407140/25642407140-1-192.mp4?e=ig8euxZM2rNcNbRBnwdVhwdlhWU3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&mid=0&deadline=1766568019&uipk=5&platform=html5&trid=14c4abe26b064af2b7ea8dd0bed1d26O&gen=playurlv3&og=cos&nbs=1&oi=1385955528&os=estgcos&upsig=1b0d93bfc9d33fc6d05bec3bde0978b0&uparams=e,mid,deadline,uipk,platform,trid,gen,og,nbs,oi,os&bvc=vod&nettype=1&bw=1266029&agrr=1&buvid=&build=7330300&dl=0&f=O_0_0&orderid=0,3',
            'title': '熊出没之夏日连连看第二集：强哥山庄'
        },
        {
            'url': 'http://upos-sz-mirrorcos.bilivideo.com/upgcxcode/46/70/25642407046/25642407046-1-192.mp4?e=ig8euxZM2rNcNbRBhwdVhwdlhWUVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&nbs=1&mid=0&os=08cbv&og=hw&deadline=1766568113&uipk=5&platform=html5&trid=0c6e144c8d7d45a2b5c7537afb80336O&gen=playurlv3&oi=1385955528&upsig=3a8dde8cc1ffbc17d71bdfa54106d01c&uparams=e,nbs,mid,os,og,deadline,uipk,platform,trid,gen,oi&bvc=vod&nettype=1&bw=1207415&f=O_0_0&agrr=1&buvid=&build=7330300&dl=0&orderid=0,3',
            'title': '熊出没之夏日连连看第三集：萤火虫之夜'
        }
    ]

    if 'ind' not in st.session_state:
        st.session_state['ind'] = 0

    # 显示当前视频
    st.header(video_arr[st.session_state['ind']]['title'])
    st.video(video_arr[st.session_state['ind']]['url'])
    
    # 添加视频播放信息
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("当前播放", f"第{st.session_state['ind'] + 1}集")
    with col_info2:
        st.metric("总集数", len(video_arr))
    with col_info3:
        st.metric("播放状态", "正在播放")

    st.markdown("---")
    
    # 播放控制
    st.markdown("### 播放控制")
    col_control1, col_control2, col_control3, col_control4, col_control5 = st.columns(5)
    
    with col_control1:
        if st.button("⏪ 上一集", use_container_width=True, key="video_prev"):
            st.session_state['ind'] = (st.session_state['ind'] - 1) % len(video_arr)

    with col_control2:
        st.button("⏸️ 暂停", use_container_width=True, key="video_pause")

    with col_control3:
        st.button("▶️ 播放", use_container_width=True, key="video_play")

    with col_control4:
        st.button("🔇 静音", use_container_width=True, key="video_mute")

    with col_control5:
        if st.button("⏩ 下一集", use_container_width=True, key="video_next"):
            st.session_state['ind'] = (st.session_state['ind'] + 1) % len(video_arr)
    
    st.markdown("---")
    
    # 视频选集
    st.markdown("### 视频选集")
    
    # 使用radio选择器
    selected_video = st.radio(
        "选择要播放的视频",
        options=range(len(video_arr)),
        format_func=lambda x: f"第{x + 1}集：{video_arr[x]['title']}",
        index=st.session_state['ind'],
        key="video_selector"
    )
    
    # 监听radio选择的变化
    if selected_video != st.session_state['ind']:
        st.session_state['ind'] = selected_video
    
    # 添加视频描述
    st.markdown("### 视频介绍")
    video_descriptions = [
        "光头强和熊大熊二在炎热的夏天为争夺纳凉地展开一系列有趣的争斗。",
        "光头强在山庄里遇到了一系列有趣的事情，与熊大熊二之间的互动更加精彩。",
        "萤火虫飞舞的夜晚，光头强和熊大熊二一起度过了一个美好的夜晚。"
    ]
    
    if st.session_state['ind'] < len(video_descriptions):
        st.markdown(f"**剧情简介：** {video_descriptions[st.session_state['ind']]}")
