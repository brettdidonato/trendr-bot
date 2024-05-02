import os
import streamlit as st

from ask_google_trends import AskGoogleTrends

# Google Fonts
st.html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
""")

def display_webpage() -> None:
    # Import local CSS style file
    with open('style.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Display webpage
    st.html("<div style='text-align:center;'><img src='https://storage.googleapis.com/ask_gtrends/trendrbot.png' style='width:50%;' /></div>")
    st.subheader("Ask me a question and I will answer based on trending data. Try asking questions about countries, topics and more. Created by [Brett DiDonato](https://www.linkedin.com/in/brettdidonato/).")

    question = st.text_input(
        label="",
        value="",
        placeholder="Ask me a question...",
        key="question"
    )

    search_button = st.button(
        label="Submit",
        key="search_button",
        type="primary"
    )

    # Execute search
    if search_button:
        a = AskGoogleTrends()

        with st.spinner("Processing..."):
            answer = a.ask(question)
            if answer:
                st.html("<hr>")
                st.write(answer)

    else:
        example_text = st.markdown("""
            **Example questions:**
            * What are the top 10 trends in the US for the latest available data? Simply list them in bullet points.
            * What's popular in Finland?
            * What are the most popular celebrities in England?
            * Are there noticeable differences in trends between European and Asian countries?
        """)

display_webpage()