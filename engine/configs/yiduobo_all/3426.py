def _dx(m, n, i, j):
    return n * ((1 + i) * i // 2 + (m - i) * (m - i - 1) // 2)


def _dy(m, n, i, j):
    return m * ((1 + j) * j // 2 + (n - j) * (n - j - 1) // 2)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    m, n, k = S['m'], S['n'], S['k']
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), f'{m}×{n} 的格子：固定一颗棋子 (i, j)，数它到其余所有格子的距离之和', 24, T['muted'], bold=True)
    c = S.get('c')
    stage = 'C(mn−2, k−2) 先算阶乘：(mn−2)!，再乘 inv 除掉 (k−2)! 和 (mn−k)!'
    if line is not None and line >= 19:
        stage = f'这一对棋子固定后，其余 {k - 2} 颗的放法 c = C({m * n - 2}, {k - 2}) = {c}'
    cv.text((x0 + 18, y0 + 48), stage, 22, T['yellow'], bold=True)
    cell = min(130, (x1 - x0 - 80) / n, 150)
    gx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    gy = y0 + 150
    ci, cj = S.get('i'), S.get('j')
    started = 'res' in S and ci is not None
    for i in range(m):
        for j in range(n):
            done = started and ((i, j) < (ci, cj) or ((i, j) == (ci, cj) and line is not None and line >= 26))
            cur = started and (i, j) == (ci, cj)
            fill = T['blue'] if cur else (T['panel2'] if not done else (52, 70, 60))
            X, Y = gx + j * cell, gy + i * cell
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=fill, r=10, outline=T['border'])
            cv.text((X + 10, Y + 8), f'({i},{j})', 16, T['bg'] if cur else T['dim'], mono=True)
            if done:
                cv.text((X + cell / 2, Y + cell / 2 + 6), _dx(m, n, i, j) + _dy(m, n, i, j), 36, T['green'], anchor='mm', bold=True)
            elif cur and line is not None and line >= 25:
                cv.text((X + cell / 2, Y + cell / 2 + 6), f"{_dx(m, n, i, j)}" + (f"+{_dy(m, n, i, j)}" if line >= 26 or 'diff_y' in S and S.get('_done') else ''), 30, T['bg'], anchor='mm', bold=True)
    yb = gy + m * cell + 24
    if started:
        cv.text((x0 + 40, yb), '格子里的数 = 固定在该格时，行方向距离和 diff_x + 列方向距离和 diff_y（还没乘 c）', 20, T['muted'])
        cv.text((x0 + 40, yb + 34), f"res（已乘 c、取模）= {S['res']}", 26, T['green'], bold=True)


