# -*- coding: utf-8 -*-

import unohelper


class Baumansicht():
    
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)
        
        self.ctx = mb.ctx
        self.mb = mb
        self.listener_treeview_symbol = TreeView_Symbol_Listener(self.ctx,self.mb)
        self.tag1_listener = Tag1_Listener(self.mb)
        self.tag2_listener = Tag2_Listener(self.mb)
        
    def start(self):
        if self.mb.debug: log(inspect.stack)

        self.mb.props[T.AB].Hauptfeld = self.erzeuge_Feld_Baumansicht(self.mb.prj_tab)  
        self.mb.class_Fenster.erzeuge_Scrollbar2()

        
    def erzeuge_Feld_Baumansicht(self,win):
        if self.mb.debug: log(inspect.stack)
        # Das aeussere Hauptfeld wird fuers Scrollen benoetigt. Das innere und eigentliche
        # Hauptfeld scrollt dann in diesem Hauptfeld_aussen

        # Hauptfeld_Aussen
        PosX,PosY,Width,Height = 22, KONST.ZEILENHOEHE + 2, 1000, 1800
        
        control1, model1 = self.mb.createControl(self.ctx,"Container",PosX,PosY,Width,Height,(),() )  
        
             
        win.addControl('Hauptfeld_aussen',control1)  
        
        # eigentliches Hauptfeld
        PosX,PosY,Width,Height = 0, 0, 1000, 10000
         
        control2, model2 = self.mb.createControl(self.ctx,"Container",PosX,PosY,Width,Height,(),() )  

        model2.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
        control1.addControl('Hauptfeld',control2)  
        self.mb.hauptfeld_aussen = control1
        return control2

  
    def erzeuge_Zeile_in_der_Baumansicht(self,eintrag,gliederung,index=0,tab_name = 'ORGANON',neuer_tab=False):
        if self.mb.debug: log(inspect.stack)
        
        # wird in projects aufgerufen
        ordinal,parent,name,lvl,art,zustand,sicht,tag1,tag2,tag3 = eintrag        

        ##### Aeusserer Container #######
        PosX,PosY,Width,Height = 2, KONST.ZEILENHOEHE * index, 600, 20
        
        prop_names = ('Text','BackgroundColor')
        prop_values = (ordinal,KONST.FARBE_HF_HINTERGRUND)
        control, model = self.mb.createControl( self.ctx, "Container", PosX, PosY, Width, Height, prop_names, prop_values )  
            
        self.mb.props[tab_name].Hauptfeld.addControl(ordinal,control)
        
        sett = self.mb.settings_proj
        sicht_tag1 = int(sett['tag1'])
        sicht_tag2 = int(sett['tag2'])
        sicht_tag3 = int(sett['tag3'])
        
        ### einzelne Elemente #####

        # Icon
        x = 16 + int(lvl) * 16
        control2, model2 = self.mb.createControl(self.ctx,"ImageControl", x, 2, 16, 16, ('Border',), (0,) ) 
        control2.addMouseListener(self.listener_treeview_symbol)
        
        tab = T.AB
        if neuer_tab:
            tab = tab_name
        
        props = self.mb.props


        if art in ('dir','prj'):
            
            if art == 'prj':
                props[tab].Projektordner = ordinal

            if zustand == 'auf':
                model2.ImageURL = KONST.IMG_ORDNER_GEOEFFNET_16 
            else:
                bild_ordner = KONST.IMG_ORDNER_16

                tree = props[tab].xml_tree 
                root = tree.getroot()

                ordner_xml = root.find('.//'+ordinal)
                if ordner_xml != None:
                    childs = list(ordner_xml)
                    if len(childs) > 0:
                        bild_ordner = KONST.IMG_ORDNER_VOLL_16

                model2.ImageURL = bild_ordner
            schriftfarbe = KONST.FARBE_SCHRIFT_ORDNER
                
        elif art == 'pg':
            model2.ImageURL = 'private:graphicrepository/res/sx03150.png' 
            schriftfarbe = KONST.FARBE_SCHRIFT_DATEI
            
        elif art == 'waste':
            
            props[tab].Papierkorb = ordinal
            
            if zustand == 'zu':
                model2.ImageURL = KONST.IMG_PAPIERKORB_LEER
            else:
                model2.ImageURL = KONST.IMG_PAPIERKORB_GEOEFFNET
            sicht_tag1 = sicht_tag2 = sicht_tag3 = False
            
            schriftfarbe = KONST.FARBE_SCHRIFT_ORDNER
        

        control.addControl('icon',control2)                       
        # return ist nur fuer neu angelegte Dokumente nutzbar 
        
                
        x += 18
        
        if sicht_tag1:
            # Tag1 Farbe
            prop_names = ('ImageURL','Border')
            prop_values = ('vnd.sun.star.extension://xaver.roemers.organon/img/punkt_%s.png' % tag1,0)
            control_tag1, model_tag1 = self.mb.createControl(self.ctx,"ImageControl",x,2,16,16,prop_names,prop_values )  
            control_tag1.addMouseListener(self.tag1_listener)
            control.addControl('tag1',control_tag1)
            x += 16
            
        if sicht_tag2:
            # Tag2 BENUTZERDEFINIERT
            prop_names = ('ImageURL','Border')
            prop_values = (tag2,0)
            control_tag2, model_tag2 = self.mb.createControl(self.ctx,"ImageControl",x,2,16,16,prop_names,prop_values )  
            control_tag2.addMouseListener(self.tag2_listener)
            
            control.addControl('tag2',control_tag2)
            x += 18
        
        if sicht_tag3:
            # Tag3 GLIEDERUNG
            prop_names = ('Label','TextColor')
            prop_values = (gliederung[ordinal],KONST.FARBE_GLIEDERUNG)
            control_tag3, model_tag3 = self.mb.createControl(self.mb.ctx,"FixedText",x,2,16,16,prop_names,prop_values )
            
            breite,hoehe = self.mb.kalkuliere_und_setze_Control(control_tag3,'w')
            control.addControl('tag3',control_tag3)
            x += breite + 4

        
        # Textfeld
        prop_names = ('Text','Border','BackgroundColor','ReadOnly','TextColor')
        prop_values = (name,0,KONST.FARBE_HF_HINTERGRUND,True,schriftfarbe)
        control1, model1 = self.mb.createControl(self.ctx,"Edit",x,0,400,20,prop_names,prop_values )  
        

        control1.addMouseListener(self.mb.class_Zeilen_Listener) 
        control1.addMouseMotionListener(self.mb.class_Zeilen_Listener)
        control1.addFocusListener(self.mb.class_Zeilen_Listener)

        control.addControl('textfeld',control1)
        
        
        if sicht == 'nein':
            control.Visible = False
        else:              
            index += 1
        return index,control
    
    
    def positioniere_icons_in_zeile(self,contr_zeile,tags,gliederung):
        #if self.mb.debug: log(inspect.stack)
        
        try:
            tag1,tag2,tag3 = tags
            
            x = contr_zeile.getControl('icon').PosSize.X +18
            breite = 0
            
            if tag1:
                tag1_contr = contr_zeile.getControl('tag1')
                tag1_contr.setPosSize(x,0,0,0,1)
                x += 16
                breite = 16
                
            if tag2:
                tag2_contr = contr_zeile.getControl('tag2')
                tag2_contr.setPosSize(x,0,0,0,1)
                x += 18
                breite = 18
                
            if tag3:
                tag3_contr = contr_zeile.getControl('tag3')
                
                ordinal = tag3_contr.AccessibleContext.AccessibleParent.AccessibleContext.AccessibleName
                if ordinal != self.mb.props[T.AB].Papierkorb:
                    tag3_contr.Model.Label = gliederung[ordinal]
                else:
                    tag3_contr.Model.Label = ''
                breite,hoehe = self.mb.kalkuliere_und_setze_Control(tag3_contr)  
                breite += 4              
                tag3_contr.setPosSize(x,0,0,0,1)
                x += breite
            

            text_contr = contr_zeile.getControl('textfeld')
            if text_contr.PosSize.X != x:
                text_contr.setPosSize(x,0,0,0,1)
            
        except:
            log(inspect.stack,tb())
            
    

    def korrigiere_scrollbar(self):
        if self.mb.debug: log(inspect.stack)
        
        tabsX = self.mb.tabsX
                
        win = tabsX.Hauptfelder[T.AB]
        SB = win.getControl('ScrollBar')   
        
        MBHoehe = 22
        tableiste_hoehe = self.mb.tabsX.tableiste_hoehe 
        mb_hoehe = self.mb.win.Size.Height - MBHoehe - tableiste_hoehe
        
        if SB.Size.Height != mb_hoehe:
            SB.setPosSize(0,0,0,mb_hoehe,8)
        
        hoehe = sorted(list(self.mb.props[T.AB].dict_zeilen_posY))

        sb_hoehe = SB.Size.Height
        
        baum_hoehe = hoehe[-1] + 20
        if hoehe != []:
            omax =  baum_hoehe - (sb_hoehe) 
            if omax > 0:
                SB.Visible = True
                SB.LineIncrement = baum_hoehe/sb_hoehe*50
                SB.BlockIncrement = 200
                SB.Maximum =  baum_hoehe  
                SB.VisibleSize = sb_hoehe - 40
                # Bei Mausradnutzung Mausradlistener einschalten
                if self.mb.settings_orga['mausrad']:
                    self.mb.mausrad_an = True
            else:
                SB.Maximum  = 1
                SB.Visible = False
                nav_cont_aussen = win.getControl('Hauptfeld_aussen')
                nav_cont = nav_cont_aussen.getControl('Hauptfeld')
                nav_cont.setPosSize(0, 0,0,0,2)
                # Mausradlistener ausschalten
                self.mb.mausrad_an = False
        
        
    # Nur fuers Debugging
    def finde_falschen_bereich(self):
        if self.mb.debug: log(inspect.stack)
        
        sections = self.mb.doc.TextSections
        names = sections.ElementNames
        if 'Bereich1' in names:
            print('Bereich ist drin')

    
    def erzeuge_neue_Zeile(self,ordner_oder_datei,neuer_Name=None):
        if self.mb.debug: log(inspect.stack)
        
        papierkorb_inhalt = self.mb.class_XML.get_papierkorb_inhalt()
        props = self.mb.props[T.AB]
        selektierte_zeile = props.selektierte_zeile
        
        if selektierte_zeile == None:       
            Popup(self.mb, 'info').text = LANG.ZEILE_AUSWAEHLEN
            return None
        elif selektierte_zeile in papierkorb_inhalt:       
            Popup(self.mb, 'info').text = LANG.NICHT_IM_PAPIERKORB_ERSTELLEN
            return None
        else:
            try:
                StatusIndicator = self.mb.desktop.getCurrentFrame().createStatusIndicator()
                StatusIndicator.start(LANG.ERZEUGE_NEUE_ZEILE,2)
                StatusIndicator.setValue(2)
                
                self.mb.doc.lockControllers()
                                
                # XML TREE
                tree = props.xml_tree
                root = tree.getroot()
                xml_sel_zeile = root.find('.//' + selektierte_zeile)
                
                # Props ordinal,parent,name,lvl,art,zustand,sicht,tag1,tag2,tag3
                ordinal = 'nr' + root.attrib['kommender_Eintrag']
                parent = xml_sel_zeile.attrib['Parent']
                name = ordinal if neuer_Name == None else neuer_Name
                lvl = xml_sel_zeile.attrib['Lvl']
                tag1 = 'leer' #xml_sel_zeile.attrib['Tag1']
                tag2 = xml_sel_zeile.attrib['Tag2']
                tag3 = xml_sel_zeile.attrib['Tag3']
                sicht = 'ja' 
                if ordner_oder_datei == 'Ordner':
                    art = 'dir'
                    zustand = 'zu'
                else:
                    art = 'pg'
                    zustand = '-'            
                eintrag = ordinal,parent,name,lvl,art,zustand,sicht,tag1,tag2,tag3 
                
                # neue Zeile / neuer XML Eintrag
                self.mb.class_XML.erzeuge_XML_Eintrag(eintrag)
                
                if self.mb.settings_proj['tag3']:
                    gliederung = self.mb.class_Gliederung.rechne(tree)
                else:
                    gliederung = None

                self.erzeuge_Zeile_in_der_Baumansicht(eintrag,gliederung)
                self.mb.class_Tags.erzeuge_tags_ordinal_eintrag(ordinal)
                self.mb.class_Tags.speicher_tags()
                            
                # neue Datei / neuen Bereich anlegen           
                # kommender Eintrag wurde in erzeuge_XML_Eintrag schon erhoeht
                nr = int(root.attrib['kommender_Eintrag']) - 1          
                inhalt = ordinal
                
                self.mb.class_Bereiche.erzeuge_neue_Datei2(nr,inhalt)
                self.mb.class_Bereiche.erzeuge_bereich2(nr,sicht)

                # Zeilen anordnen
                source = ordinal
                target = xml_sel_zeile.tag
                action = 'drunter'  
    
                # in zeilen_neu_ordnen wird auch die xml datei geschrieben
                self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(source,target,action)
                self.korrigiere_scrollbar()

                if self.mb.doc.hasControllersLocked(): 
                    self.mb.doc.unlockControllers()

            except:
                log(inspect.stack,tb())
            StatusIndicator.end()
            
            return nr
            
            
    def kontrolle(self):
        if self.mb.debug: log(inspect.stack)
        
        root2 = self.mb.props[T.AB].xml_tree.getroot()
        alle = root2.findall('.//')
        asd = []
        for i in alle:
            asd.append((i.tag,i.attrib['Lvl'],i.attrib['Sicht'],i))

    
    def in_Papierkorb_einfuegen(self,ordinal):
        '''
        Moeglichkeiten:
        
        Selektierter ist Datei oder Ordner
        Sichtbare(r) ist Datei oder Ordner
        
        
        - Selektierter ist Projektordner oder Papierkorb
            - abbrechen
        
        - Selektierter ist Datei:
            - Selektierter ist in sichtbarem Ordner:
                Selektierten verschieben und Ordner neu selektieren
                
            - Selektierter ist Sichtbarer:
                Auf Nachfolger oder Vorgaenger umschalten, Selektierten verschieben
            - Selektierter ist nicht sichtbar:
                Selektierten verschieben
                
        - Selektierter ist Ordner
            - Sichtbare sind uebergeordneter Ordner
                Selektierten Ordner verschieben und sichtbaren Ordner neu selektieren
            - Sichtbare(r) sind Teilmenge des selektierten Ordners
                Auf Nachfolger oder Vorgaenger des selektierten Ordners umschalten, Ordner verschieben
            - Sichtbare sind nicht im Ordner
                Ordner verschieben
                
        Bei zu loeschenden Dateien oder Ordnern wird auf den Vorgaenger umgeschaltet.
        Wenn kein Vorgaenger existiert, wird ein Nachfolger ausgesucht.
        
        Wenn der Vorgaenger ein Ordner ist und im Ordner keine weitere Datei existiert,
        wird der Ordner und der Papierkrob geschlossen und dann verschoben. Der Papierkorb
        wird danach wieder geoeffnet.
        
        '''
        if self.mb.debug: log(inspect.stack)
        
        props = self.mb.props[T.AB]
        root = props.xml_tree.getroot()
        
        papierkorb = props.Papierkorb
        projektordner = props.Projektordner
        
        if T.AB == 'ORGANON':
            ok = self.existiert_datei_in_anderem_tab(ordinal)
            if not ok:
                return
            
        if ordinal in [papierkorb,projektordner,None]:
            return
        
        
        try:
            def finde_vorgaenger(ordi):
                elems = []
                
                for el in root.iter():
                    if el.tag == ordi:
                        return elems[-1]
                    
                    if 'Sicht' in el.attrib:
                        if el.attrib['Sicht'] == 'ja':
                            elems.append(el.tag)
                    else:
                        elems.append(el.tag)

            def finde_nachfolger_o(ordi):
                parent = root.find( './/{0}/..'.format(ordi) )
                
                childs = [el.tag for el in parent]
                index = childs.index(ordi)
                
                if len(childs) - 1 > index:
                    nachfolger = childs[index + 1]
                    return nachfolger
                else:
                    vorgaenger = finde_vorgaenger(ordi)
                    return vorgaenger

            def finde_nachfolger_ordner(ordi):   
                nachf = finde_nachfolger_o(ordi)
                
                if nachf != papierkorb:
                    return nachf
                else:
                    return finde_vorgaenger(ordi)
            
            
            def finde_vor(ordi):
                vor = finde_vorgaenger(ordi)
                if vor not in ('ORGANON','Tabs'):
                    if vor not in props.dict_ordner:
                        return vor
                    else:
                        nachf = finde_nachfolger_ordner(ordi)
                        if nachf not in props.dict_ordner:
                            return nachf
                        else:
                            self.mb.class_Funktionen.ordner_schliessen(vor,'leer')
                            self.mb.class_Funktionen.ordner_schliessen(papierkorb,'leer')
                            return vor
                else:
                    nachf = finde_nachfolger_ordner(ordi)
                    return nachf
            
            
            #################################################
            # ART DER SICHTBAREN UND DES ORDINALS BESTIMMEN
            sichtbare = [props.dict_bereiche['Bereichsname-ordinal'][s] for s in self.mb.sichtbare_bereiche]
            
            sichtbarer_ordner = None
            if sichtbare[0] in props.dict_ordner:
                sichtbarer_ordner = sichtbare[0]
              
            datei_ist_sichtbar = ordinal in sichtbare
            selektierter_ist_datei = ordinal not in props.dict_ordner
                        
            if not selektierter_ist_datei:
    
                sel_ordner_ist_sichtbar = len( set(props.dict_ordner[ordinal]).intersection(set(sichtbare)) ) > 0
    
                if sel_ordner_ist_sichtbar:
                    zu_loeschender_ordner_ist_uebergeordnet = len(sichtbare) < len(props.dict_ordner[ordinal])
                    sel_ordner_wird_geloescht = ordinal == sichtbarer_ordner
            ##################################################
            
            
            # DATEIEN / ORDNER LOESCHEN
            
            if selektierter_ist_datei: 
                # DATEI
                #print('Datei loeschen.')
                if not datei_ist_sichtbar:
                    #print('Datei nicht sichtbar. Kann verschoben werden')
                    self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(ordinal,papierkorb,'inPapierkorbEinfuegen')
                else:
                    if not sichtbarer_ordner:
                        #print('Nur eine Datei sichtbar, daher umschalten, dann verschieben.')
                        ordi = finde_vor(ordinal)
                        self.selektiere_zeile(ordi)
                        self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(ordinal,papierkorb,'inPapierkorbEinfuegen')
                    else:
                        #print('Datei ist in Ordner {0} sichtbar, daher umschalten und neu selektieren.'.format(sichtbarer_ordner))
                        self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(ordinal,papierkorb,'inPapierkorbEinfuegen')  
                        self.selektiere_zeile(sichtbarer_ordner)
            else:
                # ORDNER
                #print('Ordner loeschen.')
                if sel_ordner_ist_sichtbar:
                    #print('Ordner ist sichtbar')
                    if zu_loeschender_ordner_ist_uebergeordnet:
                        #print('zu_loeschender_ordner_ist_uebergeordnet')
                        ordi = finde_vor(ordinal)
                        self.selektiere_zeile(ordi)
                        self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(ordinal,papierkorb,'inPapierkorbEinfuegen')
                        self.mb.class_Funktionen.projektordner_ausklappen(ordinal=papierkorb, selektiere_zeile=False, ist_papierkorb=True)
                    else:
                        if sel_ordner_wird_geloescht:
                            #print('zu loeschender Ordner ist sichtbarer Ordner')
                            ordi = finde_vor(ordinal)
                            self.selektiere_zeile(ordi)
                            self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(ordinal,papierkorb,'inPapierkorbEinfuegen')
                        else:
                            #print('zu loeschender Ordner ist Teilmenge des sichtbaren Ordners')
                            self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(ordinal,papierkorb,'inPapierkorbEinfuegen')  
                            self.selektiere_zeile(sichtbarer_ordner)
                else:
                    #print('Ordner ist nicht sichtbar. Kann verschoben werden')
                    self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(ordinal,papierkorb,'inPapierkorbEinfuegen')
            
        except:
            log(inspect.stack,tb()) 
            
        return
    
 
    def leere_Papierkorb(self):
        if self.mb.debug: log(inspect.stack)
        
        try:
            self.mb.Listener.remove_VC_selection_listener()  
            props = self.mb.props[T.AB]          
  
            tree = props.xml_tree
            root = tree.getroot()
            C_XML = self.mb.class_XML
    
            papierkorb_xml = root.find(".//" + props.Papierkorb)  
            papierkorb_xml.attrib['Zustand'] = 'zu'
            papierkorb_inhalt1 = []
            C_XML.selbstaufruf = False
            C_XML.get_tree_info(papierkorb_xml,papierkorb_inhalt1)   
            
            papierkorb_inhalt_ordi = [p[0] for p in papierkorb_inhalt1 if p[0] != props.Papierkorb]
            selektierter_ist_im_papierkorb = (props.selektierte_zeile_alt in papierkorb_inhalt_ordi or
                                              props.selektierte_zeile_alt == props.Papierkorb)
            
            if selektierter_ist_im_papierkorb:
                props.dict_ordner[props.Papierkorb] = [props.Papierkorb]
                self.selektiere_zeile(props.Papierkorb)
            
            # Icon setzen
            zeile = self.mb.props[T.AB].Hauptfeld.getControl(props.Papierkorb)
            icon = zeile.getControl('icon')
            icon.Model.ImageURL = KONST.IMG_PAPIERKORB_LEER
            
            # Zeilen im Hauptfeld loeschen
            for ordinal in papierkorb_inhalt_ordi:        
                contr = props.Hauptfeld.getControl(ordinal)               
                contr.dispose()
     
            # Eintraege in XML Tree loeschen
            papierkorb_inhalt = list(papierkorb_xml)
            for verworfene in papierkorb_inhalt:
                papierkorb_xml.remove(verworfene)
             
            if T.AB != 'ORGANON':
                Path = os.path.join(self.mb.pfade['tabs'] , T.AB +'.xml' )
            else:                    
                Path = os.path.join(self.mb.pfade['settings'] , 'ElementTree.xml' )
                 
            self.mb.tree_write(tree,Path)

            # loesche Bereich(e) und Datei(en)
            if T.AB == 'ORGANON':
                self.loesche_Bereiche_und_Dateien(papierkorb_inhalt_ordi,papierkorb_inhalt)
                
            self.erneuere_dict_bereiche()

        except:
            log(inspect.stack,tb())
                    

    def loesche_Bereiche_und_Dateien(self,papierkorb_inhalt_ordi,papierkorb_inhalt):
        if self.mb.debug: log(inspect.stack)
        
        props = self.mb.props[T.AB]
        
        papierkorb_orga_sec = props.dict_bereiche['ordinal'][props.Papierkorb]
        papierkorb_trenner_name = 'trenner' + papierkorb_orga_sec.split('OrganonSec')[1]
        
        if papierkorb_trenner_name in self.mb.doc.TextSections.ElementNames:
            p_trenner = self.mb.doc.TextSections.getByName(papierkorb_trenner_name)
            p_trenner.setPropertyValue('IsProtected',False)
            p_trenner.dispose()
            
        for ordinal in papierkorb_inhalt_ordi:
            
            try:
                # loesche datei ordinal
                Path = os.path.join(self.mb.pfade['odts'], '%s.odt' % ordinal)
                os.remove(Path)
                
                bereichsname = self.mb.props[T.AB].dict_bereiche['ordinal'][ordinal]
                
                # loesche text der Datei im Dokument
                sections = self.mb.doc.TextSections
                sec = sections.getByName(bereichsname) 
                
                # loesche Sidebareintrag
                self.mb.class_Tags.loesche_ordinal_aus_tags(ordinal)
                # loesche plain_txt
                self.mb.class_Bereiche.plain_txt_loeschen(ordinal)
                                    
                # loesche eventuell vorhandene Kind Bereiche
                ch_sections = []
                def get_childs(childs):
                    for i in range (len(childs)):
                        ch_sections.append(childs[i])
                        if childs[i].ChildSections != None:
                            get_childs(childs[i].ChildSections)

                get_childs(sec.ChildSections)
                    
                for child_sec in ch_sections:
                    child_sec.setPropertyValue('IsProtected',False)
                    child_sec.dispose()
                
                trenner_name = 'trenner' + sec.Name.split('OrganonSec')[1]
                
                filelink = sec.FileLink
                filelink.FileURL = ''
                sec.setPropertyValue('FileLink',filelink)
                
                # Loesche Bereich
                sec.IsVisible = True          
                textSectionCursor = self.mb.doc.Text.createTextCursorByRange(sec.Anchor)
                textSectionCursor.setString('')

                sec.setPropertyValue('IsProtected',False)
                sec.dispose()
                
                # sec_helfer wieder auf invisible setzen, damit er nicht geloescht wird
                self.mb.sec_helfer.IsVisible = False
                                    
                # Trenner loeschen
                if trenner_name in self.mb.doc.TextSections.ElementNames:
                    trenner = self.mb.doc.TextSections.getByName(trenner_name)
                    textSectionCursor.gotoRange(trenner.Anchor,True)
                    trenner.setPropertyValue('IsProtected',False)
                    trenner.dispose()
                    textSectionCursor.setString('')
                
                while textSectionCursor.TextSection == None:
                    textSectionCursor.goLeft(1,True)
                    
                textSectionCursor.setString('')
            except:
                log(inspect.stack,tb())
        
    
    def erneuere_dict_bereiche(self):
        if self.mb.debug: log(inspect.stack)
        
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot() 
        alle_Zeilen = root.findall('.//')
                
        # Fuer die Neuordnung des dict_bereiche
        Bereichsname_dict = {}
        ordinal_dict = {}
        Bereichsname_ord_dict = {}
        
        for i in range (len(alle_Zeilen)):
            ordinal = alle_Zeilen[i].tag
            
            Path = os.path.join(self.mb.pfade['odts'] , '%s.odt' % ordinal)  
            
            Bereichsname_dict.update({'OrganonSec'+str(i):Path})
            ordinal_dict.update({ordinal:'OrganonSec'+str(i)})
            Bereichsname_ord_dict.update({'OrganonSec'+str(i):ordinal})
             
        self.mb.props[T.AB].dict_bereiche.update({'Bereichsname':Bereichsname_dict})
        self.mb.props[T.AB].dict_bereiche.update({'ordinal':ordinal_dict})
        self.mb.props[T.AB].dict_bereiche.update({'Bereichsname-ordinal':Bereichsname_ord_dict})
        
    
    def existiert_datei_in_anderem_tab(self,ordinal):
        if self.mb.debug: log(inspect.stack)
        
        for tab in self.mb.props:
            if tab != 'ORGANON':
                
                if tab == T.AB:
                    continue
                
                root = self.mb.props[tab].xml_tree.getroot()
                
                eintrag = root.find('.//' + ordinal)
                if eintrag == None:
                    continue
                
                dateiname = eintrag.attrib['Name']
                Popup(self.mb, 'warning').text = LANG.KANN_NICHT_VERSCHOBEN_WERDEN %(dateiname,tab)
                return False
            
        return True
    
    def selektiere_zeile(self,ordinal, speichern = True):
        if self.mb.debug: log(inspect.stack)
        
        try:
        
            if ordinal not in self.mb.props[T.AB].dict_bereiche['ordinal']:
                Popup(self.mb, 'warning').text = LANG.DATEI_NICHT_IM_TAB
                return
            
            selektierte_zeile = self.mb.props[T.AB].selektierte_zeile_alt

            zeile = self.mb.props[T.AB].Hauptfeld.getControl(ordinal)
            textfeld = zeile.getControl('textfeld')
            
            self.mache_zeile_sichtbar(ordinal, zeile)
            
            # selektierte Zeile einfaerben, ehem. sel. Zeile zuruecksetzen
            ctrl = self.mb.props[T.AB].Hauptfeld.getControl(selektierte_zeile).getControl('textfeld')
            ctrl.Model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
            textfeld.Model.BackgroundColor = KONST.FARBE_AUSGEWAEHLTE_ZEILE 
                        
            # bei bearbeitetem Bereich: speichern  
            if speichern:
                bereichsname_zeile_alt = self.mb.props[T.AB].dict_bereiche['ordinal'][selektierte_zeile]
                self.mb.class_Bereiche.datei_nach_aenderung_speichern(bereichsname_zeile_alt)
                
            self.mb.props[T.AB].selektierte_zeile_alt = ordinal
            self.mb.props[T.AB].selektierte_zeile = ordinal
            self.mb.class_Sidebar.erzeuge_sb_layout()
             
            self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_der_Bereiche(zeilenordinal = ordinal)
            
        except:
            log(inspect.stack,tb())

    
    def mache_zeile_sichtbar(self,ordinal, zeile):
        if self.mb.debug: log(inspect.stack)
        
        try:
            
            
            parents = self.mb.class_XML.get_parents(ordinal)
            for p in parents:
                if p[1].attrib['Zustand'] == 'zu':
                    self.mb.class_Funktionen.projektordner_ausklappen(parents[-1][0],selektiere_zeile=False)
                    break
                
            tabsX = self.mb.tabsX
            win = tabsX.Hauptfelder[T.AB]
            SB = win.getControl('ScrollBar') 
            
            if SB == None:
                return
            
            hf = self.mb.props[T.AB].Hauptfeld
                
            sb_hoehe = SB.Size.Height
            zeile_y = zeile.PosSize.Y + zeile.PosSize.Height + hf.PosSize.Y
            
            diff = 0
            if zeile_y < 0:
                diff = zeile_y - 20
            elif sb_hoehe - zeile_y < 0:
                diff = -(sb_hoehe - zeile_y)
            
            if diff != 0:                
                y = hf.PosSize.Y - diff
                hf.setPosSize(0,y,0,0,2)
                self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_hf_ctrls()
                SB.Value = SB.Value + diff

        except:
            log(inspect.stack())
            
    
        
