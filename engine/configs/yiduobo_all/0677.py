def _kids(nd):
    return list(nd.next_char.items())


def draw_trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S.get('self.trie')
    cur = S.get('now')
    word = S.get('key', S.get('prefix'))
    name = 'key' if 'key' in S else 'prefix'
    # 这一步 now 走到了第几个字符
    depth = {}

    def walk(nd, d):
        depth[id(nd)] = d
        for _, c in _kids(nd):
            walk(c, d + 1)
    if root is not None:
        walk(root, 0)
    d = depth.get(id(cur)) if cur is not None else None
    if isinstance(word, str):
        cv.text((x0 + 20, y0 + 30), name, 22, T['muted'], anchor='lm')
        for k, ch in enumerate(word):
            X = x0 + 100 + k * 50
            c = T['green'] if d is not None and k < d else (T['yellow'] if k == d else T['panel2'])
            cv.rect((X, y0 + 10, X + 44, y0 + 50), fill=c, r=8)
            cv.text((X + 22, y0 + 30), ch, 26, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((x0 + 120 + len(word) * 50, y0 + 30), '绿 = 已走过，黄 = 当前字符', 19, T['dim'], anchor='lm')
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
    top, R = y0 + 110, 26
    sp = min(170, (x1 - x0 - 80) / n)
    dy = min(100, (y1 - top - 70) / max(1, D + 1))

    def P(nd):
        x, dep = pos[id(nd)]
        return x0 + (x1 - x0) / 2 + (x - (n - 1) / 2) * sp, top + dep * dy

    def edges(nd):
        X, Y = P(nd)
        for c, ch in _kids(nd):
            X2, Y2 = P(ch)
            cv.line([(X, Y), (X2, Y2)], T['border'], 3)
            mx, my = (X + X2) / 2, (Y + Y2) / 2
            cv.rect((mx - 15, my - 15, mx + 15, my + 15), fill=T['panel'], outline=T['border'], r=6)
            cv.text((mx, my), c, 22, T['code'], anchor='mm', mono=True, bold=True)
            edges(ch)

    def nodes(nd):
        X, Y = P(nd)
        hot = nd is cur
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['yellow'] if hot else T['panel2'],
                     outline=T['yellow'] if hot else T['border'], width=5 if hot else 2)
        cv.text((X, Y), str(nd.sum), 26, T['bg'] if hot else T['text'], anchor='mm', bold=True, mono=True)
        if hot:
            cv.text((X + R + 8, Y), 'now', 20, T['yellow'], anchor='lm', bold=True)
        for _, ch in _kids(nd):
            nodes(ch)
    edges(root)
    nodes(root)
    rx, ry = P(root)
    cv.text((rx - R - 8, ry), 'root', 20, T['muted'], anchor='rm')
    cv.text((x1 - 20, y1 - 16), '圆圈里的数字 = 经过该节点的所有词的权重之和（sum）', 19, T['dim'], anchor='rb')


def _depth(S):
    root, cur = S.get('self.trie'), S.get('now')
    st = [(root, 0)]
    while st:
        nd, d = st.pop()
        if nd is cur:
            return d
        st += [(c, d + 1) for _, c in _kids(nd)]
    return None


def _for(S, B, ret):
    w = S['key'] if 'prefix' not in S else S['prefix']
    if _depth(S) == len(w):
        return f'`{w}` 的字符都走完了'
    return f'下一个字符 `{S.char!r}`'


def _info(S):
    if 'delta' in S and 'key' in S:
        return f'插入 `{S["key"]}`：本次要加到路径上每个节点的权重差 `delta` = ==%s==' % S['delta']
    if 'prefix' in S:
        return f'查询前缀 `{S["prefix"]}`：沿路走到底，读最后一个节点的 `sum`'
    return '每个节点的 `sum` = 以“根到它”为前缀的所有词的权重和'


