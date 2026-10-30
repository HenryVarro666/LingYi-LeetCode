def _cur(S):
    nums, ans = S['nums'], S.get('ans', [])
    cum = 0
    for i in range(len(nums) - 1, -1, -1):
        cum += len(str(nums[i]))
        if cum > len(ans):
            return i
    return -1


CONFIG = dict(
    num=2553, title='分割数组中数字的数位', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='从右到左取数位 · 最后反转',
    tags=[],
    code='''
class Solution:
    def separateDigits(self, nums: list[int]) -> list[int]:
        ans = []
        for x in reversed(nums):
            while x > 0:
                ans.append(x % 10)
                x //= 10
        ans.reverse()
        return ans
''',
    call='Solution().separateDigits([13, 25, 83, 77])',
    expect=[1, 3, 2, 5, 8, 3, 7, 7],
    views=[
        dict(type='array', var='nums', label='nums（从右往左逐个拆）', h=220,
             color=lambda S, i, v: 'blue' if i == _cur(S) else None,
             dim=lambda S, i, v: i > _cur(S)),
        dict(type='array', var='ans', label='ans（先低位后高位，最后整体反转）', h=240,
             color=lambda S, i, v: 'green' if i == len(S['ans']) - 1 and S['_line'] == 6 else None),
    ],
    watch=[('x', 'x', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = []': '`ans` 准备存放数位',
        'for x in reversed': '从右往左取：当前数 `x = {x}`',
        'while x > 0': lambda S, B, r: (f'`x = {S.x} > 0`，还有数位，继续' if S.x > 0 else '`x = 0`，这个数拆完了，换前一个数'),
        'ans.append': '`x % 10 = {x % 10}` 是 {x} 的最低位，放入 `ans` → `{ans}`',
        'x //= 10': '`x //= 10` 去掉最低位，`x` 变成 `{x}`',
        'ans.reverse()': '每个数是低位在前、数从右往左：整体==反转==一次，正好得到题目要的顺序 → `{ans}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='从右往左、从低到高拆数位，最后整体反转',
        complexity='时间 `O(n log U)`，空间 `O(1)`（不计返回值）',
        problem=['把每个数按数位拆开，按原来的顺序放进答案',
                 '例如 `10921` 拆成 `[1,0,9,2,1]`',
                 '示例：`[13,25,83,77]` → `[1,3,2,5,8,3,7,7]`'],
        quote='我们可以从右到左遍历 nums，从低到高遍历 nums[i] 的数位。最后把遍历过的数位反转，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x % 10` 取最低位，`x //= 10` 去掉它，直到 `x` 为 0',
              '这样每个数的数位是==从低到高==，和题目要求相反',
              '数组也从右往左遍历，两次倒序叠加，最后反转一次就对了'],
        summary=['时间 `O(n log U)`，`U = max(nums)`；空间 `O(1)`',
                 '易错：从左往右遍历再整体反转会让数字内部顺序出错',
                 '写法一：`[int(ch) for x in nums for ch in str(x)]`，一行搞定，本视频演示写法二'],
    ),
)
