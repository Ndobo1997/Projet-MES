import streamlit as st
import os
import base64

def set_background(image_path, opacity=0.5, color="#000000"):
    """Définit l'image de fond de l'application."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{encoded_string});
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
            .caption {{
                color: white; /* Couleur blanche */
                font-weight: bold; /* Gras */
                font-size: 1.2em; /* Taille de police agrandie */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"Erreur : Image de fond non trouvée à : {image_path}")
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image de fond : {e}")

def display_author(image_path, name, email):
    """Affiche les informations d'un auteur (photo, nom, email)."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style="border: 2px solid #ddd; padding: 10px; margin: 10px; border-radius: 5px; text-align: center; background-color: rgba(255, 255, 255, 0.7);">
                <img src="data:image/jpeg;base64,{encoded_string}" style="max-width: 200px; display: block; margin-left: auto; margin-right: auto;" alt="{name}">
                <h4 style="color: black; margin-top: 5px; margin-bottom: 0;">{name}</h4>
                <p style="color: black; font-size: 14px; margin-top: 0;">{email}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.error(f"Erreur : Image d'auteur non trouvée à : {image_path}")
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image d'auteur : {e}")

def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")  # Flocon de neige

    # Chemins d'accès aux images
    background_path = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_congo.jpg"
    ma_photo_path = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/Ma_photo.jpg"
    pierre_photo_path = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/Image_Nathan.jpg"

    # Vérification de l'existence des fichiers AVANT de les utiliser
    if not os.path.exists(background_path):
        st.error(f"Erreur : Le fichier de fond n'existe pas à : {background_path}")
        return

    if not os.path.exists(ma_photo_path):
        st.error(f"Erreur : Le fichier Ma_photo.jpg n'existe pas à : {ma_photo_path}")
        return

    if not os.path.exists(pierre_photo_path):
        st.error(f"Erreur : Le fichier Pierre.jpg n'existe pas à : {pierre_photo_path}")
        return

    # Définir l'image de fond
    set_background(background_path, opacity=0.3, color="#000000")

    # Ajout des images dans l'en-tête
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://img.freepik.com/photos-gratuite/drapeau-republique-democratique-du-congo_1401-92.jpg?t=st=1735662475~exp=1735666075~hmac=970eb118a64c6d542d277cd10412aca4deaf441ce824f12ee0c974bd4b60c33a&w=826", use_container_width=True)
        st.markdown('<p class="caption">Drapeau RDC</p>', unsafe_allow_html=True)

    with col2:
        st.image("https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_bcc.jpg", use_container_width=True)
        st.markdown('<p class="caption">BCC</p>', unsafe_allow_html=True)

    with col3:
        st.image("https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/Logo_ISSEA.jpeg", use_container_width=True)
        st.markdown('<p class="caption">ISSEA</p>', unsafe_allow_html=True)

    st.markdown("""<h1 class="animated-title">BIENVENU DANS CETTE PRESENTATION</h1>""", unsafe_allow_html=True)
    st.markdown('<h2 class="fade-in-out">Salut chere utilisateur !!!!!!!!!!!!!!!</h2>', unsafe_allow_html=True)
    st.title("cette page presente les auteurs de cette application et vous pouvez les contacter via leurs adresses mails")
    # Affichage des auteurs
    col1, col2 = st.columns(2)

    with col1:
        display_author(ma_photo_path, "PIERRE NDOBO ONGUENE", "pierrendoboonguene@gmail.com")  # Remplacez ici
    with col2:
        display_author(pierre_photo_path, "NSIMOUESSA DIEUVEIL NATHAN", "nsimouessa@gmail.com")  # Remplacez ici

if __name__ == "__main__":
    main()
