import streamlit as st

def app():
    st.empty()
    
    st.markdown("""
        <style>
            .topnav {
                background-color: #0ed145;
                overflow: hidden;
                color: white;
            }
            .topnav a {
                display: block;
                color: white;
                text-align: center;
                padding: 14px 16px;
                font-size: 22px;
            }
            body {
                margin: 0;
                padding: 0;
            }
            .full-page-image {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                overflow: hidden;
                z-index: -1;
            }
            .full-page-image img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
        </style>
    """, unsafe_allow_html=True)

    # Add a container to hold the image
    st.markdown("""
        <div class="full-page-image">
            <img src="https://mir-s3-cdn-cf.behance.net/project_modules/fs/734f0d84245339.5d56863298024.jpg" />
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            [data-testid="stAppViewBlockContainer"] {
                padding: 0;
                margin: 0;
                background: transparent;
            }
            [data-testid="stHeader"] {
                background-color: white;
                padding: 0;
                margin: 0;
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    app()
