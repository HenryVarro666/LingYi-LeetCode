def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = 5
    ans = S.get('res') or []
    total = n * (n - 1)
    cv.text((x0 + 18, y0 + 4), '赛程矩阵：每列一天，每行一支队（蓝 = 主场，粉 = 客场）', 22, T['muted'], bold=True)
    lab = 70
    cw = min(52, (x1 - x0 - 40 - lab) / total)
    ch = min(50, (y1 - y0 - 170) / n)
    sx, sy = x0 + 20 + lab, y0 + 80
    px_, py_ = S.get('pre_x'), S.get('pre_y')
    for t in range(n):
        busy = t in (px_, py_)
        cv.text((sx - 12, sy + t * ch + ch / 2), f'队{t}', 22, T['orange'] if busy else T['muted'], anchor='rm', bold=True)
    for day in range(total):
        X = sx + day * cw
        cv.text((X + cw / 2, sy - 8), day + 1, 14, T['dim'], anchor='mb', mono=True)
        for t in range(n):
            cv.rect((X + 1, sy + t * ch + 1, X + cw - 1, sy + (t + 1) * ch - 1), fill=T['panel2'], r=3)
    for day, (a, b) in enumerate(ans):
        X = sx + day * cw
        last = day == len(ans) - 1
        for t, c, lt in ((a, T['blue'], '主'), (b, T['pink'], '客')):
            cv.rect((X + 1, sy + t * ch + 1, X + cw - 1, sy + (t + 1) * ch - 1), fill=c, r=3,
                    outline=T['yellow'] if last else None, width=3)
            cv.text((X + cw / 2, sy + t * ch + ch / 2), lt, 18, T['bg'], anchor='mm', bold=True)
    yb = sy + n * ch + 18
    x, y = S.get('x'), S.get('y')
    if x is not None:
        cv.text((x0 + 20, yb), f'本轮候选：x = 队{x}' + (f'，y = 队{y}' if y is not None else '，y 还没选出'), 24, T['text'], bold=True)
    cv.text((x0 + 20, yb + 36), f'已排 {len(ans)} / {total} 场；橙色队名 = 上一天比赛的队（今天不能用）', 20, T['muted'])


def _c9(S, B, r):
    if len(S.res) >= 20:
        return '20 场都排完了，结束循环'
    return f'第 {len(S.res) + 1} 天：要选一对队伍'


def _c14(S, B, r):
    if not S.heap:
        return '堆空了'
    t, h = S.heap[0]
    if h in (S.pre_x, S.pre_y):
        return f'堆顶 队{h} 昨天比过赛 → 本轮不能用'
    return f'堆顶 队{h}（已赛 {t} 场）昨天没比赛 → 可以当 x'


def _c23(S, B, r):
    if not S.heap:
        return '堆空了，选不出 y'
    t, h = S.heap[0]
    if h in (S.pre_x, S.pre_y):
        return f'堆顶 队{h} 昨天比过赛 → 不能当 y'
    if (S.x, h) in S.using_pair and (h, S.x) in S.using_pair:
        return f'堆顶 队{h} 与 x=队{S.x} 已经打满两场 → 不能当 y'
    return f'堆顶 队{h}（已赛 {t} 场）昨天没赛，且和 x=队{S.x} 打过不到两场 → 可以当 y'


def _c24(S, B, r):
    t, h = S.heap[0]
    return f'堆顶 队{h} '.format(h=h) + ('昨天比过赛' if h in (S.pre_x, S.pre_y) else '和 x 已打满两场')


def _fmt(t):
    return f'队{t[1]}·{t[0]}场'


def _pre(S):
    return S.get('pre_x') is not None


