def _ds(x):
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s


def _nums(s):
    return [x for x in range(5001) if _ds(x) == s]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    if 'cur' not in S or 'f' not in S:
        cv.text((x0 + 18, y0 + 4), '每个数位和对应一组候选数：数位和 1 → 1, 10, 100, 1000', 24, T['muted'], bold=True)
        return
    pre, cur, f = S['pre'], S['cur'], S['f']
    a, b = _nums(B.get('pre', pre) if line == 30 else pre), _nums(cur)
    j = 0 if line < 21 else S['j']
    s = 0 if line < 22 else S['s']
    x = S['x'] if 23 <= line <= 29 and 'x' in S else None
    fin = line >= 30
    bi = b.index(x) if x in b else -1

    def row(y, title, vals, cellw, fn):
        cv.text((x0 + 18, y), title, 22, T['muted'], bold=True)
        n = len(vals)
        w = min(cellw, (x1 - x0 - 60) / max(n, 1))
        sx = x0 + 30
        for k, v in enumerate(vals):
            X = sx + k * w
            fill, tc, ring, sub = fn(k, v)
            cv.rect((X + 3, y + 40, X + w - 3, y + 40 + 62), fill=fill, r=8, outline=T['border'])
            cv.text((X + w / 2, y + 40 + 31), v, 24 if w > 70 else 20, tc, anchor='mm', bold=True, mono=True)
            if ring:
                cv.rect((X + 1, y + 37, X + w - 1, y + 105), outline=T[ring], width=4, r=10)
            cv.text((X + w / 2, y + 112), sub, 22, T['text'], anchor='mt', bold=True)
        return sx, w

    def fa(k, v):
        used = k < j
        return ((T['green'] if used else T['panel2']), (T['bg'] if used else T['muted']),
                ('pink' if k == j and x is not None and not fin and j < len(a) else None), f[v] if v < len(f) else 0)

    ya = y0 + 6
    row(ya, f'a = 数位和为 {pre} 的数（上一轮；下方是 f = 以它结尾的个数；绿 = 已并入 s）', a, 96, fa)

    def fb(k, v):
        done = fin or (x is not None and (k < bi or (k == bi and line >= 29)))
        cur_ = (x is not None and k == bi)
        fill = T['yellow'] if (cur_ and not done) else (T['blue'] if done else T['panel2'])
        return fill, (T['bg'] if fill != T['panel2'] else T['muted']), None, (f[v] if done else '?')

    yb = ya + 190
    row(yb, f'b = 数位和为 {cur} 的数（这一轮；黄 = 当前 x，蓝 = 已算出 f[x]）', b, 96, fb)
    yt = yb + 190
    if x is not None:
        cv.text((x0 + 18, yt), f'双指针：a 只往右走，x 变大时 a 里 ≤ x 的数只增不减 → 累加和 s = {s}', 24, T['text'], bold=True)
    elif fin:
        cv.text((x0 + 18, yt), '这一轮结束：b 变成下一轮的 a', 24, T['text'], bold=True)
    else:
        cv.text((x0 + 18, yt), f'准备：a = 数位和 {pre} 的数；b = 数位和 {cur} 的数；s 清零', 24, T['text'], bold=True)


MOD = 1_000_000_007

