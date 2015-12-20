# -*- coding: utf-8 -*-
import uno
import unohelper
from traceback import format_exc as tb
import sys
from os import walk,path,remove
from codecs import open as codecs_open
from inspect import stack as inspect_stack
from shutil import copyfile
import json


platform = sys.platform



class Menu_Start():
    
    def __init__(self,args):
        
        (pdk,
         dialog,
         ctx,
         path_to_extension,
         win,
         dict_sb,
         debugX,
         factory,
         logX,
         class_LogX,
         konst,
         settings_orga) = args
        
        global debug,log,class_Log,KONST
        debug = debugX
        log = logX
        class_Log = class_LogX
        KONST = konst
        
        if debug: log(inspect_stack)      
        
        self.win = win
        self.pd = pdk
        global pd
        pd = pdk
        
        try:
             
            # Konstanten
            self.factory = factory
            self.dialog = dialog
            self.ctx = ctx
            self.smgr = self.ctx.ServiceManager
            self.desktop = self.smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",self.ctx)
            self.doc = self.get_doc()
            self.path_to_extension = path_to_extension
            self.programm = self.get_office_name()
            self.platform = sys.platform
            self.language = None
            self.LANG = self.lade_Modul_Language()
            self.settings_orga = settings_orga 
            self.zuletzt_geladene_Projekte = self.get_zuletzt_geladene_Projekte()
            self.dict_sb = dict_sb
            self.dict_sb['setze_sidebar_design'] = self.setze_sidebar_design
            self.templates = {}
            
            try:
                self.templates.update({'standard_stil':self.get_stil(),
                                       'get_stil':self.get_stil})
                
                if self.settings_orga['organon_farben']['design_office']:
                    event_listener = Listener_Erzeugt_Seitenleiste_Bei_OrgaDesign(self)
                    self.doc.addDocumentEventListener(event_listener)

            except:
                log(inspect_stack,tb())
                
            
            
        except Exception as e:
            log(inspect_stack,tb())
        
    
    
    def wurde_als_template_geoeffnet(self):
        if debug: log(inspect_stack)
        try:
            enum = self.desktop.Components.createEnumeration()
            comps = []

            while enum.hasMoreElements():
                comps.append(enum.nextElement())
                
            # Wenn ein neues Dokument geoeffnet wird, gibt es bei der Initialisierung
            # noch kein Fenster, aber die Komponente wird schon aufgefuehrt.
            doc = comps[0]
            
            # Pruefen, ob doc von Organon erzeugt wurde
            ok = False
            for a in doc.Args:
                if a.Name == 'DocumentTitle':
                    if a.Value.split(';')[0] == 'opened by Organon':
                        ok = True
                        projekt_pfad = a.Value.split(';')[1]
                        break
            
            if not ok:
                return False        
            

        
