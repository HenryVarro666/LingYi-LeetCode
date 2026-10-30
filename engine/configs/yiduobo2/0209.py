NUMS = [2, 3, 1, 2, 4, 3]
TARGET = 7


def _win(S):
    if 'now' not in S or 'right' not in S:
        return f'要求：子数组和 `≥ s = {TARGET}`'
    l, r = S['left'], S['right']
    if l > r:
        return f'窗口为空（left 已越过 right），`now = {S["now"]}`'
    return f"窗口 `nums[{l}..{r}]` = `{S['nums'][l:r + 1]}`，和 `now = {S['now']}`"


def _cap_grow(S, B, ret):
    r, now = B.right, B.now
    if r + 1 < len(NUMS) and now < TARGET:
        return f'`now = {now} < {TARGET}` 且右边还有数 → right 往右==试探==一格'
    if now >= TARGET:
        return f'`now = {now} ≥ {TARGET}`：找到了 left = `{S.left}` 的最小右边界 `right = {r}`'
    return f'`right = {r}` 已到末尾，`now = {now}` 仍 < {TARGET}'


def _cap_shrink(S, B, ret):
    l, r, now = B.left, B.right, B.now
    if l < r and now - NUMS[l] >= TARGET:
        return f'去掉 `nums[{l}] = {NUMS[l]}` 后 `{now} − {NUMS[l]} = {now - NUMS[l]} ≥ {TARGET}` 仍满足 → 左端点可以右移'
    if l >= r:
        return '窗口只剩一个数，不能再缩'
    return f'去掉 `nums[{l}] = {NUMS[l]}` 后 `{now} − {NUMS[l]} = {now - NUMS[l]} < {TARGET}` → 不能再缩，这就是当前最短窗口'


CONFIG = dict(
    num=209, title='长度最小的子数组', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='双指针：右边界只增不减',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def minSubArrayLen(self, s, nums):

        if not nums or sum(nums) < s:
            return 0

        now = nums[0]
        left = 0
        right = 0
        res = len(nums)
        while left < len(nums):
            while right + 1 < len(nums) and now < s:
                right += 1
                now += nums[right]
            if now < s:
                break
            while left < right and now - nums[left] >= s:
                now -= nums[left]
                left += 1
            res = min(res, right - left + 1)
            now -= nums[left]
            left += 1

        return res
''',
    call=f'Solution().minSubArrayLen({TARGET}, {NUMS})',
    expect=2,
    skip=[8, 9, 13],
    views=[
        dict(type='text', fn=_win, size=26, h=60),
        dict(type='array', var='nums', label='nums（青框 = 窗口 [left, right]，两端都包含）', h=250,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', fn=lambda S: f"当前最短 `res = {S['res']}`" if 'res' in S else '', size=28, h=70),
        dict(type='text', fn=lambda S: '关键结论：left 右移后，最优右边界 ==只会不变或右移== → right 不回头', size=24, h=56),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'if not nums or sum': '`sum(nums) = {sum(nums)} ≥ {s}`：一定有解（否则直接返回 0）',
        'now = nums[0]': '窗口 `[0, 0]` 先只放 `nums[0]`：`now = {now}`，`left = right = 0`',
        'res = len(nums)': '`res = len(nums) = {res}`：整个数组一定满足，作为初始答案',
        'while left < len(nums)': lambda S, B, r: (f'枚举左端点 `left = {B.left}`' if B.left < len(NUMS) else '左端点枚举完毕'),
        'while right + 1 <': _cap_grow,
        'now += nums[right]': '`right` → {right}，加入 `nums[{right}] = {nums[right]}`：`now = {now}`',
        'if now < s': lambda S, B, r: ('right 到头了还凑不够 → 后面的 left 更不可能，`break`' if S.now < TARGET
                                       else f'`now = {S.now} ≥ {TARGET}`，窗口满足要求'),
        'while left < right and': _cap_shrink,
        'res = min(res': '用窗口长度 `{right} − {left} + 1 = {right - left + 1}` 更新：`res = {res}`',
        21: '准备换下一个左端点：`nums[{left}] = {B.now - now}` 移出窗口，`now = {now}`',
        22: '`left` → {left}；right ==不用回退==，从原位置继续试探',
        16: '跳出循环',
        18: '`nums[{left}]` 移出窗口 → `now = {now}`',
        19: '`left` → {left}：窗口更短且仍满足',
        'return res': '返回最短长度 =={ret}==',
    },
    cards=dict(
        one_liner='对每个左端点找最小右边界，而右边界只会往右走',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定==正整数==数组 `nums` 和正整数 `s`（原文参数名，即 target）',
                 '找出总和 `≥ s` 的==长度最小==的连续子数组，返回其长度；不存在返回 `0`',
                 '示例：`s = 7, nums = [2,3,1,2,4,3]` → `2`（子数组 `[4,3]`）'],
        quote='对于i来说，若i - 1找到的最优右边界为j\'，那么==i的右边界j一定大于等于j\'==。',
        quote_src='—— yiduobo 题解原文',
        idea=['反证：若 `nums[i..j] ≥ s` 且 `j < j\'`，则 `nums[i-1..j]` 也 `≥ s`，j\' 就不是 i−1 的最优',
              '所以 right 在上一个位置的基础上==往右逐个试探==，不用回头',
              '每个 i、每个 j 只遍历一次 → `O(n)`；原文还给了前缀和 + 二分的 `O(n log n)` 做法'],
        summary=['时间 `O(n)`：left、right 都只右移',
                 '先判断 `sum(nums) < s` 直接返回 0，于是 `res = len(nums)` 可作初始值',
                 '`if now < s: break`：right 到头仍不够，更大的 left 只会更不够',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神枚举右端点、缩左端点；yiduobo 枚举左端点、推右端点'],
    ),
)
