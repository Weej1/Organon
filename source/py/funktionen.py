# -*- coding: utf-8 -*-

import unohelper
from math import sqrt
from shutil import copyfile
import json
from collections import OrderedDict

class Funktionen():
    
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)
        self.mb = mb   
        
        items = OrderedDict((
                    ('leer' , LANG.LEER),
                    ('blau' , LANG.BLAU),
                    ('braun' , LANG.BRAUN),
                    ('creme' , LANG.CREME),
                    ('gelb' , LANG.GELB),
                    ('grau' , LANG.GRAU),
                    ('gruen' , LANG.GRUEN),
                    ('hellblau' , LANG.HELLBLAU),
                    ('hellgrau' , LANG.HELLGRAU),
                    ('lila' , LANG.LILA),
                    ('ocker' , LANG.OCKER),
                    ('orange' , LANG.ORANGE),
                    ('pink' , LANG.PINK),
                    ('rostrot' , LANG.ROSTROT),
                    ('rot' , LANG.ROT),
                    ('schwarz' , LANG.SCHWARZ),
                    ('tuerkis' , LANG.TUERKIS),
                    ('weiss' , LANG.WEISS)
                      )) 
        
        self.color_items = ('leer',
                            'creme',
                            'gelb',
                            'gruen',
                            'tuerkis',
                            'hellblau',
                            'blau',                            
                            'orange',
                            'ocker',
                            'rot',
                            'pink',
                            'lila',
                            'rostrot',
                            'braun',
                            'weiss',
                            'hellgrau',
                            'grau',
                            'schwarz',
                            )
        
        self.items = OrderedDict( ( items[k] , k ) for k in self.color_items )
        
         
    def projektordner_ausklappen(self, ordinal=None, selektiere_zeile=True,ist_papierkorb=False):
        if self.mb.debug: log(inspect.stack)
        
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot()
        
        if ordinal == None:
            xml_projekt = root.find(".//*[@Name='%s']" % self.mb.projekt_name)
            alle_elem = xml_projekt.findall('.//')
            ordinal = xml_projekt.tag
        else:
            xml_projekt = root.find(".//%s" % ordinal)
            alle_elem = xml_projekt.findall('.//')


        projekt_zeile = self.mb.props[T.AB].Hauptfeld.getControl(xml_projekt.tag)
        icon = projekt_zeile.getControl('icon')
        
        if ist_papierkorb:
            icon.Model.ImageURL = KONST.IMG_PAPIERKORB_GEOEFFNET
        else:
            icon.Model.ImageURL = KONST.IMG_ORDNER_GEOEFFNET_16
        
        for zeile in alle_elem:
            zeile.attrib['Sicht'] = 'ja'
            if zeile.attrib['Art'] in ('dir','prj'):
                zeile.attrib['Zustand'] = 'auf'
                hf_zeile = self.mb.props[T.AB].Hauptfeld.getControl(zeile.tag)
                icon = hf_zeile.getControl('icon')
                icon.Model.ImageURL = KONST.IMG_ORDNER_GEOEFFNET_16
                
        
        self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_des_hf(xml_projekt.tag,xml_projekt,'zu',True)
        self.mb.class_Projekt.erzeuge_dict_ordner() 
        self.mb.class_Baumansicht.korrigiere_scrollbar()   
        if selektiere_zeile:
            self.mb.class_Baumansicht.selektiere_zeile(ordinal)
         
        if T.AB == 'ORGANON':
            Path = os.path.join(self.mb.pfade['settings'], 'ElementTree.xml')
        else:
            Path = os.path.join(self.mb.pfade['tabs'] , T.AB +'.xml' )
        self.mb.tree_write(self.mb.props[T.AB].xml_tree,Path)

    
    def ordner_schliessen(self,ordinal,bild=None):
        if self.mb.debug: log(inspect.stack)
        
        try:
            props = self.mb.props[T.AB]
            props.selektierte_zeile = ordinal
            
            tree = props.xml_tree
            root = tree.getroot()
            ordinal_xml = root.find('.//' + ordinal)                

            ordinal_xml.attrib['Zustand'] = 'zu'
            
            if bild == None:
                bild_ordner = KONST.IMG_ORDNER_16
                childs = list(ordinal_xml)
                if len(childs) > 0:
                    bild_ordner = KONST.IMG_ORDNER_VOLL_16
            else:
                bild_ordner = KONST.IMG_ORDNER_16
                
            zeile = props.Hauptfeld.getControl(ordinal)
            model = zeile.getControl('icon').Model
            model.ImageURL = bild_ordner
            
            if ordinal_xml.attrib['Art'] == 'waste':
                model.ImageURL = KONST.IMG_PAPIERKORB_LEER
                
            self.mb.class_Baumansicht.selektiere_zeile(ordinal)
   
            self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_des_hf(ordinal,ordinal_xml,'auf',hf_ctrls=False)
            self.mb.class_Projekt.erzeuge_dict_ordner() 
            self.mb.class_Baumansicht.korrigiere_scrollbar()
            self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_hf_ctrls()
            
            self.mb.class_Baumansicht.selektiere_zeile(ordinal)
            
            if T.AB == 'ORGANON':
                Path = os.path.join(self.mb.pfade['settings'], 'ElementTree.xml')
            else:
                Path = os.path.join(self.mb.pfade['tabs'] , T.AB +'.xml' )
            self.mb.tree_write(self.mb.props[T.AB].xml_tree,Path)
        
        except:
            log(inspect.stack,tb())
                    
                    
    def erzeuge_Tag1_Container(self,ord_source,X,Y,window_parent=None):
        if self.mb.debug: log(inspect.stack)

        Width = KONST.BREITE_TAG1_CONTAINER
        Height = KONST.HOEHE_TAG1_CONTAINER
        
        posSize = X,Y,Width,Height 
        flags = 1+16+32+128

        fenster,fenster_cont = self.mb.class_Fenster.erzeuge_Dialog_Container(posSize,Flags=flags,parent=window_parent)

        # create Listener
        listener = Tag_Container_Listener()
        fenster_cont.addMouseListener(listener) 
        listener.ob = fenster  

        self.erzeuge_ListBox_Tag1(fenster, fenster_cont,ord_source,window_parent)
            
    def erzeuge_ListBox_Tag1(self,window,cont,ord_source,window_parent):
        if self.mb.debug: log(inspect.stack)
        
        control, model = self.mb.createControl(self.mb.ctx, "ListBox", 4 ,  4 , 
                                       KONST.BREITE_TAG1_CONTAINER -8 , KONST.HOEHE_TAG1_CONTAINER -8 , (), ())   
        control.setMultipleMode(False)
        model.Border = 0
        model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
        
        try:       
            control.addItems(tuple(self.items.keys()), 0)           
            
            for pos,item in enumerate(self.color_items):
                model.setItemImage(pos, KONST.URL_IMGS + 'punkt_%s.png' %item)
            
            tag_item_listener = Tag1_Item_Listener(self.mb,window,ord_source)
            tag_item_listener.window_parent = window_parent
                
            control.addItemListener(tag_item_listener)
            
            cont.addControl('Eintraege_Tag1', control)
        except:
            log(inspect.stack,tb())
        
            
    def erzeuge_Tag2_Container(self,ordinal,X,Y,window_parent=None):
        if self.mb.debug: log(inspect.stack)
        try:
            
            controls = []
            icons_gallery,icons_prj_folder = self.get_icons()

            # create Listener
            listener = Tag_Container_Listener()
            listener2 = Tag2_Images_Listener(self.mb)
            listener2.ordinal = ordinal
            listener2.icons_dict = {}
            listener2.window_parent = window_parent
            
            y = 10
            x = 0            
            
            control, model = self.mb.createControl(self.mb.ctx, "FixedText", 10,y,200, 20, (), ())  
            model.Label = 'Kein Icon:'
            model.FontWeight = 150
            width,h = self.mb.kalkuliere_und_setze_Control(control,'w')
            controls.append(control)

            control, model = self.mb.createControl(self.mb.ctx, "ImageControl", 20 + width,y,18, 18, (), ())  
            model.ImageURL = ''
            model.setPropertyValue('HelpText','Kein Icon')
            model.setPropertyValue('Border',1)
            control.addMouseListener(listener2) 
                            
            controls.append(control)
            
            y += 25
            
            control, model = self.mb.createControl(self.mb.ctx, "FixedText", 10,y,200, 20, (), ())  
            model.Label = 'Im Projekt verwendete Icons:'
            model.FontWeight = 150
            prefW,h = self.mb.kalkuliere_und_setze_Control(control,'w')
            controls.append(control)
            
            y += 25
            
            anzahl = sqrt(len(icons_prj_folder))

            for iGal in icons_prj_folder:
                control, model = self.mb.createControl(self.mb.ctx, "ImageControl", x +10,y,16, 16, (), ())  

                model.ImageURL = iGal[1]
                model.setPropertyValue('HelpText',iGal[0])
                model.setPropertyValue('Border',0)
                model.setPropertyValue('ScaleImage' ,True)
                control.addMouseListener(listener2) 
                listener2.icons_dict.update({iGal[0]:iGal[1]})
                
                controls.append(control)
                
                x += 25
                
                if x > anzahl * 25:
                    y += 25
                    x = 0
            
            y += 25
            
            control, model = self.mb.createControl(self.mb.ctx, "FixedText", 10,y,200, 20, (), ())  
            model.Label = 'In der Galerie vorhandene Icons:'
            model.FontWeight = 150
            prefW1,h = self.mb.kalkuliere_und_setze_Control(control,'w')
            controls.append(control)
            
            y += 25
            x = 0
            anzahl2 = sqrt(len(icons_gallery))
            
            
            for iGal in icons_gallery:
                control, model = self.mb.createControl(self.mb.ctx, "ImageControl", x +10,y,16, 16, (), ())  

                model.ImageURL = iGal[1]
                model.setPropertyValue('HelpText',iGal[0])
                model.setPropertyValue('Border',0)
                model.setPropertyValue('ScaleImage' ,True)
                control.addMouseListener(listener2) 
                                
                controls.append(control)
                
                x += 25
                
                if x > anzahl2 * 25:
                    y += 25
                    x = 0

            breite = sorted( (prefW, prefW1, int(anzahl) * 25, int(anzahl2) *25 ) )[-1]

            posSize = X, Y, breite + 20, y +25 
            flags = 1 + 16 + 32 + 128

            fenster,fenster_cont = self.mb.class_Fenster.erzeuge_Dialog_Container(posSize,flags,parent=window_parent)
            fenster_cont.addMouseListener(listener) 
            listener.ob = fenster  
            
            for control in controls:
                fenster_cont.addControl('wer',control)
            
            listener2.win = fenster
            
        except:
            log(inspect.stack,tb())
            
            
            
    def get_icons(self):
        if self.mb.debug: log(inspect.stack)
        
        try:
            icons_gallery = []
            icons_prj_folder = []
            icons_prj_folder_names = []
                
            icons_folder = self.mb.pfade['icons']
                        
            for root, dirs, files in os.walk(icons_folder):
                for f in files:
                    name = f
                    path = os.path.join(root,f)
                    path2 = uno.systemPathToFileUrl(path)
                    icons_prj_folder.append((name,path2))
                    icons_prj_folder_names.append(name)
            
            gallery = self.mb.createUnoService("com.sun.star.gallery.GalleryThemeProvider")
            org = gallery.getByName('Organon Icons')

            for i in range(org.Count):
                url = org.getByIndex(i).URL
                
                if os.path.basename(url) not in icons_prj_folder_names:
                    url_os = uno.fileUrlToSystemPath(url)
                    name = os.path.basename(url_os).split('.')[0]
                    icons_gallery.append((name,url))
            
            
            return icons_gallery, icons_prj_folder 

        except:
            log(inspect.stack,tb())
        
        
    def find_parent_section(self,sec):
        if self.mb.debug: log(inspect.stack)
        
        def find_parsection(section):
            
            if section == None:
                # Diese Bedingung wird nur bei einem Fehler durchlaufen, dann naemlich
                # wenn der Bereich 'OrgInnerSec' faelschlich umbenannt wurde.
                # Diese Bedingung soll sicherstellen, dass die Funktion auf jeden Fall funktioniert
                return self.parsection
            
            elif 'OrgInnerSec' not in section.Name:
                find_parsection(section.ParentSection)
            else:
                self.parsection = section
                
        find_parsection(sec)
        
        return self.parsection
    
    def teile_text(self):
        if self.mb.debug: log(inspect.stack)
        
        try:

            zeilenordinal =  self.mb.props[T.AB].selektierte_zeile    
            kommender_eintrag = self.mb.props['ORGANON'].kommender_Eintrag
            
            url_source = os.path.join(self.mb.pfade['odts'],zeilenordinal + '.odt')
            URL_source = uno.systemPathToFileUrl(url_source)
            helfer_url = URL_source+'helfer'
             
            vc = self.mb.viewcursor
            go_left = vc.isAtStartOfLine()
            go_right = vc.isAtEndOfLine()
            cur_old = self.mb.doc.Text.createTextCursor()
            sec = vc.TextSection
            text = self.mb.doc.Text
            
            # parent section finden   
            parsection = self.find_parent_section(sec)
            
            # Bookmark setzen
            bm = self.mb.doc.createInstance('com.sun.star.text.Bookmark')
            bm_name = 'kompliziertkompliziert' + zeilenordinal 
            bm.Name = bm_name
            
            if bm_name in self.mb.doc.Bookmarks.ElementNames:
                zu_loeschendes_bm = self.mb.doc.Bookmarks.getByName(bm_name)
                zu_loeschendes_bm.dispose()
                    
            text.insertTextContent(vc,bm,False)
            
            # neuen dateinamen herausfinden
            cur_text = self.mb.doc.Text.createTextCursor()
            cur_text.gotoRange(bm.Anchor,False)
            cur_text.goRight(60,True)
            neuer_Name = cur_text.String.split('\n')[0].strip()
            
            # alte Datei in Helferdatei speichern
            orga_sec_name_alt = self.mb.props['ORGANON'].dict_bereiche['ordinal'][zeilenordinal]
            self.mb.class_Bereiche.datei_nach_aenderung_speichern(orga_sec_name_alt, anderer_pfad = helfer_url)
             
            # erzeuge neue Zeile
            nr_neue_zeile = self.mb.class_Baumansicht.erzeuge_neue_Zeile('dokument',neuer_Name)
            if nr_neue_zeile == None:
                return
            ordinal_neue_zeile = 'nr'+ str(nr_neue_zeile)
       
            # neue datei unsichtbar oeffnen        
            prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop.Name = 'Hidden'
            prop.Value = True

            url_target = os.path.join(self.mb.pfade['odts'],ordinal_neue_zeile + '.odt')
            URL_target = uno.systemPathToFileUrl(url_target)
               
            doc_new = self.mb.doc.CurrentController.Frame.loadComponentFromURL(helfer_url,'_blank',0,(prop,))  
            cur_new = doc_new.Text.createTextCursor()
            
            # OrgInnerSec umbenennen
            new_OrgInnerSec_name = 'OrgInnerSec' + str(kommender_eintrag)
            sec = doc_new.TextSections.getByName(parsection.Name)
            sec.setName(new_OrgInnerSec_name)
            
            # Textanfang und Bookmark in Datei loeschen 
            bms = doc_new.Bookmarks
            bm2 = bms.getByName('kompliziertkompliziert' + zeilenordinal)
            new_OrgInnerSec = doc_new.TextSections.getByName(new_OrgInnerSec_name)
            
            cur_new.gotoRange(bm2.Anchor,False)
            if go_right:
                cur_new.goRight(1,False)
            cur_new.gotoRange(new_OrgInnerSec.Anchor.Start,True)
            cur_new.setString('')
            bm2.dispose()
            
            # alte datei ueber neue speichern
            doc_new.storeToURL(URL_target,())
            doc_new.close(False)
            
            # Helfer loeschen
            os.remove(uno.fileUrlToSystemPath(helfer_url))
            
            # Ende in der getrennten Datei loeschen
            cur_old.gotoRange(bm.Anchor,False)
            if go_left:
                cur_old.goLeft(1,False)
            cur_old.gotoRange(self.parsection.Anchor.End,True)
            cur_old.setString('')
            
            # Bookmark wird von cursor geloescht
            
            # Sichtbarkeit schalten
            self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_der_Bereiche(ordinal_neue_zeile)
            
            # alte Datei speichern
            orga_sec_name_alt = self.mb.props['ORGANON'].dict_bereiche['ordinal'][zeilenordinal]
            self.mb.class_Bereiche.datei_nach_aenderung_speichern( orga_sec_name_alt, anderer_pfad = URL_source, speichern = True)
                        
            # File Link setzen, um Anzeige zu erneuern
            sec = self.mb.doc.TextSections.getByName(new_OrgInnerSec_name)
             
            SFLink = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
            SFLink.FileURL = ''
             
            SFLink2 = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
            SFLink2.FileURL = sec.FileLink.FileURL
            SFLink2.FilterName = 'writer8'
     
            sec.setPropertyValue('FileLink',SFLink)
            sec.setPropertyValue('FileLink',SFLink2)
            
            vc.gotoStart(False)
            
            self.mb.class_Bereiche.plain_txt_speichern(sec.Anchor.String, ordinal_neue_zeile)
            self.mb.class_Bereiche.plain_txt_speichern(parsection.Anchor.String, zeilenordinal)
            
            # Einstellungen, tags der alten Datei fuer neue uebernehmen
            self.mb.tags['ordinale'][ordinal_neue_zeile] = copy.deepcopy(self.mb.tags['ordinale'][zeilenordinal])
            
            tree = self.mb.props['ORGANON'].xml_tree
            root = tree.getroot()
            alt = root.find('.//'+zeilenordinal)
            neu = root.find('.//'+ordinal_neue_zeile)
            
            neu.attrib['Tag1'] = alt.attrib['Tag1']
            neu.attrib['Tag2'] = alt.attrib['Tag2']
            neu.attrib['Tag3'] = alt.attrib['Tag3']
            
            self.mb.class_Sidebar.erzeuge_sb_layout()
                
        except Exception as e:
            log(inspect.stack,tb())
            Popup(self.mb, 'error').text = 'teile_text ' + str(e)
            try:
                doc_new.close(False)
            except:
                pass
            
    def teile_text_batch(self):
        if self.mb.debug: log(inspect.stack)
        
        if T.AB != 'ORGANON':
            Popup(self.mb).text = LANG.FUNKTIONIERT_NUR_IM_PROJEKT_TAB
            
        ttb = Teile_Text_Batch(self.mb)
        ttb.erzeuge_fenster()
    
    
    def vereine_dateien(self):
        if self.mb.debug: log(inspect.stack)
        
        try:
            props = self.mb.props['ORGANON']
            selektiert = props.selektierte_zeile
            
            sichtbare = [props.dict_zeilen_posY[b][0] for b in sorted(props.dict_zeilen_posY)]
            index = sichtbare.index(selektiert)
            
            
            def pruefe_ob_kombi_moeglich():
                            
                if index > len(sichtbare) -2:
                    Popup(self.mb, zeit=1).text = LANG.KEINE_KOMBINATION_MOEGLICH
                    return False, None
                
                nachfolger = sichtbare[index + 1]
                
                tree = props.xml_tree
                root = tree.getroot()
                sel_xml = root.find('.//'+selektiert)
                nachfolger_xml = root.find('.//'+nachfolger)
                
                lvl_sel = sel_xml.attrib['Lvl']
                lvl_nach = nachfolger_xml.attrib['Lvl']
                
                if T.AB != 'ORGANON': 
                    Popup(self.mb, zeit=2).text = LANG.FUNKTIONIERT_NUR_IM_PROJEKT_TAB
                    return False, None    
                  
                elif nachfolger in props.dict_ordner[props.Papierkorb]:
                    Popup(self.mb, zeit=1).text = LANG.KEINE_KOMBINATION_MOEGLICH
                    return False, None    
                
                elif lvl_sel > lvl_nach:
                    Popup(self.mb, zeit=1).text = LANG.KEINE_KOMBINATION_MOEGLICH
                    return False, None    
                
                elif nachfolger in props.dict_ordner:
                    elems = nachfolger_xml.findall('.//')
                    if len(elems) > 0:
                        Popup(self.mb, zeit=1).text = LANG.KEINE_KOMBINATION_MOEGLICH
                        return False, None 
                    
                for tab in self.mb.props:
                    if tab != 'ORGANON':
                        tree = self.mb.props[tab].xml_tree
                        root = tree.getroot()
                        nach_xml = root.find('.//' + nachfolger)
                        if nach_xml != None:
                            dateiname = nachfolger_xml.attrib['Name']
                            txt = '{0}\r\n{1}'.format(LANG.KEINE_KOMBINATION_MOEGLICH,
                                                      LANG.NOCH_IN_TAB_GEOEFFNET.format(dateiname,tab))
                            Popup(self.mb, 'warning').text = txt
                            return False, None 
                                           
                    
                return True, nachfolger
            
            ok, nachfolger = pruefe_ob_kombi_moeglich()
            
            if not ok:
                return
                    
            url1 = self.get_pfad(selektiert)
            sec_name1 = 'OrgInnerSec' + selektiert.replace('nr','')
             
             
            url2 = self.get_pfad(nachfolger)
            sec_name2 = 'OrgInnerSec' + nachfolger.replace('nr','')
             
            doc = self.lade_doc_kombi(url1,url2,sec_name1,sec_name2)
             
            self.mb.class_Baumansicht.selektiere_zeile(nachfolger)
             
            prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop.Name = 'Overwrite'
            prop.Value = True
            doc.storeToURL(url1,(prop,))
            doc.close(False)
              
            SFLink = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
            SFLink.FileURL = url1
            sections = self.mb.doc.TextSections
            sec = sections.getByName(sec_name1)
                
            par_sec = sec.ParentSection
            SFLink_helfer = self.mb.sec_helfer.FileLink
            
            # Das Setzen des FileLinks löst den VC Listener aus
            # Er wird via selektiere_zeile() und schalte_sichtbarkeit...() wieder gesetzt
            self.mb.Listener.remove_VC_selection_listener()
            par_sec.setPropertyValue('FileLink',SFLink_helfer)
            par_sec.setPropertyValue('FileLink',SFLink)
                
            papierkorb = self.mb.props[T.AB].Papierkorb
            self.mb.class_Zeilen_Listener.zeilen_neu_ordnen(nachfolger,papierkorb,'inPapierkorbEinfuegen')
            self.mb.class_Baumansicht.selektiere_zeile(selektiert)

            # speicher plain_txt
            self.mb.class_Bereiche.plain_txt_speichern(par_sec.Anchor.String,selektiert)
            self.mb.class_Zeilen_Listener.schalte_sichtbarkeit_hf_ctrls()
            
        except:
            log(inspect.stack,tb())
    
    
    def get_pfad(self,ordi):
        if self.mb.debug: log(inspect.stack)
        
        props = self.mb.props['ORGANON']
        
        sec_name = props.dict_bereiche['ordinal'][ordi]
        pfad = props.dict_bereiche['Bereichsname'][sec_name]    
        
        url = uno.systemPathToFileUrl(pfad)
        return url   
    
    
    def lade_hidden_doc(self, pfad="private:factory/swriter", ordinal=None):
        if self.mb.debug: log(inspect.stack)

        try:
            if ordinal != None:
                sys_pfad = os.path.join( self.mb.pfade['odts'], ordinal + '.odt' )
                pfad = uno.systemPathToFileUrl(sys_pfad)
            
            prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop.Name = 'Hidden'
            prop.Value = True
            
            return self.mb.doc.CurrentController.Frame.loadComponentFromURL(pfad,'_blank',0,(prop,))
                                                    
        except:
            log(inspect.stack,tb())
            
            
    
    def lade_doc_kombi(self,url1,url2,sec_name1,sec_name2):
        if self.mb.debug: log(inspect.stack)
        
        try:
            prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop.Name = 'Hidden'
            prop.Value = True
            
            URL="private:factory/swriter"
            doc = self.mb.doc.CurrentController.Frame.loadComponentFromURL(URL,'_blank',0,(prop,))
            
            newSection0 = self.mb.doc.createInstance("com.sun.star.text.TextSection")
            newSection0.setName('parent')
            
            SFLink1 = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
            SFLink1.FileURL = url1
            newSection1 = self.mb.doc.createInstance("com.sun.star.text.TextSection")
            newSection1.setPropertyValue('FileLink',SFLink1)
            newSection1.setName('test1')
            
            SFLink2 = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
            SFLink2.FileURL = url2
            newSection2 = self.mb.doc.createInstance("com.sun.star.text.TextSection")
            newSection2.setPropertyValue('FileLink',SFLink2)
            newSection2.setName('test2')
             
            cur = doc.Text.createTextCursor()            
            vc = doc.CurrentController.ViewCursor

            doc.Text.insertTextContent(vc, newSection2, False)
            vc.gotoStart(False)
            doc.Text.insertTextContent(vc, newSection1, False)
            
            cur.gotoStart(False)
            cur.gotoEnd(True)
            doc.Text.insertTextContent(cur, newSection0, True)
            
            newSection1.dispose()
            newSection2.dispose()
            
            cur.gotoEnd(False)
            cur.goLeft(1,True)
            cur.setString('')
            
            sections = doc.TextSections
            sec = sections.getByName(sec_name1)
            sec.dispose()
            sec = sections.getByName(sec_name2)
            sec.dispose()
            
            newSection0.setName(sec_name1)
   
            return doc
        except:
            log(inspect.stack,tb())  
    
            
    def verbotene_buchstaben_austauschen(self,term):
                            
        verbotene = '<>:"/\\|?*'

        term =  ''.join(c for c in term if c not in verbotene).strip()
        if term != '':
            return term
        else:
            return 'invalid_name'
        
    def waehle_farbe(self,initial_value=0):
        if self.mb.debug: log(inspect.stack)
        
        cp = self.mb.createUnoService("com.sun.star.ui.dialogs.ColorPicker")        
        values = cp.getPropertyValues()
        
        values[0].Value = initial_value
        cp.setPropertyValues(values)
        
        cp.execute()
        cp.dispose()
        
        farbe = cp.PropertyValues[0].Value
        
        return farbe
    
    def dezimal_to_rgb(self,farbe):
        import struct
             
        f1 = hex(farbe).lstrip('0x')
        if len(f1) < 6:
            f1 = (6-len(f1)) * '0' + f1
        return struct.unpack('BBB',bytes.fromhex(f1))   
    
    def dezimal_to_hex(self,farbe):
        import struct
             
        f1 = hex(farbe).lstrip('0x')
        if len(f1) < 6:
            f1 = (6-len(f1)) * '0' + f1
        return f1 
            
    def folderpicker(self,filepath=None,sys=True):
        if self.mb.debug: log(inspect.stack)
        
        folderpicker = self.mb.createUnoService("com.sun.star.ui.dialogs.FolderPicker")
        if filepath != None:
            folderpicker.setDisplayDirectory(filepath)
        folderpicker.execute()
        
        if folderpicker.Directory == '':
            return None
        
        if sys:
            return uno.fileUrlToSystemPath(folderpicker.getDirectory())
        else:
            return folderpicker.getDirectory()
    
    def filepicker(self,filepath=None,ofilter=None,url_to_sys=True):
        if self.mb.debug: log(inspect.stack)
        
        Filepicker = self.mb.createUnoService("com.sun.star.ui.dialogs.FilePicker")
        
        # Bug in Office: funktioniert nicht
        if filepath != None:
            Filepicker.setDisplayDirectory(filepath)
            
            
        if ofilter != None:
            Filepicker.appendFilter('lang_py_file','*.' + ofilter)
            
        Filepicker.execute()

        if Filepicker.Files == '':
            return None
        if url_to_sys:
            return uno.fileUrlToSystemPath(Filepicker.Files[0])
        else:
            return Filepicker.Files[0]
        
        
    def filepicker2(self,ofilter=None,url_to_sys=True):
        if self.mb.debug: log(inspect.stack)
        
        Filepicker = self.mb.createUnoService("com.sun.star.ui.dialogs.FilePicker")
        
        # Bug in Office: funktioniert nicht
