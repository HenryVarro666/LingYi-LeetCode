EVT = 10
ST, ET = [0, 2, 4, 7], [1, 3, 6, 8]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(ST)
    T_end = S['eventTime']
    ax0, ax1 = x0 + 40, x1 - 40
    sx = lambda t: ax0 + (ax1 - ax0) * t / T_end
    cv.text((x0 + 18, y0 + 4), '时间轴：灰块 = 会议，青色框 = 窗口里的 k+1 个空余段', 24, T['muted'], bold=True)
    yb = y0 + 140
    cv.line([(ax0, yb + 70), (ax1, yb + 70)], T['border'], 2)
    for t in range(T_end + 1):
        cv.line([(sx(t), yb + 70), (sx(t), yb + 78)], T['border'], 2)
        cv.text((sx(t), yb + 84), t, 20, T['dim'], anchor='mt', mono=True)
    gaps = [(0, ST[0])] + [(ET[j - 1], ST[j]) for j in range(1, n)] + [(ET[-1], T_end)]
    win = None
    if 'i' in S and 'free' in S:
        win = (max(0, S['i'] - S['k']), S['i'])
    for j, (a, b) in enumerate(gaps):
        inw = win and win[0] <= j <= win[1]
        if b > a:
            cv.rect((sx(a), yb, sx(b), yb + 70), fill=T['cyan'] if inw else T['border'], alpha=110 if inw else 40, r=6)
            cv.text(((sx(a) + sx(b)) / 2, yb + 35), b - a, 28, T['text'], anchor='mm', bold=True)
        cv.text(((sx(a) + sx(b)) / 2, yb - 22), f'空{j}', 20, T['cyan'] if inw else T['dim'], anchor='mb', bold=True)
    for a, b in zip(ST, ET):
        cv.rect((sx(a), yb, sx(b), yb + 70), fill=(125, 133, 145), r=6)
        cv.text(((sx(a) + sx(b)) / 2, yb + 35), f'[{a},{b}]', 20, T['bg'], anchor='mm', bold=True)
    if win:
        a = gaps[win[0]][0]
        b = gaps[win[1]][1]
        cv.rect((sx(a) - 3, yb - 8, sx(b) + 3, yb + 78), outline=T['cyan'], width=4, r=8)
        cv.text(((x0 + x1) / 2, yb + 130), f'窗口里的空余合起来：{S["s"]}', 30, T['cyan'], anchor='mm', bold=True)


CONFIG = dict(
    num=3439, title='重新安排会议得到最多空余时间 I', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长滑窗 · 合并 k+1 个空余段',
    tags=['难度分 1729'],
    code='''
class Solution:
    def maxFreeTime(self, eventTime: int, k: int, startTime: List[int], endTime: List[int]) -> int:
        n = len(startTime)
        free = [0] * (n + 1)
        free[0] = startTime[0]  # 最左边的空余时间段
        for i in range(1, n):
            free[i] = startTime[i] - endTime[i - 1]  # 中间的空余时间段
        free[n] = eventTime - endTime[-1]  # 最右边的空余时间段

        # 套定长滑窗模板（窗口长为 k+1）
        ans = s = 0
        for i, f in enumerate(free):
            s += f
            if i < k:
                continue
            ans = max(ans, s)
            s -= free[i - k]
        return ans
''',
    call='Solution().maxFreeTime(10, 2, [0, 2, 4, 7], [1, 3, 6, 8])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='free', label='free（n+1 个空余时间段，框 = 窗口，长 k+1）', pointers={'i': 'blue'},
             window=(lambda S: max(0, S['i'] - S['k']) if 'i' in S else None, 'i'), h=200, cell=90),
        dict(type='text', h=70, size=32,
             fn=lambda S: (f'窗口和 `s = {S["s"]}`，答案 `ans = {S["ans"]}`' if 's' in S and 'i' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('f', 'f', 'pink'), ('k', 'k'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}` 个会议，会议之间和两端共有 `n + 1` 个空余时间段',
        'free = [0]': '先建数组 `free` 存各段空余时间的长度',
        'free[0] = startTime[0]': '最左边：从 0 到第一个会议开始，长 `{free[0]}`',
        'free[i] = ': '第 `{i - 1}`、`{i}` 个会议之间：`{startTime[i]} − {endTime[i - 1]} = {free[i]}`',
        'free[n] = ': '最右边：`{eventTime} − {endTime[-1]} = {free[n]}`；`free = {free}`',
        'ans = s = 0': '定长滑窗：窗口长 `k + 1 = {k + 1}`，因为移动 `k` 个会议可以==合并 k+1 段空余==',
        'for i, f in enumerate(free)': lambda S, B, r: ('窗口扫完了' if 'i' in B and S.i == B.i else f'第 `{S.i}` 段空余时间 `{S.f}` 进入窗口'),
        's += f': '`s += {f}` → 窗口和 `{s}`',
        'if i < k': lambda S, B, r: (f'`i = {S.i} < k = {S.k}`：窗口还没满 `k + 1` 段，先不更新答案' if S.i < S.k
                                     else f'`i = {S.i} ≥ k`：窗口刚好 `{S.k + 1}` 段，可以更新答案'),
        'continue': '继续往右扩',
        'ans = max': '`ans = max({B.ans}, {s}) = {ans}`：==合并这 k+1 段能得到的最长空余==',
        's -= free[i - k]': '最左边的一段 `free[{i - k}] = {free[i - k]}` 离开窗口 → `s = {s}`',
        'return ans': '最长连续空余时间是 `{ans}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='最多移动 k 个会议 = 合并连续 k+1 个空余段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['总时长 `eventTime`，`n` 个互不重叠的会议，==至多平移 k 个==（保持顺序、时长、不出界）',
                 '要使相邻会议间最长的连续空余时间最大',
                 '本视频：`eventTime = 10, k = 2`，会议 `[0,1] [2,3] [4,6] [7,8]` → `4`'],
        quote='一般地，最优做法是合并连续 k+1 个空余时间段。……这可以用定长滑动窗口解决，窗口大小为 k+1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['挪动一个会议，就把它两侧相邻的两段空余合并成一段',
              '挪动连续 `k` 个会议 → 合并连续 `k + 1` 段空余（相对顺序不能变）',
              '空余段共 `n + 1` 个（两端各一个，可以是 0），求长 `k + 1` 的窗口最大和'],
        summary=['时间 `O(n)`，空间 `O(n)`；写法二用函数 `get(i)` 算空余段，空间 `O(1)`',
                 '易错：空余段有 `n + 1` 个，窗口长度是 `k + 1` 不是 `k`',
                 '两端的空余段别漏：`startTime[0]` 和 `eventTime − endTime[-1]`',
                 '主写法是写法一（建 free 数组）；定长滑窗模板：入 → 更新 → 出'],
    ),
)
