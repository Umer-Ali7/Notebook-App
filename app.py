
import streamlit as st
from backend.db import NoteDatabase
from datetime import date
from fpdf import FPDF
import os

note_db = NoteDatabase()

st.set_page_config(page_title="📝 Digital Notebook (OOP Edition)", layout="centered")
st.title("📘 Digital Notebook")

# Input Fields
title = st.text_input("📝 Note Title")
content = st.text_area("📄 Note Content")
tags_input = st.text_input("🏷️ Tags (comma-separated)")
reminder_date = st.date_input("📅 Reminder Date", value=None, format="YYYY-MM-DD")

if st.button("✅ Add Note"):
    if title.strip() and content.strip():
        tags = ",".join([tag.strip() for tag in tags_input.split(",") if tag.strip()])
        note_db.add_note(title, content, tags, str(reminder_date))
        st.success("🎉 Note added successfully!")
    else:
        st.warning("⚠️ Title and Content cannot be empty!")

st.markdown("---")

# Search
st.subheader("🔍 Search Notes")
search_query = st.text_input("Type keyword to search...")
notes = note_db.search_notes(search_query) if search_query else note_db.get_notes()

st.subheader("📚 Your Notes")

def export_to_pdf(title, content, tags, created_at, reminder):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Title: {title}\nCreated: {created_at}\nReminder: {reminder}\nTags: {tags}\n\n{content}")
    filename = f"{title.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

for note in notes:
    try:
        note_id, note_title, note_content, note_created_at, note_tags, note_reminder = note
        with st.expander(f"📌 {note_title} — {note_created_at}"):
            st.write(note_content)
            if note_tags:
                st.markdown(f"**Tags:** {note_tags}")
            if note_reminder:
                st.markdown(f"📅 Reminder: `{note_reminder}`")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"❌ Delete", key=f"delete_{note_id}"):
                    note_db.delete_note(note_id)
                    st.experimental_rerun()
            with col2:
                if st.button(f"⬇️ Download PDF", key=f"pdf_{note_id}"):
                    pdf_file = export_to_pdf(note_title, note_content, note_tags, note_created_at, note_reminder)
                    with open(pdf_file, "rb") as f:
                        st.download_button(label="📄 Download Now", data=f, file_name=pdf_file, mime="application/pdf")
                    os.remove(pdf_file)
    except Exception as e:
        st.error(f"Error loading note: {e}")


st.markdown("<hr><footer>Copyright © 2025 All rights reserved. Powered by Streamlit 🚀</footer>", unsafe_allow_html=True)