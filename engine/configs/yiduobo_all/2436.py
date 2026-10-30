CONFIG = dict(
    num=2436, title='使子数组最大公约数大于一的最小分割数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='贪心 · 尽量延长当前段',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def minimumSplits(self, nums):

        res = 1
        now = nums[0]

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        for num in nums[1:]:
            g = gcd(num, now)
            if g == 1:
                res += 1
                now = num
            else:
                now = g
        
        return res
''',
    call='Solution().minimumSplits([12,6,3,14,8])',
    expect=2,
    skip=['def gcd', 'while y', 'x, y = y, x % y', 'return x'],
    views=[
        dict(type='array', var='nums', label='nums（蓝格 = 当前数 num）', h=240, cell=110,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] else None),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"当前段的公约数 `now` = =={S['now']}==，分割段数 `res` = =={S['res']}==" if 'now' in S else '')),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'cyan'), ('num', 'num', 'blue'), 'g'],
    captions={
        'res = 1': '至少有一段，`res` 从 1 开始',
        'now = nums[0]': '`now`：当前这一段所有数的最大公约数，先放进 `nums[0]` = {now}',
        'def gcd': '辗转相除求最大公约数',
        'for num in nums[1:]': lambda S, B, r: ('没有更多数了，循环结束' if 'num' in B and B.num == S.num else f'看下一个数 `num` = {S.num}，尝试放进当前段'),
        'g = gcd(num, now)': '`gcd({num}, {now})` = =={g}==：放进当前段后，整段的最大公约数会变成它',
        'if g == 1': lambda S, B, r: (f'`g = {S.g}`，等于 1 → ==放进去就不合法了==，只能另起新段' if S.g == 1
                                      else f'`g = {S.g}`，大于 1 → 还合法，==尽量加进当前段=='),
        'res += 1': '另起一段：`res` → {res}',
        'now = num': '新段只有它自己，`now` = {now}',
        'now = g': '当前段公约数缩小为 `{now}`',
        'return res': '最少分成 `{res}` 段',
    },
    cards=dict(
        one_liner='能加进当前段就加，实在加不了才另起一段',
        complexity='时间 `O(n log C)`，空间 `O(1)`',
        problem=['把 `nums` 分成若干连续子数组，要求每段的==最大公约数 > 1==',
                 '求最少要分成几段',
                 '示例：`[12,6,3,14,8]` → `[12,6,3]` + `[14,8]`，共 `2` 段'],
        quote='对于每个数都尽量将其加入到当前的子数组中，若无法加入，那么就另起一个新的子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['往一段里添数，公约数只会越来越小，所以==越早放进去越省段数==',
              '`now` 记录当前段的公约数，新数 `num` 与它求 gcd',
              'gcd 为 1 就切开，新段以 `num` 开头；否则 `now` 变成这个 gcd'],
        summary=['时间 `O(n log C)`，空间 `O(1)`',
                 '`now` 存的是整段的 gcd，不用保存整段元素',
                 '另起新段时 `now = num`，不是 `g`',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行'],
    ),
)
