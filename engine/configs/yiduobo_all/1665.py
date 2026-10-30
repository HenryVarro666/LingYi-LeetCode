def _order(S):
    return sorted(S['tasks'], key=lambda d: d[1] - d[0], reverse=True)


def _cur(S):
    if 'actuail' in S and 'minimum' in S:
        o = _order(S)
        t = [S['actuail'], S['minimum']]
        return o.index(t) if t in o else None
    return None


def _txt(S):
    c = _cur(S)
    if 'now' not in S:
        return '按 `minimum − actual` 从大到小执行（下面是排好的顺序）'
    if c is None:
        return f'遍历结束：累计补充的能量 `res = {S["res"]}`'
    if S.get('_line') in (9, 11):
        return f'任务做完，剩余能量 `now = {S["now"]}`'
    if S['now'] < S['minimum']:
        return f'剩余 `now = {S["now"]}` < 门槛 `{S["minimum"]}` → 要补 =={S["minimum"] - S["now"]}== 点'
    return f'剩余 `now = {S["now"]}` ≥ 门槛 `{S["minimum"]}`，够用，不用补'


CONFIG = dict(
    num=1665, title='完成所有任务的最少初始能量', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='差值排序 · 不够就补',
    tags=['灵神题单', '贪心与思维', '难度分 1901'],
    code='''
class Solution(object):
    def minimumEffort(self, tasks):

        now = 0
        res = 0
        for actuail, minimum in sorted(tasks, key=lambda d:d[1] - d[0], reverse=True):
            if now < minimum:
                res += minimum - now
                now = minimum - actuail
            else:
                now -= actuail
        
        return res
''',
    call='Solution().minimumEffort([[1,2],[2,4],[4,8],[5,6]])',
    expect=13,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='sorted(tasks, key=lambda d:d[1] - d[0], reverse=True)', cell=150, h=230,
             label='排序后的 [actual, minimum]',
             color=lambda S, i, v: 'yellow' if _cur(S) == i else None,
             dim=lambda S, i, v: _cur(S) is not None and i < _cur(S)),
        dict(type='text', fn=lambda S: '`now` = 当前剩余能量，`res` = 已经额外补充的初始能量', h=70),
    ],
    watch=[('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now`：假设现在手里剩余的能量，一开始是 0',
        'res = 0': '`res`：为了凑够门槛，一共补了多少能量（即答案）',
        'for actuail': '按差值从大到小取下一个任务：花费 `{actuail}`，门槛 `{minimum}`',
        'if now < minimum': lambda S, B, r: (f'`now = {S.now} < minimum = {S.minimum}`：能量不够，需要补' if S.now < S.minimum
                                             else f'`now = {S.now} ≥ minimum = {S.minimum}`：能量足够，不用补'),
        'res += minimum - now': '把 `now` 补足到门槛：补 `{minimum} − {B.now} = {minimum - B.now}`，`res` = {res}',
        'now = minimum - actuail': '补足后剩 `{minimum}`，做完任务花掉 `{actuail}` → `now = {now}`',
        'now -= actuail': '够用，直接做任务：`now` 减去 `{actuail}` → {now}',
        'return res': '补的能量总和就是最少初始能量：`{res}`',
    },
    cards=dict(
        one_liner='先把任务按 minimum−actual 排好，不够就补，够了就扣',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个任务 `[actual, minimum]`：能量不低于 minimum 才能开始，做完扣掉 actual',
                 '顺序任意，求最少初始能量',
                 '示例：`[[1,2],[2,4],[4,8],[5,6]]` → `13`'],
        quote='观察上面的反例可以知道，如果使用二者差值作为贪心的标准，那么必然是按照差值从大到小执行。一时间想不出什么反例，说明这个贪心的规则可能是正确的，那么必须要给出证明。',
        quote_src='—— yiduobo 题解原文',
        idea=['先试单个指标：只按 minimum 或只按 actual 排序，都有反例',
              '再试差值 `minimum − actual`，找不到反例，用反证法证明',
              '一趟扫描：当前能量不够就补到门槛，补的部分累加进答案'],
        summary=['时间 `O(n log n)`，排序占主导',
                 '易错点：补足后剩余能量是 `minimum − actual`，不是 0',
                 '原文变量名 `actuail` 是笔误，保持原样',
                 '对比灵神：灵神求每个位置下界的最大值；yiduobo 边扫边补差额'],
    ),
)
