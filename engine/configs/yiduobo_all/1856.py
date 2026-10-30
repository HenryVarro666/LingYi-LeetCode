def _ln(S):
    return S.get('_line') or 0


def _info(S):
    if 'res' in S:
        return '第三趟：每个数当最小值，区间尽量拉长，乘区间和，取最大'
    if 'right_pos' in S:
        return '第二趟（倒序）：求右边第一个更小的数的位置；right_pos 倒着填，最后 reverse'
    return '第一趟：栈里存下标，数值从底到顶严格递增；弹完后栈顶就是左边第一个更小的数'


def _lr(S, B, ret):
    i = S.index
    l, r = S.left_pos[i], S.right_pos[i]
    lo = l + 1
    return f'`nums[{i}] = {S.nums[i]}` 当最小值：区间 `[{lo}, {r - 1}]`，区间和 `{S.delta}`，乘积 `{S.nums[i] * S.delta}`'


CONFIG = dict(
    num=1856, title='子数组最小乘积的最大值', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 + 前缀和',
    tags=['灵神题单', '单调栈'],
    code='''
class Solution(object):
    def maxSumMinProduct(self, nums):

        n = len(nums)

        stack = []
        left_pos = []
        for index in range(n):
            while stack and nums[stack[-1]] >= nums[index]:
                stack.pop()
            if not stack:
                left_pos.append(-1)
            else:
                left_pos.append(stack[-1])
            stack.append(index)
        
        stack = []
        right_pos = []
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] >= nums[index]:
                stack.pop()
            if not stack:
                right_pos.append(n)
            else:
                right_pos.append(stack[-1])
            stack.append(index)
        right_pos.reverse()

        mod = 10 ** 9 + 7
        s = [nums[0]]
        for num in nums[1:]:
            s.append(s[-1] + num)

        res = 0
        for index in range(n):
            delta = s[right_pos[index] - 1]
            if left_pos[index] >= 0:
                delta -= s[left_pos[index]]
            res = max(res, nums[index] * delta)
        
        return res % mod
''',
    call='Solution().maxSumMinProduct([2, 3, 3, 1, 2])',
    expect=18,
    skip=['n = len(nums)', 'stack = []', 'left_pos = []', 'right_pos = []', 'mod = 10'],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, cell=90, h=190),
        dict(type='stack', var='stack', label='stack（下标，底→顶）', h=120, font=26),
        dict(type='array', var='left_pos', label='left_pos：左边第一个更小的下标（-1 = 没有）', cell=64, h=110, index=False),
        dict(type='array', var='right_pos', label='right_pos：右边第一个更小的下标（5 = 没有）', cell=64, h=110, index=False),
        dict(type='array', var='s', label='s：前缀和', cell=64, h=110, index=False),
        dict(type='text', fn=_info, size=22, h=50),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'while stack and nums[stack[-1]] >= nums[index]': lambda S, B, r: (
            f'栈顶 `{S.nums[S.stack[-1]]}` ≥ 当前 `{S.nums[S.index]}`：栈顶不会是「更小」的那个，也不会再被后面用到 → 弹出'
            if S.stack and S.nums[S.stack[-1]] >= S.nums[S.index]
            else '栈空或栈顶更小：栈顶就是离当前数最近的、更小的数，停'),
        'left_pos.append(-1)': '栈空：左边没有更小的数，区间可以一直扩到最左边 → 记 `-1`',
        'left_pos.append(stack[-1])': '左墙是下标 `{B.stack[-1]}`（值 `{nums[B.stack[-1]]}`）→ 区间只能从它右边开始',
        'right_pos.append(n)': '栈空：右边没有更小的数，区间可以扩到最右边 → 记 `n = {n}`',
        'right_pos.append(stack[-1])': '右墙是下标 `{B.stack[-1]}`（值 `{nums[B.stack[-1]]}`）→ 区间只能到它左边',
        'stack.append(index)': '当前下标入栈，保持栈内数值严格递增',
        'right_pos.reverse()': '`right_pos` 是倒着追加的，翻转后下标才对齐',
        's = [nums[0]]': '前缀和 `s[i]` = `nums[0..i]` 之和，区间和 `O(1)` 可得',
        's.append(s[-1] + num)': '`s` 末尾追加 `{s[-2]} + {num}` = =={s[-1]}==',
        'delta = s[right_pos[index] - 1]': '区间右端是 `right_pos − 1 = {right_pos[index] - 1}`：先取 `s` 到这里的和 `{delta}`',
        'delta -= s[left_pos[index]]': '减去左墙及其左边的和 `s[{left_pos[index]}]` → 区间和 =={delta}==',
        'res = max': lambda S, B, r: f'`nums[{S.index}] = {S.nums[S.index]}` 当最小值，区间 `[{S.left_pos[S.index] + 1}, {S.right_pos[S.index] - 1}]`，和 `{S.delta}`，乘积 `{S.nums[S.index] * S.delta}` → `res = max({B.res}, …)` = =={S.res}==',
        'return res % mod': '最后才取模：比较时用真实值，返回 =={ret}==',
    },
    cards=dict(
        one_liner='枚举每个数当最小值，区间能拉多长拉多长',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['区间 `[l, r]` 的最小乘积 = ==区间最小值 × 区间和==，数组元素都是正数',
                 '求所有子数组中最小乘积的最大值，结果对 `10^9 + 7` 取余',
                 '示例：`[2,3,3,1,2]` → `18`（取 `[3,3]`，3 × 6）'],
        quote='如果知道了这个最小值，又因为数组中的数都是正数，因此肯定是将l和r扩展得越远最小乘积就越大。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定最小值 `nums[i]`，数都是正的，区间越长和越大',
              '区间边界 = 左右两侧第一个更小的数，用单调栈各扫一遍求出',
              '区间和用前缀和 `O(1)` 求，每个数算一次乘积取最大'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：比较大小时不能先取模，最后才 `% mod`',
                 '弹栈条件用 `>=`，相等的数也弹出，保证边界是「严格更小」',
                 '原文为 Python 2 风格，代码未做修改即可在 Python 3 运行',
                 '题面库中缺失，题意按 LeetCode 1856 原题撰写'],
    ),
)
