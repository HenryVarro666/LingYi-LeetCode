def _trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    y0 += 34
    cv.text((x0 + 18, y0 + 4), 'trie（黄 = 当前节点 now，绿框 = final 单词结尾）', 24, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    now = S.get('now')
    pos = {}
    cnt = [0]

    def lay(n, d):
        ks = list(n.childs.items())
        if not ks:
            pos[id(n)] = [cnt[0], d]
            cnt[0] += 1
            return
        for _, c in ks:
            lay(c, d + 1)
        xs = [pos[id(c)][0] for _, c in ks]
        pos[id(n)] = [(min(xs) + max(xs)) / 2, d]

    lay(root, 0)
    maxd = max(p[1] for p in pos.values())
    W = max(cnt[0], 1)
    dx = min(120, (x1 - x0 - 80) / max(W, 1))
    dy = min(78, (y1 - y0 - 110) / max(maxd, 1))
    ox = x0 + (x1 - x0 - dx * (W - 1)) / 2
    oy = y0 + 70

    def xy(n):
        p = pos[id(n)]
        return ox + p[0] * dx, oy + p[1] * dy

    def edges(n):
        for ch, c in n.childs.items():
            a, b = xy(n), xy(c)
            cv.line([(a[0], a[1] + 20), (b[0], b[1] - 20)], T['border'], 3)
            cv.text(((a[0] + b[0]) / 2 + 10, (a[1] + b[1]) / 2), ch, 22, T['cyan'], anchor='lm', bold=True, mono=True)
            edges(c)

    def nodes(n, label):
        X, Y = xy(n)
        isnow = n is now
        cv.rect((X - 20, Y - 20, X + 20, Y + 20), fill=T['yellow'] if isnow else T['panel2'],
                outline=T['green'] if n.final else T['border'], width=5 if n.final else 2, r=20)
        cv.text((X, Y), 'root' if n is root else '', 15, T['bg'] if isnow else T['text'], anchor='mm', bold=True)
        for ch, c in n.childs.items():
            nodes(c, ch)

    edges(root)
    nodes(root, '')


def _text_view(S):
    t = S.get('text')
    if t is None or 'start_pos' not in S:
        return ''
    sp = S['start_pos']
    if 'index' in S and 'char' in S:
        return f"从 `{sp}` 出发，已看 `{t[sp:sp + S['index'] + 1]}`"
    return f'枚举起点 `start_pos = {sp}`'


CONFIG = dict(
    num=1065, title='字符串的索引对', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='Trie 树 + 枚举起点',
    tags=[],
    code='''
class Node(object):

    def __init__(self):
        self.childs = {}
        self.final = False

class Solution(object):
    def indexPairs(self, text, words):

        root = Node()
        for word in words:
            now = root
            for char in word:
                if char not in now.childs:
                    node = Node()
                    now.childs[char] = node
                now = now.childs[char]
            
            now.final = True

        res = []
        for start_pos in range(len(text)):
            now = root
            for index, char in enumerate(text[start_pos:]):
                if char not in now.childs:
                    break
                now = now.childs[char]
                if now.final:
                    res.append([start_pos, start_pos + index])
        
        return res
''',
    call='Solution().indexPairs("ababa", ["aba", "ab"])',
    expect=[[0, 1], [0, 2], [2, 3], [2, 4]],
    views=[
        dict(type='text', fn=_text_view, size=26),
        dict(type='string', var='text', label='text（蓝 = 起点，粉 = 当前字符）',
             pointers={'start_pos': 'blue', 'start_pos + index': 'pink'}, pointer_labels={'start_pos': '起点', 'start_pos + index': '当前'},
             color=lambda S, i, v: 'green' if any(r[0] <= i <= r[1] for r in S.get('res', [])) else None, h=200),
        dict(type='custom', draw=_trie, h=280),
        dict(type='text', fn=lambda S: ('已找到：' + '、'.join(f'`[{a},{b}]`' for a, b in S['res'])) if S.get('res') else '', size=24),
    ],
    watch=[('start_pos', 'start_pos', 'blue'), ('index', 'index', 'pink'), ('char', 'char', 'cyan'), ('res', 'res', 'green')],
    skip=['self.childs = {}', 'self.final = False'],
    captions={
        'root = Node()': '建空 trie 的根节点 `root`',
        'for word in words': '把单词 `{word}` 插入 trie',
        'now = root': '每次都从根出发',
        14: lambda S, B, r: (f"`'{S.char}'` 不在当前节点的孩子里 → 要新建" if S.char not in S.now.childs
                                                        else f"`'{S.char}'` 已有 → 直接往下走"),
        'now.childs[char] = node': '新建节点，挂到 `{char}` 这条边上',
        'now = now.childs[char]': '`now` 走到 `{char}` 对应的孩子',
        'now.final = True': '单词 `{word}` 结束：给这个节点打上 ==final== 标记',
        'res = []': '词表建好了；开始枚举 `text` 的每个起点',
        'for start_pos in range': '枚举起点 `start_pos = {start_pos}`',
        'for index, char in enumerate': lambda S, B, r: (f"从起点往后看第 `{S.index}` 个字符 `{S.char}`" if S.get('index') != B.get('index') or S.get('char') != B.get('char') else '这个起点的字符看完了'),
        25: lambda S, B, r: (f"`'{S.char}'` 不在 trie 的孩子里 → 没有更长的单词，==break=="
                                                        if S.char not in S.now.childs else f"`'{S.char}'` 在 trie 里 → 继续匹配"),
        'break': '以 `start_pos = {start_pos}` 起点的匹配到此为止，换下一个起点',
        'if now.final': lambda S, B, r: ('`now.final` 为真 → 走到的路径正好是一个单词' if S.now.final
                                          else '`now.final` 为假 → 只是某个单词的前缀，继续'),
        'res.append': '记录区间 `[{start_pos}, {start_pos + index}]`，当前 `res = {res}`',
        'return res': '全部起点枚举完，返回 `{res}`',
    },
    cards=dict(
        one_liner='先把词表建成 trie，再枚举每个起点沿 trie 往下走',
        complexity='时间 `O(Σ|word| + n·L)`，空间 `O(Σ|word|)`',
        problem=['给字符串 `text` 和单词列表 `words`，找出所有 `[i, j]`，使 `text[i..j]` 在 `words` 里',
                 '结果按 `i`、再按 `j` 排序',
                 '本视频：`text = "ababa"`，`words = ["aba", "ab"]` → `[[0,1],[0,2],[2,3],[2,4]]`'],
        quote='我在这里先通过words建立起trie树，然后枚举text中的所有位置作为单词的起点start_pos，接下来通过trie树判断以start_pos为起点的所有子串是否出现在words中。',
        quote_src='—— yiduobo 题解原文',
        idea=['trie 节点除了 `childs`，还要一个 ==final== 标记：这里是否是某个单词的结尾',
              '对每个起点沿 trie 往下走，走不通就 break，走到 `final` 就记一个区间',
              '起点从小到大、同起点下 `index` 从小到大 → 结果天然有序'],
        summary=['时间约 `O(Σ|word| + n·L)`，`L` 为最长单词长度；空间 `O(Σ|word|)`',
                 '易错：`final` 节点不代表要停，`aba` 路过 `ab` 时还要继续走',
                 '易错：区间终点是 `start_pos + index`（闭区间），不是 `+ 1`',
                 '原文本就能在 Python 3 运行，代码无改动'],
    ),
)
