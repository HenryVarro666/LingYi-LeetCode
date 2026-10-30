def _txt(S):
    if 'suf' not in S or 'l' not in S:
        return '前缀和 `pre` 严格递增，后缀积 `suf` 非递减：谁小就推进谁'
    pre, suf, l, r = S['pre'], S['suf'], S['l'], S['r']
    if l >= r:
        return f'`l = {l} >= r = {r}`：`pre = {pre}`，`suf = {suf}` → {"==相等，答案 " + str(l) + "==" if pre == suf else "不相等，返回 -1"}'
    rel = '<' if pre < suf else ('==' if pre == suf else '>')
    return f'`pre = {pre}` {rel} `suf = {suf}`'


CONFIG = dict(
    num=3862, title='找出最小平衡下标', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前后缀 · 相向双指针',
    tags=['滑动窗口与双指针', '动态规划', '难度分 1697'],
    code='''
class Solution:
    def smallestBalancedIndex(self, nums: list[int]) -> int:
        pre, suf = 0, 1
        l, r = 0, len(nums) - 1
        while l < r and suf <= 10 ** 14:
            if pre < suf:
                pre += nums[l]
                l += 1
            else:
                suf *= nums[r]
                r -= 1
        return l if pre == suf else -1
''',
    call='Solution().smallestBalancedIndex([2,8,2,2,5])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={'l': 'blue', 'r': 'pink'}, h=300,
             color=lambda S, i, v: ('green' if i < S['l'] else 'orange' if i > S['r'] else None) if 'r' in S and 'l' in S else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('pre', 'pre', 'green'), ('suf', 'suf', 'orange')],
    captions={
        'pre, suf = 0, 1': '空前缀的和是 `0`，空后缀的积是 `1`',
        'l, r = 0': '`l` 从左、`r` 从右出发：`[0, l-1]` 是前缀，`[r+1, n-1]` 是后缀',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`，答案下标还没确定' if S.l < S.r and S.suf <= 10 ** 14
                                         else ('后缀积超过 `10^14`，前缀和不可能追上 → 结束' if S.l < S.r else f'`l = {S.l} >= r = {S.r}`：指针汇合，结束')),
        'if pre < suf': '`pre = {pre}` 与 `suf = {suf}` 比较 → {"前缀更小，要加大它" if pre < suf else "不小于，推进后缀"}',
        'pre += nums[l]': '前缀和太小：把 `nums[{l}] = {nums[l]}` 并入前缀，`pre` = =={pre}==',
        'l += 1': '`l` 右移到 {l}',
        'suf *= nums[r]': '前缀和不小于后缀积：把 `nums[{r}] = {nums[r]}` 乘进后缀，`suf` = =={suf}==（相等时也走这里，因为 `r` 肯定不是答案）',
        'r -= 1': '`r` 左移到 {r}',
        'return l if': lambda S, B, ret: (f'`pre == suf == {S.pre}`：`l = {S.l}` 就是平衡下标' if S.pre == S.suf else '`pre != suf`，不存在平衡下标 → -1'),
    },
    cards=dict(
        one_liner='谁小就推进谁：前缀和与后缀积像两条相向的曲线',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['下标 `i` 左侧元素之和 == 右侧元素之积，称 `i` 为平衡下标',
                 '左侧为空和视为 `0`，右侧为空积视为 `1`；求最小的平衡下标，没有则 `-1`',
                 '示例：`[2,8,2,2,5]` → `2`（`2+8 = 10 = 2*5`）'],
        quote='比较前缀和与后缀积的大小，谁小就移动哪边的指针（排除了一个错误答案）。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`nums[i] > 0`：前缀和单调递增，后缀积单调不减，至多一个交点',
              '前缀和更小就并入 `nums[l]`，否则把 `nums[r]` 乘进后缀积',
              '相等时 ==必须移右指针==：左指针加 1 可能让前缀和永远追不上'],
        after=[dict(heading='方法一：前后缀分解', lines=[
            '先算前缀和数组，再倒着遍历，边走边维护后缀积 `mul`',
            '优化：先求总和，倒序时减去 `nums[i]` 就得到前缀和，空间 `O(1)`',
        ])],
        summary=['时间 `O(n)`，空间 `O(1)`（方法一前缀数组 `O(n)`）',
                 '易错：`pre == suf` 时移动右指针，不能移动左指针',
                 '`suf` 超过 `10^14`（前缀和上界）就能提前返回 -1，避免大数相乘',
                 '思考题：含 0 和负数时单调性不成立，需要重新设计'],
    ),
)
