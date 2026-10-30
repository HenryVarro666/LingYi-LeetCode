def _kids(n):
    return [(k, c) for k, c in n.childs.items()]


def _layout(root):
    """叶子等距、父节点居中；返回 {id: (col, depth)}, 列数, 深度"""
    pos, cnt = {}, [0]

    def go(n, d):
        ks = _kids(n)
        if not ks:
            pos[id(n)] = (cnt[0], d)
            cnt[0] += 1
            return cnt[0] - 1, d
        cols = [go(c, d + 1)[0] for _, c in ks]
        pos[id(n)] = ((cols[0] + cols[-1]) / 2, d)
        return pos[id(n)]

    go(root, 0)
    return pos, max(cnt[0], 1), max(d for _, d in pos.values())


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'trie：每个节点 = 一个文件夹/文件，节点里的数字 = 文件内容 v', 22, T['muted'], bold=True)
    root = S.get('self.root')
    if root is None:
        return
    pos, w, dep = _layout(root)
    cw = min(210, (x1 - x0 - 60) / w)
    rh = min(130, (y1 - y0 - 160) / max(dep, 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - cw * w) / 2 + cw / 2
    sy = y0 + 80
    P = {k: (sx + c * cw, sy + d * rh) for k, (c, d) in pos.items()}
    now, new = S.get('now'), S.get('node')
    old = set(pos) if 'self.root' in B and B['self.root'] is not None else set()
    stack = [root]
    while stack:
        n = stack.pop()
        for k, c in _kids(n):
            a, b = P[id(n)], P[id(c)]
            cv.line([(a[0], a[1] + 28), (b[0], b[1] - 28)], T['border'], 3)
            cv.text(((a[0] + b[0]) / 2 + 6, (a[1] + b[1]) / 2), k, 22, T['yellow'], anchor='lm', bold=True, mono=True)
            stack.append(c)
    stack = [root]
    while stack:
        n = stack.pop()
        X, Y = P[id(n)]
        hot = n is now
        fill = T['green'] if n is new and 'node' in S else T['panel2']
        cv.rect((X - 54, Y - 28, X + 54, Y + 28), fill=fill, r=14,
                outline=T['blue'] if hot else T['border'], width=6 if hot else 2)
        lab = '/' if n is root else ''
        v = n.v
        txt = (lab + ('  v=%s' % v if v is not None else '')).strip() or '·'
        cv.text((X, Y), txt, 24, T['bg'] if fill == T['green'] else T['text'], anchor='mm', bold=True, mono=True)
        stack.extend(c for _, c in _kids(n))
    if now is not None:
        X, Y = P[id(now)]
        cv.text((X, Y + 40), 'now', 22, T['blue'], anchor='mt', bold=True)


def _loop(S, B, t):
    if 'part' in B and B['part'] == S.part:
        return '所有层都走完了'
    return f'{t}：`{S.part}`'


def _chk(S):
    if S.part not in S.now.childs:
        return f'`{S.part}` 不在孩子里 → ' + ('父目录不存在，==不能创建==' if S['_line'] == 16 else '路径不存在')
    return f'`{S.part}` 存在，继续往下走'


CONFIG = dict(
    num=1166, title='设计文件系统', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='trie 树表示目录',
    tags=['灵神题单'],
    code='''
class Node(object):

    def __init__(self):
        self.childs = {}
        self.v = None

class FileSystem(object):

    def __init__(self):
        self.root = Node()

    def createPath(self, path, value):
        parts = path.split('/')
        now = self.root
        for part in parts[1:len(parts) - 1]:
            if part not in now.childs:
                return False
            now = now.childs[part]
        
        if parts[-1] in now.childs:
            return False
        
        node = Node()
        node.v = value
        now.childs[parts[-1]] = node
        return True

    def get(self, path):
        parts = path.split('/')
        now = self.root
        for part in parts[1:]:
            if part not in now.childs:
                return -1
            now = now.childs[part]
        
        return now.v
''',
    call="""fs = FileSystem()
r = [fs.createPath('/a', 1), fs.createPath('/a/b', 2), fs.createPath('/c/d', 3), fs.createPath('/a/b', 5), fs.get('/a/b'), fs.get('/c')]
r""",
    expect=[True, True, False, False, 2, -1],
    views=[
        dict(type='text', fn=lambda S: f"路径 `{S['path']}` → 拆成 `{S['parts']}`（第 0 项是空串，跳过）" if 'parts' in S else '', size=26, h=60),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=['path', 'part', ('value', 'value', 'green')],
    skip=['self.v = None', 'self.childs = {}', 'self.root = Node()'],
    captions={
        'parts = path.split': '`{path}` 按 `/` 拆开：`{parts}`，下标 0 是空串',
        'now = self.root': '`now` 从根节点出发，根代表 `/`',
        'for part in parts[1:len(parts) - 1]': lambda S, B, r: _loop(S, B, '逐层检查父目录'),
        'if part not in now.childs': lambda S, B, r: _chk(S),
        'now = now.childs[part]': '`now` 走进目录 `{part}`',
        'if parts[-1] in now.childs': lambda S, B, r: (f'`{S.parts[-1]}` 已经存在 → ==不能重复创建==，返回 False' if S.parts[-1] in S.now.childs else f'`{S.parts[-1]}` 还不存在，可以创建'),
        'node = Node()': '新建一个节点，代表文件 `{parts[-1]}`',
        'node.v = value': '节点里记下文件内容 `v = {value}`',
        'now.childs[parts[-1]] = node': '把新节点挂到父目录的 `childs[{parts[-1]!r}]` 下',
        'for part in parts[1:]': lambda S, B, r: _loop(S, B, '`get`：沿路径往下走'),
        'return now.v': '走到最后一层，返回文件内容 `{ret}`',
        'return False': lambda S, B, r: ('父目录不存在 → 返回 `False`' if S['_line'] == 17 else '`False`'),
        'return True': '创建成功，返回 `True`',
        'return -1': '路径不存在 → 返回 `-1`',
    },
    cards=dict(
        one_liner='用 trie 树的节点表示文件夹，节点上多存一个文件内容',
        complexity='每次操作 `O(L)`（L = 路径层数），空间 `O(总层数)`',
        problem=['`createPath(path, value)`：创建路径并记下值；父目录不存在或路径已存在 → `False`',
                 '`get(path)`：返回路径对应的值，路径不存在返回 `-1`',
                 '示例：创建 `/a`、`/a/b` 成功；`/c/d` 的父目录 `/c` 不存在 → `False`'],
        quote='非常标准的trie树的问题，使用trie树中的节点表示文件系统中的文件夹或者文件。为了记录文件的内容，除了常规trie树的孩子节点之外还需要额外添加一个变量记录当前节点的文件内容',
        quote_src='—— yiduobo 题解原文',
        idea=['`path.split("/")` 之后，每一段目录就是 trie 里的一条边',
              '创建：前面的各层必须都已存在，最后一层必须还不存在',
              '查询：沿着边一路走到底，没走通就返回 `-1`'],
        summary=['时间 `O(L)`，空间 `O(总节点数)`',
                 '易错：`parts[0]` 是空串，所以循环从 `parts[1:]` 开始',
                 '创建时只检查「最后一段」是否已存在，中间层必须已存在',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