#             # Das Editfeld ueberdeckt kurzzeitig das Startmenu fuer eine bessere Anzeige
#             control, model = self.createControl(self.ctx,"Edit",0,0,1500,1500,(),() )  
#             model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
#             self.cont.addControl('wer',control)
            
            self.cont.dispose()
            self.erzeuge_Menu()
            
            prop2 = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop2.Name = 'Overwrite'
            prop2.Value = True
            
            doc.storeAsURL(projekt_pfad,(prop2,)) 
            
            sys_pfad = uno.fileUrlToSystemPath(projekt_pfad)
            orga_name = path.basename(sys_pfad).split('.')[0] + '.organon'
            sys_pfad1 = sys_pfad.split(orga_name)[0]
            pfad = path.join(sys_pfad1,orga_name,orga_name)
            

            self.Menu_Bar.class_Projekt.lade_Projekt(False,pfad)
            
          
        except:
            log(inspect_stack,tb())

    def get_office_name(self):
        if debug: log(inspect_stack)
        frame = self.desktop.Frames.getByIndex(0)

        if 'LibreOffice' in frame.Title:
            programm = 'LibreOffice'
        elif 'OpenOffice' in frame.Title:
            programm = 'OpenOffice'
        else:
            # Fuer Linux / OSX fehlt
            programm = 'LibreOffice'
        
        return programm
       
    def erzeuge_Startmenu(self):
        if debug: log(inspect_stack)
            
        # Hauptfeld_Aussen
        Attr = (0,0,1000,1800,'Hauptfeld_aussen1', 0)    
        PosX,PosY,Width,Height,Name,Color = Attr
        
        self.cont, model1 = self.createControl(self.ctx,"Container",PosX,PosY,Width,Height,(),() )  
        model1.BackgroundColor = KONST.FARBE_HF_HINTERGRUND

        self.dialog.addControl('Hauptfeld_aussen1',self.cont)  


        Attr = (160,60,120,153,'Hauptfeld_aussen1', 0)    
        PosX,PosY,Width,Height,Name,Color = Attr
        
        control, model = self.createControl(self.ctx,"ImageControl",PosX,PosY,Width,Height,(),() )  
        
        model.ImageURL = 'vnd.sun.star.extension://xaver.roemers.organon/img/organon icon_120.png' 
        model.Border = False   
        model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
        self.cont.addControl('Hauptfeld_aussen1',control)  
        
       
        self.listener = Menu_Listener(self)
        
        
        PosX = 25
        PosY = 50
        Width = 110
        Height = 30
        
        control, model = self.createControl(self.ctx,"Button",PosX,PosY,Width,Height,(),() )  
        control.setActionCommand('neues_projekt')
        control.addActionListener(self.listener)
        model.Label = self.LANG.NEW_PROJECT
        #model.BackgroundColor = 501#KONST.FARBE_HF_HINTERGRUND
  
        #model.TextLineColor = 501
        
        #setattr(self.cont.StyleSettings, 'WorkspaceColor', 501)
        
        
        self.cont.addControl('Hauptfeld_aussen1',control)  
        
        PosY += 50
        
        control, model = self.createControl(self.ctx,"Button",PosX,PosY,Width,Height,(),() )  
        control.setActionCommand('projekt_laden')
        control.addActionListener(self.listener)
        model.Label = self.LANG.OPEN_PROJECT
        model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
                
        self.cont.addControl('Hauptfeld_aussen1',control) 
        
        
        PosY += 70
        
        control, model = self.createControl(self.ctx,"Button",PosX,PosY,Width,Height,(),() )  
        control.setActionCommand('anleitung_laden')
        control.addActionListener(self.listener)
        model.Label = self.LANG.LOAD_DESCRIPTION
        model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
        
        self.cont.addControl('Hauptfeld_aussen1',control) 
        
        PosY += 150
        
        if self.zuletzt_geladene_Projekte == []:
            return

        for proj in self.zuletzt_geladene_Projekte:
            
            
            name,pfad = proj
            
            control, model = self.createControl(self.ctx,"FixedText",PosX,PosY,200,20,(),() )  
            control.addMouseListener(self.listener)
            model.Label = name
            model.TextColor = KONST.FARBE_SCHRIFT_DATEI
            model.HelpText = pfad
            self.cont.addControl('Hauptfeld_aussen1',control) 
            PosY += 25

        ist_template = self.wurde_als_template_geoeffnet()
        if not ist_template:
            pass
        
        
    def erzeuge_Menu(self):
        if debug: log(inspect_stack)
          
        try:   
            import menu_bar
            
            args = (pd,
                    self.dialog,
                    self.ctx,
                    self.path_to_extension,
                    self.win,
                    self.dict_sb,
                    debug,
                    self.factory,
                    self,
                    log,
                    class_Log,
                    self.settings_orga,
                    self.templates
                    )
            import time
            class_Log.timer_start = time.clock()
            self.module_mb = menu_bar
            
            self.Menu_Bar = menu_bar.Menu_Bar(args)
            self.Menu_Bar.erzeuge_Menu(self.Menu_Bar.prj_tab)

        except:
            log(inspect.stack,tb())    
    
     
              
    def lade_Modul_Language(self):
        if debug: log(inspect_stack)
        try:  
            enum = self.desktop.Components.createEnumeration()
            comps = []
            
            while enum.hasMoreElements():
                comps.append(enum.nextElement())
    
            language = comps[0].CharLocale.Language
            
