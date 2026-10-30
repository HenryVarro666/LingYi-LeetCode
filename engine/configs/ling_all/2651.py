CONFIG = dict(
    num=2651, title='计算列车到站时间', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='取模', tags=[],
    code='''
class Solution:
    def findDelayedArrivalTime(self, arrivalTime: int, delayedTime: int) -> int:
        return (arrivalTime + delayedTime) % 24
''',
    call='Solution().findDelayedArrivalTime(13, 11)',
    expect=0,
    views=[
        dict(type='text', size=40, fn=lambda S: f"`({S['arrivalTime']} + {S['delayedTime']}) % 24` = `{S['arrivalTime'] + S['delayedTime']} % 24` = =={(S['arrivalTime'] + S['delayedTime']) % 24}==" if 'arrivalTime' in S else ''),
        dict(type='text', size=30, fn=lambda S: f"正点 {S['arrivalTime']}:00，延误 {S['delayedTime']} 小时，实际到站 =={(S['arrivalTime'] + S['delayedTime']) % 24}==:00" if 'arrivalTime' in S else ''),
    ],
    watch=['arrivalTime', 'delayedTime'],
    captions={
        'return': '先相加得 `{arrivalTime + delayedTime}`，再 `% 24` 回到 24 小时制：==24 点就是 0 点==，返回 `{ret}`',
    },
    cards=dict(
        one_liner='相加后对 24 取模，时间绕一圈回到 0 点',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`arrivalTime` 是正点到站的小时，`delayedTime` 是延误的小时数',
                 '24 小时制，求实际到站的小时',
                 '示例：`13, 11` → `0`（13+11=24 即 00:00）'],
        quote='`return (arrivalTime + delayedTime) % 24`',
        quote_src='—— 灵茶山艾府题解（一行代码）',
        idea=['时间是循环的：每过 24 小时回到原点',
              '总和不小于 24 时，取模把多出来的整天去掉'],
        after=[dict(heading='另一个例子', lines=['`15 + 5 = 20`，不到 24，`% 24` 不变 → `20`','`13 + 11 = 24`，`% 24` → `0`','时间每满 24 小时就回到起点，取模正好表达这个“绕圈”','`delayedTime` 最大 24，所以和最大 `46`，最多绕一圈'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：和恰好为 24 时答案是 `0`，不是 `24`',
                 '同类思路：环形、循环下标都用取模'],
    ),
)
