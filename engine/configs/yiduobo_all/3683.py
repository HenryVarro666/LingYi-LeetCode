CONFIG = dict(
    num=3683, title='完成一个任务的最早时间', difficulty='Easy', category='模拟',
    author='yiduobo', technique='列表推导取最小',
    code='''
class Solution(object):
    def earliestTime(self, tasks):
        
        return min([s + t for s, t in tasks])
''',
    call='Solution().earliestTime([[3,4],[2,3],[5,1]])',
    expect=5,
    views=[
        dict(type='table', var='tasks', rows=['任务0', '任务1', '任务2'], cols=['s 开始', 't 耗时'], h=220),
        dict(type='text', fn=lambda S: '各任务 s + t：' + '，'.join(f'{a+b}' for a, b in S['tasks']) + '，取最小', size=28, h=80),
    ],
    watch=[],
    captions={
        'return': '先算每个任务的 `s + t` = `{[s + t for s, t in tasks]}`，只需完成一个，取最小 → =={ret}==',
    },
    cards=dict(
        one_liner='只要完成一个任务，就取所有 s+t 的最小值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`tasks[index] = [s, t]`：任务在时刻 `s` 开始，要执行 `t` 个时间单位',
                 '求完成至少一个任务的最早时间', '示例：`[[3,4],[2,3],[5,1]]` → `5`'],
        quote='完成至少一个任务的最早时间，也就是说只需要完成一个任务就行了。于是一趟遍历，计算数组中每一组s与t之和，取其中的最小值即可。',
        quote_src='—— yiduobo 题解',
        idea=['每组 `s + t` 就是该任务完成的时刻', '多个任务并行，最早的那个就是答案'],
        after=[dict(heading='走一遍示例', lines=['`tasks = [[3,4],[2,3],[5,1]]`', '完成时间：`7, 5, 6`', '最小的是 `5`：第二个任务最早结束', '并行执行、耗时短的任务可能更早完成，所以要逐个比较'])],
        before=[dict(heading='为什么取最小', lines=['任务各自独立，互不影响', '完成时间 = 开始时间 + 耗时', '所以全部算出来，最小的就是最早的'])],
        summary=['时间 `O(n)`，空间 `O(n)`（列表推导临时列表）', '易错点：是 s+t 的最小值',
                 '原文为 Python 2 写法，本题无需改动'],
    ),
)
