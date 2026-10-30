def _trie(cv, box, T, root, kids, label, cur, title, foot=''):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
    if root is None:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2), '（trie 还没创建）', 28, T['muted'], anchor='mm')
        return
    pos = {}
    order = []

    def width(node, d):
        ks = kids(node) if d < 7 else []
        w = sum(width(c, d + 1) for _, c in ks)
        return max(1, w)

    depth = [0]

    def place(node, d, left, w_total):
        depth[0] = max(depth[0], d)
        ks = kids(node) if d < 7 else []
        w = width(node, d)
        pos[id(node)] = ((left + w / 2), d)
        order.append((node, d, ks))
        cl = left
        for _, c in ks:
            cw = width(c, d + 1)
            place(c, d + 1, cl, w_total)
            cl += cw
    total = width(root, 0)
    place(root, 0, 0, total)
    top, bot = y0 + 70, y1 - 56
    gap = (bot - top) / max(1, depth[0]) if depth[0] else 0
    gap = min(gap, 96)
    W = x1 - x0 - 60
    unit = min(W / total, 190)
    sx = x0 + 30 + (W - unit * total) / 2

    def xy(node):
        px, d = pos[id(node)]
        return sx + px * unit, top + d * gap
    for node, d, ks in order:
        X, Y = xy(node)
        for e, c in ks:
            X2, Y2 = xy(c)
            cv.line([(X, Y + 18), (X2, Y2 - 18)], T['muted'], 3)
            cv.text(((X + X2) / 2 + (X2 - X) * 0.0 - 14, (Y + Y2) / 2), str(e), 24, T['cyan'], anchor='mm', bold=True, mono=True)
    for node, d, ks in order:
        X, Y = xy(node)
        s = label(node)
        w = max(40, len(s) * 13 + 20)
        w = min(w, unit - 6) if unit - 6 > 40 else w
        is_cur = cur is not None and node is cur
        cv.rect((X - w / 2, Y - 18, X + w / 2, Y + 18), fill=T['yellow'] if is_cur else T['panel2'],
                outline=T['blue'], width=3, r=18)
        cv.text((X, Y), s, 20, T['bg'] if is_cur else T['text'], anchor='mm', bold=True, mono=True)
    if foot:
        cv.text((x0 + 18, y1 - 4), foot, 20, T['muted'], anchor='lb')


def _lab(n):
    ml = '∞' if n.min_len == inf else str(n.min_len)
    return f"{ml}/{getattr(n, 'best_index', '-')}"


def _kids(n):
    return [(chr(97 + i), c) for i, c in enumerate(n.son) if c is not None]


def _draw(cv, S, B, box, T):
    root = S.get('root')
    _trie(cv, box, T, root, _kids, _lab, S.get('cur'), '反转后的字典树（节点 = 最短长度 / 下标；黄 = 当前节点）',
          '从右往左读字符 = 反转后读前缀；每个节点存「经过它的最短串」')


def _depth(root, node, d=0):
    if root is node:
        return d
    for c in root.son:
        if c is not None:
            r = _depth(c, node, d + 1)
            if r >= 0:
                return r
    return -1


def _chk(S):
    if _depth(S.root, S.cur) == len(S.s):
        raise ValueError('loop end')
    return ''


def _info(S):
    if 'ans' not in S:
        return '把字符串从右往左读，最长公共后缀 → 最长公共前缀；子树根存 ==最短串及下标=='
    return f'`ans = {S["ans"]}`'


