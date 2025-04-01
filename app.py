import streamlit as st
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import io
import base64

# Configuration de la page
st.set_page_config(page_title="Formulaire de Location", layout="wide")

# Titre principal
st.title("Formulaire de Location")

# Création des onglets
tab1, tab2, tab3 = st.tabs(["Conseiller", "Locataires", "Garants"])

# Onglet Conseiller
with tab1:
    st.header("Informations Conseiller")
    
    # Informations conseiller
    col1, col2 = st.columns(2)
    with col1:
        nom_conseiller = st.text_input("Nom complet")
    with col2:
        tel_conseiller = st.text_input("Téléphone")
    
    # Ajout du champ email conseiller
    email_conseiller = st.text_input("Email conseiller")
    
    # Désignation du bien
    st.subheader("Désignation et situation du bien proposé à la location")
    adresse = st.text_input("Adresse du bien")
    col1, col2 = st.columns(2)
    with col1:
        code_postal = st.text_input("Code postal")
    with col2:
        ville = st.text_input("Ville")
    
    # Conditions financières
    st.subheader("Conditions financières")
    col1, col2 = st.columns(2)
    with col1:
        loyer = st.number_input("Loyer mensuel", min_value=0.0, step=50.0)
        depot = st.number_input("Dépôt de garantie", min_value=0.0, step=50.0)
    with col2:
        charges = st.number_input("Charges mensuelles", min_value=0.0, step=10.0)
        honoraires = st.number_input("Honoraires", min_value=0.0, step=50.0)
    
    date_entree = st.date_input("Date d'entrée souhaitée")
    
    st.info("Attention, le présent document n'est pas une réservation.")

# Onglet Locataires
with tab2:
    st.header("Dossier Locataires")
    
    # Nombre de locataires
    nb_locataires = st.radio("Nombre de candidats", [1, 2], horizontal=True)
    
    # Création d'un formulaire par locataire
    for i in range(int(nb_locataires)):
        st.subheader(f"Candidat {i+1}")
        
        # Situation familiale
        st.subheader("Situation familiale")
        situation = st.selectbox(
            "Vous êtes",
            ["Célibataire", "Marié(e)", "En instance de divorce", "Pacsé(e)", "Divorcé(e)"],
            key=f"situation_{i}"
        )
        
        # Domicile actuel
        st.subheader("Domicile actuel")
        domicile = st.selectbox(
            "Actuellement vous êtes",
            ["Propriétaire", "Locataire", "Hébergé"],
            key=f"domicile_{i}"
        )
        
        # Civilité
        st.subheader("Civilité")
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom", key=f"nom_{i}")
            nom_jeune_fille = st.text_input("Nom de jeune fille", key=f"nom_jf_{i}")
            prenom = st.text_input("Prénom", key=f"prenom_{i}")
            date_naissance = st.date_input("Né(e) le", key=f"date_naissance_{i}")
        with col2:
            ville_naissance = st.text_input("Ville de naissance", key=f"ville_naissance_{i}")
            departement = st.text_input("Département", key=f"departement_{i}")
            pays = st.text_input("Pays", key=f"pays_{i}")
            nationalite = st.text_input("Nationalité", key=f"nationalite_{i}")
        
        # Coordonnées
        st.subheader("Coordonnées")
        adresse_actuelle = st.text_input("Adresse actuelle", key=f"adresse_{i}")
        col1, col2 = st.columns(2)
        with col1:
            cp_actuel = st.text_input("Code postal", key=f"cp_{i}")
            telephone = st.text_input("Téléphone", key=f"tel_{i}")
        with col2:
            ville_actuelle = st.text_input("Ville", key=f"ville_{i}")
            email = st.text_input("Email", key=f"email_{i}")
        
        # Enfants
        col1, col2 = st.columns(2)
        with col1:
            nb_enfants = st.number_input("Nombre d'enfants au foyer", min_value=0, key=f"nb_enfants_{i}")
        with col2:
            if nb_enfants > 0:
                age_enfants = st.text_input("Age des enfants", key=f"age_enfants_{i}", 
                                          help="Séparez les âges par des virgules")

        # Situation professionnelle
        st.subheader("Situation professionnelle")
        col1, col2 = st.columns(2)
        with col1:
            profession = st.text_input("Profession", key=f"profession_{i}")
            anciennete = st.text_input("Ancienneté", key=f"anciennete_{i}")
        with col2:
            employeur = st.text_input("Employeur", key=f"employeur_{i}")
            tel_employeur = st.text_input("Téléphone de l'employeur", key=f"tel_employeur_{i}")
        
        adresse_entreprise = st.text_input("Adresse entreprise", key=f"adresse_entreprise_{i}")
        col1, col2 = st.columns(2)
        with col1:
            cp_entreprise = st.text_input("Code postal entreprise", key=f"cp_entreprise_{i}")
        with col2:
            ville_entreprise = st.text_input("Ville entreprise", key=f"ville_entreprise_{i}")

        # Ressources
        st.subheader("Ressources")
        col1, col2 = st.columns(2)
        with col1:
            revenus = st.number_input("Revenus mensuels", min_value=0.0, key=f"revenus_{i}")
            autres_revenus = st.number_input("Autres revenus justifiés", min_value=0.0, key=f"autres_revenus_{i}")
        with col2:
            total_revenus = revenus + autres_revenus
            st.write("Total des revenus :", total_revenus, "€")

    # Zone signature(s) après tous les formulaires
    st.subheader("Signature(s)")
    st.write("Je (nous) soussigné(e)(s) certifie(ons) que les renseignements ci-dessus sont sincères et véritables.")
    st.write(f"Fait à Limoges, le {st.date_input('Date de signature', key='date_sig_loc')}")

    # Afficher une ou deux zones de signature selon le nombre de locataires
    for i in range(int(nb_locataires)):
        st.write(f"Signature candidat {i+1} :")
        signature_locataire = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=2,
            stroke_color="#000000",
            background_color="#ffffff",
            width=600,
            height=150,
            drawing_mode="freedraw",
            key=f"signature_canvas_loc_{i}",
        )

