import streamlit as st
from PIL import Image
import os
import base64
from sidebar import render_sidebar

st.set_page_config(
    page_title="Contact Us",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# ─── Feedback form ────────────────────────────────────────────────────────
st.markdown(f"""
<style>
 /* 1) Centered title with10px top margin */
  h2.custom-title {{
    text-align: center !important;
    margin-top: 0px !important;
    color: #29004c;
  }}
  form label {{
      display: block;
      margin-top: 0px;
      margin-bottom: 0px;
      font-weight: bold;
  }}
  form input[type="text"],
  form input[type="email"],
  form textarea {{
      width: 100%;
      padding: 0px;
      border-radius: 5px;
      border: 1px solid #ccc;
      margin-bottom: 0px; 
  }}
  form input[type="file"] {{
      margin-top: 3px;
  }}
  form button {{
      margin-top: 0px;
      background-color: #9e9ac8;
      color: #000000;
      padding: 2px 4px;
      border-radius: 5px;
      font-size: 1.2em;
      cursor: pointer;
  }}
  form button:hover {{
      background-color: #6a51a3;
  }}
</style>


<h2 class="custom-title">SUBMISSION FORM</h2>

<form action="https://api.web3forms.com/submit" method="POST">
      <input type="hidden" name="access_key" value="4a443824-a2fc-40d1-a217-3334f40cabc9">
    
      <label for="name">Full Name *</label><br>
      <input type="text" name="name" required><br>
    
      <label for="title">Title/Position (optional)</label><br>
      <input type="text" name="title"><br>
    
      <label for="institution">Institution/Organization *</label><br>
      <input type="text" name="institution" required><br>
    
      <label for="email">Email Address *</label><br>
      <input type="email" name="email" required><br>
    
      <label for="message">Your Message/Feedback *</label><br>
      <textarea name="message" required rows="6"></textarea><br>
    
      <label for="attachment">Attach a file (optional)</label><br>
      <input type="file" name="attachment"><br>

      <!-- Honeypot Spam Protection -->
      <input type="checkbox" name="botcheck" class="hidden" style="display: none;">
    
      <div style="text-align:center;">
        <button type="submit" style="padding:10px 20px;">Submit</button>
      </div>
</form>
""", unsafe_allow_html=True)


# ─── Footer ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