from com.sun.star.style.ParagraphAdjust import CENTER 
from com.sun.star.awt import XMouseListener,XMouseMotionListener,XFocusListener
from com.sun.star.awt.MouseButton import LEFT as MB_LEFT
from com.sun.star.awt.MouseButton import RIGHT as MB_RIGHT

class Zeilen_Listener (unohelper.Base, XMouseListener,XMouseMotionListener,XFocusListener):
    def __init__(self,ctx,mb):
        if mb.debug: log(inspect.stack)
        self.pfeil = False
        self.ctx = ctx
        self.mb = mb
        # fuer den erzeugten Pfeil
        self.first_time = True
        # beschreibt die Art der Aktion
        self.einfuegen = None
        # fuer das gezogene Textfeld
        self.colored = False        
        self.edit_text = False

        self.dragged = False
        
        self.SFLink = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
        self.SFLink.FilterName = 'writer8'
        self.SFLink2 = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
        self.SFLink2.FilterName = 'writer8'
        
        # nur fuers logging
        self.log_selbstruf = False
              
    def mouseMoved(self,ev):  
        return False
    def mouseExited(self,ev):
        return True
    def mouseEntered(self,ev):
        return False
    
    def mousePressed(self, ev):
        if self.mb.debug: log(inspect.stack)
        
        # Mauslistener starten
        try:
            self.mb.mausrad_an = True
            self.mb.class_Mausrad.starte_mausrad(called_from_treeview=True)
        except:
            log(inspect.stack,tb())
            

        try:
            props = self.mb.props[T.AB]
            # die gesamte Zeile, control (ordinal)
            props.selektierte_zeile = ev.Source.Context.AccessibleContext.AccessibleName
            # control 'textfeld'   
            zeile = ev.Source
            
            # selektierte Zeile einfaerben, ehem. sel. Zeile zuruecksetzen
            zeile.Model.BackgroundColor = KONST.FARBE_AUSGEWAEHLTE_ZEILE 
            if props.selektierte_zeile != props.selektierte_zeile_alt:
                ctrl = props.Hauptfeld.getControl(props.selektierte_zeile_alt).getControl('textfeld')
                ctrl.Model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
            
            # bei bearbeitetem Bereich: speichern  
            if len(self.mb.undo_mgr.AllUndoActionTitles) > 0:
                bereichsname_zeile_alt = props.dict_bereiche['ordinal'][props.selektierte_zeile_alt ]
                self.mb.class_Bereiche.datei_nach_aenderung_speichern(bereichsname_zeile_alt)
                

            props.selektierte_zeile_alt = props.selektierte_zeile
            self.mb.class_Sidebar.erzeuge_sb_layout()
            
            # Bei Doppelclick Zeileneintrag bearbeiten
            if ev.Buttons == MB_LEFT:   
                if ev.ClickCount == 2: 
                    
                    # Projektordner von der Umbenennung ausnehmen
                    root = props.xml_tree.getroot()
                    zeile_xml = root.find('.//' + props.selektierte_zeile_alt )
                    art = zeile_xml.attrib['Art']
                    
                    if art == 'prj':
                        Popup(self.mb, 'info').text = LANG.PROJEKTORDNER_NICHT_UMBENENNBAR
                        return False
                    else:
                        zeile.Model.ReadOnly = False 
                        zeile.Model.BackgroundColor = KONST.FARBE_EDITIERTE_ZEILE
                        self.edit_text = True   
                        return False
            
            return False
        except:
            log(inspect.stack,tb())
            

    def mouseReleased(self, ev):   
        if self.mb.debug: log(inspect.stack)

        try:

            # Sichtbarkeit der Bereiche umschalten
            if self.dragged == False:  
                self.schalte_sichtbarkeit_der_Bereiche()
                   
            else:
                self.dragged = False
            
            # wenn maus gezogen und pfeil erzeugt wurde
            if self.pfeil == True:
                self.pfeil = False
                self.first_time = True
                
                if self.colored:
                    # Farbe gezogenes Textfeld
                    ev.Source.Model.BackgroundColor = self.old_color#16777215 #weiss
                    self.colored = False 
                
                
                s = self.zielordner.getControl('symbol')
    
                if s != None:
                    source = (ev.Source.AccessibleContext.AccessibleParent.AccessibleContext.AccessibleName)
                    target = self.zielordner.AccessibleContext.AccessibleName
                    action = self.einfuegen                          
                    s.dispose()
                    if source != target:
                        self.zeilen_neu_ordnen(source,target,action)   
                        self.mb.class_Baumansicht.korrigiere_scrollbar()  
    
            
        except:
            log(inspect.stack,tb())
            
                           
    def focusGained(self,ev):
        return False  
    
    def focusLost(self, ev):
        if self.mb.debug: log(inspect.stack)
        
        try:
            
            # Listener fuers Mausrad beenden
            self.mb.mausrad_an = False
            
            # Bearbeitung des Zeileneintrags wieder ausschalten
            if self.edit_text == True:
                ev.Source.Model.ReadOnly = True 
                self.edit_text = False
                # neuen Text in die xml Dateien eintragen
                zeile_ord = ev.Source.AccessibleContext.AccessibleParent.AccessibleContext.AccessibleName
                self.aendere_datei_namen(zeile_ord,ev.Source.Text)
        except:
            log(inspect.stack,tb())
            
        return False
    
    
    def aendere_datei_namen(self,zeile_ord,txt):
        if self.mb.debug: log(inspect.stack)
        
        try:
            for tab_name in self.mb.props:
                    
                tree = self.mb.props[tab_name].xml_tree
                root = tree.getroot() 
                
                xml_elem = root.find('.//'+zeile_ord)
                
                if xml_elem != None:
                
                    xml_elem.attrib['Name'] = txt
                    
                    if tab_name == 'ORGANON':
                        Path1 = os.path.join(self.mb.pfade['settings'],'ElementTree.xml')
                    else:
                        Path1 = os.path.join(self.mb.pfade['tabs'],tab_name + '.xml')
                        
                    self.mb.tree_write(tree,Path1)
                    
                    # Textfeld in allen Tabs anpassen
                    if self.mb.props[tab_name].Hauptfeld != None:
                        textfeld = self.mb.props[tab_name].Hauptfeld.getControl(zeile_ord).getControl('textfeld')
                        textfeld.Model.Text = txt
        except:
            log(inspect.stack,tb())
            
    
    

    def mouseDragged(self,ev):
