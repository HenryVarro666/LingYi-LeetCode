def _keep(name):
    last = [None]

    def f(S):
        v = S.get(name)
        if isinstance(v, (list, tuple, str)):
            last[0] = v
        return last[0]
    return f


def _l(n):
    return n.length if n is not None else 0


def _trie(S):
    t = S.get('trie')
    if t is not None and getattr(t, 'root', None) is not None:
        return t.root, t.k
    r = S.get('self.root')
    return (r, S.get('self.k')) if r is not None else (None, None)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'trie：w = 经过的单词数，L = 向下 w≥k 的最长路径', 21, T['muted'], bold=True)
    root, k = _trie(S)
    if root is None:
        cv.text((x0 + 18, y0 + 60), '（trie 尚未创建）', 24, T['dim'])
        return
    pos = {}
    cnt = [0]

    def lay(n, d):
        kids = list(n.childs.values())
        if not kids:
            pos[id(n)] = [cnt[0], d]
            cnt[0] += 1
        else:
            for c in kids:
                lay(c, d + 1)
            pos[id(n)] = [sum(pos[id(c)][0] for c in kids) / len(kids), d]

    lay(root, 0)
    depth = max(p[1] for p in pos.values())
    slots = max(cnt[0], 1)
    W = x1 - x0 - 80
    dx = min(190, W / slots)
    sx = x0 + 40 + (W - dx * (slots - 1)) / 2
    top = y0 + 70
    dy = min(150, (y1 - top - 90) / max(depth, 1))
    now = S.get('now')
    cur = S.get('w')
    R = 34

    def xy(n):
        p = pos[id(n)]
        return sx + p[0] * dx, top + p[1] * dy

    def walk(n, ch):
        X, Y = xy(n)
        for c, m in n.childs.items():
            X2, Y2 = xy(m)
            cv.line([(X, Y), (X2, Y2)], T['border'], 3)
        for c, m in n.childs.items():
            walk(m, c)
        ok = n.weight >= k
        fill = T['green'] if ok else T['panel2']
        cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['yellow'] if n is now else T['border'], width=6 if n is now else 2, r=R)
        cv.text((X, Y), ch, 34, T['bg'] if ok else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + R + 8, Y - 4), f'w={n.weight}', 21, T['text'], anchor='lb', bold=True, mono=True)
        cv.text((X + R + 8, Y + 2), f'L={n.length}', 21, T['cyan'], anchor='lt', bold=True, mono=True)

    walk(root, '根')
    if cur is not None:
        cv.text((x1 - 20, y0 + 40), f'当前单词 w = {cur}', 24, T['yellow'], anchor='ra', bold=True)


