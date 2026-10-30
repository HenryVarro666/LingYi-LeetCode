LOGS = [[1, 1], [3, 7], [2, 12], [7, 17], [0, 22]]


def _tl(S):
    lg = S['logs']
    return [lg[0][1]] + [lg[k][1] - lg[k - 1][1] for k in range(1, len(lg))]


def _same(B, S):
    try:
        return B.t1 == S.t1
    except Exception:
        return False


CONFIG = dict(
    num=2432, title='处理用时最长的那个任务的员工', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='相邻作差 + 打擂台',
    tags=[],
    code='''
class Solution:
    def hardestWorker(self, _: int, logs: List[List[int]]) -> int:
        ans, max_t = logs[0]
        for (_, t1), (i, t) in pairwise(logs):
            t -= t1
            if t > max_t or t == max_t and i < ans:
                ans, max_t = i, t
        return ans
''',
    call=f'Solution().hardestWorker(26, {LOGS})',
    expect=3,
    views=[
        dict(type='array', var='logs', label='logs = [员工 id, 结束时刻]', cell=125, h=230),
        dict(type='text', size=30, fn=lambda S: ('各任务用时：' + '  '.join(f'{x}' for x in _tl(S))) if 'logs' in S else ''),
        dict(type='text', size=32, fn=lambda S: f"目前最久：员工 =={S['ans']}==，用时 =={S['max_t']}==" if 'ans' in S and 'max_t' in S else ''),
    ],
    watch=['t1', 't', ('ans', 'ans', 'green'), ('max_t', 'max_t', 'green')],
    captions={
        'ans, max_t = logs[0]': '第 0 个任务从 0 时刻开始，用时就是 `logs[0][1]` → 员工 `{ans}`，用时 `{max_t}`',
        'for (_, t1)': lambda S, B, r: ('相邻任务都比较完了，循环结束' if _same(B, S) else f'`pairwise` 取相邻两个任务：上一个结束于 `{S.t1}`，当前由员工 `{S.i}` 做，结束于 `{S.t}`'),
        't -= t1': '当前任务用时 = 结束时刻 − 上个任务结束时刻 = `{B.t} − {t1}` = =={t}==',
        'if t > max_t': lambda S, B, r: (f'用时 `{S.t}` > 最大 `{S.max_t}` → 更新' if S.t > S.max_t
                                         else (f'用时 `{S.t}` = 最大 `{S.max_t}`，员工 `{S.i}` < `{S.ans}` → ==并列取小 id==，更新' if S.t == S.max_t and S.i < S.ans
                                               else (f'用时 `{S.t}` = 最大 `{S.max_t}`，但 id `{S.i}` ≥ `{S.ans}` → 不更新' if S.t == S.max_t
                                                     else f'用时 `{S.t}` < 最大 `{S.max_t}` → 不更新'))),
        'ans, max_t = i, t': '更新答案：员工 `{ans}`，用时 `{max_t}`',
        'return ans': '用时最长的任务属于员工 =={ret}==',
    },
    cards=dict(
        one_liner='用时是相邻结束时刻之差，边扫边打擂台，并列取小 id',
        complexity='时间 `O(m)`，空间 `O(1)`',
        problem=['`logs[i] = [id, leaveTime]`：员工 `id` 在 `leaveTime` 完成任务，任务首尾相接，第 0 个从 0 开始',
                 '返回用时最长任务的员工 id；并列取 ==最小== id',
                 '本视频：`[[1,1],[3,7],[2,12],[7,17],[0,22]]` → `3`'],
        quote='第 0 位员工的用时为 logs[0][1]；第 i（i>0）位员工的用时为 logs[i][1] - logs[i-1][1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['阅读理解：任务连着做，用时 = 本次结束 − 上次结束',
              '第 0 个任务直接拿 `logs[0]` 当初始答案',
              '`pairwise` 一次看相邻两项，比较时同时处理「更长」和「一样长但 id 更小」'],
        summary=['时间 `O(m)`，空间 `O(1)`',
                 '易错：第 0 个任务的用时是 `logs[0][1]`，不是差值',
                 '并列时取小 id：`t == max_t and i < ans`',
                 '`and` 优先级高于 `or`，条件不用加括号',
                 '本视频示例里 5 个任务用时 1,6,5,5,5，最长的是员工 3'],
    ),
)
