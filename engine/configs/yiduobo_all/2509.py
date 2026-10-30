def _anc(a, b):
    pa, pb = [a], [b]
    x, y = a, b
    while x != y:
        if x > y:
            x //= 2
            pa.append(x)
        else:
            y //= 2
            pb.append(y)
    return pa, pb, x


def _getab(S):
    if 'x' not in S or 'res' not in S or 'queries' not in S:
        return None
    k = len(S['res']) - (1 if S.get('_line', 0) >= 10 else 0)
    k = min(max(k, 0), len(S['queries']) - 1)
    a, b = sorted(S['queries'][k])
    return a, b


def _draw(cv, S, B, box, T):
    ab = _getab(S)
    x0, y0, x1, y1 = box
    n = 3
    W = x1 - x0 - 60
    lv = lambda v: v.bit_length() - 1
    pos = {}
    for v in range(1, 2 ** n):
        L = lv(v)
        k = v - 2 ** L
        pos[v] = (x0 + 30 + (k + 0.5) / 2 ** L * W, y0 + 70 + L * 130)
    live = ab is not None
    pa = pb = []
    lca = None
    if live:
        pa, pb, lca = _anc(ab[0], ab[1])
    cyc = set(pa) | set(pb)
    cv.text((x0 + 18, y0 + 4), '完全二叉树（节点编号 = 二进制前缀；蓝 = a，粉 = b，黄 = 环，绿 = 拐弯点 LCA）', 20, T['muted'], bold=True)
    for v in range(2, 2 ** n):
        p = v // 2
        on = live and v in cyc and p in cyc
        cv.line([pos[v], pos[p]], T['yellow'] if on else T['border'], 6 if on else 2)
    if live:
        cv.arc_arrow(pos[ab[0]], pos[ab[1]], 90, T['orange'], 4)
    for v in range(1, 2 ** n):
        X, Y = pos[v]
        fill = T['panel2']
        tc = T['muted']
        if live and v in cyc:
            fill, tc = T['yellow'], T['bg']
        if live and v == lca:
            fill, tc = T['green'], T['bg']
        if live and v == ab[0]:
            fill, tc = T['blue'], T['bg']
        if live and v == ab[1]:
            fill, tc = T['pink'], T['bg']
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=fill, r=30, outline=T['border'])
        cv.text((X, Y), v, 30, tc, anchor='mm', bold=True)
        cv.text((X, Y + 44), format(v, 'b'), 18, T['dim'], anchor='mt', mono=True)


def _f(S):
    ln = S.get('_line')
    ab = _getab(S)
    if ab is None or 'y' not in S:
        return ''
    a, b = ab
    if ln in (9, 10):
        return f'层级差 = {len(bin(b))-2} − {len(bin(a))-2} = =={len(bin(b)) - len(bin(a))}==，再加新边的 1'
    if ln in (12, 14):
        return f'y 右移后 = `{S["y"]:b}`，和 x = `{S["x"]:b}`' + ('：相同，x 就是 lca' if S['x'] == S['y'] else '：不同，还要看异或')
    if ln in (15, 17):
        return f'`x^y` = `{S["x"] ^ S["y"]:b}`，去掉公共前缀 → lca = `{S["lca"]:b}`' if 'lca' in S else ''
    if ln == 18 and 'lca' in S:
        return f'x 到 lca 的层数 = {len(bin(S["x"])) - len(bin(S["lca"]))}，两侧各一份'
    return f'x=`{S["x"]:b}`，y=`{S["y"]:b}`'


CONFIG = dict(
    num=2509, title='查询树中环的长度', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='二进制前缀 = 最近公共祖先',
    tags=['位运算', '链表树与回溯', '难度分 1948'],
    code='''
class Solution(object):
    def cycleLengthQueries(self, n, queries):

        res = []
        for x, y in queries:
            if x > y:
                x, y = y, x
            
            len_diff = len(bin(y)) - len(bin(x))
            res.append(len_diff + 1)

            y >>= len_diff

            if x == y:
                lca = x
            else:
                lca = x >> (len(bin(x ^ y)) - 2)
            res[-1] += (len(bin(x)) - len(bin(lca))) * 2
        
        return res
''',
    call='Solution().cycleLengthQueries(3, [[5,3],[4,7],[2,3]])',
    expect=[4, 5, 3],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=_f, size=28, h=70),
    ],
    watch=['x', 'y', 'len_diff', 'lca', ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 存每个查询的环长',
        'for x, y in queries': lambda S, B, r: ('所有查询处理完，循环结束' if len(S.res) == len(S.queries) else f'取一个查询：在 `{S.x}` 和 `{S.y}` 之间加边'),
        'if x > y': lambda S, B, r: ('`x > y`：交换，保证 x 更浅（编号小）' if S.x > S.y else '`x < y`：y 的层级 ≥ x，不用换'),
        'len_diff =': '`len(bin)` 差 = 二进制位数差 = 层级差：`len_diff = {len_diff}`，y 要上移这么多层',
        'res.append': '先记下：y 上移 `{len_diff}` 层 + 新边 1 条 = `{res[-1]}`',
        'y >>= len_diff': '右移 = 取父节点，y 上移 `{len_diff}` 层：`y = {y}`，和 x 同层',
        'if x == y': lambda S, B, r: ('同层且相同：x 就是 lca，不用继续上移' if S.x == S.y else f'`{S.x} != {S.y}`：还要一起往上走'),
        'lca = x': lambda S, B, r: (f'`lca = x = {S.lca}`' if S.x == S.y else f'`x ^ y = {S.x ^ S.y:b}`：公共前缀变 0，剩 {len(bin(S.x ^ S.y)) - 2} 位要上移 → `lca = {S.lca}`'),
        'res[-1] +=': 'x 到 lca 差 `{len(bin(x)) - len(bin(lca))}` 层，y 也一样，加上两侧共 `{(len(bin(x)) - len(bin(lca))) * 2}` → 环长 =={res[-1]}=='
        ,
        'return res': '所有查询的环长：`{res}`',
    },
    cards=dict(
        one_liner='环 = 两条树链 + 新边，lca 就是二进制的公共前缀',
        complexity='时间 `O(m·n)`（`bin` 长度 `O(n)`），空间 `O(1)`',
        problem=['完全二叉树，`v` 的孩子是 `2v` 和 `2v+1`',
                 '给 `a`、`b` 加一条边，求环的长度，查完删边',
                 '示例：`n=3, [[5,3],[4,7],[2,3]]` → `[4,5,3]`'],
        quote='每个节点在树中的位置完全取决于其数值的二进制表示，而这些节点的祖先节点则恰好是二进制表示的某个前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['环 = 新边 + a 到 lca 的链 + b 到 lca 的链，所以只要知道 lca 的层级',
              '设 x<y，二进制位数 = 层级：y 右移 `len_diff` 位，就和 x 同层',
              '再异或：公共前缀变成 0，剩下的位数就是各自还要上跳的层数'],
        summary=['`len(bin(v))` 比二进制位数多 2（含 `0b`），所以做差时抵消，单独用时要减 2',
                 '先交换保证 `x<y`，再计算层级差',
                 '同层且相同时 lca 就是自己，只加上 y 上移的层数 + 1',
                 '对比灵神：灵神直接用 `(a^(b>>d)).bit_length()` 当 lca 距离；这里显式求出 lca 再做差'],
    ),
)
