def _seg(S):
    if 'p' not in S:
        return ''
    s = f"`p={S['p']}`"
    if 'q' in S:
        s += f"　`q={S['q']}`"
    for k, name in (('middle', '中间段和'), ('left', '左延伸和'), ('right', '右延伸和')):
        if k in S:
            s += f"　{name} `{k}={S[k]}`"
    return s


CONFIG = dict(
    num=3640, title='三段式数组 II', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='以递减段为中心向两侧扩展',
    tags=['动态规划', '难度分 2278'],
    code='''
class Solution(object):
    def maxSumTrionic(self, nums):
        
        p = 0
        res = None
        while p < len(nums):
            while p + 1 < len(nums) and nums[p + 1] >= nums[p]:
                p += 1
            
            if p + 1 == len(nums):
                break
            
            q = p + 1
            middle = nums[p] + nums[q]
            while q + 1 < len(nums) and nums[q + 1] < nums[q]:
                q += 1
                middle += nums[q]

            if q + 1 == len(nums):
                break

            if p == 0 or nums[p - 1] == nums[p]:
                p = q
                continue
            
            left = nums[p - 1]
            p -= 1
            while p > 0 and nums[p - 1] < nums[p] and nums[p - 1] > 0:
                left += nums[p - 1]
                p -= 1

            if nums[q + 1] == nums[q]:
                p = q + 1
                continue
            
            right_one = nums[q + 1]
            right = nums[q + 1]
            q += 1
            while q + 1 < len(nums) and nums[q + 1] > nums[q]:
                q += 1
                right += nums[q]

            tot = left + middle + max(right, right_one)
            if res is None or res < tot:
                res = tot
            p = q
        
        return res
''',
    call='Solution().maxSumTrionic([-1,2,4,1,0,3,5,2])',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums', h=300, pointers={'p': 'blue', 'q': 'pink'},
             window=('p', 'q')),
        dict(type='text', fn=_seg, size=26, h=100),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), 'middle', 'left', 'right', ('res', 'res', 'green')],
    max_steps=90,
    skip=['res = None'],
    captions={
        'while p + 1 < len(nums) and nums[p + 1] >= nums[p]': lambda S, B, ret: (f"`nums[{S['p']+1}]={S['nums'][S['p']+1]} >= nums[{S['p']}]={S['nums'][S['p']]}`，还在上升，`p` 继续右移" if S['p'] + 1 < len(S['nums']) and S['nums'][S['p']+1] >= S['nums'][S['p']] else f"`p={S['p']}` 就是这一轮上升段的终点（峰顶），后面开始下降"),
        'if p + 1 == len(nums)': lambda S, B, ret: "`p` 已在末尾，后面没有下降段了 → 结束" if S['p'] + 1 == len(S['nums']) else "后面还有元素，可以开始找下降段",
        'q = p + 1': '以 `p={p}` 为峰顶，递减段从 `p` 到 `q`，先让 `q = {q}`',
        'middle = nums[p] + nums[q]': '递减段必须完整包含：`middle = {nums[p]} + {nums[q]} = {middle}`',
        'while q + 1 < len(nums) and nums[q + 1] < nums[q]': lambda S, B, ret: (f"`nums[{S['q']+1}]={S['nums'][S['q']+1]} < nums[{S['q']}]={S['nums'][S['q']]}`，递减继续" if S['q'] + 1 < len(S['nums']) and S['nums'][S['q']+1] < S['nums'][S['q']] else f"递减段到 `q={S['q']}` 为止（谷底）"),
        'middle += nums[q]': '递减段每个数都必须选：`middle = {middle}`',
        'if q + 1 == len(nums)': lambda S, B, ret: "谷底后面没有元素，没法再接上升段 → 结束" if S['q'] + 1 == len(S['nums']) else "谷底右边还有元素",
        'if p == 0 or nums[p - 1] == nums[p]': lambda S, B, ret: "峰顶左边没有更小的数可接上升，这个递减段作废，`p` 跳到 `q` 重新找" if S['p'] == 0 or S['nums'][S['p']-1] == S['nums'][S['p']] else "左边 `nums[p-1] < nums[p]`，左侧可以接一段上升",
        'left = nums[p - 1]': '向左：`nums[p-1]` 必选（至少两个数），`left = {left}`',
        'while p > 0 and nums[p - 1] < nums[p]': lambda S, B, ret: (f"`nums[{S['p']-1}]={S['nums'][S['p']-1]}` 递增且为正，加进来只会更大，继续左扩" if S['p'] > 0 and S['nums'][S['p']-1] < S['nums'][S['p']] and S['nums'][S['p']-1] > 0 else "再往左的数不是正数（或不再递增），不加了"),
        'left += nums[p - 1]': '`left = {left}`',
        'if nums[q + 1] == nums[q]': lambda S, B, ret: "谷底右边相等，不能严格上升 → 作废" if S['nums'][S['q']+1] == S['nums'][S['q']] else "谷底右边 `nums[q+1] > nums[q]`，可以接上升段",
        'right_one = nums[q + 1]': '向右：至少要 `nums[q+1]`（`right_one = {right_one}`）；上升段可能先降后升的和，只有「只取一个」或「全取」两种可能最大',
        'while q + 1 < len(nums) and nums[q + 1] > nums[q]': lambda S, B, ret: (f"`nums[{S['q']+1}]={S['nums'][S['q']+1]} > nums[{S['q']}]`，上升继续，全部纳入 `right`" if S['q'] + 1 < len(S['nums']) and S['nums'][S['q']+1] > S['nums'][S['q']] else f"上升段到 `q={S['q']}` 为止"),
        'tot = left': '这个三段式的和：`left + middle + max(right, right_one)` = `{left} + {middle} + max({right}, {right_one})` = =={tot}==',
        'res < tot': lambda S, B, ret: f"`res = {S['res']}`，`tot = {S['tot']}`，取较大的",
        'p = q': '下一轮从 `q = {q}` 开始（这一段的末尾还可能是下一个三段式的第一段）',
        'return res': '没有更多了，返回 `{res}`',
    },
    cards=dict(
        one_liner='中间的递减段固定死，向左右两边各自贪心扩展',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['三段式子数组：先严格递增，再严格递减，再严格递增',
                 '在所有三段式子数组中，求和最大的',
                 '示例：`[-1,2,4,1,0,3,5,2]` → `15`，对应 `[2,4,1,0,3,5]`'],
        quote='对于一个三段式子数组，其正中间 p 到 q 的单调递减的这一段必然是 nums 中一个完整的单调递减子数组，只有这样才可能在满足 p 到 q 单调递减的前提下，使得 l 到 p 以及 q 到 r 这一段单调递增。',
        quote_src='—— yiduobo 题解',
        idea=['一趟遍历，找出每个完整的递减段 `p..q` 作为中间段',
              '向左：`nums[p-1]` 必选，再往左只加递增且为正的数',
              '向右：`nums[q+1]` 必选；后面的上升段要么只取第一个，要么全取（先降后升的 V 形，最大值在端点）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`p == 0` 或 `nums[p-1] == nums[p]` 时左边接不上，这个递减段作废',
                 '易错点：向右不能贪「只加正数」，因为必须连着取；只取一个或全取两种方案比较',
                 '原文就是 Python 3 可运行的写法，代码未改动；`res` 初值是 `None`，题目保证有解'],
    ),
)