#         if filepath != None:
#             Filepicker.setDisplayDirectory(filepath)
            
        if ofilter != None:
            Filepicker.appendFilter(*ofilter)
            
        Filepicker.execute()
        file_len = len(Filepicker.Files)
        
                   
        if file_len == 0:
            return None,False
        
        path = Filepicker.Files[0]

        if url_to_sys:
            try:
                return uno.fileUrlToSystemPath(path),True
            except Exception as e:
                print(e)
                return path,True
        else:
            return path,True
        
    
    def oeffne_json(self,pfad):
        if self.mb.debug: log(inspect.stack)
        
        try:
            with open(pfad) as data:  
                try:
                    content = data.read()#.decode() 
                    odict = json.loads(content)
                except:
                    odict = json.load(data)
            
            return odict
        except:
            log(inspect.stack,tb())  
            return None
        
    def get_zuletzt_benutzte_datei(self):
        if self.mb.debug: log(inspect.stack)
        try:
            props = self.mb.props[T.AB]
            zuletzt = props.selektierte_zeile_alt
            xml = props.xml_tree
            root = xml.getroot()
            return root.find('.//' + zuletzt).attrib['Name']
        except:
            return 'None'
        
    def mache_tag_sichtbar(self,sichtbar,tag_name):
        if self.mb.debug: log(inspect.stack)
        
        sett = self.mb.settings_proj
        tags = sett['tag1'],sett['tag2'],sett['tag3']
        
        for tab_name in self.mb.props:
        
            # alle Zeilen
            if self.mb.props[tab_name].Hauptfeld == None:
                # Nicht geoeffnete Tabs brauchen nicht
                # angepasst zu werden
                continue
            
            controls_zeilen = self.mb.props[tab_name].Hauptfeld.Controls
            tree = self.mb.props[tab_name].xml_tree
            root = tree.getroot()
            
            gliederung  = None
            if sett['tag3']:
                gliederung = self.mb.class_Gliederung.rechne(tree)
            
            if not sichtbar:
                for contr_zeile in controls_zeilen:
                    ord_zeile = contr_zeile.AccessibleContext.AccessibleName
                    if ord_zeile == self.mb.props[T.AB].Papierkorb:
                        continue
                    
                    self.mb.class_Baumansicht.positioniere_icons_in_zeile(contr_zeile,tags,gliederung)
                    tag_contr = contr_zeile.getControl(tag_name)
                    tag_contr.dispose()
 
                    
            if sichtbar:
                for contr_zeile in controls_zeilen:                    

                    ord_zeile = contr_zeile.AccessibleContext.AccessibleName
                    if ord_zeile == self.mb.props[T.AB].Papierkorb:
                        continue
                    
                    zeile_xml = root.find('.//'+ord_zeile)
                    
                    if tag_name == 'tag1':
                        farbe = zeile_xml.attrib['Tag1']
                        url = 'vnd.sun.star.extension://xaver.roemers.organon/img/punkt_%s.png' % farbe
                        listener = self.mb.class_Baumansicht.tag1_listener
                    elif tag_name == 'tag2':
                        url = zeile_xml.attrib['Tag2']
                        listener = self.mb.class_Baumansicht.tag2_listener
                    elif tag_name == 'tag3':
                        url = ''
                    
                    if tag_name in ('tag1','tag2'):
                        PosX,PosY,Width,Height = 0,2,16,16
                        control_tag1, model_tag1 = self.mb.createControl(self.mb.ctx,"ImageControl",PosX,PosY,Width,Height,(),() )  
                        model_tag1.ImageURL = url
                        model_tag1.Border = 0
                        control_tag1.addMouseListener(listener)
                    else:
                        PosX,PosY,Width,Height = 0,2,16,16
                        control_tag1, model_tag1 = self.mb.createControl(self.mb.ctx,"FixedText",PosX,PosY,Width,Height,(),() )     
                        model_tag1.TextColor = KONST.FARBE_GLIEDERUNG
                        
                    contr_zeile.addControl(tag_name,control_tag1)
                    self.mb.class_Baumansicht.positioniere_icons_in_zeile(contr_zeile,tags,gliederung)
                    
                    
    def pruefe_galerie_eintrag(self):
        if self.mb.debug: log(inspect.stack)
        
        gallery = self.mb.createUnoService("com.sun.star.gallery.GalleryThemeProvider")
            
        if 'Organon Icons' not in gallery.ElementNames:
            
            paths = self.mb.createUnoService( "com.sun.star.util.PathSettings" )
            gallery_pfad = uno.fileUrlToSystemPath(paths.Gallery_writable)
            gallery_ordner = os.path.join(gallery_pfad,'Organon Icons')
                    
            entscheidung = self.mb.entscheidung(LANG.BENUTZERDEFINIERTE_SYMBOLE_NUTZEN %gallery_ordner,"warningbox",16777216)
            # 3 = Nein oder Cancel, 2 = Ja
            if entscheidung == 3:
                return False
            elif entscheidung == 2:
                try:
                    iGal = gallery.insertNewByName('Organon Icons')  
                    path_icons = os.path.join(self.mb.path_to_extension,'img','Organon Icons')
                    
                    from shutil import copy 
                    
                    # Galerie anlegen
                    if not os.path.exists(gallery_ordner):
                        os.makedirs(gallery_ordner)
                    
                    # Organon Icons einfuegen
                    for (dirpath,dirnames,filenames) in os.walk(path_icons):
                        for f in filenames:
                            url_source = os.path.join(dirpath,f)
                            url_dest   = os.path.join(gallery_ordner,f)
                            
                            copy(url_source,url_dest)
 
                            url = uno.systemPathToFileUrl(url_dest)
                            iGal.insertURLByIndex(url,0)
                    
                    return True
                
                except:
                    log(inspect.stack,tb())
        
        return True
    
    def get_writer_shortcuts(self):
        if self.mb.debug: log(inspect.stack)
        
        ctx = self.mb.ctx
        smgr = self.mb.ctx.ServiceManager
           
        config_provider = smgr.createInstanceWithContext("com.sun.star.configuration.ConfigurationProvider",ctx)
  
        prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop.Name = "nodepath"
        prop.Value = "org.openoffice.Office.Accelerators"
               
        config_access = config_provider.createInstanceWithArguments("com.sun.star.configuration.ConfigurationUpdateAccess", (prop,))
        
        glob = config_access.PrimaryKeys.Global 
        modules = config_access.PrimaryKeys.Modules
        textdoc = modules.getByName('com.sun.star.text.TextDocument')
        
        shortcuts = {}
        
        elements = textdoc.ElementNames
        
        for e in elements:
            try:
                if e in textdoc.ElementNames:
                    sc = textdoc.getByName(e)
                    shortcuts.update({e:sc.Command})
            except:
                shortcuts.update({e:'?'})
                
        elements = glob.ElementNames
        
        for e in elements:
            try:
                if e in textdoc.ElementNames:
                    sc = textdoc.getByName(e)
                    shortcuts.update({e:sc.Command})
            except:
                shortcuts.update({e:'?'})
        
        
        
        erweitert = ['F'+str(a) for a in range(1,13)]
        erweitert.extend(['DOWN','LEFT','RIGHT','UP'])
        
        mod1 = []
        mod2 = []
        #shift = []
        
        mod1_mod2 = []
        shift_mod1 = []
        shift_mod2 = []
        shift_mod1_mod2 = []
        
        for s in shortcuts:
            cmd = s.split('_')
            
            if len(cmd) == 2:
                if len(cmd[0]) == 1 or cmd[0] in erweitert:
                    
                    if 'MOD1' in s:
                        mod1.append(cmd[0])
                    elif 'MOD2' in s:
                        mod2.append(cmd[0])
            elif len(cmd) == 3:
                if len(cmd[0]) == 1 or cmd[0] in erweitert:
                    if 'SHIFT_MOD1' in s:
                        shift_mod1.append(cmd[0])
                    elif 'SHIFT_MOD2' in s:
                        shift_mod2.append(cmd[0])
                    elif 'MOD1_MOD2' in s:
                        mod1_mod2.append(cmd[0])
            elif len(cmd) == 4:
                if len(cmd[0]) == 1 or cmd[0] in erweitert:
                    if 'SHIFT_MOD1_MOD2' in s:
                        shift_mod1_mod2.append(cmd[0])
            
            
        used = {
                2:sorted(mod1),
                3:sorted(shift_mod1),
                4:sorted(mod2),
                5:sorted(shift_mod2),
                6:sorted(mod1_mod2),
                7:sorted(shift_mod1_mod2)
                }
        return used
        
        
        

    
    
    def leere_hf(self):
        if self.mb.debug: log(inspect.stack)
        
        contr = self.mb.prj_tab.getControl('Hauptfeld_aussen') 
        contr.dispose()
        contr = self.mb.prj_tab.getControl('ScrollBar')
        contr.dispose()

            
    def update_organon_templates(self):  
        if self.mb.debug: log(inspect.stack)
        
        templ = self.mb.settings_orga['templates_organon']
        pfad = templ['pfad']
        
        if pfad == '':
            return
        
        templates = []
        
        for root, dirs, files in os.walk(pfad):
            break
        
        for d in dirs:
            name = d.split('.')
            if len(name) == 2:
                if name[1] == 'organon':
                    templates.append(name[0])
                    
        templ['templates'] = templates
        
        
    def vorlage_speichern(self,pfad,name):
        if self.mb.debug: log(inspect.stack)

        pfad_zu_neuem_ordner = os.path.join(pfad,name)
        
        tree = copy.deepcopy(self.mb.props['ORGANON'].xml_tree)
        root = tree.getroot()
        
        all_elements = root.findall('.//')
        ordinale = []
        
        for el in all_elements:
            ordinale.append(el.tag)        
    
        self.mb.class_Export.kopiere_projekt(name,pfad_zu_neuem_ordner,ordinale,tree,self.mb.tags,True)  
        os.rename(pfad_zu_neuem_ordner,pfad_zu_neuem_ordner+'.organon')
    
    
    def kopiere_ordner(self,src, dst):
        if self.mb.debug: log(inspect.stack)
        
        import shutil,errno
        try:
            shutil.copytree(src, dst)
        except OSError as exc: 
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else: 
                log(inspect.stack,tb())
                
                
    def projekt_umbenannt_speichern(self,alter_pfad,neuer_pfad,name):
        if self.mb.debug: log(inspect.stack)
        
        alter_name = os.path.basename(alter_pfad)

        self.kopiere_ordner(alter_pfad,neuer_pfad)
         
        alt = os.path.join(neuer_pfad,alter_name)
        neu = os.path.join(neuer_pfad,name + '.organon')

        os.rename(alt,neu)
         
        pfad_el_tree = os.path.join(neuer_pfad,'Settings','ElementTree.xml')
              
        xml_tree = ElementTree.parse(pfad_el_tree)
        root = xml_tree.getroot()
         
        prj_xml = root.find(".//*[@Art='prj']")
        prj_xml.attrib['Name'] = name
         
        xml_tree.write(pfad_el_tree)
        
        
    def repariere_Bereiche(self):
        if self.mb.debug: log(inspect.stack)
        
        try:
            secs = [doc.TextSections.getByName(s) for s in props.dict_bereiche['Bereichsname']]            
            
            ausnahmen = []
            fehlerhafte = []
            
            for s in secs:
                try:
                    if 'OrgInnerSec' not in s.ChildSections[0].Name:
                        fehlerhafte.append(s)
                except:
                    ausnahmen.append(s)
                    
            for a in ausnahmen:
                # Ausnahmen besitzen gar keinen inneren Bereich
                name = a.name
                ordinal = props.dict_bereiche['Bereichsname-ordinal'][name]
                org_name = 'OrgInnerSec' + ordinal.replace('nr','')
                 
                newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
                newSection.setName(org_name)
                 
                cur = a.Anchor.Text.createTextCursorByRange(a.Anchor)
                a.Anchor.Text.insertTextContent(cur, newSection, True)
                
                self.mb.class_Bereiche.datei_speichern(ordinal)
                 
              
            for f in fehlerhafte:
                # fehlerhaft benannte Bereiche
                name = a.name
                ordinal = props.dict_bereiche['Bereichsname-ordinal'][name]
                org_name = 'OrgInnerSec' + ordinal.replace('nr','')
                 
                f.ChildSections[0].setName(org_name)

                self.mb.class_Bereiche.datei_speichern(ordinal)
        except:
            log(inspect.stack,tb())
        