#         if self.mb.debug: log(inspect.stack)
        
        # Papierkorb darf nicht verschoben werden
        ordinal = ev.Source.Context.AccessibleContext.AccessibleName
        if ordinal in (self.mb.props[T.AB].Papierkorb,self.mb.props[T.AB].Projektordner):
            Popup(self.mb, 'info').text = LANG.NICHT_VERSCHIEBBAR
            return

        self.dragged = True
        if self.edit_text == False:
            self.pfeil = True
            X = ev.Source.AccessibleContext.AccessibleParent.PosSize.X + ev.X
            # -1: da icon 24x24, Container aber nur 22 hoch
            Y = ev.Source.AccessibleContext.AccessibleParent.PosSize.Y -1 + ev.Y
            
            self.erzeuge_pfeil(X,Y,ev)
            
            # Textfeld waehrend des Ziehens einfaerben
            if not self.colored:
                self.colored = True
                self.old_color = ev.Source.Model.BackgroundColor
                ev.Source.Model.BackgroundColor = KONST.FARBE_GEZOGENE_ZEILE 
                           
    def erzeuge_pfeil(self,X,Y,ev):
#         if self.mb.debug: log(inspect.stack)
        
        try:        
            if self.pfeil == True:
                if self.first_time == True:
                    self.zielordner,info = self.berechne_pos(Y)
                    zeileY,art,lvl,nachfolger,ord_erster,ordinal = info

                    lvl_nf,art_nf,ord_nf = nachfolger
                    
                    self.first_time = False
                    self.Y = Y

                    # zur Sicherheit - wenn keine Abfrage greift, wird ein falsches Bild dargestellt
                    ImageURL = KONST.IMAGE_GESCHEITERT

                    sourceZeile = ev.Source.AccessibleContext.AccessibleParent.AccessibleContext
                    sourceName = sourceZeile.AccessibleName
                    sourceYPos = sourceZeile.Location.Y

                    sourceArt = self.mb.props[T.AB].dict_zeilen_posY[sourceYPos][4]

                    if sourceArt in ('dir','prj'):
                        subelements = self.mb.props[T.AB].dict_ordner[sourceName]
                    else:
                        subelements = 'quatsch'
                    
                    if sourceArt in ('dir','prj') and ordinal in subelements:
                        ImageURL = KONST.IMAGE_GESCHEITERT
                        self.einfuegen = 'gescheitert'  

                    # Wenn Erster
                    elif ordinal == ord_erster:
                        if zeileY < 10:
                            ImageURL = KONST.IMAGE_PFEIL_HOCH
                            self.einfuegen = 'drueber'
                        elif zeileY < 16:
                            ImageURL = KONST.IMAGE_PFEIL_RECHTS
                            self.einfuegen = 'inOrdnerEinfuegen'
                        else:
                            ImageURL = KONST.IMAGE_PFEIL_RUNTER
                            self.einfuegen = 'drunter'

                    # Wenn 'pg'
                    elif art == 'pg':
                        if lvl_nf < lvl:
                            if zeileY > 15:
                                lvl = lvl_nf
                                self.einfuegen = 'vorNachfolger',ord_nf                               
                            else:
                                self.einfuegen = 'drunter'                                
                        else:
                            self.einfuegen = 'drunter'
                        ImageURL = KONST.IMAGE_PFEIL_RUNTER
                     

                    # Wenn 'dir'
                    elif (art in ('dir','prj')) :
                        if lvl_nf < lvl:
                            if zeileY > 15:
                                lvl = lvl_nf
                                ImageURL = KONST.IMAGE_PFEIL_RUNTER
                                self.einfuegen = 'vorNachfolger',ord_nf                               
                            else:
                                ImageURL = KONST.IMAGE_PFEIL_RECHTS
                                self.einfuegen = 'inOrdnerEinfuegen'                                                   
                        elif art_nf in ('dir','prj'):
                            if zeileY > 15:
                                ImageURL = KONST.IMAGE_PFEIL_RUNTER
                                self.einfuegen = 'drunter'   
                            else:
                                ImageURL = KONST.IMAGE_PFEIL_RECHTS
                                self.einfuegen = 'inOrdnerEinfuegen'                                                             
                        else:
                            ImageURL = KONST.IMAGE_PFEIL_RECHTS
                            self.einfuegen = 'inOrdnerEinfuegen' 
                                                                            
                    # Wenn 'waste'                  
                    elif (art == 'waste') :
                        ImageURL = KONST.IMAGE_PFEIL_RECHTS
                        self.einfuegen = 'inPapierkorbEinfuegen'
                   

                    # Pfeil erstellen
                    Color__Container = 10202
                    Attr = (int(lvl)*16,3,16,16,'eintrag23', Color__Container)    
                    PosX,PosY,Width,Height,Name,Color = Attr
                     
                    control, model = self.mb.createControl(self.ctx,"ImageControl",PosX,PosY,Width,Height,(),() )      
                    model.Border = False                    
                    model.ImageURL = ImageURL
 
                    self.zielordner.addControl("symbol",control)
 
                else:      
                                    
                    if not (self.Y -5 < Y < self.Y+5):   
                        zielordner,info = self.berechne_pos(Y)
                        zeileY,art,lvl,nachfolger,ord_erster,ordinal = info
                        lvl_nf,art_nf,ord_nf = nachfolger
                       
                        if zielordner.AccessibleContext.AccessibleName == ord_erster:

                            self.zielordner.getControl("symbol").dispose()
                            self.first_time = True
                            self.Y = Y 

                        
                        # Code zur Beruhigung der Anzeige - weniger dispose()
                        # self.zielordner wird in first_time == True gesetzt
                        if zielordner == self.zielordner:
                            
                            if art == 'pg':
                                if lvl_nf < lvl:
                                    self.zielordner.getControl("symbol").dispose()
                                    self.first_time = True
                                    self.Y = Y  
                                else:                                    
                                    pass
                            if art in ('dir','prj'):
                                if lvl_nf < lvl:
                                    self.zielordner.getControl("symbol").dispose()
                                    self.first_time = True
                                    self.Y = Y 
                                elif art_nf in ('dir','prj'): 
                                    self.zielordner.getControl("symbol").dispose()
                                    self.first_time = True
                                    self.Y = Y 
                                else:                                    
                                    pass
                            else: 
                                pass                    
                        else:      
                            pfeil = self.zielordner.getControl("symbol")  
                            if pfeil != None:
                                pfeil.dispose()
                                self.first_time = True
                                self.Y = Y  
                    
        except:
            # Der Fehler braucht nicht geloggt zu werden, da er 
            # staendig und folgenlos auftritt
            pass #print(tb())
                
    def berechne_pos(self,Y):
