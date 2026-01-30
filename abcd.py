import streamlit as st
import random
import time

st.set_page_config(page_title="Mobile Random Box", layout="centered")


items = [
    {"name": "게임보이", "img": "게임보이.jpeg", "가격":'100원'},
    {"name": "빈 음료수 캔", "img": "빈 음료수 캔.jpeg", '가격':'10원'},
    {"name": "낡은 백과사전", "img": "낡은 백과사전.jpeg", '가격':'50원'},
    {"name": "플라스틱 우산", "img": "플라스틱 우산.jpeg", '가격':'70원'},
    {"name": "지우개", "img": "지우개.jpeg", '가격':'15원'},
    {"name": "연필", "img": "연필.jpeg", '가격':'10원'},
    {"name": "공책", "img": "공책.jpeg", '가격':'30원'},
    {"name": "고장 난 리모컨", "img": "고장 난 리모컨.jpeg", '가격':'10원'},
    {"name": "비닐봉지", "img": "비닐봉지.jpeg", '가격':'5원'},
    {"name": "동전", "img": "동전.jpeg", '가격':'100원'}
]

아이템개수 = {
    "게임보이":0,
    "빈 음료수 캔":0,
    "낡은 백과사전":0,
    "플라스틱 우산":0,
    "지우개":0,
    "연필":0,
    "공책":0,
    "고장 난 리모컨":0,
    "비닐봉지":0,
    "동전":0,
}

if 'page' not in st.session_state: 
    st.session_state.page = 'login' 

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if 'user_db' not in st.session_state: 
    st.session_state.user_db = {'이미지':[], 'tickets': 3, "collection":'', '아이템명':[], '돈':50, '아이템개수':아이템개수}

if '상대아이템' not in st.session_state:
    st.session_state.상대아이템 = random.choice(items)

if 'last_ticket_time' not in st.session_state:
    st.session_state.last_ticket_time = time.time()

if time.time() - st.session_state.last_ticket_time >= 3:
    st.session_state.user_db['tickets'] += random.randint(1, 3)
    st.session_state.last_ticket_time = time.time()



if not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.rerun()

    if st.session_state.page == 'login':
        st.image("기본창.png", width=True) 
        st.write("## 로그인")
        user_id = st.text_input("ID", placeholder="아이디를 입력하세요") 
        user_pw = st.text_input("PW", type="password", placeholder="비밀번호를 입력하세요") 

        if st.button("로그인하기"):
            if user_id in st.session_state.user_db and st.session_state.user_db[user_id] == user_pw: 
                st.session_state.page = '뽑기' 
                st.session_state.logged_in = True
                st.rerun() 
            else: 
                st.error("아이디 또는 비밀번호가 틀렸습니다.") 

        if st.button("회원가입하기"):
            st.session_state.page = 'signup'
            st.rerun()
    
    elif st.session_state.page == 'signup':
        st.image("기본창.png", width=True)
        st.write("## 회원가입")
        signup_id = st.text_input("ID", placeholder="아이디를 입력하세요")
        signup_pw = st.text_input("PW", type="password", placeholder="비밀번호를 입력하세요") 

        if st.button("회원가입확인"):
            if signup_id in st.session_state.user_db: 
                st.error("아이디 중복!") 
            elif signup_id and signup_pw: 
                st.session_state.user_db[signup_id]=signup_pw
                st.session_state.user_db['tickets']=3
                st.session_state.page = 'login'
                st.rerun() 
            else:
                st.warning('둘다 입력')
            
else:
    
    menu = st.sidebar.radio("메뉴",["🎰 뽑기",  "📖 도감", "🏪 거래소"])
    st.sidebar.markdown("---")
    st.sidebar.write(f"🎟 뽑기권: {st.session_state.user_db['tickets']}")
    st.sidebar.write(f"💸 돈: {st.session_state.user_db['돈']}")

    if  menu == '🎰 뽑기':
        st.image("기본창.png", width=True)

        if st.button("뽑기"):
            if st.session_state.user_db["tickets"] <= 0:
                st.error("뽑기권이 없습니다!")
            else:
                st.session_state.user_db["tickets"] -= 1
                st.spinner("두근두근...")
                a=random.choice(items)
                if a['name'] not in st.session_state.user_db['아이템명']:
                    st.session_state.user_db['아이템명'].append(a["name"])
                st.session_state.user_db['아이템개수'][a["name"]]+=1    
                st.write(a['name'],'뽑기 성공!')
                st.image(a['img'])
        if st.session_state.user_db['돈']>= 30:
            if st.button('뽑기권 1개 구매(30원)'):
                st.session_state.user_db['돈'] -= 30
                st.session_state.user_db['tickets'] += 1
    elif menu == '📖 도감':
        cols = st.columns(4)
        for idx, item in enumerate(items):
            with cols[idx % 4]:
                if item['name'] in st.session_state.user_db['아이템명']:
                    st.image(item['img'])
                    st.markdown(f"✅ **{item['name']} {st.session_state.user_db['아이템개수'][item['name']]}개/{item['가격']}**")
                else:
                    st.image('없음.jpeg')
                    st.markdown(f"⬜ {item['name']}")

    elif menu == '🏪 거래소':
        cols = st.columns(4)
        총개수 = 0
        with cols[0]:
            아이템 = st.selectbox('거래할거',list(st.session_state.user_db['아이템명']))
            if not 아이템 == None:
                총개수 = st.session_state.user_db['아이템개수'][아이템]           
            if 아이템 == None:
                st.image('없음.jpeg')
            else:
                st.image(f'{아이템}.jpeg')
        with cols[1]:
            cnt = st.text_input(' ',placeholder='거래할 아이템 개수', value='0')
            if int(cnt) > 총개수:
                st.error('**가지고 있는 개수보다 많습니다!**')
            if st.button('거래하기') and int(cnt) <= 총개수:
                for i in range(int(cnt)):
                    st.session_state.user_db['아이템개수'][st.session_state.상대아이템['name']]+=1
                    st.session_state.user_db['아이템개수'][아이템]-=1
                    if st.session_state.상대아이템['name'] not in st.session_state.user_db['아이템명']:
                        st.session_state.user_db['아이템명'].append(st.session_state.상대아이템['name'])
                    if st.session_state.user_db['아이템개수'][아이템] <= 0:
                        st.session_state.user_db['아이템명'].remove(아이템)
                    st.session_state.상대아이템 = random.choice(items)
                    st.session_state.user_db['돈']+=5
        with cols[2]:
            st.markdown('')
            st.markdown('')
            st.markdown(f'/{총개수}개')
            st.image(st.session_state.상대아이템['img'])

