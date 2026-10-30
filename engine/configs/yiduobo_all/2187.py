TIME = [1, 2, 3]
TOT = 5
R0 = (1 + TOT // len(TIME)) * max(TIME)


def _color(S, i, v):
    if 'l' not in S or i == 0:
        return None
    if i < S['l']:
        return 'red'
    if i >= S['r']:
        return 'green'
    return None


def _t_color(S, i, v):
    if 't' in S and S['_line'] in (9, 10) and 'cnt' in S and S['time'].index(S['t']) == i:
        return 'yellow'
    return None


def _top(S):
    if 'cnt' in S and 'mid' in S and 8 <= S['_line'] <= 12:
        return f"时间 `mid = {S['mid']}` 内：累计完成 `cnt = {S['cnt']}` 趟（目标 `{TOT}`）"
    if 'r' in S:
        return f"答案在 `[l, r] = [{S['l']}, {S['r']}]` 里：红 = 不够，绿 = 已知够了"
    return '时间越长，完成的趟数越多 → ==二分最终答案=='


def _cmp(S, B, ret):
    if S.cnt >= S.totalTrips:
        return f'`cnt = {S.cnt} >= {S.totalTrips}`：时间 `{S.mid}` 够了 → 答案 `<= {S.mid}`，`r = mid`'
    return f'`cnt = {S.cnt} < {S.totalTrips}`：时间 `{S.mid}` 不够 → 答案在右边，`l = mid + 1`'


CONFIG = dict(
    num=2187, title='完成旅途的最少时间', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 平均分配定上界',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1641'],
    code='''
class Solution(object):
    def minimumTime(self, time, totalTrips):

        l = 1
        r = (1 + totalTrips // len(time)) * max(time)
        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            for t in time:
                cnt += mid // t
            
            if cnt >= totalTrips:
                r = mid
            else:
                l = mid + 1
        
        return l
''',
    call=f'Solution().minimumTime({TIME}, {TOT})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(R0 + 1)),
             label='候选时间（红 = 不够，绿 = 已知够了；0 不是候选）', cell=90, index=False, color=_color,
             dim=lambda S, i, v: i == 0,
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'}, h=240),
        dict(type='array', var='time', label='time（黄 = 正在累加的车）', cell=100, color=_t_color, h=180),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('t', 't'),
           ('cnt', 'cnt', 'green'), 'totalTrips'],
    captions={
        'l = 1': '时间至少为 1：`l = 1`',
        'r = (1 + totalTrips': '上界：每辆车分 `1 + {totalTrips} // {len(time)}` 趟、都按最慢的 `{max(time)}` 算 → `r = {r}` 一定够',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：还没确定 → 继续二分' if S.l < S.r
                                        else f'`l = r = {S.l}`：区间缩成一个数，就是答案'),
        'mid = (l + r) >> 1': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'cnt = 0': '统计 `{mid}` 时间内所有车完成的趟数',
        'cnt += mid // t': '一趟用时 `{t}` 的车：`{mid} // {t} = {mid // t}` 趟 → `cnt = {cnt}`',
        'if cnt >= totalTrips': _cmp,
        'r = mid': '`r` → {r}',
        'l = mid + 1': '`l` → {l}',
        'return l': '返回最少时间 =={ret}==',
    },
    cards=dict(
        one_liner='时间越长趟数越多：二分最终答案，看能否跑够',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['`time[i]` 是第 `i` 辆公交车跑一趟的用时，车可以连续跑、互相独立',
                 '求所有车==总共==完成至少 `totalTrips` 趟的最少时间',
                 '示例：`time = [1,2,3], totalTrips = 5` → `3`'],
        quote='时间越长，完成旅途的趟数就越多，反过来，时间越短，完成旅途的趟数就越少，因此在这里可以==二分最终的答案==',
        quote_src='—— yiduobo 题解原文',
        idea=['对二分到的 `mid`，每辆车完成 `mid // t` 趟，求和得 `cnt`',
              '`cnt >= totalTrips` 说明够了 → `r = mid`；否则 `l = mid + 1`',
              '上界：让每辆车都跑 `1 + totalTrips // n` 趟、按最慢的车算，一定够'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '上界 `(1 + totalTrips // n) × max(time)` 比 `min × totalTrips` 更紧时能少几次二分',
                 '`r = mid` 而不是 `mid − 1`：mid 可能就是答案',
                 '原文为 Python 2 写法，`totalTrips / len(time)` 和 `mid / t` 已改为 `//`',
                 '对比灵神：开区间写法，左端点 `min_t − 1`、右端点 `min_t × totalTrips`'],
    ),
)
