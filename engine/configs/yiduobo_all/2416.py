_CUR = 'now'
_WLABEL = 'word'
_LEGEND = '节点里的数字 = weight（经过它的字符串个数）'


def _kids(node):
    return list(node.childs.items())


def _root(S):
    return S.get('root')


def _word(S):
    return S.get('word')


def _label(S, nd):
    return nd.weight if nd is not S.get('root') else None


def _note(S, nd):
    return None


def _path_len(root, target):
    stack = [(root, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is target:
            return d
        stack += [(ch, d + 1) for _, ch in _kids(nd)]
    return None


def draw_trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = _root(S)
    word = _word(S)
    cur = S.get(_CUR)
    d = _path_len(root, cur) if (root is not None and cur is not None) else None
    if isinstance(word, str):
        cv.text((x0 + 20, y0 + 30), _WLABEL, 22, T['muted'], anchor='lm')
        for k, ch in enumerate(word):
            X = x0 + 150 + k * 50
            c = T['green'] if d is not None and k < d else (T['yellow'] if k == d else T['panel2'])
            cv.rect((X, y0 + 10, X + 44, y0 + 50), fill=c, r=8)
            cv.text((X + 22, y0 + 30), ch, 26, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((x0 + 170 + len(word) * 50, y0 + 30), '绿 = 已走过，黄 = 当前字母', 19, T['dim'], anchor='lm')
    if root is None:
        cv.text((x0 + 20, y0 + 90), '（Trie 尚未创建）', 24, T['dim'])
        return
    pos, cnt = {}, [0]

    def lay(nd, dep):
        ch = _kids(nd)
        if not ch:
            pos[id(nd)] = (cnt[0], dep)
            cnt[0] += 1
            return cnt[0] - 1
        xs = [lay(c, dep + 1) for _, c in ch]
        pos[id(nd)] = ((xs[0] + xs[-1]) / 2, dep)
        return pos[id(nd)][0]
    lay(root, 0)
    n = max(1, cnt[0])
    D = max(p[1] for p in pos.values())
    top, R = y0 + 100, 24
    sp = min(190, (x1 - x0 - 80) / n)
    dy = min(110, (y1 - top - 70) / max(1, D + 1))

    def P(nd):
        x, dep = pos[id(nd)]
        return x0 + (x1 - x0) / 2 + (x - (n - 1) / 2) * sp, top + dep * dy

    def edges(nd):
        X, Y = P(nd)
        for c, ch in _kids(nd):
            X2, Y2 = P(ch)
            cv.line([(X, Y), (X2, Y2)], T['border'], 3)
            mx, my = (X + X2) / 2 + (18 if X2 > X + 1 else -18 if X2 < X - 1 else 22), (Y + Y2) / 2
            cv.rect((mx - 15, my - 15, mx + 15, my + 15), fill=T['panel'], outline=T['border'], r=6)
            cv.text((mx, my), c, 22, T['code'], anchor='mm', mono=True, bold=True)
            edges(ch)

    def nodes(nd):
        X, Y = P(nd)
        hot = nd is cur
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['panel2'],
                     outline=T['yellow'] if hot else T['border'], width=5 if hot else 2)
        lab = _label(S, nd)
        if lab is not None:
            cv.text((X, Y), lab, 24, T['green'], anchor='mm', bold=True)
        note = _note(S, nd)
        if note:
            cv.text((X, Y + R + 6), note, 17, T['cyan'], anchor='mt')
        if hot:
            cv.text((X - R - 6, Y - 4), _CUR, 20, T['yellow'], anchor='rm', bold=True)
        for _, ch in _kids(nd):
            nodes(ch)
    edges(root)
    nodes(root)
    rx, ry = P(root)
    cv.text((rx + R + 8, ry), 'root', 20, T['muted'], anchor='lm')
    cv.text((x1 - 20, y1 - 16), _LEGEND, 19, T['dim'], anchor='rb')


CONFIG = dict(
    num=2416, title='字符串的前缀分数和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='Trie 树 · weight 记前缀出现次数',
    tags=['字典树', '难度分 1725'],
    code='''
class Node(object):

    def __init__(self):
        self.weight = 0
        self.childs = {}

class Solution(object):
    def sumPrefixScores(self, words):

        root = Node()
        for word in words:
            now = root
            for char in word:
                if char not in now.childs:
                    now.childs[char] = Node()
                now = now.childs[char]
                now.weight += 1

        res = []
        for word in words:
            now = root
            res.append(0)
            for char in word:
                now = now.childs[char]
                res[-1] += now.weight

        return res
''',
    call='Solution().sumPrefixScores(["abc", "ab", "b"])',
    expect=[5, 4, 1],
    skip=['self.weight = 0', 'self.childs = {}'],
    views=[
        dict(type='array', var='words', label='words（黄 = 当前处理的字符串）', h=150, cell=70,
             color=lambda S, i, v: 'yellow' if S.get('word') == v else None),
        dict(type='custom', draw=draw_trie, h=580),
        dict(type='array', var='res', label='res', h=120, cell=70),
    ],
    watch=['word', 'char', ('now.weight', lambda S: S['now'].weight if 'now' in S else None, 'green')],
    captions={
        'root = Node()': '先建一个空的根节点：`weight = 0`，`childs` 是空字典',
        'now = root': '`now` 回到根节点，准备走 `{word!r}`',
        'for char in word': lambda S, B, ret: (f'下一个字符 `char = {S.word[_path_len(S.root, S.now)]!r}`' if _path_len(S.root, S.now) < len(S.word)
                                               else f'`{S.word!r}` 的字符都走完了'),
        'if char not in now.childs': lambda S, B, ret: (f'`{S.char!r}` 不在 `now.childs` 里：这个前缀第一次出现' if S.char not in S.now.childs
                                                      else f'`{S.char!r}` 已经在 `now.childs` 里：和之前的字符串共用这条路'),
        'now.childs[char] = Node()': '新建一个节点，挂在 `now` 的 `{char!r}` 下面',
        'now = now.childs[char]': '走到 `{char!r}` 对应的节点',
        'now.weight += 1': '这个前缀又出现了一次：`weight` → ==`{now.weight}`==',
        'res = []': '第二遍：再走一遍每个字符串，累加路径上的 `weight`',
        'res.append(0)': '给 `{word!r}` 在 `res` 末尾放一个 0，等着累加',
        'res[-1] += now.weight': '这个前缀出现 `{now.weight}` 次 → `res[-1]` 累计为 ==`{res[-1]}`==',
        'return res': '每个字符串的前缀出现次数都累加完了，返回 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='涉及所有前缀，就上 Trie：节点上记录前缀出现次数',
        complexity='时间 `O(L)`（L 为总字符数），空间 `O(L)`',
        problem=['每个字符串的每个前缀，都要数一数它在 `words` 里作为前缀出现了几次',
                 '再把同一个字符串的所有前缀的次数加起来，字符串本身也算前缀',
                 '本视频：`["abc","ab","b"]` → `[5,4,1]`'],
        quote='题目要求计算每个字符串的每种前缀在所有字符串中出现的次数，既然涉及到了所有前缀，那么很自然想到使用trie树来解决。',
        quote_src='—— yiduobo 题解',
        idea=['在常规 Trie 的基础上，每个节点多记一个 ==`weight`==：有多少个字符串经过它',
              '第一遍：逐个字符串插入，路过的节点 `weight += 1`',
              '第二遍：再走一次每个字符串，把路上每个节点的 `weight` 加到 `res[-1]`'],
        summary=['时间 `O(L)`，空间 `O(L)`，`L` 是所有字符串长度之和',
                 '==先把所有字符串都插入==，再统一查询，否则 `weight` 还不完整',
                 '`res.append(0)` 之后用 `res[-1]` 累加，不需要额外的 sum 变量',
                 '原文为 Python 2 风格（`class X(object)`），Python 3 下可直接运行，代码未做修改'],
    ),
)
