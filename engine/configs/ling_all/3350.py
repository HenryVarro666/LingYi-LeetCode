CONFIG = dict(
    num=3350, title='检测相邻递增子数组 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 严格递增段',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1600'],
    code='''
class Solution:
    def maxIncreasingSubarrays(self, nums: List[int]) -> int:
        ans = pre_cnt = cnt = 0
        for i, x in enumerate(nums):
            cnt += 1
            if i == len(nums) - 1 or x >= nums[i + 1]:  # i 是严格递增段的末尾
                ans = max(ans, cnt // 2, min(pre_cnt, cnt))
                pre_cnt = cnt
                cnt = 0
        return ans
''',
    call='Solution().maxIncreasingSubarrays([2,5,7,8,9,2,3,4,3,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, window=('i - cnt + 1', 'i'), h=300,
             label='nums（框 = 当前递增段，蓝 = i）',
             color=lambda S, i, v: None),
        dict(type='text', fn=lambda S: f"`pre_cnt = {S['pre_cnt']}`，`cnt = {S['cnt']}`：同段切半 `cnt // 2 = {S['cnt'] // 2}`，相邻两段 `min = {min(S['pre_cnt'], S['cnt'])}`" if 'cnt' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('cnt', 'cnt', 'cyan'), ('pre_cnt', 'pre_cnt', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = pre_cnt': '`ans` 答案；`pre_cnt` 上一个递增段长度；`cnt` 当前递增段长度，都从 0 开始',
        'cnt += 1': '`nums[{i}] = {x}` 并入当前递增段，`cnt` = {cnt}',
        'if i == len': lambda S, B, r: (f'`{S.x} ≥ nums[{S.i+1}] = {S.nums[S.i+1]}` → 递增在这里断了，`i` 是这一段的末尾'
                                       if S.i < len(S.nums) - 1 and S.x >= S.nums[S.i + 1]
                                       else ('`i` 是数组最后一个元素 → 也是一段的末尾' if S.i == len(S.nums) - 1
                                             else f'`{S.x} < nums[{S.i+1}] = {S.nums[S.i+1]}` → 还在递增，继续')),
        'ans = max': '本段长 `{cnt}`：同段切两半 `{cnt}//2 = {cnt//2}`；与上一段取小 `min({pre_cnt}, {cnt}) = {min(pre_cnt, cnt)}`；`ans` = =={ans}==',
        'pre_cnt = cnt': '这一段处理完，变成「上一段」：`pre_cnt = {pre_cnt}`',
        'cnt = 0': '`cnt` 清零，开始数下一段',
        'return ans': '最大的 k 是 `{ans}`',
    },
    cards=dict(
        one_liner='把数组切成严格递增段，答案只有两种来源',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最大的 `k`，使得存在两个相邻、长度都为 `k` 的严格递增子数组',
                 '相邻：第二个紧接在第一个后面',
                 '示例：`[2,5,7,8,9,2,3,4,3,1]` → `3`（`[7,8,9]` 和 `[2,3,4]`）'],
        quote='两个子数组属于同一个严格递增段，那么 k 最大是 floor(cnt/2)。两个子数组分别属于一对相邻的严格递增段，那么 k 最大是 min(preCnt, cnt)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先找严格递增段，如示例 1：`[2,5,7,8,9]`、`[2,3,4]`、`[3]`、`[1]`',
              '同一段内切两半：`k = cnt // 2`',
              '相邻两段：取前一段后缀与后一段前缀，`k = min(pre_cnt, cnt)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：段末判断 `x >= nums[i+1]` 要用大于等于（严格递增）',
                 '最后一个元素也要当作段末，所以加 `i == len(nums) - 1`',
                 '处理完一段别忘了 `pre_cnt = cnt` 和 `cnt = 0`'],
    ),
)
