import streamlit as st
from main import ppt

st.set_page_config(page_title="AI-PPT Generator", page_icon='🎥',layout="centered")


hide_decoration_bar_style = '''
    <style>
        [data-testid="stDecoration"] {
            display: none;
        }
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.title("📽️ AI-PPT Generator")
st.caption('Made by SIDDHESHUMESHSARANG')
topic = st.text_input("Enter the Topic of Presentation")
num_slides = st.number_input("Enter the Number of Slides", min_value=1, max_value=50)

if st.button("Generate Presentation"):
    if topic and num_slides:
        try:
            with st.spinner("Generating your slides..."):
                result = ppt.getPPT(topic, int(num_slides))  
            st.success("Presentation generated successfully!")
            st.caption("Check your files to get the pptx")
            if result:  
                st.text(result)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill in both fields.")