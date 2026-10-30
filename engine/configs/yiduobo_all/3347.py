CONFIG = dict(
    num=3347, title='执行操作后元素的最高频率 II', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='候选中心点 + 滑动窗口', tags=['三指针', '难度分 2156'],
    code='''
class Solution(object):
    def maxFrequency(self, nums, k, numOperations):
        cnt = {}
        num_set = set()
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            num_set.add(v)
            num_set.add(v - k)
            num_set.add(v + k)

        nums.sort()
        left = 0
        right = 0
        res = 0
        for v in sorted(list(num_set)):
            while right < len(nums) and nums[right] - k <= v:
                right += 1
            while nums[left] + k < v:
                left += 1

            res = max(res, min(numOperations, right - left - cnt.get(v, 0)) + cnt.get(v, 0))
        return res
''',
    call='Solution().maxFrequency([1,2,4,4,7], 2, 2)',
    expect=3,
    max_steps=110, skip=[3, 4, 6, 7, 8, 12, 13, 14, 15],
    views=[
        dict(type='text', size=28, fn=lambda S: (f"目标 v=`{S['v']}`：窗口 [v−k, v+k] = `[{S['v'] - S['k']}, {S['v'] + S['k']}]` 覆盖 `{S['right'] - S['left']}` 个数，其中 `{S['cnt'].get(S['v'], 0)}` 个本来就是 v" if 'v' in S and 'right' in S and 'left' in S and S['_line'] >= 16 else f"候选目标：每个 v、v−k、v+k（共 {len(S['num_set'])} 个）" if 'num_set' in S and S['_line'] >= 12 else f"k=`{S['k']}`，numOperations=`{S['numOperations']}`")),
        dict(type='array', var='nums', h=280, pointers={'left': 'blue', 'right - 1': 'pink'}, pointer_labels={'right - 1': 'right-1'},
             window=('left', 'right - 1'),
             color=lambda S, idx, v: ('green' if 'v' in S and v == S['v'] and 'left' in S else None)),
        dict(type='map', var='cnt', h=140, fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('v', 'v', 'green'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'for v in nums': '遍历 `v = {v}`',
        'num_set.add(v + k)': '`cnt[{v}]` → {cnt[v]}；候选点：`{v}`、`{v - k}`、`{v + k}`（共 {len(num_set)} 个）',
        'nums.sort()': '排序：到 v 距离 ≤ k 的数是一段连续区间',
        'while right < len(nums)': lambda S, B, r: (f'目标 `v={S.v}`：`nums[{S.right}] - k = {S.nums[S.right] - S.k} <= v = {S.v}`：能变成 v → right 右移' if S.right < len(S.nums) and S.nums[S.right] - S.k <= S.v else f'目标 `v={S.v}`：`right = {S.right}`，再往右的数 `- k > v`，够不到 v'),
        'right += 1': '`right` → {right}',
        'while nums[left] + k < v': lambda S, B, r: (f'`nums[{S.left}] + k = {S.nums[S.left] + S.k} < v`：变不到 v → left 右移' if S.nums[S.left] + S.k < S.v else f'`nums[{S.left}] + k >= v`：left 停下'),
        'left += 1': '`left` → {left}',
        'res = max(res': '覆盖 `{right - left}` 个，`{cnt.get(v, 0)}` 个已是 v：`min({numOperations}, {right - left - cnt.get(v, 0)}) + {cnt.get(v, 0)}` → `res` = =={res}==',
        'return res': '最高频率 `{res}`',
    },
    cards=dict(
        one_liner='把每个数看成区间，找覆盖次数最多的点，操作数限制取 min',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次操作选一个没选过的下标，把它加上 `[-k, k]` 内一个整数，共 `numOperations` 次',
                 '求操作后出现次数最多的元素的频率',
                 '本视频：`[1,2,4,4,7]`，`k=2`，`numOperations=2` → `3`'],
        quote='最多区间相交的下标一定处于某个区间的起点或者终点。最多只有 n * 3 种可能的下标位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[i]` 变成 `[nums[i]-k, nums[i]+k]`：求被覆盖最多的点',
              '候选点只有 `v`、`v-k`、`v+k`；排序后用滑动窗口数 `[v-k, v+k]` 里有几个数',
              '窗口里本来等于 v 的 `cnt[v]` 个不用操作，其余最多改 `numOperations` 个'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '公式 `min(numOperations, m - cnt[v]) + cnt[v]`：本来等于 v 的不占操作次数',
                 '易错：`cnt.get(v, 0)`，v 不在 nums 里时 cnt 为 0',
                 '原文为 Python 2 风格，只删去了函数开头的空行',
                 '对比灵神：灵神枚举 nums 里的 x，再单独处理“变成不在 nums 的数”'],
    ),
)