#             if language not in ('de'):
#                 language = 'en'
                
            self.language = language
            
            import lang_en 
            
            try:
                exec('import lang_' + language)
            except Exception as e:
                pass
                #log(inspect_stack,tb())    
    
            if 'lang_' + language in vars():
                lang = vars()['lang_' + language]
            else:
                lang = lang_en
            
            return lang
        except Exception as e:
            log(inspect_stack,tb())    
    
    
    def get_zuletzt_geladene_Projekte(self):
        if debug: log(inspect_stack)
        
        try:
            projekte = self.settings_orga['zuletzt_geladene_Projekte']
            
            # Fuer projekte erstellt vor v0.9.9.8b
            if isinstance(projekte, dict):
                list_proj = list(projekte)
                projekte = [[p,projekte[p]] for p in list_proj]
                
            
            inexistent = [p for p in projekte if not path.exists(p[1])]
            
            for i in inexistent:
                index = projekte.index(i)
                del(projekte[index])
                
            self.settings_orga['zuletzt_geladene_Projekte'] = projekte
            
            return projekte
        except Exception as e:
            print(e)
            try:
                if debug: log(inspect_stack,tb())
            except:
                pass
        return []
    
    def get_doc(self):
        if debug: log(inspect_stack)
        
        enum = self.desktop.Components.createEnumeration()
        comps = []
        
        while enum.hasMoreElements():
            comps.append(enum.nextElement())
            
        # Wenn ein neues Dokument geoeffnet wird, gibt es bei der Initialisierung
        # noch kein Fenster, aber die Komponente wird schon aufgefuehrt.
        # Hat die zuletzt erzeugte Komponente comps[0] kein ViewData,
        # dann wurde sie neu geoeffnet.
        if comps[0].ViewData == None:
            doc = comps[0]
        else:
            doc = self.desktop.getCurrentComponent() 
            
        return doc
    
    def get_stil(self):
        if debug: log(inspect_stack)

        try:
            ctx = uno.getComponentContext()
            smgr = ctx.ServiceManager
            desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
            doc = desktop.getCurrentComponent() 
            
            if doc == None:
                doc = self.get_doc()                
            
            oStyleFamilies = doc.StyleFamilies 
            oPageStyles = oStyleFamilies.getByName("PageStyles")
            oDefaultStyle = oPageStyles.getByName("Standard")
            
            style = {}
            
            nicht_nutzbar_OO = ['DisplayName','FooterText','FooterTextLeft','FooterTextRight',
                            'HeaderText','HeaderTextLeft','HeaderTextRight',
                            'ImplementationName','IsPhysical','Name','ParentStyle',
                            'PropertiesToDefault','PropertyToDefault'
                            ]
            
            nicht_nutzbar_LO = ['DisplayName','FooterText','FooterTextLeft','FooterTextRight',
                            'HeaderText','HeaderTextLeft','HeaderTextRight',
                            'ImplementationName','IsPhysical','Name','ParentStyle',
                            'PropertiesToDefault','PropertyToDefault',
    
                            'FillBitmap','FooterTextFirst','HeaderTextFirst',
                            'FillBackground','FillBitmapLogicalSize','FillBitmapMode',
                            'FillBitmapName','FillBitmapOffsetX','FillBitmapOffsetY',
                            'FillBitmapPositionOffsetX','FillBitmapPositionOffsetY',
                            'FillBitmapRectanglePoint','FillBitmapSizeX','FillBitmapSizeY',
                            'FillBitmapStretch','FillBitmapTile','FillColor',
                            'FillGradient','FillGradientName','FillGradientStepCount',
                            'FillHatch','FillHatchName','FillStyle','FillTransparence',
                            'FillTransparenceGradient','FillTransparenceGradientName',
                            'FooterIsShared','HeaderIsShared'
                            ]
            
            for o in dir(oDefaultStyle):
                value = getattr(oDefaultStyle,o)
                if type(value) in [str,int,type(u''),bool,type(None)]:
                    style.update({o:value})
                    
            if self.programm == 'OpenOffice':
                nicht_nutzbar = nicht_nutzbar_OO
            else:
                nicht_nutzbar = nicht_nutzbar_LO
                    
            default_template_style = {s:style[s] for s in style}# if s[0] not in nicht_nutzbar}
            
            #log(inspect_stack,extras=str(len(default_template_style)))
            
        except Exception as e:
            log(inspect_stack,tb())
            return {}
        
        return default_template_style


    def setze_sidebar_design(self): 
        # In LO wird setze_sidebar_design bei aktivem Design durch 
        # einen Thread gerufen. Globale Variablen stehen nicht zur
        # Verfuegung, daher wird inspect erneut importiert.
        import inspect
        
        if debug: log(inspect.stack)
        try:
            
            def get_farbe(value):
                if isinstance(value, int):
                    return value
                else:
                    return self.settings_orga['organon_farben'][value]
            
            
            personen = self.dict_sb['controls']['organon_sidebar']
            theme = personen[0].Theme
    
            
            sett = self.settings_orga['organon_farben']['office']['sidebar']
            
            hintergrund = get_farbe(sett['hintergrund'])
            schrift = get_farbe(sett['schrift'])
            
            titel_hintergrund = get_farbe(sett['titel_hintergrund'])
            titel_schrift = get_farbe(sett['titel_schrift'])
            
            panel_titel_hintergrund = get_farbe(sett['panel_titel_hintergrund'])
            panel_titel_schrift = get_farbe(sett['panel_titel_schrift'])
    
            leiste_hintergrund = get_farbe(sett['leiste_hintergrund'])
            leiste_selektiert_hintergrund = get_farbe(sett['leiste_selektiert_hintergrund'])
            leiste_icon_umrandung = get_farbe(sett['leiste_icon_umrandung'])
            
            border_horizontal = get_farbe(sett['border_horizontal'])
            border_vertical = get_farbe(sett['border_vertical'])
            
            # folgende muessen bereits in factory.py gesetzt werden
            # selected_schrift, eigene_fenster_hintergrund, schrift, selected_hintergrund
            
            
            # Tabbar  
            theme.setPropertyValue('Paint_TabBarBackground', leiste_hintergrund)
            theme.setPropertyValue('Paint_TabItemBackgroundNormal', leiste_hintergrund)
            theme.setPropertyValue('Color_TabMenuSeparator', leiste_hintergrund)
            theme.setPropertyValue('Paint_TabItemBackgroundHighlight', leiste_selektiert_hintergrund)
            theme.setPropertyValue('Color_TabItemBorder', leiste_icon_umrandung)            
            theme.setPropertyValue('Int_ButtonCornerRadius', 0)
            
            # Hintergruende
            theme.setPropertyValue('Paint_PanelBackground', hintergrund)
            theme.setPropertyValue('Paint_DeckBackground', hintergrund)
            theme.setPropertyValue('Paint_DeckTitleBarBackground', titel_hintergrund)
            
            tbb = theme.Paint_PanelTitleBarBackground
            tbb.StartColor = panel_titel_hintergrund
            tbb.EndColor = panel_titel_hintergrund
            theme.setPropertyValue('Paint_PanelTitleBarBackground', tbb)
    
            # Borders
            theme.setPropertyValue('Paint_HorizontalBorder', border_horizontal)
            theme.setPropertyValue('Paint_VerticalBorder', border_vertical)
            
            # Schriften
            theme.setPropertyValue('Color_DeckTitleFont', titel_schrift)
            theme.setPropertyValue('Color_PanelTitleFont', panel_titel_schrift)
            
    
            theme.setPropertyValue('Paint_ToolBoxBorderBottomRight', hintergrund) # buttons Umrandung
            theme.setPropertyValue('Paint_ToolBoxBorderTopLeft', hintergrund) # buttons Umrandung
    
            tbb = theme.Paint_ToolBoxBackground # buttons Hintergrund
            tbb.StartColor = hintergrund 
            tbb.EndColor = hintergrund
            theme.setPropertyValue('Paint_ToolBoxBackground', tbb)
            
            rot = 16275544
                       
            theme.setPropertyValue('Paint_DropDownBackground', rot)
            theme.setPropertyValue('Paint_ToolBoxBorderCenterCorners', rot) #??? 
            theme.setPropertyValue('Color_Highlight', rot)
            theme.setPropertyValue('Color_HighlightText', rot)
            theme.setPropertyValue('Color_DropDownBorder', rot)
            theme.setPropertyValue('Color_PanelTitleFont', rot)
            
            # Panel Titel
            dict_sb = self.dict_sb
            sl = dict_sb['seitenleiste']
            
            if sl:
                try:
                    # erzeugt in fedora xfce einen fehler
                    sl.StyleSettings.ButtonTextColor = schrift
                except:
                    pass
                self.dict_sb['design_gesetzt'] = True

            sb = personen[1]
            sb.requestLayout()
            
            
            
            
        except:
            log(inspect.stack,tb())
            
        
   
    # Handy function provided by hanya (from the OOo forums) to create a control, model.
    def createControl(self,ctx,type,x,y,width,height,names,values):
        smgr = ctx.getServiceManager()
        ctrl = smgr.createInstanceWithContext("com.sun.star.awt.UnoControl%s" % type,ctx)
        ctrl_model = smgr.createInstanceWithContext("com.sun.star.awt.UnoControl%sModel" % type,ctx)
        ctrl_model.setPropertyValues(names,values)
        ctrl.setModel(ctrl_model)
        ctrl.setPosSize(x,y,width,height,15)
        return (ctrl, ctrl_model)
    
    def createUnoService(self,serviceName):
        sm = uno.getComponentContext().ServiceManager
        return sm.createInstanceWithContext(serviceName, uno.getComponentContext())




