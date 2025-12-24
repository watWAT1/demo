import streamlit as st

st.set_page_config(page_title="视频中心")

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
    },
    {
        'url': 'http://upos-sz-mirrorcos.bilivideo.com/upgcxcode/64/69/25642406964/25642406964-1-192.mp4?e=ig8euxZM2rNcNbRg7wdVhwdlhWNMhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&deadline=1766568317&trid=24843260edd74f9592241739035a6c3O&oi=2067284620&og=cos&nbs=1&uipk=5&platform=html5&mid=0&gen=playurlv3&os=estgcos&upsig=54df35d8b7ca01e6c8ad24cecd3e721d&uparams=e,deadline,trid,oi,og,nbs,uipk,platform,mid,gen,os&bvc=vod&nettype=1&bw=999574&buvid=&build=7330300&dl=0&f=O_0_0&agrr=1&orderid=0,3',
        'title': '熊出没之夏日连连看第四集：叫俺漫画家'
    },
    {
        'url': 'http://upos-sz-mirrorcos.bilivideo.com/upgcxcode/70/69/25642406970/25642406970-1-192.mp4?e=ig8euxZM2rNcNbRz7zdVhwdlhWhahwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&os=bdbv&og=hw&mid=0&uipk=5&trid=9f9fd36dfa464f91bd28042de55d020O&nbs=1&oi=144233936&deadline=1766568339&platform=html5&gen=playurlv3&upsig=1ff007df31db3770508fc19411bec306&uparams=e,os,og,mid,uipk,trid,nbs,oi,deadline,platform,gen&bvc=vod&nettype=1&bw=1100137&agrr=1&buvid=&build=7330300&dl=0&f=O_0_0&orderid=0,3',
        'title': '熊出没之夏日连连看第五集：森林游园会'
    }
]

if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

st.title(video_arr[st.session_state['ind']]['title'])

st.video(video_arr[st.session_state['ind']]['url'])

def playVideo(e):
    st.session_state['ind'] = int(e)

for i in range(len(video_arr)):
    if i % 3 == 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            if i < len(video_arr):
                st.button('第' + str(i + 1) + '集', on_click=playVideo, args=([i]), key=f'btn_{i}')
        with col2:
            if i + 1 < len(video_arr):
                st.button('第' + str(i + 2) + '集', on_click=playVideo, args=([i + 1]), key=f'btn_{i+1}')
        with col3:
            if i + 2 < len(video_arr):
                st.button('第' + str(i + 3) + '集', on_click=playVideo, args=([i + 2]), key=f'btn_{i+2}')
