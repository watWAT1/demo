import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title='动物园轮播相册',
    page_icon='🐒'
)

# 标题
st.title("🦁 动物园轮播相册")
st.markdown("---")

# 图片数组（只保留3张）
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

# 导航函数
def next_image():
    st.session_state.current_index = (st.session_state.current_index + 1) % total_images

def prev_image():
    st.session_state.current_index = (st.session_state.current_index - 1) % total_images

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
        prev_image()
        st.rerun()

with col2:
    # 显示当前索引
    st.write(f"第 {st.session_state.current_index + 1} 张")

with col3:
    if st.button("下一张 ▶️", use_container_width=True):
        next_image()
        st.rerun()
