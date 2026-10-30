def _xy(S):
    return ('x' in S and 'mn' in S)

CONFIG = dict(
    num=910, title='最小差值 II', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 枚举分界线',
    tags=['贪心与思维', '难度分 2135'],
    code='''
class Solution:
    def smallestRangeII(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = nums[-1] - nums[0]
        for x, y in pairwise(nums):
            mx = max(x + k, nums[-1] - k)
            mn = min(nums[0] + k, y - k)
            ans = min(ans, mx - mn)
        return ans
''',
    call='Solution().smallestRangeII([6,1,10,3], 3)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"前半 `≤ {S['x']}` 全部 ==+k==，后半 `≥ {S['y']}` 全部 ==−k=="
                                         + (f"：最大 `{S['mx']}`" if 'mx' in S and S['_line'] >= 6 else '')
                                         + (f'，最小 `{S["mn"]}`' if 'mn' in S and S['_line'] >= 7 else '')) if 'y' in S else ''),
        dict(type='array', var='nums', h=300,
             color=lambda S, i, v: ('blue' if v <= S['x'] else 'pink') if 'y' in S else None),
        dict(type='text', fn=lambda S: (f"分数 `{S['mx']} − {S['mn']}` = =={S['mx']-S['mn']}==，目前最小 `{S['ans']}`" if 'mn' in S and 'ans' in S and S['_line'] >= 7 else ''), size=30),
    ],
    watch=['k', ('x', 'x', 'blue'), ('y', 'y', 'pink'), 'mx', 'mn', ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '先排序：`{nums}`，方便枚举「前面变大、后面变小」的分界线',
        'ans = nums[-1]': '全部 `+k` 或全部 `-k`，分数都是 `max − min` = `{ans}`，作为答案的初值',
        'for x, y in pairwise': lambda S, B, r: (f'分界线在 `{S.x}` 与 `{S.y}` 之间：`nums[0]` 到 `{S.x}` 都变大 `k`，`{S.y}` 到末尾都变小 `k`' if S.x != B.get('x') else '相邻对都枚举完了，退出循环'),
        'mx = max': '最大值只可能是 `x + k = {x + k}` 或 `nums[-1] - k = {nums[-1] - k}` → `mx = {mx}`',
        'mn = min': '最小值只可能是 `nums[0] + k = {nums[0] + k}` 或 `y - k = {y - k}` → `mn = {mn}`',
        'ans = min': '这条分界线的分数 `{mx} − {mn}` = {mx - mn}，`ans = min({B.ans}, …) = {ans}`',
        'return ans': '枚举完所有分界线，最小分数 `{ans}`',
    },
    cards=dict(
        one_liner='排序后，前面的数 +k、后面的数 −k，枚举分界线',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每个 `nums[i]` 必须变成 `nums[i]+k` 或 `nums[i]-k`',
                 '分数 = 最大值 − 最小值，求最小分数',
                 '示例：`[0,10], k=2` → `6`；本视频：`[6,1,10,3], k=3` → `4`'],
        quote='考虑把 nums[0] 到 nums[i-1] 都变大 k，把 nums[i] 到 nums[n-1] 都变小 k。如此变化后，数组的最大值要么是 nums[i-1]+k，要么是 nums[n-1]-k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案初值：全部同加或同减，分数 `nums[-1] − nums[0]`', '枚举分界线 `(x, y)`：左边 +k，右边 −k', '最大值取 `max(x+k, 末尾−k)`，最小值取 `min(首+k, y−k)`'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '`ans` 初值不能漏：对应所有数同加或同减',
                 '最大、最小值各有两个候选，别只取其中一个',
                 '思考题：恰好修改 m 个元素时，答案如何变化'],
    ),
)
