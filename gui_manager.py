from pathlib import Path
import PySimpleGUI as simpleGui
import work_pixil
from os import replace


class GuiManager:

    def __init__(self):
        self.config = {
            "font": ("Arial", 13),
            "strings": work_pixil.read_file("string.json")
        }
        self.list_col = ['COL_READ', 'COL_GEN', 'COL_MERGE', 'COL_EXT', 'COL_DEL']
        self.cmd_list = ['read', 'gen', 'merge', 'ext', 'del']
        operation_list_column = [
            [simpleGui.Text("SCEGLI L'OPERAZIONE", font=self.config['font'])],
            [
                simpleGui.Combo(self.cmd_list, size=(45, 1), enable_events=True, key='LIST_OP', font=self.config['font'])
            ],
            [simpleGui.Text("", size=(5, 2))],
            [simpleGui.HorizontalSeparator()],
            [simpleGui.Text("", key="LBL_HELP", font=self.config['font'])],
        ]
        spalla_destra = {
            "COL_READ": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", size=(25, 1), font=self.config['font']),
                    simpleGui.In(size=(55, 1), enable_events=False, key="FILE_SOURCE", font=self.config['font']),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", font=self.config['font'], button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("", size=(77, 1)),
                    simpleGui.Text("REPORT SU FILE DI TESTO", size=(23, 1), font=self.config['font']),
                    simpleGui.Checkbox('', key="PRINT_FILE_READ", default=False)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER LEGGERE I LAYER CONTENUTI NEL FILE", size=(80, 1), font=self.config['font']),
                    simpleGui.Button("LEGGI FILE", key="BUTTON_READ", font=self.config['font'])
                ],
                [
                    simpleGui.Text("LISTA DEI LAYER (IN ORDINE) CONTENUTI NEL FILE SELEZIONATO", size=(80, 1), font=self.config['font']),
                ],
                [
                    simpleGui.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX", visible=False, font=self.config['font'])
                ]
            ],
            "COL_GEN": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", size=(25, 1), font=self.config['font']),
                    simpleGui.In(size=(55, 1), enable_events=False, key="FILE_GEN_SOURCE", font=self.config['font']),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", font=self.config['font'], button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("FILE JSON TEMPLATE", size=(25, 1), font=self.config['font']),
                    simpleGui.In(size=(55, 1), enable_events=False, key="FILE_GEN_TEMPLATE", font=self.config['font']),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/template", font=self.config['font'], button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("", size=(65, 1)),
                    simpleGui.Text("NUMERO DI IMMAGINI DA GENERARE", size=(30, 1), font=self.config['font']),
                    simpleGui.In(size=(5, 1), enable_events=False, default_text="1", key="NUM_FILE_GEN", font=self.config['font'])
                ],
                [
                    simpleGui.Text("", size=(77, 1)),
                    simpleGui.Text("REPORT SU FILE DI TESTO", size=(23, 1), font=self.config['font']),
                    simpleGui.Checkbox('', key="PRINT_FILE_GEN", default=False)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER GENERARE UN'IMMAGINE", size=(75, 1), font=self.config['font']),
                    simpleGui.Button("GENERA IMMAGINE", key="BUTTON_GEN", font=self.config['font'])
                ],
                [
                    simpleGui.Text("IMMAGINE GENERATA", size=(20, 1), font=self.config['font']),
                    simpleGui.Text("LISTA DEI LAYER (IN ORDINE) CONTENUTI NELL'IMMAGINE GENERATA", size=(60, 1), font=self.config['font']),
                ],
                [
                    simpleGui.Image(key="IMAGE_GEN"),
                    simpleGui.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_GEN", visible=False, font=self.config['font'])
                ]
            ],
            "COL_MERGE": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", size=(25, 1), font=self.config['font']),
                    simpleGui.In(size=(55, 1), enable_events=False, key="FILE_MERGE_SOURCE", font=self.config['font']),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE", font=self.config['font']),
                ],
                [
                    simpleGui.Text("FILE PIXIL DA MERGIARE", size=(25, 1), font=self.config['font']),
                    simpleGui.In(size=(55, 1), enable_events=False, key="FILE_MERGE_ADD", font=self.config['font']),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE", font=self.config['font']),
                ],
                [
                    simpleGui.Text("SCEGLI LA POSIZIONE A CUI INSERIRE I NUOVI LAYER", size=(80, 1), font=self.config['font']),
                    simpleGui.In(size=(10, 1), enable_events=False, key="POS_MERGE", font=self.config['font'])
                ],
                [
                    simpleGui.Text("", size=(77, 1)),
                    simpleGui.Text("REPORT SU FILE DI TESTO", size=(23, 1), font=self.config['font']),
                    simpleGui.Checkbox('', key="PRINT_FILE_MERGE", default=False)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER UNIRE I DUE FILE", size=(80, 1), font=self.config['font']),
                    simpleGui.Button("MERGIA FILE", key="BUTTON_MERGE", font=self.config['font'])
                ],
                [
                    simpleGui.Text(self.config['strings']['confirm_merge'], size=(60, 5), font=self.config['font']),
                    simpleGui.In(size=(20, 1), enable_events=False, key="NAME_MERGE", default_text="finale.pixil", font=self.config['font']),
                    simpleGui.Button("CONFERMA\nMERGE", key="BUTTON_MERGE_CONFIRM", font=self.config['font'])
                ],
                [
                    simpleGui.Text("LISTA DEI LAYER (IN ORDINE) CONTENUTI NEL FILE PIXIL GENERATO DAL MERGE", size=(80, 1), font=self.config['font']),
                ],
                [simpleGui.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_MERGE", visible=False, font=self.config['font'])]
            ],
            "COL_EXT": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", size=(25, 1), font=self.config['font']),
                    simpleGui.In(size=(55, 1), enable_events=False, key="FILE_EXT_SOURCE", font=self.config['font']),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE", font=self.config['font']),
                ],
                [
                    simpleGui.Text("SCEGLI I LAYER DA ESTARRE (SEPARATI DA VIRGOLA)", size=(65, 1), font=self.config['font']),
                    simpleGui.In(size=(15, 1), enable_events=False, key="EXP_EXT", font=self.config['font'])
                ],
                [
                    simpleGui.Text("", size=(77, 1)),
                    simpleGui.Text("REPORT SU FILE DI TESTO", size=(23, 1), font=self.config['font']),
                    simpleGui.Checkbox('', key="PRINT_FILE_EXT", default=False)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER CREARE UN FILE CON SOLO I LAYER SCELTI", size=(60, 1), font=self.config['font']),
                    simpleGui.In(size=(15, 1), enable_events=False, key="NAME_EXT", default_text="export.pixil", font=self.config['font']),
                    simpleGui.Button("ESTRAI LAYER", key="BUTTON_EXT", font=self.config['font'])
                ],
                [
                    simpleGui.Text("LISTA DEI LAYER (IN ORDINE) CONTENUTI NEL FILE PIXIL GENERATO DALL'ESTRAZIONE", size=(80, 1), font=self.config['font']),
                ],
                [simpleGui.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_EXT", visible=False, font=self.config['font'])]
            ],
            "COL_DEL": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", size=(25, 1), font=self.config['font']),
                    simpleGui.In(size=(55, 1), enable_events=False, key="FILE_DEL_SOURCE", font=self.config['font']),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE", font=self.config['font']),
                ],
                [
                    simpleGui.Text("SCEGLI I LAYER DA ELIMINARE (SEPARATI DA VIRGOLA)", size=(65, 1), font=self.config['font']),
                    simpleGui.In(size=(15, 1), enable_events=False, key="EXP_DEL", font=self.config['font'])
                ],
                [
                    simpleGui.Text("", size=(77, 1)),
                    simpleGui.Text("REPORT SU FILE DI TESTO", size=(23, 1), font=self.config['font']),
                    simpleGui.Checkbox('', key="PRINT_FILE_DEL", default=False)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER RIMUOVERE DAL FILE SORGENTE I LAYER SCELTI", size=(60, 1), font=self.config['font']),
                    simpleGui.In(size=(15, 1), enable_events=False, key="NAME_DEL", default_text="export.pixil", font=self.config['font']),
                    simpleGui.Button("ELIMINA LAYER", key="BUTTON_DEL", font=self.config['font'])
                ],
                [
                    simpleGui.Text("LISTA DEI LAYER (IN ORDINE) RIMASTI NEL FILE PIXIL", size=(50, 1), font=self.config['font']),
                    simpleGui.Text("LISTA DEI LAYER (IN ORDINE) RIMOSSI DAL FILE PIXIL", size=(50, 1), font=self.config['font']),
                ],
                [
                    simpleGui.Column([[simpleGui.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_REMAIN", visible=False, font=self.config['font'])]]),
                    simpleGui.Listbox(values=[], enable_events=False, size=(50, 20), key="FILE_CTX_DEL", visible=False, font=self.config['font'])
                ]
            ]
        }
        layout = [[simpleGui.Column(operation_list_column, size=(410, 600)), simpleGui.VSeperator()]]
        for key, val in spalla_destra.items():
            layout[0].append(simpleGui.Column(val, key=key, visible=False))
        self.window = simpleGui.Window("CryptoWiz Tool", layout, size=(1230, 600))

    def clean_all(self):
        for col in self.list_col:
            self.window[col].update(visible=False)

    def command_list_op(self, values):
        operation = values.split(" - ")[0]
        if operation in self.cmd_list:
            self.clean_all()
            self.window[f'COL_{str.upper(operation)}'].update(visible=True)
            self.window['LBL_HELP'].update(self.config['strings'][f'{operation}_lbl_help'])

    def command_read(self, values, print_file):
        if print_file:
            print_file = str(Path(__file__).parent.resolve()) + "/workdir/out.txt"
        self.window["FILE_CTX"].update(work_pixil.print_all_layers(values, print_file), visible=True)

    def command_gen(self, source, template, print_file, num_file_gen):
        for i in range(int(num_file_gen)):
            file_name, layer_ctx = work_pixil.gen_img(source, template, print_file, path_out=f"gen/final_{i}.png")
            self.window["IMAGE_GEN"].update(filename=file_name)
            self.window["FILE_CTX_GEN"].update(layer_ctx, visible=True)

    def command_merge(self, source, to_add, position, print_file):
        self.window['FILE_CTX_MERGE'].update(work_pixil.merge_pixil(source, to_add, int(position), print_file), visible=True)

    def command_ext(self, source, express, filename, print_file):
        dest = str(Path(__file__).parent.resolve()) + "/workdir/" + filename
        self.window['FILE_CTX_EXT'].update(work_pixil.extract_pixil(source, express, print_file, dest), visible=True)

    def command_del(self, source, express, filename, print_file):
        dest = str(Path(__file__).parent.resolve()) + "/workdir/" + filename
        layer_del, layer_remain = work_pixil.delete_layer(source, express, print_file, dest)
        self.window['FILE_CTX_REMAIN'].update(layer_remain, visible=True)
        self.window['FILE_CTX_DEL'].update(layer_del, visible=True)

    @staticmethod
    def command_confirm_merge(filename):
        dest = str(Path(__file__).parent.resolve()) + "/source/" + filename
        source = str(Path(__file__).parent.resolve()) + "/workdir/merge_definitivo.pixil"
        replace(source, dest)

    def run_gui(self):
        while True:
            event, values = self.window.read()
            if event is not None:
                funzioni = {
                    'LIST_OP': self.command_list_op,
                    'BUTTON_READ': self.command_read,
                    'BUTTON_GEN': self.command_gen,
                    'BUTTON_MERGE': self.command_merge,
                    'BUTTON_EXT': self.command_ext,
                    'BUTTON_DEL': self.command_del,
                    'BUTTON_MERGE_CONFIRM': GuiManager.command_confirm_merge
                }
                parametri = {
                    'LIST_OP': [values['LIST_OP']],
                    'BUTTON_READ': [values["FILE_SOURCE"], values["PRINT_FILE_READ"]],
                    'BUTTON_GEN': [values["FILE_GEN_SOURCE"], values["FILE_GEN_TEMPLATE"], values["PRINT_FILE_GEN"], values['NUM_FILE_GEN']],
                    'BUTTON_MERGE': [values["FILE_MERGE_SOURCE"], values["FILE_MERGE_ADD"], values['POS_MERGE'], values["PRINT_FILE_MERGE"]],
                    'BUTTON_EXT': [values["FILE_EXT_SOURCE"], values["EXP_EXT"], values['NAME_EXT'], values["PRINT_FILE_EXT"]],
                    'BUTTON_DEL': [values["FILE_DEL_SOURCE"], values["EXP_DEL"], values['NAME_DEL'], values["PRINT_FILE_DEL"]],
                    'BUTTON_MERGE_CONFIRM': [values['NAME_MERGE']]
                }
                funzioni[event](*parametri[event])
            else:
                break
        self.window.close()


if __name__ == "__main__":
    gui_manager = GuiManager()
    gui_manager.run_gui()
