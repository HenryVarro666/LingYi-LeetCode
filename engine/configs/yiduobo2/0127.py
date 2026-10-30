import views as V

BEGIN, END = 'hit', 'cog'
WORDS = ['hot', 'dot', 'dog', 'lot', 'log', 'cog']

# 画图用的固定坐标（相对位置，0~1）
POS = {'hit': (0.06, 0.5), 'hot': (0.27, 0.5), 'dot': (0.5, 0.18), 'lot': (0.5, 0.82),
       'dog': (0.73, 0.18), 'log': (0.73, 0.82), 'cog': (0.94, 0.5)}
LEVEL_COLORS = ['purple', 'cyan', 'orange', 'yellow', 'green', 'pink']


def _leak_after(S):
    """当前 word 的 3 个 key 也加进去之后的 leak_dict（内层循环的几行不单独成步）"""
    if 'leak_dict' not in S:
        return None
    d = {k: list(v) for k, v in S['leak_dict'].items()}
    if 'q' in S or 'key' in S and 'word' not in S:
        return d
    w = S.get('word')
    if w is None:
        return d
    done = any(w in v for v in d.values())
    if not done:
        for i in range(len(w)):
            k = w[:i] + '_' + w[i + 1:]
            d.setdefault(k, []).append(w)
    return d


def _edges(S):
    g = S.get('g')
    if g and any(g.values()):
        es = set()
        for a, bs in g.items():
            for b in bs:
                es.add(tuple(sorted((a, b))))
        return es, True
    d = _leak_after(S) or {}
    es = set()
    for ws in d.values():
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                es.add(tuple(sorted((ws[i], ws[j]))))
    return es, False


def _graph(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '图：词 = 点，能一步变换的词连边（颜色 = BFS 层数）', 24, T['muted'], bold=True)
    gx0, gy0, gx1, gy1 = x0 + 70, y0 + 70, x1 - 70, y1 - 40
    P = {w: (gx0 + (gx1 - gx0) * px, gy0 + (gy1 - gy0) * py) for w, (px, py) in POS.items()}
    words = S.get('wordList') or [BEGIN] + WORDS
    es, solid = _edges(S)
    for a, b in sorted(es):
        if a in P and b in P:
            if solid:
                cv.line([P[a], P[b]], T['border'], 3)
            else:
                cv.dashed(P[a], P[b], T['dim'], 2)
    fa = S.get('fa') or {}
    lv = S.get('level_dict') or {}
    for w, ps in fa.items():
        for p in ps or []:
            if p in P and w in P:
                (ax, ay), (bx, by) = P[p], P[w]
                dx, dy = bx - ax, by - ay
                L = max(1, (dx * dx + dy * dy) ** 0.5)
                cv.arrow((ax + dx / L * 36, ay + dy / L * 36), (bx - dx / L * 38, by - dy / L * 38), T['green'], 4, 13)
    now, nxt = S.get('now'), S.get('next_word')
    for w in words:
        if w not in P:
            continue
        X, Y = P[w]
        lvl = lv.get(w, -1)
        fill = V.col(LEVEL_COLORS[lvl % len(LEVEL_COLORS)]) if lvl >= 0 else T['panel2']
        out, wd = T['border'], 2
        if w == nxt and 'q' in S and S.get('_line') != _NOW_LINE:
            out, wd = T['pink'], 6
        if w == now:
            out, wd = T['blue'], 6
        cv.rect((X - 34, Y - 24, X + 34, Y + 24), fill=fill, outline=out, width=wd, r=12)
        cv.text((X, Y), w, 24, T['bg'] if lvl >= 0 else T['text'], anchor='mm', bold=True, mono=True)
        if lvl >= 0:
            cv.text((X, Y + 30), f'第{lvl}层', 18, V.col(LEVEL_COLORS[lvl % len(LEVEL_COLORS)]), anchor='mt', bold=True)
        if w == END:
            cv.text((X, Y - 30), 'end', 18, T['muted'], anchor='mb')
        if w == BEGIN:
            cv.text((X, Y - 30), 'begin', 18, T['muted'], anchor='mb')
    if fa and any(fa.values()):
        cv.text((x1 - 20, y1 - 8), '绿箭头 = fa（上一个词）', 18, T['green'], anchor='rb')


def _info(cv, S, B, box, T):
    st = {'_S': S, '_B': B}
    if 'q' not in S:
        spec = dict(var=_leak_after, label='leak_dict：删去一个字符后的 key → 能形成它的词（黄 = 本步新增）',
                    fmt=lambda k, v: f"{k}: {','.join(v)}", font=21)
    else:
        spec = dict(var=lambda S: {w: d for w, d in S['level_dict'].items() if d >= 0},
                    label='level_dict：到达每个词需要的最少步数（-1 的不显示）', fmt=lambda k, v: f'{k}: {v}', font=22)
    V.v_map(cv, spec, st, box, 0, {})


