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
        return max(1, sum(width(c, d + 1) for _, c in ks))

    depth = [0]

    def place(node, d, left):
        depth[0] = max(depth[0], d)
        ks = kids(node) if d < 7 else []
        w = width(node, d)
        pos[id(node)] = (left + w / 2, d)
        order.append((node, d, ks))
        cl = left
        for _, c in ks:
            place(c, d + 1, cl)
            cl += width(c, d + 1)
    total = width(root, 0)
    place(root, 0, 0)
    top, bot = y0 + 70, y1 - 56
    gap = min((bot - top) / max(1, depth[0]), 96)
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
            cv.text(((X + X2) / 2 - 14, (Y + Y2) / 2), str(e), 24, T['cyan'], anchor='mm', bold=True, mono=True)
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


def _draw(cv, S, B, box, T):
    tr = S.get('trie')
    root = tr.root if tr is not None else None
    _trie(cv, box, T, root, lambda n: list(n.childs.items()), lambda n: f'{n.index}/{n.length}',
          S.get('now'), '反转后的 trie（节点 = 下标 index / 长度 length；黄 = now）',
          '每个节点存「经过它的、最短且下标最小」的单词')


def _info(S):
    if 'trie' not in S:
        return '翻转单词和查询：最长公共后缀 → 最长公共前缀；节点记 ==index / length=='
    if 'now' in S and 'char' in S:
        return f'`char = {S["char"]}`，当前节点 `index = {S["now"].index}`，`length = {S["now"].length}`'
    return ''


CONFIG = dict(
    num=3093, title='最长公共后缀查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='翻转 + trie 节点记 index/length',
    tags=['灵神题单·常用数据结构', '字典树', '难度分 2118'],
    code='''
class TreeNode(object):
    def __init__(self, index, length):
        self.childs = {}
        self.index = index
        self.length = length

    def update(self, new_index, new_length):
        if new_length < self.length or (new_length == self.length and new_index < self.index):
            self.index = new_index
            self.length = new_length

class Trie(object):
    def __init__(self, root_index, root_length):
        self.root = TreeNode(root_index, root_length)
    
    def add(self, s, s_index):
        now = self.root
        length = len(s)
        for char in s[::-1]:
            now.update(s_index, length)
            if char not in now.childs:
                now.childs[char] = TreeNode(s_index, length)
            now = now.childs[char]

        now.update(s_index, length)
    
    def find(self, s):
        now = self.root
        for char in s[::-1]:
            if char not in now.childs:
                break
            now = now.childs[char]
        
        return now.index

class Solution(object):
    def stringIndices(self, wordsContainer, wordsQuery):

        trie = Trie(0, len(wordsContainer[0]))
        for index, s in enumerate(wordsContainer):
            trie.add(s, index)
        
        return [trie.find(s) for s in wordsQuery]
''',
    call='Solution().stringIndices(["abc", "ab", "xbc"], ["bc", "zc", "xyz"])',
    expect=[0, 0, 1],
    views=[
        dict(type='array', var='wordsContainer', label='wordsContainer', cell=80, h=150,
             color=lambda S, i, v: 'blue' if S.get('index') == i and 'now' in S and 's_index' in S else None),
        dict(type='array', var='wordsQuery', label='wordsQuery', cell=80, h=150, index=False,
             color=lambda S, i, v: 'blue' if S.get('s') == v and 'trie' in S and 'index' not in S else None),
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', h=70, size=28, fn=_info),
    ],
    watch=[('s', 's', 'cyan'), ('char', 'char', 'pink'), ('length', 'length', 'orange'), ('s_index', 's_index', 'blue')],
    captions={
        'trie = Trie(0, len': '建 trie：根节点先记下 `wordsContainer[0]`，下标 `0`、长度 `{len(wordsContainer[0])}`，保证没有公共后缀时也有答案',
        'for index, s in enumerate': lambda S, B, r: (f'第 `{S.index}` 个单词 `{S.s}`：翻转后插入 trie' if B.get('index') != S.index
                                                      else '单词都插入完了，trie 建好，开始处理查询'),
        'trie.add(s, index)': '把 `{s}` 倒着插入，沿途更新每个节点的 index/length',
        19: '`char = {char}`：从右往左读，等价于翻转后读前缀',
        29: '查询 `{s}` 倒着读：`char = {char}`',
        'if new_length < self.length': lambda S, B, r: (
            f'新单词 `(下标 {S.new_index}, 长度 {S.new_length})` vs 节点已记 `({S.self.index}, {S.self.length})`：'
            + ('==更优，替换==' if (S.new_length < S.self.length or (S.new_length == S.self.length and S.new_index < S.self.index)) else '不更优，保留')),
        'self.index = new_index': '`index` → `{self.index}`',
        'self.length = new_length': '`length` → `{self.length}`',
        21: lambda S, B, r: f'`{S.char}` 这条边' + ('不存在 → ==新建节点==' if S.char not in S.now.childs else '已存在，直接走'),
        22: '新建子节点 `{char}`，初始记当前单词：index `{s_index}`，length `{length}`',
        25: '走完最后一个字符，也要更新终点节点',
        30: lambda S, B, r: f'`{S.char}` 这条边' + ('不存在 → 匹配到此为止，==break==' if S.char not in S.now.childs else '存在 → 继续往下走'),
        31: '无路可走，停在当前节点',
        'return now.index': '`now` 停在最长公共后缀对应的节点，答案 ==`{now.index}`==（该后缀下最短、最靠前的单词）',
    },
    skip=['self.childs = {}', 'self.index = index', 'self.length = length', 'self.root = TreeNode', 'now = self.root', 'return [trie.find',
          'now.update(s_index, length)', 'now = now.childs[char]', 'length = len(s)'],
    max_steps=130,
    cards=dict(
        one_liner='翻转后求最长公共前缀；trie 每个节点记最短且最靠前的单词',
        complexity='时间 `O(L1 + L2)`（字符集小），空间 `O(L1)`',
        problem=['给两个字符串数组，对每个 `wordsQuery[i]`，在 `wordsContainer` 里找与它最长公共后缀的串',
                 '并列时取长度最短，再并列取下标最小；输出下标数组',
                 '本视频：`["abc","ab","xbc"]`，查询 `["bc","zc","xyz"]` → `[0,0,1]`'],
        quote='对于公共后缀问题，如果将单词和查询都翻转，那么原题中的最长公共后缀实际上就变成了最长公共前缀问题，最直观的思路自然是trie树。',
        quote_src='—— yiduobo 题解原文',
        idea=['单词和查询都用 `s[::-1]` 倒着走，后缀问题变成前缀问题',
              '每个节点额外记 `index` 和 `length`，`update` 里先比长度、再比下标',
              '查询时尽量往下走，走不动就停，当前节点的 `index` 就是答案'],
        summary=['时间 `O(L1 + L2)`，空间 `O(L1)`，L1、L2 是两个数组的总长度',
                 '根节点也要初始化为第 0 个单词：没有任何公共后缀时回答它',
                 '`update` 同时处理「更短」和「同长更靠前」两种情况',
                 '对比灵神：灵神把 index/min_len 直接写进插入循环；yiduobo 封装成 `update` 方法'],
    ),
)
