import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL')

groq_api_key="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"

generic_url=st.text_input("URL",label_visibility="collapsed")


prompt_template="""
    Provide a summary of the following content in 300 words:
    content:{text}
"""

prompt=PromptTemplate(template=prompt_template,input_varibles=["text"])
from langchain.schema import Document
from youtube_transcript_api import YouTubeTranscriptApi

if st.button("Summarize the content from YT or website"):
    llm=ChatGroq(model="gemma2-9b-it",groq_api_key=groq_api_key)
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL.It can may be a YT video URL or website url")
    else:
        try:
            with st.spinner("Waiting..."):
                if "youtube.com" in generic_url:  #Means it is a youtube video url
                    video_id=generic_url.split("v=")[-1]
                    transcript=YouTubeTranscriptApi.get_transcript(video_id=video_id)
                    text=" ".join([entry['text'] for entry in transcript])
                    docs=[Document(page_content=text)]
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                  headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                    docs=loader.load()

                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception: {e}")
