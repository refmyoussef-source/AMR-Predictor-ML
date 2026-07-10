# 🧬 AMR-Predictor-ML: Machine Learning for Meropenem Resistance in Klebsiella pneumoniae

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Optimized-red.svg)](https://xgboost.readthedocs.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Enabled-orange.svg)](https://scikit-learn.org/)

## 📖 Project Overview
Antimicrobial Resistance (AMR) is one of the top global public health threats. This project leverages Machine Learning to predict **Meropenem** (a last-resort antibiotic) resistance in *Klebsiella pneumoniae* directly from genomic data. By extracting 6-mer DNA motifs and applying an optimized, cost-sensitive XGBoost model, we decode the genomic signatures of resistance.

## 🎯 Key Objectives
* Formulate AMR prediction as a binary classification problem (Susceptible vs. Resistant).
* Handle the "Curse of Dimensionality" using statistical feature selection (ANOVA F-Test).
* Address extreme class imbalance using Cost-Sensitive Learning to maximize the detection of resistant strains (Recall).
* Interpret the biological relevance of the model's top predictive K-mers.

## 📊 Dataset
* **Source:** Derived from the PATRIC (Pathosystems Resource Integration Center) database.
* **Samples:** 2,836 complete bacterial genomes.
* **Features:** 4,096 genomic 6-mer frequencies + 5 metadata columns.
* **Target:** `AMR_Label` (0 = Susceptible, 1 = Resistant).

## 🛠️ Machine Learning Pipeline
The project is structured into 6 main phases documented in Jupyter Notebooks:
1. **`01_data_exploration.ipynb`**: Exploratory Data Analysis (EDA) and phenotype distribution.
2. **`02_data_preprocessing.ipynb`**: Target encoding and genomic sequence scaling.
3. **`03_baseline_modeling.ipynb`**: Establishing baselines with Random Forest and XGBoost.
4. **`04_feature_selection.ipynb`**: Dimensionality reduction (4,096 ➡️ 500 features) using SelectKBest.
5. **`05_model_optimization.ipynb`**: Applying `scale_pos_weight` (1.65) to penalize False Negatives. 
6. **`06_interpretability_deployment.ipynb`**: Extracting Top 20 biological K-mer motifs and saving the `.pkl` model.

## 🏆 Final Model Performance (Champion Model)
Our best-performing model is the **Cost-Sensitive XGBoost trained on all 4,096 features**. It successfully balanced general accuracy with a highly penalized recall for the resistant class.

* **Global Accuracy:** `70.25%`
* **ROC-AUC Score:** `75.31%`
* **Resistant Recall:** `59%` *(Improved from 35% baseline)*

### Biological Interpretability
The model identified C-rich and G-rich motifs (e.g., `CACCCC`, `CCCCTG`) as the top predictive features. These motifs are strongly correlated with plasmid and transposon regions, which are the primary vehicles for AMR genes (like *blaKPC* or *blaNDM*) in *K. pneumoniae*.
