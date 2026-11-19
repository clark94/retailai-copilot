import os,requests,streamlit as st,pandas as pd
API=os.getenv('API_URL','http://localhost:8000').rstrip('/')
st.set_page_config(page_title='RetailAI Copilot',page_icon='📦',layout='wide')
st.title('RetailAI Copilot — Démonstrateur sécurisé')
token=st.sidebar.text_input('Jeton de démonstration',type='password',value=os.getenv('DEMO_API_TOKEN',''))
headers={'Authorization':'Bearer '+token} if token else {}
st.sidebar.caption('Les filtres de sécurité sont appliqués côté API.')
st.caption('Données commerciales synthétiques et corpus documentaire fictif. Aucun accès aux systèmes Hoortrade.')
t1,t2,t3=st.tabs(['Assistant documentaire','Ventes','Stocks'])
with t1:
    q=st.text_input('Pose une question sur le corpus de démonstration')
    if st.button('Rechercher',key='rag') and q:
        try:
            result=requests.post(API+'/ask',json={'question':q},headers=headers,timeout=90).json()
            st.write(result.get('answer',''))
            st.caption('Mode : '+result.get('mode',''))
            for s in result.get('sources',[]):st.expander(s['source']).write(s['extrait'])
        except requests.RequestException as e:st.error(str(e))
with t2:
    dim=st.selectbox('Regrouper par',['marque','pays','categorie','canal_vente'])
    try:
        rows=requests.get(API+'/sales',params={'group_by':dim},headers=headers,timeout=10).json()['rows']
        frame=pd.DataFrame(rows)
        st.dataframe(frame,use_container_width=True)
        if not frame.empty:st.bar_chart(frame.set_index('dimension')['ca_eur'])
    except (requests.RequestException,KeyError) as e:st.error(str(e))
with t3:
    st.info('Les variations de stock marocaines ne constituent pas un stock actuel sans stock initial.')
    try:
        rows=requests.get(API+'/stocks/movements',headers=headers,timeout=10).json()['rows']
        st.dataframe(pd.DataFrame(rows),use_container_width=True)
    except (requests.RequestException,KeyError) as e:st.error(str(e))
