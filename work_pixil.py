from json import loads, dump
from re import match
from base64 import b64decode
from PIL import Image
from io import BytesIO
from random import choice
from argparse import ArgumentParser, RawTextHelpFormatter
from sys import exit
from os import makedirs


class WorkPixil:

    def __init__(self):
        print("SONO WORK PIXIL")

    @staticmethod
    def check_param_cli(op, source, layers, merge, pos, extract, delete):
        error = False
        if op is None or op not in ['read', 'gen', 'merge', 'ext', 'del']:
            error = True
        if op == 'read' and source is None:
            error = True
        if op == 'gen' and (source is None or layers is None):
            error = True
        if op == 'merge' and (source is None or merge is None or pos is None):
            error = True
        if op == 'ext' and (source is None or extract is None):
            error = True
        if op == 'del' and (source is None or delete is None):
            error = True
        return error

    def read_file(self, filename, json=True):
        f = open(filename)
        ctx = f.read()
        f.close()
        if json:
            ctx = loads(ctx)
        return ctx

    def write_file(self, filename, ctx, json=False):
        f = open(filename, "w")
        if json:
            dump(ctx, f)
        else:
            f.write(ctx)
        f.close()
        return

    def print_all_layers(self, source, destination=None):
        to_ret = []
        to_write = ""
        index = 1
        for c in self.read_file(source)['frames'][0]['layers']:
            to_ret.append(f'{str(index)} - {c["name"]}')
            to_write += f'{str(index)} - {c["name"]}\n'
            index += 1
        if destination is not None:
            self.write_file(destination, to_write)
        return to_ret

    def merge_pixil(self, source, merge, index, path_out="merge/merge_definitivo"):
        makedirs("merge", exist_ok=True)
        ctx_src = self.read_file(source)
        ctx_merge = self.read_file(merge)
        for c in ctx_merge['frames'][0]['layers']:
            ctx_src['frames'][0]['layers'].insert(index, c)
            index += 1
        self.write_file(f"{path_out}.pixil", ctx_src, json=True)
        return self.print_all_layers(f"{path_out}.pixil", f"{path_out}.txt")

    def extract_pixil(self, source, extract, path_out="extract/extract"):
        makedirs("extract", exist_ok=True)
        layer_list = []
        layer_extract = []
        to_ret = []
        to_write = ""
        for s in extract.split(","):
            layer_extract.append(s)
        ctx_src = self.read_file(source)
        for layer in layer_extract:
            index = 1
            for c in ctx_src['frames'][0]['layers']:
                if match(layer, c['name']):
                    layer_list.append(c)
                    to_ret.append(f'{str(index)} - {c["name"]}')
                    to_write += f'{str(index)} - {c["name"]}\n'
                index += 1
        ctx_src['frames'][0]['layers'] = layer_list
        self.write_file(f"{path_out}.pixil", ctx_src, json=True)
        self.write_file(f"{path_out}.txt", to_write)
        return to_ret

    def delete_layer(self, source, delete, path_out="delete/remain"):
        makedirs("delete", exist_ok=True)
        layer_list = []
        layer_delete = []
        to_write = ""
        to_ret = []
        to_write_remain = ""
        to_ret_remain = []
        for s in delete.split(","):
            layer_delete.append(s)
        ctx_src = self.read_file(source)
        for layer in layer_delete:
            for c in ctx_src['frames'][0]['layers']:
                if not match(layer, c['name']):
                    layer_list.append(c)
                    to_write_remain += f"{c['name']}\n"
                    to_ret_remain.append(c['name'])
                else:
                    to_write += f"{c['name']}\n"
                    to_ret.append(c['name'])
        ctx_src['frames'][0]['layers'] = layer_list
        self.write_file(f"{path_out}.pixil", ctx_src, json=True)
        self.write_file("delete/delete.txt", to_write)
        self.write_file(f"{path_out}.txt", to_write_remain)
        return to_ret, to_ret_remain

    def gen_img(self, source, layers, path_out="gen/final"):
        # ctx_json['frames'][0]['layers'].reverse()
        makedirs("gen", exist_ok=True)
        final_layers = []
        to_write = ""
        to_ret = []
        ctx_source = self.read_file(source)
        ctx_layers = self.read_file(layers)
        for key, val in ctx_layers.items():
            extra = None
            if 'possibility' not in val.keys():
                key_r = choice(list(val.keys()))
                value = choice(val[key_r]['possibility'])
                dependency = val[key_r]['dependency']
                key += key_r
                if 'extra' in val[key_r].keys():
                    extra = choice(val[key_r]['extra'][value])
            else:
                value = choice(val['possibility'])
                dependency = val['dependency']
            index = 1
            for c in ctx_source['frames'][0]['layers']:
                if (c['name'].find(key) == 0 and c['name'].find(value) > 0) or (dependency is not None and c['name'] in dependency) or (extra is not None and c['name'].find(extra) == 0):
                    to_write += f"{index} - {c['name']}\n"
                    to_ret.append(f"{index} - {c['name']}")
                    final_layers.append(Image.open(BytesIO(b64decode(c['src'].split(",")[1]))))
                index += 1
        for lay in final_layers[1:]:
            final_layers[0].paste(lay, (0, 0), lay)
        final_layers[0].save(path_out + ".png")
        self.write_file(path_out + ".txt", to_write)
        return path_out + ".png", to_ret


