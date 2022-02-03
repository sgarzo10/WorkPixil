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
        self.size_listbox = (25, 25)
        self.size_text_filename = (12, 1)
        self.size_text_number = (7, 1)
        self.size_text_reg_exp = (20, 1)
        operation_list_column = [
            [
                simpleGui.Text("SCEGLI L'OPERAZIONE", key='LBL_OP', size=(50, 1))
            ],
            [
                simpleGui.Combo(self.cmd_list, enable_events=True, key='LIST_OP', readonly=True)
            ],
            [
                simpleGui.Text("")
            ],
            [
                simpleGui.HorizontalSeparator()
            ],
            [
                simpleGui.Multiline("", disabled=True, key="LBL_HELP", no_scrollbar=True, expand_x=True, expand_y=True, text_color="white", background_color="#64778d", border_width=0)
            ]
        ]
        spalla_destra = {
            "COL_READ": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE"),
                    simpleGui.In(key="FILE_SOURCE"),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("REPORT SU FILE DI TESTO", expand_x=True),
                    simpleGui.Checkbox('', key="PRINT_FILE_READ", default=False)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER LEGGERE I LAYER CONTENUTI NEL FILE", expand_x=True),
                    simpleGui.Button("LEGGI FILE", key="BUTTON_READ")
                ],
                [
                    simpleGui.HorizontalSeparator()
                ],
                [
                    simpleGui.Text("LAYER (IN ORDINE) CONTENUTI NEL FILE SELEZIONATO"),
                ],
                [
                    simpleGui.Listbox(values=[], select_mode=simpleGui.LISTBOX_SELECT_MODE_EXTENDED, key="FILE_CTX", visible=False, size=self.size_listbox)
                ]
            ],
            "COL_GEN": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", expand_x=True),
                    simpleGui.In(key="FILE_GEN_SOURCE"),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("FILE JSON TEMPLATE", expand_x=True),
                    simpleGui.In(key="FILE_GEN_TEMPLATE"),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/template", button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("NUMERO DI IMMAGINI DA GENERARE", expand_x=True),
                    simpleGui.In(default_text="1", key="NUM_FILE_GEN", size=self.size_text_number)
                ],
                [
                    simpleGui.Text("REPORT SU FILE DI TESTO", expand_x=True),
                    simpleGui.Checkbox('', key="PRINT_FILE_GEN", default=False)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER GENERARE UN'IMMAGINE", expand_x=True),
                    simpleGui.Button("GENERA IMMAGINE", key="BUTTON_GEN")
                ],
                [
                    simpleGui.HorizontalSeparator()
                ],
                [
                    simpleGui.Column([
                        [
                            simpleGui.Text("IMMAGINE GENERATA")
                        ],
                        [
                            simpleGui.Image(key="IMAGE_GEN", expand_y=True)
                        ]
                    ], expand_y=True, expand_x=True),
                    simpleGui.Column([
                        [
                            simpleGui.Text("LAYER (IN ORDINE) CONTENUTI NELL'IMMAGINE")
                        ],
                        [
                            simpleGui.Listbox(values=[], select_mode=simpleGui.LISTBOX_SELECT_MODE_EXTENDED, key="FILE_CTX_GEN", visible=False, size=self.size_listbox)
                        ]
                    ], expand_y=True, expand_x=True)
                ]
            ],
            "COL_MERGE": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", expand_x=True),
                    simpleGui.In(key="FILE_MERGE_SOURCE"),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("FILE PIXIL DA MERGIARE", expand_x=True),
                    simpleGui.In(key="FILE_MERGE_ADD"),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("SCEGLI LA POSIZIONE A CUI INSERIRE I NUOVI LAYER", expand_x=True),
                    simpleGui.In(key="POS_MERGE", size=self.size_text_number)
                ],
                [
                    simpleGui.Text("REPORT SU FILE DI TESTO", expand_x=True),
                    simpleGui.Checkbox('', key="PRINT_FILE_MERGE", default=False)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER UNIRE I DUE FILE", expand_x=True),
                    simpleGui.Button("MERGIA FILE", key="BUTTON_MERGE")
                ],
                [
                    simpleGui.HorizontalSeparator()
                ],
                [
                    simpleGui.Text("LAYER (IN ORDINE) CONTENUTI NEL FILE PIXIL GENERATO DAL MERGE"),
                ],
                [
                    simpleGui.Listbox(values=[], select_mode=simpleGui.LISTBOX_SELECT_MODE_EXTENDED, key="FILE_CTX_MERGE", visible=False, size=self.size_listbox)
                ],
                [
                    simpleGui.HorizontalSeparator()
                ],
                [
                    simpleGui.Text("NOME DEL FILE PIXIL CHE VIENE GENERATO ALLA CONFERMA DEL MERGE", expand_x=True),
                    simpleGui.In(key="NAME_MERGE", default_text="finale.pixil", size=self.size_text_filename)
                ],
                [
                    simpleGui.Multiline(self.config['strings']['confirm_merge'], key="LBL_CONFIRM_MERGE", disabled=True, no_scrollbar=True, expand_x=True, expand_y=True, text_color="white", background_color="#64778d", border_width=0),
                    simpleGui.Button("\nCONFERMA\nMERGE\n", key="BUTTON_MERGE_CONFIRM")
                ],
            ],
            "COL_EXT": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", expand_x=True),
                    simpleGui.In(key="FILE_EXT_SOURCE"),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("SCEGLI I LAYER DA ESTARRE (SEPARATI DA VIRGOLA)", expand_x=True),
                    simpleGui.In(key="EXP_EXT", size=self.size_text_reg_exp)
                ],
                [
                    simpleGui.Text("REPORT SU FILE DI TESTO", expand_x=True),
                    simpleGui.Checkbox('', key="PRINT_FILE_EXT", default=False)
                ],
                [
                    simpleGui.Text("NOME DEL FILE PIXIL CHE VIENE GENERATO", expand_x=True),
                    simpleGui.In(key="NAME_EXT", default_text="export.pixil", size=self.size_text_filename)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER CREARE UN FILE CON SOLO I LAYER SCELTI", expand_x=True),
                    simpleGui.Button("ESTRAI LAYER", key="BUTTON_EXT")
                ],
                [
                    simpleGui.HorizontalSeparator()
                ],
                [
                    simpleGui.Text("LAYER (IN ORDINE) CONTENUTI NEL FILE PIXIL GENERATO DALL'ESTRAZIONE"),
                ],
                [
                    simpleGui.Listbox(values=[], select_mode=simpleGui.LISTBOX_SELECT_MODE_EXTENDED, key="FILE_CTX_EXT", visible=False, size=self.size_listbox)
                ]
            ],
            "COL_DEL": [
                [
                    simpleGui.Text("FILE PIXIL SORGENTE", expand_x=True),
                    simpleGui.In(key="FILE_DEL_SOURCE"),
                    simpleGui.FileBrowse(initial_folder=str(Path(__file__).parent.resolve()) + "/source", button_text="BROWSE"),
                ],
                [
                    simpleGui.Text("SCEGLI I LAYER DA ELIMINARE (SEPARATI DA VIRGOLA)", expand_x=True),
                    simpleGui.In(key="EXP_DEL", size=self.size_text_reg_exp)
                ],
                [
                    simpleGui.Text("REPORT SU FILE DI TESTO", expand_x=True),
                    simpleGui.Checkbox('', key="PRINT_FILE_DEL", default=False)
                ],
                [
                    simpleGui.Text("NOME DEL FILE PIXIL CHE VIENE GENERATO", expand_x=True),
                    simpleGui.In(key="NAME_DEL", default_text="export.pixil", size=self.size_text_filename)
                ],
                [
                    simpleGui.Text("PREMI IL PULSANTE PER RIMUOVERE DAL FILE SORGENTE I LAYER SCELTI", expand_x=True),
                    simpleGui.Button("ELIMINA LAYER", key="BUTTON_DEL")
                ],
                [
                    simpleGui.HorizontalSeparator()
                ],
                [
                    simpleGui.Column([
                        [
                            simpleGui.Text("LAYER (IN ORDINE) RIMASTI NEL FILE PIXIL"),
                        ],
                        [
                            simpleGui.Listbox(values=[], select_mode=simpleGui.LISTBOX_SELECT_MODE_EXTENDED, key="FILE_CTX_REMAIN", visible=False, size=self.size_listbox)
                        ]
                    ]),
                    simpleGui.Column([
                        [
                            simpleGui.Text("LAYER RIMOSSI DAL FILE PIXIL"),
                        ],
                        [
                            simpleGui.Listbox(values=[], select_mode=simpleGui.LISTBOX_SELECT_MODE_EXTENDED, key="FILE_CTX_DEL", visible=False, size=self.size_listbox)
                        ]
                    ])
                ]
            ]
        }
        layout = [[simpleGui.Column(operation_list_column, expand_y=True), simpleGui.VSeperator()]]
        for key, val in spalla_destra.items():
            layout[0].append(simpleGui.Column(val, key=key, visible=False))
        self.window = simpleGui.Window("CryptoWiz Tool", layout, resizable=True, finalize=True, font=self.config['font'])
        self.screen_width = self.window.get_screen_size()[0]
        self.screen_heigth = self.window.get_screen_size()[1]
        self.window.set_min_size((int(self.screen_width*0.68), int(self.screen_heigth*0.70)))
        self.window.move(int(self.screen_width*0.20), int(self.screen_heigth*0.10))
        self.window['LBL_HELP'].set_cursor("arrow")
        self.window['LBL_CONFIRM_MERGE'].set_cursor("arrow")

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
        self.window['FILE_CTX_MERGE'].update(work_pixil.merge_pixil(source, to_add, int(position) - 1, print_file), visible=True)

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
