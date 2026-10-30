EVS = [[1, 3, 2], [4, 5, 6], [2, 4, 3], [6, 7, 4]]
TMAX = 8


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '活动（蓝 = 当前枚举的第一场，粉 = 可选的后一场，青 = f[p] 对应的最优）', 22, T['muted'], bold=True)
    lx, rx = x0 + 60, x1 - 40
    sc = (rx - lx) / TMAX
    top = y0 + 60
    n = len(EVS)
    rh = min(62, (y1 - top - 50) / n)
    start, end = S.get('start'), S.get('end')
    ev = S['events']
    cur = p = None
    inner = S.get('_inner', {})
    if 'index' in inner and S.get('_line', 0) >= 14 and end:
        cur = end[inner['index']]
        pp = S.get('p')
        if pp is not None and pp < n:
            p = start[pp]
    best = None
    if p is not None and S.get('f'):
        fp = S['f'][S['p']]
        for k in range(S['p'], n):
            if ev[start[k]][2] == fp:
                best = start[k]
                break
    for t in range(TMAX + 1):
        cv.line([(lx + t * sc, top - 8), (lx + t * sc, top + rh * n)], T['border'], 1)
        cv.text((lx + t * sc, top + rh * n + 6), t, 18, T['dim'], anchor='mt', mono=True)
    for k, e in enumerate(ev):
        s, en, v = e
        y = top + k * rh
        col = (90, 96, 108)
        if k == cur:
            col = T['blue']
        elif k == best:
            col = T['cyan']
        elif k == p:
            col = T['pink']
        cv.rect((lx + s * sc, y + 6, lx + (en + 1) * sc, y + rh - 6), fill=col, r=6)
        cv.text(((lx + s * sc + lx + (en + 1) * sc) / 2, y + rh / 2), f'#{k} [{s},{en}]  价值 {v}', 20, T['bg'], anchor='mm', bold=True)


def _info(S):
    if 'f' not in S:
        return ''
    return f'`f[i]` = 按开始时间排序后，从第 i 个到最后的最大价值：`{S["f"]}`'


CONFIG = dict(
    num=2054, title='两个最好的不重叠活动', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='双排序 + 后缀最大值 + 单调移动指针',
    tags=['单调栈', '动态规划', '难度分 1883'],
    code='''
class Solution(object):
    def maxTwoEvents(self, events):

        n = len(events)
        start = sorted(range(n), key=lambda d:events[d][0])
        end = sorted(range(n), key=lambda d:events[d][1])

        f = [events[start[-1]][2]]
        for index in range(n - 2, -1, -1):
            f.append(max(f[-1], events[start[index]][2]))
        
        f.reverse()
        
        p = 0
        res = 0
        now = 0
        for index in range(n):
            while p < n and events[start[p]][0] <= events[end[index]][1]:
                p += 1
            
            if p != n:
                res = max(res, events[end[index]][2] + f[p])
            else:
                res = max(res, events[end[index]][2])
        
        return res
''',
    call='Solution().maxTwoEvents(%s)' % EVS,
    expect=10,
    views=[
        dict(type='text', fn=_info),
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='f', label='f（后缀最大价值，下标 = 按开始时间排序后的名次）', pointers={'p': 'pink'}, h=190),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'cyan'), ('index', 'index', 'yellow'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    skip=['now = 0'],
    captions={
        'n = len(events)': '`n = {n}` 个活动',
        'start = sorted': '`start`：活动编号按==开始时间==从小到大排：`{start}`',
        'end = sorted': '`end`：活动编号按==结束时间==从小到大排：`{end}`',
        'f = [events[start[-1]][2]]': '`f` 从后往前算：最后一名（开始最晚）的价值 `{f[0]}`',
        'for index in range(n - 2': '往前依次算后缀最大值',
        'f.append(max(f[-1]': '`f` 追加 `max(之前最大, 价值 {events[start[index]][2]})` → `{f}`（此时还是倒序）',
        'f.reverse()': '翻转后 `f[i]` 就是==开始时间排名第 i 起到最后==的最大价值：`{f}`',
        'p = 0': '`p` 指向「开始时间可用」的第一个活动，它只会向后走',
        'res = 0': '`res` 记录最大价值和',
        'for index in range(n):': '枚举前一场活动：结束时间第 `{index}` 早的活动 `#{end[index]}`',
        'while p < n and': lambda S, B, ret: (
            f'活动 `#{S.start[S.p]}` 开始于 `{S.events[S.start[S.p]][0]}` ≤ 当前结束 `{S.events[S.end[S.index]][1]}` → 重叠，`p` 后移' if S.p < S.n and S.events[S.start[S.p]][0] <= S.events[S.end[S.index]][1]
            else ('`p` 已到末尾，没有能接在后面的活动' if S.p >= S.n else f'活动 `#{S.start[S.p]}` 开始于 `{S.events[S.start[S.p]][0]}` > 当前结束 `{S.events[S.end[S.index]][1]}` → 从这里起都可选')),
        'p += 1': '`p` → {p}（均摊下来 `p` 总共只走 n 步）',
        'if p != n': lambda S, B, ret: (f'`p = {S.p}` ≠ n → 后面有可选活动，最好的是 `f[{S.p}] = {S.f[S.p]}`' if S.p != S.n
                                       else '`p = n` → 没有能接在后面的活动，只能选当前这一个'),
        'res = max(res, events[end[index]][2] + f[p])': '两场：`{events[end[index]][2]} + f[{p}]` = {events[end[index]][2] + f[p]}，`res = {res}`',
        'res = max(res, events[end[index]][2])': '只选一场：价值 `{events[end[index]][2]}`，`res = {res}`',
        'return res': '最大价值和 `{res}`',
    },
    cards=dict(
        one_liner='枚举前一场，后一场只看「开始得晚的」里最值钱的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`events[i] = [开始, 结束, 价值]`，最多选两场==时间不重叠==的活动',
                 '结束时间等于另一场的开始时间也算重叠',
                 '本视频：`%s` → `10`' % EVS],
        quote='令f[i]表示按endTime排序后，第i到第n - 1场活动中的最大价值……当index先后移动时，p也会跟着向后移动，从而在均摊O(1)的时间内找出每个index对应的p。',
        quote_src='—— yiduobo 题解原文',
        idea=['两场等价，不妨枚举前一场，后一场要开始在它结束之后',
              '分别按开始、结束时间排序，前一场结束越晚，可选的后一场越少',
              '所以指针 `p` 单调后移，`f[p]` 直接给出可选集合里的最大价值'],
        summary=['时间 `O(n log n)`（两次排序），双指针部分 `O(n)`',
                 '开始 `<=` 结束才算重叠，所以 while 条件里是 `<=`',
                 '`p == n` 时没有可选的后一场，只能单选',
                 '原文为 Python 2 风格，代码无需改动即可运行',
                 '原文把 f 说成「按 endTime 排序」，代码里实际是按开始时间的 `start` 顺序；视频以代码为准',
                 '对比灵神：灵神一次遍历 + 单调栈二分，yiduobo 用两次排序 + 后缀最大'],
    ),
)
