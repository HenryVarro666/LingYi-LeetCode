def _cell(S, r, c, v):
    j, k = S.get('j'), S.get('k')
    if j is None or k is None or S.get('_line') not in (12, 13, 14):
        return None
    if (r, c) == (j, k):
        return 'yellow'
    if (r, c) == (j - S['cnt0'], k - S['cnt1']):
        return 'blue'
    return None


def _formula(S):
    if 'cnt0' not in S:
        return '`f[j][k]` = 至多 `j` 个 0、`k` 个 1 时，最多能选的字符串个数'
    s = S['s']
    base = f'`"{s}"`：`cnt0 = {S["cnt0"]}`，`cnt1 = {S["cnt1"]}`'
    j, k = S.get('j'), S.get('k')
    if j is not None and k is not None and S.get('_line') in (12, 13, 14):
        return base + f'；`f[{j}][{k}]` 与 `f[{j - S["cnt0"]}][{k - S["cnt1"]}] + 1` 比大小'
    if 'sum0' in S and S.get('_line', 0) >= 8:
        return base + f'；`sum0 = {S["sum0"]}`，`sum1 = {S["sum1"]}`（只更新到这里）'
    return base


CONFIG = dict(
    num=474, title='一和零', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='二维费用 0-1 背包 · 滚动数组 + 范围优化',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        f = [[0] * (n + 1) for _ in range(m + 1)]
        sum0 = sum1 = 0
        for s in strs:
            cnt0 = s.count('0')
            cnt1 = len(s) - cnt0
            sum0 = min(sum0 + cnt0, m)
            sum1 = min(sum1 + cnt1, n)
            for j in range(sum0, cnt0 - 1, -1):
                for k in range(sum1, cnt1 - 1, -1):
                    v = f[j - cnt0][k - cnt1] + 1
                    if v > f[j][k]:  # 手写 max，效率更高
                        f[j][k] = v
        return max(map(max, f))
''',
    call='Solution().findMaxForm(["10", "0", "1", "11"], 1, 2)',
    expect=2,
    max_steps=90,
    skip=['for j in range', 'for k in range'],
    views=[
        dict(type='array', var='strs', label='strs（蓝 = 当前字符串）', h=150, cell=90,
             color=lambda S, i, v: 'blue' if v == S.get('s') and 'cnt0' in S else None),
        dict(type='text', fn=_formula, size=22, h=70),
        dict(type='table', var='f', label='f[j][k]：j 个 0、k 个 1 的预算下最多选几个（黄 = 更新，蓝 = f[j-cnt0][k-cnt1]）', h=330, cell=80,
             rows=lambda S: [f'{i}个0' for i in range(S['m'] + 1)], cols=lambda S: [f'{i}个1' for i in range(S['n'] + 1)],
             color=_cell),
    ],
    watch=[('s', 's', 'blue'), ('cnt0', 'cnt0', 'cyan'), ('cnt1', 'cnt1', 'orange'),
           ('sum0', 'sum0', 'purple'), ('sum1', 'sum1', 'purple'), ('j', 'j', 'yellow'), ('k', 'k', 'yellow')],
    captions={
        'f = [[0]': '`f[j][k]`：至多 `j` 个 0、`k` 个 1 时最多选几个字符串；开始什么都没选，全是 0',
        'sum0 = sum1 = 0': '`sum0`、`sum1`：目前为止所有字符串里 0 和 1 的总数（不超过 `m`、`n`）',
        'for s in strs': '考虑字符串 `"{s}"`：选或不选，是一个 0-1 背包物品',
        'cnt0 = s.count': '`"{s}"` 有 `{cnt0}` 个 0',
        'cnt1 = len(s)': '长度 `{len(s)}` 减去 0 的个数，得 `{cnt1}` 个 1。物品体积 = (`{cnt0}`, `{cnt1}`)',
        'sum0 = min': '前面已有的 0 一共 `{sum0}` 个（封顶 `m = {m}`）：==再大的 j 根本凑不出来==，不必枚举',
        'sum1 = min': '1 的总数封顶 `{sum1}`：`k` 只需从 `{sum1}` 开始往下枚举',
        'v = f[j - cnt0]': '选它：`f[{j - cnt0}][{k - cnt1}] + 1` = =={v}==（腾出体积后的最优 + 1 个）',
        'if v > f[j][k]': '`{v} > f[{j}][{k}] = {f[j][k]}`？' ,
        'f[j][k] = v': '选它更好 → `f[{j}][{k}]` = =={v}==。==倒序==保证 `f[j-cnt0][k-cnt1]` 还是上一个字符串的值',
        'return max': lambda S, B, r: f'优化后只更新了部分格子，最大值未必在 `f[m][n]` → 遍历全表取最大 = =={r}==',
    },
    cards=dict(
        one_liner='物品有两种体积：0 的个数和 1 的个数',
        complexity='时间 `O(kmn+L)`，空间 `O(mn)`',
        problem=['二进制字符串数组 `strs` 和整数 `m`、`n`',
                 '选出最大的子集，使其中 ==至多 m 个 0、至多 n 个 1==，求子集大小',
                 '示例：`["10","0001","111001","1","0"], m=5, n=3` → `4`；本视频：`["10","0","1","11"], m=1, n=2` → `2`'],
        quote='这相当于背包有两种体积（二维），所以在定义状态的时候，相比只有一种体积的 0-1 背包，要多加一个参数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[j][k]` 表示最多 `j` 个 0、`k` 个 1 时最多选几个，转移 `f[j][k] = max(f[j][k], f[j-cnt0][k-cnt1] + 1)`',
              '去掉「前 i 个」这一维，==j、k 都倒序==，避免同一字符串选两次',
              '进一步优化：前面字符串的 0、1 总数有限，`j`、`k` 的起点用 `sum0`、`sum1` 封顶'],
        summary=['时间 `O(kmn+L)`，空间 `O(mn)`',
                 '易错：优化后只有部分格子被更新，答案要取整张表的最大值，不是 `f[m][n]`',
                 '易错：两层循环都要倒序',
                 '前面几种写法：记忆化搜索、三维递推、不加范围优化的二维滚动，答案一致'],
    ),
)
