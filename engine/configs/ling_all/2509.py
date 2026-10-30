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
    return (S['a'], S['b']) if 'a' in S and 'b' in S else None


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
    if 'a' not in S or 'b' not in S:
        return ''
    a, b = S['a'], S['b']
    if ln == 4:
        return f'a=`{a:b}`，b=`{b:b}`（保证 a ≤ b，b 更深或同层）'
    if ln == 5 and 'd' in S:
        return f'深度差 d = {b.bit_length()} − {a.bit_length()} = =={S["d"]}=='
    if ln == 6 and 'd' in S:
        d = S['d']
        s = b >> d
        return f'b>>{d} = `{s:b}`，a^(b>>d) = `{a ^ s:b}`，长度 L = =={(a ^ s).bit_length()}=='
    return f'a=`{a:b}`，b=`{b:b}`'


CONFIG = dict(
    num=2509, title='查询树中环的长度', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='位运算求 LCA',
    tags=['位运算', '链表树与回溯', '难度分 1948'],
    code='''
class Solution:
    def cycleLengthQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        for i, (a, b) in enumerate(queries):
            if a > b: a, b = b, a  # 保证 a <= b
            d = b.bit_length() - a.bit_length()
            queries[i] = d + (a ^ (b >> d)).bit_length() * 2 + 1
        return queries
''',
    call='Solution().cycleLengthQueries(3, [[5,3],[4,7],[2,3]])',
    expect=[4, 5, 3],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=_f, size=28, h=70),
    ],
    watch=['i', 'a', 'b', 'd', ('queries', 'queries', 'green')],
    captions={
        'for i, (a, b)': lambda S, B, r: ('所有查询处理完，循环结束' if 'i' in B and B.i == S.i else f'取第 `{S.i}` 个查询：在 `{S.a}` 和 `{S.b}` 之间连一条边'),
        'if a > b': lambda S, B, r: ('`a > b`：交换，保证 `a ≤ b`（编号大的更深）' if S.a != B.a else '`a ≤ b`：不用交换'),
        'd = b.bit_length()': '二进制长度 = 深度：`d = {b.bit_length()} − {a.bit_length()} = {d}`，b 要上跳 d 步才和 a 同层',
        'queries[i] =': '`b>>d` 把 b 上跳到 a 的层；`a ^ (b>>d)` 的长度 `L = {(a ^ (b >> d)).bit_length()}`：两人各上跳 L 步到 LCA。环长 = `{d} + 2×{(a ^ (b >> d)).bit_length()} + 1` = =={queries[i]}==',
        'return queries': '所有查询都已改写成答案：`{queries}`',
    },
    cards=dict(
        one_liner='编号二进制的长度是深度，异或看公共前缀',
        complexity='时间 `O(m)`，空间 `O(1)`',
        problem=['完全二叉树，节点 `v` 的左右孩子是 `2v`、`2v+1`',
                 '每次在 `a`、`b` 间加一条边，求形成的环长',
                 '示例：`n=3, [[5,3],[4,7],[2,3]]` → `[4,5,3]`'],
        quote='节点编号的二进制的长度恰好等于节点深度。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['环 = a 到 LCA + LCA 到 b + 新边，所以环长 = 两段距离 + 1',
              '先把深的 b 右移 d 位，和 a 同层；若相等，a 就是 LCA，答案 `d+1`',
              '不等时 `a ^ (b>>d)` 去掉公共前缀，剩下的长度 L 就是各自还要上跳的步数'],
        summary=['时间 `O(m)`，每个查询 `O(1)`；空间 `O(1)`（原地改写 queries）',
                 '方法一：`a>b` 就让 a //= 2，否则 b //= 2，直到相等，`O(nm)`',
                 '易错：先交换保证 a ≤ b，再算 d；异或长度要乘 2',
                 '同层且相等时 XOR 为 0，长度 0，公式自然退化为 `d+1`'],
    ),
)
