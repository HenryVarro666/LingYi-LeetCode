def _kids(n):
    return list(n.childs.items())


def _draw(cv, S, B, box, T):
    t = S.get('t')
    root = t.root if t is not None else S.get('self.root')
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'Trie（节点 = 前缀数 prefix_cnt / 结尾数 end_cnt；黄 = now）', 24, T['muted'], bold=True)
    if root is None:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2), '（Trie 还没创建）', 28, T['muted'], anchor='mm')
        return
    pos, order, depth = {}, [], [0]

    def width(n):
        return max(1, sum(width(c) for _, c in _kids(n)))

    def place(n, d, left):
        depth[0] = max(depth[0], d)
        pos[id(n)] = (left + width(n) / 2, d)
        order.append((n, _kids(n)))
        cl = left
        for _, c in _kids(n):
            place(c, d + 1, cl)
            cl += width(c)
    total = width(root)
    place(root, 0, 0)
    top, bot = y0 + 80, y1 - 70
    gap = min((bot - top) / max(1, depth[0]), 96)
    W = x1 - x0 - 60
    unit = min(W / total, 200)
    sx = x0 + 30 + (W - unit * total) / 2

    def xy(n):
        px, d = pos[id(n)]
        return sx + px * unit, top + d * gap
    cur = S.get('now')
    for n, ks in order:
        X, Y = xy(n)
        for e, c in ks:
            X2, Y2 = xy(c)
            cv.line([(X, Y + 18), (X2, Y2 - 18)], T['muted'], 3)
            cv.text(((X + X2) / 2 - 16, (Y + Y2) / 2), str(e), 24, T['cyan'], anchor='mm', bold=True, mono=True)
    for n, ks in order:
        X, Y = xy(n)
        s = f'{n.prefix_cnt}/{n.end_cnt}'
        hot = cur is n
        cv.rect((X - 36, Y - 18, X + 36, Y + 18), fill=T['yellow'] if hot else (T['green'] if n.end_cnt > 0 else T['panel2']),
                outline=T['blue'], width=3, r=18)
        cv.text((X, Y), s, 20, T['bg'] if hot or n.end_cnt > 0 else T['text'], anchor='mm', bold=True, mono=True)
    rx, ry = xy(root)
    cv.text((rx - 46, ry), 'root', 20, T['muted'], anchor='rm')
    cv.text((x0 + 18, y1 - 4), '绿 = 有单词在此结束（end_cnt > 0）', 20, T['muted'], anchor='lb')


def _info(S):
    r = S.get('r')
    return f'已返回的查询结果 `r = {r}`' if r else '每个节点两个计数：prefix_cnt（经过它的单词数）、end_cnt（在此结束的单词数）'