#         if self.mb.debug: log(inspect.stack)
        
        y = ( math_floor( Y / KONST.ZEILENHOEHE ) ) 
        
        ord_papierkorb = self.mb.props['ORGANON'].Papierkorb
        zeile_papierkorb = self.mb.props[T.AB].Hauptfeld.getControl(ord_papierkorb)
        pos_papierkorb = zeile_papierkorb.PosSize.Y / KONST.ZEILENHOEHE

        # abfangen: wenn Mauspos ueber Hauptfeld oder unter Papierkorb hinausgeht
        if y < 0:
            y = 0
        elif y > pos_papierkorb:
            y = pos_papierkorb

        posY = (y * KONST.ZEILENHOEHE)       
        posY_nachf = ((y+1) * KONST.ZEILENHOEHE)
        
        ordinal,parent,text,lvl,art,zustand,sicht,tag1,tag2,tag3 = self.mb.props[T.AB].dict_zeilen_posY[posY]
        ord_erster = self.mb.props[T.AB].dict_zeilen_posY[0][0]
        
        # try/except um nur eine Abfrage an das Dict zu stellen
        try:
            nf = self.mb.props[T.AB].dict_zeilen_posY[posY_nachf]
            # lvl = nf[3]
            # art = nf[4]
            # ord = nf[0]
            nachfolger = (nf[3], nf[4], nf[0])
        except:
            # Papierkorb: Nachfolger ist immer auf hoeherem lvl
            nachfolger = (100, 'keiner', 'sdfsf')
        
        zeileY = Y - posY
        info = (zeileY, art, lvl, nachfolger, ord_erster, ordinal)
        zielordner = self.mb.props[T.AB].Hauptfeld.getControl(ordinal)
         
        return (zielordner,info)
 
           
    def zeilen_neu_ordnen(self,source,target,action,schalte_bereiche=True):
        if self.mb.debug: log(inspect.stack)

        if action != 'gescheitert':
            
            ok = self.wird_datei_in_papierkorb_verschoben(source,target)
            if not ok:
                return

            if 'vorNachfolger' in action:
                # wenn der Nachfolger gleich der Quelle ist, nicht verschieben
                if source == action[1]:
                    return
 
            eintraege = self.xml_neu_ordnen(source,target,action)
            self.posY_in_tv_anpassen(eintraege)
            
            if 'inPapierkorbEinfuegen' in action:
                 
                props = self.mb.props[T.AB]
                tree = props.xml_tree
                root = tree.getroot()
 
                papierk = root.find('.//' + props.Papierkorb)
                 
                if papierk.attrib['Zustand'] == 'zu':
                    for el in papierk.findall('.//'):
                        el.attrib['Sicht'] = 'nein'
                        cont = props.Hauptfeld.getControl(el.tag)
                        cont.setVisible(False)
                        
            # dict_ordner updaten
            self.mb.class_Projekt.erzeuge_dict_ordner()

            # Bereiche neu verlinken
            sections = self.mb.doc.TextSections
            self.verlinke_Bereiche(sections)
            

            # Sichtbarkeit der Bereiche umschalten
            if schalte_bereiche:
                self.schalte_sichtbarkeit_der_Bereiche(action=action)     
            
            if T.AB == 'ORGANON':   
                Path = os.path.join(self.mb.pfade['settings'] , 'ElementTree.xml' )
            else:
                Path = os.path.join(self.mb.pfade['tabs'] , T.AB + '.xml' )
            self.mb.tree_write(self.mb.props[T.AB].xml_tree,Path)
            
            self.schalte_sichtbarkeit_hf_ctrls()
            
            return True

            
                
    def wird_datei_in_papierkorb_verschoben(self,source,target):
        if self.mb.debug: log(inspect.stack)
        
        try:
            if T.AB != 'ORGANON':
                return True
            
            if target != self.mb.props['ORGANON'].Papierkorb:
                return True
                    
            if source in self.mb.props['ORGANON'].dict_ordner:
                ordinale = self.mb.props['ORGANON'].dict_ordner[source]
            else:
                ordinale = source,
            
            
            for ordn in ordinale:
                for tab in self.mb.props:
                    if tab != 'ORGANON':
                        
                        root = self.mb.props[tab].xml_tree.getroot()
                        
                        eintrag = root.find('.//' + ordn)
                        if eintrag == None:
                            continue
                        
                        dateiname = eintrag.attrib['Name']
                        Popup(self.mb, 'warning').text = LANG.KANN_NICHT_VERSCHOBEN_WERDEN %(dateiname,tab)
                        return False
        except:
            log(inspect.stack,tb())
                    
        return True
        
    def posY_in_tv_anpassen(self,eintraege): 
        if self.mb.debug: log(inspect.stack)
        
        props = self.mb.props[T.AB]
        
        # ordnen des dict_zeilen_posY
        props.dict_zeilen_posY = {}
        props.dict_posY_ctrl = {}
        index = 0
        
        for eintrag in eintraege:
            
            ordinal,parent,text,lvl,art,zustand,sicht,tag1,tag2,tag3 = eintrag
            
            if sicht == 'ja':
                # dict_zeilen_posY updaten  
                pos_Y = KONST.ZEILENHOEHE*index         
                props.dict_zeilen_posY.update({pos_Y:eintrag})  
                                            
                # Y_Wert sichtbarer Eintraege setzen
                contr_zeile = props.Hauptfeld.getControl(ordinal)
                props.dict_posY_ctrl.update({pos_Y:contr_zeile})
                                
                # der X-Wert ALLER Eintraege wird in xml_m neu gesetzt
                y = KONST.ZEILENHOEHE*index
                if contr_zeile.PosSize.Y != y:
                    contr_zeile.setPosSize(0,y,0,0,2)# 2: Flag fuer: nur Y Wert aendern
                          
                index += 1  

        
    def xml_neu_ordnen(self,source,target,action):
        if self.mb.debug: log(inspect.stack)
        
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot()
        C_XML = self.mb.class_XML
        target_xml = root.find('.//'+target)
                
        # bei Verschieben in einen geschlossenen Ordner
        if 'inOrdnerEinfuegen' in action and target_xml.attrib['Zustand'] == 'zu':
            target_xml.attrib['Zustand'] = 'auf'
            self.schalte_sichtbarkeit_des_hf(target,target_xml,'zu')
            
            tar_cont = self.mb.props[T.AB].Hauptfeld.getControl(target)
            tar = tar_cont.getControl('icon')
            tar.Model.ImageURL = KONST.IMG_ORDNER_GEOEFFNET_16
        
        
        if 'drunter' in action:
            C_XML.drunter_einfuegen(source,target)
        elif 'inOrdnerEinfuegen' in action:
            C_XML.in_Ordner_einfuegen(source,target)
        elif 'vorNachfolger' in action:
            C_XML.vor_Nachfolger_einfuegen(source,nachfolger = action[1])
        elif 'inPapierkorbEinfuegen' in action:
            C_XML.in_Papierkorb_einfuegen(source,target)
        elif 'drueber' in action:
            C_XML.drueber_einfuegen(source,target)
        
                  
        # bei Verschieben in den Papierkorb
        if 'inPapierkorbEinfuegen' in action and target_xml.attrib['Zustand'] == 'zu':
            
            # dict_ordner muss vorher erneuert werden
            self.mb.class_Projekt.erzeuge_dict_ordner()               
            self.schalte_sichtbarkeit_des_hf(target,target_xml,'auf')
            
        
        eintraege = []
        # selbstaufruf nur fuer den debug
        C_XML.selbstaufruf = False
        C_XML.get_tree_info(root,eintraege)

        return eintraege
        
   
    def schalte_sichtbarkeit_des_hf(self,selbst,selbst_xml,zustand,zeige_projektordner=False,hf_ctrls=True):
        #if self.mb.debug: log(inspect.stack)
        
        props = self.mb.props[T.AB]
        tree = props.xml_tree
        root = tree.getroot()
        
        def durchlaufe_baum(odir):  
            for child in odir:
                #print(child.tag,child.attrib['Name'])
                if child.attrib['Art'] in ('dir','waste','prj'):  
                    #print('wird sichtbar 1', child.attrib['Name'],child.attrib['Zustand'],child.attrib['Parent'])  
                    tar = props.Hauptfeld.getControl(child.tag)
                    tar.Visible = True   
                    
                    elem = root.find('.//'+ child.tag)
                    elem.attrib['Sicht'] = 'ja'
                           
                    if child.attrib['Zustand'] == 'auf':                        
                        durchlaufe_baum(child)
                else:
                    if odir.attrib['Zustand'] == 'auf':
                        #print('wird sichtbar 2', child.attrib['Name'],'pg')
                        tar = props.Hauptfeld.getControl(child.tag)
                        tar.Visible = True           
                        
                        elem = root.find('.//'+ child.tag)
                        elem.attrib['Sicht'] = 'ja'   
        
        if zeige_projektordner:
            selbst_xml.attrib['Zustand'] = 'auf'
            durchlaufe_baum(selbst_xml)
        
        if zustand == 'auf':
            odir = props.dict_ordner[selbst]
            
            for child in odir:
                if child != selbst:
                    tar = props.Hauptfeld.getControl(child)
                    tar.Visible = False
                    elem = root.find('.//'+ child)
                    elem.attrib['Sicht'] = 'nein'
                    #print('wird unsichtbar',elem.attrib['Name'],elem.attrib['Sicht'])
        else:   
            durchlaufe_baum(selbst_xml)
            
        self.positioniere_elemente_im_baum_neu()          
        self.update_dict_zeilen_posY() 
        if T.AB == 'ORGANON':
            path = os.path.join(self.mb.pfade['settings'] , 'ElementTree.xml' )
        else:
            path = os.path.join(self.mb.pfade['tabs'] ,  T.AB + '.xml' )
        tree = props.xml_tree
        self.mb.tree_write(tree,path)
        
        if hf_ctrls:
            self.schalte_sichtbarkeit_hf_ctrls()
        
        
    def schalte_sichtbarkeit_hf_ctrls(self):
        if self.mb.debug: log(inspect.stack)
        
        try:
            props = self.mb.props[T.AB]
            co = props.Hauptfeld.PosSize.Y
            tv = self.mb.win.PosSize.Height
            tableiste = self.mb.tabsX.tableiste.Size
    
            untergrenze = -co - 20
            obergrenze = -co + tv - tableiste.Height - 20
            
            Ys = props.dict_zeilen_posY
    
            for y in Ys:
                if untergrenze < y < obergrenze:
                    props.dict_posY_ctrl[y].setVisible(True)
                else:
                    props.dict_posY_ctrl[y].setVisible(False)
        except:
            log(inspect.stack,tb())
         
        
    def verlinke_Bereiche(self,sections):
        if self.mb.debug: log(inspect.stack)
        
        # langsame und sichere Loesung: es werden alle Bereiche neu verlinkt, 
        # nicht nur die verschobenen
        # NEU UND SCHNELLER: Es werden nur noch sichtbare Bereiche neu verlinkt in: self.verlinke_Sektion

        # Der VC Listener wird von IsVisible ausgeloest,
        # daher wird er vorher ab- und hinterher wieder angeschaltet
        self.mb.Listener.remove_VC_selection_listener() 
                
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot() 
        alle_Zeilen = root.findall('.//')
        
        # Fuer die Neuordnung des dict_bereiche
        Bereichsname_dict = {}
        ordinal_dict = {}
        Bereichsname_ord_dict = {}

        try:
            # Blendet den Papierkorb aus, wenn neuer Bereich eingefuegt wurde
            letzte_zeile = sections.getByIndex(sections.Count - 1)
            letzte_zeile.IsVisible = False   
        except:
            log(inspect.stack,tb())
                
        for i in range (len(alle_Zeilen)):
            ordinal = alle_Zeilen[i].tag
            Path = os.path.join(self.mb.pfade['odts'] , '%s.odt' % ordinal)  
            
            Bereichsname_dict.update({'OrganonSec'+str(i):Path})
            ordinal_dict.update({ordinal:'OrganonSec'+str(i)})
            Bereichsname_ord_dict.update({'OrganonSec'+str(i):ordinal})
            
        self.mb.props[T.AB].dict_bereiche.update({'Bereichsname':Bereichsname_dict})
        self.mb.props[T.AB].dict_bereiche.update({'ordinal':ordinal_dict})
        self.mb.props[T.AB].dict_bereiche.update({'Bereichsname-ordinal':Bereichsname_ord_dict})

        self.mb.Listener.add_VC_selection_listener()         
        
    def get_links(self):
        if self.mb.debug: log(inspect.stack)
        
        odict = {}
        sections = self.mb.doc.TextSections
        names = sections.ElementNames
         
        for name in names:
            if 'OrganonSec' in name:
                sec = sections.getByName(name)

                if sec.FileLink.FileURL != '':
                    odict.update({sec.FileLink.FileURL:sec.Name})
         
        return odict
    
    
    def get_sections(self):
        
        odict = {}
        sections = self.mb.doc.TextSections
        names = sections.ElementNames

        for name in names:
            if 'OrganonSec' in name:
                sec = sections.getByName(name)
                odict.update({name:sec})
        return odict
    
    
    def get_links2(self,sections_uno):
        if self.mb.debug: log(inspect.stack)
        
        try:
            odict = {}
    
            for name in sections_uno:
                sec = sections_uno[name]
                odict.update({sec.FileLink.FileURL:sec.Name})
    
            return odict  
        except:
            log(inspect.stack,tb())     
    
        
    def schalte_sichtbarkeit_der_Bereiche(self,zeilenordinal=None, action=None, add_listener=True):
        if self.mb.debug: log(inspect.stack)

        try:
            props = self.mb.props[T.AB]
            
            # Der VC Listener wird von IsVisible ausgeloest,
            # daher wird er vorher ab- und hinterher wieder angeschaltet
            self.mb.Listener.remove_VC_selection_listener() 

            if zeilenordinal == None:
                if props.selektierte_zeile != None:
                    zeilenordinal = props.selektierte_zeile
                else:
                    return
            
            sections_uno = self.get_sections()
                                   
            # Ordner
            if zeilenordinal in props.dict_ordner:
                zeilen_in_ordner_ordinal = props.dict_ordner[zeilenordinal]
                
                einzublendende = [props.dict_bereiche['ordinal'][z] for z in zeilen_in_ordner_ordinal]
                                
                first_time = True
                self.mb.sec_helfer.IsVisible = True
                
                # Sichtbare ausblenden                
                for bereich in reversed(self.mb.sichtbare_bereiche): 
                    if bereich not in einzublendende:                            
                        sec = sections_uno[bereich]
                        sec.setPropertyValue('IsVisible', False)
                        self.entferne_Trenner(sec)
                                
                # alle Zeilen im Ordner einblenden
                for ordnereintrag_name in einzublendende:
                    #time.sleep(.5)
                    z_in_ordner = sections_uno[ordnereintrag_name]
                    self.verlinke_Sektion(ordnereintrag_name,z_in_ordner,sections_uno)

                    z_in_ordner.IsVisible = True
                    self.mache_Kind_Bereiche_sichtbar(z_in_ordner)
                
                    if first_time:
                        first_time = False
                        self.mb.viewcursor.gotoRange(z_in_ordner.Anchor.Start,False)

                    # Wenn mehr als nur ein geschlossener Ordner zu sehen ist
                    if len(zeilen_in_ordner_ordinal) > 1:
                        # Wenn die Zeile im Papierkorb ist, darf der letzte trenner nicht gezeigt werden, da
                        # er nicht existiert
                        if zeilenordinal in props.dict_ordner[props.Papierkorb]:
                            if ordnereintrag_name != einzublendende[-1]:
                                self.zeige_Trenner(z_in_ordner,zeilenordinal)
                        else:
                            self.zeige_Trenner(z_in_ordner,zeilenordinal)
                    # Wenn der Ordner keine Kinder hat
                    else:
                        self.entferne_Trenner(z_in_ordner)
       
                # sichtbare Bereiche wieder in Prop eintragen
                self.mb.sichtbare_bereiche = [ props.dict_bereiche['ordinal'][b] for b in zeilen_in_ordner_ordinal ]
                
                self.mb.sec_helfer.IsVisible = False
            else:
            # Dateien 
                
                selekt_bereich_name = props.dict_bereiche['ordinal'][zeilenordinal]
                selekt_bereich = self.mb.doc.TextSections.getByName(selekt_bereich_name)
                sichtbare = self.mb.sichtbare_bereiche
                
                if len(sichtbare) > 1:
                    first_section = self.mb.doc.TextSections.getByName(sichtbare[0])
                    try:
                        self.mb.viewcursor.gotoRange(first_section.Anchor.Start,False)
                    except:
                        pass
                
                self.mb.sec_helfer.IsVisible = True
                selekt_bereich.IsVisible = False
                
                self.verlinke_Sektion(selekt_bereich_name,selekt_bereich,sections_uno)
                
                self.mache_Kind_Bereiche_sichtbar(selekt_bereich)
                
                if action != 'lade_projekt':
                    self.entferne_Trenner(selekt_bereich)
                
                selekt_bereich.IsVisible = True 
                              
                for bereich in reversed(self.mb.sichtbare_bereiche):
                    #time.sleep(.5)
                    if bereich != selekt_bereich_name:
                        
                        section = self.mb.doc.TextSections.getByName(bereich)  
                        section.IsVisible = False
                        
                        if action != 'lade_projekt':
                            self.entferne_Trenner(section)

                
                self.mb.viewcursor.gotoRange(selekt_bereich.Anchor.Start,False)
                self.mb.sec_helfer.IsVisible = False
                self.mb.sichtbare_bereiche = [selekt_bereich_name]
                  
            self.mb.loesche_undo_Aktionen()    

            if add_listener:
                self.mb.Listener.add_VC_selection_listener() 

        except:
            log(inspect.stack,tb())
            
    
    def schalte_sichtbarkeit_des_ersten_Bereichs(self):
        if self.mb.debug: log(inspect.stack)

        zeilenordinal =  self.mb.props[T.AB].selektierte_zeile
        sections_uno = self.get_sections()
        
        # Ordner
        if zeilenordinal in self.mb.props[T.AB].dict_ordner:
            zeilen_in_ordner_ordinal = self.mb.props[T.AB].dict_ordner[zeilenordinal][0],
            
            # alle Zeilen im Ordner einblenden
            for z in zeilen_in_ordner_ordinal:
                ordnereintrag_name = self.mb.props[T.AB].dict_bereiche['ordinal'][z]
                z_in_ordner = self.mb.doc.TextSections.getByName(ordnereintrag_name)
                self.verlinke_Sektion(ordnereintrag_name,z_in_ordner,sections_uno)    

            # uebrige noch sichtbare ausblenden
            for bereich in self.mb.sichtbare_bereiche:                        
                bereich_ord = self.mb.props[T.AB].dict_bereiche['Bereichsname-ordinal'][bereich]                     
                if bereich_ord not in zeilen_in_ordner_ordinal:                            
                    sec = self.mb.doc.TextSections.getByName(bereich)
                    sec.IsVisible = False 
                    self.entferne_Trenner(sec)      

    
    def verlinke_Sektion(self,name,bereich,sections_uno):
        if self.mb.debug: log(inspect.stack)
        
        dict_filelinks = self.get_links2(sections_uno)
        
        try:
            url_in_dict = uno.systemPathToFileUrl(self.mb.props[T.AB].dict_bereiche['Bereichsname'][name])
            url_sec = bereich.FileLink.FileURL
            
            if url_in_dict != url_sec:
            
                self.SFLink.FileURL = url_in_dict

                if url_in_dict in dict_filelinks:
                    sec = sections_uno[dict_filelinks[url_in_dict]]
                    
                    empty_file = os.path.join(self.mb.pfade['odts'],'empty_file.odt') 
                    self.SFLink2.FileURL = uno.systemPathToFileUrl(empty_file)
                    sec.setPropertyValue('FileLink',self.SFLink2)

                if url_in_dict != bereich.FileLink.FileURL:
                    bereich.setPropertyValue('FileLink',self.SFLink)

        except:
            log(inspect.stack,tb())
    

    ## NUR ZU TESTZWECKEN ##
    def pruefe_vorkommen(self,url_in_dict,child):  
        dict_filelinks = self.get_links()
        if url_in_dict in dict_filelinks:
            print('url immer noch vorhanden') 

        else:
            print('link nicht vorhanden')
            
        sections = self.mb.doc.TextSections
        names = sections.ElementNames
        
        if child in names:
            sec = sections.getByName(child)
            print(child,'ist in den Sections: als Kind von:', sec.ParentSection.Name)
            
            
            for name in names:
                if 'OrganonSec' in name:
                    sec = sections.getByName(name)
                    time.sleep(0.04)
                    if sec.IsVisible:
                        print(sec.Name,'ist sichtbar')
                    else:
                        print(sec.Name,'ist unsichtbar')
            
        else:
            print(child,'ist nicht in den Sections')
            
    def mache_Kind_Bereiche_sichtbar(self,sec):
        # self.log_selbstruf: um mache_Kind_Bereiche_sichtbar nur
        # 1x zu loggen
        try:
            
            if not self.log_selbstruf:
                if self.mb.debug: log(inspect.stack)

            self.log_selbstruf = True

            for kind in sec.ChildSections:
                kind.setPropertyValue('IsVisible',True)
                
                #print('blende Kind ein:',kind.Name)
                if len(kind.ChildSections) > 0:
                    self.mache_Kind_Bereiche_sichtbar(kind)
            
            self.log_selbstruf = False
        except:
            log(inspect.stack,tb())
            
    
    def zeige_Trenner(self,sec,source_ordinal):  
        if self.mb.debug: log(inspect.stack)

        try:
            trenner_name = 'trenner' + sec.Name.split('OrganonSec')[1]
                        
            sec_ordinal = os.path.basename(sec.FileLink.FileURL).split('.')[0]
            sec_nachfolger_name = 'OrganonSec' + str(int(sec.Name.split('OrganonSec')[1])+1)
            
            if trenner_name in self.mb.doc.TextSections.ElementNames:
                trennerSec = self.mb.doc.TextSections.getByName(trenner_name)
                trennerSec.IsVisible = True
                
                if len(sec.ChildSections) != 0:
                    #trennerSec.BackColor = sec.ChildSections[0].BackColor
                    self.setze_Trenner_Formatierung(trennerSec,sec_nachfolger_name,source_ordinal,sec_ordinal)
                return trennerSec
            
            newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
                     
            newSection.setName(trenner_name)
            newSection.IsProtected = True
            if len(sec.ChildSections) != 0:
                newSection.BackColor = sec.ChildSections[0].BackColor
    
            
            sec_nachfolger = self.mb.doc.TextSections.getByName(sec_nachfolger_name)
            
            sec_text = sec.Anchor.Text
            sec_nachfolger_text = sec_nachfolger.Anchor.Text

            cur = None
            
            if sec_text != sec_nachfolger_text:
                # Vor einer Tabelle
                enum = sec_nachfolger.Anchor.createEnumeration()
                
                cont = []
                while enum.hasMoreElements():
                    cont.append(enum.nextElement())
                
                texts = []
                for i in range(len(cont)):
                    texts.append((i,cont[i].Anchor.Text))
                    
                    if cont[i].Anchor.Text == sec_text:
                        cur = cont[i].Anchor.Text.createTextCursor()
                        cur.gotoRange(cur.TextSection.Anchor.Start,False) 
            else:    
                cur = sec_nachfolger.Anchor.Text.createTextCursor()
                cur.gotoRange(sec_nachfolger.Anchor,False)
                cur.gotoRange(cur.TextSection.Anchor.Start,False)     
                
            if cur == None:
                # Nach einer Tabelle
                cur = sec_nachfolger.Anchor.Text.createTextCursor()
                cur.gotoRange(sec_nachfolger.Anchor,False)
                cur.gotoRange(cur.TextSection.Anchor.Start,False) 
                sec = sec_nachfolger  
                
            try:
                sec.Anchor.End.Text.insertTextContent(cur, newSection, False)
                
                cur.goLeft(1,False)
                cur.ParaStyleName = 'Standard'
                cur.PageDescName = ""
                
                self.setze_Trenner_Formatierung(newSection,sec_nachfolger_name,source_ordinal,sec_ordinal)
            except:
                log(inspect.stack,tb())
                

            return newSection
        except:
            log(inspect.stack,tb())
            
            
    def setze_Trenner_Formatierung(self,sec_trenner,sec_nachfolger_name,source_ordinal,sec_ordinal):  
        if self.mb.debug: log(inspect.stack)
        try:
            nachfolger_ordinal = self.mb.props[T.AB].dict_bereiche['Bereichsname-ordinal'][sec_nachfolger_name]
    
            if nachfolger_ordinal == self.mb.props[T.AB].Papierkorb:
                sec_trenner.setPropertyValue('BackGraphicURL','')
                sec_trenner.Anchor.setString('')
                return
                    
            tree = self.mb.props[T.AB].xml_tree
            root = tree.getroot()
            nachfolger_xml = root.find('.//'+nachfolger_ordinal)
            source_xml = root.find('.//'+source_ordinal)
            sec_xml = root.find('.//'+sec_ordinal)
            
            
            def get_dateiname():
                lvl = sec_xml.attrib['Lvl']
                list_root = root.findall('.//')
                anz = len(list_root)
                ind = list_root.index(sec_xml)+1
    
                i = range(ind,anz)
                if anz == ind:
                    return
                for i in range(ind,anz):
                    if list_root[i].attrib['Lvl'] <= lvl:
                        name = list_root[i].attrib['Name']
                        return name
                return '?'
    
            if int(nachfolger_xml.attrib['Lvl']) <= int(source_xml.attrib['Lvl']):
                sec_trenner.setPropertyValue('BackGraphicURL','')
                sec_trenner.Anchor.setString('')
                sec_trenner.Anchor.ParaBackColor = -1
                return
            
            sett_trenner = self.mb.settings_orga['trenner']
            trenner_format = sett_trenner['trenner']
    
            if trenner_format == 'farbe':
                
                if sec_xml.attrib['Zustand'] == 'zu':
                    datei_name = get_dateiname()
                else:
                    datei_name = nachfolger_xml.attrib['Name']
                sec_trenner.Anchor.setString(datei_name)
                sec_trenner.Anchor.ParaAdjust = CENTER
                sec_trenner.Anchor.ParaBackColor = KONST.FARBE_TRENNER_HINTERGRUND
                sec_trenner.Anchor.CharColor = KONST.FARBE_TRENNER_SCHRIFT 
                
                sec_trenner.setPropertyValue('BackGraphicURL','')

            elif trenner_format == 'strich':
                bgl = sec_trenner.BackGraphicLocation
                bgl.value = 'MIDDLE_BOTTOM'
                 
                KONST.URL_TRENNER = 'vnd.sun.star.extension://xaver.roemers.organon/img/trenner.png'
                sec_trenner.Anchor.setString('')
                sec_trenner.setPropertyValue('BackGraphicURL',KONST.URL_TRENNER)
                sec_trenner.setPropertyValue("BackGraphicLocation", bgl)
            
            elif trenner_format == 'keiner':
                sec_trenner.Anchor.setString('')
                sec_trenner.setPropertyValue('BackGraphicURL','')
            
            elif trenner_format == 'user':
                sec_trenner.Anchor.setString('')
                sec_trenner.setPropertyValue('BackGraphicURL',sett_trenner['trenner_user_url'])
        except:
            log(inspect.stack,tb())
            
                
    def entferne_Trenner(self,sec):
        if self.mb.debug: log(inspect.stack)
        
        trenner_name = 'trenner' + sec.Name.split('OrganonSec')[1]

        try:
            if trenner_name not in self.mb.doc.TextSections.ElementNames:
                return
            trenner = self.mb.doc.TextSections.getByName(trenner_name)
            trenner.setPropertyValue('IsVisible',False)
            if trenner.IsVisible:
                trenner.IsVisible = False
        except:
            log(inspect.stack,tb())
                
        
    def update_dict_zeilen_posY(self):
        if self.mb.debug: log(inspect.stack)
        
        props = self.mb.props[T.AB]
        
        tree = props.xml_tree
        root = tree.getroot()
        C_XML = self.mb.class_XML
           
        eintraege = []
        C_XML.selbstaufruf = False
        C_XML.get_tree_info(root,eintraege)
        props.dict_zeilen_posY = {}
        props.dict_posY_ctrl = {}
 
        i = 0
        for eintrag in eintraege:
            ordinal,parent,name,lvl,art,zustand,sicht,tag1,tag2,tag3 = eintrag  
            if sicht == 'ja':
                pos_Y = i*KONST.ZEILENHOEHE
                props.dict_zeilen_posY.update({ pos_Y : eintrag})
                ctrl = props.Hauptfeld.getControl(ordinal)
                props.dict_posY_ctrl.update({ pos_Y : ctrl})
                i += 1
        
        
    def positioniere_elemente_im_baum_neu(self):
        if self.mb.debug: log(inspect.stack)
        
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot()

        alle_sichtbaren = root.findall(".//*[@Sicht='ja']")
        self.mb.props[T.AB].dict_posY_ctrl = {}
        
        index = 0
        for elem in alle_sichtbaren:
            zeile = self.mb.props[T.AB].Hauptfeld.getControl(elem.tag)
            
            pos_Y = index * KONST.ZEILENHOEHE            
            zeile.setPosSize(0, pos_Y, 0, 0, 2)
            index += 1
            
    def disposing(self,ev):
        return False
            
            
