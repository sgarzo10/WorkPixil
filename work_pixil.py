from json import loads, dump
from re import match
from base64 import b64decode
from PIL import Image
from io import BytesIO
from random import choice
from argparse import ArgumentParser, RawTextHelpFormatter
from sys import exit
from os import makedirs


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


def print_all_layers(source, print_file=False):
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


def gen_img(source, layers, print_file, path_out="gen/final.png"):
    # ctx_json['frames'][0]['layers'].reverse()
    makedirs("gen", exist_ok=True)
    final_layers = []
    to_write = ""
    to_ret = []
    ctx_source = read_file(source)
    ctx_layers = read_file(layers)
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
    final_layers[0].save(f"{path_out}")
    if print_file:
        write_file(f"{path_out.split('.')[0]}.txt", to_write)
    return path_out, to_ret


def merge_pixil(source, merge, index, print_file, path_out="workdir/merge_definitivo.pixil"):
    makedirs("workdir", exist_ok=True)
    ctx_src = read_file(source)
    ctx_merge = read_file(merge)
    for c in ctx_merge['frames'][0]['layers']:
        ctx_src['frames'][0]['layers'].insert(index, c)
        index += 1
    write_file(f"{path_out}", ctx_src, json=True)
    return print_all_layers(f"{path_out}", f"{path_out.split('.')[0]}.txt") if print_file else print_all_layers(f"{path_out}")


def extract_pixil(source, extract, print_file, path_out="workdir/extract.pixil"):
    makedirs("workdir", exist_ok=True)
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
            if match(layer, c['name']):
                layer_list.append(c)
                to_ret.append(f'{str(index)} - {c["name"]}')
                to_write += f'{str(index)} - {c["name"]}\n'
            index += 1
    ctx_src['frames'][0]['layers'] = layer_list
    write_file(f"{path_out}", ctx_src, json=True)
    if print_file:
        write_file(f"{path_out.split('.')[0]}.txt", to_write)
    return to_ret


def delete_layer(source, delete, print_file, path_out="workdir/remain.pixil"):
    makedirs("workdir", exist_ok=True)
    layer_list = []
    layer_delete = []
    to_write = ""
    to_ret = []
    to_write_remain = ""
    to_ret_remain = []
    for s in delete.split(","):
        layer_delete.append(s)
    ctx_src = read_file(source)
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
    write_file(f"{path_out}", ctx_src, json=True)
    if print_file:
        write_file(f"{path_out.split('.')[0]}_delete.txt", to_write)
        write_file(f"{path_out.split('.')[0]}.txt", to_write_remain)
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
