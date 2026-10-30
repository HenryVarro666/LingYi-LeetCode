def _cover(S):
    d = S.get('diff')
    if d is None:
        return []
    return list(accumulate(d))


def _fin(S):
    return S.get('_line') == 8


CONFIG = dict(
    num=2848, title='与车相交的点', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='一维差分数组',
    tags=['差分', '难度分 1230'],
    code='''
class Solution:
    def numberOfPoints(self, nums: List[List[int]]) -> int:
        max_end = max(end for _, end in nums)
        diff = [0] * (max_end + 2)  # 注意下面有 end+1
        for start, end in nums:
            diff[start] += 1
            diff[end + 1] -= 1
        return sum(s > 0 for s in accumulate(diff))
''',
    call='Solution().numberOfPoints([[3,6],[1,5],[4,7]])',
    expect=7,
    views=[
        dict(type='array', var='diff', h=170, label='diff 差分数组（下标 = 数轴上的点）',
             color=lambda S, i, v: ('green' if v > 0 else 'pink' if v < 0 else None)),
        dict(type='array', var=_cover, h=170, label='accumulate(diff)：每个点被覆盖的次数（最后一步才算）',
             color=lambda S, i, v: 'green' if (S.get('_line') == 8 and v > 0) else None,
             dim=lambda S, i, v: S.get('_line') != 8),
        dict(type='text', size=26, fn=lambda S: (f"区间 `[{S['start']}, {S['end']}]`：`diff[{S['start']}] +1`，`diff[{S['end']+1}] −1`" if 'start' in S and 'end' in S and S.get('_line') in (6, 7) else '')),
    ],
    watch=[('max_end', 'max_end', 'blue'), ('start', 'start', 'blue'), ('end', 'end', 'pink')],
    skip=[],
    captions={
        'max_end = max': '最大终点 `max_end = {max_end}`，数轴上的点只会出现在 `1~{max_end}`',
        'diff = [0]': '建差分数组，长度 `max_end + 2 = {max_end + 2}`：==下面要访问 `end + 1`==，不多开一位会越界',
        'diff[start] += 1': '区间从 `{start}` 开始：差分在 `{start}` 处 `+1`，表示==从这里往后每个点覆盖次数都多 1==',
        'diff[end + 1] -= 1': '区间在 `{end}` 结束：差分在 `{end + 1}` 处 `−1`，把后面的 +1 抵消掉',
        'return sum': '`accumulate(diff)` 做前缀和还原出每个点的覆盖次数，统计 `> 0` 的点：=={ret}== 个',
    },
    cards=dict(
        one_liner='差分数组标记区间，前缀和还原覆盖次数',
        complexity='时间 `O(n+U)`，空间 `O(U)`，U 为最大终点',
        problem=['`nums[i] = [start, end]` 是一辆车在数轴上占的整数点',
                 '求被任意一辆车覆盖的整数点个数',
                 '示例：`[[3,6],[1,5],[4,7]]` → 点 1~7 都被覆盖，答案 `7`'],
        quote='计算每个点被覆盖了多少次。统计覆盖次数大于 0 的点，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['想象一个全 0 数组 `a`，每个区间让 `a[start..end]` 都加 1',
              '「区间内都加一」用差分：==`diff[start] += 1`，`diff[end+1] -= 1`==',
              '对 diff 做前缀和就还原出 `a`，数 `> 0` 的个数'],
        summary=['复杂度：`O(n+U)` 时间，`O(U)` 空间',
                 '易错点：数组长度要 `max_end + 2`，因为会访问 `end + 1`',
                 '同一题也能「排序 + 合并区间」做，见题单区间贪心',
                 '更多差分题见灵神数据结构题单「差分」'],
    ),
)