CONFIG = dict(
    num=3093, title='最长公共后缀查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='反向读 + 字典树节点存最短串',
    tags=['灵神题单·常用数据结构', '字典树', '难度分 2118'],
    code='''
class Node:
    __slots__ = 'son', 'min_len', 'best_index'

    def __init__(self):
        self.son = [None] * 26
        self.min_len = inf  # 子树中的最短字符串的长度

class Solution:
    def stringIndices(self, wordsContainer: List[str], wordsQuery: List[str]) -> List[int]:
        ord_a = ord('a')
        root = Node()
        for i, s in enumerate(wordsContainer):
            len_s = len(s)
            if len_s < root.min_len:
                root.min_len = len_s
                root.best_index = i

            # 把 s[::-1] 插入字典树
            cur = root
            for ch in reversed(s):
                c = ord(ch) - ord_a
                if cur.son[c] is None:
                    cur.son[c] = Node()
                cur = cur.son[c]
                # 维护 cur 子树中的最短字符串的长度及其下标
                # 由于我们是按照 i 从小到大的顺序遍历，字符串长度相同时不更新 best_index
                if len_s < cur.min_len:
                    cur.min_len = len_s  
                    cur.best_index = i

        ans = []
        for s in wordsQuery:
            cur = root
            for ch in reversed(s):
                c = ord(ch) - ord_a
                if cur.son[c] is None:
                    break
                cur = cur.son[c]
            # 退出循环时，cur 即最长公共前缀（的对应节点），cur.best_index 是前缀为 cur 的最短字符串的下标
            ans.append(cur.best_index)
        return ans
''',
    call='Solution().stringIndices(["abc", "ab", "xbc"], ["bc", "zc", "xyz"])',
    expect=[0, 0, 1],
    views=[
        dict(type='array', var='wordsContainer', label='wordsContainer', cell=80, h=130, pointers={'i': 'blue'}),
        dict(type='array', var='wordsQuery', label='wordsQuery', cell=80, h=130, index=False,
             color=lambda S, i, v: 'blue' if S.get('s') == v and 'ans' in S else None),
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', h=70, size=28, fn=_info),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch', 'pink'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'root = Node()': '根节点代表「空串」：它的 `min_len` 初始是 ∞，先建好',
        'if len_s < root.min_len': '`len_s = {len_s}`，根 = 所有串的公共前缀（空），比较 `{len_s} < {root.min_len}`：更短才更新（相等不更新，下标小的优先）',
        'root.min_len = len_s': '根记下最短串：长度 `{len_s}`',
        'root.best_index = i': '根的最优下标 = `{i}`；就算查询和谁都没有公共后缀，也回答这个',
        'for ch in reversed(s)': lambda S, B, r: _chk(S) or (f'`ch = {S.ch}`：从右往左读 `{S.s}`（等价于反转后插入前缀树）' if 'ans' not in S
                                                  else f'`ch = {S.ch}`：查询串也从右往左读，沿字典树往下走'),
        'if cur.son[c] is None:': lambda S, B, r: (
            f'`{S.ch}` 这条边' + ('不存在 → ==新建节点==' if S.cur.son[ord(S.ch) - 97] is None else '已存在，直接走') if 'ans' not in S
            else (f'`{S.ch}` 这条边不存在 → 后缀匹配到此为止，==break==' if S.cur.son[ord(S.ch) - 97] is None
                  else f'`{S.ch}` 这条边存在 → 继续往下')),
        'cur.son[c] = Node()': '新建子节点，边 `{ch}`',
        'if len_s < cur.min_len': lambda S, B, r: f'走到子节点，比较子树最短长度 `{S.len_s} < {S.cur.min_len}`' + (' → ==更短，更新==' if S.len_s < S.cur.min_len else '：不更短 → 保留原来的（同长时下标小的优先）'),
        'cur.min_len = len_s': '`min_len = {len_s}`',
        'cur.best_index = i': '`best_index = {i}`：这个后缀下目前最优的串是 `{wordsContainer[i]}`',
        'ans = []': '字典树建好了，开始处理查询',
        'for s in wordsQuery': '查询 `{s}`：从根出发，尽量往下走',
        'cur = root': lambda S, B, r: ('每次插入都从根出发' if 'ans' not in S else '每次查询都从根出发'),
        'ans.append(cur.best_index)': lambda S, B, r: f'停在的节点就是最长公共后缀；它子树里的最短串下标 ==`{S.cur.best_index}`== → 对 `{S.s}` 的答案',
        'return ans': '全部查询答完：`{ans}`',
    },
    skip=['self.son = [None]', 'self.min_len = inf', 'ans = []', 'cur = root', 'cur.son[c] = Node()', 'cur = cur.son[c]', 'ord_a = ord', 'c = ord(ch) - ord_a', 'len_s = len(s)'],
    max_steps=140,
    cards=dict(
        one_liner='从右往左读 = 前缀问题；字典树每个节点记住子树里最短的串',
        complexity='时间 `O(L1·26 + L2)`，空间 `O(L1·26)`',
        problem=['给两个字符串数组，对每个 `wordsQuery[i]`，在 `wordsContainer` 里找和它最长公共后缀的串',
                 '并列时取长度最短的，再并列取下标最小的；输出下标数组',
                 '本视频：`["abc","ab","xbc"]`，查询 `["bc","zc","xyz"]` → `[0,0,1]`'],
        quote='有着相同前缀的字符串，都在同一棵子树中。为了 O(1) 找到子树中的最短字符串，我们可以在子树的根节点处，保存子树中的最短字符串长度 minLen 及其下标。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把字符串反转（或从右到左遍历），公共后缀变成公共前缀',
              '同一棵子树里的串前缀相同，所以每个节点只要存「子树内最短串的长度和下标」',
              '按下标从小到大插入，长度相同不更新，天然满足「下标小优先」；查询走到哪个节点就答哪个节点'],
        summary=['时间 `O(L1·26 + L2)`，空间 `O(L1·26)`，L1、L2 是两个数组的总长度',
                 '根节点也要维护：查询和任何串都没有公共后缀时，答案是全局最短串',
                 '严格小于才更新：长度相同保留更早的下标',
                 '`best_index` 没在 `__init__` 里赋值，由插入时第一次更新写入（用了 `__slots__`）'],
    ),
)
