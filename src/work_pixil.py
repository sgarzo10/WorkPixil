from json import loads, dump, dumps
from re import match
from base64 import b64decode
from PIL import Image
from io import BytesIO
from random import choice
from argparse import ArgumentParser, RawTextHelpFormatter
from sys import exit
from os import makedirs
from os import remove
from treelib import Node, Tree
from WorkPixil.src.dbmanager import DbManager


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


def read_file(filename, json=True):
    f = open(filename)
    ctx = f.read()
    f.close()
    if json:
        ctx = loads(ctx)
    return ctx


def write_file(filename, ctx, json=False):
    f = open(filename, "w")
    if json:
        dump(ctx, f)
    else:
        f.write(ctx)
    f.close()
    return


def check_start_word(init_word, keys):
    to_ret = ""
    for k in keys:
        if init_word not in keys and match(k, init_word):
            to_ret = k
    return to_ret


def get_init_word(source):
    words = {}
    filename = "tree.txt"
    tree = Tree()
    tree.create_node("INIT", "init")
    for c in read_file(source)["frames"][0]['layers']:
        init_word = c["name"].split("_")[0]
        second_word = ''.join(i for i in c["name"].split("_")[1:])
        if init_word not in words.keys():
            words[init_word] = {}
            tree.create_node(str("{:5d}".format(len(words.keys()))) + init_word, init_word, parent="init")
        '''
        if second_word not in words[init_word].keys():
            words[init_word][second_word] = {}
            tree.create_node(str("{:5d}".format(len(words[init_word].keys()))) + second_word, init_word+second_word, parent=init_word)
        '''
    tree.save2file(filename)
    ctx = read_file(filename, False)
    remove(filename)
    print(ctx)
    return ''.join([i for i in ctx if not i.isdigit() and i != ' '])


def print_all_layers(source, print_file=False):
    makedirs("../workdir", exist_ok=True)
    to_ret = []
    to_write = ""
    index = 1
    for c in read_file(source)["frames"][0]['layers']:
        to_ret.append(f'{str(index)} - {c["name"]}')
        to_write += f'{str(index)} - {c["name"]}\n'
        index += 1
    if print_file:
        write_file(print_file, to_write)
    return to_ret


def gen_img(source, layers, print_file, path_out="../gen/final.png", path_db=''):
    # ctx_json['frames'][0]['layers'].reverse()
    makedirs('/'.join(path_out.split("/")[:-1]), exist_ok=True)
    final_layers = []
    to_write = ""
    to_ret = {"layers": []}
    query = "SELECT * FROM LAYER_STATS WHERE "
    total_stats = {
        "stamina": 0,
        "attack": 0,
        "defense": 0,
        "precision": 0,
        "speed": 0
    }
    try:
        ctx_source = read_file(source)
        ctx_layers = read_file(layers)
        for key, val in ctx_layers.items():
            extra = None
            if 'possibility' not in val.keys():
                key_r = choice(list(val.keys()))
                value = choice(val[key_r]['possibility'])
                dependency = val[key_r]['dependency']
                key += key_r
                query += f"(CATEGORY = '{key[:-1]}' AND SUB_CATEGORY = '{value}') OR "
                if 'extra' in val[key_r].keys():
                    extra = choice(val[key_r]['extra'][value])
                    query += f"(CATEGORY = '{extra.split('_')[0]}' AND SUB_CATEGORY = '{extra.split('_')[1]}') OR "
            else:
                value = choice(val['possibility'])
                dependency = val['dependency']
                query += f"(CATEGORY = '{key[:-1]}' AND SUB_CATEGORY = '{value}') OR "
            index = 1
            for c in ctx_source['frames'][0]['layers']:
                if (c['name'].find(key) == 0 and c['name'].find(value) > 0) or (dependency is not None and c['name'] in dependency) or (extra is not None and c['name'].find(extra) == 0):
                    to_write += f"{index} - {c['name']}\n"
                    to_ret["layers"].append(f"{index} - {c['name']}")
                    final_layers.append(Image.open(BytesIO(b64decode(c['src'].split(",")[1]))))
                index += 1
        query = query[:-4] + ";"
        DbManager(path_db + "workpixil.db")
        stats = DbManager.select(query)
        for stat in stats:
            for key, value in stat.items():
                if key in total_stats.keys():
                    total_stats[key] += value
        DbManager.close_db()
        for lay in final_layers[1:]:
            final_layers[0].paste(lay, (0, 0), lay)
        final_layers[0].save(f"{path_out}")
        # write_file(f"{path_out.split('.png')[0]}.json", dumps({"items": stats, "total": total_stats}, indent=4))
        to_ret["json"] = {"items": stats, "total": total_stats}
        if print_file:
            write_file(f"{path_out.split('.png')[0]}.txt", to_write)
    except Exception as e:
        to_ret = str(e)
    return to_ret