class Teile_Text_Batch():
    def __init__(self,mb):
        self.mb = mb
        
    def erzeuge_fenster(self):
        if self.mb.debug: log(inspect.stack)
                
        try:
            self.dialog_batch_devide()
        except:
            log(inspect.stack,tb())
                        
            
    def dialog_batch_devide_elemente(self):
        if self.mb.debug: log(inspect.stack)
        
        listener = self.listener
        
        controls = [
            10,
            ('control_Titel',"FixedText",1,       
                                    'tab0',0,30,20,    
                                    ('Label','FontWeight'),
                                    (LANG.TEXT_BATCH_DEVIDE ,150),                  
                                    {}
                                    ), 
            35,
            ('control_Text',"Edit",0,        
                                    'tab0x-tab1-E',0,100,20,    
                                    (),
                                    (),                  
                                    {}
                                    ),                     
            40, ]
        
        elemente = 'GANZES_WORT','REGEX','UEBERSCHRIFTEN','LEERZEILEN'
                
        for el in elemente:
            controls.extend([
            ('control_{}'.format(el),"CheckBox",1,      
                                    'tab0',0,200,20,    
                                    ('Label','State'),
                                    (getattr(LANG, el),0),        
                                    {'setActionCommand':el,'addActionListener':(listener,)} 
                                    ),  
            25 if el != 'REGEX' else 45])
            
        controls.extend([
            20,
            ('control_link',"CheckBox",1,      
                                    'tab0x',0,20,20,    
                                    ('Label','State','HelpText'),
                                    (LANG.VERLINKE_IN_NEUE_DATEIEN,0,LANG.VERLINKE_IN_NEUE_DATEIEN_HELP),        
                                    {'setActionCommand':'link','addActionListener':(listener,)} 
                                    ), 
            30,
            ('control_start',"Button",0,      
                                    'tab1-max',0,80,30,    
                                    ('Label',),
                                    (LANG.START,),        
                                    {'setActionCommand':'start','addActionListener':(listener,)} 
                                    ),  
            20])
        
        # feste Breite, Mindestabstand
        tabs = {
                 0 : (None, 10),
                 1 : (None, 10),
                 }
        
        abstand_links = 10
        controls2,tabs3,max_breite = self.mb.class_Fenster.berechne_tabs(controls, tabs, abstand_links)
          
        return controls2,max_breite
        
        #return controls

 
    def dialog_batch_devide(self): 
        if self.mb.debug: log(inspect.stack)
        
        try:
            posSize_main = self.mb.desktop.ActiveFrame.ContainerWindow.PosSize
            X = self.mb.dialog.Size.Width
            Y = posSize_main.Y         

            # Listener erzeugen 
            self.listener = Batch_Text_Devide_Listener(self.mb)         
            
            controls,max_breite = self.dialog_batch_devide_elemente()
            ctrls,pos_y = self.mb.class_Fenster.erzeuge_fensterinhalt(controls)   
            
            self.listener.ctrls = ctrls
            self.listener.ttb = self
            
            # Hauptfenster erzeugen
            posSize = X,Y,max_breite,pos_y
            fenster,fenster_cont = self.mb.class_Fenster.erzeuge_Dialog_Container(posSize)             
              
            # Controls in Hauptfenster eintragen
            for c in ctrls:
                fenster_cont.addControl(c,ctrls[c])
           
            self.fenster = fenster
           
        except:
            log(inspect.stack,tb())
            
            
    def werte_controls_aus(self,ctrls):
        if self.mb.debug: log(inspect.stack)
        
        text = ctrls['control_Text'].Text
        ganzes_wort = ctrls['control_GANZES_WORT'].State
        regex = ctrls['control_REGEX'].State
        ueberschriften = ctrls['control_UEBERSCHRIFTEN'].State
        leerzeilen = ctrls['control_LEERZEILEN'].State
        verlinken = ctrls['control_link'].State
        
        if text == '' and not ueberschriften and not leerzeilen:
            Popup(self.mb, 'info').text = LANG.NICHTS_AUSGEWAEHLT_BATCH
        else:
            args = text, ganzes_wort, regex, ueberschriften, leerzeilen, verlinken
            self.fenster.dispose()
            self.run(args)


    def run(self,args):
        if self.mb.debug: log(inspect.stack)
        
        try:
            text, ganzes_wort, regex, ueberschriften, leerzeilen, verlinken = args
            
            ergebnis1 = []
            ergebnis2 = []
            ergebnis3 = []
            
            url = self.get_pfad() 
            ordinal = os.path.basename(url).split('.')[0]
            self.mb.class_Bereiche.datei_speichern(ordinal)
            
            doc = self.lade_doc(url)  
            
            erster = self.get_ersten_paragraph(doc)    
                   
            if text != '':
                ergebnis3 = self.get_suchbegriff(doc, suchbegriff=text, ganzes_wort=ganzes_wort, regex=regex)
            if ueberschriften:
                ergebnis1 = self.get_ueberschriften(doc)
            if leerzeilen:
                ergebnis2 = self.get_leerzeilen(doc)
              
            ordnung = sorted(erster + ergebnis1 + ergebnis2 + ergebnis3, key = lambda x : (x[2])) 
    
            ausgesonderte,ordnung = self.erstelle_bereiche(doc,ordnung)              
            ordnung = [o for o in ordnung if o not in ausgesonderte] 
            
            if len(ordnung) > 10:
                entscheidung = self.mb.entscheidung(LANG.ERSTELLT_WERDEN.format(len(ordnung)),"warningbox",16777216)
                # 3 = Nein oder Cancel, 2 = Ja
                if entscheidung == 3:
                    doc.close(False)
                    return
  
            tree = self.erstelle_tree(ordnung)  
            
            root = tree.getroot()
            anz = len(root.findall('.//'))
            
            if anz < 2:
                Popup(self.mb, 'info').text = LANG.KEINE_TRENNUNG
                doc.close(False)
                return
            
            speicherordner = self.mb.pfade['odts']
            pfad_helfer_system = os.path.join(speicherordner,'batchhelfer.odt')
            pfad_helfer = uno.systemPathToFileUrl(pfad_helfer_system)
            
            self.mb.class_Querverweise.querverweise_umbenennen(doc, ordinal, verlinken)
            
            doc.storeToURL(pfad_helfer,())
            doc.close(False)
               
            tree_new = self.fuege_tree_in_xml_ein(tree)
            anz = self.neue_Dateien_erzeugen(pfad_helfer, tree)            

            os.remove(pfad_helfer_system)
            self.schreibe_neuen_elementtree(tree_new,anz)
            self.lege_dict_sbs_an(tree)
            self.mb.class_Tags.speicher_tags()

            self.mb.Listener.remove_Undo_Manager_Listener()
            self.mb.Listener.remove_VC_selection_listener()
             
            self.mb.class_Projekt.lade_Projekt2()
            
        except:
            log(inspect.stack,tb())
            try:
                doc.close(False)
            except:
                pass
            
        
    def get_pfad(self):
        if self.mb.debug: log(inspect.stack)
        
        props = self.mb.props['ORGANON']
        selektiert = props.selektierte_zeile
        
        sec_name = props.dict_bereiche['ordinal'][selektiert]
        pfad = props.dict_bereiche['Bereichsname'][sec_name]    
        
        url = uno.systemPathToFileUrl(pfad)
        return url
    
    
    def lade_doc(self,url):
        if self.mb.debug: log(inspect.stack)
        
        try:
            prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop.Name = 'Hidden'
            prop.Value = True
            
            URL="private:factory/swriter"
            doc = self.mb.doc.CurrentController.Frame.loadComponentFromURL(URL,'_blank',0,(prop,))
                                                    
            SFLink = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
            SFLink.FileURL = url
            SFLink.FilterName = 'writer8'
            
            newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
            newSection.setPropertyValue('FileLink',SFLink)
            newSection.setName('test')
            
            cur = doc.Text.createTextCursor()
            doc.Text.insertTextContent(cur, newSection, True)

            sections = doc.TextSections
            secs = []
            for i in range(sections.Count):
                secs.append(sections.getByIndex(i))

            for s in secs:
                s.dispose()
                
            return doc
        except:
            log(inspect.stack,tb())
            
     
    def get_ueberschriften(self,doc):
        if self.mb.debug: log(inspect.stack)
        
        try:
            sd = doc.createSearchDescriptor()
            sd.SearchStyles = True
            viewcursor = doc.CurrentController.ViewCursor
             
            StyleFamilies = doc.StyleFamilies
            ParagraphStyles = StyleFamilies.getByName("ParagraphStyles")
             
            headings = []
            display_names = []

            for p in ParagraphStyles.ElementNames:
                if 'Heading' in p[0:7]:
                    headings.append(p)
                    elem = ParagraphStyles.getByName(p)
                    display_names.append(elem.DisplayName)
             
            ergebnisse = []

            for dn in range(len(display_names)):
                sd.SearchString = display_names[dn]
                ergebnisse.append(doc.findAll(sd))
             
            ordnung = []
            x = 0

            for e in ergebnisse:
                for count in range(e.Count):
                    erg = e.getByIndex(count)
                    viewcursor.gotoRange(erg.Start,False)
                    vd = int(doc.CurrentController.ViewData.split(';')[1])
                    ordnung.append([erg.ParaStyleName,viewcursor.Page,vd,erg,erg.String])
                    x += 1

        except:
            log(inspect.stack,tb())
            ordnung = []
         
        return ordnung
    
    
    def get_leerzeilen(self,doc):
        if self.mb.debug: log(inspect.stack)
        
        try:
            sd = doc.createSearchDescriptor()
            viewcursor = doc.CurrentController.ViewCursor
            
            regex_leerzeile = '^$'
            
            sd.SearchRegularExpression = True
            sd.SearchString = regex_leerzeile

            ergebnisse1 = doc.findAll(sd)
            
            sd.SearchString = '^\s*$'
            ergebnisse2 = doc.findAll(sd)
            
            zeilen = []
            

            def get_zeilen(ergs,zeilen):
                erg = ergs.getByIndex(count)
                
                if erg.ParaStyleName == 'Footnote':
                    return

                viewcursor.gotoRange(erg.Start,False)
                vd = int(doc.CurrentController.ViewData.split(';')[1])
                zeilen.append(['leer',viewcursor.Page,vd,viewcursor.Start,erg.String])
                
            
            for count in range(ergebnisse1.Count):
                get_zeilen(ergebnisse1,zeilen)
                
            for count in range(ergebnisse2.Count):
                get_zeilen(ergebnisse2,zeilen)

        except:
            log(inspect.stack,tb())
            
        return zeilen
    
    
    def get_suchbegriff(self,doc,suchbegriff,ganzes_wort,regex):
        if self.mb.debug: log(inspect.stack)
        
        try:
            zeilen = []
            
            sd = doc.createSearchDescriptor()
            viewcursor = doc.CurrentController.ViewCursor

            if regex:
                sd.SearchRegularExpression = True
            if ganzes_wort:
                sd.SearchWords = True
                
            sd.SearchString = suchbegriff
            ergebnisse = doc.findAll(sd)
            
            x = 0

            for count in range(ergebnisse.Count):
                
                erg = ergebnisse.getByIndex(count)
                #erg.CharBackColor = 502
                viewcursor.gotoRange(erg.Start,False)

                vd = int(doc.CurrentController.ViewData.split(';')[1])
                #print(viewcursor.CharStyleName + viewcursor.ParaStyleName)
                if 'footnote' not in viewcursor.ParaStyleName.lower():
                    zeilen.append(['suchbegriff',viewcursor.Page,vd,erg,erg.String])
                    x += 1
               
        except:
            log(inspect.stack,tb())
        
        return zeilen
               
     
    def erstelle_bereiche(self,doc,ordnung):
        if self.mb.debug: log(inspect.stack)
        
        cur = doc.Text.createTextCursor()
        
        x = self.mb.props['ORGANON'].kommender_Eintrag
        ausgesonderte = []
        
        try:    
            
            txt_frames = [doc.TextFrames.getByIndex(i) for i in range(doc.TextFrames.Count)] 
            text_ranges = []
            
            for f in txt_frames:
                cur2 = doc.Text.createTextCursorByRange(f.Text.Anchor)
                cur2.goLeft(1,False)
                text_ranges.append(cur2)
            
            
            def is_txt_frame(erg):
                for t in text_ranges:
                    try:
                        #print(doc.Text.compareRegionStarts(t,erg))
                        if doc.Text.compareRegionStarts(t,erg) == 0:
                            text_ranges.remove(t)
                            return True
                    except:
                        pass
                return False
            

            # pro Ueberschrift 1 Ordner
            for o in range(len(ordnung)):
                
                aussondern = True
                
                fund = ordnung[o][3]
                if o + 1 < len(ordnung):
                    fund_ende = ordnung[o+1][3]
                else:
                    fund_ende = None
                
                # Cursor setzen
                if ordnung[o][0] == 'leer':
                    cur.gotoRange(fund.Start,False)
                    if  is_txt_frame(cur):
                        aussondern = False
                    cur.goRight(1,False)
                    fund = cur.Start
                                                
                cur.gotoRange(fund.Start,False)
                                    
                if fund_ende != None:
                    cur.gotoRange(fund_ende.Start,True)
                else:
                    cur.gotoEnd(True)
                    
                # leere Bereiche aussparen
                if cur.String.strip() == '':   
                    if aussondern:                                 
                        ausgesonderte.append(ordnung[o])
                        continue
                
                try:
                    newSection = doc.createInstance("com.sun.star.text.TextSection")
                    doc.Text.insertTextContent(cur, newSection, True)
                    newSection.setName('organon_nr{}'.format(x))
                    ordnung[o][4] = cur.String
                    x += 1
                except:
                    if aussondern:                                 
                        ausgesonderte.append(ordnung[o])
                        continue
                    
              
        except:
            log(inspect.stack,tb())
            
        return ausgesonderte,ordnung
    
     
    def setze_attribute(self,element,name,art,level,parent):
        if self.mb.debug: log(inspect.stack)
        
        if art == 'dir':
            zustand = 'auf'
        else:
            zustand = '-'
        
        element.attrib['Name'] = name.split('\n')[0]
        element.attrib['Zustand'] = zustand
        element.attrib['Sicht'] = 'ja'
        element.attrib['Parent'] = parent.tag
        element.attrib['Lvl'] = str(level)
        element.attrib['Art'] = art
        
        element.attrib['Tag1'] = 'leer'
        element.attrib['Tag2'] = 'leer'
        element.attrib['Tag3'] = 'leer'
     
     
    def erstelle_tree(self,geordnete):
        if self.mb.debug: log(inspect.stack)
        
        # XML TREE
        et = ElementTree   
        root = et.Element('root')
        root.attrib['NameH'] = 'AAA'
        tree = et.ElementTree(root)
        
        props = self.mb.props['ORGANON']
        
        kE = props.kommender_Eintrag
        el = root
        
        selektiert = props.selektierte_zeile
        root_orig = props.xml_tree.getroot()
        sel_xml = root_orig.find('.//'+selektiert)
        lvl_sel = int(sel_xml.attrib['Lvl'])
        
        lvl = lvl_sel - 1
        erste_pg = True
        
        try:
            for o in range(len(geordnete)):
                
                heading = geordnete[o][0]
                name = geordnete[o][4]
                name = name.strip() if len(name) < 60 else name[0:60].strip()
                
                if heading in ['leer','suchbegriff','erster']:
                    if erste_pg: 
                        if el.tag == 'root':
                            par = el
                        else:
                            par = root.find('.//'+el.tag)
                        lvl += 1
                    else:
                        par = root.find('.//'+el.tag+'/..')
                    el = et.SubElement(par,'nr'+str(o+kE))
                    
                    el.attrib['NameH'] = heading
                
                    par = root.find('.//'+el.tag+'/..')
                    self.setze_attribute(el,name,'pg',lvl,par)
                    erste_pg = False
                    continue
                
                elif heading > el.attrib['NameH']:
                    el = et.SubElement(el,'nr'+str(o+kE))
                    lvl += 1
                    
                elif heading == el.attrib['NameH']:
                    par = root.find('.//'+el.tag+'/..')
                    el = et.SubElement(par,'nr'+str(o+kE))
                     
                else:
                    par = el
                    while heading <= par.attrib['NameH']:
                        par = root.find('.//'+par.tag+'/..')
                        lvl -= 1
                    lvl += 1

                    el = et.SubElement(par,'nr'+str(o+kE))
                   
                el.attrib['NameH'] = heading
                
                par = root.find('.//'+el.tag+'/..')
                self.setze_attribute(el,name,'dir',lvl,par)
                erste_pg = True
        except:
            log(inspect.stack,tb())
            tree = None
            
        alle = root.findall('.//')
        for a in alle:
            del a.attrib['NameH']
        
        return tree
    
    
    def get_ersten_paragraph(self,doc):
        if self.mb.debug: log(inspect.stack)
        
        vc = doc.CurrentController.ViewCursor
        vc.gotoStart(False)
        erg = vc.Start
        vd = 0
        return [['erster',vc.Page,vd,erg,erg.String]]
    
    
    def neue_Dateien_erzeugen(self,pfad_helfer,tree):
        if self.mb.debug: log(inspect.stack)
        
        root = tree.getroot()
        neue_dateien = root.findall('.//')
        ordinale = [n.tag for n in neue_dateien]

        StatusIndicator = self.mb.desktop.getCurrentFrame().createStatusIndicator()
        StatusIndicator.start(LANG.ERZEUGE_DATEI %(1,len(ordinale)),len(ordinale))
        
        speicherordner = self.mb.pfade['odts']
        
        zaehler = 0

        try:
            prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop.Name = 'Hidden'
            prop.Value = True
            
            URL="private:factory/swriter"
            
            for o in ordinale:
                StatusIndicator.setValue(zaehler)
                StatusIndicator.setText(LANG.ERZEUGE_DATEI %(zaehler+1,len(ordinale)))
                
                new_doc = self.mb.desktop.loadComponentFromURL(URL,'_blank',8+32,(prop,))
                cur = new_doc.Text.createTextCursor()
                
                SFLink = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
                SFLink.FileURL = pfad_helfer
                SFLink.FilterName = 'writer8'
                
                newSection = new_doc.createInstance("com.sun.star.text.TextSection")
                newSection.Name = 'OrgInnerSec' + o.replace('nr','')
                new_doc.Text.insertTextContent(cur, newSection, True)
                
                cur.goLeft(1,False)
                cur.setString(' ')
                
                newSection2 = new_doc.createInstance("com.sun.star.text.TextSection")
                newSection2.setPropertyValue('FileLink',SFLink)
                newSection2.LinkRegion = 'organon_' + o
                  
                new_doc.Text.insertTextContent(cur, newSection2, True)
                
                if newSection2.Anchor.String.startswith('***Inserted By Organon***'):
                    # Wegen eines Bugs in Writer: Durch Organon eingefuegte Zeile
                    # wieder loeschen. Vgl. querverweise querverweise_umbenennen()
                    # benenne_listen_und_ueberschriften_um()
                    cur2 = newSection2.Anchor.Text.createTextCursorByRange(newSection2.Anchor)
                    cur2.gotoStartOfParagraph(False)
                    cur2.gotoNextParagraph(True)
                    cur2.setString('')
                
                    
                newSection2.dispose()
                
                cur.gotoEnd(False)
                cur.goLeft(1,True)
                cur.setString('')                
                
                pfad = os.path.join(speicherordner,o +'.odt')
                pfad2 = uno.systemPathToFileUrl(pfad)
                new_doc.storeToURL(pfad2,())
                self.mb.class_Bereiche.plain_txt_speichern(new_doc.Text.String,o)
                new_doc.close(False)
                
                zaehler += 1
            
        except:
            log(inspect.stack,tb())
            StatusIndicator.end()
            return 0
            
        StatusIndicator.end()
        return zaehler
    
    
    def fuege_tree_in_xml_ein(self,new_tree):
        if self.mb.debug: log(inspect.stack)
        
        try:        
            tree_old = copy.deepcopy(self.mb.props[T.AB].xml_tree)
            root = tree_old.getroot()
            
            name_selek_zeile = self.mb.props['ORGANON'].selektierte_zeile
            xml_selekt_zeile = root.find('.//'+name_selek_zeile)
            
            parent = root.find('.//'+xml_selekt_zeile.tag+'/..')
            liste = list(parent)
            index_sel = liste.index(xml_selekt_zeile)
            
            children_new_tree = list(new_tree.getroot())
            
            for c in range(len(children_new_tree)):
                child = children_new_tree[c]
                child.attrib['Parent'] = parent.tag
                parent.insert(index_sel+1+c,child)  
            
            return tree_old
        
        except:
            log(inspect.stack,tb())
            
            
    def schreibe_neuen_elementtree(self,tree,zaehler):
        root = tree.getroot()
        kE = int(root.attrib['kommender_Eintrag'])  
        root.attrib['kommender_Eintrag'] = str(kE + zaehler)
        
        self.mb.props['ORGANON'].kommender_Eintrag += zaehler
        
        path = os.path.join(self.mb.pfade['settings'],'ElementTree.xml')
        self.mb.tree_write(tree,path)
        
    def lege_dict_sbs_an(self,tree):
        root = tree.getroot()
        alle = root.findall('.//')
        for a in alle:
            self.mb.class_Tags.erzeuge_tags_ordinal_eintrag(a.tag)
            


