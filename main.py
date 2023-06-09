import streamlit as st
import pandas as pd
import pyzipper

@st.cache_data()
def get_recs(title,top_n=3):
    sub_df=df[df['title']==title]
    recs=[]
    for i in range(top_n):
        idx=int(sub_df['top_'+str(i+1)])
        recs.append(df.iloc[idx]['title'])
    return recs

# @st.cache_resource()
def load_css():
        # print('css ran')
        st.markdown(f"""<style>
                                @font-face {{
                                            font-family: 'Noto Nastaleeq Urdu';
                                            src: 'fonts/NotoNastaliqUrdu-VariableFont_wght.ttf';
                                            }}
                                html, body, [class*="css"] {{
                                font-family: 'Noto Nastaleeq Urdu';
                                direction: rtl;
                                text-align: justify;
                                ont-size: 20px;
                                line-height: 2;
                                }}
                                .title {{
                                text-align: right;
                                line-height: 2;
                                }}
                                .subheader {{
                                text-align: right;
                                line-height: 2;
                                }}
                                .stButton button:first-child {{
                                text-align: right;
                                height: 75px;
                                width: 225px;
                                }}
                                .button-container {{
                                display: flex;
                                justify-content: flex-end;
                                }}
                        </style>""", unsafe_allow_html=True)
        
      
def get_ghazal(title):
    return df[df['title']==title]


def set_ghazal(title):
    st.session_state.selected_ghazal = title
    return

def run_app():
    # st.title("Ghazal Recommender")
    ghazal_title_placeholder= st.empty()
    author_placeholder=st.empty()
    st.write("---")
    ghazal_placeholder = st.empty()
    tmp_df=get_ghazal(selectbox_01)
    title=tmp_df['title'].to_list()[0]
    st.session_state.default_idx=int(tmp_df.index.values)
    ghazal_title_placeholder.markdown(f'<h1 class="title">{title}</h1>', unsafe_allow_html=True)
    author_placeholder.markdown(f'<h6 class="title">{tmp_df.author.to_list()[0]}</h6>', unsafe_allow_html=True)
    urdu_text=tmp_df['text'].to_list()[0].replace('\n','<br>')
    # print(len(urdu_text))
    # Display the Urdu text with increased font size and line spacing
    ghazal_placeholder.markdown(f'<h5 class="urdu-text">{urdu_text}</h5>',
                                 unsafe_allow_html=True)
    

    #recommender
    st.write('---')
    subheader='یہ اوپری تین تجویزات ہیں اگر آپ کو بالا مذکور غزل پسند ہے۔'
    st.markdown(f'<h3 class="subheader">{subheader}</h3>', unsafe_allow_html=True)
    top_n=3
    recs=get_recs(title,top_n)
    cols = st.columns(top_n)
    button_idx=0
    buttons=[]
    for col in cols:
        with col:
            # tmp_title='...'+recs[button_idx][:24]
            st.write(button_idx+1)
            tmp_title=recs[button_idx]
            buttons.append(
                st.button(tmp_title,key=button_idx,on_click=set_ghazal,
                          kwargs=dict(title=recs[button_idx])))
            button_idx+=1



def decrypt_data():
    # Decrypt the ZIP file with the password
    with open('data/data.zip', 'rb') as f_in:
        with pyzipper.AESZipFile(f_in) as f_zip:
            f_zip.setpassword(bytes(st.secrets.my_cool_secrets['pwd'],'UTF-8'))
            for name in f_zip.namelist():
                data = f_zip.read(name)
                with open(name, 'wb') as f_out:
                    f_out.write(data)
    return 1

@st.cache_data
def load_data():
    # print('it ran')
    decrypt_data()
    df = pd.read_parquet('data_rekhta.parquet')
    return df

st.set_page_config(
    page_title="Ghazal Recommender",
    page_icon=":smiley:",
    # initial_sidebar_state="expanded",
    )

#prep app
load_css()
df=load_data()

#this will randomly select a ghazal to display 
if 'default_idx' not in st.session_state:
    st.session_state.default_idx=int(df.sample(1).index.values)

selectbox_01 = st.sidebar.selectbox(' انتخاب شدہ غزل ', df['title'].to_list(),
                                    index=st.session_state.default_idx,key='selected_ghazal')

if __name__ == "__main__":
    run_app()
