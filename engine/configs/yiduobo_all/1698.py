def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    root = S.get('root')
    now = S.get('now')
    idx = S.get('index')
    cv.text((x0 + 18, y0 + 4), f"s = \"{s}\"；当前起点 index = {idx if idx is not None else '-'}；不同子串数 res = {S.get('res', 0)}", 24, T['muted'], bold=True)
    if root is None:
        return
    # 起点后缀：已走过的字符标绿
    if idx is not None:
        for k, ch in enumerate(s):
            X = x0 + 24 + k * 54
            on = k >= idx
            c = T['panel2'] if not on else T['yellow']
            if on and 'char' in S and now is not None:
                pass
            cv.rect((X, y0 + 44, X + 48, y0 + 92), fill=c, r=8)
            cv.text((X + 24, y0 + 68), ch, 28, T['bg'] if on else T['dim'], anchor='mm', bold=True, mono=True)
        cv.text((x0 + 24 + len(s) * 54 + 10, y0 + 68), '黄 = 以 index 为起点的后缀', 20, T['dim'], anchor='lm')
    pos, cnt = {}, [0]

    def lay(nd, dep):
        ch = list(nd.childs.items())
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
    top, R = y0 + 150, 24
    sp = min(130, (x1 - x0 - 80) / n)
    dy = min(90, (y1 - top - 50) / max(1, D))

    def P(nd):
        x, dep = pos[id(nd)]
        return x0 + (x1 - x0) / 2 + (x - (n - 1) / 2) * sp, top + dep * dy

    def edges(nd):
        X, Y = P(nd)
        for c, ch in nd.childs.items():
            X2, Y2 = P(ch)
            cv.line([(X, Y), (X2, Y2)], T['border'], 3)
            mx, my = (X + X2) / 2, (Y + Y2) / 2
            cv.rect((mx - 15, my - 15, mx + 15, my + 15), fill=T['panel'], outline=T['border'], r=6)
            cv.text((mx, my), c, 22, T['code'], anchor='mm', mono=True, bold=True)
            edges(ch)

    def nodes(nd):
        X, Y = P(nd)
        hot = nd is now
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['green'] if nd is not root else T['panel2'],
                     outline=T['yellow'] if hot else T['border'], width=5 if hot else 2)
        if hot:
            cv.text((X + R + 6, Y), 'now', 20, T['yellow'], anchor='lm', bold=True)
        for ch in nd.childs.values():
            nodes(ch)
    edges(root)
    nodes(root)
    rx, ry = P(root)
    cv.text((rx - R - 8, ry), 'root', 20, T['muted'], anchor='rm')
    cv.text((x1 - 20, y1 - 16), '每个绿色节点 = 一个不同的子串', 19, T['dim'], anchor='rb')


def _depth(S):
    def f(nd, d):
        if nd is S['now']:
            return d
        for c in nd.childs.values():
            r = f(c, d + 1)
            if r is not None:
                return r
    return (f(S['root'], 0) or 0) + 1


CONFIG = dict(
    num=1698, title='字符串的不同子字符串个数', difficulty='Medium', category='字符串',
    author='yiduobo', technique='Trie 插入所有后缀',
    tags=['灵神题单', '字符串'],
    code='''
class TreeNode(object):

    def __init__(self):
        self.childs = {}

class Solution(object):
    def countDistinct(self, s):

        res = 0
        root = TreeNode()

        for index in range(len(s)):
            now = root
            for char in s[index:]:
                if char not in now.childs:
                    res += 1
                    tmp = TreeNode()
                    now.childs[char] = tmp
                
                now = now.childs[char]
        
        return res
''',
    call='Solution().countDistinct("abab")',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'pink'), ('res', 'res', 'green')],
    captions={
        'self.childs = {}': '`childs`：字典，字符 → 子节点',
        'res = 0': '`res` 统计不同子串个数 = Trie 里新建节点的个数',
        'root = TreeNode()': '建一个空的 Trie 根节点（不对应任何子串）',
        'for index in range': lambda S, B, r: (f"枚举后缀起点 `index = {S.index}`：后缀 `\"{S.s[S.index:]}\"`" if S.get('index') != B.get('index') or 'index' not in B else '所有后缀都插完了'),
        'now = root': '每个后缀都从 `root` 出发往下走',
        'for char in s[index:]': lambda S, B, r: '这个后缀的字符都走完了，换下一个起点' if S.index + _depth(S) > len(S.s) else f"沿后缀取字符 `char = '{S.char}'`，对应子串 `\"{S.s[S.index:S.index + _depth(S)]}\"`" if 'char' in S else '后缀走完',
        'if char not in now.childs': lambda S, B, r: (
            f"`'{S.char}'` 不在 `now.childs` 里 → 这条路没走过 → ==新的不同子串==" if S.char not in S.now.childs
            else f"`'{S.char}'` 已在 `now.childs` 里 → 这个子串以前见过，不计数"),
        'res += 1': '新节点 = 新的不同子串：`res` → {res}',
        'tmp = TreeNode()': '新建节点',
        'now.childs[char] = tmp': '把新节点挂到 `now` 的 `{char!r}` 边上',
        'now = ': '`now` 沿 `{char!r}` 边下移，继续匹配后缀的下一个字符',
        'return res': '所有后缀都插入完，`res = {res}` 个不同子串',
    },
    skip=['tmp = TreeNode()', 'self.childs = {}'],
    max_steps=90,
    cards=dict(
        one_liner='把每个后缀插进 Trie，每多一个新节点就多一个不同子串',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`（后缀数组可做到 `O(n)`）',
        problem=['给字符串 `s`，返回它的==不同子字符串==的个数',
                 '示例：`"aabbaba"` → `21`',
                 '本视频：`"abab"` → `7`（a, b, ab, ba, aba, bab, abab）'],
        quote='字符串中的每个子串都是其某个后缀字符串的前缀……将以当前字符为起点的所有子串加入到trie树中，在这个过程中每新产生一个节点说明就多出一种不同的子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个子串 = 某个后缀的前缀；把后缀插进 Trie，路径上的节点 = 前缀',
              '节点是新建的 → 这个前缀（子串）此前没出现过 → `res += 1`',
              '作者说王道做法是后缀数组 `O(n)`，这里偷懒用 `O(n^2)` 暴力'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '计数的是 ==新建节点数==，不是单词数',
                 '空串不算子串；根节点不计数',
                 '更优：后缀数组（总子串数减去高度数组之和）或后缀自动机',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行；类名 `TreeNode` 是作者自己定义的 Trie 节点'],
    ),
)
