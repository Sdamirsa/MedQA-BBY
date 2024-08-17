import streamlit as st
import json
import pandas as pd
from io import StringIO
import tempfile
import os
from pathlib import Path


def load_jsonl(file):
    data = []
    content = file.read().decode('utf-8')
    for line in content.split('\n'):
        if line.strip():
            data.append(json.loads(line))
    return data


def serialize_streamlit(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, list):
        return [serialize_streamlit(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_streamlit(value) for key, value in obj.items()}
    else:
        return str(obj)

def save_jsonl(data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        for item in data:
            serialized_item = serialize_streamlit(item)
            json.dump(serialized_item, temp_file, ensure_ascii=False)
            temp_file.write('\n')
    
    with open(temp_file.name, 'r', encoding='utf-8') as file:
        content = file.read()
    
    os.unlink(temp_file.name)
    return content

def rtl_text_area(label, value, height, key):
    st.markdown(f"""
    <div dir="rtl">
        <p>{label}</p>
        <textarea style="width: 100%; height: {height}px; direction: rtl; text-align: right;" name="{key}" id="{key}">{value}</textarea>
    </div>
    """, unsafe_allow_html=True)
    return st.text_input(f"Hidden input for {label}", value=value, key=f"hidden_{key}", label_visibility="collapsed")

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
    .rtl {
        direction: rtl;
        text-align: right;
    }
    textarea {
        font-size: 14px;
        font-family: Arial, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.title("Settings")
persian_question_height = st.sidebar.slider("Persian Question Height", min_value=100, max_value=500, value=150, step=50)
persian_option_height = st.sidebar.slider("Persian Option Height", min_value=50, max_value=200, value=50, step=25)
enrich_height = st.sidebar.slider("Enrich MedQA Text Height", min_value=50, max_value=200, value=50, step=25)
labels_height = st.sidebar.slider("Labels Text Height", min_value=50, max_value=200, value=50, step=25)

uploaded_file = st.file_uploader("Choose a JSONL file", type="jsonl")

if uploaded_file is not None:
    original_filename = uploaded_file.name
    data = load_jsonl(uploaded_file)
    
    # Get unique labels
    unique_topic_systems = r"Endocrine System,  Nervous System,  Gastrointestinal System, Cardiovascular System,  Musculoskeletal System & Skin,  Respiratory System,  Renal & Urinary System,  Hematologic System,  Immune System,  Psychiatry & Behavioral Health,  General Principles,  Biochemistry,  Ophthalmic system,  Pediatrics,  Behavioral Health,  Biostatistics & Epidemiology,  Reproductive System"
    unique_topic_disciplines = "Clinical Diagnosis and Management, **Diagnosis, Management, Investigation**, Pharmacology,  Pathology,  Microbiology and Immunology,  Genetics,  Epidemiology and Biostatistics,  Physiology,  Biochemistry,  Anatomy,  Ethics,  Embryology,  Cognitive Skills,  Preventive Medicine,  Psychology,  Pediatrics,  Nutrition, Pyschology"
    unique_subspecialities = r"Pediatrics,  Gastroenterology,  Obstetrics & Gynecology,  Endocrinology, Neurology,  Infectious Diseases,  Hematology,  Cardiology,  Pulmonology,  Emergency Medicine,  Psychiatry,  Nephrology,  Rheumatology,  Surgery,  Internal Medicine,  Dermatology,  Allergy & Immunology,  Urology,  Geriatrics,  Education & Management,  Critical Care,  Ophthalmology, Anesthesiology,  Otolaryngology,  Infection Diseases,  Orthopedic Surgery,  Pathology,  Sports Medicine"
    
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
            st.write(f'Correct answer is: ✔️**{item['answer']}**')
            
            st.subheader("Options:")
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

            st.markdown("--------")  
            st.subheader("Revise Labels")
            st.info("Provide multiple tags separated by ';'. Use items from the current list.")
            
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
                st.write(f"*Current list*: {unique_labels}")
                st.write("\n")
                
                # Convert back to list if necessary
                if ';' in new_value:
                    item[key] = [label.strip() for label in new_value.split(';') if label.strip()]
                else:
                    item[key] = [new_value] if new_value else []
                    
            st.markdown("--------")                   
            st.subheader("Enrich MedQA")
            
            # New question stem
            item['new_question_stem'] = st.text_area(
                "New question stem (in English)",
                value=item.get('new_question_stem', item['question']),
                height=persian_question_height,
                key=f"new_question_stem_{idx}"
            )
                      
            # New contradictory option
            item['new_contradictory_option'] = st.text_area(
                "Contradictory option (in English)",
                item.get('new_contradictory_option', ''),
                height=enrich_height,
                key=f"new_opt_{idx}"
            )
            item['new_contradictory_option_source'] = st.text_area(
                "Source for the contradictory option",
                item.get('new_contradictory_option_source', ''),
                height=enrich_height,
                key=f"new_opt_source_{idx}"
            )
            
            # Additional correct answer
            item['additional_correct_answer'] = st.text_area(
                "Additional correct answer (in English)",
                item.get('additional_correct_answer', ''),
                height=enrich_height,
                key=f"add_correct_{idx}"
            )
            item['additional_correct_answer_source'] = st.text_area(
                "Source for the additional correct answer",
                item.get('additional_correct_answer_source', ''),
                height=enrich_height,
                key=f"add_correct_source_{idx}"
            )
            

            st.markdown("--------") 
            if st.button(f"Save Question {idx + 1}", key=f"save_{idx}"):
                st.success(f"Changes for Question {idx + 1} saved successfully!")

    if st.button("Export Modified File"):
        output = save_jsonl(data)
        
        # Generate the new filename
        base_name = Path(original_filename).stem
        new_filename = f"{base_name}_modified.jsonl"
        
        st.download_button(
            label="Download modified JSONL",
            data=output,
            file_name=new_filename,
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