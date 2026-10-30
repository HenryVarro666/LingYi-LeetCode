CONFIG = dict(
    num=3683, title='完成一个任务的最早时间', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='遍历取最小',
    code='''
class Solution:
    def earliestTime(self, tasks: List[List[int]]) -> int:
        return min(s + t for s, t in tasks)
''',
    call='Solution().earliestTime([[1,6],[2,3],[4,9],[3,5]])',
    expect=5,
    views=[
        dict(type='table', var='tasks', rows=['任务0', '任务1', '任务2', '任务3'], cols=['开始 s', '耗时 t'], h=260),
        dict(type='text', fn=lambda S: '完成时间 = s + t：' + '，'.join(f'{a}+{b}={a+b}' for a, b in S['tasks']) + '；取最小', size=28, h=80),
    ],
    watch=[],
    captions={
        'return': '每个任务完成时间是 `s + t`：`{[a+b for a, b in tasks]}`，取最小 → =={ret}==（最早完成的任务在这一时刻结束）',
    },
    cards=dict(
        one_liner='每个任务完成时间 s+t，取最小值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`tasks[i] = [s, t]`：任务在 `s` 时刻开始，需要 `t` 个时间单位', '求至少完成一个任务的最早时间',
                 '示例：`[[1,6],[2,3]]` → `5`'],
        quote='根据题意，答案为 s_i + t_i 的最小值。遍历 tasks 即可算出。',
        quote_src='—— 灵茶山艾府题解',
        idea=['任务 i 的完成时间就是 `s + t`', '只要完成一个，所以取所有完成时间的最小值'],
        after=[dict(heading='走一遍示例', lines=['`tasks = [[1,6],[2,3],[4,9],[3,5]]`', '完成时间：`7, 5, 13, 8`', '最小的是 `5`：第二个任务最早结束', '开始晚、耗时短的任务可能更早完成，所以要逐个比较'])],
        before=[dict(heading='为什么取最小', lines=['任务各自独立，互不影响', '完成时间 = 开始时间 + 耗时', '所以全部算出来，最小的就是最早的'])],
        summary=['时间 `O(n)`，空间 `O(1)`', '写法二：`min(map(sum, tasks))`，每个任务 `[s, t]` 求和',
                 '易错点：答案是 s+t 的最小值，不是 t 的最小值'],
    ),
)