CONFIG = dict(
    num=3680, title='生成赛程', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='贪心 · 堆选场次最少且昨天没赛的队',
    tags=['灵神题单', '难度分 2378'],
    code='''
class Solution(object):
    def generateSchedule(self, n):
        
        heap = [(0, index) for index in range(n)]
        pre_x, pre_y = None, None
        using_pair = set()
        res = []

        while len(res) < n * (n - 1):
            pending_same = []
            pending_x = []
            x, y = None, None
            while y is None:
                while heap and (heap[0][1] == pre_x or heap[0][1] == pre_y):
                    pending_same.append(heapq.heappop(heap))
            
                if heap:
                    tx, x = heapq.heappop(heap)
                else:
                    return []
            
                pending_y = []
                while heap and (heap[0][1] == pre_x or heap[0][1] == pre_y or ((x, heap[0][1]) in using_pair and (heap[0][1], x) in using_pair)):
                    if heap[0][1] == pre_x or heap[0][1] == pre_y:
                        pending_same.append(heapq.heappop(heap))
                    else:
                        pending_y.append(heapq.heappop(heap))
            
                if heap:
                    ty, y = heapq.heappop(heap)
                else:
                    heap = pending_y[:]
                    pending_x.append((tx, x))
            
            if (x, y) in using_pair:
                x, y = y, x
                tx, ty = ty, tx
            
            res.append([x, y])
            using_pair.add((x, y))
            heapq.heappush(heap, (tx + 1, x))
            heapq.heappush(heap, (ty + 1, y))
            for p in pending_same:
                heapq.heappush(heap, p)
            for p in pending_x:
                heapq.heappush(heap, p)
            for p in pending_y:
                heapq.heappush(heap, p)

            pre_x, pre_y = x, y
        
        return res
''',
    call='Solution().generateSchedule(5)',
    expect=[[0, 1], [2, 3], [4, 0], [1, 2], [3, 4], [1, 0], [3, 2], [0, 4], [2, 1], [4, 3], [0, 2], [1, 3], [4, 2], [0, 3], [1, 4], [2, 0], [3, 1], [2, 4], [3, 0], [4, 1]],
    views=[
        dict(type='custom', draw=_draw, h=450),
        dict(type='heap', var='heap', fmt=_fmt, h=140),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('pre', '(pre_x, pre_y)', 'orange'), ('场数', 'len(res)', 'green')],
    max_steps=48,
    skip=['pending_same = []', 'pending_x = []', 'x, y = None, None', 'pending_y = []', 'if heap:', 'while y is None', 'for p in',
          'heapq.heappush(heap, p)', 'using_pair.add', 'pre_x, pre_y = x, y', 'while len(res) <', 'while heap and (heap[0][1] == pre_x or heap[0][1] == pre_y):', 'while heap and (heap[0][1] == pre_x or heap[0][1] == pre_y or', 'if (x, y) in using_pair', 'heapq.heappush(heap, (tx + 1, x))', '(ty + 1, y)', 'tx, ty = ty, tx', 'pre_x, pre_y = None', 'using_pair = set()', 'res = []'],
    captions={
        4: '堆里存 `(已赛场数, 队号)`，每次先取场次最少的队，让各队场次接近',
        9: _c9,
        14: _c14,
        15: lambda S, B, r: f'队{S.pending_same[-1][1]} 昨天比过赛 → 放进 `pending_same`，本轮不能用，轮末放回堆',
        18: '第 {len(res) + 1} 天：堆顶是场次最少、昨天没比赛的队 → 取出 `x = 队{x}`（已赛 {tx} 场）',
        20: '堆空了还没选出 x：无解，返回 `[]`',
        23: _c23,
        24: _c24,
        25: lambda S, B, r: f'队{S.pending_same[-1][1]} 昨天比过赛 → 放进 `pending_same`',
        27: lambda S, B, r: f'队{S.pending_y[-1][1]} 与 x=队{S.x} 已经打满两场 → 放进 `pending_y`：只是本轮不能当 y，换 x 后还要用',
        30: '取出 `y = 队{y}`（已赛 {ty} 场）→ 本轮对阵 ==队{x} vs 队{y}==',
        32: '堆里再没有能和 x 配对的队：把堆恢复成 `pending_y`，x 暂时没人配 → 记入 `pending_x`',
        33: '`x = 队{x}` 记入 `pending_x`，回到循环开头换一个 x 重选',
        35: lambda S, B, r: (f'队{S.x} 主场打队{S.y} 已经打过了' if (S.x, S.y) in S.using_pair else f'队{S.x} 与队{S.y} 还没交手过，队{S.x} 当主场'),
        36: '已经打过一次 → 这次交换主客：==队{x} 当主场==，保证「一主一客」',
        39: lambda S, B, r: (f'第 {len(S.res)} 天：`{S.res[-1]}`，前一天 `{S.res[-2]}` 无共同队伍；两队场数 +1 放回堆，明天不能用这两队' if len(S.res) > 1 else f'第 1 天：`{S.res[-1]}`；两队场数 +1 放回堆，明天不能用这两队'),
        52: '共 `{len(res)}` 场，每队两两一主一客，相邻两天没有共同队伍',
    },
    cards=dict(
        one_liner='堆里挑「场次最少、昨天没赛」的队配对',
        complexity='时间不易估算（`n ≤ 50` 够用），空间 `O(n^2)`',
        problem=['`n` 支队伍两两比赛两次（一主一客），每天一场',
                 '要求没有队伍在==连续两天==都比赛，返回任意一个赛程，没有就返回空',
                 '本视频：`n = 5`，共 20 场'],
        quote='每一轮都安排目前进行比赛最少，且上一轮没有安排过比赛，同时之前也没有进行过比赛的两只队伍进行比赛就是可行的处理方法。',
        quote_src='—— yiduobo 题解原文',
        idea=['堆里存 `(已赛场数, 队号)`，场数最少的在堆顶，这样各队场次始终接近',
              '堆顶是昨天的队 → 放进 `pending_same`，本轮不能用；选 y 时还要和 x 没打满两场',
              '选不出 y，就把 x 换掉重选；还没选出合法的 x 就返回空'],
        summary=['作者自己也说：复杂度不好算、构造不优美，靠 `n ≤ 50` 的小规模过关',
                 '三个等待数组：`pending_same` 昨天的队、`pending_x` 配不上对的 x、`pending_y` 暂时不能当 y 的队，本轮后要全部放回堆',
                 '`(x, y)` 已经打过就交换成 `(y, x)`，这样第二次比赛就是客场变主场',
                 '原文已是 Python 3 可运行，没有改动',
                 '对比灵神：灵神按差值 d 直接构造，不需要堆和回退'],
    ),
)
