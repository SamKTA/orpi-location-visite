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
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch, mm
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    
    # Créer un objet BytesIO pour stocker le PDF
    buffer = io.BytesIO()
    
    # Créer le document avec SimpleDocTemplate pour une meilleure mise en page
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                          rightMargin=20*mm, leftMargin=20*mm,
                          topMargin=30*mm, bottomMargin=20*mm)
    
    # Définir les styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Title',
                            fontName='Helvetica-Bold',
                            fontSize=18,
                            alignment=1,  # 0=left, 1=center, 2=right
                            spaceAfter=10*mm))
    
    styles.add(ParagraphStyle(name='Heading1',
                            fontName='Helvetica-Bold',
                            fontSize=16,
                            leading=20,
                            spaceBefore=5*mm,
                            spaceAfter=5*mm))
    
    styles.add(ParagraphStyle(name='Heading2',
                            fontName='Helvetica-Bold',
                            fontSize=14,
                            leading=18,
                            spaceBefore=3*mm,
                            spaceAfter=3*mm))
    
    styles.add(ParagraphStyle(name='Normal',
                            fontName='Helvetica',
                            fontSize=11,
                            leading=16,
                            spaceBefore=1*mm,
                            spaceAfter=1*mm))
    
    # Couleur Orpi pour les titres
    orpi_red = colors.HexColor('#ec1f26')
    
    # Liste des éléments à ajouter au PDF
    elements = []
    
    # Fonction pour ajouter un en-tête Orpi à chaque page
    def add_orpi_header(canvas, doc):
        canvas.saveState()
        width, height = A4
        
        # Ajouter le texte "Orpi ImmoConseil" en rouge
        canvas.setFont('Helvetica-Bold', 16)
        canvas.setFillColor(orpi_red)
        canvas.drawString(20*mm, height - 15*mm, "Orpi ImmoConseil")
        
        # Ajouter une ligne rouge en dessous
        canvas.setStrokeColor(orpi_red)
        canvas.setLineWidth(1)
        canvas.line(20*mm, height - 18*mm, width - 20*mm, height - 18*mm)
        
        # Ajouter le numéro de page
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.black)
        canvas.drawString(width - 30*mm, 15*mm, f"Page {doc.page}")
        
        canvas.restoreState()
    
    # Titre principal
    elements.append(Paragraph("Formulaire de Location", styles['Title']))
    elements.append(Spacer(1, 10*mm))
    
    # --- PARTIE CONSEILLER ---
    elements.append(Paragraph("INFORMATIONS CONSEILLER", styles['Heading1']))
    
    # Tableau pour les informations du conseiller
    data = [
        ["Nom complet:", nom_conseiller],
        ["Téléphone:", tel_conseiller],
        ["Email:", email_conseiller]
    ]
    
    t = Table(data, colWidths=[100, 350])
    t.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 5*mm))
    
    # Désignation du bien
    elements.append(Paragraph("Désignation et situation du bien", styles['Heading2']))
    
    data = [
        ["Adresse:", adresse],
        ["Code postal:", code_postal],
        ["Ville:", ville]
    ]
    
    t = Table(data, colWidths=[100, 350])
    t.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 5*mm))
    
    # Conditions financières
    elements.append(Paragraph("Conditions financières", styles['Heading2']))
    
    data = [
        ["Loyer mensuel:", f"{loyer} €"],
        ["Charges mensuelles:", f"{charges} €"],
        ["Dépôt de garantie:", f"{depot} €"],
        ["Honoraires:", f"{honoraires} €"],
        ["Date d'entrée souhaitée:", str(date_entree)]
    ]
    
    t = Table(data, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
    ]))
    
    elements.append(t)
    
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph("Attention, le présent document n'est pas une réservation.", 
                             ParagraphStyle(name='Warning', parent=styles['Normal'], 
                                           textColor=orpi_red, fontName='Helvetica-Bold')))
    
    # Saut de page avant la partie locataires
    elements.append(Paragraph("<br/><br/><br/>", styles['Normal']))
    
    # --- PARTIE LOCATAIRES ---
    elements.append(Paragraph("DOSSIER LOCATAIRES", styles['Heading1']))
    elements.append(Paragraph(f"Nombre de candidats: {nb_locataires}", styles['Normal']))
    elements.append(Spacer(1, 5*mm))
    
    # Pour chaque locataire
    for i in range(int(nb_locataires)):
        elements.append(Paragraph(f"CANDIDAT {i+1}", styles['Heading2']))
        elements.append(Spacer(1, 3*mm))
        
        # Situation familiale
        elements.append(Paragraph("Situation familiale", ParagraphStyle(name='SubHeading', 
                                                                     parent=styles['Heading2'], 
                                                                     textColor=orpi_red)))
        
        situation = st.session_state.get(f"situation_{i}", "")
        data = [["État civil:", situation]]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 3*mm))
        
        # Domicile actuel
        elements.append(Paragraph("Domicile actuel", ParagraphStyle(name='SubHeading', 
                                                                 parent=styles['Heading2'], 
                                                                 textColor=orpi_red)))
        
        domicile = st.session_state.get(f"domicile_{i}", "")
        data = [["Situation actuelle:", domicile]]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 3*mm))
        
        # Civilité
        elements.append(Paragraph("Civilité", ParagraphStyle(name='SubHeading', 
                                                         parent=styles['Heading2'], 
                                                         textColor=orpi_red)))
        
        nom = st.session_state.get(f"nom_{i}", "")
        prenom = st.session_state.get(f"prenom_{i}", "")
        nom_jeune_fille = st.session_state.get(f"nom_jf_{i}", "")
        date_naissance = st.session_state.get(f"date_naissance_{i}", "")
        ville_naissance = st.session_state.get(f"ville_naissance_{i}", "")
        departement = st.session_state.get(f"departement_{i}", "")
        pays = st.session_state.get(f"pays_{i}", "")
        nationalite = st.session_state.get(f"nationalite_{i}", "")
        
        data = [
            ["Nom:", nom],
            ["Prénom:", prenom],
            ["Nom de jeune fille:", nom_jeune_fille],
            ["Né(e) le:", str(date_naissance)],
            ["Ville de naissance:", ville_naissance],
            ["Département:", departement],
            ["Pays:", pays],
            ["Nationalité:", nationalite]
        ]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 3*mm))
        
        # Coordonnées
        elements.append(Paragraph("Coordonnées", ParagraphStyle(name='SubHeading', 
                                                            parent=styles['Heading2'], 
                                                            textColor=orpi_red)))
        
        adresse_actuelle = st.session_state.get(f"adresse_{i}", "")
        cp_actuel = st.session_state.get(f"cp_{i}", "")
        ville_actuelle = st.session_state.get(f"ville_{i}", "")
        telephone = st.session_state.get(f"tel_{i}", "")
        email = st.session_state.get(f"email_{i}", "")
        
        data = [
            ["Adresse actuelle:", adresse_actuelle],
            ["Code postal:", cp_actuel],
            ["Ville:", ville_actuelle],
            ["Téléphone:", telephone],
            ["Email:", email]
        ]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 3*mm))
        
        # Enfants
        nb_enfants = st.session_state.get(f"nb_enfants_{i}", 0)
        age_enfants = st.session_state.get(f"age_enfants_{i}", "") if nb_enfants > 0 else ""
        
        data = [
            ["Nombre d'enfants au foyer:", str(nb_enfants)],
            ["Age des enfants:", age_enfants] if nb_enfants > 0 else ["", ""]
        ]
        
        if nb_enfants > 0:
            t = Table(data, colWidths=[150, 300])
            t.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
            ]))
            elements.append(t)
        else:
            t = Table([data[0]], colWidths=[150, 300])
            t.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
            ]))
            elements.append(t)
        
        elements.append(Spacer(1, 3*mm))
        
        # Situation professionnelle
        elements.append(Paragraph("Situation professionnelle", ParagraphStyle(name='SubHeading', 
                                                                        parent=styles['Heading2'], 
                                                                        textColor=orpi_red)))
        
        profession = st.session_state.get(f"profession_{i}", "")
        anciennete = st.session_state.get(f"anciennete_{i}", "")
        employeur = st.session_state.get(f"employeur_{i}", "")
        adresse_entreprise = st.session_state.get(f"adresse_entreprise_{i}", "")
        cp_entreprise = st.session_state.get(f"cp_entreprise_{i}", "")
        ville_entreprise = st.session_state.get(f"ville_entreprise_{i}", "")
        tel_employeur = st.session_state.get(f"tel_employeur_{i}", "")
        
        data = [
            ["Profession:", profession],
            ["Ancienneté:", anciennete],
            ["Employeur:", employeur],
            ["Adresse entreprise:", adresse_entreprise],
            ["Code postal:", cp_entreprise],
            ["Ville:", ville_entreprise],
            ["Téléphone employeur:", tel_employeur]
        ]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 3*mm))
        
        # Ressources
        elements.append(Paragraph("Ressources", ParagraphStyle(name='SubHeading', 
                                                          parent=styles['Heading2'], 
                                                          textColor=orpi_red)))
        
        revenus = st.session_state.get(f"revenus_{i}", 0)
        autres_revenus = st.session_state.get(f"autres_revenus_{i}", 0)
        total_revenus = revenus + autres_revenus
        
        data = [
            ["Revenus mensuels:", f"{revenus} €"],
            ["Autres revenus:", f"{autres_revenus} €"],
            ["Total revenus:", f"{total_revenus} €"]
        ]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 5*mm))
        
        # Signature
        elements.append(Paragraph("Je soussigné(e) certifie que les renseignements ci-dessus sont sincères et véritables.", styles['Normal']))
        date_signature = st.session_state.get("date_sig_loc", "")
        elements.append(Paragraph(f"Fait à Limoges, le {date_signature}", styles['Normal']))
        
        # Espace pour signature
        elements.append(Spacer(1, 20*mm))
        
        # Saut de page pour le prochain locataire s'il y en a
        if i < int(nb_locataires) - 1:
            elements.append(Paragraph("<br/><br/><br/>", styles['Normal']))
    
    # --- PARTIE GARANTS ---
    elements.append(Paragraph("<br/><br/><br/>", styles['Normal']))
    elements.append(Paragraph("DOSSIER GARANTS", styles['Heading1']))
    elements.append(Paragraph(f"Nombre de garants: {nb_garants}", styles['Normal']))
    elements.append(Spacer(1, 5*mm))
    
    # Pour chaque garant (code similaire à celui des locataires)
    for i in range(int(nb_garants)):
        elements.append(Paragraph(f"GARANT {i+1}", styles['Heading2']))
        elements.append(Spacer(1, 3*mm))
        
        # [Structure similaire aux locataires avec sous-sections et tableaux]
        # ...
        
        # Situation familiale
        elements.append(Paragraph("Situation familiale", ParagraphStyle(name='SubHeading', 
                                                                     parent=styles['Heading2'], 
                                                                     textColor=orpi_red)))
        
        situation_garant = st.session_state.get(f"situation_garant_{i}", "")
        data = [["État civil:", situation_garant]]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 3*mm))
        
        # Domicile actuel
        elements.append(Paragraph("Domicile actuel", ParagraphStyle(name='SubHeading', 
                                                                 parent=styles['Heading2'], 
                                                                 textColor=orpi_red)))
        
        domicile_garant = st.session_state.get(f"domicile_garant_{i}", "")
        data = [["Situation actuelle:", domicile_garant]]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 3*mm))
        
        # Civilité
        elements.append(Paragraph("Civilité", ParagraphStyle(name='SubHeading', 
                                                         parent=styles['Heading2'], 
                                                         textColor=orpi_red)))
        
        nom_garant = st.session_state.get(f"nom_garant_{i}", "")
        prenom_garant = st.session_state.get(f"prenom_garant_{i}", "")
        nom_jf_garant = st.session_state.get(f"nom_jf_garant_{i}", "")
        date_naissance_garant = st.session_state.get(f"date_naissance_garant_{i}", "")
        ville_naissance_garant = st.session_state.get(f"ville_naissance_garant_{i}", "")
        departement_garant = st.session_state.get(f"departement_garant_{i}", "")
        pays_garant = st.session_state.get(f"pays_garant_{i}", "")
        nationalite_garant = st.session_state.get(f"nationalite_garant_{i}", "")
        
        data = [
            ["Nom:", nom_garant],
            ["Prénom:", prenom_garant],
            ["Nom de jeune fille:", nom_jf_garant],
            ["Né(e) le:", str(date_naissance_garant)],
            ["Ville de naissance:", ville_naissance_garant],
            ["Département:", departement_garant],
            ["Pays:", pays_garant],
            ["Nationalité:", nationalite_garant]
        ]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 3*mm))
        
        # Autres sections pour les garants...
        # (Structure similaire à celle des locataires)
        
        # Signature
        elements.append(Paragraph("Je soussigné(e) certifie que les renseignements ci-dessus sont sincères et véritables.", styles['Normal']))
        date_signature_garant = st.session_state.get("date_sig_garant", "")
        elements.append(Paragraph(f"Fait à Limoges, le {date_signature_garant}", styles['Normal']))
        
        # Espace pour signature
        elements.append(Spacer(1, 20*mm))
        
        # Saut de page pour le prochain garant s'il y en a
        if i < int(nb_garants) - 1:
            elements.append(Paragraph("<br/><br/><br/>", styles['Normal']))
    
    # Mentions légales
    elements.append(Paragraph("<br/><br/><br/>", styles['Normal']))
    elements.append(Paragraph("MENTIONS LÉGALES", styles['Heading1']))
    elements.append(Paragraph("""
    Les informations recueillies font l'objet d'un traitement informatique nécessaire à l'exécution des missions de l'agent immobilier. 
    Conformément à la loi informatique et libertés du 6 janvier 1978 modifiée, les candidats bénéficient d'un droit d'accès, 
    de rectification et de suppression des informations qui les concernent. Pour exercer ce droit, 
    les parties peuvent s'adresser à l'Agence.
    """, styles['Normal']))
    
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph("Important : tout dossier incomplet ne peut être soumis à l'étude pour validation.", 
                             ParagraphStyle(name='Warning', parent=styles['Normal'], 
                                           textColor=orpi_red, fontName='Helvetica-Bold')))
    
    # Construire le document
    doc.build(elements, onFirstPage=add_orpi_header, onLaterPages=add_orpi_header)
    
    buffer.seek(0)
    return buffer.getvalue()