CONFIG = dict(
    num=1804, title='实现 Trie （前缀树） II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='Trie 节点记 end_cnt / prefix_cnt',
    tags=['灵神题单·常用数据结构', '字典树'],
    code='''
class Node(object):

    def __init__(self):
        self.childs = {}
        self.end_cnt = 0
        self.prefix_cnt = 0

class Trie(object):

    def __init__(self):
        self.root = Node()

    def insert(self, word):

        now = self.root
        for char in word:
            if char not in now.childs:
                node = Node()
                now.childs[char] = node

            now = now.childs[char]
            now.prefix_cnt += 1
        
        now.end_cnt += 1

    def countWordsEqualTo(self, word):

        now = self.root
        for char in word:
            if char not in now.childs:
                return 0
            now = now.childs[char]
        
        return now.end_cnt

    def countWordsStartingWith(self, prefix):

        now = self.root
        for char in prefix:
            if char not in now.childs:
                return 0
            now = now.childs[char]
        
        return now.prefix_cnt

    def erase(self, word):

        now = self.root
        for char in word:
            now = now.childs[char]
            now.prefix_cnt -= 1
        
        now.end_cnt -= 1
''',
    call='''t = Trie()
r = []
t.insert("ab"); t.insert("abc"); t.insert("ab")
r.append(t.countWordsEqualTo("ab"))
r.append(t.countWordsStartingWith("ab"))
t.erase("ab")
r.append(t.countWordsEqualTo("ab"))
r.append(t.countWordsStartingWith("ab"))
r''',
    expect=[2, 3, 1, 2],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', h=70, size=28, fn=_info),
    ],
    watch=[('char', 'char', 'pink'), ('word', lambda S: S.get('word', S.get('prefix')), 'cyan'),
           ('now.prefix_cnt', lambda S: S['now'].prefix_cnt if S.get('now') is not None else None, 'orange'),
           ('now.end_cnt', lambda S: S['now'].end_cnt if S.get('now') is not None else None, 'green')],
    captions={
        17: lambda S, B, r: f'`{S.char}` 这条边' + ('不存在 → ==要新建节点==' if S.char not in B.now.childs else '已存在，直接走'),
        19: '新节点挂到 `{char}` 这条边上',
        22: '走到 `{char}` 节点：经过它的单词又多一个，`prefix_cnt` → =={now.prefix_cnt}==',
        24: '单词到此结束：`end_cnt` → =={now.end_cnt}==（同一个单词出现的次数）',
        30: lambda S, B, r: f'`{S.char}` 这条边' + ('不存在 → 单词没出现过，返回 0' if S.char not in S.now.childs else '存在，继续走'),
        40: lambda S, B, r: f'`{S.char}` 这条边' + ('不存在 → 没有这个前缀，返回 0' if S.char not in S.now.childs else '存在，继续走'),
        32: '走到 `{char}` 节点',
        42: '走到 `{char}` 节点',
        34: '走完整个单词，当前节点的 `end_cnt` = ==`{now.end_cnt}`== 就是它出现的次数',
        44: '走完整个前缀，当前节点的 `prefix_cnt` = ==`{now.prefix_cnt}`== 就是以它为前缀的单词数',
        50: '走到 `{char}` 节点（单词一定存在，不用判断）',
        51: '经过它的单词少一个：`prefix_cnt` → =={now.prefix_cnt}==',
        53: '`end_cnt` 减 1 → =={now.end_cnt}==：删掉一个单词，节点本身不拆',
    },
    skip=['self.childs = {}', 'self.end_cnt = 0', 'self.prefix_cnt = 0', 'self.root = Node()', 'now = self.root', 'node = Node()',
          16, 21, 29, 39, 49],
    max_steps=110,
    cards=dict(
        one_liner='Trie 每个节点多记两个数：经过它的单词数，和在此结束的单词数',
        complexity='每次操作 `O(len(word))`，空间 `O(总字符数)`',
        problem=['实现 Trie：`insert`、`countWordsEqualTo`、`countWordsStartingWith`、`erase`',
                 '`countWordsEqualTo(w)`：`w` 在 Trie 里出现几次；`countWordsStartingWith(p)`：以 `p` 为前缀的有几个',
                 '本视频：插入 `ab`、`abc`、`ab`，查询，删掉一个 `ab` 再查询'],
        quote='对于其中的每个节点，都需要额外维护两个成员变量end_cnt以及prefix_cnt，分别表示当前字符串出现的次数以及当前字符串为前缀的字符串的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['插入：沿路每走到一个节点，`prefix_cnt += 1`；走完最后一个字符，`end_cnt += 1`',
              '查询：沿路走，走不通返回 0；走完返回 `end_cnt` 或 `prefix_cnt`',
              '删除：沿路 `prefix_cnt -= 1`，最后 `end_cnt -= 1`，节点本身不用拆'],
        summary=['插入、查询、删除都是 `O(len)`，空间 `O(总字符数)`',
                 '`erase` 保证单词存在，所以不用判断 `char in childs`',
                 '删除只减计数，不删节点：计数为 0 的节点等价于不存在',
                 '原文可直接在 Python 3 运行，没有改动（类名 `Node` 会覆盖预置的 `Node`）'],
    ),
)
