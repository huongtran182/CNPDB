import streamlit as st
import streamlit.components.v1 as components

# Your GA4 Measurement ID
GA_MEASUREMENT_ID = "G-VWK5FWH61R"  # <- use your actual GA4 ID here

# Inject the Google Analytics script
components.html(f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}');
</script>
""", height=0)

# Simple Streamlit content
st.title("Google Analytics Test Page")
st.write("If GA is working, you'll see this page hit in your GA4 Realtime tab.")
