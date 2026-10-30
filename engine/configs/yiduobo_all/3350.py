CONFIG = dict(
    num=3350, title='检测相邻递增子数组 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='切分递增段 · 取半或取小',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1600'],
    code='''
class Solution(object):
    def maxIncreasingSubarrays(self, nums):
        
        res = 0
        pre_len = 0
        pre = nums[0]
        now_len = 1
        for v in nums[1:]:
            if v > pre:
                now_len += 1
            else:
                res = max(res, now_len // 2, min(pre_len, now_len))
                pre_len = now_len
                now_len = 1
            
            pre = v
        
        res = max(res, now_len // 2, min(pre_len, now_len))
        return res
''',
    call='Solution().maxIncreasingSubarrays([2,5,7,8,9,2,3,4,3,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', pointers={'v': 'blue'}, h=300, label='nums（当前扫到的 v 用蓝色箭头标出）',
             color=lambda S, i, v: None),
        dict(type='text', fn=lambda S: f"`pre_len = {S['pre_len']}`，`now_len = {S['now_len']}`：取半 `{S['now_len'] // 2}`，取小 `{min(S['pre_len'], S['now_len'])}`" if 'now_len' in S else ''),
    ],
    watch=[('v', 'v', 'blue'), ('pre', 'pre', 'purple'), ('now_len', 'now_len', 'cyan'), ('pre_len', 'pre_len', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 是最大的 k',
        'pre_len = 0': '`pre_len`：上一个递增段的长度',
        7: '`now_len`：当前递增段长度，`nums[0]` 自己算 1',
        'pre = nums[0]': '`pre` 记前一个数，从 `nums[0] = {pre}` 开始',
        'for v in nums[1:]': lambda S, B, r: ('遍历结束，还差最后一段没结算' if getattr(B, 'v', None) == S.v and S.v == S.nums[-1] and S.pre == S.v else f'看下一个数 `v = {S.v}`'),
        'if v > pre': lambda S, B, r: (f'`{S.v} > {S.pre}` → 仍然严格递增' if S.v > S.pre else f'`{S.v} ≤ {S.pre}` → 递增断了'),
        'now_len += 1': '接在当前段后面，`now_len` = {now_len}',
        'res = max(res, now_len // 2, min(pre_len, now_len))': '结算一段：从中间劈开 `{now_len}//2 = {now_len//2}`；与上一段取小 `min({pre_len}, {now_len}) = {min(pre_len, now_len)}`；`res` = =={res}==',
        'pre_len = now_len': '当前段变成上一段：`pre_len = {pre_len}`',
        14: '新的一段从 `v` 开始，`now_len = 1`',
        'pre = v': '`pre` 更新为 `{pre}`',
        'return res': '最大的 k 是 `{res}`',
    },
    cards=dict(
        one_liner='尽量长的递增段：要么从中间劈开，要么取相邻两段的较短者',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最大的 `k`，使得存在两个相邻、长度都为 `k` 的严格递增子数组',
                 '3349 题是给定 k 判断是否存在，3350 直接求最大 k',
                 '本视频：`[2,5,7,8,9,2,3,4,3,1]` → `3`'],
        quote='最大的k要么是两个相邻的递增子数组中长度的较小值，要么是某个递增子数组长度的一半。',
        quote_src='—— yiduobo 题解原文',
        idea=['情况 1：前半段末尾 ≥ 后半段开头，如 `[7,8,9,2,3,4]`：左段后缀 + 右段前缀',
              '情况 2：一个递增段从中间劈开，如 `[1,2,3,4]`',
              '一趟遍历切出尽量长的递增段，每段结算一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：循环结束后最后一段还没结算，要在循环外再算一次',
                 '`v > pre` 是严格递增，相等也算断开',
                 '原文是 Python 3 也能运行的写法（`//` 本来就是整除），未做修改',
                 '对比灵神：灵神在段末判断（看 `nums[i+1]`）；yiduobo 在断点处回头结算，所以要补最后一段'],
    ),
)