CONFIG = dict(
    num=3485, title='删除元素后 K 个字符串的最长公共前缀', difficulty='Hard', category='字符串',
    author='yiduobo', technique='Trie 树 + 最大/次大孩子',
    tags=['难度分 2290'],
    code='''
class Node(object):
    def __init__(self):
        self.childs = {}
        self.fa = None
        self.weight = 0
        self.length = 0
        self.first = None
        self.second = None

class Trie(object):
    def __init__(self, words, k):
        self.root = Node()
        self.root.weight = k
        self.k = k
        for w in words:
            self.update(w, 1)
        self.calc_length(self.root)
    
    def update(self, w, delta):
        now = self.root
        for char in w:
            if char not in now.childs:
                now.childs[char] = Node()
                now.childs[char].fa = now
            now = now.childs[char]
            now.weight += delta
        return now

    def get_length(self, node):
        if node is None:
            return 0
        return node.length

    def calc_length(self, now):
        if now.weight < self.k:
            now.length = 0
            return
        
        for char in now.childs:
            self.calc_length(now.childs[char])
            if self.get_length(now.childs[char]) > self.get_length(now.first):
                now.first, now.second = now.childs[char], now.first
            elif self.get_length(now.childs[char]) > self.get_length(now.second):
                now.second = now.childs[char]
        
        now.length = self.get_length(now.first) + 1
    
    def modify_word(self, w):
        now = self.update(w, -1)
        while now:
            if now.weight < self.k:
                now.length = 0
            else:
                now.length = max(self.get_length(now.first), self.get_length(now.second)) + 1
            now = now.fa
        
        res = self.root.length

        now = self.update(w, 1)
        while now:
            if now.weight < self.k:
                now.length = 0
            else:
                now.length = max(self.get_length(now.first), self.get_length(now.second)) + 1
            now = now.fa

        return res - 1

class Solution(object):
    def longestCommonPrefix(self, words, k):
        
        trie = Trie(words, k)
        res = []
        for w in words:
            res.append(trie.modify_word(w))
        return res
''',
    call='Solution().longestCommonPrefix(["ab","ab","ac"], 2)',
    expect=[1, 1, 2],
    views=[
        dict(type='custom', draw=_draw, h=540),
        dict(type='array', var='words', label='words', h=110,
             color=lambda S, i, v: 'yellow' if S.get('w') == v and isinstance(S.get('res'), list) and len(S['res']) == i else None),
        dict(type='array', var=_keep('res'), label='res', h=110),
    ],
    watch=['k', 'w', 'delta', ('res', 'res', 'green')],
    max_steps=48,
    skip=[3, 4, 5, 6, 7, 8, 9, 'self.root.weight = k', 'self.k = k', 'if node is None', 'return 0',
          'return node.length', 'now = self.root', 'for char in w', 'if char not in now.childs',
          'now.childs[char] = Node()', '.fa = now', 'now = now.childs[char]', 'return now', 'now = now.fa',
          'res = []', 'while now', 'for char in now.childs', 'for w in words'],
    captions={
        'self.root = Node()': '先建 trie 的根节点',
        'self.root.weight = k': '根节点的 weight 设成 `k`：空前缀永远算「够 k 个」',
        'self.update(w, 1)': '把单词 `{w}` 插入 trie，路径上每个节点 `weight += 1`',
        'self.calc_length(self.root)': '所有单词插完 → 自底向上算每个节点的 `length`',
        'now.weight += delta': '走到字符 `{char}` 的节点（没有就新建）：`weight` += `{delta}` → =={now.weight}==，即经过它的单词数',
        'if now.weight < self.k': lambda S, B, r: (f'`weight = {S.now.weight} < k = {S.k}`：不够 k 个 → 判断成立，length 记 0' if S.now.weight < S.k else f'`weight = {S.now.weight} >= k = {S.k}`：够 k 个单词共享 → 不成立，继续算 length'),
        'now.length = 0': '这条前缀不足 `k` 个单词 → `length = 0`',
        'if self.get_length(now.childs[char]) > self.get_length(now.first)': '孩子 `{char}` 的 length 比当前最大孩子更大？更大就成为 `first`，旧 first 退为 `second`',
        'elif self.get_length': '没超过 first，那是否超过 `second`？超过就替换 second',
        'now.length = self.get_length(now.first) + 1': lambda S, B, r: f'该节点 length = 最大孩子 length + 1 = `{_l(S.now.first)} + 1` = =={_l(S.now.first) + 1}==',
        'now = self.update(w, -1)': '「删掉」单词 `{w}`：沿路径 `weight -= 1`，得到末尾节点',
        'while now': '自底向上修正祖先的 length（`now` 为空即越过根）',
        'now.length = max': lambda S, B, r: f'重算 `max(first, second) + 1` = `max({_l(S.now.first)}, {_l(S.now.second)}) + 1` = =={max(_l(S.now.first), _l(S.now.second)) + 1}==：删掉的分支可能正是 first，second 要备着',
        'res = self.root.length': '根节点的 length = 删掉 `{w}` 后最长公共前缀长度 + 1（根算一层）：`{res}`',
        'now = self.update(w, 1)': '答案记下了 → 把 `{w}` 加回去（`weight += 1`），再自底向上恢复 length',
        'return res - 1': '根自己多算了 1 层 → 返回 `{res} - 1` = =={res - 1}==',
        'res.append': '对 `{w}` 调用 `modify_word`：删掉它 → 读根的 length → 加回去，结果追加进 `res`',
        'return res': '全部答案 `{res}`',
        'Trie(words, k)': '用 words 建 trie',
    },
    cards=dict(
        one_liner='用 trie 记录每个前缀的单词数，删一个就临时改 weight',
        complexity='时间 `O(L)`，空间 `O(L)`',
        problem=['给 `words` 和 `k`，对每个下标：删去该单词后，任选 `k` 个单词的最长公共前缀长度',
                 '不足 `k` 个时为 0',
                 '本视频：`["ab","ab","ac"], k=2` → `[1,1,2]`'],
        quote='若路径上所有节点的weight都大于等于k，说明至少有k个不同字符串都有这个公共前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['单词都插进 trie，节点记 `weight`（命中该前缀的单词数）',
              '`length` = 往下 weight ≥ k 的最长路径，每个节点还记最大的两个孩子 `first / second`',
              '枚举每个单词：`weight` 减 1，自底向上重算 `length`，读根的 length，再加回去'],
        summary=['时间 `O(L)`（L 为总长度），空间 `O(L)`',
                 '根的 weight 设成 `k`，根的 length 比真实前缀长度多 1，所以返回 `res - 1`',
                 '记最大的两个孩子，是因为删单词后最大孩子可能不够 k 个，要退到次大',
                 '原文已是 Python 3 可运行写法，未作改动'],
    ),
)
