mishtee_css = """
/* Import High-End Serif Font */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&display=swap');

/* GLOBAL SETTINGS */
.gradio-container {
    background-color: #FAF9F6 !important; /* Off-White */
    color: #333333 !important; /* Charcoal */
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; /* Clean Sans-Serif Base */
}

/* TYPOGRAPHY */
/* Clean, Spaced-out Serif for Headings */
.prose h1, .prose h2, .prose h3, .prose h4 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em;
    color: #333333 !important;
    margin-bottom: 1.5rem !important;
}

/* Lightweight Sans-Serif for Tables and Body */
table, p, li, span, label {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    font-weight: 300 !important;
    line-height: 1.6;
}

/* BUTTONS */
/* Sober Terracotta, Sharp Lines */
button {
    background-color: #C06C5C !important;
    color: #FFFFFF !important;
    border-radius: 0px !important; /* Sharp corners */
    border: none !important;
    box-shadow: none !important; /* No shadows */
    padding: 12px 30px !important; /* Generous padding */
    text-transform: uppercase;
    font-size: 0.9rem;
    letter-spacing: 1px;
    transition: opacity 0.2s ease;
}

button:hover {
    opacity: 0.9;
}

/* INPUTS & PANELS */
/* Minimalist, Thin Borders, White Background */
input, textarea, select, .gr-box, .gr-panel {
    background-color: #FFFFFF !important;
    border: 1px solid #E0E0E0 !important; /* Thin border */
    border-radius: 0px !important; /* Sharp corners */
    box-shadow: none !important;
    color: #333333 !important;
}

/* TABLE STYLING */
table {
    border-collapse: collapse;
    width: 100%;
}

th {
    border-bottom: 1px solid #333333 !important; /* Darker line for header */
    text-align: left;
    padding: 20px !important; /* Significant whitespace */
    text-transform: uppercase;
    font-size: 0.85rem;
    font-weight: 600 !important;
}

td {
    border-bottom: 1px solid #E0E0E0 !important;
    padding: 20px !important;
}

/* LAYOUT UTILITIES */
/* Enforce spacing between blocks */
.gradio-row, .gradio-column {
    gap: 30px !important;
}

/* Remove any default rounded corners globally */
* {
    border-radius: 0px !important;
}
"""
