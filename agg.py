import streamlit as st
from datetime import date

# 页面配置
st.set_page_config(
    page_title="个人简历生成器",
    layout="wide"
)

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
st.title("个人简历生成器")

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
    
    # 性别选择 - 单选框（只有男/女两种选项）
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
    
    # 语言能力 - 单选框
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
    
    # 技能选择 - 单选框
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
    
    # 显示上传的照片（如果有）- 放在个人简历下面
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
    
    # 出生日期 - 格式化为字符串显示
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
