A0 = [3, 2, 5, 6]
B0 = [2, -6, 4, -3, 2]


def _fmt(v):
    return '-∞' if v == float('-inf') else str(v)


def _formula(S, B):
    y, j = S.get('y'), S.get('j')
    if y is None or j is None or S.get('_line', 0) < 6:
        return '`f[k]` = 已看过的 `b` 里选 k 个数，与 `a` 的前 k 个相乘的最大点积'
    a, g = S['a'], B['f']
    return f'`f[{j + 1}] = max({_fmt(g[j + 1])}, {_fmt(g[j])} + {a[j]}×{y})` = =={_fmt(S["f"][j + 1])}=='


CONFIG = dict(
    num=3290, title='最高乘法得分', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='选或不选 · 0-1 背包式一维 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1692'],
    code='''
class Solution:
    def maxScore(self, a: List[int], b: List[int]) -> int:
        f = [0] + [-inf] * 4
        for y in b:
            for j in range(3, -1, -1):
                f[j + 1] = max(f[j + 1], f[j] + a[j] * y)
        return f[4]
''',
    call=f'Solution().maxScore({A0}, {B0})',
    expect=26,
    max_steps=90,
    skip=['for j in range'],
    views=[
        dict(type='array', var='a', label='a（粉 = 当前乘的 a[j]）', h=150, cell=64,
             color=lambda S, i, v: 'pink' if S.get('j') == i and S.get('_line', 0) >= 6 else None),
        dict(type='text', fn=lambda S: f"当前 `y = {S['y']}`（`b` 里正在考虑的数）" if 'y' in S else '', size=26, h=50),
        dict(type='array', var='f', label='f[k]：选了 k 个数的最大得分（黄 = 正在更新的 f[j+1]，绿 = 用到的 f[j]）', h=210, cell=84,
             color=lambda S, i, v: ('yellow' if S.get('j') is not None and S.get('_line', 0) >= 6 and i == S['j'] + 1 else
                                    'green' if S.get('j') is not None and S.get('_line', 0) >= 6 and i == S['j'] else None)),
        dict(type='text', fn=_formula, size=24, h=60),
    ],
    watch=[('y', 'y', 'blue'), ('j', 'j', 'pink'), ('a[j]', 'a[j]', 'pink')],
    captions={
        'f = [0]': '`f[0] = 0`：一个数都不选，得分 0；`f[1..4] = -∞`：还凑不出，不合法',
        'for y in b': lambda S, B, r: (('考虑 `b` 里的下一个数 `y = %d`：对每个 `j` 决定选不选它。`j` ==倒序==，这样用到的 `f[j]` 还是上一个数留下的（和 0-1 背包一样）' % S.y) if S.y != B.get('y')
                                       else '`b` 全部考虑完了'),
        'f[j + 1] =': lambda S, B, r: (f'`y = {S.y}`，不选 `y`：保持 `f[{S.j + 1}] = {_fmt(B.f[S.j + 1])}`；选 `y` 当第 {S.j + 1} 个：`f[{S.j}] + a[{S.j}]×y` = `{_fmt(B.f[S.j])} + {S.a[S.j]}×{S.y}`'
                                       f' → 取大 =={_fmt(S.f[S.j + 1])}=='),
        'return f[4]': '`f[4]` 就是选满 4 个数的最大得分 = =={ret}==',
    },
    cards=dict(
        one_liner='每个 b[i]：选，还是不选？',
        complexity='时间 `O(mn)`（`m = 4`），空间 `O(m)`',
        problem=['`a` 长度为 4，`b` 长度至少 4。从 `b` 里按下标递增选 4 个数 `b[i0..i3]`',
                 '得分 = `a[0]×b[i0] + a[1]×b[i1] + a[2]×b[i2] + a[3]×b[i3]`，求最大得分',
                 '示例：`a=[3,2,5,6]`，`b=[2,-6,4,-5,-3,2,-7]` → `26`'],
        quote='从 b 中选一个长为 4 的子序列，与 a 计算点积，返回最大点积。……像 0-1 背包那样，去掉第一个维度，把 f[i+1] 和 f[i] 保存到同一个数组中。……j 要倒序枚举。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「选或不选」：对 `b[i]`，不选就保持 `f[j+1]`；选就是 `f[j] + a[j]·b[i]`',
              '状态 `f[k]` = 选了 `k` 个数的最大点积；`f[0] = 0`，其余 `-∞` 表示不合法',
              '压成一维后 `j` 倒序，避免同一个 `b[i]` 被选两次'],
        summary=['时间 `O(mn)`，`m = 4`；空间 `O(m)`',
                 '易错：不合法状态要用 `-inf`，不能用 0，否则 `max` 会选到凑不出的方案',
                 '易错：`j` 必须倒序，正序会让同一个 `b[i]` 重复使用',
                 '题解还给了记忆化搜索、二维递推，以及展开成 `f0~f3` 四个变量的写法，这里演示一维版'],
    ),
)
