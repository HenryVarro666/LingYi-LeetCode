def _txt(S):
    if 'idx' not in S:
        return ''
    t = f"当前答案：按钮 `idx = {S['idx']}`，最长按压 `max_diff = {S['max_diff']}`"
    if 'd' in S and 't1' in S:
        t += f"　|　本次：`{S['t2']} − {S['t1']}` = {S['d']}（按钮 {S['i']}）"
    return t


def _row(S, i, j, v):
    if 'i' in S and 't2' in S and 't1' in S:
        ev = S['events']
        for k in range(1, len(ev)):
            if ev[k][0] == S['i'] and ev[k][1] == S['t2'] and ev[k - 1][1] == S['t1']:
                if i == k:
                    return 'blue'
                if i == k - 1:
                    return 'cyan'
    return None


CONFIG = dict(
    num=3386, title='按下时间最长的按钮', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='遍历 · 维护最大时间差',
    tags=[],
    code='''
class Solution:
    def buttonWithLongestTime(self, events: List[List[int]]) -> int:
        idx, max_diff = events[0]
        for (_, t1), (i, t2) in pairwise(events):
            d = t2 - t1
            if d > max_diff or d == max_diff and i < idx:
                idx, max_diff = i, d
        return idx
''',
    call='Solution().buttonWithLongestTime([[1,2],[2,5],[3,9],[1,15]])',
    expect=1,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='grid', var='events', label='events = [按钮下标, 时间]（青 = 上一次，蓝 = 这一次）', h=380, color=_row,
             rows=lambda S: [f'事件{k}' for k in range(len(S['events']))], cols=['idx', 'time']),
    ],
    watch=[('idx', 'idx', 'green'), ('max_diff', 'max_diff', 'orange'), 'd', ('t1', 't1', 'cyan'), ('t2', 't2', 'blue')],
    captions={
        'idx, max_diff = events[0]': '第一个按钮的按压时间就是它的时间戳：`idx = {idx}`，`max_diff = {max_diff}`，先当作答案',
        'for (_, t1)': lambda S, B, r: ('相邻事件都看完了，循环结束' if 't2' in B and B.get('t2') == S.t2 and B.get('t1') == S.t1
                                         else f'取相邻两个事件：上一次时间 `t1 = {S.t1}`，这次按下按钮 `i = {S.i}`、时间 `t2 = {S.t2}`'),
        'd = t2 - t1': '按钮 `{i}` 的按压时间 = 这次时间 − 上次时间 = `{t2} − {t1}` = =={d}==',
        'if d > max_diff': lambda S, B, r: (
            f'`{S.d} > {S.max_diff}` → ==更长==，更新答案' if S.d > S.max_diff
            else f'`{S.d} == {S.max_diff}` 且 `{S.i} < {S.idx}` → ==一样长但下标更小==，更新答案' if S.d == S.max_diff and S.i < S.idx
            else f'`d = {S.d}`：没有更长（相等时下标 {S.i} 也不比 {S.idx} 小）→ 不更新'),
        'idx, max_diff = i, d': '更新答案：`idx = {idx}`，`max_diff = {max_diff}`',
        'return idx': '遍历完，按压最久的按钮是 `{idx}`',
    },
    cards=dict(
        one_liner='遍历相邻事件，维护最大时间差和对应按钮',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`events[i] = [按钮下标, 按下时间]`，按时间递增',
                 '按压时间 = 与前一次按下的时间差；第一个就是它的时间戳',
                 '求按压最久的按钮，并列取下标最小。示例 `[[1,2],[2,5],[3,9],[1,15]]` → `1`'],
        quote='遍历的过程中，维护答案 idx，以及最大时间差 maxDiff。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用第一个事件初始化：`idx, max_diff = events[0]`',
              '`pairwise` 取相邻两个事件，时间差就是后一个按钮的按压时间',
              '更长则更新；一样长则比下标，小的胜出'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：第一个按钮的按压时间是时间戳本身，不是 0',
                 '易错：并列时要比下标，`d == max_diff and i < idx`',
                 '`pairwise` 是 Python 3.10+ 的 itertools 函数，引擎已注入'],
    ),
)