from com.sun.star.awt import XActionListener,XMouseListener
    
class Menu_Listener (unohelper.Base, XActionListener,XMouseListener):
    def __init__(self,menu):
        self.menu = menu

    def actionPerformed(self, ev):
        if debug: log(inspect_stack)
        
        try:
            if ev.ActionCommand == 'neues_projekt':
                self.menu.cont.dispose()
                self.menu.erzeuge_Menu()
                self.menu.Menu_Bar.class_Projekt.erzeuge_neues_Projekt()
                
            elif ev.ActionCommand == 'projekt_laden':
                self.menu.cont.dispose()
                self.menu.erzeuge_Menu()
                self.menu.Menu_Bar.class_Projekt.lade_Projekt()
                
            elif ev.ActionCommand == 'anleitung_laden':
                pfad = self.get_Org_description_path()
                self.menu.cont.dispose()
                self.menu.erzeuge_Menu()
                self.menu.Menu_Bar.class_Projekt.lade_Projekt(False,pfad)
                self.menu.Menu_Bar.anleitung_geladen = True
        except:
            log(inspect.stack,tb())
            
    def get_Org_description_path(self):
        if debug: log(inspect_stack)
        
        path_HB = path.join(self.menu.path_to_extension,'description','Handbuecher')

        ordner = []
        for (dirpath, dirnames, filenames) in walk(path_HB):
            ordner.extend(dirnames)
            break
        
        if self.menu.language in ordner:
            path_HB = path.join(path_HB,self.menu.language)
        else:
            path_HB = path.join(path_HB,'en')
            
        projekt_name = []
        for (dirpath, dirnames, filenames) in walk(path_HB):
            projekt_name.extend(dirnames)
            break
        
        desc_path = path.join(path_HB,projekt_name[0],projekt_name[0])
        return desc_path
    
    def mouseReleased(self, ev):  
        return False
    def mouseExited(self,ev):
        return False
    def mouseEntered(self,ev):
        return False
    
    def mousePressed(self, ev):
        if debug: log(inspect_stack)
        
        try:
            projekt_pfad = ev.Source.Model.HelpText
            
            # Das Editfeld ueberdeckt kurzzeitig das Startmenu fuer eine bessere Anzeige
            control, model = self.menu.createControl(self.menu.ctx,"Edit",0,0,1500,1500,(),() )  
            model.BackgroundColor = KONST.FARBE_HF_HINTERGRUND
            self.menu.cont.addControl('wer',control)
    
            self.menu.erzeuge_Menu()
            self.menu.Menu_Bar.class_Projekt.lade_Projekt(False,projekt_pfad)
            
            self.menu.cont.dispose()
        except:
            log(inspect.stack,tb())
        
    def disposing(self,ev):
        pass
           

