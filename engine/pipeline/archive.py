"""Download packages: all solutions + mp4 videos as zip files.

python pipeline/archive.py ROOT [--budget 140] [--part-gb 1.5]

Writes
  ROOT/下载/LingYi-LeetCode-题解文字版.zip         every .md (题解 / 刷题路径 / 学习笔记 / 索引 / README) + 我的代码, no images/videos;
                                                   small enough (< 100 MB) to live in the git repo
  ROOT/_work/release/LingYi-LeetCode-partNN-<range>.zip   for GitHub Releases (each < 2 GB): every problem folder of that
                                                   range (README + 两份题解 .md + .mp4); part00-common = 题解图片、分类概念视频、
                                                   刷题路径、学习笔记、我的代码、索引、README
Resumable: zips are filled in append mode until --budget seconds, re-run to continue; a part is finished when
its name is listed in _work/release/DONE.txt.
"""
import argparse
import glob
import json
import os
import time
import zipfile

ap = argparse.ArgumentParser()
ap.add_argument('root')
ap.add_argument('--budget', type=float, default=140)
ap.add_argument('--part-gb', type=float, default=1.5)
a = ap.parse_args()
R = a.root
T0 = time.time()
REL = os.path.join(R, '_work', 'release')
os.makedirs(REL, exist_ok=True)
os.makedirs(os.path.join(R, '下载'), exist_ok=True)
DONE = os.path.join(REL, 'DONE.txt')
done = set(open(DONE, encoding='utf-8').read().split('\n')) if os.path.exists(DONE) else set()
PREFIX = 'LingYi-LeetCode'


def files_under(rel, exts):
    out = []
    for dp, dn, fn in os.walk(os.path.join(R, rel)):
        dn[:] = sorted(d for d in dn if d not in ('__pycache__',))
        for f in sorted(fn):
            if f.endswith(exts) and '.part.' not in f:
                out.append(os.path.relpath(os.path.join(dp, f), R))
    return out


def fill(zip_path, names, arc_prefix=''):
    """add missing names to zip_path (append mode); returns True when complete"""
    have = set()
    if os.path.exists(zip_path):
        try:
            with zipfile.ZipFile(zip_path) as z:
                have = set(z.namelist())
        except zipfile.BadZipFile:
            os.replace(zip_path, zip_path + '.broken')
    todo = [n for n in names if arc_prefix + n not in have]
    if not todo:
        return True
    with zipfile.ZipFile(zip_path, 'a', allowZip64=True) as z:
        for n in todo:
            if time.time() - T0 > a.budget:
                return False
            comp = zipfile.ZIP_STORED if n.endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.zip')) else zipfile.ZIP_DEFLATED
            z.write(os.path.join(R, n), arc_prefix + n, compress_type=comp)
    return True


def mark(name):
    done.add(name)
    open(DONE, 'w', encoding='utf-8').write('\n'.join(sorted(x for x in done if x)))


# 1) text-only package that goes into the repo
text_zip = os.path.join(R, '下载', f'{PREFIX}-题解文字版.zip')
if 'text' not in done:
    names = [f for f in files_under('题解', ('.md',))]
    for d in ('刷题路径', '学习笔记'):
        names += files_under(d, ('.md', '.csv', '.ipynb'))
    names += files_under('我的代码', ('.py', '.md')) + ['README.md', '索引.md']
    if fill(text_zip + '.part', names, PREFIX + '/'):
        os.replace(text_zip + '.part', text_zip)
        mark('text')

# 2) release parts
buckets = sorted(d for d in os.listdir(os.path.join(R, '题解')) if os.path.isdir(os.path.join(R, '题解', d)) and d != '_assets')
buckets = [b for b in buckets if b[:4].isdigit()] + [b for b in buckets if not b[:4].isdigit()]


def bucket_files(b):
    return files_under(os.path.join('题解', b), ('.md', '.mp4'))


parts = [('part00-common', files_under('题解/_assets', ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))
          + files_under('分类概念视频', ('.mp4', '.md')) + files_under('刷题路径', ('.md', '.csv'))
          + files_under('学习笔记', ('.md', '.csv', '.ipynb', '.py', '.json')) + files_under('我的代码', ('.py', '.md'))
          + ['README.md', '索引.md'])]
# release asset names must stay ASCII (GitHub rewrites other characters)
def label(bs):
    nums = [b for b in bs if b[:4].isdigit()]
    s = f'{nums[0][:4]}-{nums[-1][-4:]}' if nums else ''
    if len(nums) < len(bs):
        s += ('-' if s else '') + 'LCP-LCR-LCS-misc'
    return s


cur, cur_b, cur_size = [], [], 0
limit = a.part_gb * 2**30
for b in buckets:
    fs = bucket_files(b)
    size = sum(os.path.getsize(os.path.join(R, f)) for f in fs)
    if cur and cur_size + size > limit:
        parts.append((f'part{len(parts):02d}-{label(cur_b)}', cur))
        cur, cur_b, cur_size = [], [], 0
    cur += fs
    cur_b.append(b)
    cur_size += size
if cur:
    parts.append((f'part{len(parts):02d}-{label(cur_b)}', cur))

manifest = []
for name, names in parts:
    path = os.path.join(REL, f'{PREFIX}-{name}.zip')
    manifest.append({'file': os.path.basename(path), 'files': len(names),
                     'size': sum(os.path.getsize(os.path.join(R, f)) for f in names)})
    if name in done:
        continue
    if time.time() - T0 > a.budget:
        break
    if fill(path + '.part', names, PREFIX + '/'):
        os.replace(path + '.part', path)
        mark(name)
json.dump(manifest, open(os.path.join(REL, 'parts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
notes = ['LingYi-LeetCode 全部题解（灵茶山艾府 + yiduobo 原文 Markdown）和动画讲解 mp4，按题号区间分卷，解压后目录结构与仓库一致。', '',
         '| 文件 | 内容 | 大小 |', '|---|---|---|']
for m in manifest:
    what = '公共部分：题解图片、分类概念视频、刷题路径、学习笔记、我的代码、索引' if 'common' in m['file'] else \
        '题号 ' + m['file'].split('-', 3)[-1][:-4].replace('-LCP-LCR-LCS-misc', ' + LCP/LCR/LCS/面试题等') + ' 的题解与视频'
    notes.append(f"| {m['file']} | {what}（{m['files']} 个文件） | {m['size'] / 2**30:.2f} GB |")
notes += ['', '只要文字版（所有题解 Markdown，不含图片和视频）：仓库里的 `下载/LingYi-LeetCode-题解文字版.zip`。']
open(os.path.join(REL, 'NOTES.md'), 'w', encoding='utf-8').write('\n'.join(notes) + '\n')
left = [n for n, _ in parts if n not in done] + ([] if 'text' in done else ['text'])
print(f'parts {len(parts)} (+ text); finished {len(done & ({n for n, _ in parts} | {"text"}))}; '
      f'left {left[:6]}{"…" if len(left) > 6 else ""}; {time.time() - T0:.0f}s')
