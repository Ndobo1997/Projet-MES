import streamlit as st

def set_background(image_url, opacity=0.5, color="#000000"):
    """Définit l'image de fond de l'application."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
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

def display_author(image_url, name, email):
    """Affiche les informations d'un auteur (photo, nom, email)."""
    st.markdown(
        f"""
        <div style="border: 2px solid #ddd; padding: 10px; margin: 10px; border-radius: 5px; text-align: center; background-color: rgba(255, 255, 255, 0.7);">
            <img src="{image_url}" style="max-width: 200px; display: block; margin-left: auto; margin-right: auto;" alt="{name}">
            <h4 style="color: black; margin-top: 5px; margin-bottom: 0;">{name}</h4>
            <p style="color: black; font-size: 14px; margin-top: 0;">{email}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")  # Flocon de neige

    # Chemins d'accès aux images en ligne
    background_url = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_congo.jpg"
    ma_photo_url = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/Ma_photo.jpg"
    pierre_photo_url = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/Image_Nathan.jpg"

    # Définir l'image de fond
    set_background(background_url, opacity=0.3, color="#000000")

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
    st.markdown('<h2 class="fade-in-out">Salut cher utilisateur !!!!!!!!!!!!!!!</h2>', unsafe_allow_html=True)
    st.title("Cette page présente les auteurs de cette application et vous pouvez les contacter via leurs adresses mails.")

    # Affichage des auteurs
    col1, col2 = st.columns(2)

    with col1:
        display_author(ma_photo_url, "PIERRE NDOBO ONGUENE", "pierrendoboonguene@gmail.com")  # Remplacez ici
    with col2:
        display_author(pierre_photo_url, "NSIMOUESSA DIEUVEIL NATHAN", "nsimouessa@gmail.com")  # Remplacez ici

if __name__ == "__main__":
    main()
