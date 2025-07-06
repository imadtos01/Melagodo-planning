import streamlit as st
import pandas as pd
from planning_core import generate_planning

st.set_page_config(page_title="Planning Melagodo", layout="wide")
st.title("📅 Générateur de planning pour Melagodo")

# ------------------ 1. Configurer les jours et heures
DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
HOURS = [f"{h}:00" for h in range(10, 24)]

# ------------------ 2. Créer le tableau initial si aucun fichier n'est chargé
default_data = {hour: [0] * len(DAYS) for hour in HOURS}
default_data["Jour"] = DAYS
df = pd.DataFrame(default_data)
df = df[["Jour"] + HOURS]  # Réorganiser colonnes

st.header("📝 Modifier les besoins horaires par jour et créneau horaire")
edited_df = st.data_editor(df, num_rows="fixed", use_container_width=True)

# ------------------ 3. Choisir le nombre d'employés
st.header("👨‍🍳 Nombre d’employés disponibles")
num_workers = st.slider("Sélectionner le nombre d'employés", min_value=1, max_value=20, value=6)

# ------------------ 4. Générer le planning
if st.button("📊 Générer le planning"):
    try:
        # Préparer les besoins sous forme de dict
        weekly_chef_need = {row["Jour"]: [int(row[h]) for h in HOURS] for _, row in edited_df.iterrows()}
        planning_df = generate_planning(num_workers, weekly_chef_need)

        if planning_df is not None:
            st.success("✅ Planning généré avec succès !")
            st.dataframe(planning_df, use_container_width=True)

            # Export Excel
            st.download_button(
                label="📥 Télécharger le planning (Excel)",
                data=planning_df.to_excel(index=False),
                file_name="planning_melagodo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("❌ Aucun planning trouvé. Essayez d’ajuster les besoins ou le nombre d’employés.")
    except Exception as e:
        st.error(f"Erreur : {e}")
