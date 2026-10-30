"""Naming rules for the LC_Video repo (one folder per problem) + the master problem list.

all.json (written by pipeline/manifest.py) is a list of problems in study-path order:
  {id, key, title, diff, rating, ling, yiduobo, paths, todo, done, existing, slug, rank, ...}
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_ITEMS = None
AUTHORS = {'ling': '灵茶山艾府', 'yiduobo': 'yiduobo'}
CFG_DIRS = {'ling': ['ling_all', 'ling2', 'ling'], 'yiduobo': ['yiduobo_all', 'yiduobo2', 'yiduobo']}
NEW_DIRS = {'ling_all': 'ling', 'yiduobo_all': 'yiduobo'}
_BAD = str.maketrans({'/': '／', '\\': '＼', ':': '：', '?': '？', '*': '＊', '"': '＂', '<': '＜', '>': '＞', '|': '｜'})


def items():
    global _ITEMS
    if _ITEMS is None:
        _ITEMS = json.load(open(os.path.join(HERE, 'all.json'), encoding='utf-8'))
    return _ITEMS


def by_key():
    return {it['key']: it for it in items()}


def safe(s):
    return s.translate(_BAD).strip()


def disp(it):
    return f"{int(it['id']):04d}" if it['id'].isdigit() else it['id']


def bucket(it):
    if it['id'].isdigit():
        lo = int(it['id']) // 100 * 100
        return f'{lo:04d}-{lo + 99:04d}'
    return it['id'].split(' ')[0].split('-')[0]


def folder(it):
    """题解/<bucket>/<NNNN 题名>"""
    return f"题解/{bucket(it)}/{disp(it)} {safe(it['title'])}"


def video(it, author):
    """author: 'ling' | 'yiduobo'"""
    f = folder(it)
    return f"{f}/{os.path.basename(f)} · {AUTHORS[author]}.mp4"


def solution(it, author):
    return f"{folder(it)}/{AUTHORS[author]}.md"