def _for_word(S, B, ret):
    if S.get('word') == B.get('word') and 'word' in B:
        return '所有词的 key 都整理好了'
    w = S.word
    keys = '、'.join(f'`{w[:i]}_{w[i + 1:]}`' for i in range(len(w)))
    return f'`{w}` 删去一个字符 → {keys}，分别把 `{w}` 记进去'


def _next_cap(S, B, ret):
    nw, now = S.next_word, S.now
    head = f'`{now}` 的邻居 `{nw}`：'
    if B['fa'][nw] is None:
        extra = '（起点的 fa 也是 None，会被再入队一次，不影响答案）' if nw == BEGIN else ''
        return head + f'fa 为 None → ==第一次访问=={extra}'
    if B['level_dict'][nw] == B['level_dict'][now] + 1:
        return head + f'已访问，但层数也是 `{B["level_dict"][now] + 1}` → 同样最短（126 题要记下）'
    return head + f'已访问过（第 {B["level_dict"][nw]} 层）→ 跳过'


def _while_cap(S, B, ret):
    if B.left < B.right:
        return f'`left = {B.left} < right = {B.right}`：队列里还有第 {B.level_dict[B.q[B.left]]} 层的词，按层扩展'
    return '队列空了'


CONFIG = dict(
    num=127, title='单词接龙', difficulty='Hard', category='图论',
    author='yiduobo', technique='删一个字符建图 + 按层 BFS',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def findLadders(self, beginWord, endWord, wordList):
        if beginWord not in wordList:
            wordList.append(beginWord)
        if endWord not in wordList:
            return []

        wordNum = len(wordList)
        wordLen = len(wordList[0])
        g = {word : [] for word in wordList}

        leak_dict = {}
        for word in wordList:
            for index in range(wordLen):
                key = word[:index] + '_' + word[index + 1:]
                if key not in leak_dict:
                    leak_dict[key] = []
                leak_dict[key].append(word)

        for key in leak_dict:
            leak_len = len(leak_dict[key])
            for i in range(leak_len - 1):
                for j in range(i + 1, leak_len):
                    g[leak_dict[key][i]].append(leak_dict[key][j])
                    g[leak_dict[key][j]].append(leak_dict[key][i])

        q = [beginWord]
        fa = {word : None for word in wordList}
        left = 0
        right = 1
        level_dict = {word : -1 for word in wordList}
        level_dict[beginWord] = 0
        while left < right:
            new_right = right
            for index in range(left, right):
                now = q[index]
                for next_word in g[now]:
                    if fa[next_word] is None:
                        q.append(next_word)
                        fa[next_word] = [now]
                        new_right += 1
                        level_dict[next_word] = level_dict[now] + 1
                    elif level_dict[next_word] == level_dict[now] + 1:
                        fa[next_word].append(now)
            if fa[endWord] is not None:
                break
            left = right
            right = new_right

        if fa[endWord] is None:
            return []

        res = [[endWord]]
        for index in range(level_dict[endWord]):
            res = [[y] + x for x in res for y in fa[x[0]]]

        return res
''',
    call=f'''res = Solution().findLadders("{BEGIN}", "{END}", {WORDS!r})
len(res[0]) if res else 0''',
    expect=5,
    views=[
        dict(type='custom', draw=_graph, h=310),
        dict(type='array', var='q', label='q（BFS 队列，框 = 当前层 [left, right)）', cell=84, h=190,
             window=('left', 'right - 1'), pointers={'index': 'blue'}),
        dict(type='custom', draw=_info, h=130),
    ],
    watch=[('left', 'left'), ('right', 'right'), ('new_right', 'new_right'), ('now', 'now', 'blue'),
           ('next_word', 'next_word', 'pink')],
    skip=['wordNum = len', 'for index in range(wordLen)', "key = word[:index]", 'if key not in leak_dict',
          'leak_dict[key] = []', 'leak_dict[key].append(word)',
          'for key in leak_dict', 'leak_len = len', 'for i in range(leak_len', 'for j in range(i + 1',
          'g[leak_dict[key][i]]', 'g[leak_dict[key][j]]', 'q.append(next_word)', 'new_right += 1',
          'left = 0', 'right = 1', 'wordList.append', 'wordLen = len', 'level_dict = {word',
          'level_dict[next_word] = level_dict', 'for index in range(level_dict', 'elif level_dict',
          'for next_word in g[now]', 'for index in range(left, right)', 'new_right = right', 'left = right',
          'if endWord not in wordList', 'fa = {word', 'if fa[endWord] is None', 'res = [[endWord]]', 'res = [[y] + x'],
    captions={
        'if beginWord not in wordList': '`beginWord = hit` 不在词表里 → 先把它加进词表，它也是图中的一个点',
        'if endWord not in wordList': '`endWord = cog` 在词表里（不在就直接无解）',
        'wordLen = len': '所有词长度相同：`wordLen = {wordLen}`',
        'g = {word': '`wordLen = {wordLen}`；邻接表 `g`：每个词一个空列表',
        'leak_dict = {}': '`leak_dict`：把每个词==删去一个字符==后剩下的部分作为 key',
        'for word in wordList:': _for_word,
        'q = [beginWord]': '同一个 key 里的词两两连边，==图就构造好了==；从 `hit` 开始 BFS',
        'fa = {word': '`fa[w]`：w 的上一个词（None = 还没访问）',
        'level_dict[beginWord] = 0': '`fa[w]`：上一个词（None = 未访问）；`level_dict[w]`：最少步数，起点 `hit` 是第 0 层',
        'while left < right': _while_cap,
        'for index in range(left, right)': lambda S, B, ret: (f'取当前层的 `q[{S.index}]`' if S.get('index') != B.get('index') or 'index' not in B
                                                             else '这一层扩展完了'),
        'now = q[index]': '扩展 `{now}`（第 {level_dict[now]} 层）',
        'for next_word in g[now]': lambda S, B, ret: (f'`{S.now}` 的邻居：`{S.next_word}`' if S.get('next_word') != B.get('next_word') or S.get('now') != B.get('now')
                                                     else f'`{S.now}` 的邻居都看完了'),
        'if fa[next_word] is None': _next_cap,
        'fa[next_word] = [now]': '记下 `fa[{next_word}] = [{now}]`，入队；`{next_word}` 在第 =={level_dict[now] + 1}== 层',
        'fa[next_word].append(now)': '同层的另一条最短路：`fa[{next_word}]` 再加入 `{now}` → `{fa[next_word]}`',
        'if fa[endWord] is not None:': lambda S, B, ret: (f'`cog` 被访问到了，在第 {S.level_dict["cog"]} 层 → ==BFS 结束=='
                                                         if S.fa['cog'] is not None else '这一层还没到 `cog`，继续下一层'),
        'break': '`break`：127 的答案已经出来了：`level_dict[cog] + 1` = =={level_dict[endWord] + 1}== 个词',
        'left = right': '下一层：`left` = {left}',
        'right = new_right': '进入下一层：`left, right = {left}, {right}`，当前层是 `q[{left}:{right}]`',
        'if fa[endWord] is None': '`cog` 可达',
        'res = [[endWord]]': '（126 题的部分）从 `cog` 沿 fa 反推所有最短路径',
        'res = [[y] + x': '往前接一层：`res = {res}`',
        'return res': '（126 的部分）沿 fa 从 `cog` 反推出 {len(ret)} 条最短路径，如 `{" → ".join(ret[0])}`，共 =={len(ret[0])}== 个词',
    },
    max_steps=75,
    cards=dict(
        one_liner='删去一个字符得到的 key 相同，两个词就连边；再按层 BFS',
        complexity='建图 `O(N·L²)`；同 key 两两连边，边数最坏 `O(N²)`',
        problem=['从 `beginWord` 变到 `endWord`，每次==只改一个字母==，中间词都要在 `wordList` 里',
                 '求最短转换序列的==单词数==，不存在返回 `0`',
                 '示例：`hit → hot → dot → dog → cog`，答案 `5`'],
        quote='将词作为点，==在同一个key中的词之间两两连上边==，这样图就构造好了。对于127题，直接bfs一边就能得出答案。',
        quote_src='—— yiduobo 题解（126 & 127 合写）',
        idea=['`hit` → `_it`、`h_t`、`hi_`；`hot` 也能形成 `h_t` → 一步可达',
              'BFS 按层扩展，`level_dict` 记到达每个词的最少步数',
              '原文只给了 126 的代码：127 的答案就是 `level_dict[endWord] + 1`'],
        summary=['`left`/`right` 圈出当前层，`new_right` 是下一层的右端',
                 '本视频跑的是原文 126 的代码，取 `len(res[0])` 即 127 的答案',
                 '小坑：`fa[beginWord]` 也是 None，起点会被再入队一次（不影响结果）',
                 '原文为 Python 2 风格：只删去了类型说明文档字符串，代码未改'],
    ),
)

_NOW_LINE = next(i + 1 for i, l in enumerate(CONFIG['code'].strip('\n').split('\n')) if 'now = q[index]' in l)
