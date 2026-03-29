# -*- coding: utf-8 -*-
"""App for Phosphate Prediction"""

import gradio as gr
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'Donnees_Phosphate.csv')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl22')
MODEL_SITE_PATH = os.path.join(BASE_DIR, 'modele_site.pkl')
MODEL_QUALITE_PATH = os.path.join(BASE_DIR, 'modele_qualite.pkl')
FLAG_DIR = os.path.join(BASE_DIR, 'flagged_data')
FLAG_CSV_PATH = os.path.join(FLAG_DIR, 'flags.csv')

# Vérifier l'existence des fichiers
print("Fichiers présents :", os.listdir(BASE_DIR))

# Charger le scaler et les modèles avec gestion d'erreurs
try:
    scaler = joblib.load(SCALER_PATH)
    model_site = joblib.load(MODEL_SITE_PATH)
    model_qualite = joblib.load(MODEL_QUALITE_PATH)
    print("Fichiers chargés avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement des fichiers : {e}")
    raise

# Définir les encodages des catégories
site_encoding = {'Sidi Chennane': 0, 'Sidi Daoui': 1}
quality_encoding = {'Faible': 0, 'Haute': 1, 'Moyenne': 2}

# Fonction pour obtenir les plages
def get_ranges(raw_data_path):
    raw_data = pd.read_csv(raw_data_path)
    features = raw_data.drop(['Site d\'extraction', 'Qualité du Phosphate'], axis=1)
    return {col: (features[col].min(), features[col].max()) for col in features.columns}

# Charger les plages
ranges = get_ranges(DATA_PATH)
feature_names = list(ranges.keys())

# Fonction de prédiction avec sortie simplifiée
def predict(p2o5, cao, sio2, humidite, granulometrie):
    try:
        input_data = np.array([p2o5, cao, sio2, humidite, granulometrie]).reshape(1, -1)
        input_df = pd.DataFrame(input_data, columns=feature_names)

        # Appliquer la normalisation
        input_df_normalized = scaler.transform(input_df)

        # Prédire les valeurs
        pred_site = model_site.predict(input_df_normalized)[0]
        pred_qualite = model_qualite.predict(input_df_normalized)[0]

        # Décoder les résultats
        pred_site_name = [k for k, v in site_encoding.items() if v == pred_site][0]
        pred_quality_name = [k for k, v in quality_encoding.items() if v == pred_qualite][0]

        # Sortie brute sans HTML
        result = f"Site d'extraction : {pred_site_name}\nQualité du phosphate : {pred_quality_name}"
        return result
    except Exception as e:
        return f"Erreur : {str(e)}"


def save_flag(p2o5, cao, sio2, humidite, granulometrie, prediction, flag_reason):
    try:
        if prediction is None or str(prediction).strip() == "":
            return "⚠️ Faites d'abord une prédiction, puis cliquez sur Flag."

        os.makedirs(FLAG_DIR, exist_ok=True)
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "p2o5": p2o5,
            "cao": cao,
            "sio2": sio2,
            "humidite": humidite,
            "granulometrie": granulometrie,
            "prediction": prediction,
            "flag_reason": flag_reason,
        }

        df_row = pd.DataFrame([row])
        write_header = not os.path.exists(FLAG_CSV_PATH)
        df_row.to_csv(FLAG_CSV_PATH, mode="a", header=write_header, index=False)

        return " Flag saved successfully . Thank you for your feedback!"
    except Exception as e:
        return f"Erreur lors de l'enregistrement du flag : {e}"

