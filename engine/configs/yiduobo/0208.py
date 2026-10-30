def _kids(node):
    return [(k, v) for k, v in node.items() if k != 'end']


def _path_len(root, target):
    """now 在第几层（= 已经走过的字符数）"""
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
    cur = S.get('now')
    d = _path_len(root, cur) if (root is not None and cur is not None) else None
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
        end = nd.get('end', False)
        hot = nd is cur
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['green'] if end else T['panel2'],
                     outline=T['yellow'] if hot else T['border'], width=5 if hot else 2)
        if hot:
            cv.text((X + R + 6, Y), 'now', 20, T['yellow'], anchor='lm', bold=True)
        for _, ch in _kids(nd):
            nodes(ch)
    edges(root)
    nodes(root)
    rx, ry = P(root)
    cv.text((rx - R - 8, ry), 'root', 20, T['muted'], anchor='rm')
    cv.text((x1 - 20, y1 - 16), "绿色节点 = 字典里有 'end': True", 19, T['dim'], anchor='rb')


def _for(S, B, ret):
    w = S.get('prefix', S.get('word'))
    if _path_len(S['self.root'], S.now) < len(w):
        return f'下一个字符 `char = {S.char!r}`'
    return f'`{w!r}` 的字符都走完了'


CONFIG = dict(
    num=208, title='实现 Trie (前缀树)', difficulty='Medium', category='图论',
    author='yiduobo', technique='嵌套 dict 实现字典树',
    code='''
class Trie(object):

    def __init__(self):
        self.root = {}

    def insert(self, word):
        now = self.root
        for char in word:
            if char not in now:
                now[char] = {}
            now = now[char]
        now['end'] = True

    def search(self, word):
        now = self.root
        for char in word:
            if char not in now:
                return False
            now = now[char]

        return now.get('end', False)

    def startsWith(self, prefix):
        now = self.root
        for char in prefix:
            if char not in now:
                return False
            now = now[char]

        return True
''',
    call='''t = Trie()
t.insert("cat"); t.insert("car"); t.search("ca"); t.startsWith("ca"); t.search("cow")
t.search("car")''',
    expect=True,
    views=[dict(type='custom', draw=draw_trie, h=560)],
    watch=[('word', lambda S: S.get('prefix', S.get('word'))), 'char',
           ("now 的键", lambda S: list(S['now'].keys()))],
    captions={
        'self.root = {}': '根节点就是一个空 `dict`：键是字符，值是下一层的 `dict`',
        7: 'insert(`{word!r}`)：`now` 从根出发',
        15: 'search(`{word!r}`)：`now` 从根出发',
        24: 'startsWith(`{prefix!r}`)：`now` 从根出发',
        'for char in': _for,
        'if char not in now': lambda S, B, ret: (f'`{S.char!r}` 不在 `now` 里' if S.char not in S.now
                                                 else f'`{S.char!r}` 在 `now` 里：直接迭代过去'),
        "now[char] = {}": '在 `now` 中加入 `{char!r}` 对应的新节点 `{{}}`',
        'now = now[char]': '迭代到 `{char!r}` 对应的节点',
        "now['end'] = True": "最后一个字符：置标记 `now['end'] = True`，表示根到这里的路径是一个词",
        'return False': lambda S, B, ret: f'`{S.char!r}` 走不通 → 返回 `False`',
        "return now.get('end', False)": lambda S, B, ret: (f"路径走完，`now.get('end', False)` = `{ret}` → "
                                                           + ('==是一个完整的词==' if ret else '==只是前缀，不是词==')),
        'return True': '前缀的路径走完了，不需要 `end` 标记 → 返回 `True`',
    },
    max_steps=70,
    cards=dict(
        one_liner='每个节点一个 dict：有这个字符就走过去，没有就新建',
        complexity='insert/search/startsWith 都是 `O(n)`，`n` 为单词长度',
        problem=['实现 `Trie`：`insert(word)` 插入单词，`search(word)` 判断单词是否插入过',
                 '`startsWith(prefix)` 判断是否有已插入的单词以 `prefix` 开头',
                 '本视频：插入 `cat`、`car`，再查 `ca`(F)、前缀 `ca`(T)、`cow`(F)、`car`(T)'],
        quote='对于每个节点都维护一个dict，若当前字符在dict中，那么迭代到dict中的对应节点，否则在dict中加入对应的节点并迭代过去。若当前字符是单词的最后一个字符，则在当前节点中置一个标记。',
        quote_src='—— yiduobo 题解',
        idea=['不定义节点类，直接用==嵌套的 dict==：`{\'c\': {\'a\': {\'t\': {\'end\': True}}}}`',
              '“是不是一个词”用特殊键 `\'end\'` 标记；它有 3 个字符，不会和单个字母冲突',
              '`search` 最后看 `end`，`startsWith` 只要路径存在就返回 `True`'],
        summary=['时间：每次操作 `O(n)`；空间：所有插入单词的总长度',
                 '==search 和 startsWith 的唯一区别==：最后是否检查 `end` 标记',
                 '`now.get(\'end\', False)` 避免了 `KeyError`',
                 '原文为 Python 2 风格，删去了 `"""docstring"""` 和 LeetCode 模板注释'],
    ),
)
