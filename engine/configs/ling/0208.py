def _kids(node):
    return list(node.son.items())


def _path_len(root, target):
    """cur 在第几层（= 已经走过的字符数）"""
    stack = [(root, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is target:
            return d
        stack += [(ch, d + 1) for _, ch in _kids(nd)]
    return None


def draw_trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S.get('self.root')
    word = S.get('prefix', S.get('word'))
    cur = S.get('cur')
    d = _path_len(root, cur) if (root is not None and cur is not None) else None
    # 顶部：当前单词，已走过的字符标绿
    if isinstance(word, str):
        cv.text((x0 + 20, y0 + 30), 'prefix' if 'prefix' in S else 'word', 22, T['muted'], anchor='lm')
        for k, ch in enumerate(word):
            X = x0 + 100 + k * 50
            c = T['green'] if d is not None and k < d else (T['yellow'] if k == d else T['panel2'])
            cv.rect((X, y0 + 10, X + 44, y0 + 50), fill=c, r=8)
            cv.text((X + 22, y0 + 30), ch, 26, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((x0 + 120 + len(word) * 50, y0 + 30), '绿 = 已走过的字母，黄 = 当前字母', 19, T['dim'], anchor='lm')
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
    top, R = y0 + 110, 24
    sp = min(170, (x1 - x0 - 80) / n)
    dy = min(90, (y1 - top - 60) / max(1, D + 1))

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
        fill = T['green'] if nd.end else T['panel2']
        hot = nd is cur
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['yellow'] if hot else T['border'], width=5 if hot else 2)
        if hot:
            cv.text((X + R + 6, Y), 'cur', 20, T['yellow'], anchor='lm', bold=True)
        for _, ch in _kids(nd):
            nodes(ch)
    edges(root)
    nodes(root)
    if type(S.get('self')).__name__ == 'Node' and cur is not None and id(cur) in pos:  # 正在执行 Node()：新节点还没挂上去
        X, Y = P(cur)
        GX, GY = X + (sp * 0.6 if _kids(cur) else 0), Y + dy
        cv.dashed((X, Y + R), (GX, GY - R), T['yellow'], 3)
        cv.d.ellipse((GX - R, GY - R, GX + R, GY + R), outline=T['yellow'], width=3)
        cv.text((GX + R + 6, GY), f"新节点（马上挂到 {S.get('c')!r} 上）", 19, T['yellow'], anchor='lm')
    rx, ry = P(root)
    cv.text((rx - R - 8, ry), 'root', 20, T['muted'], anchor='rm')
    cv.text((x1 - 20, y1 - 16), '绿色节点 = end（某个单词在这里结束）', 19, T['dim'], anchor='rb')


def _who(S):
    return 'startsWith' if 'prefix' in S else 'search'


def _ret0(S, B, ret):
    return f'`{S.c!r}` 不是 `cur` 的儿子：==道不同，不相为谋== → `find` 返回 0，`{_who(S)}` 得到 `False`'


def _ret12(S, B, ret):
    tail = f'`startsWith` 只要非 0 → `True`' if 'prefix' in S else f'`search` 要求等于 2 → `{ret == 2}`'
    kind = '完全匹配' if ret == 2 else '只是前缀'
    return f'走过同样的路，`cur.end = {S.cur.end}` → 返回 =={ret}==（{kind}）；{tail}'


CONFIG = dict(
    num=208, title='实现 Trie (前缀树)', difficulty='Medium', category='图论',
    author='灵茶山艾府', technique='26 叉树（字典存儿子）',
    code='''
class Node:
    __slots__ = 'son', 'end'

    def __init__(self):
        self.son = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        cur = self.root
        for c in word:
            if c not in cur.son:  # 无路可走？
                cur.son[c] = Node()  # 那就造路！
            cur = cur.son[c]
        cur.end = True

    def find(self, word: str) -> int:
        cur = self.root
        for c in word:
            if c not in cur.son:  # 道不同，不相为谋
                return 0
            cur = cur.son[c]
        # 走过同样的路（2=完全匹配，1=前缀匹配）
        return 2 if cur.end else 1

    def search(self, word: str) -> bool:
        return self.find(word) == 2

    def startsWith(self, prefix: str) -> bool:
        return self.find(prefix) != 0
''',
    call='''t = Trie()
t.insert("cat"); t.insert("car"); t.search("ca"); t.startsWith("ca"); t.search("cow")
t.search("car")''',
    expect=True,
    skip=['self.son = {}', 'self.end = False'],
    views=[dict(type='custom', draw=draw_trie, h=560)],
    watch=[('word', lambda S: S.get('prefix', S.get('word'))), 'c', ('cur.end', lambda S: S['cur'].end)],
    captions={
        'self.root = Node()': '创建 Trie：一开始只有一个空的根节点 `root`',
        13: 'insert(`{word!r}`)：从根节点出发',
        'for c in word': lambda S, B, ret: (f'下一个字母 `c = {S.c!r}`' if _path_len(S['self.root'], S.cur) < len(S.word)
                                            else f'`{S.word!r}` 的字母都走完了'),
        'if c not in cur.son:  # 无路可走': lambda S, B, ret: (f'`{S.c!r}` 不在 `cur.son` 里：==无路可走==' if S.c not in S.cur.son
                                                             else f'`{S.c!r}` 已经在 `cur.son` 里：有路，直接走（共享前缀）'),
        'cur.son[c] = Node()': '那就造路！新建一个节点，作为 `cur` 的儿子 `{c!r}`',
        'cur = cur.son[c]': '沿着 `{c!r}` 往下走一层',
        'cur.end = True': '走完了：把最后一个节点标记为 ==end==，表示有单词在这里结束',
        21: '从根节点出发，查找 `{word!r}`',
        'if c not in cur.son:  # 道不同': lambda S, B, ret: (f'`{S.c!r}` 不在 `cur.son` 里 → 走不下去' if S.c not in S.cur.son
                                                           else f'`{S.c!r}` 在 `cur.son` 里，继续走'),
        'return 0': _ret0,
        'return 2 if cur.end else 1': _ret12,
        'return self.find(word) == 2': 'search(`{word!r}`)：调用 `find`，==必须完全匹配==（返回 2）',
        'return self.find(prefix) != 0': 'startsWith(`{prefix!r}`)：调用 `find`，==只要路径存在==（返回非 0）',
    },
    max_steps=70,
    cards=dict(
        one_liner='把字母看成方向，单词就是一条从根出发的路径',
        complexity='insert/search/startsWith 都是 `O(n)`，`n` 为单词长度',
        problem=['实现 `Trie`：`insert(word)` 插入单词，`search(word)` 判断单词是否插入过',
                 '`startsWith(prefix)` 判断是否有已插入的单词以 `prefix` 开头',
                 '本视频：插入 `cat`、`car`，再查 `ca`(F)、前缀 `ca`(T)、`cow`(F)、`car`(T)'],
        quote='“若我俩都走过同样的路，则我俩心意相通。”假设字符串里只有 a 和 b，把 a 视作往左走，把 b 视作往右走……推广到 26 种字母，其实就是一棵 26 叉树。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`insert`：沿路径走，==无路可走就造路==，最后把终点标记为 `end`',
              '`search` 和 `startsWith` 复用同一个 `find`：返回 0 = 走不通，1 = 前缀匹配，2 = 完全匹配',
              '`search` 要求返回 2，`startsWith` 只要非 0'],
        summary=['时间：每次操作 `O(n)`；空间：所有插入单词的总长度',
                 '==search 必须检查 end==：插入 `cat` 后，`ca` 有路径但不是单词',
                 '`__slots__` 可以省内存；儿子也可以用长为 26 的列表（题解的另一种写法）',
                 '共享前缀的单词共用节点：`cat`、`car` 共用 `c → a`'],
    ),
)