from com.sun.star.awt import XActionListener
class Batch_Text_Devide_Listener (unohelper.Base, XActionListener):
    def __init__(self,mb):
        self.mb = mb
        
        self.ctrls = None
        self.ttb = None
       
    def actionPerformed(self,ev):
        if self.mb.debug: log(inspect.stack)
        
        cmd = ev.ActionCommand
        
        if cmd == 'GANZES_WORT':
            ctrl = self.ctrls['control_REGEX']
            ctrl.State = 0
        elif cmd == 'REGEX':
            ctrl = self.ctrls['control_GANZES_WORT']
            ctrl.State = 0
        elif cmd == 'start':
            self.ttb.werte_controls_aus(self.ctrls)
        
        
    def disposing(self,ev):
        return False

        
     
from com.sun.star.awt import XMouseListener,XItemListener
class Tag_Container_Listener (unohelper.Base, XMouseListener):
    def __init__(self):
        self.ob = None
       
    def mousePressed(self, ev):
        return False
   
    def mouseExited(self, ev): 
        
        point = uno.createUnoStruct('com.sun.star.awt.Point')
        point.X = ev.X
        point.Y = ev.Y

        enthaelt_Punkt = ev.Source.AccessibleContext.containsPoint(point)
        
        if enthaelt_Punkt:
            pass
        else:            
            self.ob.dispose()    
        return False
    
    def mouseEntered(self, ev):  
        return False
    def mouseReleased(self,ev):
        return False
    def disposing(self,ev):
        return False
  
            
