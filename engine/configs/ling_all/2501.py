NUMS = [4, 3, 6, 16, 2, 256]


def _col(S, i, v):
    x, cnt = S.get('x'), S.get('cnt')
    if x is None or cnt is None:
        return None
    if v == x:
        return 'blue'
    if any(v ** (2 ** j) == x for j in range(1, cnt + 1)):
        return 'green'
    return None


def _txt(S):
    if 'cnt' not in S or 'x' not in S:
        return '从每个数出发不断平方：`x → x×x`，只要还在集合里就继续'
    x, cnt = S['x'], S['cnt']
    if x in S['s']:
        return f'`x = {x}` 在集合里 → 方波长度 `cnt = {cnt}`，下一项 `x×x = {x * x}`'
    return f'`x = {x}` 不在集合里 → 链条结束，长度 `cnt = {cnt}`，`ans = {S["ans"]}`'


CONFIG = dict(
    num=2501, title='数组中最长的方波', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='暴力枚举起点 · 哈希集合 + 不断平方',
    tags=['灵神题单', '动态规划', '难度分 1480'],
    code='''
class Solution:
    def longestSquareStreak(self, nums: List[int]) -> int:
        ans, s = 0, set(nums)
        for x in s:
            cnt = 0
            while x in s:
                cnt += 1
                x *= x
            ans = max(ans, cnt)
        return ans if ans > 1 else -1
''',
    call=f'Solution().longestSquareStreak({NUMS!r})',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前 x，绿 = 已走过的链条）', h=190, cell=100, color=_col),
        dict(type='set', var='s', label='s = set(nums)', fmt=lambda x: str(x), h=170, font=30),
        dict(type='text', fn=_txt, size=26, h=90),
    ],
    watch=[('x', 'x', 'blue'), ('cnt', 'cnt', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans, s = 0, set(nums)': '`s` 是 `nums` 的集合，用来 `O(1)` 判断“某个数在不在数组里”；`ans = 0`',
        'for x in s': lambda S, B, r: (f'枚举方波的起点 `x = {S.x}`（每个数都试一遍）' if S.x in S.s else '所有起点都试过了'),
        'cnt = 0': '从这个起点重新数长度：`cnt = 0`',
        'while x in s': lambda S, B, r: (f'`{S.x}` 在集合里 → ==还能接上==，继续' if S.x in S.s
                                         else f'`{S.x}` 不在集合里 → 链条断了'),
        'cnt += 1': '又接上一项：`cnt = {cnt}`',
        'x *= x': lambda S, B, r: (f'下一项必须是平方：`x = {S.x}`。数字至少 2，平方几次就会超过 10^5，所以==循环很短==' if S.cnt == 1 else f'再平方：`x = {S.x}`'),
        'ans = max': '`ans = max({B.ans}, {cnt}) = {ans}`',
        'return ans': lambda S, B, r: (f'最长链长度 `{S.ans}`，大于 1 → 返回 =={r}==' if S.ans > 1 else '最长只有 1，不是方波 → 返回 ==-1=='),
    },
    max_steps=70,
    cards=dict(
        one_liner='枚举起点，不断平方，最多只会平方 log log U 次',
        complexity='时间 `O(n log log U)`，空间 `O(n)`',
        problem=['选出子序列，排序后除第一个外每个数都是前一个的==平方==，长度至少为 2',
                 '求最长方波的长度，没有则返回 `-1`',
                 '示例：`[4,3,6,16,8,2]` → `3`；本视频：`[4,3,6,16,2,256]` → `4`'],
        quote='由于数组元素至少为 2，平方 k 次后，元素至少为 2^(2^(k-1))。因此只要暴力枚举初始项，不断平方即可，至多循环 log log U 次。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['排序后的子序列由起点唯一确定：`x, x², x⁴, …`，所以==只枚举起点==',
              '子序列不要求连续，只要数在数组里即可 → 用集合判断',
              '数字增长极快（双指数），每个起点只循环很少几次'],
        summary=['时间 `O(n log log U)`，空间 `O(n)`',
                 '易错：长度为 1 不算方波，最后 `ans > 1` 才返回，否则 `-1`',
                 '`for x in s` 遍历集合，循环里改了 `x` 不影响下一个起点',
                 '方法二：`@cache` 记忆化 `dfs(x) = 1 + dfs(x*x)`，复杂度 `O(n)`，本视频演示方法一'],
    ),
)