# Créer l'interface Gradio
def create_interface():
    info = "<div style='font-size: 12px; color: #000000; margin-top: 10px; margin-bottom: 20px; text-align: center;'>Propulsé par le SVM pour une précision exceptionnelle : 90 % de fiabilité pour l'identification des sites d'extraction et 99 % pour l’évaluation de la qualité des phosphates. Explorez les sites de Sidi Chennane et Sidi Daoui, et transformez vos données en insights puissants.</div>"
    custom_css = """
            .gradio-container {
                background: #e6f3e6;
                font-family: Arial, sans-serif;
                border: 2px solid #006633;
                border-radius: 5px;
                padding: 20px;
            }
            .description {
                font-size: 14px;
                color: #000000;
                padding: 10px;
                background-color: #f5f5f5;
                border-left: 3px solid #006633;
                border-radius: 3px;
                margin-bottom: 20px;
            }
            .gr-button {
                background-color: #006633;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            .gr-button:hover {
                background-color: #004d26;
            }
            .gr-input {
                border: 1px solid #006633;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 15px;
            }
            .gr-input label {
                font-weight: bold;
                margin-bottom: 5px;
                display: block;
            }
            .gr-number-input input {
                width: 100%;
            }
        """

    with gr.Blocks(theme=gr.themes.Soft(primary_hue="green"), css=custom_css) as interface:
        gr.HTML("<div style='text-align: center;'><div style='display: flex; align-items: center; justify-content: center; margin-bottom: 10px;'><img src='https://images.seeklogo.com/logo-png/22/2/ocp-logo-png_seeklogo-222172.png' style='height: 100px; margin-right: 20px;'><div><h1 style='font-size: 28px; margin: 0; padding: 0; color: #000000; font-weight: bold;'>Prédiction de la Qualité et du Site d'Extraction des Phosphates</h1><div style='font-size: 18px; color: #006633; font-weight: bold; margin-top: 5px; font-style: italic;'>- OCP Khouribga -</div></div></div></div>")
        gr.HTML(info)

        with gr.Row():
            with gr.Column(scale=1):
                p2o5 = gr.Number(label="Teneur en P2O5 (%)", value=ranges['Teneur en P2O5 (%)'][0], minimum=ranges['Teneur en P2O5 (%)'][0], maximum=ranges['Teneur en P2O5 (%)'][1])
                cao = gr.Number(label="Teneur en CaO (%)", value=ranges['Teneur en CaO (%)'][0], minimum=ranges['Teneur en CaO (%)'][0], maximum=ranges['Teneur en CaO (%)'][1])
                sio2 = gr.Number(label="Teneur en SiO2 (%)", value=ranges['Teneur en SiO2 (%)'][0], minimum=ranges['Teneur en SiO2 (%)'][0], maximum=ranges['Teneur en SiO2 (%)'][1])
                humidite = gr.Number(label="Humidité (%)", value=ranges['Humidité (%)'][0], minimum=ranges['Humidité (%)'][0], maximum=ranges['Humidité (%)'][1])
                granulometrie = gr.Number(label="Granulométrie (mm)", value=ranges['Granulométrie (mm)'][0], minimum=ranges['Granulométrie (mm)'][0], maximum=ranges['Granulométrie (mm)'][1])

                with gr.Row():
                    clear_btn = gr.Button("Clear")
                    submit_btn = gr.Button("Submit", variant="primary")

                gr.Examples(
                    examples=[
                        [25.63, 39.0, 0.6, 3.03, 0.93],
                        [31.24, 32.6, 3.07, 14.22, 0.42],
                        [26.58, 32.86, 0.6, 14.35, 0.84]
                    ],
                    inputs=[p2o5, cao, sio2, humidite, granulometrie]
                )

            with gr.Column(scale=1):
                output = gr.Textbox(label="output", lines=3)
                flag_reason = gr.Dropdown(
                    choices=["Résultat incorrect", "Valeurs d'entrée invalides", "Autre"],
                    value="Résultat incorrect",
                    label="Raison du flag"
                )
                flag_btn = gr.Button("Flag")
                flag_status = gr.Markdown(value="")

        submit_btn.click(
            fn=predict,
            inputs=[p2o5, cao, sio2, humidite, granulometrie],
            outputs=output
        )

        clear_btn.click(
            fn=lambda: [
                ranges['Teneur en P2O5 (%)'][0],
                ranges['Teneur en CaO (%)'][0],
                ranges['Teneur en SiO2 (%)'][0],
                ranges['Humidité (%)'][0],
                ranges['Granulométrie (mm)'][0],
                "",
                ""
            ],
            inputs=None,
            outputs=[p2o5, cao, sio2, humidite, granulometrie, output, flag_status]
        )

        flag_btn.click(
            fn=save_flag,
            inputs=[p2o5, cao, sio2, humidite, granulometrie, output, flag_reason],
            outputs=flag_status
        )

    return interface
    
# Lancer l'interface directement
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()