# Onglet Garants
with tab3:
    st.header("Dossier Garants")
    
    # Nombre de garants
    nb_garants = st.radio("Nombre de garants", [1, 2], horizontal=True)
    
    # Création d'un formulaire par garant
    for i in range(int(nb_garants)):
        st.subheader(f"Garant {i+1}")
        
        # Situation familiale
        st.subheader("Situation familiale")
        situation_garant = st.selectbox(
            "Vous êtes",
            ["Célibataire", "Marié(e)", "En instance de divorce", "Pacsé(e)", "Divorcé(e)"],
            key=f"situation_garant_{i}"
        )
        
        # Domicile actuel
        st.subheader("Domicile actuel")
        domicile_garant = st.selectbox(
            "Actuellement vous êtes",
            ["Propriétaire", "Locataire", "Hébergé"],
            key=f"domicile_garant_{i}"
        )
        
        # Civilité
        st.subheader("Civilité")
        col1, col2 = st.columns(2)
        with col1:
            nom_garant = st.text_input("Nom", key=f"nom_garant_{i}")
            nom_jf_garant = st.text_input("Nom de jeune fille", key=f"nom_jf_garant_{i}")
            prenom_garant = st.text_input("Prénom", key=f"prenom_garant_{i}")
            date_naissance_garant = st.date_input("Né(e) le", key=f"date_naissance_garant_{i}")
        with col2:
            ville_naissance_garant = st.text_input("Ville de naissance", key=f"ville_naissance_garant_{i}")
            departement_garant = st.text_input("Département", key=f"departement_garant_{i}")
            pays_garant = st.text_input("Pays", key=f"pays_garant_{i}")
            nationalite_garant = st.text_input("Nationalité", key=f"nationalite_garant_{i}")

        # Coordonnées garant
        st.subheader("Coordonnées")
        adresse_actuelle_garant = st.text_input("Adresse actuelle", key=f"adresse_garant_{i}")
        col1, col2 = st.columns(2)
        with col1:
            cp_actuel_garant = st.text_input("Code postal", key=f"cp_garant_{i}")
            telephone_garant = st.text_input("Téléphone", key=f"tel_garant_{i}")
        with col2:
            ville_actuelle_garant = st.text_input("Ville", key=f"ville_garant_{i}")
            email_garant = st.text_input("Email", key=f"email_garant_{i}")
        
        # Enfants garant
        col1, col2 = st.columns(2)
        with col1:
            nb_enfants_garant = st.number_input("Nombre d'enfants au foyer", min_value=0, key=f"nb_enfants_garant_{i}")
        with col2:
            if nb_enfants_garant > 0:
                age_enfants_garant = st.text_input("Age des enfants", key=f"age_enfants_garant_{i}", 
                                                 help="Séparez les âges par des virgules")

        # Situation professionnelle garant
        st.subheader("Situation professionnelle")
        col1, col2 = st.columns(2)
        with col1:
            profession_garant = st.text_input("Profession", key=f"profession_garant_{i}")
            anciennete_garant = st.text_input("Ancienneté", key=f"anciennete_garant_{i}")
        with col2:
            employeur_garant = st.text_input("Employeur", key=f"employeur_garant_{i}")
            tel_employeur_garant = st.text_input("Téléphone de l'employeur", key=f"tel_employeur_garant_{i}")
        
        adresse_entreprise_garant = st.text_input("Adresse entreprise", key=f"adresse_entreprise_garant_{i}")
        col1, col2 = st.columns(2)
        with col1:
            cp_entreprise_garant = st.text_input("Code postal entreprise", key=f"cp_entreprise_garant_{i}")
        with col2:
            ville_entreprise_garant = st.text_input("Ville entreprise", key=f"ville_entreprise_garant_{i}")

        # Ressources garant
        st.subheader("Ressources")
        col1, col2 = st.columns(2)
        with col1:
            revenus_garant = st.number_input("Revenus mensuels", min_value=0.0, key=f"revenus_garant_{i}")
            autres_revenus_garant = st.number_input("Autres revenus justifiés", min_value=0.0, key=f"autres_revenus_garant_{i}")
        with col2:
            total_revenus_garant = revenus_garant + autres_revenus_garant
            st.write("Total des revenus :", total_revenus_garant, "€")

    # Zone signature(s) après tous les formulaires garants
    st.subheader("Signature(s)")
    st.write("Je (nous) soussigné(e)(s) certifie(ons) que les renseignements ci-dessus sont sincères et véritables.")
    st.write(f"Fait à Limoges, le {st.date_input('Date de signature', key='date_sig_garant')}")

    # Afficher une ou deux zones de signature selon le nombre de garants
    for i in range(int(nb_garants)):
        st.write(f"Signature garant {i+1} :")
        signature_garant = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=2,
            stroke_color="#000000",
            background_color="#ffffff",
            width=600,
            height=150,
            drawing_mode="freedraw",
            key=f"signature_canvas_garant_{i}",
        )

