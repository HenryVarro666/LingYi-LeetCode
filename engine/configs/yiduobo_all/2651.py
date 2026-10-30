CONFIG = dict(
    num=2651, title='计算列车到站时间', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='相加再取模', tags=[],
    code='''
class Solution(object):
    def findDelayedArrivalTime(self, arrivalTime, delayedTime):

        return (arrivalTime + delayedTime) % 24
''',
    call='Solution().findDelayedArrivalTime(15, 5)',
    expect=20,
    views=[
        dict(type='text', size=40, fn=lambda S: f"`{S['arrivalTime']} + {S['delayedTime']}` = {S['arrivalTime'] + S['delayedTime']}，`% 24` → =={(S['arrivalTime'] + S['delayedTime']) % 24}==" if 'arrivalTime' in S else ''),
        dict(type='text', size=30, fn=lambda S: f"计划 {S['arrivalTime']} 点到，延误 {S['delayedTime']} 小时" if 'arrivalTime' in S else ''),
    ],
    watch=['arrivalTime', 'delayedTime'],
    captions={
        'return': '计划到站时间加上延误时间 `{arrivalTime} + {delayedTime}` = {arrivalTime + delayedTime}，对 24 取模，实际到站 =={ret}== 点',
    },
    cards=dict(
        one_liner='计划时间加延误时间，再对 24 取模',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给出正点到站时间 `arrivalTime` 和延误小时数 `delayedTime`',
                 '按 24 小时制返回实际到站时间',
                 '示例：`15, 5` → `20`；`13, 11` → `0`'],
        quote='比较基础的题目，计划到站的时间加上延误的时间，再对24取模即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个时间直接相加就是“不考虑绕圈”的到站时刻',
              '超过 24 就进入第二天，取模后正好是当天的钟点'],
        after=[dict(heading='两个例子对照', lines=['`15 + 5 = 20` → 还在当天，答案 `20`','`13 + 11 = 24` → 刚好午夜，`24 % 24 = 0`','取模前的数可以超过 24，取模后一定落在 `0~23`','提示里 `arrivalTime < 24`，不会有额外的整天'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：结果为 24 时要变成 `0`，取模自动做到',
                 '原文为 Python 2 风格，只是 `class Solution(object)` 写法，无需修改'],
    ),
)
