S0, WORDS = 'season', ['sea', 'seas', 'son', 'on']


def _phase2(S):
    return 'res' in S


def _text(S):
    if _phase2(S):
        now = S.get('now')
        if now is None:
            return '第二步：记忆化搜索 `res[i]` = 前 i 位的所有拆法，从 `res[6]` 开始往回拼'
        if now == 0:
            return '`dfs(now = 0)`：空前缀，递归边界'
        return f"`dfs({now})`：求前 {now} 位 \"{S0[:now]}\" 的所有拆法，最后一个单词从 {'/'.join(S['f'][now])} 中选"
    if 'j' not in S or 'i' not in S:
        return '第一步：`f[i]` 记下「能结尾在第 i 位的单词」（空 = 前 i 位拆不开）'
    i, j = S['i'], S['j']
    ok = S0[j:i] in WORDS
    left = '`j == 0`' if j == 0 else f"`f[{j}]` {'非空' if S['f'][j] else '为空'}"
    return f"分割点 `j = {j}`：{left}，`s[{j}:{i}]` = \"{S0[j:i]}\" {'==∈ 字典==' if ok else '∉ 字典'}"


def _fcolor(S, k, v):
    if _phase2(S):
        now = S.get('now')
        return 'yellow' if k == now else ('green' if v != '·' else None)
    if k == S.get('i'):
        return 'yellow'
    if k == S.get('j'):
        return 'blue'
    return 'green' if v != '·' else None


def _cap_if(S, B, ret):
    i, j, s = S.i, S.j, S.s
    seg = s[j:i]
    if j == 0:
        head = '`j == 0`'
    elif S.f[j]:
        head = f'`f[{j}]` 非空'
    else:
        return f'`f[{j}]` 为空：前 {j} 位拆不开 → 跳过'
    if seg in S.word_set:
        return head + f'，且 `"{seg}"` 在字典里 → 成立'
    return head + f'，但 `"{seg}"` 不在字典里'


