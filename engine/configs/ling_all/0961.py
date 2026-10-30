CONFIG = dict(
    num=961, title='在长度 2N 的数组中找出重复 N 次的元素', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='摩尔投票',
    tags=['随机算法', '摩尔投票法', '难度分 1162'],
    code='''
class Solution:
    def repeatedNTimes(self, nums: List[int]) -> int:
        ans = hp = 0
        for x in nums[1:]:  # 也可以写 for i in range(1, len(nums)) 避免切片
            if x == nums[0]:
                return x
            if hp == 0:  # x 是初始擂主，生命值为 1
                ans, hp = x, 1
            else:  # 比武，同门加血，否则扣血
                hp += 1 if x == ans else -1
        return ans
''',
    call='Solution().repeatedNTimes([1,5,2,5,3,5,4,5])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 当前擂主 ans 的值）', h=190, cell=90,
             color=lambda S, i, v: ('green' if 'ans' in S and v == S['ans'] and S['hp'] > 0 else None)),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"擂主 ==`{S['ans']}`==，生命值 ==`{S['hp']}`==" if 'hp' in S else ''),
    ],
    watch=['x', ('ans 擂主', 'ans', 'green'), ('hp 生命值', 'hp', 'yellow')],
    captions={
        'ans = hp = 0': '擂主 `ans` 还没有，生命值 `hp = 0`',
        'for x in nums[1:]': '跳过 `nums[0]`，逐个取 `x = {x}`',
        'if x == nums[0]': lambda S, B, r: (f'`x = {S.x}` 和 `nums[0] = {S.nums[0]}` 相等 → 重复元素找到了，直接返回' if S.x == S.nums[0] else f'`x = {S.x}` 不等于 `nums[0] = {S.nums[0]}`：`nums[0]` 不是答案的话，继续投票'),
        'if hp == 0': lambda S, B, r: (f'`hp = {S.hp}`：擂台空了，`x` 上台' if S.hp == 0 else f'`hp = {S.hp} > 0`：擂台有人，要比武'),
        'ans, hp = x, 1': '`x = {x}` 成为擂主，`ans = {ans}`，生命值 `hp = {hp}`',
        'hp += 1': lambda S, B, r: (f'`x = {S.x}` 和擂主 `{S.ans}` 同门 → 加血，`hp` = {S.hp}' if S.x == S.ans else f'`x = {S.x}` 与擂主 `{S.ans}` 不同 → 扣血，`hp` = {S.hp}'),
        'return ans': '`nums[0]` 之外 `{ans}` 是绝对众数，返回 `{ret}`',
    },
    cards=dict(
        one_liner='去掉 nums[0] 后，答案变成绝对众数，摩尔投票一遍扫完',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['长为 `2n` 的数组有 `n+1` 个不同元素，其中一个恰好出现 `n` 次，其余各一次',
                 '找出重复了 `n` 次的元素',
                 '本视频：`[1,5,2,5,3,5,4,5]` → `5`'],
        quote='如果 nums[0] 在下标 [1,n-1] 中出现过，那么返回 nums[0]。否则，去掉 nums[0]，剩下 2n-1 个数，出现次数为 n 的那个数变成绝对众数，可以用 169 题的算法解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['若 `nums[0]` 就是答案，它一定在后面再出现，遇到相等就直接返回',
              '否则去掉 `nums[0]` 后，答案占 `n` 个、总数 `2n-1`，==超过一半==，成了绝对众数',
              '摩尔投票的擂台：同门加血，否则扣血，血空了换人，最后留下的擂主就是众数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：要从下标 1 开始循环，并先判断 `x == nums[0]`，不能把 `nums[0]` 也交给投票',
                 '另外三种写法：哈希集合 `O(n)` 空间；检查相邻 3 个元素（`n≥3` 时必有间距 ≤ 2）；随机选两个下标，期望 `O(1)`'],
    ),
)
