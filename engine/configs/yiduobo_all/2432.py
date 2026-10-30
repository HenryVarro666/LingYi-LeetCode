LOGS = [[1, 1], [3, 7], [2, 12], [7, 17], [0, 22]]


def _tl(S):
    lg = S['logs']
    return [lg[0][1]] + [lg[k][1] - lg[k - 1][1] for k in range(1, len(lg))]


CONFIG = dict(
    num=2432, title='处理用时最长的那个任务的员工', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 + 打擂台',
    tags=[],
    code='''
class Solution(object):
    def hardestWorker(self, n, logs):

        res, ma = logs[0]
        for index in range(1, len(logs)):
            if logs[index][1] - logs[index - 1][1] > ma:
                ma = logs[index][1] - logs[index - 1][1]
                res = logs[index][0]
            elif logs[index][1] - logs[index - 1][1] == ma and logs[index][0] < res:
                res = logs[index][0]
        
        return res
''',
    call=f'Solution().hardestWorker(26, {LOGS})',
    expect=3,
    views=[
        dict(type='array', var='logs', label='logs = [员工 id, 结束时刻]', cell=125, h=230,
             pointers={'index': 'blue'}),
        dict(type='text', size=30, fn=lambda S: ('各任务用时：' + '  '.join(f'{x}' for x in _tl(S))) if 'logs' in S else ''),
        dict(type='text', size=32, fn=lambda S: f"目前最久：员工 =={S['res']}==，用时 =={S['ma']}==" if 'res' in S and 'ma' in S else ''),
    ],
    watch=['index', ('res', 'res', 'green'), ('ma', 'ma', 'green')],
    captions={
        'res, ma = logs[0]': '第一个任务的用时就是 `leaveTime[0]` → 员工 `{res}`，用时 `{ma}`',
        'for index in range': lambda S, B, r: ('所有任务都扫完了' if B.index == S.index and S.index == len(S.logs) - 1 else '`index = {}`：用时 = `leaveTime[{}] − leaveTime[{}]` = {}'.format(S.index, S.index, S.index - 1, S.logs[S.index][1] - S.logs[S.index - 1][1])),
        6: lambda S, B, r: (lambda d: f'任务 {S.index} 用时 `{d}`，比 `ma = {S.ma}` {"更长 → 更新员工和用时" if d > S.ma else "不长 → 看是否并列"}')(S.logs[S.index][1] - S.logs[S.index - 1][1]),
        7: '最长用时更新为 `{ma}`',
        8: '答案换成这个任务的员工 `{res}`',
        9: lambda S, B, r: (lambda d: (f'用时 `{d}` = `ma`，员工 `{S.logs[S.index][0]}` < 当前答案 `{S.res}` → ==并列取小 id==' if d == S.ma and S.logs[S.index][0] < S.res
                                            else f'用时 `{d}` 与 `ma = {S.ma}` 并列且 id 不更小，或更短 → 不更新'))(S.logs[S.index][1] - S.logs[S.index - 1][1]),
        10: '并列且 id 更小 → 答案换成 `{res}`',
        'return res': '用时最长的任务属于员工 =={ret}==',
    },
    cards=dict(
        one_liner='一趟遍历算每个任务用时，并列时取 id 小的',
        complexity='时间 `O(m)`，空间 `O(1)`',
        problem=['`logs[i] = [id, leaveTime]`，任务首尾相接，第 0 个从时刻 0 开始', '返回用时最长任务的员工 id，并列取最小 id',
                 '本视频：`[[1,1],[3,7],[2,12],[7,17],[0,22]]` → `3`'],
        quote='第一个任务的用时就是leaveTime[0]，而后续第i个任务的用时则是leaveTime[i] - leaveTime[i - 1]',
        quote_src='—— yiduobo 题解原文',
        idea=['只需要一趟遍历，算每个任务的用时', '用时更长就换成这个员工；用时相同取 id 更小的', '第一个任务直接作为初始答案'],
        summary=['时间 `O(m)`，空间 `O(1)`',
                 '第一个任务用时是 `logs[0][1]`，不用减',
                 '用时相同时才比较 id，所以有 `elif`',
                 '原文是 Python 2 风格，但这段代码在 Python 3 下无需改动'],
    ),
)
