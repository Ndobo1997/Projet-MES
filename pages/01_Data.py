import streamlit as st
import os
import base64
import pandas as pd
import numpy as np

def set_background(image_path, opacity=0.5, color="#000000"):
    with open(image_path, "rb") as f:
        image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{image_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: {color};
            opacity: {opacity};
            z-index: -1;
        }}
        .stApp h1, .stApp h2 {{
            color: white !important;
        }}
        .animated-title {{
            font-size: 2.5em;
            font-weight: bold;
            animation: text-animation 10s linear infinite;
            text-shadow: 2px 2px 4px #000000;
        }}
        @keyframes text-animation {{
            0% {{ transform: translateX(-100%); opacity: 0; }}
            10% {{ transform: translateX(0%); opacity: 1;}}
            90% {{transform: translateX(0%); opacity: 1;}}
            100% {{ transform: translateX(100%); opacity: 0; }}
        }}
        .fade-in-out {{
            animation: fade 3s ease-in-out infinite alternate;
            color: #ADD8E6;
        }}
        @keyframes fade {{
            0% {{ opacity: 0.2; color: #ADD8E6;}}
            50% {{ opacity: 1; color: #87CEEB; }}
            100% {{ opacity: 0.2; color: #ADD8E6; }}
        }}
        .fixed-text {{
            color: #006400; /* Vert foncé */
            font-size: 1.5em; /* Taille de police */
            font-weight: normal; /* Poids de police normal */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")
    background_path = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_BDD.jpg"
    set_background(background_path, opacity=0.3, color="#000000")

    st.markdown("""<h1 class="animated-title">Base de donnés RDC</h1>""", unsafe_allow_html=True)
    st.markdown("""<h1 class="animated-title">Période étude : 1999 - 2023 </h1>""", unsafe_allow_html=True)
    st.markdown('<h2 class="fade-in-out">Soit une serie de 24 ans. </h2>', unsafe_allow_html=True)
    st.title("Les données présentées sur cette page résultent d'une collecte d'informations à partir de differents rapports de la banque centrale du congo (BCC).")
    
if __name__ == '__main__':
    main()


def main():
    st.header("Présentation de la Base")
    file_path = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/refs/heads/main/base%20de%20donnees%20RDC.xlsx"

    #try:
    df = pd.read_excel(file_path, engine='openpyxl')

        # Fonction pour formater l'affichage des nombres
    def format_number(value):
            if isinstance(value, (int, float)):
                return f"{value:.2f}"
            return value

        # Application du formatage à l'ensemble du DataFrame
    styled_df = df.style.format(formatter=format_number)

        # Affichage du DataFrame stylisé
    st.dataframe(styled_df)

        

if __name__ == '__main__':
    main()