class Tag2_Images_Listener (unohelper.Base, XMouseListener):
    
    def __init__(self,mb):
        self.mb = mb
        self.ordinal = None
        self.icons_dict = None
        self.window_parent = None
       
       
    def mousePressed(self, ev):
        if self.mb.debug: log(inspect.stack) 

        url = ev.Source.Model.ImageURL
        
        if url != '':
            self.galerie_icon_im_prj_ordner_evt_loeschen()
            url = self.galerie_icon_im_prj_ordner_speichern(url) 
        else:
            if self.window_parent == None:
                # Beim Aufruf aus Calc kann nicht geloescht werden,
                # geloescht wird daher beim Schliessen von Calc
                self.galerie_icon_im_prj_ordner_evt_loeschen()
            
        self.tag2_in_allen_tabs_xml_anpassen(self.ordinal,url)

        if self.window_parent != None:
            self.icon_in_calc_anpassen(self.ordinal,url)
        
        self.win.dispose()


    def tag2_in_allen_tabs_xml_anpassen(self,ord_source,url):
        if self.mb.debug: log(inspect.stack) 
        try:
            tabnamen = self.mb.props.keys()

            for name in tabnamen:
            
                tree = self.mb.props[name].xml_tree
                root = tree.getroot()        
                source_xml = root.find('.//'+ord_source)
                
                if source_xml != None:
                
                    source_xml.attrib['Tag2'] = url
                    
                    if name == 'ORGANON':
                        Path = os.path.join(self.mb.pfade['settings'], 'ElementTree.xml')
                    else:
                        Path = os.path.join(self.mb.pfade['tabs'], name + '.xml')
                    
                        
                    try:
                        # Wenn noch nicht alle Tabs aufgerufen worden sind, existieren manche
                        # Hauptfelder noch nicht. Daher try/except als schnelle Loesung
                        tag2_button = self.mb.props[name].Hauptfeld.getControl(ord_source).getControl('tag2')
                        if tag2_button != None:
                            tag2_button.Model.ImageURL = url
                    except:
                        pass
                    
                    self.mb.tree_write(tree,Path)
        except:
            log(inspect.stack,tb())

    
    def galerie_icon_im_prj_ordner_speichern(self,url):  
        if self.mb.debug: log(inspect.stack)
        
        try:            
            url = uno.fileUrlToSystemPath(url)
            pfad_icons_prj_ordner = self.mb.pfade['icons']
            name = os.path.basename(url)
            neuer_pfad = os.path.join(pfad_icons_prj_ordner,name)

            if not os.path.exists(neuer_pfad):
                copyfile(url, neuer_pfad)
                
            return uno.systemPathToFileUrl(neuer_pfad)

        except:
            log(inspect.stack,tb())
    
    def galerie_icon_im_prj_ordner_evt_loeschen(self): 
        if self.mb.debug: log(inspect.stack)
        
        try:
            tree = self.mb.props['ORGANON'].xml_tree
            root = tree.getroot()
            
            ord_xml = root.find('.//' + self.ordinal)
            url = ord_xml.attrib['Tag2']
            
            if 'uno_packages' in url:
                return
            all_xml = root.findall('.//')
            
            for el in all_xml:
                if el.tag == self.ordinal:
                    continue
                if el.attrib['Tag2'] == url:
                    return
    
            # Wenn die url nicht mehr im Dokument vorhanden ist, wird sie geloescht
            os.remove(uno.fileUrlToSystemPath(url))
        except:
            log(inspect.stack,tb())
            
    
    def icon_in_calc_anpassen(self,ord_source,url):
        if self.mb.debug: log(inspect.stack) 
        try:
            # ctx von calc
            ctx = uno.getComponentContext()
            smgr = ctx.ServiceManager
            desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
            
            draw_page = desktop.CurrentComponent.DrawPages.getByIndex(0)
            
            form = draw_page.Forms.getByName('IMGU_'+ ord_source)
            form.ControlModels[0].setPropertyValue('ImageURL',url)
            
            if url == '':
                form.ControlModels[0].setPropertyValue('Border',2)
                form.ControlModels[0].setPropertyValue('BorderColor',4147801)
            else:
                form.ControlModels[0].setPropertyValue('Border',0)
                hintergrund = self.mb.settings_orga['organon_farben']['office']['dok_hintergrund']
                form.ControlModels[0].setPropertyValue('BorderColor',hintergrund)
                
        except:
            log(inspect.stack,tb())
            
   
    def mouseExited(self, ev): 
        ev.value.Source.Model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
        return False
    def mouseEntered(self, ev):   
        ev.value.Source.Model.BackgroundColor = KONST.FARBE_GEZOGENE_ZEILE
        return False
    def mouseReleased(self,ev):
        return False
    def disposing(self,ev):
        return False
        
             
