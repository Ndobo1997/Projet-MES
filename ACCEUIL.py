import streamlit as st
import os
import base64

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
    background_path = "C://Users//djetek_user//Desktop//ISE 3//Pierre et Nathan projet//image_congo.jpg"
    set_background(background_path, opacity=0.3, color="#000000")

    st.markdown("""<h1 class="animated-title">BIENVENUE DANS CET ESPACE D'ANALYSE DE LA SITUATION MACROÉCONOMIQUE DE LA RDC</h1>""", unsafe_allow_html=True)
    st.markdown('<h2 class="fade-in-out">Bonne navigation</h2>', unsafe_allow_html=True)
    st.title("Cette page, fruit du groupe constitué de PIERRE et NATHAN, vous donne une vue sur la base de données utilisée pour faire des analyses, la description des différentes chroniques retenues, la modélisation ARDL et les simulations.")
    st.title("Pour voir le contenu d'une section, il vous suffit de cliquer sur le nom correspondant pour y accéder. Et pour faire des simulations, vous allez vous-même entrer vos propres données selon le guide que vous trouverez sur la page en question.")
    

if __name__ == '__main__':
    main()