from com.sun.star.document import XDocumentEventListener
class Listener_Erzeugt_Seitenleiste_Bei_OrgaDesign(unohelper.Base,XDocumentEventListener):

    def __init__(self,ms):
        if debug: log(inspect_stack)
        self.ms = ms

    def documentEventOccured(self,ev):        
        
        if ev.EventName == 'OnLayoutFinished':
            
            # Abfrage, ob ueberhaupt ein Layout fuer die 
            # Seitenleiste erzeugt werden soll, fehlt.
            # TODO: Design Seitenleiste und Design Organon insgesamt trennen,
            # da die Seitenleiste jetzt ohne Neustart designed werden kann.
            # Evt. gilt das aber auch für das gesamte Dokument
            
            ctrl = self.ms.dict_sb['controls']
            
            if 'organon_sidebar' not in ctrl:
                if debug: log(inspect_stack)
                
                self.seitenleiste_erzeugen()
                
            self.ms.doc.removeDocumentEventListener(self)
      
    def disposing(self,ev):
        return False
    
    def seitenleiste_erzeugen(self):
        if debug: log(inspect_stack)
        
        try:       
            def get_seitenleiste():
                
                desk = self.ms.desktop
                contr = desk.CurrentComponent.CurrentController
                wins = contr.ComponentWindow.Windows
                
                childs = []
                
                from com.sun.star.uno.TypeClass import INTERFACE
                otype = uno.Type('com.sun.star.awt.XTopWindow2',INTERFACE)
        
                for w in wins:
                    if not w.isVisible():continue
                    
                    if w.AccessibleContext.AccessibleChildCount == 0:
                        continue
                    else:
                        child = w.AccessibleContext.getAccessibleChild(0)
                        if 'Organon: dockable window' == child.AccessibleContext.AccessibleName:
                            continue
                        if otype not in child.Types:
                            continue
                        else:
                            childs.append(child)
                            
                orga_sb = None
                if len(childs) == 1:
                    seitenleiste = childs[0]
                else:
                    seitenleiste = None
                
                if seitenleiste:
                    for w in seitenleiste.Windows:
                        try:
                            for w2 in w.Windows:
                                if w2.AccessibleContext.AccessibleDescription == 'Organon':
                                    orga_sb = w2
                        except:
                            pass
                
                return orga_sb,seitenleiste
            
                        
            def dispatch2(cmd,oprop=('',None)):
                    
                    if debug: log(inspect_stack,extras='dispatch erzeugt')
                    sm = uno.getComponentContext().ServiceManager
                    dispatcher = sm.createInstanceWithContext("com.sun.star.frame.DispatchHelper", uno.getComponentContext())
                    
                    prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
                       
                    prop.Name = oprop[0]
                    prop.Value = oprop[1]
                    
                    res = dispatcher.executeDispatch(self.ms.desktop.ActiveFrame, ".uno:{}".format(cmd), "", 0, (prop,))
            
            
            
            def sl_erzeugen():

                def sleeper(fkt,fkt2,dict_sb,orga_sb): 
                    
                    import time
                    
                    while orga_sb == None:
                        time.sleep(.1) 
                        orga_sb,seitenleiste = fkt()
                        
                    fkt2(orga_sb,dict_sb)
            
                def resume(orga_sb,dict_sb): 
                    
                    orga_sb.setState(True)  
                    
                    import time 
                    time.sleep(.2) 
                    dict_sb['setze_sidebar_design']()
                    dict_sb['sb_closed'] = False
                    dict_sb['orga_sb'] = orga_sb
                    
                    
                try:   
                    dict_sb = self.ms.dict_sb
                    orga_sb,seitenleiste = get_seitenleiste()
                    
                    if seitenleiste and not orga_sb:
                        # LO
                        dict_sb['seitenleiste'] = seitenleiste
                        
                        from threading import Thread
                        t = Thread(target=sleeper,args=(get_seitenleiste,resume,dict_sb,orga_sb))
                        t.start() 
                        
                    elif seitenleiste and orga_sb:
                        # OO
                        orga_sb.setState(True)   
                        dict_sb['setze_sidebar_design']()
                        dict_sb['sb_closed'] = False
                        dict_sb['seitenleiste'] = seitenleiste
                        dict_sb['orga_sb'] = orga_sb

                except:
                    log(inspect_stack,tb())
            
            t = sl_erzeugen()

        except:
            log(inspect_stack,tb())
            

   
    def set_seitenleiste_stiel_OO(self,seitenleiste):
        if debug: log(inspect_stack)
        try:
            ctx = uno.getComponentContext()
            smgr = ctx.ServiceManager
            toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)    
            desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
            frame = desktop.Frames.getByIndex(0)
            comp = frame.ComponentWindow
            
            rot = 16275544
    
            hf = KONST.FARBE_HF_HINTERGRUND
            menu = KONST.FARBE_MENU_HINTERGRUND
            schrift = KONST.FARBE_SCHRIFT_DATEI
            menu_schrift = KONST.FARBE_MENU_SCHRIFT
            selected = KONST.FARBE_AUSGEWAEHLTE_ZEILE
            ordner = KONST.FARBE_SCHRIFT_ORDNER
            
            sett = self.ms.settings_orga['organon_farben']['office']
            
            def get_farbe(value):
                if isinstance(value, int):
                    return value
                else:
                    return self.ms.settings_orga['organon_farben'][value]
            
            # Kann button_schrift evt. herausgenommen werden?
            button_schrift = get_farbe(sett['button_schrift'])
            
            statusleiste_schrift = get_farbe(sett['statusleiste_schrift'])
            statusleiste_hintergrund = get_farbe(sett['statusleiste_hintergrund'])
            
            felder_hintergrund = get_farbe(sett['felder_hintergrund'])
            felder_schrift = get_farbe(sett['felder_schrift'])
            
            # Sidebar
            sidebar_eigene_fenster_hintergrund = get_farbe(sett['sidebar']['eigene_fenster_hintergrund'])
            sidebar_selected_hintergrund = get_farbe(sett['sidebar']['selected_hintergrund'])
            sidebar_selected_schrift = get_farbe(sett['sidebar']['selected_schrift'])
            sidebar_schrift = get_farbe(sett['sidebar']['schrift'])
            
            trenner_licht = get_farbe(sett['trenner_licht'])
            trenner_schatten = get_farbe(sett['trenner_schatten'])
            
            # Lineal
            OO_anfasser_trenner = get_farbe(sett['OO_anfasser_trenner'])
            OO_lineal_tab_zwischenraum = get_farbe(sett['OO_lineal_tab_zwischenraum'])
            OO_schrift_lineal_sb_liste = get_farbe(sett['OO_schrift_lineal_sb_liste'])
            
            LO_anfasser_text = get_farbe(sett['LO_anfasser_text'])
            LO_tabsumrandung = get_farbe(sett['LO_tabsumrandung'])
            LO_lineal_bg_innen = get_farbe(sett['LO_lineal_bg_innen'])
            LO_tab_fuellung = get_farbe(sett['LO_tab_fuellung'])
            LO_tab_trenner = get_farbe(sett['LO_tab_trenner'])
            
            
            LO = ('LibreOffice' in frame.Title)
            
            STYLES = {  
                      # Allgemein
                        'ButtonRolloverTextColor' : button_schrift, # button rollover
                        
                        'FieldColor' : felder_hintergrund, # Hintergrund Eingabefelder
                        'FieldTextColor' : felder_schrift,# Schrift Eingabefelder
                        
                        # Trenner
                        'LightColor' : trenner_licht, # Fenster Trenner
                        'ShadowColor' : trenner_schatten, # Fenster Trenner
                        
                        # OO Lineal + Trenner
                         
                        'DarkShadowColor' : (LO_anfasser_text if LO    # LO Anfasser + Lineal Text
                                            else OO_anfasser_trenner), # OO Anfasser +  Document Fenster Trenner 
                        'WindowTextColor' : (schrift if LO      # Felder (Navi) Schriftfarbe Sidebar 
                                             else OO_schrift_lineal_sb_liste),     # Felder (Navi) Schriftfarbe Sidebar + OO Lineal Schriftfarbe   
                            
                        # Sidebar
                        'LabelTextColor' : sidebar_schrift, # Schriftfarbe Sidebar + allg Dialog
                        'DialogColor' : sidebar_eigene_fenster_hintergrund, # Hintergrund Sidebar Dialog
                        'FaceColor' : (hf if LO        # LO Formatvorlagen Treeview Verbinder
                                        else hf),           # OO Hintergrund Organon + Lineal + Dropdowns  
                        'WindowColor' : (hf if LO                           # LO Dialog Hintergrund
                                        else OO_lineal_tab_zwischenraum),   # OO Lineal Tabzwischenraum
                        'HighlightColor' : sidebar_selected_hintergrund, # Sidebar selected Hintergrund
                        'HighlightTextColor' : sidebar_selected_schrift, # Sidebar selected Schrift
                        
                        
#                         'ActiveBorderColor' : rot,#k.A.
#                         'ActiveColor' : rot,#k.A.
#                         'ActiveTabColor' : rot,#k.A.
#                         'ActiveTextColor' : rot,#k.A.
#                         'ButtonTextColor' : rot,# button Textfarbe / LO Statuszeile Textfarbe
#                         'CheckedColor' : rot,#k.A.
#                         'DeactiveBorderColor' : rot,#k.A.
#                         'DeactiveColor' : rot,#k.A.
#                         'DeactiveTextColor' : rot,#k.A.
#                         'DialogTextColor' : rot,#k.A.
#                         'DisableColor' : rot,
#                         'FieldRolloverTextColor' : rot,#k.A.
#                         'GroupTextColor' : rot,#k.A.
#                         'HelpColor' : rot,#k.A.
#                         'HelpTextColor' : rot,#k.A.
#                         'InactiveTabColor' : rot,#k.A.
#                         'InfoTextColor' : rot,#k.A.
#                         'MenuBarColor' : rot,#k.A.
#                         'MenuBarTextColor' : rot,#k.A.
#                         'MenuBorderColor' : rot,#k.A.
#                         'MenuColor' : rot,#k.A.
#                         'MenuHighlightColor' : rot,#k.A.
#                         'MenuHighlightTextColor' : rot,#k.A.
#                         'MenuTextColor' : rot,#k.A.
#                         'MonoColor' : rot, #k.A.
#                         'RadioCheckTextColor' : rot,#k.A.
#                         'WorkspaceColor' : rot, #k.A.
#                         erzeugen Fehler:
#                         'FaceGradientColor' : 502,
#                         'SeparatorColor' : 502,                    
                        }
            
     
            def stilaenderung(win,ignore=[]):
    
                for s in STYLES:
                    if s in ignore: 
                        pass
                    else:
                        try:
                            val = STYLES[s]
                            setattr(win.StyleSettings, s, val)
                        except Exception as e:
                            pass
                        
                    win.setBackground(statusleiste_hintergrund) # Hintergrund Statuszeile
                    win.setForeground(statusleiste_schrift)     # Schrift Statuszeile
            
            
            
            
            stilaenderung(seitenleiste)
            
            
            
            
            
            return
        
            
            
        except Exception as e:
            log(inspect_stack,tb())
            

            

            
            
            
