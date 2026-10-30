def _txt(S):
    if 'p' not in S:
        return '`f[i][j]`：花费不超过 i、用了 j 张券的最大口味'
    return f'当前水果：价格 `{S["p"]}`，口味 `{S["t"]}`；优惠券价格 `{S["p"]} // 2 = {S["p"] // 2}`'


CONFIG = dict(
    num=2431, title='最大限度地提高购买水果的口味', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='二维费用背包 · 优惠券维度',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def maxTastiness(self, price, tastiness, maxAmount, maxCoupons):

        f = [[0] * (maxCoupons + 1) for _ in range(maxAmount + 1)]
        for p, t in zip(price, tastiness):
            for j in range(maxCoupons, -1, -1):
                mi = p
                if j > 0:
                    mi //= 2
                
                for i in range(maxAmount, mi - 1, -1):
                    if i >= p:
                        f[i][j] = max(f[i - p][j] + t, f[i][j])
                    if j > 0:
                        f[i][j] = max(f[i - p // 2][j - 1] + t, f[i][j])

        return max(f[-1])
''',
    call='Solution().maxTastiness([4,6,6], [3,5,5], 8, 1)',
    expect=8,
    max_steps=52,
    skip=['mi = p'],
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='table', var='f', label='f[i][j]（行 i = 花费，列 j = 用券数；黄 = 正在更新）', h=420, cell=60,
             rows=lambda S: [str(i) for i in range(len(S['f']))],
             cols=lambda S: [f'券{j}' for j in range(len(S['f'][0]))],
             cursors=[('i', 'j', 'yellow', '(i,j)')],
             color=lambda S, i, j, v: 'green' if v else None),
    ],
    watch=[('p', 'p', 'pink'), ('t', 't', 'cyan'), ('i', 'i', 'blue'), ('j', 'j', 'yellow'), ('max(f[-1])', 'max(f[-1])', 'green')],
    captions={
        'f = [[0]': '`f[i][j]`：花费不超过 `i`、用了 `j` 张券最多买到的口味，初始都是 0',
        'for p, t in zip': '处理下一种水果：价格 `{p}`，口味 `{t}`',
        'for j in range': '优惠券数 `j = {j}` 也从大到小，配合倒序原地更新',
        'if j > 0': lambda S, B, r: ('`j > 0`：可以用券，最小花费降为 `p // 2`' if S.j > 0 else '`j = 0`：不能用券，最小花费是 `p`'),
        'mi //= 2': '有券时半价最低 `{mi}`，`i` 只需遍历到 `{mi}`',
        'for i in range': '花费 `i` 从大到小：保证每种水果只买一次',
        'if i >= p': lambda S, B, r: (f'`i = {S.i} ≥ p = {S.p}`：钱够原价买' if S.i >= S.p else f'`i = {S.i} < p = {S.p}`：钱不够原价买'),
        'f[i][j] = max(f[i - p][j] + t': '原价买：`f[{i} − {p}][{j}] + {t}` = `{B.f[i - p][j] + t}` 对比不买 `{B.f[i][j]}` → =={f[i][j]}==',
        'if j > 0:': lambda S, B, r: ('可以用券' if S.j > 0 else '没有券可用'),
        'f[i][j] = max(f[i - p // 2]': '用券买：`f[{i} − {p // 2}][{j} − 1] + {t}` = `{B.f[i - p // 2][j - 1] + t}` 对比当前 `{B.f[i][j]}` → =={f[i][j]}==',
        'return max': '`max(f[-1])`：花费用满 `maxAmount` 时各种券数里最好的口味 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='背包多加一维：已经用了几张优惠券',
        complexity='时间 `O(n·A·C)`，空间 `O(A·C)`',
        problem=['`price[i]` 是水果价格，`tastiness[i]` 是口味，预算 `maxAmount`，最多 `maxCoupons` 张半价券（向下取整）',
                 '每种水果最多买一次，每种最多用一张券，求最大总口味',
                 '本视频：`[4,6,6], [3,5,5], 8, 1` → `8`'],
        quote='对于优惠券，最直观的处理方法就是令f[k][i][j]表示前k种水果糖，使用i的代价以及j次优惠券最多可以买到的水果味道是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['普通背包 + 一维「券数」：每种水果有三选一：不买 / 原价买 / 半价买',
              '原价：`f[i−p][j] + t`；半价：`f[i−p//2][j−1] + t`',
              '倒序原地更新省掉水果这一维'],
        summary=['时间 `O(n·A·C)`，空间 `O(A·C)`',
                 '半价向下取整：用 `p // 2`，`j = 0` 时最小花费是 `p`',
                 '`i` 与 `j` 都要倒序，否则会重复买或重复用券',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`mi /= 2`、`p / 2`）'],
    ),
)
