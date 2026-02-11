import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(page_title="Collecte Proximité", page_icon="📋")

# Titre de l'application
st.title("📋 Fiche Contact - Proximité")
st.markdown("---")

# Fonction pour charger ou créer le fichier de données
def load_data(filename="donnees_proximite.csv"):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=[
            "Date de saisie", "Nom", "Prénom", "Âge", 
            "Date de Naissance", "Adresse", "Code Postal", 
            "Statut FT/ML", "Téléphone", "Observations"
        ])

# Formulaire de saisie
with st.form("contact_form", clear_on_submit=True):
    st.subheader("Informations Personnelles")
    
    col1, col2 = st.columns(2)
    nom = col1.text_input("NOM")
    prenom = col2.text_input("PRÉNOM")
    
    col3, col4 = st.columns(2)
    # L'âge pourrait être calculé automatiquement, mais je laisse le champ libre comme demandé
    age = col3.number_input("ÂGE", min_value=16, max_value=100, step=1)
    date_naissance = col4.date_input("DATE DE NAISSANCE", min_value=datetime(1950, 1, 1))
    
    st.subheader("Coordonnées")
    adresse = st.text_input("ADRESSE")
    code_postal = st.text_input("CODE POSTAL", max_chars=5)
    telephone = st.text_input("NUMÉRO DE TÉLÉPHONE")
    
    st.subheader("Situation")
    statut = st.radio(
        "INSCRIT À FRANCE TRAVAIL ou MISSION LOCALE ?",
        ("Oui", "Non", "Ne sait pas"),
        horizontal=True
    )
    
    observations = st.text_area("OBSERVATIONS DIVERSES")
    
    # Bouton de validation
    submitted = st.form_submit_button("Enregistrer le profil")

# Traitement lors de la validation
if submitted:
    if not nom or not telephone:
        st.error("⚠️ Le NOM et le TÉLÉPHONE sont obligatoires.")
    else:
        new_data = {
            "Date de saisie": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nom": nom.upper(),
            "Prénom": prenom.capitalize(),
            "Âge": age,
            "Date de Naissance": date_naissance,
            "Adresse": adresse,
            "Code Postal": code_postal,
            "Statut FT/ML": statut,
            "Téléphone": telephone,
            "Observations": observations
        }
        
        df = load_data()
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv("donnees_proximite.csv", index=False)
        
        st.success(f"✅ Profil de {prenom} {nom} enregistré avec succès !")

# Section pour visualiser/exporter les données (visible uniquement par vous)
st.markdown("---")
with st.expander("📂 Voir les données enregistrées"):
    df_view = load_data()
    st.dataframe(df_view)
    
    # Bouton de téléchargement CSV
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger les données (CSV)",
        data=csv,
        file_name='contacts_proximite.csv',
        mime='text/csv',
    )
