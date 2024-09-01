import streamlit as st

def app():
    st.empty()
    with st.container():
        st.markdown("""
            <style>
                .topnav {
                    background-color: #0ed145;
                    overflow: hidden;
                    text-color: white;
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
                }
                .full-page-image img {
                    width: 100%;
                    height: 100vh;
                    object-fit: cover;
                    
                }
            </style>
            <body>
                <div class="topnav"></div>
            </body>
        """, unsafe_allow_html=True)

    # Directly load and display the image using Streamlit's st.image
    st.image(image="https://mir-s3-cdn-cf.behance.net/project_modules/fs/734f0d84245339.5d56863298024.jpg", use_column_width=True)

    st.markdown("""
            <style>
                [data-testid="stAppViewBlockContainer"] {
                    padding: 0;
                    margin: 0;
                    background-size:cover;
                }
                [data-testid="stHeader"] {
                    background-color: white;
                    padding:0;
                    margin:0;
                }
                .sidebar {
                    float: right;
                    width: 50%;
                    padding: 0 20px 20px 15px;
                }
                .sidebar p {
                    display: block;
                    color: black;
                    text-align: left;
                    padding: 5px 16px;
                    font-size: 17px;
                }
                #content {
                    text-align: left;
                    width: 100%;
                    padding: 5px 16px;
                }
                .Paragraph {
                    overflow: hidden;
                }
                .Paragraph a {
                    display: block;
                    color: black;
                    text-align: left;
                    padding: 5px 40px;
                    font-size: 17px;
                }
            </style>
            <body>
            </body>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    app()
