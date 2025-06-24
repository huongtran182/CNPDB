import streamlit as st
import os
from sidebar import render_sidebar

st.set_page_config(
    page_title="Contact Us",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# ─── Feedback form ────────────────────────────────────────────────────────
st.markdown("""
<style>
.contact-section {
  width: 100%;
  max-width: 40rem;
  margin-left: auto;
  margin-right: auto;
  padding: 3rem 1rem;
}

.contact-intro > * + * {
  margin-top: 1rem;
}

.contact-title {
  font-size: 1.875rem;
  line-height: 2.25rem;
  font-weight: 700;
}

.contact-description {
  color: rgb(107 114 128);
}

.form-group-container {
  display: grid;
  gap: 1rem;
  margin-top: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  margin-bottom: 0.5rem;
}

.form-input,
.form-textarea {
  padding: 0.5rem;
  border: 1px solid #e5e7eb;
  display: flex;
  height: 2.5rem;
  width: 100%;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.form-input::placeholder,
.form-textarea:focus-visible {
  color: #6b7280;
}

.form-input:focus-visible,
.form-textarea:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

.form-textarea {
  min-height: 120px;
}

.form-submit {
  width: 100%;
  margin-top: 1.2rem;
  background-color: #3124ca;
  color: #fff;
  padding: 13px 5px;
  border-radius: 0.375rem;
}
</style>

<section class="contact-section">
  <div class="contact-intro">
    <h2 class="contact-title">SUBMISSION FORM</h2>
    <p class="contact-description">
      Fill out the form below and we'll get back to you as soon as possible.
    </p>
  </div>

  <form class="contact-form" action="https://api.web3forms.com/submit" method="POST" enctype="multipart/form-data">
    <input type="hidden" name="access_key" value="4a443824-a2fc-40d1-a217-3334f40cabc9" />
    <input type="hidden" name="subject" value="New Contact Form Submission from Web3Forms" />
    <input type="hidden" name="from_name" value="My Website" />
    <input type="hidden" name="template" value="box" />

    <label for="name">Full Name *</label><br>
    <input type="text" name="name" required style="width:100%; padding:5px;"><br><br>

    <label for="title">Title/Position (optional)</label><br>
    <input type="text" name="title" style="width:100%; padding:5px;"><br><br>
    
    <label for="institution">Institution/Organization *</label><br>
    <input type="text" name="institution" required style="width:100%; padding:5px;"><br><br>
    
    <label for="email">Email Address *</label><br>
    <input type="email" name="email" required style="width:100%; padding:5px;"><br><br>
    
    <label for="message">Your Message/Feedback *</label><br>
    <textarea name="message" required rows="6" style="width:100%; padding:5px;"></textarea><br><br>
    
    <label for="attachment">Attach a file (optional)</label><br>
    <input type="file" name="attachment"><br>
    
    <button type="submit" style="padding:5px 5px; type="primary"">Submit</button>
  </form>
</section>
""", unsafe_allow_html=True)


# ─── Footer ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
