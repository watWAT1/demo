import streamlit as st

st.set_page_config(page_title="音乐播放器", page_icon="🎵")

# -------------------------------------------------
# 1. 歌库（想加歌继续往里塞）
# -------------------------------------------------
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

# -------------------------------------------------
# 2. session 状态
# -------------------------------------------------
if "sid" not in st.session_state:
    st.session_state.sid = "1"  # 默认第一首

def switch_song():
    st.session_state.sid = st.session_state.pick

def prev_song():
    song_ids = list(SONGS.keys())
    current_idx = song_ids.index(st.session_state.sid)
    prev_idx = (current_idx - 1) % len(song_ids)
    st.session_state.sid = song_ids[prev_idx]
    st.session_state.pick = st.session_state.sid

def next_song():
    song_ids = list(SONGS.keys())
    current_idx = song_ids.index(st.session_state.sid)
    next_idx = (current_idx + 1) % len(song_ids)
    st.session_state.sid = song_ids[next_idx]
    st.session_state.pick = st.session_state.sid

# -------------------------------------------------
# 3. 页面布局
# -------------------------------------------------
left, right = st.columns([1, 2])

with left:
    st.image(SONGS[st.session_state.sid]["pic"], width=240)

with right:
    st.markdown("### 正在播放")
    st.write(f"**歌曲：** {SONGS[st.session_state.sid]['name']}")
    st.write(f"**歌手：** {SONGS[st.session_state.sid]['artist']}")
    st.write(f"**专辑：** {SONGS[st.session_state.sid]['album']}")

    options = {k: f"{v['name']} - {v['artist']}" for k, v in SONGS.items()}
    st.selectbox(
        "切换歌曲",
        options.keys(),
        format_func=lambda x: options[x],
        key="pick",
        on_change=switch_song,
    )

    # 上一首和下一首按钮
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⏮️ 上一首", on_click=prev_song)
    with col2:
        st.button("⏭️ 下一首", on_click=next_song)

    st.audio(SONGS[st.session_state.sid]["url"], format="audio/mp3")
