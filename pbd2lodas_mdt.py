from flask import Flask
from flask import request
import os, webbrowser
from flask import render_template
from shutil import copyfile
from fpdf import FPDF


app = Flask(__name__)

@app.route('/')
def homepage():
    if os.path.exists("daten/abrechnungszeitraum.txt"):
        filequelle=open("daten/abrechnungszeitraum.txt","r", encoding='utf-8')
        for x in filequelle:
            var_abrmonat,var_abrjahr=x.split("|")
            break
        filequelle.close()
        var_textabr="Abrechnungszeitraum ist gewählt "
    else:
        var_abrmonat="MM"
        var_abrjahr="JJJJ"
        var_textabr="und wähle dann den Abrechnungszeitraum! "
    if os.path.exists("daten/basisdaten.txt"):
        var_textstamm="Konfiguration ist vorhanden "
    else:
        var_textstamm="Lege zuerst eine Konfiguration an "
    var_text=var_textstamm+var_textabr
    return render_template('index.html', v_text=var_text, v_monat=var_abrmonat, v_jahr=var_abrjahr)
# Block ok !

@app.route('/index.html', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        fileziel=open("daten/abrechnungszeitraum.txt","w")
        fileziel.write(request.form['form_monat']+"|"+request.form['form_jahr'])
        fileziel.close()
        var_textabr="Abrechnungszeitraum ist gewählt "
        var_abrmonat=request.form['form_monat']
        var_abrjahr=request.form['form_jahr']
    elif os.path.exists("daten/abrechnungszeitraum.txt"):
        filequelle=open("daten/abrechnungszeitraum.txt","r", encoding='utf-8')
        for x in filequelle:
            var_abrmonat,var_abrjahr=x.split("|")
            break
        filequelle.close()
        var_textabr="Abrechnungszeitraum ist gewählt "
    else:
        var_abrmonat="MM"
        var_abrjahr="JJJJ"
        var_textabr="Fehler: kein Abrechnungszeitraum gewählt! "
    if os.path.exists("daten/basisdaten.txt"):
        var_textstamm="Konfiguration ist vorhanden "
    else:
        var_textstamm="Fehler: Konfiguration ist nicht vorhanden! "
    var_text=var_textstamm+var_textabr
    return render_template('index.html', v_text=var_text, v_monat=var_abrmonat, v_jahr=var_abrjahr)
#Block ok

@app.route('/protokoll.html', methods=['POST', 'GET'])
def protokoll():
    if os.path.exists("daten/basisdaten.txt"):
        filequelle=open("daten/basisdaten.txt","r")
        for x in filequelle:
            var_beraternummer,var_mandantenummer,var_3,var_4,var_5,var_6,var_7,var_8,var_9,var_10,var_11,var_12,var_13,var_14,var_15,var_16,var_17,var_18,var_19,var_20,var_21,var_22=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: Konfiguration ist nicht vorhanden!"
        return render_template('index.html', v_text=var_text)
    if os.path.exists("daten/abrechnungszeitraum.txt"):
        filequelle=open("daten/abrechnungszeitraum.txt","r", encoding='utf-8')
        for x in filequelle:
            var_abrmonat,var_abrjahr=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: Es ist noch kein Abrechnungszeitraum ausgewählt! "
        return render_template('index.html', v_text=var_text)
        
 # Erstellen einer pdf  
    if os.path.exists("daten/abrechnungsdaten.txt"):
        class PDF(FPDF):
            def header(self):
                # Logo
                self.image('static/image001.png', 10, 8, 33)
                # Arial bold 15
                self.set_font('Arial', 'B', 15)
                # Move to the right
                self.cell(80)
                # Title
                self.cell(80, 10, 'Erfassungsprotokoll', 1, 0, 'C')
                # Line break
                self.ln(20)

            # Page footer
            def footer(self):
                # Position at 1.5 cm from bottom
                self.set_y(-15)
                # Arial italic 8
                self.set_font('Arial', 'B', 8)
                # Page number
                self.cell(0, 10, 'Seite ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

        # Instantiation of inherited class
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', '', 10)
    
        protokoll=open("daten/abrechnungsdaten.txt", "r")
    
        for line in protokoll:
            pdf.cell(0, 5, str(line), 0, 1)
        pdf.output('protokoll.pdf', 'F')
    
        protokoll.close()
        # Öffnen der Datei 
        os.startfile('protokoll.pdf')
    else:
        var_text="Fehler: Es sind keine Abrechnungsdaten erfasst! "
        return render_template('index.html', v_text=var_text)

    return render_template('index.html', v_bnr=var_beraternummer, v_mdt=var_mandantenummer, v_monat=var_abrmonat, v_jahr=var_abrjahr)
# Protokoll ok
# kann noch aufbereiten der Daten


#### Personalfragebogen der Daten ####
@app.route('/personalstammdaten.html', methods=['POST', 'GET'])
def personalstammdaten():

## Stammdaten und Abrechnungszeitraum vorhanden? 
    if os.path.exists("daten/basisdaten.txt"):
        filequelle=open("daten/basisdaten.txt","r")
        for x in filequelle:
            var_beraternummer,var_mandantenummer,var_3,var_4,var_5,var_6,var_7,var_8,var_9,var_10,var_11,var_12,var_13,var_14,var_15,var_16,var_17,var_18,var_19,var_20,var_21,var_22=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: Konfiguration ist nicht vorhanden! "
        return render_template('index.html', v_text=var_text)

    if os.path.exists("daten/abrechnungszeitraum.txt"):
        filequelle=open("daten/abrechnungszeitraum.txt","r", encoding='utf-8')
        for x in filequelle:
            var_abrmonat,var_abrjahr=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: Es ist noch kein Abrechnungszeitraum ausgewählt! "
        return render_template('index.html', v_text=var_text)

    if request.method == 'POST':
        if os.path.exists("daten/abrechnungsdaten.txt"):
        ## Datei öffnen und Daten werden angehangen
            # print("Datei offen")
            fileziel=open("daten/abrechnungsdaten.txt","a")
        else:
        ## Datei neu öffnen und Kopfdaten schreiben
            fileziel=open("daten/abrechnungsdaten.txt","w")
        # schreiben in Lodas Importdatei
            fileziel.write("[Allgemein]\nZiel=LODAS\nVersion_SST=1.0\nBeraterNr=")
            fileziel.write(var_beraternummer)
            fileziel.write("\nMandantenNr=")
            fileziel.write(var_mandantenummer)
            fileziel.write("\nDatumsformat=JJJJ-MM-TT")
            # Test Datum so wie von Bootstrap kommt
            fileziel.write("\nStringbegrenzer='")
            fileziel.write("\n\n* LEGENDE:\n* Datei erzeugt mit Tool pbd2lodas\n* AP: Andreé Rosenkranz; andree@rosenkranz.one\n\n")
            fileziel.write("* Satzbeschreibungen zur Übergabe von Bewegungsdaten für Mitarbeiter\n[Satzbeschreibung]\n")
            fileziel.write("\n10;u_lod_bwd_buchung_standard;abrechnung_zeitraum#bwd;pnr#bwd;la_eigene#bwd;bs_nr#bwd;bs_wert_butab#bwd;kostenstelle#bwd;")
            fileziel.write("\n20;u_lod_psd_beschaeftigung;pnr#psd;eintrittdatum#psd;austrittdatum#psd;arbeitsverhaeltnis#psd;schriftl_befristung#psd;datum_urspr_befr#psd;abschl_befr_arbvertr#psd;verl_befr_arbvertr#psd;befr_gr_2_monate#psd;")
            fileziel.write("\n21;u_lod_psd_mitarbeiter;pnr#psd;duevo_familienname#psd;duevo_vorname#psd;adresse_strassenname#psd;adresse_strasse_nr#psd;adresse_ort#psd;adresse_plz#psd;staatsangehoerigkeit#psd;geburtsdatum_ttmmjj#psd;geschlecht#psd;familienstand#psd;sozialversicherung_nr#psd;adresse_anschriftenzusatz#psd;gebort#psd;")
            fileziel.write("\n22;u_lod_psd_taetigkeit;pnr#psd;berufsbezeichnung#psd;persgrs#psd;schulabschluss#psd;ausbildungsabschluss#psd;stammkostenstelle#psd;")
            fileziel.write("\n23;u_lod_psd_arbeitszeit_regelm;pnr#psd;az_wtl_indiv#psd;")
            fileziel.write("\n24;u_lod_psd_steuer;pnr#psd;identifikationsnummer#psd;els_2_haupt_ag_kz#psd;st_klasse#psd;kfb_anzahl#psd;faktor#psd;")
            fileziel.write("\n25;u_lod_psd_sozialversicherung;pnr#psd;kz_zuschl_pv_kinderlose#psd;kv_bgrs#psd;rv_bgrs#psd;av_bgrs#psd;pv_bgrs#psd;")
            fileziel.write("\n26;u_lod_psd_ma_bank;pnr#psd;ma_bank_zahlungsart#psd;ma_iban#psd;")
            fileziel.write("\n27;u_lod_psd_festbezuege;pnr#psd;festbez_id#psd;lohnart_nr#psd;betrag#psd;")
            fileziel.write("\n28;u_lod_psd_lohn_gehalt_bezuege;pnr#psd;std_lohn_1#psd;")
            fileziel.write("\n\n")

        if request.form['form_personalnummer'] == "":
            pass
            # Fehler wird vom Frontend abgefangen
            # print("Fehler PNR")
        else:
            #Geburtsdatum muss formatiert werden
            var_geburtsdatum=request.form['form_gebdatum']
            var_geburtsdatum=str(var_geburtsdatum)   
            var_geburtsjahr=var_geburtsdatum[0:4]   
            var_geburtsmonat=var_geburtsdatum[5:7]
            var_geburtstag=var_geburtsdatum[8:10]
            #print(var_geburtsdatum)
            #print(var_geburtstag)
            #print(var_geburtsmonat)
            #print(var_geburtsjahr)
            
            
            fileziel.write("\n\n[Stammdaten]\n20;"+request.form['form_personalnummer']+";"+request.form['form_eintrittsdatum']+";"+request.form['form_austrittsdatum']+";;;;;;")
            fileziel.write("\n21;"+request.form['form_personalnummer']+";'"+request.form['form_name']+"';'"+request.form['form_vorname']+"';'"+request.form['form_strasse']+"';'"+request.form['form_hausnummer']+"';'"+request.form['form_wohnort']+"';"+request.form['form_plz']+";000;"+var_geburtstag+var_geburtsmonat+var_geburtsjahr+";"+request.form['form_geschlecht']+";;"+request.form['form_svnummer']+";;"+request.form['form_geburtsort']+";")
            fileziel.write("\n22;"+request.form['form_personalnummer']+";"+request.form['form_berufsbezeichnung']+";"+request.form['form_pgr']+";"+request.form['form_schulabschluss']+";"+request.form['form_berufsausbildung']+";"+request.form['form_kostenstelle']+";")
            fileziel.write("\n23;"+request.form['form_personalnummer']+";"+request.form['form_waz']+";")
            fileziel.write("\n24;"+request.form['form_personalnummer']+";"+request.form['form_steuerid']+";"+request.form['form_artderbeschaeftigung']+";"+request.form['form_steuerklasse']+";"+request.form['form_kinderfreibetrag']+";;")
            fileziel.write("\n25;"+request.form['form_personalnummer']+";"+request.form['form_elterneigenschaft']+";"+request.form['form_KV']+";"+request.form['form_RV']+";"+request.form['form_AV']+";"+request.form['form_PV']+";")
            fileziel.write("\n26;"+request.form['form_personalnummer']+";5;"+request.form['form_iban']+";")
            if request.form['form_gehalt'] == "1":
                if request.form['form_eurovorkomma'] == "":
                    pass
                else:
                    # Gehalt eLOA 1
                    fileziel.write("\n27;"+request.form['form_personalnummer']+";1;1;"+request.form['form_eurovorkomma']+","+request.form['form_euronachkomma']+";")
            elif request.form['form_gehalt'] == "2":
                # Festlohn eLOA 51 
                fileziel.write("\n27;"+request.form['form_personalnummer']+";1;51;"+request.form['form_eurovorkomma']+","+request.form['form_euronachkomma']+";")
            elif request.form['form_gehalt'] == "3":
                # Stundenlohn
                fileziel.write("\n28;"+request.form['form_personalnummer']+";"+request.form['form_eurovorkomma']+","+request.form['form_euronachkomma']+";")
            else:
                pass
            fileziel.write("\n[Hinweisdaten]\n")
            fileziel.write("Hinweis: PNR: "+request.form['form_personalnummer']+" Krankenkasse: "+request.form['form_krankenkasse']+" Staatsangehörigkeit: "+request.form['form_staatsang']+"\n")
            
            if request.form['form_geburtsland'] == "" and request.form['form_steuerklasse'] == "":
                pass
            else:
                fileziel.write("Hinweis: PNR: "+request.form['form_personalnummer']+" Geburtsland: "+request.form['form_geburtsland']+" Steuerklasse "+request.form['form_steuerklasse'])
        ## Fehler 
            if request.form['form_kinderfreibetrag'] == "" and request.form['form_konfession'] == "":
                pass
            else:
                fileziel.write(" Kinderfreibetrag "+request.form['form_kinderfreibetrag']+" Konfession: "+request.form['form_konfession']+"\n")
            
            if request.form['form_freiertext'] == "":
                pass
            else:
                fileziel.write("\n Text aus der Erfassung: "+request.form['form_freiertext']+"\n")
        fileziel.close()
    else:
        pass
    return render_template('personalstammdaten.html', v_bnr=var_beraternummer, v_mdt=var_mandantenummer, v_monat=var_abrmonat, v_jahr=var_abrjahr)



@app.route('/basisdaten.html', methods=['POST', 'GET'])
def basisdaten():
##############################################################
### Anlage der Stammdaten (Konfiguration) für die Erfassung
### Beraternummer, Mandant und Lohnarten mit Text = 5 für Stunden, 5 für Betrag
##############################################################

    if request.method == 'POST':
        fileziel=open("daten/basisdaten.txt","w")
        # schreiben in Datei für Basisdaten
        fileziel.write(request.form['form_berater']+"|"+request.form['form_mandant']+"|")
        if (request.form['loa_ns1'] != "" and request.form['loa_ts1'] != "") and (request.form['loa_ns1'] != "Nummer") :
            fileziel.write(request.form['loa_ns1']+"|"+request.form['loa_ts1']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_ns2'] != "" and request.form['loa_ts2'] != "") and (request.form['loa_ns2'] != "Nummer"):
            fileziel.write(request.form['loa_ns2']+"|"+request.form['loa_ts2']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_ns3'] != "" and request.form['loa_ts3'] != "" ) and (request.form['loa_ns3'] != "Nummer"):
            fileziel.write(request.form['loa_ns3']+"|"+request.form['loa_ts3']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_ns4'] != "" and request.form['loa_ts4'] != "") and (request.form['loa_ns4'] != "Nummer"):
            fileziel.write(request.form['loa_ns4']+"|"+request.form['loa_ts4']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_ns5'] != "" and request.form['loa_ts5'] != "") and (request.form['loa_ns5'] != "Nummer"):
            fileziel.write(request.form['loa_ns5']+"|"+request.form['loa_ts5']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_nb1'] != "" and request.form['loa_tb1'] != "") and (request.form['loa_nb1'] != "Nummer"):
            fileziel.write(request.form['loa_nb1']+"|"+request.form['loa_tb1']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_nb2'] != "" and request.form['loa_tb2'] != "") and (request.form['loa_nb2'] != "Nummer"):
            fileziel.write(request.form['loa_nb2']+"|"+request.form['loa_tb2']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_nb3'] != "" and request.form['loa_tb3'] != "") and (request.form['loa_nb3'] != "Nummer"):
            fileziel.write(request.form['loa_nb3']+"|"+request.form['loa_tb3']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_nb4'] != "" and request.form['loa_tb4'] != "") and (request.form['loa_nb4'] != "Nummer"):
            fileziel.write(request.form['loa_nb4']+"|"+request.form['loa_tb4']+"|")
        else:
            fileziel.write("nicht|buchen|")
        if (request.form['loa_nb5'] != "" and request.form['loa_tb5'] != "") and (request.form['loa_nb5'] != "Nummer"):
            fileziel.write(request.form['loa_nb5']+"|"+request.form['loa_tb5'])
        else:
            fileziel.write("nicht|buchen")
        fileziel.close()
    else:
        pass
    return render_template('basisdaten.html')

###############################################
#### Stundenerfassung und Anlage der Daten ####

@app.route('/erfassungstunden.html', methods=['POST', 'GET'])
def stundenerfassung():

## stammdaten lesen - qualitätssicherung fehlt noch 
    if os.path.exists("daten/basisdaten.txt"):
        filequelle=open("daten/basisdaten.txt","r")
        for x in filequelle:
            var_beraternummer,var_mandantenummer,var_3,var_4,var_5,var_6,var_7,var_8,var_9,var_10,var_11,var_12,var_13,var_14,var_15,var_16,var_17,var_18,var_19,var_20,var_21,var_22=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: Konfiguration ist nicht vorhanden! "
        return render_template('index.html', v_text=var_text)
#        return render_template('basisdaten.html')
    if os.path.exists("daten/abrechnungszeitraum.txt"):
        filequelle=open("daten/abrechnungszeitraum.txt","r", encoding='utf-8')
        for x in filequelle:
            var_abrmonat,var_abrjahr=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: Du hast noch keinen Abrechnungszeitraum angelegt!"
        return render_template('index.html', v_text=var_text)

    if request.method == 'POST':
        if os.path.exists("daten/abrechnungsdaten.txt"):
        ## Datei öffnen und Daten werden angehangen
            fileziel=open("daten/abrechnungsdaten.txt","a")
            fileziel.write("\n* Stunden zur Abrechnung von Mitarbeitern\n")
            fileziel.write("[Bewegungsdaten]\n")
        else:
        ## Datei neu öffnen und Kopfdaten schreiben
            fileziel=open("daten/abrechnungsdaten.txt","w")
        # schreiben in Lodas Importdatei
            fileziel.write("[Allgemein]\nZiel=LODAS\nVersion_SST=1.0\nBeraterNr=")
            fileziel.write(var_beraternummer)
            fileziel.write("\nMandantenNr=")
            fileziel.write(var_mandantenummer)
            fileziel.write("\nDatumsformat=JJJJ-MM-TT")
            # Test Datum so wie von Bootstrap komm
            # t
            fileziel.write("\nStringbegrenzer='")
            fileziel.write("\n\n* LEGENDE:\n* Datei erzeugt mit Tool pbd2lodas\n* AP: Andreé Rosenkranz; andree@rosenkranz.one\n\n")
            fileziel.write("* Satzbeschreibungen zur Übergabe von Bewegungsdaten für Mitarbeiter\n[Satzbeschreibung]\n")
            fileziel.write("\n10;u_lod_bwd_buchung_standard;abrechnung_zeitraum#bwd;pnr#bwd;la_eigene#bwd;bs_nr#bwd;bs_wert_butab#bwd;kostenstelle#bwd;")
            fileziel.write("\n20;u_lod_psd_beschaeftigung;pnr#psd;eintrittdatum#psd;austrittdatum#psd;arbeitsverhaeltnis#psd;schriftl_befristung#psd;datum_urspr_befr#psd;abschl_befr_arbvertr#psd;verl_befr_arbvertr#psd;befr_gr_2_monate#psd;")
            fileziel.write("\n21;u_lod_psd_mitarbeiter;pnr#psd;duevo_familienname#psd;duevo_vorname#psd;adresse_strassenname#psd;adresse_strasse_nr#psd;adresse_ort#psd;adresse_plz#psd;staatsangehoerigkeit#psd;geburtsdatum_ttmmjj#psd;geschlecht#psd;familienstand#psd;sozialversicherung_nr#psd;adresse_anschriftenzusatz#psd;gebort#psd;")
            fileziel.write("\n22;u_lod_psd_taetigkeit;pnr#psd;berufsbezeichnung#psd;persgrs#psd;schulabschluss#psd;ausbildungsabschluss#psd;stammkostenstelle#psd;")
            fileziel.write("\n23;u_lod_psd_arbeitszeit_regelm;pnr#psd;az_wtl_indiv#psd;")
            fileziel.write("\n24;u_lod_psd_steuer;pnr#psd;identifikationsnummer#psd;els_2_haupt_ag_kz#psd;st_klasse#psd;kfb_anzahl#psd;faktor#psd;")
            fileziel.write("\n25;u_lod_psd_sozialversicherung;pnr#psd;kz_zuschl_pv_kinderlose#psd;kv_bgrs#psd;rv_bgrs#psd;av_bgrs#psd;pv_bgrs#psd;")
            fileziel.write("\n26;u_lod_psd_ma_bank;pnr#psd;ma_bank_zahlungsart#psd;ma_iban#psd;")
            fileziel.write("\n27;u_lod_psd_festbezuege;pnr#psd;festbez_id#psd;lohnart_nr#psd;betrag#psd;")
            fileziel.write("\n28;u_lod_psd_lohn_gehalt_bezuege;pnr#psd;std_lohn_1#psd;")
            fileziel.write("\n\n")
            fileziel.write("* Stunden zur Abrechnung von Mitarbeitern\n\n")
            fileziel.write("[Bewegungsdaten]\n\n")

        if request.form['form_personalnummer'] == "" or request.form['form_wert'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_3+";1;"+request.form['form_wert']+";"+request.form['form_kostenstelle']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fw2'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_5+";1;"+request.form['fw2']+";"+request.form['fk2']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fw3'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_7+";1;"+request.form['fw3']+";"+request.form['fk3']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fw4'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_9+";1;"+request.form['fw4']+";"+request.form['fk4']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fw5'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_11+";1;"+request.form['fw5']+";"+request.form['fk5']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fl6'] == "" or request.form['fw6'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+request.form['fl6']+";1;"+request.form['fw6']+";"+request.form['fk6']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fl7'] == "" or request.form['fw7'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+request.form['fl7']+";1;"+request.form['fw7']+";"+request.form['fk7']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fl8'] == "" or request.form['fw8'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+request.form['fl8']+";1;"+request.form['fw8']+";"+request.form['fk8']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fl9'] == "" or request.form['fw9'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+request.form['fl9']+";1;"+request.form['fw9']+";"+request.form['fk9']+";\n")
        fileziel.close()
    else:
        pass
    
    return render_template('erfassungstunden.html', v_bnr=var_beraternummer, v_mdt=var_mandantenummer, v_monat=var_abrmonat, v_jahr=var_abrjahr, v_sn1=var_3,v_st1=var_4,v_sn2=var_5,v_st2=var_6,
    v_sn3=var_7,v_st3=var_8,v_sn4=var_9,v_st4=var_10,v_sn5=var_11,v_st5=var_12,v_bn1=var_13,v_bt1=var_14,v_bn2=var_15,v_bt2=var_16,v_bn3=var_17,v_bt3=var_18,v_bn4=var_19,v_bt4=var_20,v_bn5=var_21,
    v_bt5=var_22)


@app.route('/erfassungbetrag.html', methods=['POST', 'GET'])
def betragerfassung():
    
    if os.path.exists("daten/basisdaten.txt"):
        filequelle=open("daten/basisdaten.txt","r")
        for x in filequelle:
            var_beraternummer,var_mandantenummer,var_3,var_4,var_5,var_6,var_7,var_8,var_9,var_10,var_11,var_12,var_13,var_14,var_15,var_16,var_17,var_18,var_19,var_20,var_21,var_22=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: Konfiguration ist nicht vorhanden! "
        return render_template('index.html', v_text=var_text)
#        return render_template('basisdaten.html')
    if os.path.exists("daten/abrechnungszeitraum.txt"):
        filequelle=open("daten/abrechnungszeitraum.txt","r", encoding='utf-8')
        for x in filequelle:
            var_abrmonat,var_abrjahr=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: Du hast noch keinen Abrechnungszeitraum angelegt!"
        return render_template('index.html', v_text=var_text)
    
    if request.method == 'POST':
## stammdaten lesen - qualitätssicherung fehlt noch 
        if os.path.exists("daten/abrechnungsdaten.txt"):
        ## Datei öffnen und Daten werden angehangen
            fileziel=open("daten/abrechnungsdaten.txt","a")
            fileziel.write("\n* Beträge zur Abrechnung von Mitarbeitern\n")
            fileziel.write("[Bewegungsdaten]\n\n")
        else:
        ## Datei neu öffnen und Kopfdaten schreiben
            fileziel=open("daten/abrechnungsdaten.txt","w")
        # schreiben in Lodas Importdatei
            fileziel.write("[Allgemein]\nZiel=LODAS\nVersion_SST=1.0\nBeraterNr=")
            fileziel.write(var_beraternummer)
            fileziel.write("\nMandantenNr=")
            fileziel.write(var_mandantenummer)
            fileziel.write("\nDatumsformat=JJJJ-MM-TT")
            # Test Datum so wie von Bootstrap komm
            # t
            fileziel.write("\nStringbegrenzer='")
            fileziel.write("\n\n* LEGENDE:\n* Datei erzeugt mit Tool pbd2lodas\n* AP: Andreé Rosenkranz; andree@rosenkranz.one\n\n")
            fileziel.write("* Satzbeschreibungen zur Übergabe von Bewegungsdaten für Mitarbeiter\n[Satzbeschreibung]\n")
            fileziel.write("\n10;u_lod_bwd_buchung_standard;abrechnung_zeitraum#bwd;pnr#bwd;la_eigene#bwd;bs_nr#bwd;bs_wert_butab#bwd;kostenstelle#bwd;")
            fileziel.write("\n20;u_lod_psd_beschaeftigung;pnr#psd;eintrittdatum#psd;austrittdatum#psd;arbeitsverhaeltnis#psd;schriftl_befristung#psd;datum_urspr_befr#psd;abschl_befr_arbvertr#psd;verl_befr_arbvertr#psd;befr_gr_2_monate#psd;")
            fileziel.write("\n21;u_lod_psd_mitarbeiter;pnr#psd;duevo_familienname#psd;duevo_vorname#psd;adresse_strassenname#psd;adresse_strasse_nr#psd;adresse_ort#psd;adresse_plz#psd;staatsangehoerigkeit#psd;geburtsdatum_ttmmjj#psd;geschlecht#psd;familienstand#psd;sozialversicherung_nr#psd;adresse_anschriftenzusatz#psd;gebort#psd;")
            fileziel.write("\n22;u_lod_psd_taetigkeit;pnr#psd;berufsbezeichnung#psd;persgrs#psd;schulabschluss#psd;ausbildungsabschluss#psd;stammkostenstelle#psd;")
            fileziel.write("\n23;u_lod_psd_arbeitszeit_regelm;pnr#psd;az_wtl_indiv#psd;")
            fileziel.write("\n24;u_lod_psd_steuer;pnr#psd;identifikationsnummer#psd;els_2_haupt_ag_kz#psd;st_klasse#psd;kfb_anzahl#psd;faktor#psd;")
            fileziel.write("\n25;u_lod_psd_sozialversicherung;pnr#psd;kz_zuschl_pv_kinderlose#psd;kv_bgrs#psd;rv_bgrs#psd;av_bgrs#psd;pv_bgrs#psd;")
            fileziel.write("\n26;u_lod_psd_ma_bank;pnr#psd;ma_bank_zahlungsart#psd;ma_iban#psd;")
            fileziel.write("\n27;u_lod_psd_festbezuege;pnr#psd;festbez_id#psd;lohnart_nr#psd;betrag#psd;")
            fileziel.write("\n28;u_lod_psd_lohn_gehalt_bezuege;pnr#psd;std_lohn_1#psd;")
            fileziel.write("\n\n")
            fileziel.write("* Stunden und Beträge zur Abrechnung von Mitarbeitern\n\n")
            fileziel.write("[Bewegungsdaten]\n\n")

        if request.form['form_personalnummer'] == "" or request.form['form_wert'] == "":
            pass # Pflichtfeld im Frontend print("Fehler im backend - kann aber nicht sein!")
    
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_13+";2;"+request.form['form_wert']+";"+request.form['form_kostenstelle']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fw2'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_15+";2;"+request.form['fw2']+";"+request.form['fk2']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fw3'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_17+";2;"+request.form['fw3']+";"+request.form['fk3']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fw4'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_19+";2;"+request.form['fw4']+";"+request.form['fk4']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fw5'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+var_21+";2;"+request.form['fw5']+";"+request.form['fk5']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fl6'] == "" or request.form['fw6'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+request.form['fl6']+";2;"+request.form['fw6']+";"+request.form['fk6']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fl7'] == "" or request.form['fw7'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+request.form['fl7']+";2;"+request.form['fw7']+";"+request.form['fk7']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fl8'] == "" or request.form['fw8'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+request.form['fl8']+";2;"+request.form['fw8']+";"+request.form['fk8']+";\n")
        if request.form['form_personalnummer'] == "" or request.form['fl9'] == "" or request.form['fw9'] == "":
            pass
        else:
            fileziel.write("10;"+var_abrjahr+"-"+var_abrmonat+"-01;"+request.form['form_personalnummer']+";"+request.form['fl9']+";2;"+request.form['fw9']+";"+request.form['fk9']+";\n")
        fileziel.close()
    else:
        pass
    return render_template('erfassungbetrag.html', v_bnr=var_beraternummer, v_mdt=var_mandantenummer, v_monat=var_abrmonat, v_jahr=var_abrjahr,v_sn1=var_3,v_st1=var_4,v_sn2=var_5,v_st2=var_6,
    v_sn3=var_7,v_st3=var_8,v_sn4=var_9,v_st4=var_10,v_sn5=var_11,v_st5=var_12,v_bn1=var_13,v_bt1=var_14,v_bn2=var_15,v_bt2=var_16,v_bn3=var_17,v_bt3=var_18,v_bn4=var_19,v_bt4=var_20,v_bn5=var_21,
    v_bt5=var_22)

@app.route('/konvertierung.html', methods=['POST', 'GET'])
def konvert():
    if os.path.exists("daten/basisdaten.txt"):
        filequelle=open("daten/basisdaten.txt","r")
        for x in filequelle:
            var_beraternummer,var_mandantenummer,var_3,var_4,var_5,var_6,var_7,var_8,var_9,var_10,var_11,var_12,var_13,var_14,var_15,var_16,var_17,var_18,var_19,var_20,var_21,var_22=x.split("|")
            break
        filequelle.close()
    else:
        var_text=("Fehler: ** Es kann keine Lodas Datei erstellt werden ** Konfiguration nicht vorhanden! ****")
        return render_template('index.html', v_text=var_text)

    if os.path.exists("daten/abrechnungszeitraum.txt"):
        filequelle=open("daten/abrechnungszeitraum.txt","r", encoding='utf-8')
        for x in filequelle:
            var_abrmonat,var_abrjahr=x.split("|")
            break
        filequelle.close()
    else:
        var_text="Fehler: ** Es kann keine Lodas Datei erstellt werden ** Du hast noch keinen Abrechnungszeitraum angelegt! ****"
        return render_template('index.html', v_text=var_text)

    if os.path.exists("daten/abrechnungsdaten.txt"):
        copyfile('daten/abrechnungsdaten.txt', 'daten/'+var_abrjahr+var_abrmonat+'_'+var_mandantenummer+'_'+var_beraternummer+'_lodas.txt') 
        os.remove('daten/abrechnungszeitraum.txt')
        os.remove('daten/abrechnungsdaten.txt')
        var_text="Die Datei "+var_abrjahr+var_abrmonat+"_"+var_mandantenummer+"_"+var_beraternummer+"_lodas.txt wurde im Verzeichniss /daten erstellt. Stelle diese Datei deinem Steuerberater zur Verfügung"
    else:
        var_text="Fehler: **** Es gibt keine Datei mit Abrechnungsdaten, es konnte keine Datei konvertiert werden. ****"

    return render_template('index.html', v_text=var_text)

webbrowser.open('http://localhost:1701')

if __name__ =='__main__':
    app.run(port=1701, debug=False)