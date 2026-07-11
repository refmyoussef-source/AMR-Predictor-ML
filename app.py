import streamlit as st
import pandas as pd
import joblib
import itertools
from Bio import SeqIO
from io import StringIO

# --- 1. Page Config ---
st.set_page_config(page_title="AMR Predictor", page_icon="🧬", layout="centered")

st.title("🧬 AMR-Predictor: Meropenem Resistance")
st.markdown("Upload a *Klebsiella pneumoniae* FASTA file to predict Meropenem resistance using our Cost-Sensitive XGBoost Model.")

# --- 2. Load the Model ---
@st.cache_resource
def load_model():
    return joblib.load("models/final_xgboost_amr_model.pkl")

try:
    model = load_model()
    st.success("✅ Model loaded successfully!")
except Exception as e:
    st.error(f"⚠️ Error loading model: {e}")

# --- 3. K-mer Extraction Function ---
def extract_kmers(fasta_text, k=6):
    bases = ['A', 'C', 'G', 'T']
    all_kmers = [''.join(p) for p in itertools.product(bases, repeat=k)]
    kmer_counts = {kmer: 0 for kmer in all_kmers}
    
    record = SeqIO.read(StringIO(fasta_text), "fasta")
    seq = str(record.seq).upper()
    
    total_kmers = len(seq) - k + 1
    for i in range(total_kmers):
        kmer = seq[i:i+k]
        if kmer in kmer_counts:
            kmer_counts[kmer] += 1
            
    df_kmers = pd.DataFrame([kmer_counts])
    return df_kmers, record.id

# --- 4. User Interface ---
uploaded_file = st.file_uploader("Upload FASTA File (.fasta, .fa, .fna)", type=["fasta", "fa", "fna"])

if uploaded_file is not None:
    fasta_string = uploaded_file.getvalue().decode("utf-8")
    
    with st.spinner("⏳ Analyzing DNA sequence and extracting 4,096 K-mers..."):
        try:
            features_df, genome_id = extract_kmers(fasta_string)
            st.write(f"**Genome ID / Header:** `{genome_id}`")
            
            # 🔥 THE FIX: Align column names and order exactly as the model expects
            expected_features = model.feature_names_in_
            
            # Add missing columns with 0 if any (just in case), though itertools covers all
            for col in expected_features:
                if col not in features_df.columns:
                    features_df[col] = 0
                    
            # Reorder to match model strictly
            features_df = features_df[expected_features]
            
            # Make Prediction
            prediction = model.predict(features_df)[0]
            probability = model.predict_proba(features_df)[0][1] * 100
            
            # Display Results
            st.markdown("### 📊 Prediction Result")
            if prediction == 1:
                st.error(f"🚨 **RESISTANT to Meropenem** (Confidence: {probability:.2f}%)")
                st.markdown("⚠️ This strain likely carries AMR genes.")
            else:
                st.success(f"🟢 **SUSCEPTIBLE to Meropenem** (Confidence: {100 - probability:.2f}%)")
                st.markdown("✅ This strain can likely be treated with Meropenem.")
                
        except Exception as e:
            # Now it will print the EXACT error if it fails again
            st.error(f"⚠️ App Error: {str(e)}")
