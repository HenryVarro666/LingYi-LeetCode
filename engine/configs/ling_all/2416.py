_CUR = 'cur'
_WLABEL = 'word'
_LEGEND = '节点里的数字 = 分数（经过它的字符串个数）'


def _kids(node):
    return [(k, v) for k, v in node.items() if k is not None]


def _root(S):
    return S.get('root')


def _word(S):
    return S.get('word')


def _label(S, nd):
    return nd.get(None) if None in nd else None


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
    author='灵茶山艾府', technique='字典树 · 节点记经过次数',
    tags=['字典树', '难度分 1725'],
    code='''
class Solution:
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        trie = lambda: defaultdict(trie)
        root = trie()
        for word in words:
            cur = root
            for c in word:
                cur = cur[c]
                cur[None] = cur.get(None, 0) + 1  # 更新所有前缀的分数

        ans = []
        for word in words:
            cur, sum = root, 0
            for c in word:
                cur = cur[c]
                sum += cur[None]  # 累加分数，即可得到答案
            ans.append(sum)
        return ans
''',
    call='Solution().sumPrefixScores(["abc", "ab", "b"])',
    expect=[5, 4, 1],
    views=[
        dict(type='array', var='words', label='words（黄 = 当前处理的字符串）', h=150, cell=70,
             color=lambda S, i, v: 'yellow' if S.get('word') == v and S.get('_line', 0) else None),
        dict(type='custom', draw=draw_trie, h=580),
        dict(type='array', var='ans', label='ans', h=120, cell=70),
    ],
    watch=['word', 'c', ('cur 的分数', lambda S: S['cur'].get(None) if 'cur' in S else None, 'green'), ('sum', lambda S: S['sum'] if 'sum' in S else None, 'orange')],
    captions={
        'trie = lambda': '`trie` 是个工厂：每次调用返回一个会自动生成子节点的 `defaultdict`',
        'root = trie()': '根节点：一个空字典，不代表任何字母',
        'for c in word': lambda S, B, ret: (f'下一个字母 `c = {S.word[_path_len(S.root, S.cur)]!r}`' if _path_len(S.root, S.cur) < len(S.word)
                                            else f'`{S.word!r}` 的字母都处理完了'),
        'cur = root': '回到根节点，准备走 `{word!r}`',
        'cur = cur[c]': lambda S, B, ret: (f'沿字母 `{S.c!r}` 走一层：路已经有了（共享前缀）' if None in S.cur
                                           else f'沿字母 `{S.c!r}` 走一层：没有这条路，`defaultdict` 自动造出新节点'),
        'cur[None] = cur.get': '用 `None` 当键存分数：经过这个节点的字符串又多了一个 → 分数 ==`{cur[None]}`==',
        'ans = []': '第二遍：再走一次每个字符串，把路径上的分数加起来',
        'cur, sum = root': '从根出发，`sum = 0` 累加 `{word!r}` 各个前缀的分数',
        'sum += cur[None]': '这个前缀的分数是 `{cur[None]}` → `sum = {sum}`',
        'ans.append(sum)': '`{word!r}` 所有前缀的分数之和 = ==`{sum}`==，存入 `ans`',
        'return ans': '全部算完，返回 `{ans}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='节点在插入时记下“有几个字符串经过我”，分数就是它',
        complexity='时间 `O(L)`（L 为总字符数），空间 `O(L)`',
        problem=['`words` 是一组非空字符串；`term` 的分数 = 以它为前缀的字符串个数',
                 '求每个 `words[i]` 的==所有非空前缀分数之和==，字符串也是自己的前缀',
                 '本视频：`["abc","ab","b"]` → `[5,4,1]`'],
        quote='由于每个节点都是其子树节点的前缀，题干中的分数就是在字符串插入字典树的过程中，经过该节点的字符串个数，即以该节点为前缀的字符串的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一遍：把所有字符串插入字典树，==每经过一个节点分数 +1==',
              '第二遍：再沿同样的路径走一遍，累加路径上每个节点的分数',
              '用 `None` 做键存分数，不会和小写字母的键冲突；`defaultdict` 省掉“无路则造路”的判断'],
        summary=['时间 `O(L)`，空间 `O(L)`，`L` 是所有字符串长度之和',
                 '==分数要在插入时就累加==，第二遍查询时路径一定存在，不用判断',
                 '另一种写法：插入后 DFS 整棵树，累加路径上的分数，节点里用列表存相同字符串的下标',
                 '同类题：208 实现前缀树、1268 搜索推荐系统'],
    ),
)