CONFIG = dict(
    num=3883, title='统计满足数位和数组的非递减数组数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前缀和优化 DP · 双指针优化',
    tags=['灵神题单·动态规划', '前缀和优化 DP', '难度分 2172'],
    code='''
MOD = 1_000_000_007
MX = 5001
MAX_DIGIT_SUM = 31  # 4999 的数位和最大
sum_to_nums = [[] for _ in range(MAX_DIGIT_SUM + 1)]
dig_sum = [0] * MX
for x in range(MX):
    # 去掉 x 的个位，问题变成 x // 10 的数位和，即 dig_sum[x // 10]
    dig_sum[x] = dig_sum[x // 10] + x % 10
    sum_to_nums[dig_sum[x]].append(x)

class Solution:
    def countArrays(self, digitSum: List[int]) -> int:
        f = [0] * MX  # f[x] 表示以 x 结尾的有效数组的个数
        f[0] = 1
        pre = 0

        for cur in digitSum:
            if cur > MAX_DIGIT_SUM:
                return 0
            a = sum_to_nums[pre]
            j, m = 0, len(a)
            s = 0
            for x in sum_to_nums[cur]:
                # 有效数组的前一个数只要 <= x 就行
                while j < m and a[j] <= x:
                    s += f[a[j]]
                    j += 1
                # s 现在就是以 x 结尾的有效数组的个数
                f[x] = s % MOD
            pre = cur  # 记录上一个数位和

        return sum(f[x] for x in sum_to_nums[pre]) % MOD
''',
    call='Solution().countArrays([1, 1])',
    expect=10,
    skip=[18, 22],
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=[('cur', 'cur', 'blue'), ('x', 'x', 'yellow'), ('j', 'j', 'pink'), ('s', 's', 'green')],
    captions={
        13: '`f[x]`：以 `x` 结尾的有效数组个数，先全 0',
        14: '`f[0] = 1`：空数组算 1 种；第一个数的「前一个数」当作 0',
        15: '`pre` = 上一个数位和，起点是 0（候选只有数 0）',
        17: lambda S, B, r: ('`digitSum` 都处理完了（`f[1000]` 已是第二轮的 4）' if S.get('x') is not None and S.f[1000] == 4 else f'处理 `digitSum` 的下一项：`cur = {S.cur}`'),
        18: '`cur > 31` 就不可能有数（5000 以内数位和最大是 31）→ 本题答案 0；这里 `cur = {cur}` 没问题',
        20: '`a` = 数位和为 `{pre}` 的所有数（有序）：它们是上一位的候选值',
        21: '`j` 是 `a` 的指针，`m = {m}` 是 `a` 的长度',
        22: '`s` 累加 `a` 中已经 `<= x` 的那些数的 `f`',
        23: lambda S, B, r: (f'这一位的候选 `x = {S.x}`（`b = sum_to_nums[cur]`，从小到大）' if S.x != B.get('x') or S.j != B.get('j') and False else '`b` 里的候选都处理完了'),
        25: lambda S, B, r: (f'`a[{S.j}] = {S.a[S.j]} <= x = {S.x}` → 它能接在 `x` 前面，并入 `s`' if S.j < S.m and S.a[S.j] <= S.x else (f'`a` 已用完（`j = {S.j} = m`）→ 不再累加' if S.j >= S.m else f'`a[{S.j}] = {S.a[S.j]} > x = {S.x}` → 后面的更大，也不行 → 停；`x` 变大才会再接纳它')),
        26: '`s += f[{a[j - 0]}]`：前一个数取 `{a[j]}` 的方案数并入 → `s = {s}`',
        27: '`j` 右移 → `{j}`：`a` 和 `x` 都递增，指针不用回头',
        29: '`f[{x}] = s = {s}`：前一个数 `<= {x}` 的所有方案数之和',
        30: '这一轮的数位和成为下一轮的「上一个」：`pre = {pre}`',
        32: '答案 = 以 `pre` 对应候选结尾的方案数之和 = =={ret}==',
    },
    cards=dict(
        one_liner='只看数位和相同的那些数，a、b 两个有序列表用双指针累加',
        complexity='时间 `O(nV)`，`V ≤ 365`；空间 `O(U)`，`U = 5000`',
        problem=['`arr` 长 `n`，每项在 `[0, 5000]`，非递减，且 `arr[i]` 的数位和等于 `digitSum[i]`',
                 '数出不同的有效数组，对 `10^9+7` 取模',
                 '示例：`[1]` → `4`；本视频：`digitSum = [1, 1]` → `10`'],
        quote='我们其实只需考虑数组 a 和 b 中的数字如何转移，无需考虑 [0,5000] 中的所有数字，从而减少计算量。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[x]` = 以 `x` 结尾的有效数组个数 = 上一位所有 `≤ x` 的候选 `y` 的 `f[y]` 之和',
              '候选数按数位和预处理成有序列表：`a`（上一轮）、`b`（这一轮）',
              '`a`、`b` 都递增 → 指针 `j` 只增不减，`s` 累加，免去前缀和数组'],
        summary=['时间 `O(nV)`，空间 `O(U)`；题解方法一用前缀和数组 `O(nU)`，这里选更快的方法二',
                 '`cur > 31` 直接返回 0：5000 以内数位和最大是 31',
                 '`f` 跨轮复用：只有 `b` 里的位置被覆盖，`a` 的值读完后就用不到了',
                 '最后只对 `pre` 对应的候选数求和，别漏掉 `% MOD`',
                 '预处理在模块层，不计入题解的主体复杂度'],
    ),
)
