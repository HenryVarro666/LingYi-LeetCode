CONFIG = dict(
    num=334, title='递增的三元子序列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='LIS 贪心 + 二分', tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        g = []
        for x in nums:
            j = bisect_left(g, x)
            if j == 2:  # LIS 长度至少是 3
                return True
            if j == len(g):  # >=x 的 g[j] 不存在
                g.append(x)
            else:
                g[j] = x
        return False
''',
    call='Solution().increasingTriplet([2,1,5,0,4,6])',
    expect=True,
    views=[
        dict(type='array', var='nums', h=200, label='nums（黄色 = 当前 x）',
             color=lambda S, i, v: 'yellow' if 'x' in S and v == S['x'] else None),
        dict(type='array', var='g', h=200, label='g：长为 j+1 的递增子序列的最小结尾',
             pointers={'j': 'pink'}),
        dict(type='text', fn=lambda S: f"`g = {S['g']}`，长度 {len(S['g'])}，要凑够 ==3==" if 'g' in S else ''),
    ],
    watch=[('x', 'x', 'yellow'), ('j', 'j', 'pink'), ('g', 'g', 'cyan')],
    captions={
        'g = []': '`g[j]` 表示长度为 `j+1` 的递增子序列里，最小的结尾；先空着',
        'j = bisect_left': '二分找 `g` 中第一个 `>= {x}` 的位置：`j = {j}`',
        'if j == 2': lambda S, B, r: (f'`j = {S.j}`：说明 `g[0]`、`g[1]` 都比 `{S.x}` 小 → 已有长 2 的递增序列接上 `{S.x}`，==长度达到 3==' if S.j == 2
                                      else f'`j = {S.j} < 2`：`{S.x}` 最多接成长 {S.j + 1}，还不到 3'),
        'if j == len(g)': lambda S, B, r: (f'`j = {S.j} = len(g)`：`g` 里没有 `>= {S.x}` 的数 → `{S.x}` 比所有结尾都大，可以让序列变长'
                                           if S.j == len(S.g) else f'`g[{S.j}] = {S.g[S.j]} >= {S.x}`：`{S.x}` 能替换它，同样长度结尾更小'),
        'g.append': '`g` 末尾加入 `{x}`：最长递增子序列长度变为 =={len(g)}==',
        'g[j] = x': '用 `{x}` 替换 `g[{j}]`：长度不变，但结尾更小，后面更容易接上',
        'return True': '找到长度为 3 的递增子序列 → ==返回 True==',
        'return False': '扫完也没有长度 3 的递增子序列',
    },
    cards=dict(
        one_liner='递增子序列的子序列仍递增：LIS 长度 ≥ 3 即可',
        complexity='时间 `O(n log K)`（K = 2，视作 `O(n)`），空间 `O(1)`',
        problem=['判断数组里是否存在下标 `i<j<k` 且 `nums[i]<nums[j]<nums[k]`',
                 '示例：`[2,1,5,0,4,6]` → `True`（如 `1,4,6`）'],
        quote='由于递增子序列的子序列一定是递增的，我们可以先计算 nums 的最长递增子序列，然后从中取出一个长为 3 的子序列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把本题看成 300 题的 LIS，只问 ==L ≥ 3== 是否成立',
              '`g[j]` 存长为 `j+1` 的递增子序列的最小结尾，`g` 一定递增，用二分找位置',
              '`bisect_left` 返回 2，就说明接在长 2 的后面，立刻返回'],
        summary=['`g` 至多两个元素，二分视作常数，整体 `O(n)`',
                 '求严格递增用 `bisect_left`，非降要换 `bisect_right`',
                 '`g` 不是真正的子序列，只记录各长度的最小结尾',
                 '把 3 改成 k，只需把 `j == 2` 改成 `j == k - 1`'],
    ),
)