# Mentions légales en bas de page
st.markdown("---")
st.markdown("""
Les informations recueillies font l'objet d'un traitement informatique nécessaire à l'exécution des missions de l'agent immobilier.
Conformément à la loi informatique et libertés du 6 janvier 1978 modifiée, les candidats bénéficient d'un droit d'accès,
de rectification et de suppression des informations qui les concernent. Pour exercer ce droit, les parties peuvent s'adresser à l'Agence.
""")

st.warning("Important : tout dossier incomplet ne peut être soumis à l'étude pour validation.")

# Fonction pour générer le PDF
def generer_pdf():
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    # Créer un objet BytesIO pour stocker le PDF
    buffer = io.BytesIO()
    
    # Créer le PDF avec ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    
    # Titre
    c.drawString(100, 750, "Formulaire de Location")
    
    # Informations conseiller
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 700, "Informations Conseiller")
    c.setFont("Helvetica", 12)
    c.drawString(50, 680, f"Nom complet: {nom_conseiller}")
    c.drawString(50, 660, f"Telephone: {tel_conseiller}")
    c.drawString(50, 640, f"Email: {email_conseiller}")
    
    # Bien immobilier
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 600, "Designation et situation du bien")
    c.setFont("Helvetica", 12)
    c.drawString(50, 580, f"Adresse: {adresse}")
    c.drawString(50, 560, f"Code postal: {code_postal}")
    c.drawString(50, 540, f"Ville: {ville}")
    
    # Conditions financières
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 500, "Conditions financieres")
    c.setFont("Helvetica", 12)
    c.drawString(50, 480, f"Loyer mensuel: {loyer} EUR")
    c.drawString(50, 460, f"Charges mensuelles: {charges} EUR")
    c.drawString(50, 440, f"Depot de garantie: {depot} EUR")
    c.drawString(50, 420, f"Honoraires: {honoraires} EUR")
    c.drawString(50, 400, f"Date d'entree souhaitee: {date_entree}")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()
