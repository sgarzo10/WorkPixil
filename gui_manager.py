from pathlib import Path
import PySimpleGUI as sg
from work_pixil import WorkPixil


class GuiManager:

    def __init__(self):
        operation_list_column = [
            [sg.Text("SCEGLI L'OPERAZIONE")],
            [
                sg.Combo(
                    [
                        'read',
                        'gen',
                        'merge',
                        'ext',
                        'del'
                    ], size=(45, 1), enable_events=True, key='LIST_OP')
            ],
            [sg.Text("", size=(45, 5))],
            [sg.HorizontalSeparator()],
            [sg.Text("", key="LBL_HELP")],
        ]
        read_viewer_column = [
            [
                sg.Text("FILE PIXIL SORGENTE", size=(25, 1)),
                sg.In(size=(55, 1), enable_events=False, key="FILE_SOURCE"),
                sg.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source"),
            ],
            [
                sg.Text("PREMI IL PULSANTE PER LEGGERE I LAYER CONTENUTI NEL FILE", size=(80, 1)),
                sg.Button("LEGGI FILE", key="BUTTON_READ")
            ],
            [
                sg.Text("LISTA DEI LAYER (IN ORDINE) CONTENUTI NEL FILE SELEZIONATO", size=(80, 1)),
            ],
            [
                sg.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX", visible=False)
            ]
        ]
        gen_viewer_column = [
            [
                sg.Text("FILE PIXIL SORGENTE", size=(25, 1)),
                sg.In(size=(55, 1), enable_events=False, key="FILE_GEN_SOURCE"),
                sg.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source"),
            ],
            [
                sg.Text("FILE JSON TEMPLATE", size=(25, 1)),
                sg.In(size=(55, 1), enable_events=False, key="FILE_GEN_TEMPLATE"),
                sg.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/template"),
            ],
            [
                sg.Text("PREMI IL PULSANTE PER GENERARE UN'IMMAGINE", size=(75, 1)),
                sg.Button("GENERA IMMAGINE", key="BUTTON_GEN")
            ],
            [
                sg.Text("IMMAGINE GENERATA", size=(20, 1)),
                sg.Text("LISTA DEI LAYER (IN ORDINE) CONTENUTI NELL'IMMAGINE GENERATA", size=(60, 1)),
            ],
            [
                sg.Image(key="IMAGE_GEN"),
                sg.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_GEN", visible=False)
            ]
        ]
        merge_viewer_column = [
            [
                sg.Text("FILE PIXIL SORGENTE", size=(25, 1)),
                sg.In(size=(55, 1), enable_events=False, key="FILE_MERGE_SOURCE"),
                sg.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source"),
            ],
            [
                sg.Text("FILE PIXIL DA MERGIARE", size=(25, 1)),
                sg.In(size=(55, 1), enable_events=False, key="FILE_MERGE_ADD"),
                sg.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source"),
            ],
            [
                sg.Text("SCEGLI LA POSIZIONE A CUI INSERIRE I NUOVI LAYER", size=(75, 1)),
                sg.In(size=(5, 1), enable_events=False, key="POS_MERGE")
            ],
            [
                sg.Text("PREMI IL PULSANTE PER UNIRE I DUE FILE", size=(75, 1)),
                sg.Button("MERGIA FILE", key="BUTTON_MERGE")
            ],
            [
                sg.Text("LISTA DEI LAYER (IN ORDINE) CONTENUTI NEL FILE PIXIL GENERATO DAL MERGE", size=(80, 1)),
            ],
            [sg.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_MERGE", visible=False)]
        ]
        ext_viewer_column = [
            [
                sg.Text("FILE PIXIL SORGENTE", size=(25, 1)),
                sg.In(size=(55, 1), enable_events=False, key="FILE_EXT_SOURCE"),
                sg.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source"),
            ],
            [
                sg.Text("SCEGLI I LAYER DA ESTARRE (SEPARATI DA VIRGOLA)", size=(65, 1)),
                sg.In(size=(15, 1), enable_events=False, key="EXP_EXT")
            ],
            [
                sg.Text("PREMI IL PULSANTE PER CREARE UN FILE CON SOLO I LAYER SCELTI", size=(75, 1)),
                sg.Button("ESTRAI LAYER", key="BUTTON_EXT")
            ],
            [
                sg.Text("LISTA DEI LAYER (IN ORDINE) CONTENUTI NEL FILE PIXIL GENERATO DALL'ESTRAZIONE", size=(80, 1)),
            ],
            [sg.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_EXT", visible=False)]
        ]
        del_viewer_column = [
            [
                sg.Text("FILE PIXIL SORGENTE", size=(25, 1)),
                sg.In(size=(55, 1), enable_events=False, key="FILE_DEL_SOURCE"),
                sg.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source"),
            ],
            [
                sg.Text("SCEGLI I LAYER DA ELIMINARE (SEPARATI DA VIRGOLA)", size=(65, 1)),
                sg.In(size=(15, 1), enable_events=False, key="EXP_DEL")
            ],
            [
                sg.Text("PREMI IL PULSANTE PER RIMUOVERE DAL FILE SORGENTE I LAYER SCELTI", size=(75, 1)),
                sg.Button("ELIMINA LAYER", key="BUTTON_DEL")
            ],
            [
                sg.Text("LISTA DEI LAYER (IN ORDINE) RIMASTI NEL FILE PIXIL", size=(50, 1)),
                sg.Text("LISTA DEI LAYER (IN ORDINE) RIMOSSI DAL FILE PIXIL", size=(50, 1)),
            ],
            [
                sg.Column([[sg.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_REMAIN", visible=False)]]),
                sg.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_DEL", visible=False)
            ]
        ]
        layout = [
            [
                sg.Column(operation_list_column, size=(320, 500)),
                sg.VSeperator(),
                sg.Column(read_viewer_column, key="COL_READ", visible=False),
                sg.Column(gen_viewer_column, key="COL_GEN", visible=False),
                sg.Column(merge_viewer_column, key="COL_MERGE", visible=False),
                sg.Column(ext_viewer_column, key="COL_EXT", visible=False),
                sg.Column(del_viewer_column, key="COL_DEL", visible=False)
            ]
        ]
        self.window = sg.Window("CryptoWiz Tool", layout, size=(970, 500))

    def clean_all(self):
        list_col = ['COL_READ', 'COL_GEN', 'COL_MERGE', 'COL_EXT', 'COL_DEL']
        for col in list_col:
            self.window[col].update(visible=False)

    def run_gui(self):
        work_pixil = WorkPixil()
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "LIST_OP":
                operation = values['LIST_OP'].split(" - ")[0]
                if operation == 'read':
                    self.clean_all()
                    self.window['COL_READ'].update(visible=True)
                    self.window['LBL_HELP'].update("COMANDO READ\n\n\n"
                                                   "---- DESCRIZIONE ----\n"
                                                   "INDICA TUTTI I LAYER CONTENUTI IN UN FILE PIXIL\n\n\n"
                                                   "RICHIEDE 1 PARAMETRO:\n\n"
                                                   "1 - FILE SORGENTE - FILE PIXIL DA CUI LEGGERE TUTTI\n"
                                                   "I LAYER. IL FILE VIENE CERCATO NELLA CARTELLA SOURCE")
                if operation == 'gen':
                    self.clean_all()
                    self.window['COL_GEN'].update(visible=True)
                    self.window['LBL_HELP'].update("COMANDO GEN\n\n\n"
                                                   "---- DESCRIZIONE ----\n"
                                                   "GENERA UN'IMMAGINE UTILIZZANDO UN FILE PIXIL COME\nBASE DA CUI LEGGERE TUTTI I LAYER "
                                                   "E UN FILE JSON\nCOME TEMPLATE PER FILTRARE TUTTI I LAYER PRESENTI\nNEL FILE SORGENTE. "
                                                   "QUESTI FILE PERMETTONO DI DEDICERE\nQUALI COMBINAZIONI SI POSSONO VERIFICARE\n"
                                                   "DURANTE LA GENERAZIONE DELL'IMMAGINE.\n"
                                                   "IL FILE FINALE VIENE INSERITO NELLA CARTELLA GEN\n\n\n"
                                                   "RICHIEDE 2 PARAMETRI:\n\n"
                                                   "1 - FILE SORGENTE - FILE PIXIL DA CUI LEGGERE TUTTI\n"
                                                   "I LAYER. IL FILE VIENE CERCATO NELLA CARTELLA SOURCE\n\n"
                                                   "2 - TEMPLATE JSON - FILE JSON DA UTILIZZARE PER\n"
                                                   "FILTRARE I LAYER CONTENUTI NEL FILE SORGENTE\n"
                                                   "IL FILE VIENE CERCATO NELLA CARTELLA TEMPLATE")
                if operation == 'merge':
                    self.clean_all()
                    self.window['COL_MERGE'].update(visible=True)
                    self.window['LBL_HELP'].update("COMANDO MERGE\n\n\n"
                                                   "---- DESCRIZIONE ----\n"
                                                   "UNISCE I LAYER DI DUE FILE PIXIL IN UN\n"
                                                   "UNICO FILE PIXIL, AGGIUNGE AD UN FILE BASE\n"
                                                   "I LAYER CONTENUTI NEL FILE DA UNIRE.\n"
                                                   "HA BISOGNO DI SAPERE IN QUALE POSIZIONE\n"
                                                   "INSIRIRE I FILE. ESEMPIO:\n"
                                                   "SE VIENE INDICATO 5, I LAYER AGGIUNTIVI\n"
                                                   "VERRANNO MESSI DOPO I PRIMI 5 LAYER\n"
                                                   "DEL FILE DI BASE, QUINDI IN POSIZIONE 6.\n"
                                                   "IL FILE FINALE VIENE INSERITO NELL CARTELLA MERGE\n\n\n"
                                                   "RICHIEDE 3 PARAMETRI:\n\n"
                                                   "1 - FILE BASE - FILE PIXIL BASE AL QUALE AGGIUNGERE\n"
                                                   "I LAYER. IL FILE VIENE CERCATO NELLA CARTELLA SOURCE\n\n"
                                                   "2 - FILE AGGIUNTIVO - FILE PIXIL CHE CONTINE I LAYER\n"
                                                   "DA AGGIUNGERE AL FILE BASE. IL FILE VIENE CERCATO\n"
                                                   "NELLA CARTELLA SOURCE\n\n"
                                                   "3 - POSZIONE DI INSERIMENTO - NUMERO CHE INDICA\n"
                                                   "DA QUALE POSIZIONE INZIARE AD INSIRIRE I LAYER\n"
                                                   "NEL FILE BASE")
                if operation == 'ext':
                    self.clean_all()
                    self.window['COL_EXT'].update(visible=True)
                    self.window['LBL_HELP'].update("COMANDO EXT\n\n\n"
                                                   "---- DESCRIZIONE ----\n"
                                                   "ESTRAE DEI LAYER DA UN FILE PIXIL, NEL FILTRO\n"
                                                   "PER L'ESTRAZIONE SI POSSONO UTILIZZARE\n"
                                                   "ESPRESSIONI REGOLARI, ALCUNI ESEMPI:\n\n"
                                                   ".*BTC ESTRAE TUTTE LE RISORSE CHE TERMIANO CON BTC\n"
                                                   "VE.* ESTARE TUTTE LE RISORSE CHE INIZIANO CON VE\n"
                                                   "VE.*BTC ESTARE TUTTE LE RISORSE CHE INIZIANO\n"
                                                   "CON VE E TERMINANO CON BTC\n"
                                                   "IL FILE FINALE VIENE INSERITO NELL CARTELLA EXTRACT\n\n\n"
                                                   "RICHIEDE 2  PARAMETRI:\n\n"
                                                   "1 - FILE SORGENTE - FILE PIXIL DA CUI ESTRARRE I LAYER\n"
                                                   "IL FILE VIENE CERCATO NELLA CARTELLA SOURCE\n\n"
                                                   "2 - FILTRO PER ESTRAZIONE - LISTA DI ESPRESSIONI\n"
                                                   "SEPARTE DA VIRGOLA UTILIZZATE PER FILTRARE\n"
                                                   "I LAYER DEL FILE SORGENTE\n"
                                                   "ESEMPIO: VE.*,CPC.*,OCH.*")
                if operation == 'del':
                    self.clean_all()
                    self.window['COL_DEL'].update(visible=True)
                    self.window['LBL_HELP'].update("COMANDO DEL\n\n\n"
                                                   "---- DESCRIZIONE ----\n"
                                                   "CANCELLA DEI LAYER DA UN FILE PIXIL, NEL FILTRO\n"
                                                   "PER L'ESTRAZIONE SI POSSONO UTILIZZARE\n"
                                                   "ESPRESSIONI REGOLARI, ALCUNI ESEMPI:\n\n"
                                                   ".*BTC ELIMINA TUTTE LE RISORSE CHE TERMIANO CON BTC\n"
                                                   "VE.* ELIMINA TUTTE LE RISORSE CHE INIZIANO CON VE\n"
                                                   "VE.*BTC ELIMINA TUTTE LE RISORSE CHE INIZIANO\n"
                                                   "CON VE E TERMINANO CON BTC\n"
                                                   "IL FILE FINALE VIENE INSERITO NELL CARTELLA DELETE\n\n\n"
                                                   "RICHIEDE 2  PARAMETRI:\n\n"
                                                   "1 - FILE SORGENTE - FILE PIXIL DA CUI ELIMINA I LAYER\n"
                                                   "IL FILE VIENE CERCATO NELLA CARTELLA SOURCE\n\n"
                                                   "2 - FILTRO PER ESTRAZIONE - LISTA DI ESPRESSIONI\n"
                                                   "SEPARTE DA VIRGOLA UTILIZZATE PER TROVARE\n"
                                                   "I LAYER DA ELIMINARE DAL FILE SORGENTE\n"
                                                   "ESEMPIO: VE.*,CPC.*,OCH.*")
            if event == "BUTTON_READ":
                self.window["FILE_CTX"].update(work_pixil.print_all_layers(values["FILE_SOURCE"]), visible=True)
            if event == "BUTTON_GEN":
                file_name, layer_ctx = work_pixil.gen_img(values["FILE_GEN_SOURCE"], values["FILE_GEN_TEMPLATE"])
                self.window["IMAGE_GEN"].update(filename=file_name)
                self.window["FILE_CTX_GEN"].update(layer_ctx, visible=True)
            if event == "BUTTON_MERGE":
                self.window['FILE_CTX_MERGE'].update(work_pixil.merge_pixil(values["FILE_MERGE_SOURCE"], values["FILE_MERGE_ADD"], int(values['POS_MERGE'])), visible=True)
            if event == "BUTTON_EXT":
                self.window['FILE_CTX_EXT'].update(work_pixil.extract_pixil(values["FILE_EXT_SOURCE"], values["EXP_EXT"]), visible=True)
            if event == "BUTTON_DEL":
                layer_del, layer_remain = work_pixil.delete_layer(values["FILE_DEL_SOURCE"], values["EXP_DEL"])
                self.window['FILE_CTX_REMAIN'].update(layer_remain, visible=True)
                self.window['FILE_CTX_DEL'].update(layer_del, visible=True)
        self.window.close()


if __name__ == "__main__":
    gui_manager = GuiManager()
    gui_manager.run_gui()
