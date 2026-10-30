import math


def _tlayout(ch, node, depth, acc, nxt):
    kids = [c for c in ch(node) if c is not None]
    if not kids:
        acc[id(node)] = (nxt[0], depth, node)
        nxt[0] += 1
        return
    for c in kids:
        _tlayout(ch, c, depth + 1, acc, nxt)
    xs = [acc[id(c)][0] for c in kids]
    acc[id(node)] = (sum(xs) / len(xs), depth, node)


def _cur_tree_node(S):
    now = S.get('now')
    if isinstance(now, int):
        return now
    v = S.get('v')
    s = S.get('s')
    if isinstance(v, int) and s:
        for i, x in enumerate(s):
            if x == v:
                return i
    return None


def _draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g, s = S.get('g'), S.get('s')
    cv.text((x0 + 18, y0 + 4), '树：节点里是编号，旁边 `值 → 子树和 s`（黄 = 当前处理的节点）'.replace('`', ''), 22, T['muted'], bold=True)
    if not g or not S.get('values'):
        return
    vals = S['values']
    kids = {}
    seen = {0}
    order = [0]
    for u in order:
        kids[u] = [w for w in g[u] if w not in seen]
        for w in kids[u]:
            seen.add(w)
            order.append(w)
    acc, nxt = {}, [0]

    def lay(u, d):
        if not kids[u]:
            acc[u] = (nxt[0], d)
            nxt[0] += 1
            return
        for w in kids[u]:
            lay(w, d + 1)
        acc[u] = (sum(acc[w][0] for w in kids[u]) / len(kids[u]), d)
    lay(0, 0)
    leaves = nxt[0]
    maxd = max(d for _, d in acc.values())
    top, bot = y0 + 70, y1 - 40
    left, right = x0 + 110, x1 - 150
    pos = {u: ((left + right) / 2 if leaves == 1 else left + acc[u][0] * (right - left) / (leaves - 1),
               top + (acc[u][1] * (bot - top) / max(maxd, 1))) for u in acc}
    cur = _cur_tree_node(S)
    for u in acc:
        for w in kids[u]:
            cv.line([pos[u], pos[w]], T['border'], 4)
    for u, (px, py) in pos.items():
        hot = (u == cur)
        cv.rect((px - 28, py - 28, px + 28, py + 28), fill=T['yellow'] if hot else T['panel2'], outline=T['border'], r=28)
        cv.text((px, py), u, 28, T['bg'] if hot else T['text'], anchor='mm', bold=True)
        sv = s[u] if s else 0
        lab = f'{vals[u]}' + (f' → {sv}' if sv else '')
        cv.text((px + 36, py), lab, 24, T['green'] if sv else T['muted'], anchor='lm', bold=True, mono=True)


def _draw_trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'trie：存已经加入的子树和的二进制（边 = 0 / 1，黄 = 当前走到的节点）', 22, T['muted'], bold=True)
    trie = S.get('trie')
    if trie is None:
        return
    acc, nxt = {}, [0]
    _tlayout(lambda n: n.childs, trie, 0, acc, nxt)
    leaves = max(nxt[0], 1)
    maxd = max(d for _, d, _ in acc.values())
    LV = 3
    top, bot = y0 + 70, y1 - 30
    left, right = x0 + 150, x1 - 90
    pos = {}
    for k, (xu, d, nd) in acc.items():
        px = (left + right) / 2 if leaves == 1 else left + xu * (right - left) / (leaves - 1)
        pos[k] = (px, top + d * (bot - top) / LV)
    now = S.get('now')
    for k, (xu, d, nd) in acc.items():
        for b_, c in enumerate(nd.childs):
            if c is not None:
                p, q = pos[k], pos[id(c)]
                cv.line([p, q], T['dim'], 4)
                cv.text(((p[0] + q[0]) / 2 + (-14 if b_ == 0 else 14), (p[1] + q[1]) / 2), b_, 22,
                        T['cyan'] if b_ == 0 else T['orange'], anchor='mm', bold=True, mono=True)
    for k, (xu, d, nd) in acc.items():
        px, py = pos[k]
        hot = nd is now
        cv.rect((px - 14, py - 14, px + 14, py + 14), fill=T['yellow'] if hot else T['panel2'], outline=T['border'], r=14)
    for dep in range(LV + 1):
        yy = top + dep * (bot - top) / LV
        cv.text((x0 + 18, yy), '根' if dep == 0 else f'第 {LV - dep} 位', 22, T['dim'], anchor='lm')


