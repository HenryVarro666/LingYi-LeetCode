CONFIG = dict(
    num=1250, title='检查「好数组」', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='整体 gcd 是否为 1', tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def isGoodArray(self, nums):
        now = nums[0]
        for num in nums[1:]:
            while num:
                now, num = num, now % num
            if now == 1:
                break

        return now == 1
''',
    call='Solution().isGoodArray([6,10,15])',
    expect=True,
    views=[
        dict(type='array', var='nums', h=200, label='nums',
             color=lambda S, i, v: 'green' if S.get('now') == 1 else None),
        dict(type='text', h=90, fn=lambda S: f"当前公约数 `now` = =={S['now']}==" + ('，已经是 1，不用再看了' if S.get('now') == 1 else '') if 'now' in S else ''),
    ],
    watch=[('now', 'now', 'green'), ('num', 'num', 'blue')],
    captions={
        'now = nums[0]': '先把第一个数当作公约数：`now = {now}`',
        'for num in nums[1:]': '取下一个数 `num = {num}`，把它并入公约数',
        'while num': lambda S, B, r: (f'`num = {S.num}` 不为 0，继续辗转相除' if S.num else f'`num = 0`：辗转相除结束，`now = {S.now}` 就是前面所有数的最大公约数'),
        'now, num = num, now % num': '辗转相除：`now, num = {B.num}, {B.now} % {B.num}` → `now = {now}`，`num = {num}`',
        'if now == 1': lambda S, B, r: (f'`now = 1`：说明能选出互质的数，可以提前结束' if S.now == 1 else f'`now = {S.now}` 不是 1，继续看下一个数'),
        'break': '最大公约数已是 1，不会再变小，直接跳出',
        'return now == 1': '`now == 1` → =={ret}==：整体最大公约数为 1，必能凑出 1',
    },
    cards=dict(
        one_liner='能凑出 1 当且仅当整个数组的最大公约数是 1',
        complexity='时间 `O(n log C)`，空间 `O(1)`',
        problem=['给一个正整数数组，每个数可以乘上任意整数后相加（子集选取）',
                 '问能否凑出和为 `1`（好数组），返回 `True` / `False`',
                 '示例：`[6,10,15]` → `True`'],
        quote='于是我们可以求出数组中所有数中的最大公约数，若为1，说明必然可以选出一组互质的x和y，否则说明无解。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目等价于 `a*x + b*y = 1` 有整数解',
              '扩展欧几里得：有解的前提是 `x`、`y` 互质',
              '所以把数组所有数的 gcd 滚动求出来，看是不是 1'],
        summary=['时间 `O(n log C)`，空间 `O(1)`',
                 '`now` 在整个数组上持续保留，相当于滚动求 gcd',
                 '一旦 `now == 1` 可以提前 `break`',
                 '原文代码未改动（仅 Python 2/3 通用写法）',
                 '同类：裴蜀定理、2543 判断点是否可达'],
    ),
)
