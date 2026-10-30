def _cap_upd(S, B, ret):
    j, c, s = S.j, S.c, S.s
    new = B.f[j - c] + s[c - 1]
    if new > B.f[j]:
        return f'取 `{c}` 枚：`f[{j - c}] + s[{c - 1}] = {B.f[j - c]} + {s[c - 1]} = {new}` 比 `f[{j}] = {B.f[j]}` 大 → 更新为 =={new}=='
    return f'取 `{c}` 枚：`f[{j - c}] + s[{c - 1}] = {new}`，不比 `f[{j}] = {B.f[j]}` 大 → 不变'


CONFIG = dict(
    num=2218, title='从栈中取出 K 个硬币的最大面值和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前缀和 + 滚动数组背包',
    tags=['灵神题单', '动态规划', '难度分 2158'],
    code='''
class Solution(object):
    def maxValueOfCoins(self, piles, k):

        f = [0] * (k + 1)
        for pile in piles:
            s = [pile[0]]
            for coin in pile[1:]:
                s.append(s[-1] + coin)
                
            for j in range(k, -1, -1):
                for c in range(1, min(j, len(s)) + 1):
                    f[j] = max(f[j], f[j - c] + s[c - 1])

        return f[-1]
''',
    call='Solution().maxValueOfCoins([[1,100,3],[7,8],[5,2]], 3)',
    expect=108,
    views=[
        dict(type='text', fn=lambda S: ('这一堆的前缀和 s：' + ', '.join(f'取{i+1}个={v}' for i, v in enumerate(S['s']))) if 's' in S else '每堆只能取顶上若干枚，先做前缀和', size=24, h=60),
        dict(type='array', var='s', label='前缀和 s', h=190, pointers={'c': 'pink'}, index=True),
        dict(type='array', var='f', label='f[j]：操作 j 次的最大面值', h=230, pointers={'j': 'blue'}),
    ],
    watch=['k', 'j', 'c', ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f = [0]': '`f[j]`：处理完已看过的堆，一共操作 `j` 次能得到的最大面值，初始 0',
        'for pile in piles': '换一堆硬币，用它更新 `f`',
        's = [pile[0]]': '`s[0]` = 取 1 枚的面值 `{s[0]}`',
        's.append': '`s[{len(s)-1}]` = 取 {len(s)} 枚的面值和 `{s[-1]}`',
        'for j in range': '`j` 从大到小：这样 `f[j - c]` 还是上一堆的旧值，不用二维数组',
        'for c in range': '枚举在这一堆取 `c` 枚，`c` 最多 `min(j, 堆大小)`',
        'f[j] = max': _cap_upd,
        'return f[-1]': '操作 `{k}` 次的最大面值和 ==`{f[-1]}`==',
    },
    skip=['for coin in pile', 'for c in range'],
    cards=dict(
        one_liner='每堆取前缀，用前缀和做转移，倒序滚动 f',
        complexity='时间 `O(k·sum(len))`，空间 `O(k)`',
        problem=['若干堆硬币，每次只能拿某堆最上面的一枚', '恰好拿 `k` 次，求面值之和最大',
                 '示例：`[[1,100,3],[7,8,9]], k=2` → `101`；视频用 `[[1,100,3],[7,8],[5,2]], k=3`'],
        quote='令f[i][j]表示前i堆硬币，操作j次可以得到的最大面值，那么对于f[i][j]，就可以尝试对第i - 1堆硬币操作0到min(j, len(piles[i - 1]))次。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j] = max(f[i-1][j], f[i-1][j-c] + s[c-1])`，`c` 是这一堆取的枚数',
              '`s` 是这一堆的前缀和，取 `c` 枚的面值直接查 `s[c-1]`',
              '每轮只依赖上一轮，`j` 倒着遍历就能省掉 `i` 这一维'],
        summary=['时间 `O(k·sum(piles[i].length))`，空间 `O(k)`',
                 '易错：`j` 必须倒序，否则同一堆会被重复取',
                 '`c` 从 1 开始，不取的情况由 `f[j]` 自己保留',
                 '对比灵神：灵神把每栈看成分组背包并限制 `j` 的上界；这里直接遍历到 `k`'],
    ),
)