class TreeView_Symbol_Listener (unohelper.Base, XMouseListener):
    
    def __init__(self,ctx,mb):
        if mb.debug: log(inspect.stack)
        self.ctx = ctx
        self.mb = mb
        
    def disposing(self,ev):
        return False

    def mousePressed(self, ev):
        if self.mb.debug: log(inspect.stack)
        
        ordinal = ev.Source.Context.Model.Text
        ist_ordner = ordinal in self.mb.props['ORGANON'].dict_ordner
        
        if ev.Buttons == MB_RIGHT:
            self.menu_rightclick(ev,ist_ordner,ordinal)

        
        if ev.Buttons == MB_LEFT and ist_ordner:    
            if ev.ClickCount == 2: 
                
                try:
                    props = self.mb.props[T.AB]
                    selektierter = props.selektierte_zeile_alt
                    props.selektierte_zeile = ordinal
                    umschalten = False
                    
                    tree = props.xml_tree
                    root = tree.getroot()
                    ordinal_xml = root.find('.//' + ordinal)
                    zustand = ordinal_xml.attrib['Zustand']
                    
                    if zustand == 'zu':
                        ordinal_xml.attrib['Zustand'] = 'auf'
                        if ordinal_xml.attrib['Art'] in ('dir','prj'):
                            ev.Source.Model.ImageURL = KONST.IMG_ORDNER_GEOEFFNET_16
                        if ordinal_xml.attrib['Art'] == 'waste':
                            ev.Source.Model.ImageURL = KONST.IMG_PAPIERKORB_GEOEFFNET
                                                    
                    else:
                        ordinal_xml.attrib['Zustand'] = 'zu'
                        if ordinal_xml.attrib['Art'] in ('dir','prj'):
                            bild_ordner = KONST.IMG_ORDNER_16
                            childs = list(ordinal_xml)
                            if len(childs) > 0:
                                bild_ordner = KONST.IMG_ORDNER_VOLL_16
                            ev.Source.Model.ImageURL = bild_ordner
                        if ordinal_xml.attrib['Art'] == 'waste':
                            ev.Source.Model.ImageURL = KONST.IMG_PAPIERKORB_LEER
                                                
                        if selektierter in props.dict_ordner[ordinal]:
                            umschalten = True
                        
                            
                    self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_des_hf(ordinal,ordinal_xml,zustand,hf_ctrls=False)
                    self.mb.class_Projekt.erzeuge_dict_ordner() 
                    self.mb.class_Baumansicht.korrigiere_scrollbar()
                    self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_hf_ctrls()
                    
                    if umschalten:
                        self.mb.class_Baumansicht.selektiere_zeile(ordinal)
                    
                except:
                    log(inspect.stack,tb())
                
            return False
        
    def mouseReleased(self,ev):
        return False
    def mouseExited(self,ev):
        return False
    def mouseEntered(self,ev):
        return False
    
    def menu_rightclick(self,ev,ist_ordner,ordinal):
        if self.mb.debug: log(inspect.stack)
        
        try:

            papierkorb = self.mb.props[T.AB].Papierkorb
            projektordner = self.mb.props[T.AB].Projektordner

            controls = []
            maus_listener = Symbol_Popup_Mouse_Listener(self.mb,ordinal)
            
            if ordinal == papierkorb:
                prop_names = ('Label',)
                prop_values = (LANG.PAPIERKORB_LEEREN,)
                control, model = self.mb.createControl(self.mb.ctx, "FixedText", 0, 0, 0,0, prop_names, prop_values)
                control.addMouseListener(maus_listener)
                controls.append(control)
            else:
            
                # IN PAPIERKORB VERSCHIEBEN
                if ordinal not in(papierkorb,projektordner):
                    prop_names = ('Label',)
                    prop_values = (LANG.IN_PAPIERKORB_VERSCHIEBEN,)
                    control, model = self.mb.createControl(self.mb.ctx, "FixedText", 0, 0, 0,0, prop_names, prop_values)
                    control.addMouseListener(maus_listener)
                    controls.append(control)
                
                # PROJEKTORDNER AUSKLAPPEN
                if ist_ordner:
                    if ordinal != papierkorb:
                        prop_names = ('Label',)
                        prop_values = (LANG.ORDNER_AUSKLAPPEN,)
                        control, model = self.mb.createControl(self.mb.ctx, "FixedText", 0, 0, 0,0, prop_names, prop_values)
                        control.addMouseListener(maus_listener)
                        controls.append(control)
                
            b = 0
            h = 0
            
            for ctrl in controls:
                breite,hoehe = self.mb.kalkuliere_und_setze_Control(ctrl)
                if breite > b:
                    b = breite
                
                ctrl.setPosSize(30,h+5,breite+10,0,7)
                h += hoehe
            
            if len(controls) == 0:
                return
            
            # SEPERATOR
            control, model = self.mb.createControl(self.mb.ctx, "FixedLine", 20, 5, 5,h,(),())
            model.Orientation = 1
            controls.append(control)

            x,y = self.mb.class_Tools.get_mausposition(ev)
            posSize = x, y, b + 50, h + 10
            
            # Fenster erzeugen
            win,cont = self.mb.class_Fenster.erzeuge_Dialog_Container(posSize,1+16)
            
            # Listener fuers Dispose des Fensters
            from menu_bar import Schliesse_Menu_Listener
            listener = Schliesse_Menu_Listener(self.mb)
            cont.addMouseListener(listener) 
            listener.ob = win
            

            cont.Model.BorderColor = 16580864
            
            maus_listener.window = win
            
            for ctrl in controls:
                cont.addControl(ctrl.Model.Label,ctrl)
        except:
            log(inspect.stack,tb())

            
