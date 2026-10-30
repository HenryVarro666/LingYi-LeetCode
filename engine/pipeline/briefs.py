"""Write compact per-problem briefs for config-writing agents.

python briefs.py DATA_ROOT manifest.json OUT_DIR
"""
import json, os, re, sys

ROOT, MAN, OUT = sys.argv[1:4]
ONLY = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else None  # optional: only these keys
CODE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(MAN)), 'ling_fetched_code.json'), encoding='utf-8')) \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(MAN)), 'ling_fetched_code.json')) else {}
os.makedirs(OUT, exist_ok=True)
items = json.load(open(MAN, encoding='utf-8'))


def body(text):
    text = re.sub(r'^---\n.*?\n---\n', '', text, count=1, flags=re.S)
    return text


def decallout(s):
    out = []
    for line in s.split('\n'):
        if line.startswith('> '):
            line = line[2:]
        elif line == '>':
            line = ''
        out.append(line)
    return '\n'.join(out)


def squeeze(s):
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


def ling_parts(path):
    t = body(open(path, encoding='utf-8').read())
    meta = ''
    m = re.search(r'> \[!info\][^\n]*', t)
    if m:
        meta = m.group(0)
    topics = ''
    m = re.search(r'> \[!abstract\] 所属题单\n((?:>.*\n)+)', t)
    if m:
        topics = re.sub(r'\[\[[^|\]]*\|([^\]]*)\]\]', r'\1', decallout(m.group(1))).strip()
    stmt = ''
    m = re.search(r'> \[!question\][^\n]*\n((?:>.*\n?)+)', t)
    if m:
        stmt = squeeze(decallout(m.group(1)))
    sol = ''
    m = re.search(r'> \[!success\][^\n]*\n((?:>.*\n?)+)', t)
    if m:
        sol = decallout(m.group(1))
        sol = re.split(r'\n## 分类题单', sol)[0]
        sol = re.sub(r'\[\[[^|\]]*\|([^\]]*)\]\]', r'\1', sol)
        sol = squeeze(sol)
    return meta, topics, stmt, sol


BOILER = ('祖传的手艺不想丢了', '计划每日两题', 'leetcode-cn.com/problems', 'leetcode.cn/problems', '最后附上python代码')


def yid_parts(path):
    t = body(open(path, encoding='utf-8').read())
    lines = []
    for line in t.split('\n'):
        if line.startswith('> [!info]') or line.startswith('> 力扣：') or line.startswith('# '):
            continue
        if any(b in line for b in BOILER[:3]):
            continue
        lines.append(line)
    s = '\n'.join(lines)
    s = re.sub(r'\n\s*"""\n(\s*:type[^\n]*\n|\s*:rtype[^\n]*\n|\s*\n)*\s*"""', '', s)  # strip :type docstrings
    s = re.sub(r'\[\[[^|\]]*\|([^\]]*)\]\]', r'\1', s)
    return squeeze(s)


n = 0
for it in items:
    if not it['todo'] or (ONLY and it['key'] not in ONLY):
        continue
    k = it['key']
    head = [f"# {it['id']}. {it['title']}", '',
            f"- 题号 `num`：{it['id'] if it['id'].isdigit() else repr(it['id'])}（配置文件名 `{k}.py`）",
            f"- 难度：{it['diff'] or '未知'}" + (f" · 难度分 {it['rating']}" if it.get('rating') else ''),
            f"- 待做：{', '.join({'ling': '灵茶山艾府 → configs/ling_all/' + k + '.py', 'yiduobo': 'yiduobo → configs/yiduobo_all/' + k + '.py'}[a] for a in it['todo'])}",
            f"- 所在刷题路径：{'、'.join(it['paths']) or '（无）'}"]
    stmt = sol = topics = ''
    if it['ling']:
        meta, topics, stmt, sol = ling_parts(os.path.join(ROOT, '灵茶山艾府题解/solutions', it['ling']))
    if topics:
        head.append('- 灵神题单位置：' + topics.replace('\n', ' ').replace('- ', ''))
    parts = ['\n'.join(head), '']
    parts += ['## 题目描述', '', stmt if stmt else
              '（库里没有题面。根据 yiduobo 文章和你对这道 LeetCode 题的了解写题意；拿不准题意就按规则跳过，写明原因“题意不明”。）', '']
    if it['key'] in CODE:
        lang, src = CODE[it['key']]
        if lang == 'go':
            sol += ('\n\n### 灵神原文代码（Go，来自力扣原题解；本库归档时只保留了 Python，这里补回）\n\n'
                    '**原文为 Go**：请按任务说明「灵神原文只有 Go 代码时」逐行等价转写为 Python 3。\n\n```go\n' + src.rstrip() + '\n```')
        else:
            sol += '\n\n### 灵神原文代码（Python，来自力扣原题解，本库归档时漏掉了）\n\n```python\n' + src.rstrip() + '\n```'
    if 'ling' in it['todo'] or (it['ling'] and sol):
        ref = 'ling' not in it['todo']
        if ref and len(sol) > 1500:
            sol = sol[:1500] + '\n……（参考部分已截断）'
        parts += ['## 灵茶山艾府题解' + ('（仅供参考，本题不做灵神视频）' if ref else ''), '', sol or '（无正文）', '']
    if it['yiduobo']:
        parts += [f"## yiduobo 题解（{it['yiduobo'][:-3]}）" + ('' if 'yiduobo' in it['todo'] else '（仅供参考，本题不做 yiduobo 视频）'), '',
                  yid_parts(os.path.join(ROOT, 'yiduobo题解/solutions', it['yiduobo'])), '']
    open(os.path.join(OUT, k + '.md'), 'w', encoding='utf-8').write('\n'.join(parts))
    n += 1
print('briefs', n)
