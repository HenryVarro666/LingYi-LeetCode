def _trie(S):
    """从 root 递归布局：返回 (节点列表[(node, depth, x_leaf_pos)], 边列表[(父, 子, 字符)], 叶子数)"""
    root = S.get('root')
    if root is None:
        return [], [], 0
    nodes, edges, cnt = [], [], [0]

    def go(n, d):
        ch = [(c, v) for c, v in n.childs.items()]
        if not ch:
            x = cnt[0]
            cnt[0] += 1
        else:
            xs = []
            for c, v in ch:
                xs.append(go(v, d + 1))
                edges.append((n, v, c))
            x = sum(xs) / len(xs)
        nodes.append((n, d, x))
        return x
    go(root, 0)
    return nodes, edges, max(1, cnt[0])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'trie（节点里的数字 = 权重 w：建树时经过它的次数；黄 = 当前节点 now）', 24, T['muted'], bold=True)
    nodes, edges, leaves = _trie(S)
    if not nodes:
        return
    maxd = max(d for _, d, _ in nodes)
    W, H = x1 - x0 - 120, y1 - y0 - 150
    pos = {}
    for n, d, x in nodes:
        px = x0 + 60 + (x + 0.5) / leaves * W
        py = y0 + 90 + (d / max(1, maxd)) * H * min(1.0, maxd / 3)
        pos[id(n)] = (px, py)
    now = S.get('now')
    for a, b, c in edges:
        (ax, ay), (bx, by) = pos[id(a)], pos[id(b)]
        cv.line([(ax, ay), (bx, by)], T['border'], 3)
        cv.text(((ax + bx) / 2 + 12, (ay + by) / 2), c, 26, T['cyan'], anchor='lm', bold=True, mono=True)
    for n, d, x in nodes:
        px, py = pos[id(n)]
        is_now = n is now
        fill = T['yellow'] if is_now else (70, 76, 86)
        cv.rect((px - 26, py - 26, px + 26, py + 26), fill=fill, r=26)
        label = 'root' if n is S.get('root') else n.w
        cv.text((px, py), label, 18 if label == 'root' else 26, T['bg'] if is_now else T['text'], anchor='mm', bold=True)


def _txt(S):
    if 'pref' not in S:
        return ''
    if 'char' in S and S.get('_line', 0) >= 19:
        return f"查找前缀 `{S['pref']}`：当前字符 `{S['char']}`"
    if 'word' in S:
        return f"建树：word = `{S['word']}`" + (f"，当前字符 `{S['char']}`" if 'char' in S else '')
    return ''


CONFIG = dict(
    num=2185, title='统计包含给定前缀的字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='带权重的 Trie 树', tags=[],
    code='''
class Node(object):
    def __init__(self):
        self.w = 1
        self.childs = {}

class Solution(object):
    def prefixCount(self, words, pref):

        root = Node()
        for word in words:
            now = root
            for char in word:
                if char in now.childs:
                    now = now.childs[char]
                    now.w += 1
                else:
                    tmp = Node()
                    now.childs[char] = tmp
                    now = tmp

        now = root
        for char in pref:
            if char not in now.childs:
                return 0
            now = now.childs[char]
        
        return now.w
''',
    call='Solution().prefixCount(["ab", "abc", "ba", "abd"], "ab")',
    expect=3,
    views=[
        dict(type='text', size=30, h=100, fn=_txt),
        dict(type='custom', draw=_draw, h=460),
    ],
    watch=[('word', 'word', 'blue'), ('char', 'char', 'pink'), ('now.w', lambda S: S['now'].w if S.get('now') is not None else '', 'green')],
    captions={
        'root = Node()': '先建一个空的根节点 `root`',
        'for word in words': lambda S, B, r: (f'依次把每个单词插入 trie：`word = {S.word}`' if S.word != B.get('word') else '单词都插入完了，trie 建好'),
        11: '每个单词都从根节点出发',
        21: '回到根节点，准备沿着 `pref` 查找',
        'for char in word': lambda S, B, r: (f'逐个字符往下走：`char = {S.char}`' if S.char != B.get('char') or S.word != B.get('word') else f'`{S.word}` 的字符走完，换下一个单词'),
        'if char in now.childs': lambda S, B, r: ('`' + S.char + '` 已在当前节点的孩子里 → 沿着走下去，权重加一' if S.char in S.now.childs else '`' + S.char + '` 不在孩子里 → 要新建节点'),
        'now = now.childs[char]': '走到已有节点 `{char}`',
        'now.w += 1': '又有一个单词经过这里：权重 `w` → =={now.w}==',
        'tmp = Node()': '新建节点，权重初始是 1（本单词经过一次）',
        'now.childs[char] = tmp': '挂到当前节点下，边上的字符是 `{char}`',
        'now = tmp': '`now` 走到新节点',
        'for char in pref': lambda S, B, r: (f'找前缀，`char = {S.char}`' if S.char != B.get('char') or B.get('now') is B.get('root') else '`pref` 的字符都匹配上了'),
        'if char not in now.childs': lambda S, B, r: ('`' + S.char + '` 在孩子里，前缀还能匹配' if S.char in S.now.childs else '`' + S.char + '` 不在孩子里 → 没有单词有这个前缀，答案 0'),
        'return 0': '找不到前缀 → `0`',
        'return now.w': '走完整个 `pref`，当前节点的权重 `w = {now.w}` 就是以它为前缀的单词数',
    },
    skip=['self.w = 1', 'self.childs = {}'],
    max_steps=100,
    cards=dict(
        one_liner='trie 的每个节点记「经过次数」，前缀节点的次数就是答案',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['给定字符串数组 `words` 和字符串 `pref`',
                 '返回 `words` 中以 `pref` 作为前缀的字符串个数',
                 '示例：`["pay","attention","practice","attend"]`，`pref="at"` → `2`',
                 '本视频：`["ab","abc","ba","abd"]`，`pref="ab"` → `3`'],
        quote='在常规trie树的基础上给每个节点额外设置了一个权重，表示建树时经过这个节点的次数，这个次数实际上就是数组中包含该前缀的字符串数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据很小，暴力也行；作者选了 trie 来练手',
              '插入时：已有的边就走过去并 `w += 1`，没有的边新建节点',
              '查前缀：沿着 `pref` 走，走不通 → `0`；走得通 → 终点的 `w`'],
        summary=['时间、空间 `O(总字符数)`',
                 '新建节点 `w = 1`，已有节点才 `+= 1`，所以每个节点的 `w` 恰好是经过它的单词数',
                 '易错点：`root` 的权重不参与计数，查找要从 `root.childs` 开始',
                 '原文本身可直接在 Python 3 运行，未做修改；暴力写法 `startswith` 也能过'],
    ),
)
