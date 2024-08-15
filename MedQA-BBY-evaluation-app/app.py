import streamlit as st
import json
import pandas as pd
from io import StringIO
import tempfile
import os

def load_jsonl(file):
    data = []
    for line in file:
        data.append(json.loads(line))
    return data

def save_jsonl(data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        for item in data:
            json.dump(item, temp_file, ensure_ascii=False)
            temp_file.write('\n')
    
    with open(temp_file.name, 'r', encoding='utf-8') as file:
        content = file.read()
    
    os.unlink(temp_file.name)
    return content

def rtl_text_area(label, value, height, key):
    return st.text_area(label, value, height=height, key=key)

def get_unique_labels(data, key):
    unique_labels = set()
    for item in data:
        value = item.get(key, '')
        if isinstance(value, list):
            unique_labels.update(value)
        elif isinstance(value, str):
            unique_labels.update(value.split(';'))
    return list(unique_labels)

def display_and_edit_labels(item, key, unique_labels, height, idx):
    current_value = item.get(key, '')
    if isinstance(current_value, list):
        current_value = ';'.join(current_value)
    
    label = key.replace('meta_info_', '')
    new_value = st.text_area(
        label,
        current_value,
        height=height,
        key=f"{key}_{idx}"
    )
    st.write(f"Current list: {', '.join(unique_labels)}")
    
    # Convert back to list if necessary
    if ';' in new_value:
        item[key] = [label.strip() for label in new_value.split(';') if label.strip()]
    else:
        item[key] = [new_value] if new_value else []

st.set_page_config(layout="wide")
st.title("MedQA Translation and Enrichment App")

# Apply RTL styling only to specific elements
st.markdown("""
<style>
    .rtl textarea {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.title("Settings")
persian_question_height = st.sidebar.slider("Persian Question Height", min_value=100, max_value=500, value=200, step=50)
persian_option_height = st.sidebar.slider("Persian Option Height", min_value=50, max_value=200, value=100, step=25)
enrich_height = st.sidebar.slider("Enrich MedQA Text Height", min_value=50, max_value=200, value=100, step=25)
labels_height = st.sidebar.slider("Labels Text Height", min_value=50, max_value=200, value=100, step=25)

uploaded_file = st.file_uploader("Choose a JSONL file", type="jsonl")

if uploaded_file is not None:
    data = load_jsonl(uploaded_file)
    
    # Get unique labels
    unique_topic_systems = get_unique_labels(data, 'meta_info_TopicSystem')
    unique_topic_disciplines = get_unique_labels(data, 'meta_info_TopicDiscipline')
    unique_subspecialities = get_unique_labels(data, 'meta_info_SubSpeciality')
    
    # Create tabs for each question
    tabs = st.tabs([f"Question {idx + 1}" for idx in range(len(data))])
    
    for idx, (item, tab) in enumerate(zip(data, tabs)):
        with tab:
            st.subheader("Persian Translation Revision")
            st.text("English Question:")
            st.write(item['question'])
            
            st.markdown("Persian Question:")
            item['question_persian'] = rtl_text_area(
                f"Persian Question {idx + 1}",
                item['question_persian'],
                persian_question_height,
                key=f"persian_q_{idx}"
            )
            
            st.write("Options:")
            for opt, text in item['options'].items():
                col1, col2 = st.columns(2)
                with col1:
                    st.text(f"{opt}: {text}")
                with col2:
                    item['options_persian'][opt] = rtl_text_area(
                        f"Persian Option {opt}",
                        item['options_persian'][opt],
                        persian_option_height,
                        key=f"persian_opt_{idx}_{opt}"
                    )
                st.markdown("---")  # Add a separator between options
            
            st.subheader("Enrich MedQA")
            
            # New contradictory option
            item['new_contradictory_option'] = rtl_text_area(
                "Contradictory option (in Persian)",
                item.get('new_contradictory_option', ''),
                enrich_height,
                key=f"new_opt_{idx}"
            )
            item['new_contradictory_option_source'] = st.text_area(
                "Source for the contradictory option",
                item.get('new_contradictory_option_source', ''),
                height=enrich_height,
                key=f"new_opt_source_{idx}"
            )
            
            # Additional correct answer
            item['additional_correct_answer'] = rtl_text_area(
                "Additional correct answer (in Persian)",
                item.get('additional_correct_answer', ''),
                enrich_height,
                key=f"add_correct_{idx}"
            )
            item['additional_correct_answer_source'] = st.text_area(
                "Source for the additional correct answer",
                item.get('additional_correct_answer_source', ''),
                height=enrich_height,
                key=f"add_correct_source_{idx}"
            )
            
            st.subheader("Revise Labels")
            st.write("Provide multiple tags separated by ';'. Use items from the current list.")
            
            for key, unique_labels in [
                ('meta_info_TopicSystem', unique_topic_systems),
                ('meta_info_TopicDiscipline', unique_topic_disciplines),
                ('meta_info_SubSpeciality', unique_subspecialities)
            ]:
                label = key.replace('meta_info_', '')
                current_value = item.get(key, '')
                if isinstance(current_value, list):
                    current_value = ';'.join(current_value)
                
                new_value = st.text_area(
                    label,
                    current_value,
                    height=labels_height,
                    key=f"{key}_{idx}"
                )
                st.write(f"Current list: {', '.join(unique_labels)}")
                
                # Convert back to list if necessary
                if ';' in new_value:
                    item[key] = [label.strip() for label in new_value.split(';') if label.strip()]
                else:
                    item[key] = [new_value] if new_value else []
            
            if st.button(f"Save Question {idx + 1}", key=f"save_{idx}"):
                st.success(f"Changes for Question {idx + 1} saved successfully!")

    if st.button("Save All Changes"):
        output = save_jsonl(data)
        st.download_button(
            label="Download modified JSONL",
            data=output,
            file_name="modified_medqa.jsonl",
            mime="application/json"
        )

st.sidebar.markdown("""
## Instructions
1. Upload a JSONL file using the file uploader.
2. Adjust text box heights in the sidebar settings.
3. Use the tabs to navigate between questions.
4. Review and modify the Persian translations for questions and options.
5. In the Enrich MedQA section, add or edit contradictory options and additional correct answers with their sources.
6. In the Revise Labels section, update the topic system, discipline, and subspeciality. Use semicolons (;) to separate multiple tags.
7. Click 'Save Question X' to save changes for a specific question.
8. Click 'Save All Changes' to download the complete modified JSONL file.
9. You can reupload the modified file for further editing.
""")