if __name__ == "__main__":
    p = ArgumentParser(formatter_class=RawTextHelpFormatter)
    p.add_argument("-op", "--operation", help="Scegli operazione:\n"
                                              "read: scrive tutti i nomi dei layer in un file - Richiede un parametro\n"
                                              "\t-s (--source)\n"
                                              "gen: genera un'immagine in formato PNG - Richiede due parametri:\n"
                                              "\t-s (--source)\n\t-l (--layers)\n"
                                              "merge: unisce due file PIXIL - Richiede tre parametri:\n"
                                              "\t-s (--source)\n\t-m (--merge)\n\t-p (--position)\n"
                                              "ext: estrae i layer dal file PIXIL - Richiede due parametri:\n"
                                              "\t-s (--source)\n\t-e (--extract)\n"
                                              "del: elimina i layer dal file PIXIL - Richiede due parametri:\n"
                                              "\t-s (--source)\n\t-d (--delete)\n"
                                              "I file devono essere nella cartelle specifiche\n", type=str)
    p.add_argument("-s", "--source", help="Nome del file PIXIL da cui leggere i source\nEsempio: -s finale.pixil", type=str)
    p.add_argument("-l", "--layers", help="Nome del file da cui leggere i layers\nEsempio: -l mage_btc.json", type=str)
    p.add_argument("-m", "--merge", help="Nome del file PIXIL da cui leggere i layers da mergiare nel file source\nEsempio: -m bombette_ada.pixil", type=str)
    p.add_argument("-p", "--position", help="Indice al quale inserire i layer del merge, se si scrive 5 il primo layer sarà in posizione 6\n"
                                            "Il numero specifica quanti layer mettere \"dietro\"\nEsempio: -p 134", type=int)
    p.add_argument("-e", "--extract", help="Lista dei layer da estratte,\n"
                                           "VE.*BTC estrae tutti i vestiti di BTC\n"
                                           ".*BTC estrae tutte le risorse che terminano con BTC"
                                           "AC.* estrae tutti gli accessori\nEsempio: -e VE...BTC,.*_ADA", type=str)
    p.add_argument("-d", "--delete", help="Lista dei layer da rimuovere,\n"
                                           "VE.*BTC rimuove tutti i vestiti di BTC\n"
                                           ".*BTC rimuove tutte le risorse che terminano con BTC"
                                           "AC.* rimuove tutti gli accessori\nEsempio: -d VE...BTC,.*_ADA", type=str)
    opt = p.parse_args()
    if WorkPixil.check_param_cli(opt.operation, opt.source, opt.layers, opt.merge, opt.position, opt.extract, opt.delete):
        p.print_help()
        exit()
    cls = WorkPixil()
    if opt.operation == 'gen':
        cls.gen_img(opt.source, opt.layers)
    if opt.operation == 'read':
        cls.print_all_layers(opt.source, "out.txt")
    if opt.operation == 'merge':
        cls.merge_pixil(opt.source, opt.merge, opt.position)
    if opt.operation == 'ext':
        cls.extract_pixil(opt.source, opt.extract)
    if opt.operation == 'del':
        cls.delete_layer(opt.source, opt.delete)
