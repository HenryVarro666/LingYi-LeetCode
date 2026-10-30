CONFIG = dict(
    num=1529, title='灯泡开关 IV', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='从左到右 · 只看当前灯泡与翻转奇偶',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def minFlips(self, target):
        now = 0
        res = 0
        for char in target:
            if now == int(char):
                continue
            else:
                res += 1
                now = 1 - now

        return res
''',
    call='Solution().minFlips("10111")',
    expect=3,
    views=[
        dict(type='text', size=34, fn=lambda S: (f"灯泡当前状态 `now = {S['now']}`" + (f"，目标 `{S['char']}`" if 'char' in S else '')) if 'now' in S else ''),
        dict(type='string', var='target', h=240, label='target（目标状态）'),
    ],
    watch=[('now', 'now', 'blue'), ('res', 'res', 'green'), 'char'],
    captions={
        'now = 0': '`now` 是当前位置灯泡被前面操作影响后的状态，一开始全是 0',
        'res = 0': '`res` 累计翻转次数',
        'for char in target': '处理目标 `{char}`，此时灯泡状态是 `{now}`',
        'if now == int(char)': lambda S, B, r: (f'`now = {S.now}` 等于目标 `{S.char}`：这个位置不用翻' if S.now == int(S.char) else f'`now = {S.now}` 不等于目标 `{S.char}`：必须从这里翻转'),
        'continue': '状态已对，直接看下一个',
        'res += 1': '从这里翻转后缀一次：`res` → {res}',
        'now = 1 - now': '后面所有灯泡的状态都被翻转：`now` → {now}',
        'return res': '一共翻转 `{res}` 次',
    },
    cards=dict(
        one_liner='先处理靠前的灯泡，只需记住当前翻转的奇偶',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['n 个灯泡一开始全灭（0），每次选下标 `i`，翻转 `i` 到末尾的所有灯泡',
                 '给定目标状态 `target`，求最少翻转次数',
                 '示例：`"10111"` → `3`'],
        quote='对于两个位置p和q，若p < q，对p进行的翻转也将影响到q，而对q进行的翻转则不会影响到p，也就是说应该优先处理掉靠前的灯泡。',
        quote_src='—— yiduobo 题解原文',
        idea=['后面的翻转碰不到前面，所以从左往右处理',
              '当前位置已被翻转 `k` 次，只需关心 `k` 的奇偶，即 `now`',
              '`now` 与目标不同就必须翻一次，同时 `now` 取反'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`target` 是字符串，要 `int(char)` 再比较',
                 '原文为 Python 2 风格，只删去了空行里的多余缩进，逻辑未改',
                 '同类题：3192 使二进制数组全部等于 1 的最少操作次数 II'],
    ),
)
