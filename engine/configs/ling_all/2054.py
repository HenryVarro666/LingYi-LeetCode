EVS = [[1, 3, 2], [4, 5, 2], [2, 4, 3], [6, 7, 4]]
SORTED_ = sorted(EVS, key=lambda e: e[1])


def _cur(S):
    if 'end_time' in S and 'start_time' in S and 'value' in S:
        return [S['start_time'], S['end_time'], S['value']]
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '活动按结束时间排序（蓝 = 当前活动，绿 = 栈里保留的活动，灰 = 被淘汰）', 22, T['muted'], bold=True)
    evs = S.get('events', SORTED_)
    if 'st' not in S:
        evs = EVS
    lx, rx = x0 + 60, x1 - 40
    tmax = 8
    sc = (rx - lx) / tmax
    top = y0 + 60
    rh = min(62, (y1 - top - 50) / len(SORTED_))
    cur = _cur(S)
    st = S.get('st') or []
    kept = {(e, v) for e, v in st}
    for t in range(tmax + 1):
        cv.line([(lx + t * sc, top - 8), (lx + t * sc, top + rh * len(SORTED_))], T['border'], 1)
        cv.text((lx + t * sc, top + rh * len(SORTED_) + 6), t, 18, T['dim'], anchor='mt', mono=True)
    sorted_now = 'st' in S
    for k, e in enumerate(SORTED_ if sorted_now else EVS):
        s, en, v = e
        y = top + k * rh
        is_cur = cur == e
        inkept = (en, v) in kept and not is_cur
        col = T['blue'] if is_cur else (T['green'] if inkept else (90, 96, 108))
        cv.rect((lx + s * sc, y + 6, lx + (en + 1) * sc, y + rh - 6), fill=col, r=6)
        cv.text(((lx + s * sc + lx + (en + 1) * sc) / 2, y + rh / 2), f'[{s},{en}]  价值 {v}', 20, T['bg'], anchor='mm', bold=True)
    if cur and 'i' in S and S['i'] >= 0 and S.get('_line', 0) >= 10 and 'start_time' in S:
        # 第一个活动：st[i] 对应的结束时间 < start_time
        pass


def _stinfo(S):
    st = S.get('st')
    if st is None:
        return ''
    cur = _cur(S)
    s = f'栈（结束时间↑ 价值↑）：`{st}`'
    if cur and 'i' in S and S.get('_line', 0) >= 10:
        s += f'；第一个活动 = `st[{S["i"]}]`'
    return s


CONFIG = dict(
    num=2054, title='两个最好的不重叠活动', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='按结束时间排序 + 单调栈上二分',
    tags=['单调栈', '动态规划', '难度分 1883'],
    code='''
class Solution:
    def maxTwoEvents(self, events: List[List[int]]) -> int:
        # 按照结束时间排序
        events.sort(key=lambda e: e[1])  

        # 从栈底到栈顶，结束时间递增，价值递增
        st = [(0, 0)]  # 栈底哨兵 
        ans = 0
        for start_time, end_time, value in events:
            # 二分查找最后一个结束时间 < start_time 的活动
            i = bisect_left(st, (start_time,)) - 1
            ans = max(ans, st[i][1] + value)
            # 遇到比栈顶更大的价值，入栈
            if value > st[-1][1]:
                st.append((end_time, value))
        return ans
''',
    call='Solution().maxTwoEvents([[1,3,2],[4,5,2],[2,4,3],[6,7,4]])',
    expect=7,
    views=[
        dict(type='text', fn=_stinfo),
        dict(type='custom', draw=_draw, h=330),
        dict(type='stack', var='st', label='单调栈（结束时间, 价值）', fmt=lambda x: f'({x[0]},{x[1]})', h=170),
    ],
    watch=[('start', 'start_time', 'blue'), ('end', 'end_time', 'cyan'), ('value', 'value', 'pink'), ('i', 'i', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'events.sort': '先按==结束时间==排序：这样「结束得早」的活动排在前面',
        'st = [(0, 0)]': '栈底放哨兵 `(0, 0)`：结束时间 0、价值 0，表示「不选第一个活动」',
        'ans = 0': '`ans` 记录最大价值和',
        'for start_time': '枚举==第二个活动==：开始 `{start_time}`，结束 `{end_time}`，价值 `{value}`',
        'i = bisect_left': '在栈里二分：最后一个结束时间 < `{start_time}` 的活动在下标 `{i}`，即 `{st[i]}`',
        'ans = max': '第一个活动选栈里 `{st[i]}`（价值最大的合法者），`{st[i][1]} + {value}` = {st[i][1] + value}，`ans = {ans}`',
        'if value > st[-1][1]': lambda S, B, ret: (
            f'价值 `{S.value}` > 栈顶价值 `{S.st[-1][1]}` → 它比栈顶更值钱，值得记录' if S.value > S.st[-1][1]
            else f'价值 `{S.value}` ≤ 栈顶价值 `{S.st[-1][1]}`，又结束得更晚 → ==全方面不如栈顶==，忽略'),
        'st.append': '入栈 `({end_time}, {value})`：栈里结束时间、价值都严格递增',
        'return ans': '最大价值和 `{ans}`',
    },
    cards=dict(
        one_liner='排序后只记录「更值钱」的活动，二分找第一个活动',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`events[i] = [开始, 结束, 价值]`，最多选两个==时间不重叠==的活动',
                 '结束时间等于下一个开始时间也算重叠',
                 '本视频：`[[1,3,2],[4,5,2],[2,4,3],[6,7,4]]` → `7`（选 `[2,4]` 与 `[6,7]`）'],
        quote='活动二的结束时间又晚，价值又小，全方面不如活动一，是垃圾数据，直接忽略。……只在遇到更大价值的活动时，才记录该活动。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举第二个活动，第一个活动要在它开始前结束，且价值最大',
              '按结束时间排序，栈里只留价值递增的活动，非常适合二分',
              '栈底放哨兵 `(0, 0)`，找不到第一个活动时就等于只选一个'],
        after=[dict(heading='灵神的另一种写法', lines=['写法二：把 events 本身当作栈（size 记栈大小），空间 O(1)', '缺点是没法放哨兵，要多判断 `i >= 0`', '进阶：至多选 k 个，见 1751 题'])],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`bisect_left(st, (start_time,))` 找的是结束时间 ==严格小于== start_time，因为端点相等算重叠',
                 '先用栈顶更新 `ans`，再决定是否入栈',
                 '只选一个活动的情况由哨兵 `(0, 0)` 自动覆盖'],
    ),
)