def _info(S):
    v = S.get('v')
    if isinstance(v, int) and 'digit' in S and S.get('index') is not None and S['_line'] in range(9, 35):
        return f'`v = {v}` = ==' + format(v, '03b') + '==（二进制）' + (f'　`ma = {S["ma"]:b}`' if 'ma' in S and S['_line'] < 25 else '')
    return '每个子树和 `s[x]` 先查询（和 trie 里已有的数异或取最大），再加入 trie'


CONFIG = dict(
    num=2479, title='两个不重叠子树的最大异或值', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='子树和 + 01 Trie（后序先查再插）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Node(object):

    def __init__(self):
        self.childs = [None, None]

class Solution(object):
    def maxXor(self, n, edges, values):

        def check(v):
            ma = 0
            now = trie
            for index in range(2, -1, -1):
                digit = (v >> index) & 1
                target = 1 - digit
                if now.childs[target] is not None:
                    ma = ma + ma + 1
                    now = now.childs[target]
                elif now.childs[digit] is not None:
                    ma = ma + ma
                    now = now.childs[digit]
                else:
                    return 0

            return ma

        def add(v):
            now = trie
            for index in range(2, -1, -1):
                digit = (v >> index) & 1
                if now.childs[digit] is None:
                    tmp = Node()
                    now.childs[digit] = tmp
                
                now = now.childs[digit]

        def dfs(now, fa):
            s[now] = values[now]
            for next in g[now]:
                if next != fa:
                    s[now] += dfs(next, now)

            return s[now]

        def query(now, fa):
            global res
            res = max(res, check(s[now]))
            for next in g[now]:
                if next != fa:
                    query(next, now)
            
            add(s[now])

        trie = Node()

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        s = [0] * n
        dfs(0, None)

        global res
        res = 0
        query(0, None)

        return res
''',
    call='Solution().maxXor(3, [[0,1],[0,2]], [1,2,4])',
    expect=6,
    views=[
        dict(type='custom', draw=_draw_tree, h=230),
        dict(type='custom', draw=_draw_trie, h=320),
        dict(type='text', h=70, size=26, fn=_info),
    ],
    max_steps=150,
    watch=['now', 'v', 'ma'],
    skip=['self.childs', 'target = 1 - digit', 'tmp = Node()', 'for _ in range', 12, 28, 29, 34, 38, 47, 10, 'g[y].append', 'g[x].append', 64, 39, 48, 'for x, y in edges'],
    captions={
        'ma = 0': '`ma` 记这次查询已经凑出的异或结果（从高位往低位一位一位拼）',
        'now = trie': '从 trie 的根出发，`v = {v}`',
        'digit = (v >> index) & 1': '`v` 的第 `{index}` 位是 `digit = {digit}`；想异或出 1，就要找这一位是 `1 - digit = {1 - digit}` 的前缀',
        'if now.childs[target] is not None': lambda S, B, r: (
            f'trie 里有第 {B.index} 位为 `{1 - B.digit}` 的前缀 → 这一位能异或出 ==1==' if B.now.childs[1 - B.digit] is not None else f'trie 里没有第 {B.index} 位为 `{1 - B.digit}` 的前缀，这一位异或不出 1'),
        'ma = ma + ma + 1': '这一位异或出 1：`ma = {B.ma}×2 + 1 = {ma}`',
        'now = now.childs[target]': '沿着相反的那条边走：贪心让高位尽量为 1',
        'elif now.childs[digit] is not None': lambda S, B, r: ('只有同号这一侧有节点，这一位只能是 0' if B.now.childs[B.digit] is not None else '两侧都没有（trie 为空）'),
        'ma = ma + ma': '这一位异或出 0：`ma = {B.ma}×2 = {ma}`',
        'now = now.childs[digit]': '只好走同号的边',
        'return 0': 'trie 是空的，没有可配对的子树，返回 `0`',
        'return ma': '这次查询得到的最大异或值是 `{ret}`',
        'if now.childs[digit] is None': lambda S, B, r: (f'`v = {B.v}` 的第 {B.index} 位是 `{B.digit}`：这条边还没有 → 新建节点' if B.now.childs[B.digit] is None else f'第 {B.index} 位是 `{B.digit}` 的边已经有了，直接走'),
        'now.childs[digit] = tmp': '新建的节点挂到第 `{index}` 位的 `{digit}` 边上',
        's[now] = values[now]': '先令 `s[{now}]` = 自己的值 `{s[now]}`',
        'for next in g[now]': lambda S, B, r: (f'访问邻居 `{S.next}`' if S.get('next') is not None and B.get('next') != S.get('next') else '邻居都看完了'),
        's[now] += dfs(next, now)': '`{B.next}` 是 `{B.now}` 的孩子 → 递归求它的子树和，加到 `s[{B.now}]` 上',
        'return s[now]': '`s[{now}]` = 以 {now} 为根的子树点权和 `{ret}`',
        'res = max(res, check(s[now]))': lambda S, B, r: ('先查询：用 `s[{}]` 和 trie 里已有的子树和配对'.format(B.now) if r is None and S.get('res') is None else f'`res = max({B.res}, check(s[{B.now}]))` → `{S.res}`'),
        'if next != fa': lambda S, B, r: (f'`{B.next}` 不是父亲 → 是孩子，往下查询' if B.next != B.fa else f'`{B.next}` 是父亲，跳过'),
        'query(next, now)': '`{B.next}` 是孩子 → 先递归处理它的子树，再回来处理自己 `{B.now}`',
        'add(s[now])': '自己和所有孩子都查询完了，才把 `s[{now}] = {s[now]}` 加入 trie：这样后面的查询绝不会碰到自己的祖先或后代',
        'trie = Node()': 'trie 一开始是空的，只有根',
        'dfs(0, None)': '先 dfs 算出每个节点的子树和 `s`',
        'query(0, None)': '再做一遍后序遍历：先孩子，再自己，==先查后插==',
        'return res': '最大异或值是 `{res}`',
    },
    cards=dict(
        one_liner='后序遍历：每个子树先查询、再插入，保证不重叠',
        complexity='时间 `O(n log C)`，空间 `O(n log C)`',
        problem=['无向树，`n` 个节点，点权 `values`；选两个==不重叠==的子树，求它们点权和的最大异或值',
                 '没有两个子树时返回 `0`',
                 '本视频：`n=3`，`edges=[[0,1],[0,2]]`，`values=[1,2,4]` → `6`'],
        quote='先进行一次dfs，求解以每个节点为根节点的子树中的节点值之后，然后再采用类似后续遍历的处理方法，先递归求解子树并完成子树中的查询，然后完成当前节点的查询。查询完成后，再将当前节点值加入到trie树中。这样一来就可以保证不会出现重叠的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs` 先算出每个节点的子树和 `s[x]`',
              '最大异或问题用 01 trie：从高位往低位，尽量走和 `v` 相反的那条边',
              '`query` 里==后序==：先递归孩子，再查询自己、最后才 `add(s[now])`。trie 里永远只有已经处理完的、与当前不重叠的子树'],
        summary=['时间 `O(n log C)`，空间 `O(n log C)`',
                 '原文用 47 位（点权和可达 `5*10^14` 量级）。演示的数很小，把 `range(46, -1, -1)` 改成了 `range(2, -1, -1)`（3 位），逻辑完全不变',
                 '易错：必须先查询再插入，否则会和自己重叠；trie 为空时 `check` 返回 `0`',
                 '`global res` 在嵌套函数 `query` 里修改外层的结果'],
    ),
)
