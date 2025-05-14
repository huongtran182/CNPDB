import streamlit as st
from sidebar import render_sidebar  # 👈 This brings in the shared sidebar

# Set the page config
st.set_page_config(page_title="About CNPD", layout="wide")

# Show the sidebar
render_sidebar()

# Main content
st.markdown('<h1>About CNPD – Crustacean Neuropeptide Database</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h2>Overview</h2>
<p>The current release of <span class="highlight">CNPD (Version 1.0, 2025)</span> contains <span class="highlight">[X]</span> curated neuropeptide entries from <span class="highlight">[Y]</span> crustacean species, organized into <span class="highlight">[Z]</span> neuropeptide families.</p>
<p>Data is manually curated from peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases such as <b>UniProt</b> and <b>NCBI</b>.</p>
</div>

<div class="section">
<h2>What CNPD Provides</h2>
<ul>
<li>Neuropeptide sequence (FASTA format)</li>
<li>Species taxonomy & homology</li>
<li>Physicochemical properties (mass, charge, hydrophobicity, etc.)</li>
<li>Post-translational modifications (PTMs)</li>
<li>Experimental validation methods (LC-MS/MS, transcriptomic mining, etc.)</li>
<li>MS Imaging of the peptide showing their distribution in tissues</li>
<li>Predicted 3D Structure</li>
<li>Predicted Half-life</li>
<li>Predicted/validated biological functions</li>
</ul>
<p>CNPD also provides cross-links to <b>UniProt, NCBI, and PubMed</b>, along with search and analysis tools for neuropeptide research.</p>
</div>

<div class="section">
<h2>Database Features & Tools</h2>
<ul>
<li><b>Flexible Search Engine</b> – Find neuropeptides by name, sequence, family, or function.</li>
<li><b>Comparative Peptide Analysis</b> – Compare neuropeptide sequences across crustacean species.</li>
<li><b>Sequence Alignment & Homology Search</b> – Identify conserved motifs and sequence similarities.</li>
<li><b>Mass Spectrometry Data Integration</b> – Explore MS-validated peptides and spectral evidence.</li>
<li><b>Peptide Property Calculator</b> – Compute GRAVY scores, hydrophobicity, half-life, 3D structures, and more.</li>
</ul>
</div>

<div class="section">
<h2>Crustacean Species Covered</h2>
<ul>
<li><i>Homarus americanus</i> (American Lobster)</li>
<li><i>Callinectes sapidus</i> (Blue Crab)</li>
<li><i>Cancer borealis</i> (Jonah Crab)</li>
<li><i>Litopenaeus vannamei</i> (Pacific White Shrimp)</li>
<li><i>Pandalus borealis</i> (Northern Shrimp)</li>
</ul>
</div>

<div class="section">
<h2>Data Sources & Curation</h2>
<ul>
<li><b>Experimental Data</b> – Mass spectrometry & neuropeptide bioassays</li>
<li><b>Literature Mining</b> – Curated from PubMed & primary research papers</li>
<li><b>Public Databases</b> – Cross-linked with UniProt, NCBI, and NeuroPep</li>
<li><b>Computational Predictions</b> – Sequence-based neuropeptide identification</li>
</ul>
<p>Every neuropeptide entry undergoes <b>manual examination</b> to ensure accuracy and reliability.</p>
</div>

<div class="section">
<h2>Get Involved & Contribute</h2>
<ul>
<li>Submit new neuropeptide sequences</li>
<li>Report missing or updated annotations</li>
<li>Share mass spectrometry datasets</li>
<li>Suggest additional features or improvements</li>
</ul>
<p>For collaborations, submissions, or feedback, please contact <a href="mailto:lingjun.li@wisc.edu" class="email">Dr. Lingjun Li</a>.</p>
</div>

<div class="section">
<h2>Citation & Funding</h2>
<p>If you use CNPD in your research, please cite:</p>
<p><b>Crustacean Neuropeptide Database (CNPD): A curated resource for neuropeptide research in crustacean species.</b> [Authors]. [Journal Name], [Year]. DOI: [XXXX].</p>
<p><b>Funding:</b> This work is supported by [Funding Agencies].</p>
</div>

<div class="section">
<h2>Future Updates</h2>
<ul>
<li>Expansion to more crustacean species</li>
<li>Enhanced peptide discovery tools</li>
<li>Improved mass spectrometry integration</li>
<li>User-submitted experimental data uploads</li>
</ul>
</div>

<div class="section" style="text-align: center; font-size: 14px; color: #2a2541;">
<p><em>Last update: Jul 2025</em></p>
</div>
""", unsafe_allow_html=True)
