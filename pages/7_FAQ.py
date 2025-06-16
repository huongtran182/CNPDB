import streamlit as st
from sidebar import render_sidebar
import textwrap

st.set_page_config(
    page_title="FAQ",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# Page header
st.markdown("# Frequently Asked Questions")

# Your FAQ data
faqs = [
    {
        "num": "01",
        "question": "What is the definition of neuropeptide?",
        "answer": textwrap.dedent("""
            While there are many controversial definitions, we consider a neuropeptide to be included in this database if it has the following characteristics:
            1. Must be synthesized and released by a neuron;
            2. Endogenous, small protein-like molecule composed of short chains of amino acids that function as signaling molecules in the nervous system;
            3. Derived from neuropeptide prohormones/precursors.
        """)
    },
    {
        "num": "02",
        "question": "How do I search for neuropeptides of interest in the cNPDB?",
        "answer": textwrap.dedent("""
            The Database Search Engine on the left allows users to search by specific sequence, family, organism, and other propepties. 
            Visit the Tutorials page for detailed instructions on how to use the search engine and download the results.
        """)
    },
    {
        "num": "03",
        "question": "How often is the database updated?",
        "answer": textwrap.dedent("""
            The database is maintained and updated yearly. Additionally, any new submissions/requests from the community will be addressed promtly upon receipt. 
        """)
    },
    {
        "num": "04",
        "question": "What does the “Instability Index” mean?",
        "answer": textwrap.dedent("""
            The Instability Index is a computational measure that predicts the in vitro stability of a peptide or protein based on the presence of certain dipeptides known to affect stability.
            The peptide is predicted to be stable if its index < 40.
        """)
    },
    {
    "num": "05",
        "question": "What do the terms “de novo,” “MS/MS,” and “predicted” mean?",
        "answer": textwrap.dedent("""
            These terms describe the type of evidence supporting the existence of each neuropeptide in the database.
            1. De novo: Identified directly from raw MS data using computational algorithms purely based on fragmentation patterns.
            2. MS/MS: Identified from MS/MS experiments and matched against known neuropeptide databases.
            3. Predicted: Not observed experimentally but predicted through bioinformatics analysis (e.g. in silico prediction or gene annotation).
        """)
    },
    {
    "num": "06",
        "question": "How can I contact for new data submission, request new features, or report an error?",
        "answer": textwrap.dedent("""
            Please fill out the Feedback Form in the Contact Us page. For collaborations or urgent request, please contact Prof. Li directly at lingjun.li@wisc.edu.
        """)
    },
]

# 4. Helper to render one card
def render_card(faq):
    html = f"""
    <div style="
        background-color: #9e9ac8;
        border-radius: 10px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        padding: 20px;
        display: flex;
        flex-direction: column;
        min-height: 400px;
        min-width: 330px;
    ">
      <!-- underline fixed at 50px down -->
      <div style="
          position: absolute;
          top: 100px;
          left: 80px;
          right: 0px;
          border-bottom: 3px solid black;
      "></div>

      <!-- Header -->
      <div style="
          display: flex;
          align-items: flex-start;
          gap: 10px;
          min-height: 70px;
          margin-top: 0;            /* no extra top margin */
      ">
        <div style="
            font-size: 55px;
            font-weight: bold;
            color: black;
            flex-shrink: 0;
        ">{faq['num']}</div>
        <div style="flex:1;">
          <!-- remove this inner border-bottom -->
          <div style="
              font-size: 22px;
              font-weight: bold;
              color: black;
              margin: 0;
              line-height: 25px;
          ">{faq['question']}</div>
        </div>
      </div>
      <!-- Answer -->
      <div style="
          position: absolute;
          top: 90px;
          flex: 1;
          font-size: 17px;
          line-height: 22px;
          color: #333;
          text-align: justify;
          text-justify: inter-word;
          overflow-y: auto;
          min-height: 0;
      ">
        {faq['answer'].replace('\n', '<br>')}
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# 5. Lay out in rows of 3
for i in range(0, len(faqs), 3):
    row = faqs[i:i+3]
    cols = st.columns(3, gap="large")
    for col, faq in zip(cols, row):
        with col:
            render_card(faq)
    # after each row (except the last), insert a 40px tall spacer
    if i + 3 < len(faqs):
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# footers
st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