CONFIG = dict(
    num=677, title='键值映射', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='字典树 + 节点前缀和',
    tags=['灵神题单', '常用数据结构'],
    code='''
class TreeNode(object):

    def __init__(self):
        self.next_char = {}
        self.sum = 0

class MapSum(object):

    def __init__(self):
        self.trie = TreeNode()
        self.key_dict = {}

    def insert(self, key, val):
        now = self.trie
        if key in self.key_dict:
            delta = val - self.key_dict[key]
        else:
            delta = val
        self.key_dict[key] = val

        for char in key:
            if char not in now.next_char:
                tmp = TreeNode()
                now.next_char[char] = tmp
            
            now = now.next_char[char]
            now.sum += delta

    def sum(self, prefix):
        now = self.trie
        for char in prefix:
            if char not in now.next_char:
                return 0
            now = now.next_char[char]
        
        return now.sum
''',
    call='''m = MapSum()
m.insert("ab", 3)
m.insert("ac", 2)
m.insert("ab", 5)
m.sum("a")''',
    expect=7,
    views=[
        dict(type='custom', draw=draw_trie, h=470),
        dict(type='map', var='self.key_dict', label='key_dict（每个词当前的权重）', fmt=lambda k, v: f"'{k}': {v}", h=120, font=30),
        dict(type='text', h=80, size=30, fn=_info),
    ],
    watch=[('key', lambda S: S.get('key')), ('delta', 'delta', 'orange'), ('prefix', lambda S: S.get('prefix')), 'char'],
    captions={
        'self.trie = TreeNode()': '根节点：`next_char` 存子节点，`sum` 存前缀权重和',
        'self.key_dict = {}': '`key_dict` 记录每个词当前的权重，用来算覆盖时的差值',
        'now = self.trie': lambda S, B, ret: (f'`insert({S.key!r}, {S.val})`：从根出发' if 'key' in S and 'prefix' not in S
                                              else f'`sum({S.prefix!r})`：从根出发'),
        'if key in self.key_dict': lambda S, B, ret: (
            f'`{S.key!r}` 之前插入过吗？' + ('是 → 只需加“新权重 − 旧权重”' if S.key in S['self.key_dict'] else '否 → 差值就是 `val`')),
        'delta = val - self.key_dict[key]': '已存在：新权重 `{val}` − 旧权重 `{val - delta}`，差值 `delta` = =={delta}==，路径上每个节点只加这个差',
        'delta = val': '新词：`delta = {delta}`',
        'self.key_dict[key] = val': '记下 `{key!r}` 的新权重 `{val}`',
        'for char in key': _for,
        'for char in prefix': _for,
        'self.next_char = {}': '新节点：`next_char` 是空字典（还没有子节点）',
        'self.sum = 0': '新节点：`sum = 0`',
        'if char not in now.next_char': lambda S, B, ret: (
            (f'`{S.char!r}` 还不是当前节点的子节点 → ==要新建节点==' if S.char not in S.now.next_char
                                                         else f'`{S.char!r}` 已经是子节点 → 直接走过去')),
        'tmp = TreeNode()': '新建一个子节点（`sum = 0`）',
        'now.next_char[char] = tmp': '把新节点挂到 `{char!r}` 这条边上',
        'now = now.next_char[char]': '走到 `{char!r}` 对应的子节点',
        'now.sum += delta': '途经节点都加上 `delta`：这个节点的 `sum` = =={now.sum}==（以该前缀开头的词权重和）',
        'return 0': '`{char!r}` 走不通，没有词以这个前缀开头 → 返回 `0`',
        'return now.sum': '前缀走完，当前节点的 `sum` 就是答案 `{ret}`，不用再往下遍历',
    },
    max_steps=90,
    cards=dict(
        one_liner='每个 Trie 节点直接存“以此为前缀的权重和”',
        complexity='`insert` / `sum` 都是 `O(L)`，`L` 为词长；空间 `O(总长度)`',
        problem=['设计 `MapSum`：`insert(key, val)` 插入键值对，键已存在则覆盖',
                 '`sum(prefix)` 返回所有以 `prefix` 开头的键的值之和',
                 '本视频：`ab=3`、`ac=2`，再把 `ab` 改成 5，查前缀 `a` → 7'],
        quote='对于每个节点我们额外维护从根节点到当前节点这一前缀的所有词的前缀之和。……若其已经出现在词表中，那么我们计算这个词要新插入的权重与之前插入的权重的差值，然后从根节点往下走，对于途经的所有节点都加上该差值。',
        quote_src='—— yiduobo 题解',
        idea=['普通 Trie 多加一个 `sum`：插入时沿路径把权重加上去',
              '覆盖旧值时不能重复加，只加==差值== `val − 旧值`，所以要有 `key_dict`',
              '查询时走到前缀末尾的节点，直接返回它的 `sum`'],
        summary=['时间：插入、查询都 `O(L)`；空间 `O(总字符数)`',
                 '==覆盖更新要加差值==，直接加 `val` 会重复计数',
                 '前缀不存在时要返回 `0`，别忘了 `char not in next_char` 的判断',
                 '原文为 Python 2 风格，删去了 `__init__` 里的 `"""docstring"""`'],
    ),
)