def merge_pixil(source, merge, index, print_file, path_out="../workdir/merge_definitivo.pixil"):
    makedirs("../workdir", exist_ok=True)
    ctx_src = read_file(source)
    ctx_merge = read_file(merge)
    for c in ctx_merge['frames'][0]['layers']:
        ctx_src['frames'][0]['layers'].insert(index, c)
        index += 1
    write_file(f"{path_out}", ctx_src, json=True)
    return print_all_layers(f"{path_out}", f"{path_out.split('.pixil')[0]}.txt") if print_file else print_all_layers(f"{path_out}")


def extract_pixil(source, extract, print_file, path_out="../workdir/extract.pixil"):
    makedirs("../workdir", exist_ok=True)
    layer_list = []
    layer_extract = []
    to_ret = []
    to_write = ""
    for s in extract.split(","):
        layer_extract.append(s)
    ctx_src = read_file(source)
    for layer in layer_extract:
        index = 1
        for c in ctx_src['frames'][0]['layers']:
            if match(layer, c['name']) and c not in layer_list:
                layer_list.append(c)
                to_ret.append(f'{str(index)} - {c["name"]}')
                to_write += f'{str(index)} - {c["name"]}\n'
            index += 1
    ctx_src['frames'][0]['layers'] = layer_list
    write_file(f"{path_out}", ctx_src, json=True)
    if print_file:
        write_file(f"{path_out.split('.pixil')[0]}.txt", to_write)
    return to_ret


def delete_layer(source, delete, print_file, path_out="../workdir/remain.pixil"):
    makedirs("../workdir", exist_ok=True)
    layer_list = []
    layer_delete_list = []
    layer_delete = []
    to_write = ""
    to_ret = []
    to_write_remain = ""
    to_ret_remain = []
    for s in delete.split(","):
        layer_delete.append(s)
    ctx_src = read_file(source)
    for c in ctx_src['frames'][0]['layers']:
        for layer in layer_delete:
            if match(layer, c['name']):
                layer_delete_list.append(c)
                to_write += f"{c['name']}\n"
                to_ret.append(c['name'])
    for c in ctx_src['frames'][0]['layers']:
        if c not in layer_delete_list:
            layer_list.append(c)
            to_write_remain += f"{c['name']}\n"
            to_ret_remain.append(c['name'])
    ctx_src['frames'][0]['layers'] = layer_list
    write_file(f"{path_out}", ctx_src, json=True)
    if print_file:
        write_file(f"{path_out.split('.pixil')[0]}_delete.txt", to_write)
        write_file(f"{path_out.split('.pixil')[0]}.txt", to_write_remain)
    return to_ret, to_ret_remain


if __name__ == "__main__":
    strings = read_file("string.json")
    p = ArgumentParser(formatter_class=RawTextHelpFormatter)
    p.add_argument("-op", "--operation", help=strings['operation_param_help'], type=str)
    p.add_argument("-s", "--source", help=strings['source_param_help'], type=str)
    p.add_argument("-l", "--layers", help=strings['layers_param_help'], type=str)
    p.add_argument("-m", "--merge", help=strings['merge_param_help'], type=str)
    p.add_argument("-p", "--position", help=strings['position_param_help'], type=int)
    p.add_argument("-e", "--extract", help=strings['extract_param_help'], type=str)
    p.add_argument("-d", "--delete", help=strings['del_param_help'], type=str)
    opt = p.parse_args()
    if check_param_cli(opt.operation, opt.source, opt.layers, opt.merge, opt.position, opt.extract, opt.delete):
        p.print_help()
        exit()
    funzioni = {
        'read': print_all_layers,
        'gen': gen_img,
        'merge': merge_pixil,
        'ext': extract_pixil,
        'del': delete_layer,
    }
    parametri = {
        'read': [opt.source, "out.txt"],
        'gen': [opt.source, opt.layers, True],
        'merge': [opt.source, opt.merge, opt.position, True],
        'ext': [opt.source, opt.extract, True],
        'del': [opt.source, opt.delete, True]
    }
    result = funzioni[opt.operation](*parametri[opt.operation])
