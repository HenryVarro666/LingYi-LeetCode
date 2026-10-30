N0 = 4
EDGES0 = [[0, 2], [0, 3], [3, 1]]
LABEL0 = 'bbac'
POS = [(0.4, 0.62), (0.9, 0.3), (0.12, 0.3), (0.65, 0.62)]


def _bits(m):
    return [i for i in range(N0) if m >> i & 1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '图（字母 = label；蓝 = 路径左端，粉 = 右端，绿 = 路径上的点，黄 = 要加入的新端点）', 22, T['muted'], bold=True)
    line = S.get('_line', 0)
    w_, h_ = x1 - x0, y1 - y0 - 50
    pts = [(x0 + px * w_, y0 + 60 + py * h_) for px, py in POS]
    live = line >= 25 and S.get('state') is not None
    state, left, right = S.get('state'), S.get('left'), S.get('right')
    nl = S.get('new_left') if line >= 26 else None
    nr = S.get('new_right') if line >= 29 else None
    for a, b in EDGES0:
        hot = live and ((a == left and b == nl) or (b == left and a == nl) or (a == right and b == nr) or (b == right and a == nr)) and line >= 30
        cv.line([pts[a], pts[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    for i, (px, py) in enumerate(pts):
        fill = T['panel2']
        if live:
            if state >> i & 1:
                fill = T['green']
            if i == left:
                fill = T['blue']
            if i == right and right != left:
                fill = T['pink']
            if i in (nl, nr) and line >= 30 and not (state >> i & 1):
                fill = T['yellow']
        r = 42
        cv.rect((px - r, py - r, px + r, py + r), fill=fill, r=r, outline=T['border'])
        cv.text((px, py - 4), LABEL0[i], 36, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((px, py + r + 12), f'节点 {i}', 18, T['dim'], anchor='mt')


def _formula(S):
    line = S.get('_line', 0)
    if line >= 25 and S.get('state') is not None and line <= 43:
        st, l, r = S['state'], S['left'], S['right']
        return f'当前路径：点集 {_bits(st)}，两端 `left={l}`（{LABEL0[l]}）、`right={r}`（{LABEL0[r]}），回文长度 `f = {S["f"][st][l][r]}`'
    if line >= 47:
        return f'`res = {S.get("res")}`'
    return f'`f[state][left][right]` = 点集为 state、两端是 left/right 的回文路径长度；已记 `res = {S.get("res", 0)}`'


def _cap_ok(S, B, ret):
    a, b = S.new_left, S.new_right
    if S.label[a] != S.label[b]:
        return f'`label[{a}] = {S.label[a]}` ≠ `label[{b}] = {S.label[b]}` → 两端字母不同，不能同时加'
    return f'`label[{a}] = label[{b}] = {S.label[a]}` ==相同== → 左右各加一个点，回文长度 +2'


CONFIG = dict(
    num=3615, title='图中的最长回文路径', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='两端扩展的状压 BFS',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2463'],
    code='''
class Solution(object):
    def maxLen(self, n, edges, label):
        
        g = [set() for _ in range(n)]
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        max_state = 1 << n
        f = [[[None] * n for _ in range(n)] for _ in range(max_state)]
        
        q = []
        res = 0
        for left in range(n):
            q.append((1 << left, left, left))
            f[1 << left][left][left] = 1
            for right in range(left + 1, n):
                if label[left] == label[right] and left in g[right]:
                    q.append(((1 << left) | (1 << right), left, right))
                    f[(1 << left) | (1 << right)][left][right] = 2

        head, tail = 0, len(q)
        while head < tail:
            for state, left, right in q[head : tail]:
                res = max(res, f[state][left][right])
                for new_left in g[left]:
                    if state & (1 << new_left) == 1 << new_left:
                        continue
                    for new_right in g[right]:
                        if new_left == new_right:
                            continue
                        if state & (1 << new_right) == 1 << new_right:
                            continue
                        if label[new_left] != label[new_right]:
                            continue
                        
                        new_state = state | (1 << new_left) | (1 << new_right)
                        ma, mi = new_left, new_right
                        if ma < mi:
                            ma, mi = mi, ma
                        if f[new_state][mi][ma] is None:
                            f[new_state][mi][ma] = f[state][left][right] + 2
                            q.append((new_state, mi, ma))
        
            head, tail = tail, len(q)

        return res
''',
    call=f'Solution().maxLen({N0}, {EDGES0}, {LABEL0!r})',
    expect=3,
    skip=['g = [set()', 'g[x].add', 'g[y].add', 'for x, y in edges', 'max_state = 1', 'f = [[[None]', 'q = []', 'for right in range', 'continue', 'ma, mi = new', 'if ma < mi', 'ma, mi = mi', 'res = 0', 'for left in range(n)', 'for new_left in g[left]', 'for new_right in g[right]', 'for state, left, right in'],
    max_steps=60,
    views=[
        dict(type='text', fn=_formula, size=24, h=80),
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=lambda S: f'队列 `q` 里共 {len(S["q"])} 个状态（点集, left, right）：' + '，'.join(f'({"".join(map(str, _bits(a)))}|{b},{c})' for a, b, c in S['q'][-6:]) if 'q' in S else '', size=22, h=90),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('new_left', 'new_left', 'yellow'), ('new_right', 'new_right', 'yellow'), ('res', 'res', 'green')],
    captions={
        'q.append((1 << left, left, left))': '奇回文中心：单个点 `{left}` 本身就是长度 1 的回文，入队',
        'f[1 << left][left][left] = 1': '`f[{(1 << left)}][{left}][{left}] = 1`',
        'if label[left] == label[right] and left in g[right]': lambda S, B, r: (f'`({S.left},{S.right})` 相邻且字母相同 → 可以当偶回文中心' if (S.label[S.left] == S.label[S.right] and S.left in S.g[S.right])
                                                                                else f'`({S.left},{S.right})` 不是「相邻且字母相同」，不能当偶回文中心'),
        'f[(1 << left) | (1 << right)][left][right] = 2': '偶回文中心：长度 2',
        'head, tail = 0, len(q)': '初始状态都在队列里（`{len(q)}` 个），按层 BFS，每层从两端各扩一个点',
        'while head < tail': lambda S, B, r: (f'这一层有 `{S.tail - S.head}` 个状态要扩展' if S.head < S.tail else '队列空了，全部扩展完'),
        'res = max(res, f[state]': lambda S, B, r: f'状态 点集={_bits(S.state)}，两端 `{S.left}`/`{S.right}`，长度 `{S.f[S.state][S.left][S.right]}`；`res` → =={S.res}==',
        'if state & (1 << new_left)': lambda S, B, r: (f'左端 `{S.left}` 的邻居 `new_left = {S.new_left}`：已在路径里 → 跳过' if S.state >> S.new_left & 1 else f'左端的邻居 `new_left = {S.new_left}` 还没走过'),
        'if new_left == new_right': lambda S, B, r: ('两端会走到同一个点 → 不行' if S.new_left == S.new_right else f'`new_right = {S.new_right}` 与 `new_left` 不同，继续'),
        'if state & (1 << new_right)': lambda S, B, r: (f'`new_right = {S.new_right}` 已在路径里 → 跳过' if S.state >> S.new_right & 1 else f'`new_right = {S.new_right}` 没走过'),
        'if label[new_left] != label[new_right]': _cap_ok,
        'new_state = state': '新状态：点集加入 `{new_left}` 和 `{new_right}` → `{new_state:0{n}b}`；端点按（小, 大）存成 `mi, ma`，省掉一半重复',
        'if f[new_state][mi][ma] is None': lambda S, B, r: ('这个状态还没访问过 → 记录并入队' if S.f[S.new_state][S.mi][S.ma] is None else '已经访问过，不重复入队'),
        'f[new_state][mi][ma] = f[state]': '`f[新状态][{mi}][{ma}] = {f[state][left][right]} + 2` = =={f[state][left][right] + 2}==：两端各加一个点，回文长度 +2',
        'q.append((new_state, mi, ma))': '新状态入队，下一层继续向外扩',
        'head, tail = tail': '这一层处理完，下一层是新加入队列的状态',
        'return res': '`f` 里的最大值 = =={ret}==',
    },
    cards=dict(
        one_liner='以回文中心为起点，两端同时扩，BFS 记长度',
        complexity='时间 `O(n^4 · 2^n)`，空间 `O(n^2 · 2^n)`',
        problem=['无向图 `n ≤ 14` 个点，每个点带一个字母，每个点最多走一次',
                 '找一条路径，使路径上的字母拼成==最长的回文串==，返回长度',
                 '示例：`n=4, edges=[[0,2],[0,3],[3,1]], label="bbac"` → `3`（`0→3→1` = `"bcb"`）'],
        quote='状态设计应该是 f[state][left][right] 表示选择 state 中的节点，且形成的路径中两个端点分别是 left 和 right 时构成的回文串长度。其中 left 是编号较小的节点，right 是编号较大的节点，这样做的理由是可以省去一半不必要的重复状态。',
        quote_src='—— yiduobo 题解',
        idea=['回文要记住==路径两端==是谁，所以状态是 `(点集, left, right)`',
              '初始化：每个点（长度 1）和每对相邻同字母点（长度 2）当作中心，进队列',
              'BFS 扩展：两端各接一个没走过、字母相同、互不相同的邻居，长度 +2'],
        summary=['时间 `O(n^4 2^n)`，空间 `O(n^2 2^n)`',
                 '易错：`new_left ≠ new_right`；两个新点都不能已在 `state` 里；存储时把编号小的放前面去重',
                 '`f[...]` 为 None 表示没访问过，所以每个状态只入队一次',
                 '与灵神的区别：这里是 BFS 往外推，灵神是 `@cache` 记忆化 + 完全图/理论最大值剪枝'],
    ),
)
