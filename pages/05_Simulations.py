import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64

# CSS pour ajouter une image de fond 
page_bg_img = ''' 
<style> 
.stApp { 
    background-image: url("https://html.scribdassets.com/9nmtrjs70g7tm80y/images/1-0e9a41e842.jpg"); 
    background-size: cover; 
    } 
    </style> 
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)

import streamlit as st

st.info("Bienvenue dans l'application de Simulation ARDL ! \n\n"
        "Pour utiliser cette application, suivez les étapes suivantes :\n"
        "1. Entrez les valeurs initiales pour chaque variable dans les champs prévus à cet effet. Attention les valeurs à renseigner doivent etre en valeur:Exemple PIBR = 2000000. \n"
        "2. Cliquez sur le bouton 'Lancer la Simulation'.\n"
        "3. Les résultats de la simulation s'afficheront sous forme de tableau et de graphiques.\n"
        "4. Vous pouvez télécharger un rapport PDF en cliquant sur le lien de téléchargement en bas de la page.")

# Ou avec un style différent :
st.success("C'est partit pour une simmulation avec succès ! Les résultats s'affichent ci-dessous.")
st.warning("Mais attention !!!!!! : certaines valeurs d'entrée pourraient donner des résultats non interprétables car les prévisions avec les modèles ARDL doivent se faire une courte période.")


def safe_log(value, default=1.0):
    """Calcule le logarithme d'une valeur en gérant les erreurs."""
    try:
        if value > 0:
            return log(value)
        else:
            st.warning(f"La valeur entrée ({value}) n'est pas positive. Le logarithme ne peut pas être calculé. Une valeur par défaut de {default} sera utilisée.")
            return log(default)
    except ValueError:
        st.warning(f"Une erreur mathématique est survenue. La valeur entrée ({value}) pourrait être trop petite. Utiliser une valeur positive pour le calcul du logarithme.")
        return log(default)
    
# Définir les coefficients estimés pour les trois équations
coefficients_eq1 = {
    'LOG_PIBR(-1)': 0.871930,
    'LOG_MMO': -0.003737,
    'LOG_MMO(-1)': 0.007930,
    'TINFLAT': 0.000142,
    'TINDIRECT': -0.000716,
    'LOG_DEP': 0.041792,
    'LOG_TCHANGE': -0.023284,
    'C': 1.574531
}

coefficients_eq2 = {
    'TINFLAT(-1)': 0.025367,
    'LOG_MMO': 8.652144,
    'LOG_MMO(-1)': -17.32212,
    'TINDIRECT': -0.242194,
    'LOG_TCHANGE': 85.79578,
    'LOG_TCHANGE(-1)': -78.71177,
    'LOG_DEP': 10.01347,
    'C': -67.96063
}

coefficients_eq3 = {
    'LOG_DEP(-1)': 0.134440,
    'LOG_PIBR': 1.143247,
    'LOG_DETTE': 0.058670,
    'LOG_DETTE(-1)': 0.116507,
    'LOG_TOC': 0.434239,
    'C': -9.243426
}

import streamlit as st
from math import log

# Validation et normalisation des variables
def validate_and_normalize_tinflat(tinflat):
    if tinflat > 100 or tinflat < -50:
        raise ValueError("La valeur de l'inflation doit être réaliste (entre -50% et 100%).")
    # Normalisation : convertir le pourcentage en décimale si nécessaire
    if tinflat > 1 or tinflat < -1:
        tinflat = tinflat / 100.0
    return tinflat

# Fonctions pour simuler les valeurs
def simulate_log_pibr(log_pibr_lag1, log_mmo, log_mmo_lag1, tinflat, tindirect, log_dep, log_tchange, periods=10):
    log_pibr_values = []
    for _ in range(periods):
        log_pibr = (coefficients_eq1['LOG_PIBR(-1)'] * log_pibr_lag1 +
                    coefficients_eq1['LOG_MMO'] * log_mmo +
                    coefficients_eq1['LOG_MMO(-1)'] * log_mmo_lag1 +
                    coefficients_eq1['TINFLAT'] * tinflat +
                    coefficients_eq1['TINDIRECT'] * tindirect +
                    coefficients_eq1['LOG_DEP'] * log_dep +
                    coefficients_eq1['LOG_TCHANGE'] * log_tchange +
                    coefficients_eq1['C'])
        log_pibr_values.append(log_pibr)
        log_pibr_lag1 = log_pibr
        log_mmo_lag1 = log_mmo
    return log_pibr_values, pd.DataFrame({'LOG_PIBR': log_pibr_values, 'Period': range(1, periods + 1)})

def simulate_tinflat(tinflat_lag1, log_mmo, log_mmo_lag1, tindirect, log_tchange, log_tchange_lag1, log_dep_values, periods=10):
    tinflat_values = []
    for i in range(periods):
        log_dep = log_dep_values[i]
        tinflat = (coefficients_eq2['TINFLAT(-1)'] * tinflat_lag1 +
                   coefficients_eq2['LOG_MMO'] * log_mmo +
                   coefficients_eq2['LOG_MMO(-1)'] * log_mmo_lag1 +
                   coefficients_eq2['TINDIRECT'] * tindirect +
                   coefficients_eq2['LOG_TCHANGE'] * log_tchange +
                   coefficients_eq2['LOG_TCHANGE(-1)'] * log_tchange_lag1 +
                   coefficients_eq2['LOG_DEP'] * log_dep +
                   coefficients_eq2['C'])
        tinflat_values.append(tinflat)
        tinflat_lag1 = tinflat
        log_mmo_lag1 = log_mmo
        log_tchange_lag1 = log_tchange
    return pd.DataFrame({'TINFLAT': tinflat_values, 'Period': range(1, periods + 1)})

def simulate_log_dep(log_dep_lag1, log_pibr_values, log_dette, log_dette_lag1, log_toc, periods=10):
    log_dep_values = []
    for j in range(periods):
        log_pibr = log_pibr_values[j]
        log_dep = (coefficients_eq3['LOG_DEP(-1)'] * log_dep_lag1 +
                   coefficients_eq3['LOG_PIBR'] * log_pibr +
                   coefficients_eq3['LOG_DETTE'] * log_dette +
                   coefficients_eq3['LOG_DETTE(-1)'] * log_dette_lag1 +
                   coefficients_eq3['LOG_TOC'] * log_toc +
                   coefficients_eq3['C'])
        log_dep_values.append(log_dep)
        log_dep_lag1 = log_dep
        log_dette_lag1 = log_dette
    return log_dep_values, pd.DataFrame({'LOG_DEP': log_dep_values, 'Period': range(1, periods + 1)})

# Génération des commentaires automatiques basés sur l'allure du graphique
def generate_comment(data, column):
    if data[column].iloc[-1] > data[column].iloc[0]:
        return f"Le graphique montre que la variable {column} va continuer d'augmenter sur les {periods} prochaines années."
    elif data[column].iloc[-1] < data[column].iloc[0]:
        return f"Le graphique montre que la variable  {column} va baisser globalement sur les {periods} qui suivent si rien est fait."
    else:
        return f"Le graphique de la variable {column} montre une tendance stable dans le temps."

# Fonction pour créer un PDF
def create_pdf(data, filename="rapport_simulation.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Titre
    pdf.cell(200, 10, txt="Rapport de Simulation ARDL", ln=True, align='C')
    pdf.ln(10)
    
    # Introduction
    pdf.cell(200, 10, txt="Introduction", ln=True)
    pdf.multi_cell(0, 10, txt="Ce rapport présente les résultats des simulations effectuées à l'aide du modèle ARDL. Les simulations ont été réalisées en utilisant les valeurs initiales fournies pour les variables PIBR, TINFLAT et DEP.")
    pdf.ln(5)
    
    # Méthodologie
    pdf.cell(200, 10, txt="Méthodologie", ln=True)
    pdf.multi_cell(0, 10, txt="Les valeurs initiales ont été utilisées pour simuler les comportements des variables PIBR, TINFLAT et DEP sur une période de simulation définie. Les équations ARDL ont été utilisées pour prédire les valeurs futures de ces variables.")
    pdf.ln(5)
    
    # Tableau des résultats
    pdf.cell(200, 10, txt="Résultats de la Simulation", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    
    # Ajout des résultats dans le tableau
    cols = data.columns.to_list()
    rows = data.values.tolist()

    # Entêtes des colonnes
    for col in cols:
        pdf.cell(40, 10, txt=col, border=1)
    pdf.ln(10)
    
    # Données des lignes
    for row in rows:
        for item in row:
            pdf.cell(40, 10, txt=str(item), border=1)
        pdf.ln(10)

    # Conclusion et Commentaires
        pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Conclusion et Commentaires", ln=True)
    pdf.ln(5)
    for col in data.columns:
        if col != 'Period':
            pdf.multi_cell(0, 10, txt=generate_comment(data, col))
            pdf.ln(5)
    
    pdf.output(filename)

    # Conversion en base64 pour téléchargement
    with open(filename, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return base64_pdf

# Interface utilisateur avec Streamlit
st.title('Simulation ARDL')
from math import log
# Entrée des valeurs initiales pour les équations
st.header('Valeurs Initiales pour les Simulations')
log_pibr_lag1 = safe_log(st.number_input("Entrez la valeur du PIBR de l'an dernier", value=0.0, key='log_pibr_lag1'))
log_mmo = safe_log(st.number_input('Quelle est le niveau de la Masse Monetaire ?', value=0.0, key='log_mmo'))
log_mmo_lag1 = safe_log(st.number_input("Quelle était le niveau de la Masse Monetaire l'an dernier ?", value=0.0, key='log_mmo_lag1'))
tinflat = st.number_input("Veillez renseigner le niveau d'inflation actuelle ", value=0.0, key='tinflat')
tindirect = st.number_input("Quelle est le niveau de Taux d'interet Directeur ?", value=0.0, key='tindirect')
log_dep = safe_log(st.number_input('Quel est le niveau de Depenses publiques ?', value=0.0, key='log_dep'))
log_tchange = safe_log(st.number_input('Veillez renseigner le taux de change actuel.', value=0.0, key='log_tchange'))
tinflat_lag1 = st.number_input("Veillez renseigner le niveau d'inflation l'an dernier ", value=0.0, key='tinflat_lag1')
log_tchange_lag1 = safe_log(st.number_input("Veillez renseigner le taux de change l'an dernier ", value=0.0, key='log_tchange_lag1'))
log_dep_lag1 = safe_log(st.number_input("Veillez renseigner le niveau de depenses publiques de l'an dernier ", value=0.0, key='log_dep_lag1'))
log_dette = safe_log(st.number_input('Veillez renseigner le niveau de la dette publique actuelle.', value=0.0, key='log_dette'))
log_dette_lag1 = safe_log(st.number_input("Quel etait le niveau de la dette l'an dernier", value=0.0, key='log_dette_lag1'))
log_toc = safe_log(st.number_input("Veillez renseigner le  Taux d'Ouverture Commerciale ", value=0.0, key='log_toc'))
periods = st.number_input('Nombre de périodes de simulation', value=10, min_value=1, key='periods')

# Bouton pour lancer les simulations
if st.button('Lancer la Simulation'):
    log_pibr_values, results_1 = simulate_log_pibr(log_pibr_lag1, log_mmo, log_mmo_lag1, validate_and_normalize_tinflat(tinflat), tindirect, log_dep, log_tchange, periods)
    log_dep_values, results_3 = simulate_log_dep(log_dep_lag1, log_pibr_values, log_dette, log_dette_lag1, log_toc, periods)
    results_2 = round(simulate_tinflat(tinflat_lag1, log_mmo, log_mmo_lag1, tindirect, log_tchange, log_tchange_lag1, log_dep_values, periods),3)
    
    results = pd.concat([results_1, results_2['TINFLAT'], results_3['LOG_DEP']], axis=1)
    
    st.write('Résultats de la Simulation:')
    st.dataframe(results)
    
    # Création des graphiques interactifs avec plotly
    fig1 = px.line(results, x='Period', y='LOG_PIBR', title='Simulation de LOG_PIBR')
    st.plotly_chart(fig1)
    st.write(generate_comment(results, 'LOG_PIBR'))
    
    fig2 = px.line(results, x='Period', y='TINFLAT', title='Simulation de TINFLAT')
    st.plotly_chart(fig2)
    st.write(generate_comment(results, 'TINFLAT'))
    
    fig3 = px.line(results, x='Period', y='LOG_DEP', title='Simulation de LOG_DEP')
    st.plotly_chart(fig3)
    st.write(generate_comment(results, 'LOG_DEP'))
    
    # Création du rapport PDF
    pdf_content = create_pdf(results)
    href = f'<a href="data:application/pdf;base64,{pdf_content}" download="rapport_simulation.pdf">Télécharger le rapport en PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
