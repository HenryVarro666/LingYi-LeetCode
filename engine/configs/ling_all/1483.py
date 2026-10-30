def _layout_tree(ch, root):
    pos, cnt = {}, [0]

    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            x = cnt[0]
            cnt[0] += 1
        else:
            xs = [go(v, d + 1) for v in kids]
            x = (xs[0] + xs[-1]) / 2
        pos[u] = (x, d)
        return x
    go(root, 0)
    return pos, cnt[0]


def _tree_view(ch, root, colors, title, tags=None, wt=None, lab=None):
    """ch: {父: [子...]}；colors(S) -> {节点: 颜色名}；tags(S) -> {节点: 小字}；wt: {子: 边权}"""
    pos, W = _layout_tree(ch, root)
    D = max(d for _, d in pos.values()) + 1

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        cell = min(120, (x1 - x0 - 60) / max(W, 1))
        rowh = min(110, (y1 - y0 - 165) / max(D - 1, 1))
        sx = x0 + 30 + ((x1 - x0 - 60) - cell * W) / 2
        r = min(28, cell * 0.36, rowh * 0.42)
        P = {u: (sx + (x + 0.5) * cell, y0 + 80 + d * rowh) for u, (x, d) in pos.items()}
        for u, kids in ch.items():
            for v in kids:
                cv.line([P[u], P[v]], T['border'], 3)
                if wt:
                    left = P[v][0] <= P[u][0] + 1
                    cv.text(((P[u][0] + P[v][0]) / 2 + (-10 if left else 10), (P[u][1] + P[v][1]) / 2 - 6), wt[v], 22, T['orange'],
                            anchor='rm' if left else 'lm', bold=True)
        cm = colors(S) or {}
        tg = (tags(S) if tags else None) or {}
        for u, (X, Y) in P.items():
            c = cm.get(u)
            cv.rect((X - r, Y - r, X + r, Y + r), fill=T[c] if c else T['panel2'], outline=T['border'], width=2, r=r)
            cv.text((X, Y), lab(u) if lab else u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
            if u in tg:
                cv.text((X + r + 6, Y + r * 0.5), tg[u], 20, T['muted'], anchor='lm', bold=True)
    return dict(type='custom', draw=draw, h=0)
PARENT = [-1, 0, 0, 1, 3, 4, 2]
CH = {}
for _i, _p in enumerate(PARENT):
    if _p != -1:
        CH.setdefault(_p, []).append(_i)


def _colors(S):
    if 'k' in S and S.get('node') is not None and S['node'] >= 0:
        return {S['node']: 'pink'}
    if 'x' in S and 'p' in S and S.get('p') is not None and S['p'] != -1 and S.get('_line') in (7, 8):
        return {S['x']: 'yellow', S['p']: 'green'}
    if 'x' in S and 'n' in S and S['x'] < len(PARENT):
        return {S['x']: 'yellow'}
    return {}


def _pa(S):
    return S['pa'] if 'pa' in S else S.get('self.pa')


def _cell(S, r, c, v):
    if 'k' in S:
        if S.get('node') == r and S.get('i') == c:
            return 'pink'
        return None
    x, i, p = S.get('x'), S.get('i'), S.get('p')
    if x is None or i is None or 'n' not in S:
        return None
    if (r, c) == (x, i):
        return 'blue'
    if S.get('_line') in (7, 8) and p not in (None, -1) and (r, c) == (p, i):
        return 'green'
    if (r, c) == (x, i + 1):
        return 'yellow'
    return None


def _formula(S):
    if 'k' in S:
        k = S['k']
        i = S.get('i')
        if i is None:
            return f'`k = {k}` 的二进制是 =={k:b}==：每个 1 对应一次上跳'
        return f'`k = {k}` = `{k:b}`₂：第 `{i}` 位 = =={k >> i & 1}==，为 1 就跳 `2^{i}` = {2 ** i} 步'
    return '`pa[x][i]` = 节点 `x` 往上第 `2^i` 个祖先，`-1` 表示不存在'


CONFIG = dict(
    num=1483, title='树节点的第 K 个祖先', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='倍增（预处理 2^i 级祖先）',
    tags=['链表树与回溯', '难度分 2115'],
    code='''
class TreeAncestor:
    def __init__(self, n: int, parent: List[int]):
        m = n.bit_length() - 1
        pa = [[p] + [-1] * m for p in parent]
        for i in range(m):
            for x in range(n):
                if (p := pa[x][i]) != -1:
                    pa[x][i + 1] = pa[p][i]
        self.pa = pa

    def getKthAncestor(self, node: int, k: int) -> int:
        for i in range(k.bit_length()):
            if k >> i & 1:  # k 的二进制从低到高第 i 位是 1
                node = self.pa[node][i]
                if node < 0:
                    break
        return node

    # 另一种写法，不断去掉 k 的最低位的 1
    def getKthAncestor2(self, node: int, k: int) -> int:
        while k and node != -1:
            lb = k & -k
            node = self.pa[node][lb.bit_length() - 1]
            k ^= lb
        return node
''',
    call='''t = TreeAncestor(7, [-1, 0, 0, 1, 3, 4, 2])
[t.getKthAncestor(5, 3), t.getKthAncestor(5, 4), t.getKthAncestor(6, 3)]''',
    expect=[1, 0, -1],
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(_tree_view(CH, 0, _colors, '树（粉 = 当前跳到的节点，黄 = 正在算 pa[x][i+1]，绿 = 它的 2^i 级祖先）'), h=360),
        dict(type='table', var=_pa, label='pa[x][i]：行 = 节点 x，列 = i（第 2^i 个祖先）', rows=list(range(7)), cols=[0, 1, 2],
             color=_cell, cell=64, h=400),
    ],
    max_steps=56,
    watch=['n', 'm', 'node', 'k', 'i', ('p', 'p', 'green')],
    captions={
        'm = n.bit_length()': '`n = {n}`，至多需要 2^{m} 级：`m = n.bit_length() - 1 = {m}`',
        'pa = [[p] + [-1] * m': '第 0 列是父节点（`-1` 为根），其余先填 `-1`',
        'for i in range(m)': '先枚举 `i`、再枚举 `x`：算完所有 2^i 级，才能算 2^(i+1) 级',
        'for x in range(n)': '处理节点 `x = {x}`',
        'if (p := pa[x][i]) != -1': lambda S, B, ret: (f'`pa[{S.x}][{S.i}] = {S.p}`：存在 → 可以继续往上拼' if S.p != -1
                                                      else f'`pa[{S.x}][{S.i}] = -1`：2^{S.i} 级祖先已不存在，下一列也是 `-1`'),
        'pa[x][i + 1] = pa[p][i]': '2^i 级祖先 `{p}` 再跳 2^i 步：`pa[{x}][{i + 1}]` = `pa[{p}][{i}]` = =={pa[x][i + 1]}==',
        'self.pa = pa': '预处理完成，之后每次询问只看 `k` 的二进制',
        'for i in range(k.bit_length())': lambda S, B, ret: f'`k = {S.k}` 的二进制有 {S.k.bit_length()} 位，从低到高逐位看 → `i = {S.i}`' if 'i' in S else '开始扫描 `k` 的二进制位',
        'if k >> i & 1': lambda S, B, ret: (f'第 {S.i} 位是 1 → 要往上跳 `2^{S.i}` = {2 ** S.i} 步' if S.k >> S.i & 1
                                            else f'第 {S.i} 位是 0 → 这一档不用跳'),
        'node = self.pa[node][i]': '查表一步到位：`pa[·][{i}]` → 节点 ==`{node}`==',
        'if node < 0': lambda S, B, ret: ('`node = -1`：祖先不够 `k` 层，提前结束' if S.node < 0 else '`node` 还在树里，继续看下一位'),
        'break': '跳出：答案是 `-1`',
        'return node': '第 `k` 个祖先 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='k 拆成若干个 2 的幂，每一档查表跳一步',
        complexity='预处理 `O(n log n)`，每次询问 `O(log k)`；空间 `O(n log n)`',
        problem=['树按 `parent` 数组给出，根是 `0`',
                 '`getKthAncestor(node, k)`：返回 `node` 往上第 `k` 个祖先，不存在返回 `-1`',
                 '本视频：`parent = [-1,0,0,1,3,4,2]`，查 `(5,3)`、`(5,4)`、`(6,3)`'],
        quote='预处理出每个节点的第 2^i 个祖先节点，即第 1,2,4,8,… 个祖先节点。由于任意 k 可以分解为若干不同的 2 的幂（例如 13=8+4+1），所以只需要预处理出这些 2^i 祖先节点，就可以快速地到达任意第 k 个祖先节点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pa[x][i+1] = pa[pa[x][i]][i]`：2^i 步再走 2^i 步 = 2^(i+1) 步',
              '先枚举 `i`、再枚举 `x`，保证用到的上一列都已算好',
              '查询：看 `k` 的每个二进制 1，上跳对应的 2^i 步；掉出树外就是 `-1`'],
        summary=['预处理 `O(n log n)`，询问 `O(log k)`',
                 '易错：外层循环是 `i`，内层是 `x`；`pa[x][i]` 为 `-1` 时不能再往下查',
                 '题解还给了 `getKthAncestor2`：不断去掉 `k` 的最低位 1，视频只演示第一种',
                 '同一套 `pa` 表可以拿来求 LCA（见 3553、3559）'],
    ),
)
