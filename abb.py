import streamlit as st
import pandas as pd
import numpy as np

# 设置页面配置
st.set_page_config(
    page_title="亚索 - 英雄介绍",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# 英雄熟练度 - 使用metric函数
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
st.markdown("<h3 style='color: #3498db;'>⚡ 狂风绝息斩 (R)</h3>", unsafe_allow_html=True)
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
def yasooskill():
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