class Tag1_Item_Listener(unohelper.Base, XItemListener):
    def __init__(self,mb,window,ord_source):
        if mb.debug: log(inspect.stack)
        self.mb = mb
        self.window = window
        self.ord_source = ord_source
        self.window_parent = None
        
    def itemStateChanged(self, ev):   
        if self.mb.debug: log(inspect.stack) 
        
        try:
            sel = ev.value.Source.Items[ev.value.Selected]
            sel = self.mb.class_Funktionen.items[sel]
            
            # image tag1 aendern
            src = self.mb.props[T.AB].Hauptfeld.getControl(self.ord_source).getControl('tag1')
            if src != None:
                src.Model.ImageURL = KONST.URL_IMGS+'punkt_%s.png' %sel
    
            url = self.tag1_in_allen_tabs_xml_anpassen(self.ord_source,sel)
            
            # Wenn von Calc gerufen
            if self.window_parent != None:
                self.icon_in_calc_anpassen(self.ord_source,url)
    
            self.window.dispose()
        except:
            log(inspect.stack,tb())

    def tag1_in_allen_tabs_xml_anpassen(self,ord_source,sel):
        if self.mb.debug: log(inspect.stack) 
        
        try:
            tabnamen = self.mb.props.keys()
            
            for name in tabnamen:
            
                tree = self.mb.props[name].xml_tree
                root = tree.getroot()        
                source_xml = root.find('.//'+ord_source)
                
                if source_xml != None:
                
                    source_xml.attrib['Tag1'] = sel
                    
                    if name == 'ORGANON':
                        Path = os.path.join(self.mb.pfade['settings'], 'ElementTree.xml')
                    else:
                        Path = os.path.join(self.mb.pfade['tabs'], name + '.xml')
                        
                    try:
                        # Wenn noch nicht alle Tabs aufgerufen worden sind, existieren manche
                        # Hauptfelder noch nicht. Daher try/except als schnelle Loesung
                        tag1_button = self.mb.props[name].Hauptfeld.getControl(ord_source).getControl('tag1')
                        if tag1_button != None:
                            tag1_button.Model.ImageURL = KONST.URL_IMGS+'punkt_%s.png' %sel
                    except:
                        pass
                    
                    self.mb.tree_write(tree,Path)
                    
            return KONST.URL_IMGS+'punkt_%s.png' %sel
        except:
            log(inspect.stack,tb())


    def icon_in_calc_anpassen(self,ord_source,url):
        if self.mb.debug: log(inspect.stack) 
        try:
            # ctx von calc
            ctx = uno.getComponentContext()
            smgr = ctx.ServiceManager
            desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
            
            draw_page = desktop.CurrentComponent.DrawPages.getByIndex(0)
            
            form = draw_page.Forms.getByName('IMG_'+ ord_source)
            form.ControlModels[0].setPropertyValue('ImageURL',url)
            
            if 'punkt_leer' in url:
                form.ControlModels[0].setPropertyValue('Border',2)
                form.ControlModels[0].setPropertyValue('BorderColor',4147801)
            else:
                form.ControlModels[0].setPropertyValue('Border',0)
                hintergrund = self.mb.settings_orga['organon_farben']['office']['dok_hintergrund']
                form.ControlModels[0].setPropertyValue('BorderColor',hintergrund)
            
        except:
            log(inspect.stack,tb())
            
