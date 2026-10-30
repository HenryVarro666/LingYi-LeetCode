PARENTS = [-1, 0, 0, 1, 2, 2]
DONE = {}
_G = [[] for _ in PARENTS]
for _i in range(1, len(PARENTS)):
    _G[PARENTS[_i]].append(_i)


def _pos(box):
    x0, y0, x1, y1 = box
    n = len(PARENTS)
    depth, xs = {}, {}
    cnt = [0]

    def go(u, d):
        depth[u] = d
        if not _G[u]:
            xs[u] = cnt[0]
            cnt[0] += 1
        else:
            for v in _G[u]:
                go(v, d + 1)
            xs[u] = (xs[_G[u][0]] + xs[_G[u][-1]]) / 2
    go(0, 0)
    md = max(depth.values()) + 1
    sp = min(170, (x1 - x0 - 60) / max(1, cnt[0]))
    dy = min(120, (y1 - y0 - 90) / max(1, md))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * cnt[0]) / 2 + sp / 2
    return {u: (sx + xs[u] * sp, y0 + 70 + depth[u] * dy) for u in range(n)}


def _res(u):
    return '0' + ''.join(sorted(_res(v) for v in _G[u])) + '1'


_PRE = []


def _go(u):
    _PRE.append(u)
    for v in _G[u]:
        _go(v)


_go(0)


def _desc(u):
    out = []
    for v in _G[u]:
        out += [v] + _desc(v)
    return out


def _done(S):
    I = S.get('_inner') or {}
    x = I.get('x')
    if x is None:
        return {}
    anc, p = set(), PARENTS[x]
    while p >= 0:
        anc.add(p)
        p = PARENTS[p]
    d = {u for u in _PRE[:_PRE.index(x)] if u not in anc}
    if 'a' in I:
        d |= set(_desc(x))
    if S.get('_line') == 10:
        d.add(x)
    return {u: _res(u) for u in d}


def track(fn, record=False):
    def cap(S, B, ret):
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'parents 建出的树（蓝 = 正在 dfs 的节点，绿 = 已返回，旁边是返回的字符串）', 22, T['muted'], bold=True)
    pos = _pos(box)
    DN = _done(S) if 'g' in S else {}
    cur = S['_inner'].get('x') if '_inner' in S else None
    if 'g' not in S:
        cur = None
    for u in range(len(PARENTS)):
        for v in _G[u]:
            if 'g' in S and v in S['g'][u]:
                cv.line([pos[u], pos[v]], T['border'], 3)
    rad = 24
    for u in range(len(PARENTS)):
        if 'g' not in S:
            break
        X, Y = pos[u]
        fill = T['panel']
        out = T['border']
        if u in DN:
            out = T['green']
        if u == cur:
            out = T['blue']
        cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=out, width=4, r=rad)
        cv.text((X, Y), u, 26, T['text'], anchor='mm', bold=True)
        if u in DN:
            s = DN[u]
            w = cv.tlen(s, 20, mono=True) + 16
            cv.rect((X - w / 2, Y + rad + 6, X + w / 2, Y + rad + 34), fill=T['panel'], outline=T['green'], width=2, r=8)
            cv.text((X, Y + rad + 20), s, 20, T['green'], anchor='mm', mono=True)


def _sorted_cap(S, B, ret):
    I = S['_inner']
    x = I.get('x')
    if 'a' not in I:
        kids = _G[x]
        return f'进入 `dfs({x})`：' + (f'节点 {x} 有孩子 {kids}，先递归处理它们' if kids else f'节点 {x} 是叶子，没有孩子')
    a = I['a']
    if not a:
        return f'`dfs({x})`：叶子，没有子树结果，`a = []`'
    return f'`dfs({x})` 收齐孩子的结果后排序：`a = {a}` → ==小的排前面==，拼出来字典序最小'


def _ret_cap(S, B, ret):
    x = S['_inner'].get('x')
    return f'`dfs({x})` 返回 `"0" + 子树结果 + "1"` = `{ret}`：进入记 0，回退记 1'


CONFIG = dict(
    num='LCP 80', title='生物进化录', difficulty='Hard', category='二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 子树字符串排序拼接', tags=[],
    code='''
class Solution:
    def evolutionaryRecord(self, parents: List[int]) -> str:
        n = len(parents)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[parents[i]].append(i)  # 建树

        def dfs(x: int) -> str:
            a = sorted(dfs(y) for y in g[x])
            return "0" + ''.join(a) + "1"
        return dfs(0)[1:].rstrip('1')  # 去掉根节点以及返回根节点的路径
''',
    call=f'Solution().evolutionaryRecord({PARENTS})',
    expect='00101100',
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=210),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('a', lambda S: S['_inner'].get('a'), 'cyan')],
    skip=['n = len', 'g = [[]', 'for i in range', 'g[parents'],
    captions={
        'g[parents[i]]': '建树：`{i}` 挂在父节点 `{parents[i]}` 下',
        'a = sorted': track(_sorted_cap),
        'return "0"': track(_ret_cap, record=True),
        'return dfs(0)': '从根 `0` 开始 `dfs`；回来后去掉开头给根的 `0`、末尾回退的 `1`（指针可停在任意节点）',
    },
    cards=dict(
        result='`dfs(0)` = `000101100111`，去掉开头的 `0` 和末尾的 `1` → ==00101100==',
        one_liner='每棵子树记成 0…1 字符串，排序后拼接，字典序最小',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['`parents[i]` 是节点 `i` 的父节点，记 `0` 表示新建子节点并进入，记 `1` 表示回退到父节点',
                 '求能复刻这棵树、字典序最小的 `01` 字符串，指针可停在任意节点',
                 '示例：`[-1,0,0,1,2,2]` → `"00101100"`'],
        quote='把所有子树的结果排序，然后拼接起来，在开头加上 0，末尾加上 1，然后返回。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子树的字典序最小，整棵树才可能最小 → ==自底向上递归==',
              '每个子树字符串 `0…1` 自成一块，按字符串排序再拼起来',
              '最后去掉根的 `0` 和结尾所有的 `1`，因为不用回到根；排序不影响这一步的正确性'],
        summary=['时间 `O(n²)`（字符串拼接是瓶颈），空间 `O(n)`',
                 '`dfs(0)[1:]` 去掉根节点的 `0`，`rstrip(\'1\')` 去掉结尾回退的 `1`',
                 '易错：别忘了「指针可以停在任意节点」，所以末尾的 `1` 必须去掉',
                 '去掉末尾 1 后字典序仍最小：各种顺序的 0、1 总数相同，较小的排列去掉相同数量的结尾后仍是最小',
                 '同类题：761. 特殊的二进制序列（同一个排序拼接技巧）'],
    ),
)
