def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, k = S['n'], S['k']
    lo, hi = max(n - k, 1), n + k
    xs = list(range(lo, hi + 1))
    cur = S.get('x')
    line = S.get('_line', 0)
    w = max(n.bit_length(), hi.bit_length())
    cv.text((x0 + 18, y0 + 4), f'n = {n} = {n:0{w}b}（二进制）；枚举 x ∈ [{lo}, {hi}]，看 n & x 是否为 0', 24, T['muted'], bold=True)
    cols = [x0 + 40, x0 + 190, x0 + 400, x0 + 640]
    yh = y0 + 56
    for c, h in zip(cols, ['x', 'x 的二进制', 'n & x', '兼容？']):
        cv.text((c, yh), h, 22, T['dim'], bold=True)
    rh = min(58, (y1 - yh - 110) / max(len(xs), 1))
    for r, x in enumerate(xs):
        y = yh + 40 + r * rh
        ok = (n & x) == 0
        seen = cur is not None and (x < cur or (x == cur and line >= 6))
        here = cur == x
        col = (T['green'] if ok else T['pink']) if seen else T['dim']
        if here:
            cv.rect((x0 + 14, y - 6, x1 - 14, y + rh - 12), outline=T['yellow'], width=4, r=10)
        cv.text((cols[0], y), str(x), 28, T['text'] if seen or here else T['dim'], mono=True, bold=True)
        cv.text((cols[1], y), f'{x:0{w}b}', 28, T['text'] if seen or here else T['dim'], mono=True)
        if seen or (here and line >= 6):
            cv.text((cols[2], y), f'{n & x:0{w}b}', 28, col, mono=True, bold=True)
            cv.text((cols[3], y), '是，累加' if ok else '否', 26, col, bold=True)
    cv.text((x1 - 14, y1 - 10), f"res = {S.get('res', 0)}", 30, T['green'], anchor='rb', bold=True, mono=True)


CONFIG = dict(
    num=3954, title='区间内的兼容数字之和 I', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='暴力枚举区间',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def sumOfGoodIntegers(self, n, k):
        
        res = 0
        for x in range(max(n - k, 1), n + k + 1):
            if (n & x) == 0:
                res += x

        return res
''',
    call='Solution().sumOfGoodIntegers(5, 3)',
    expect=10,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('n', 'n', 'blue'), ('x', 'x', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计兼容整数之和',
        'for x in range': lambda S, B, r: (f'枚举 `x = {S.x}`（范围 `[max(n-k, 1), n+k]` = `[{max(S.n - S.k, 1)}, {S.n + S.k}]`）'
                                            if B.get('x') != S.x else '范围里的 x 都枚举完了，循环结束'),
        'if (n & x) == 0': lambda S, B, r: (f'`{S.n} & {S.x}` = `{S.n:04b} & {S.x:04b}` = `{S.n & S.x:04b}` → '
                                             + ('==为 0==，x 兼容' if S.n & S.x == 0 else '不为 0，有某一位两边都是 1 → 跳过')),
        'res += x': '`res` += `{x}` → =={res}==',
        'return res': '所有兼容整数之和：`{res}`',
    },
    cards=dict(
        one_liner='数据只有 100，直接枚举区间里每个 x',
        complexity='时间 `O(k)`，空间 `O(1)`',
        problem=['正整数 `x` 兼容：`abs(n - x) <= k` 且 `n & x == 0`，求所有兼容整数之和',
                 '`n, k` 都不超过 100',
                 '示例：`n = 2, k = 3` → `10`；本视频 `n = 5, k = 3` → `10`'],
        quote='由于题目的数据规模较小，在这里可以直接从max(1, n - k)到n + k枚举所有可能的x，若当前的x与n按位与结果为0，就将x累加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`abs(n - x) <= k` 等价于 `x ∈ [n-k, n+k]`，再保证 `x >= 1`',
              '区间长度最多 `2k+1`，逐个检查 `(n & x) == 0`'],
        summary=['时间 `O(k)`，空间 `O(1)`',
                 '下界要取 `max(n - k, 1)`：x 必须是==正==整数',
                 '`range` 右端点开区间，所以写 `n + k + 1`',
                 '`n & x` 要加括号：`==` 的优先级比 `&` 高',
                 '原文为 Python 2 写法，这里无需改动',
                 '对比灵神：灵神把同样的暴力作为方法一，另给了数据范围更大的数位 DP / 贡献法'],
    ),
)