CONFIG = dict(
    num=3426, title='所有安放棋子方案的曼哈顿距离', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='贡献法 · 枚举固定点 + 逆元',
    tags=['灵神题单', '难度分 2443'],
    code='''
class Solution(object):
    def distanceSum(self, m, n, k):
        
        c = 1
        mod = 10 ** 9 + 7
        for v in range(1, m * n - 1):
            c = c * v % mod
        
        inv = [None, 1]
        for v in range(2, max(3, k - 1, m * n - k + 1)):
            inv.append((mod - mod // v) * inv[mod % v] % mod)

        for v in range(1, k - 1):
            c = c * inv[v] % mod
        
        for v in range(1, m * n - k + 1):
            c = c * inv[v] % mod

        print(c)

        res = 0
        for i in range(m):
            for j in range(n):
                diff_x = n * ((1 + i) * i // 2 + (m - i) * (m - i - 1) // 2) % mod
                diff_y = m * ((1 + j) * j // 2 + (n - j) * (n - j - 1) // 2) % mod
                res = (res + (diff_x + diff_y) * c) % mod
        
        return res * inv[2] % mod
''',
    call='Solution().distanceSum(2, 3, 3)',
    expect=100,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=['c', 'v', 'i', 'j', ('res', 'res', 'green')],
    captions={
        'c = 1': '`c` 要算成 `C(mn−2, k−2)`，先从 `1` 开始连乘',
        'mod = 10': '答案对 `10^9+7` 取模',
        'c = c * v % mod': lambda S, B, r: f"`c` 乘 `{S['v']}`：现在 `c = {S['c']}`" + ('（已是 `(mn−2)!`）' if S['v'] == S['m'] * S['n'] - 2 else ''),
        'inv = [None': '准备逆元表：`inv[1] = 1`，除法要变成乘逆元',
        'inv.append': '线性递推：`inv[{v}] = (mod − mod // {v}) × inv[mod % {v}]` = `{inv[-1]}`',
        'for v in range(1, k - 1)': lambda S, B, r: ('`inv[1..k−2]` 乘完了' if B.get('v') == S['v'] and S['v'] == S['k'] - 2 else '再乘 `inv[1..k−2]`：相当于除以 `(k−2)!`'),
        'for v in range(1, m * n - k + 1)': lambda S, B, r: ('`inv[1..mn−k]` 乘完了' if B.get('v') == S['v'] and S['v'] == S['m'] * S['n'] - S['k'] else '再乘 `inv[1..mn−k]`：相当于除以 `(mn−k)!`'),
        'c = c * inv[v]': '`c` 乘 `inv[{v}]` → `{c}`',
        'print(c)': '`c` = `(mn−2)! / ((k−2)!(mn−k)!)` = `C(mn−2, k−2)` = =={c}==',
        'res = 0': '`res` 累加所有「固定点 + 另一点」的距离',
        'for i in range': lambda S, B, r: ('所有行都枚举完了' if 'i' in B and B.i == S['i'] and S['i'] == S['m'] - 1 and B.get('j') == S.get('j') and S['j'] == S['n'] - 1 else f"固定点所在行 `i = {S['i']}`"),
        'for j in range': lambda S, B, r: ('这一行的列枚举完了' if B.get('j') == S['j'] and S['j'] == S['n'] - 1 else f"固定点 `(i, j) = ({S['i']}, {S['j']})`"),
        'diff_x =': '行方向：其余格到第 `{i}` 行的距离和 `n × (上方 + 下方)` = =={diff_x}==',
        'diff_y =': '列方向：其余格到第 `{j}` 列的距离和 `m × (左边 + 右边)` = =={diff_y}==',
        'res = (res +': '`res += ({diff_x} + {diff_y}) × c`：固定这一点的所有距离 × 其余棋子放法 → `{res}`',
        'return res': '每一对被数了两次 → 乘 `inv[2]`（模意义下的除以 2）= =={ret}==',
    },
    cards=dict(
        one_liner='固定一颗棋子，数其他格到它的距离和，最后除以 2',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m×n` 的格子里放 `k` 个相同的棋子，每格至多一个；求所有方案中每对棋子曼哈顿距离之和，对 `10^9+7` 取模',
                 '示例：`m=2, n=2, k=2` → `8`',
                 '本视频：`m=2, n=3, k=3` → `100`'],
        quote='由于题目需要计算的是曼哈顿距离，那么不妨将其拆分成水平上的距离和竖直上的距离，这样一来第二种方法似乎就可行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['一对棋子的距离乘上其余 `k−2` 颗的放法 `C(mn−2, k−2)`，就是这一对的总贡献',
              '固定其中一个点 `(i, j)`，把距离拆成水平、竖直两段，用等差和公式一列一列地求',
              '每一对被两个端点各算了一次 → 最后 ×2 的逆元'],
        summary=['时间 `O(mn)`，不用组合数表，只用线性逆元',
                 '`c` 要连乘 `(mn−2)!` 再乘 `inv` 去掉 `(k−2)!` 和 `(mn−k)!`',
                 '易错：每对棋子被算两次，最后要 `* inv[2]`；`inv` 表至少要到下标 2',
                 '原文为 Python 2 写法，`print c` 已改为 `print(c)`；`//` 本来就是整除，无需改动',
                 '对比灵神：灵神把横、纵求和化简成 `C(n+1,3)` 直接 `O(1)`；yiduobo 逐格枚举，更直观'],
    ),
)
