ST, ET = [0, 2, 4, 7], [1, 3, 6, 8]


def _win(S):
    """(first, last) meeting indices inside the window, or None"""
    k, n = S['k'], len(S['startTime'])
    L = S['_line']
    idx = S.get('index')
    if L <= 9:
        return None if idx is None or 's' not in S else (0, idx)
    if L >= 16:
        return (n - k, n - 1)
    if L <= 11:
        return (idx - k, idx - 1)
    if L == 12:
        return (idx - k + 1, idx - 1)
    return (idx - k + 1, idx)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(S['startTime'])
    st, et = S['startTime'], S['endTime']
    T_end = S['eventTime']
    ax0, ax1 = x0 + 40, x1 - 40
    sx = lambda t: ax0 + (ax1 - ax0) * t / T_end
    cv.text((x0 + 18, y0 + 4), '时间轴：青色 = 窗口内的 k 个会议，橙色括号 = 上界', 24, T['muted'], bold=True)
    yb = y0 + 150
    cv.line([(ax0, yb + 70), (ax1, yb + 70)], T['border'], 2)
    for t in range(T_end + 1):
        cv.line([(sx(t), yb + 70), (sx(t), yb + 78)], T['border'], 2)
        cv.text((sx(t), yb + 84), t, 20, T['dim'], anchor='mt', mono=True)
    w = _win(S) if 's' in S else None
    for j in range(n):
        inw = w and w[0] <= j <= w[1]
        cv.rect((sx(st[j]), yb, sx(et[j]), yb + 70), fill=T['cyan'] if inw else (125, 133, 145), r=6)
        cv.text(((sx(st[j]) + sx(et[j])) / 2, yb + 35), f'{et[j] - st[j]}', 26, T['bg'], anchor='mm', bold=True)
        cv.text(((sx(st[j]) + sx(et[j])) / 2, yb - 8), f'#{j}', 20, T['cyan'] if inw else T['dim'], anchor='mb', bold=True)
    L = S['_line']
    if w and L >= 11 and 'pre' in S:
        idx = S.get('index', n)
        lo = S['pre'] if L <= 13 or L >= 16 else S['pre']
        hi = st[idx] if L < 16 and idx < n else T_end
        if L >= 14 and L < 16:
            lo = S['pre']
        cv.line([(sx(lo), yb - 40), (sx(hi), yb - 40)], T['orange'], 4)
        cv.line([(sx(lo), yb - 48), (sx(lo), yb - 32)], T['orange'], 4)
        cv.line([(sx(hi), yb - 48), (sx(hi), yb - 32)], T['orange'], 4)
        cv.text(((sx(lo) + sx(hi)) / 2, yb - 60), f'{hi} − {lo} = {hi - lo}（含会议）', 22, T['orange'], anchor='mb', bold=True)
        cv.text(((x0 + x1) / 2, yb + 130), f'空余 ≤ {hi - lo} − 会议总长 {S["s"]} = {hi - lo - S["s"]}', 30, T['green'], anchor='mm', bold=True)


CONFIG = dict(
    num=3439, title='重新安排会议得到最多空余时间 I', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='定长滑窗 · 连续 k 个会议',
    tags=['难度分 1729'],
    code='''
class Solution(object):
    def maxFreeTime(self, eventTime, k, startTime, endTime):
        
        s = 0
        pre = 0
        res = 0
        for index in range(k):
            s += endTime[index] - startTime[index]
        
        for index in range(k, len(startTime)):
            res = max(res, startTime[index] - pre - s)
            s -= (endTime[index - k] - startTime[index - k])
            s += (endTime[index] - startTime[index])
            pre = endTime[index - k]
        
        res = max(res, eventTime - pre - s)
        return res
''',
    call='Solution().maxFreeTime(10, 2, [0, 2, 4, 7], [1, 3, 6, 8])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='startTime', label='startTime', pointers={'index': 'blue'}, h=170, cell=80),
        dict(type='array', var='endTime', label='endTime', h=140, cell=80),
    ],
    watch=[('index', 'index', 'blue'), ('k', 'k'), ('s', 's', 'cyan'), ('pre', 'pre', 'pink'), ('res', 'res', 'green')],
    captions={
        4: '`s` 记录窗口内 `k` 个会议的总时长',
        'pre = 0': '`pre`：窗口前一个会议的结束时间（最前面没有会议，就是 0）',
        'res = 0': '`res` 记录最大空余时间',
        'for index in range(k)': lambda S, B, r: ('前 `k` 个会议的总时长统计完了' if 'index' in B and S.index == B.index else f'先把前 `k` 个会议装进窗口：第 `{S.index}` 个'),
        's += endTime[index] - startTime[index]': '会议 `{index}` 时长 `{endTime[index] - startTime[index]}` → `s = {s}`',
        'for index in range(k, len': lambda S, B, r: ('所有窗口都滑完了，还差最后一个窗口' if 'index' in B and S.index == B.index
                                                    else f'窗口右移：下一个会议是第 `{S.index}` 个，窗口是第 `{S.index - S.k}`~`{S.index - 1}` 个会议'),
        'res = max(res, startTime': '窗口夹在 `pre = {pre}` 和 `startTime[{index}] = {startTime[index]}` 之间：总共 `{startTime[index] - pre}`，减去会议 `{s}`，最大空余 ==`{startTime[index] - pre - s}`==；`res` → {res}',
        's -= ': '最前面的会议 `{index - k}` 离开窗口：`s` 减去 `{endTime[index - k] - startTime[index - k]}` → `{s}`',
        's += (endTime[index]': '会议 `{index}` 进入窗口：`s` 加上 `{endTime[index] - startTime[index]}` → `{s}`',
        'pre = endTime[index - k]': '窗口前沿移动：`pre = endTime[{index - k}] = {pre}`',
        'res = max(res, eventTime': '最后一个窗口夹在 `pre = {pre}` 和 `eventTime = {eventTime}`：`{eventTime} − {pre} − {s} = {eventTime - pre - s}` → `res = {res}`',
        'return res': '最大空余时间 `{res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='挪动的必是连续 k 个会议：夹在两侧会议之间，减去会议总长',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['总时长 `eventTime`，`n` 个互不重叠的会议，==至多平移 k 个==（保持顺序和时长）',
                 '求重排后相邻会议之间最长的连续空余时间',
                 '本视频：`eventTime = 10, k = 2`，会议 `[0,1] [2,3] [4,6] [7,8]` → `4`'],
        quote='相邻会议最大的空余时间的上限，就是区间总时间startTime[index + k] - endTime[index - 1]，再减去这k个会议需要消耗的时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['调整的会议必然连续，否则有些调整没有作用',
              '调整第 `index`~`index+k-1` 个会议：它们被夹在 `endTime[index-1]` 与 `startTime[index+k]` 之间',
              '把 k 个会议紧挨前一个会议排好，空余就是 ==总间隔 − k 个会议的总时长==，取最大'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：最后一个窗口的右边界是 `eventTime`，循环外还要再算一次',
                 '`pre` 记录窗口前一个会议的结束时间，开头没有会议所以是 0',
                 '对比灵神：灵神把空余段当元素，窗口 `k+1`；yiduobo 以会议为元素，窗口 `k`，答案相同'],
    ),
)
