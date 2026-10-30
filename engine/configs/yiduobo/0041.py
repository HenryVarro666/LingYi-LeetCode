NUMS = [3, 4, -1, 1, 1]


def _while_cap(S, B, ret):
    i, nums = B.index, B.nums
    n, v = len(nums), nums[i]
    if not (v > 0 and v <= n):
        return f'`nums[{i}] = {v}` 不在 `1..{n}` 之间：==不用考虑==，看下一个位置'
    if v - 1 == i:
        return f'`nums[{i}] = {v}` 已经在自己的位置 `{v - 1}` 上'
    if nums[v - 1] == v:
        return f'位置 `{v - 1}` 上已经有一个 `{v}`：==重复的 p 不再移动=='
    return f'`p = {v}` 不该在位置 `{i}`，应归位到 `{v - 1}`（那里是 `{nums[v - 1]}`）→ 交换'


def _if_cap(S, B, ret):
    i, v = B.index, B.nums[B.index]
    if v - 1 != i:
        return f'`nums[{i}] = {v}`，`{v} − 1 ≠ {i}`：==nums 中不存在 {i + 1}=='
    return f'`nums[{i}] = {v}` 在正确位置，说明 `{i + 1}` 存在'


CONFIG = dict(
    num=41, title='缺失的第一个正数', difficulty='Hard', category='普通数组',
    author='yiduobo', technique='原地哈希（交换归位）',
    code='''
class Solution(object):
    def firstMissingPositive(self, nums):
        for index in range(len(nums)):
            while nums[index] > 0 and nums[index] <= len(nums) and \\
                    nums[index] - 1 != index and nums[nums[index] - 1] != nums[index]:
                tmp = nums[index]
                nums[index] = nums[tmp - 1]
                nums[tmp - 1] = tmp

        for index in range(len(nums)):
            if nums[index] -1 != index:
                return index + 1
        return len(nums) + 1
''',
    call=f'Solution().firstMissingPositive({NUMS})',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 已归位：nums[k] = k + 1）', pointers={'index': 'yellow'},
             color=lambda S, k, v: 'green' if v == k + 1 else None,
             dim=lambda S, k, v: not (0 < v <= len(NUMS)), cell=100, h=230),
    ],
    skip=['nums[index] - 1 != index and'],
    watch=[('index', 'index', 'yellow'), 'tmp', ('nums', 'nums', 'cyan')],
    captions={
        3: lambda S, B, ret: (f'扫描 `index = {S.index}`，把这里的数尽量归位' if 'index' not in B or S.index != B.index else '归位结束'),
        4: _while_cap,
        'tmp = nums[index]': '拿出 `p = tmp = {tmp}`',
        'nums[index] = nums[tmp - 1]': '位置 `{tmp - 1}` 上的 `{nums[index]}` 换到当前位置 `{index}`',
        'nums[tmp - 1] = tmp': '`{tmp}` 归位到 `nums[{tmp - 1}]`：==每次交换都使一个数归位==',
        10: lambda S, B, ret: (f'扫描 `0..n−1`：看 `index = {S.index}`' if S.index != B.index else '扫描完毕'),
        11: _if_cap,
        'return index + 1': '缺失的最小正数是 =={ret}==',
        'return len(nums) + 1': '`1..n` 全都有，答案是 `n + 1`',
    },
    cards=dict(
        one_liner='答案一定在 1 到 n+1 之间：把 1..n 的数换回 nums[p−1]，再找第一个不对的位置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找出未排序整数数组中==没有出现的最小正整数==',
                 '要求时间 `O(n)`，只用常数额外空间',
                 '示例：`[3,4,-1,1]` → `2`；`[7,8,9,11,12]` → `1`',
                 '演示用 `[3,4,-1,1,1]` → `2`（含重复的 1）'],
        quote='由此可得答案一定是出现在1到n + 1之间的……因此我们实际上只要考察nums中的1到n，对于负数或大于n的数都无需考虑。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想哈希数组 `hash[x] = x + 1`：把 `1..n` 填进去，再扫一遍找第一个缺的',
              '要常数空间 → ==把哈希覆盖到 nums 上==：`p` 在 `1..n` 且不在位置 `p−1`，就和 `nums[p−1]` 交换',
              '前提是 `nums[p−1] ≠ p`：有多个 `p` 且某个已归位时，==就不应该继续移动 p 了=='],
        summary=['看上去是平方复杂度，但每次交换都让一个数归位，最多 `n − 1` 次 → `O(n)`',
                 '`nums[nums[index] - 1] != nums[index]` 防止重复元素来回交换、死循环',
                 '先用 `tmp` 存住 `p`，再两步赋值完成交换（不会被改乱下标）',
                 '原文 while 条件写在一行，这里只用 `\\` 折成两行显示，逻辑不变',
                 '原文代码可直接在 Python 3 运行，只删去了 docstring'],
    ),
)
