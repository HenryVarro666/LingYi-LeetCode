"""从 Obsidian 题解库抽出两位作者的 Python 代码块，生成 allcode.json。
在 Leetcode 库根目录运行：python3 Python刷题函数/变量命名统计/extract.py"""
import os, re, json
out = []
for author, d in (('灵茶山艾府', '灵茶山艾府题解/solutions'), ('yiduobo', 'yiduobo题解/solutions')):
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.md'):
            continue
        lines = open(os.path.join(d, fn), encoding='utf-8').read().splitlines()
        blocks, cur, inblk, prefix, lang = [], None, False, '', ''
        for l in lines:
            m = re.match(r'^((?:\s*>)*\s*)```\s*([A-Za-z0-9+#]*)\s*$', l)
            if not inblk and m:
                inblk = True; prefix = m.group(1); lang = m.group(2).lower(); cur = []
                continue
            if inblk:
                s = l
                if prefix.strip():   # 去掉 callout 的 "> " 前缀
                    s = re.sub(r'^(\s*>\s?){1,%d}' % prefix.count('>'), '', s)
                if re.match(r'^\s*```\s*$', s):
                    if lang in ('python', 'python3', 'py'):
                        blocks.append('\n'.join(cur))
                    inblk = False
                    continue
                cur.append(s)
        out.append(dict(author=author, file=fn, num=fn[:4], title=fn[5:].split(' · ')[0], code=blocks))
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, 'allcode.json'), 'w'), ensure_ascii=False)
print(len(out), 'files')