def _cap_for_i(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '`f` 填完：每个 `f[i]` 都记下了所有可能的「最后一个单词」'
    return f'`f[{S.i}]`：枚举分割点 `j = 0..{S.i - 1}`'


def _cap_memo(S, B, ret):
    if not B.res[B.now]:
        return f'`res[{B.now}]` 还没算过 → 置为 `[]`，现在算'
    return f'`res[{B.now}]` 已经算过 → ==直接用记忆=='


def _cap_word(S, B, ret):
    if 'word' in S and (B.get('word') != S.word or B.get('now') != S.now or S['_line'] == 23 and 'word' not in B):
        return f'最后一个单词选 `"{S.word}"` → 递归求前 `{S.now} − {len(S.word)} = {S.now - len(S.word)}` 位的所有拆法'
    return f'`f[{S.now}]` 里的单词都试过了'


def _draw_sf(cv, S, B, box, T):
    """s 的字符夹在 f 的格子之间：f[i] 在第 i 个字符之后（= 前 i 位）"""
    x0, y0, x1, y1 = box
    f = S.get('f')
    n = len(S0)
    width = x1 - x0 - 40
    cell = min(110, width / (n + 1))
    sx = x0 + 20 + (width - cell * (n + 1)) / 2
    cv.text((x0 + 18, y0 + 4), 's 与 f[i]（f[i] 在第 i 个字符之后 = 前 i 位；黄 = 当前，蓝 = 分割点 j）', 22, T['muted'], bold=True)
    yc, yfr = y0 + 44, y0 + 128
    seg, segc = None, None
    if _phase2(S):
        if 'word' in S and S.get('now') and S['_line'] in (23, 25) and S['word'] in (f[S['now']] if f else []):
            seg, segc = (S['now'] - len(S['word']), S['now']), T['green']
    elif 'j' in S and 'i' in S:
        seg, segc = (S['j'], S['i']), T['cyan']
    for k, ch in enumerate(S0):
        X = sx + (k + 1) * cell
        on = seg is not None and seg[0] <= k < seg[1]
        cv.rect((X - cell * 0.36, yc, X + cell * 0.36, yc + 56), fill=segc if on else T['panel2'], r=8, outline=T['border'])
        cv.text((X, yc + 28), ch, 30, T['bg'] if on else T['text'], anchor='mm', bold=True, mono=True)
    if f is None:
        return
    for i in range(n + 1):
        X = sx + i * cell
        w = f[i]
        txt = '/'.join(w) if w else '·'
        c = _fcolor(S, i, txt)
        fill = T[c] if c else T['panel2']
        cv.rect((X + 4, yfr, X + cell - 4, yfr + 70), fill=fill, r=10, outline=T['border'])
        fs = 26 if len(txt) <= 6 else 20
        cv.text((X + cell / 2, yfr + 35), txt, fs, T['bg'] if c else T['muted'], anchor='mm', bold=True)
        cv.text((X + cell / 2, yfr + 76), i, 18, T['dim'], anchor='mt', mono=True)
    if not _phase2(S):
        for r, (name, c) in enumerate((('j', T['blue']), ('i', T['yellow']))):
            v = S.get(name)
            if isinstance(v, int):
                X = sx + v * cell + cell / 2
                cv.tri_up(X, yfr + 102, 9, c)
                cv.text((X, yfr + 116), name, 20, c, anchor='mt', bold=True)


def _draw_res(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(S0)
    width = x1 - x0 - 40
    cell = min(110, width / (n + 1))
    sx = x0 + 20 + (width - cell * (n + 1)) / 2
    cv.text((x0 + 18, y0 + 4), 'res[i]：前 i 位的所有拆法（· = 还没算，[] = 正在算）', 22, T['muted'], bold=True)
    res = S.get('res')
    if res is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    bres = B.get('res') or res
    now = S.get('now')
    top, bot = y0 + 40, y1 - 30
    for i in range(n + 1):
        X = sx + i * cell
        r = res[i]
        changed = r != bres[i]
        fill = T['yellow'] if i == now else (T['green'] if r else T['panel2'])
        cv.rect((X + 4, top, X + cell - 4, bot), fill=fill, r=10, outline=T['yellow'] if changed else T['border'],
                width=3 if changed else 1)
        tc = T['bg'] if (i == now or r) else T['muted']
        if r is None:
            cv.text((X + cell / 2, (top + bot) / 2), '·', 26, tc, anchor='mm', bold=True)
        elif not r:
            cv.text((X + cell / 2, (top + bot) / 2), '[]', 24, tc, anchor='mm', bold=True)
        else:
            lines = [' '.join(x) for x in r]
            lh = min(30, (bot - top - 10) / len(lines))
            y = (top + bot) / 2 - lh * (len(lines) - 1) / 2
            for ln in lines:
                cv.text((X + cell / 2, y), ln, 19, tc, anchor='mm', bold=True)
                y += lh
        cv.text((X + cell / 2, bot + 4), i, 18, T['dim'], anchor='mt', mono=True)


CONFIG = dict(
    num=140, title='单词拆分 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='DP 记下结尾单词 + 记忆化搜索拼方案',
    tags=['字节30天'],
    code='''
class Solution(object):
    def wordBreak(self, s, wordDict):
        word_set = set(wordDict)
        f = [[] for _ in range(len(s) + 1)]

        for i in range(1, len(s) + 1):
            for j in range(i):
                if (j == 0 or len(f[j]) > 0) and s[j : i] in word_set:
                    f[i].append(s[j : i])

        if not f[len(s)]:
            return []

        res = [None] * (len(s) + 1)
        self.dfs(f, len(s), res)
        return [' '.join(x) for x in res[len(s)]]

    def dfs(self, f, now, res):
        if now == 0:
            return [[]]
        if not res[now]:
            res[now] = []
            for word in f[now]:
                tmp = self.dfs(f, now - len(word), res)
                res[now].extend(x + [word] for x in tmp)

        return res[now]
''',
    call=f'Solution().wordBreak("{S0}", {WORDS})',
    expect=['sea son', 'seas on'],
    skip=['for j in range(i)', 'f = [[]', 'res[now] = []', 'tmp = self.dfs', 'res = [None]', 'if now == 0'],
    views=[
        dict(type='text', fn=_text, h=56),
        dict(type='custom', draw=_draw_sf, h=265),
        dict(type='custom', draw=_draw_res, h=175),
        dict(type='calls', h=125, hide=('f', 'res')),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'blue'), ('now', 'now', 'yellow'), ('word', 'word', 'green')],
    captions={
        'word_set = set': '字典转成集合；`f` 开 `len(s) + 1` 个空列表',
        'for i in range': _cap_for_i,
        'if (j == 0': _cap_if,
        'f[i].append': lambda S, B, r: f'记下 `"{S.s[S.j:S.i]}"` → `f[{S.i}] = {S.f[S.i]}`' + ('；==不 break==，所有单词都要' if len(S.f[S.i]) > 1 else ''),
        'if not f[len(s)]': '`f[{len(s)}] = {f[len(s)]}` 非空 → 能拆，接着把方案拼出来',
        'self.dfs(f, len(s), res)': '`res = [None] * {len(s) + 1}` 当记忆；从整个串 `now = {len(s)}` 开始搜索',
        'return [[]]': '`now == 0`：空前缀只有一种拆法——返回 `[[]]`（一个空方案）',
        'if not res[now]': _cap_memo,
        'for word in f[now]': _cap_word,
        'res[now].extend': lambda S, B, r: f'前 {S.now - len(S.word)} 位的每种拆法后面拼上 `"{S.word}"` → `res[{S.now}] = {S.res[S.now]}`',
        'return res[now]': '返回 `res[{now}]`（同时已存进记忆）',
        "return [' '.join": '每种方案用空格连起来：=={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='f[i] 存下所有能结尾在第 i 位的单词，再记忆化搜索把方案拼出来',
        complexity='DP `O(n³)`；拼方案与答案总长度同阶（最坏指数级）',
        problem=['给字符串 `s` 和字典 `wordDict`，在 `s` 中加空格拆成字典里的单词',
                 '返回==所有==可能的句子（单词可重复使用）',
                 '示例：`"catsanddog"` → `["cats and dog","cat sand dog"]`',
                 '本视频：`"season"`，`["sea","seas","son","on"]` → `["sea son","seas on"]`'],
        quote='对于140题……f[i]表示s的前i位如果能被拆分，那么==当前这一位可能拆成哪些单词==。……在求出最后的f[len(s)]后，使用记忆化搜索，res[i]表示前i位的拆分方案。',
        quote_src='—— yiduobo 题解原文（139 & 140 合写的一篇）',
        idea=['和 139 一样枚举分割点 j：前 j 位能拆、`s[j:i]` 是单词 → 把这个单词加进 `f[i]`',
              '`f[n]` 为空直接返回 `[]`，避免无谓的搜索',
              '`dfs(now)`：枚举 `f[now]` 里的最后一个单词 word，先求前 `now − len(word)` 位的方案，再拼上 word'],
        summary=['DP 部分 `O(n³)`（分割点 `O(n²)` × 切片 `O(n)`）；拼方案的代价取决于答案个数',
                 '易错：`now == 0` 要返回 `[[]]`（一种空方案），不是 `[]`',
                 '`f` 只存能拼通的单词，所以 dfs 不会走进死路',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
