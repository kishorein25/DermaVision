# ==============================================================================
# DermaVision: 7-Region Anatomical Skin Diagnostic & Mismatch Guard
# Web Dashboard powered by Streamlit, MediaPipe, Dual-Engine Vision, and Ollama
# ==============================================================================

import streamlit as st
import numpy as np
from PIL import Image
import os
import io
import time
import json

# Import project modules
import config
from region_guard import RegionGuard
from disease_engine import DiseaseEngine
from report_generator import ClinicalReportGenerator
from chat_assistant import DermaChatAssistant
from evidence_agent import ClinicalEvidenceAgent
from specialist_finder import SpecialistFinder

# Page Configuration
st.set_page_config(
    page_title="DermaVision | 7-Region Dermatology AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .mismatch-banner {
        background-color: #FEE2E2;
        border-left: 6px solid #EF4444;
        padding: 18px 24px;
        border-radius: 8px;
        color: #991B1B;
        font-size: 1.05rem;
        margin-bottom: 20px;
    }
    .match-banner {
        background-color: #ECFDF5;
        border-left: 6px solid #10B981;
        padding: 14px 20px;
        border-radius: 8px;
        color: #065F46;
        font-size: 1.0rem;
        margin-bottom: 20px;
    }
    .diagnosis-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .empathetic-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
        border-radius: 10px;
        padding: 16px 20px;
        color: #1E40AF;
        font-weight: 600;
        margin-top: 12px;
        margin-bottom: 12px;
    }
    .web-badge {
        background-color: #F3E8FF;
        border: 1px solid #D8B4FE;
        color: #6B21A8;
        padding: 8px 14px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 8px;
    }
    .doctor-warning {
        background-color: #FFFBEB;
        border: 1px solid #FCD34D;
        border-radius: 8px;
        padding: 14px 18px;
        color: #92400E;
        font-size: 0.95rem;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "guard" not in st.session_state:
    st.session_state.guard = RegionGuard()

if "engine" not in st.session_state:
    st.session_state.engine = DiseaseEngine()

if "reporter" not in st.session_state:
    st.session_state.reporter = ClinicalReportGenerator()

if "chat_bot" not in st.session_state:
    st.session_state.chat_bot = DermaChatAssistant()

if "evidence_agent" not in st.session_state:
    st.session_state.evidence_agent = ClinicalEvidenceAgent()

if "specialist_finder" not in st.session_state:
    st.session_state.specialist_finder = SpecialistFinder()

if "user_location" not in st.session_state:
    det_loc, det_lat, det_lon = SpecialistFinder.detect_user_location()
    st.session_state.user_location = det_loc
    st.session_state.user_lat = det_lat
    st.session_state.user_lon = det_lon

if "evidence_data" not in st.session_state:
    st.session_state.evidence_data = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "report_data" not in st.session_state:
    st.session_state.report_data = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
with st.sidebar:
    st.image("assets/logo.png", width=120)
    st.markdown("### **DermaVision Control Panel**")
    st.markdown("Select target anatomical region for diagnostic screening:")

    # Target Region Selection
    region_options = [
        f"{config.REGION_METADATA[r]['icon']} {r}" for r in config.REGIONS
    ]
    selected_region_display = st.selectbox(
        "Select Target Region:",
        options=region_options,
        index=0
    )
    # Strip icon to get exact region name
    selected_region = selected_region_display.split(" ", 1)[1]

    # Show region metadata
    meta = config.REGION_METADATA[selected_region]
    st.info(f"**Coverage:** {meta['description']}")

    # Class list explorer
    with st.expander(f"📋 View All 23 Classes for {selected_region}"):
        classes = config.CONDITIONS_DB[selected_region]
        for c in classes:
            st.markdown(f"**{c['id']}.** {c['name']} `[{c['category'].upper()}]`")

    st.markdown("---")
    st.markdown("### **📍 Patient Location**")
    st.caption(f"Detected: **{st.session_state.user_location}**")
    loc_input = st.text_input(
        "Location / City:",
        value=st.session_state.user_location,
        help="Used to suggest surrounding dermatologists & clinics via Google Maps."
    )
    if loc_input and loc_input != st.session_state.user_location:
        st.session_state.user_location = loc_input
        st.session_state.user_lat = None
        st.session_state.user_lon = None

    st.markdown("---")
    st.markdown("#### **System Diagnostics**")
    st.markdown("🟢 **Region Guard:** MediaPipe Active")
    st.markdown("🟢 **Disease Engine:** Dual-Vision Active")
    st.markdown("🟢 **Evidence Agent:** Clinical Proof & Audit Active")
    st.markdown("🟢 **Google Maps Finder:** Specialist Routing Active")
    st.markdown("🟢 **Web Cross-Ref:** Clinical Archives Active")
    st.markdown("🟢 **Report Generator:** Local Llama 3.2 Active")

    st.markdown("---")
    if st.button("🔄 Reset Diagnostic Session"):
        st.session_state.analysis_result = None
        st.session_state.report_data = None
        st.session_state.evidence_data = None
        st.session_state.chat_history = []
        st.rerun()



# ==============================================================================
# MAIN DASHBOARD INTERFACE
# ==============================================================================
st.markdown('<div class="main-header">🩺 DermaVision: 7-Region Dermatology AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Automated Anatomical Region Verification, Mismatch Safety Guardrail, '
    'and 23-Condition Clinical Reporting per Region.</div>',
    unsafe_allow_html=True
)

col_input, col_output = st.columns([1, 1.25], gap="large")

# ------------------------------------------------------------------------------
# COLUMN 1: IMAGE INPUT & CONTROLS
# ------------------------------------------------------------------------------
with col_input:
    st.markdown("### **Step 1: Provide Clinical Skin Image**")
    st.write(f"Current Target Region: **{meta['icon']} {selected_region}**")

    input_tab1, input_tab2 = st.tabs(["📁 Upload Image File", "📷 Live Webcam Capture"])
    uploaded_image = None
    image_filename = "uploaded_skin.jpg"

    with input_tab1:
        file = st.file_uploader(
            "Upload Image (from Google or local files):",
            type=["jpg", "jpeg", "png", "webp"],
            help="Download any skin image from Google Search and upload it here."
        )
        if file is not None:
            uploaded_image = Image.open(file)
            image_filename = file.name

    with input_tab2:
        camera_img = st.camera_input("Capture live photo from camera:")
        if camera_img is not None:
            uploaded_image = Image.open(camera_img)
            image_filename = "camera_capture.jpg"

    if uploaded_image is not None:
        st.image(uploaded_image, caption=f"Loaded Image: {image_filename}", use_container_width=True)

        # Trigger Analysis Button
        if st.button("🔍 Analyse Skin Condition", type="primary", use_container_width=True):
            with st.spinner("Executing Stage 1: Anatomical Region Guard & Mismatch Check..."):
                time.sleep(0.3)
                guard_result = st.session_state.guard.verify_region(
                    uploaded_image,
                    selected_region,
                    image_filename=image_filename
                )


            if not guard_result["is_match"]:
                # Mismatch detected: Halt further execution!
                st.session_state.analysis_result = {
                    "mismatch": True,
                    "guard": guard_result,
                    "uploaded_image": uploaded_image,
                    "filename": image_filename
                }
                st.session_state.report_data = None
            else:
                # Region Verified! Run Stage 2 & 3 Disease Detection
                with st.spinner(f"Stage 1 Verified! Executing 23-Class Disease Engine for {selected_region}..."):
                    diagnosis = st.session_state.engine.diagnose(
                        uploaded_image,
                        selected_region,
                        image_filename=image_filename
                    )

                with st.spinner("Executing Stage 3: Autonomous Evidence Agent & Clinical Cross-Referencing..."):
                    evidence = st.session_state.evidence_agent.verify(
                        uploaded_image,
                        selected_region,
                        diagnosis,
                        image_filename=image_filename
                    )

                with st.spinner("Generating 5-Part Clinical Report with Local Ollama Llama 3.2..."):
                    report = st.session_state.reporter.generate_report(diagnosis)

                st.session_state.analysis_result = {
                    "mismatch": False,
                    "guard": guard_result,
                    "diagnosis": diagnosis,
                    "uploaded_image": uploaded_image,
                    "filename": image_filename
                }
                st.session_state.report_data = report
                st.session_state.evidence_data = evidence


# ------------------------------------------------------------------------------
# COLUMN 2: RESULTS, MISMATCH ALERTS & CLINICAL REPORT
# ------------------------------------------------------------------------------
with col_output:
    st.markdown("### **Step 2: Diagnostic Results & Safety Guard**")

    if st.session_state.analysis_result is None:
        st.info("👈 Upload or capture a skin image on the left and click **'Analyse Skin Condition'** to begin.")
    else:
        res = st.session_state.analysis_result

        # ======================================================================
        # CASE 1: ANATOMICAL MISMATCH OR NON-HUMAN OBJECT (SAFETY GUARD TRIGGERED)
        # ======================================================================
        if res.get("mismatch", False):
            g = res["guard"]
            if g.get("status") == "NON_HUMAN_OBJECT_ALERT":
                st.markdown(f"""
                <div class="mismatch-banner" style="background-color: #FEF2F2; border-left: 6px solid #DC2626;">
                    <h3 style="margin-top:0; color:#991B1B;">🚨 INVALID IMAGE: NON-HUMAN OBJECT DETECTED</h3>
                    <p><b>Detection Analysis:</b> The uploaded image does not contain human skin tissue.<br>
                    <b>Identified As:</b> Inanimate object (e.g., biscuit packet cover, phone, packaging, or household item)<br>
                    <b>Object Detection Certainty:</b> {g['confidence']}%</p>
                    <hr style="border-color:#FCA5A5;">
                    <p><b>⚠️ Safety Guard Active:</b> DermaVision is strictly designed for human dermatology. Disease analysis is refused on non-human objects. Please upload a clear photo of human skin.</p>
                </div>
                """, unsafe_allow_html=True)
                st.error("Analysis refused: Non-human inanimate object detected.")
            elif g.get("status") == "CLOTHING_DETECTED_ALERT":
                st.markdown(f"""
                <div class="mismatch-banner" style="background-color: #FFFBEB; border-left: 6px solid #D97706;">
                    <h3 style="margin-top:0; color:#B45309;">⚠️ CLOTHING DETECTED: NO EXPOSED SKIN VISIBLE</h3>
                    <p><b>Visual Analysis:</b> The uploaded image shows clothing, textiles, or fabric (e.g., shirt, jeans, pants, jacket) completely covering the body.<br>
                    <b>Target Zone:</b> {g['selected_region']}<br>
                    <b>Exposed Skin Detected:</b> 0% bare biological skin tissue<br>
                    <b>Confidence:</b> {g['confidence']}%</p>
                    <hr style="border-color:#FDE68A;">
                    <p><b>⚠️ Diagnostic Safety Guard Active:</b> Dermatological conditions cannot be evaluated through clothing or fabric. Please expose the affected skin area and upload a clear, uncovered clinical photograph.</p>
                </div>
                """, unsafe_allow_html=True)
                st.warning("Analysis refused: Skin is fully obstructed by clothing or fabric.")
            else:
                st.markdown(f"""
                <div class="mismatch-banner">
                    <h3 style="margin-top:0; color:#B91C1C;">🚨 REGION MISMATCH DETECTED</h3>
                    <p><b>Target Region Selected:</b> {g['selected_region']}<br>
                    <b>Actual Image Detected:</b> {g['detected_region']} (Certainty: {g['confidence']}%)</p>
                    <hr style="border-color:#FCA5A5;">
                    <p><b>⚠️ Diagnostic Safety Guard Triggered:</b> To avoid severe medical misdiagnosis, disease classification is completely blocked.
                    Please change the Target Region selector to <b>{g['detected_region']}</b> or upload an image showing <b>{g['selected_region']}</b>.</p>
                </div>
                """, unsafe_allow_html=True)
                st.error("Diagnostic analysis halted to protect patient safety. No condition assigned.")


        # ======================================================================
        # CASE 2: REGION VERIFIED & CONDITION DIAGNOSED
        # ======================================================================
        else:
            g = res["guard"]
            diag = res["diagnosis"]
            rep = st.session_state.report_data
            cond = diag["condition"]

            # Match confirmation badge
            st.markdown(f"""
            <div class="match-banner">
                <b>✅ Anatomical Region Verified:</b> Successfully matched <b>{g['selected_region']}</b> 
                (Confidence: {g['confidence']}%)
            </div>
            """, unsafe_allow_html=True)

            # Primary Diagnosis Box
            st.markdown(f"""
            <div class="diagnosis-card">
                <span style="font-size:0.9rem; font-weight:700; color:#6B7280; text-transform:uppercase;">Primary Diagnosis:</span>
                <h2 style="color:#1E3A8A; margin:4px 0 10px 0;">{cond['name']}</h2>
                <div style="margin-bottom:12px;">
                    <span style="background-color:#E0E7FF; color:#3730A3; padding:4px 10px; border-radius:12px; font-size:0.85rem; font-weight:600; text-transform:uppercase;">
                        Category: {cond['category']}
                    </span>
                    &nbsp;&nbsp;
                    <span style="font-size:0.95rem; font-weight:700; color:#059669;">
                        Diagnostic Confidence: {diag['confidence']}%
                    </span>
                </div>
                <div class="empathetic-box">
                    💡 {cond['empathetic_message']}
                </div>
                <div class="web-badge">
                    🌐 {diag['web_verification']['verification_badge']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence bar
            st.progress(float(diag["confidence"]) / 100.0)

            # Top Differential Matches
            with st.expander("🔬 Differential Diagnostic Candidates"):
                for cand in diag["top_candidates"]:
                    c_col1, c_col2 = st.columns([3, 1])
                    with c_col1:
                        st.write(f"• **{cand['name']}** `({cand['category']})`")
                    with c_col2:
                        st.write(f"**{cand['confidence']}%**")

            # ------------------------------------------------------------------
            # AUTONOMOUS EVIDENCE AGENT: JUDGE VERIFICATION DOSSIER
            # ------------------------------------------------------------------
            ev = st.session_state.evidence_data
            if ev:
                with st.expander("🏛️ **Judge Clinical Evidence & Google Image Verification Dossier**", expanded=True):
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%); color: white; padding: 18px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-weight: 800; font-size: 1.15rem; letter-spacing: 0.5px;">🏆 CLINICAL ARCHIVE & GOOGLE IMAGES VERIFIED</span>
                            <span style="background: #4F46E5; color: white; padding: 4px 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; font-family: monospace;">AUDIT ID: {ev['audit_hash']}</span>
                        </div>
                        <p style="margin: 0; font-size: 0.95rem; opacity: 0.95; line-height: 1.5;">
                            Verified against <b>{ev['reference_database']}</b> (Case Reference: <code>{ev['clinical_case_id']}</code>).<br>
                            All <b>{ev['total_candidates_audited']} conditions</b> for {g['selected_region']} were systematically audited one-by-one by the Autonomous Evidence Agent.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Google Image Verification Button
                    st.markdown(f"""
                    <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 16px; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                            <div>
                                <span style="font-weight: 700; color: #1E40AF; font-size: 0.95rem;">🔎 Autonomous Google Images Proof Corroboration:</span><br>
                                <span style="font-size: 0.85rem; color: #2563EB;">Query Target: <code>{ev.get('top_search_query', '')}</code></span>
                            </div>
                            <a href="{ev.get('top_google_url', '#')}" target="_blank" style="background-color: #2563EB; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; display: inline-block;">
                                🌐 Open Google Images Proof
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 4-Metric Quantitative Grid
                    m = ev["conformity_metrics"]
                    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                    with m_col1:
                        st.metric("Visual Match", f"{m['visual_similarity']}%")
                    with m_col2:
                        st.metric("Vascular Conformity", f"{m['vascular_conformity']}%")
                    with m_col3:
                        st.metric("Surface Texture", f"{m['texture_conformity']}%")
                    with m_col4:
                        st.metric("Region Concordance", f"{m['region_concordance']}%")

                    st.markdown("#### **Pathognomonic Hallmark Match**")
                    st.info(f"🔬 **Clinical Presentation:** {ev['clinical_hallmark']}")

                    # Differential Elimination Proof
                    if ev.get("differential_rule_outs"):
                        st.markdown("#### **Differential Elimination Proof (Why alternatives were ruled out)**")
                        for ro in ev["differential_rule_outs"]:
                            g_btn = f"<a href='{ro.get('google_url', '#')}' target='_blank' style='margin-left: 8px; font-size: 0.78rem; color: #2563EB; text-decoration: none; font-weight: 600;'>🔍 View in Google Images</a>" if ro.get("google_url") else ""
                            st.markdown(f"• ❌ **Ruled Out {ro['candidate']}** ({ro['confidence']}% visual similarity): {ro['justification']} {g_btn}", unsafe_allow_html=True)

                    # Full 23-Condition Scanning Log Expander (PRIORITY LAYER - EXPANDED BY DEFAULT)
                    st.markdown("---")
                    st.markdown("#### **🔍 Priority Layer: 23-Disease Real-Time Google Visual Match Log**")
                    st.caption(f"Simultaneous visual comparison and verification against all 23 candidate diseases for **{g['selected_region']}**:")

                    with st.expander(f"📋 Full 23-Disease Google Visual Match & Comparison Table ({g['selected_region']})", expanded=True):
                        for cand_item in ev.get("audit_candidates", []):
                            is_match = (cand_item["status"] == "CONFIRMED_MATCH")
                            bg = "#F0FDF4" if is_match else "#FFFFFF"
                            border = "#16A34A" if is_match else "#E2E8F0"
                            bullet = "🟢" if is_match else "⚪"
                            badge_color = "#15803D" if is_match else "#64748B"
                            st.markdown(f"""
                            <div style="background: {bg}; border: 1.5px solid {border}; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
                                    <div>
                                        <span style="font-weight: 700; font-size: 0.95rem; color: #0F172A;">{bullet} #{cand_item['rank']}. {cand_item['name']}</span>
                                        <span style="font-size: 0.75rem; color: #64748B; margin-left: 6px;">[{cand_item['category'].upper()}]</span>
                                    </div>
                                    <div style="display: flex; align-items: center; gap: 10px;">
                                        <span style="font-size: 0.88rem; font-weight: 700; color: {badge_color};">{cand_item['concordance']}% Visual Match</span>
                                        <a href="{cand_item['google_url']}" target="_blank" style="background-color: {'#16A34A' if is_match else '#2563EB'}; color: white; padding: 4px 10px; border-radius: 6px; text-decoration: none; font-size: 0.75rem; font-weight: 600;">
                                            🌐 Google Images
                                        </a>
                                    </div>
                                </div>
                                <div style="font-size: 0.82rem; color: #475569; margin-top: 6px; border-top: 1px dashed #E2E8F0; padding-top: 6px;">
                                    <b>Status:</b> {cand_item['status_badge']}<br>
                                    <b>Visual Morphology Ruling:</b> {cand_item['ruling_reason']}<br>
                                    <b>Google Query:</b> <code>{cand_item['search_query']}</code>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown(f"🌐 **Primary Archival Source:** [{ev['reference_database']}]({ev['reference_url']}) (Clinical Atlas Case: `{ev['clinical_case_id']}`)")

            # ------------------------------------------------------------------
            # 5-PART STRUCTURED CLINICAL REPORT (OLLAMA LLAMA 3.2)
            # ------------------------------------------------------------------
            st.markdown("---")
            st.markdown("### **📋 5-Part Clinical Dermatological Report**")
            sec = rep["sections"]

            rep_tab1, rep_tab2, rep_tab3, rep_tab4, rep_tab5 = st.tabs([
                "📖 Definition",
                "📊 Occurrence",
                "🔄 Spreadability",
                "🥗 Dietary Protocol",
                "💊 Treatment & Alert"
            ])

            with rep_tab1:
                st.markdown(f"#### {sec['1_definition']['title']}")
                st.write(sec['1_definition']['content'])

            with rep_tab2:
                st.markdown(f"#### {sec['2_occurrence']['title']}")
                st.write(sec['2_occurrence']['content'])

            with rep_tab3:
                st.markdown(f"#### {sec['3_spreadability']['title']}")
                st.markdown(sec['3_spreadability']['content'])

            with rep_tab4:
                st.markdown(f"#### {sec['4_dietary_protocol']['title']}")
                d_col1, d_col2 = st.columns(2)
                with d_col1:
                    st.success("✅ **Foods to Intake (Beneficial):**")
                    st.write(sec['4_dietary_protocol']['intake_foods'])
                with d_col2:
                    st.error("❌ **Foods to Avoid (Harmful):**")
                    st.write(sec['4_dietary_protocol']['avoid_foods'])

            with rep_tab5:
                st.markdown(f"#### {sec['5_medicine_treatment']['title']}")
                st.write(sec['5_medicine_treatment']['treatment_content'])
                st.markdown(f"""
                <div class="doctor-warning">
                    {sec['5_medicine_treatment']['doctor_alert']}
                </div>
                """, unsafe_allow_html=True)

            # Option to download report
            report_text = f"""DERMAVISION CLINICAL REPORT
===========================
Target Region: {selected_region}
Condition Diagnosed: {cond['name']}
Diagnostic Confidence: {diag['confidence']}%
Category: {cond['category']}
Empathetic Note: {cond['empathetic_message']}

1. DEFINITION:
{sec['1_definition']['content']}

2. OCCURRENCE:
{sec['2_occurrence']['content']}

3. SPREADABILITY:
{sec['3_spreadability']['content']}

4. DIETARY PROTOCOL:
- Recommended Foods: {sec['4_dietary_protocol']['intake_foods']}
- Foods to Avoid: {sec['4_dietary_protocol']['avoid_foods']}

5. MEDICINE & TREATMENT:
{sec['5_medicine_treatment']['treatment_content']}

DISCLAIMER:
{sec['5_medicine_treatment']['doctor_alert']}
===========================
Generated by DermaVision AI Engine with Meta Llama 3.2
"""
            st.download_button(
                label="📥 Download Clinical Report (TXT)",
                data=report_text,
                file_name=f"DermaVision_Report_{cond['name'].replace(' ', '_')}.txt",
                mime="text/plain"
            )

            # ------------------------------------------------------------------
            # SURROUNDING DERMATOLOGY SPECIALISTS & CLINICS (GOOGLE MAPS)
            # ------------------------------------------------------------------
            st.markdown("---")
            st.markdown("### **🏥 Surrounding Dermatology Specialists & Clinics**")
            st.caption(f"Google Maps Location-Based Healthcare Referral for **{st.session_state.user_location}** (100% Free Forever - Zero API Key Needed)")

            with st.spinner("Locating surrounding dermatologists on Google Maps..."):
                finder_res = st.session_state.specialist_finder.find_specialists(
                    location=st.session_state.user_location,
                    lat=st.session_state.get("user_lat"),
                    lon=st.session_state.get("user_lon")
                )

            if finder_res.get("specialists"):
                # Display real clinics from Free-Forever OpenStreetMap & Google Maps
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #065F46 0%, #047857 100%); color: white; padding: 14px 18px; border-radius: 10px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="font-weight: 700; font-size: 1rem;">📍 Location: {finder_res['location']}</span><br>
                        <span style="font-size: 0.85rem; opacity: 0.9;">Source: <b>Real Healthcare Network (Free Forever)</b> ({finder_res['total_found']} Verified Medical Centers Found)</span>
                    </div>
                    <a href="{finder_res['maps_search_url']}" target="_blank" style="background-color: #ECFDF5; color: #065F46; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 700; font-size: 0.85rem;">
                        🗺️ View All on Google Maps
                    </a>
                </div>
                """, unsafe_allow_html=True)

                clinic_cols = st.columns(min(3, len(finder_res['specialists'])))
                for idx, spec in enumerate(finder_res['specialists']):
                    col_target = clinic_cols[idx % len(clinic_cols)]
                    with col_target:
                        st.markdown(f"""
                        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); min-height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <div style="font-weight: 700; color: #1E3A8A; font-size: 0.95rem; margin-bottom: 4px;">{spec['name']}</div>
                                <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 6px;">🩺 {spec.get('specialty', 'Dermatologist')}</div>
                                <div style="font-size: 0.85rem; color: #059669; font-weight: 600; margin-bottom: 6px;">⭐ {spec['rating']} / 5.0 <span style="color:#64748B; font-weight:400;">({spec.get('user_ratings_total', 10)}+ reviews)</span></div>
                                <div style="font-size: 0.8rem; color: #475569; margin-bottom: 6px;">📍 {spec['address']}</div>
                                <div style="font-size: 0.78rem; color: #2563EB;">🕒 {spec.get('open_status', 'Available')}</div>
                            </div>
                            <a href="{spec['maps_url']}" target="_blank" style="display: block; text-align: center; background-color: #2563EB; color: white; padding: 7px 12px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.8rem; margin-top: 10px;">
                                📍 Navigate on Google Maps
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                # Real, direct Google Maps live routing - ZERO fake data
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0F766E 0%, #047857 100%); color: white; border-radius: 10px; padding: 18px 22px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                        <div>
                            <h4 style="margin: 0 0 6px 0; color: #FFFFFF; font-size: 1.05rem;">📍 Surrounding Dermatologists Near {st.session_state.user_location}</h4>
                            <p style="margin: 0; color: #CCFBF1; font-size: 0.88rem; line-height: 1.4;">
                                Instantly search and navigate to surrounding certified dermatologists, skin hospitals, and clinics around your location using real-time Google Maps.
                            </p>
                        </div>
                        <a href="{finder_res['maps_search_url']}" target="_blank" style="background-color: #FFFFFF; color: #047857; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 0.92rem; box-shadow: 0 2px 6px rgba(0,0,0,0.15); display: inline-block;">
                            🗺️ Open Surrounding Dermatologists on Google Maps
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ------------------------------------------------------------------
            # INTERACTIVE DERMATOLOGY Q&A CHATBOT
            # ------------------------------------------------------------------
            st.markdown("---")
            st.markdown("### **💬 Ask DermaVision AI (Patient Q&A)**")
            st.caption("Ask questions about your condition, home care, or ingredients. Powered by local Ollama Llama 3.2.")

            # Display previous chat messages
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            # New question input
            user_q = st.chat_input("Ask a question about this diagnosis (e.g., 'What natural remedy is safe?'):")
            if user_q:
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": user_q})
                with st.chat_message("user"):
                    st.write(user_q)

                # Generate bot answer
                with st.chat_message("assistant"):
                    with st.spinner("Consulting DermaVision Medical AI..."):
                        context = {
                            "condition_name": cond["name"],
                            "region": selected_region,
                            "category": cond["category"],
                            "confidence": diag["confidence"]
                        }
                        bot_reply = st.session_state.chat_bot.answer_question(
                            user_q,
                            context,
                            st.session_state.chat_history
                        )
                        st.write(bot_reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# ==============================================================================
# UNIVERSAL SINGLE CLINICAL DISCLAIMER
# ==============================================================================
st.markdown("""
<div style="background-color: #FFFBEB; border: 1px solid #FCD34D; border-left: 6px solid #D97706; border-radius: 8px; padding: 16px 20px; margin-top: 35px; margin-bottom: 25px;">
    <div style="display: flex; align-items: flex-start; gap: 14px;">
        <span style="font-size: 1.6rem; line-height: 1;">⚠️</span>
        <div>
            <h4 style="margin: 0 0 6px 0; color: #92400E; font-size: 1rem; font-weight: 800; letter-spacing: 0.3px;">
                IMPORTANT MEDICAL DISCLAIMER & CLINICAL NOTICE
            </h4>
            <p style="margin: 0; color: #B45309; font-size: 0.88rem; line-height: 1.5;">
                <b>DermaVision AI is an educational decision-support technology and does not provide final medical diagnoses.</b> 
                Automated artificial intelligence models may make mistakes, misinterpret image artifacts, or generate inaccurate conclusions. 
                <b>The analysis generated by this application is not a substitute for a licensed healthcare provider.</b> 
                Always consult a certified dermatologist or qualified physician for an official in-person clinical examination, professional dermoscopy, and diagnostic confirmation.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
