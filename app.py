import streamlit as st
import pandas as pd
from planning_core import generate_planning

st.set_page_config(page_title="Planning Restaurant", layout="wide")

st.title("📅 Générateur de planning pour restaurant")

# 1️⃣ Téléverser un fichier de besoins
uploaded_file = st.file_uploader("1️⃣ Charger le fichier de besoins (Excel)", type=["xlsx"])

if uploaded_file:
    besoins_df = pd.read_excel(uploaded_file)
    st.success("✅ Fichier chargé avec succès.")
else:
    # Exemple de tableau par défaut
    besoins_df = pd.DataFrame({
        "Jour": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
        **{f"{h}:00": [1]*7 for h in range(10, 24)}  # Besoins de 10h à 23h
    })
    st.info("ℹ️ Aucun fichier importé, modèle par défaut utilisé.")

# 2️⃣ Modifier les besoins horaires
st.subheader("2️⃣ Modifier les besoins horaires")
editable_df = st.data_editor(besoins_df, num_rows="dynamic", use_container_width=True)

# 3️⃣ Nombre d’employés disponibles
st.subheader("3️⃣ Nombre d’employés disponibles")
num_workers = st.slider("Sélectionner le nombre d'employés", min_value=1, max_value=20, value=6)

# 4️⃣ Générer le planning
if st.button("4️⃣ Générer le planning"):
    with st.spinner("⏳ Génération du planning..."):
        try:
            # Créer le dictionnaire des besoins
            weekly_chef_need = {}
            for _, row in editable_df.iterrows():
                jour = row["Jour"]
                heures = [int(row[f"{h}:00"]) for h in range(10, 24)]
                weekly_chef_need[jour] = heures

            # Générer le planning
            output_path = generate_planning(num_workers, weekly_chef_need)

            st.success("✅ Planning généré avec succès.")
            with open(output_path, "rb") as file:
                st.download_button("📥 Télécharger le planning Excel", data=file, file_name="planning.xlsx")

        except Exception as e:
            st.error(f"❌ Erreur : {e}")