class Symbol_Popup_Mouse_Listener (unohelper.Base, XMouseListener):
    
    def __init__(self,mb,ordinal):
        if mb.debug: log(inspect.stack)
        self.mb = mb
        self.window = None
        self.ordinal = ordinal
    
    
    def mouseReleased(self, ev):
        if self.mb.debug: log(inspect.stack)
          
        # Der Listener wird ansonsten vom Mouserelease ebenfalls ausgeloest
        label = ev.Source.Text
        
        if label == LANG.ORDNER_AUSKLAPPEN:
            self.mb.class_Funktionen.projektordner_ausklappen(self.ordinal)
        
        if label == LANG.IN_PAPIERKORB_VERSCHIEBEN:
            self.mb.class_Baumansicht.in_Papierkorb_einfuegen(self.ordinal)
            
        if label == 'Papierkorb leeren':
            self.mb.class_Baumansicht.leere_Papierkorb()   

        self.window.dispose()
        
        return False
                        
    def mouseEntered(self,ev):
        ev.value.Source.Model.FontWeight = 150
        return False
    def mouseExited(self,ev):
        ev.value.Source.Model.FontWeight = 100
        return False
    def mousePressed(self, ev): 
        return False
    def disposing(self,ev):
        return False

class Tag1_Listener (unohelper.Base, XMouseListener):
    
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)
        self.mb = mb
        
    def mousePressed(self, ev):
        if self.mb.debug: log(inspect.stack)
        if ev.Buttons == MB_LEFT and ev.ClickCount == 2 or ev.Buttons == MB_RIGHT: 
            ord_source = ev.Source.AccessibleContext.AccessibleParent.AccessibleContext.AccessibleName 
            X,Y = self.mb.class_Tools.get_mausposition(ev)
            self.mb.class_Funktionen.erzeuge_Tag1_Container(ord_source,X,Y)
        return False
       
    def mouseEntered(self,ev):
        return False
    def mouseExited(self,ev):
        return False
    def disposing(self,ev):
        return False
    
class Tag2_Listener (unohelper.Base, XMouseListener):
    
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)
        self.mb = mb
        
    def mousePressed(self, ev):
        if self.mb.debug: log(inspect.stack)
        if ev.Buttons == MB_LEFT and ev.ClickCount == 2 or ev.Buttons == MB_RIGHT:  
            ordinal = ev.Source.Context.AccessibleContext.AccessibleName  
            X,Y = self.mb.class_Tools.get_mausposition(ev)
            self.mb.class_Funktionen.erzeuge_Tag2_Container(ordinal,X,Y-60)
                
    def mouseEntered(self,ev):
        return False
    def mouseExited(self,ev):
        return False
    def mouseReleased(self,ev):
        return False
    def disposing(self,ev):
        return False


    
  
