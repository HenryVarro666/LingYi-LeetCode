CONFIG = dict(
    num='LCP 22', title='黑白方格画', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='枚举行数 · 组合数',
    code='''
class Solution(object):
    def paintingPlan(self, n, k):

        if k == n * n:
            return 1

        C = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 10, 6, 1]]

        res = 0
        for x in range(n):
            if k >= x * n and (k - x * n) % (n - x) == 0:
                y = (k - x * n) // (n - x)
                res += C[n][x] * C[n][y]
        
        return res
''',
    call='Solution().paintingPlan(3, 5)',
    expect=9,
    views=[
        dict(type='custom', h=330, draw=lambda cv, S, B, box, T: _draw(cv, S, box, T)),
        dict(type='text', fn=lambda S: (f"黑格数 `(x + y) × n − x × y` = `({S['x']} + {S['y']}) × {S['n']} − {S['x']} × {S['y']}` = =={(S['x'] + S['y']) * S['n'] - S['x'] * S['y']}==" if 'y' in S and 'x' in S and S.get('_line', 0) >= 12 else (f"试 x = {S['x']} 行" if 'x' in S else '')), size=34),
        dict(type='text', fn=lambda S: f"方案数累计 ==`{S['res']}`==" if 'res' in S else ''),
    ],
    watch=['n', 'k', 'x', 'y', ('res', 'res', 'green')],
    captions={
        'if k == n * n': '全部格子都要涂黑：只有 1 种方案吗？`k = {k}`，`n × n = {n * n}` → {"是，直接返回 1" if k == n * n else "不是，继续算"}',
        'C = [[1]': '`C[n][x]` 是杨辉三角（预先写好的组合数表）：从 n 里选 x 个',
        'res = 0': '`res` 累计方案数',
        'for x in range(n)': '枚举涂黑的行数 `x = {x}`（列数 y 由 k 算出）',
        'if k >= x * n': '总黑格 `(x+y)n − xy = k`，整理得 `y(n − x) = k − xn`；需要 `k − xn = {k - x * n}` 非负且能被 `n − x = {n - x}` 整除 → {"满足" if (k >= x * n and (k - x * n) % (n - x) == 0) else "不满足，换下一个 x"}',
        'y = (k - x * n)': '解出 `y = ({k} − {x} × {n}) // ({n} − {x})` = =={y}==',
        'res += C[n][x]': '选行 `C({n},{x}) = {C[n][x]}`，选列 `C({n},{y}) = {C[n][y]}`，相乘累加 → `res` = =={res}==',
        'return res': '所有 x 枚举完，一共 `{res}` 种',
    },
    cards=dict(
        one_liner='设涂黑 x 行 y 列，黑格数 (x+y)n − xy = k',
        complexity='时间 `O(n)`，空间 `O(1)`（组合数表为常数大小）',
        problem=['`n × n` 的白色方格，每次选一整行或一整列涂黑，可以重复选',
                 '求恰好得到 `k` 个黑格的方案数（行列选法不同就算不同方案）',
                 '本视频：`n = 3, k = 5` → `9`'],
        quote='不妨设最终涂黑了x行、y列，那么一共就有(x + y) * n - x * y个格子被涂黑，这里减去x * y的理由是一共有x * y个格子是在行和列涂黑时都被计算了的。',
        quote_src='—— yiduobo 题解原文',
        idea=['行列交叉的 `x·y` 个格子被算了两次，所以要减掉',
              '`n` 很小，直接枚举 x，看 y 是否有整数解',
              '每组 `(x, y)` 贡献 `C(n,x) × C(n,y)` 种选法'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`k == n*n` 要单独返回 1（此时 x=n 不在循环里）；`n − x` 作除数，x 只枚举到 `n − 1`',
                 '`k − x·n` 必须非负且能整除 `n − x`',
                 '原文为 Python 2 写法，`y` 的整数除法 `/` 已改为 `//`'],
    ),
)


def _draw(cv, S, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    cell = min(80, (y1 - y0 - 40) / n)
    sx = x0 + ((x1 - x0) - cell * n) / 2
    sy = y0 + 20
    x = S.get('x')
    y = S.get('y') if S.get('_line', 0) >= 12 else None
    for r in range(n):
        for c in range(n):
            black = (x is not None and r < x) or (y is not None and c < y)
            both = (x is not None and r < x) and (y is not None and c < y)
            fill = (235, 238, 242) if not black else (150, 70, 40) if both else (40, 44, 52)
            cv.rect((sx + c * cell + 2, sy + r * cell + 2, sx + (c + 1) * cell - 2, sy + (r + 1) * cell - 2), fill=fill, r=4)
    if x is not None:
        cv.text((x0 + (x1 - x0) / 2, sy + n * cell + 10), f'涂黑前 {x} 行' + ('，前 %d 列（橙 = 重复格）' % y if y is not None else ''), 22, T['muted'], anchor='mt')
