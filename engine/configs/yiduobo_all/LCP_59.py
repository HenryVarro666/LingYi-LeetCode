from collections import Counter as _C


def _sim(wood):
    """复刻算法，收集所有出现过的坐标，用来固定数轴范围"""
    L, R, sb, eb, pts = [], [], 0, 0, []
    import heapq as hq
    for i, (x, y) in enumerate(wood):
        pts += [x, y]
        if i == 0:
            L.append(-x)
            R.append(x)
            continue
        sb -= y - x
        eb += wood[i - 1][1] - wood[i - 1][0]
        s, e = -L[0] + sb, R[0] + eb
        pts += [s, e]
        if x < s:
            hq.heappop(L)
            hq.heappush(L, sb - x)
            hq.heappush(L, sb - x)
            hq.heappush(R, s - eb)
        elif s <= x <= e:
            hq.heappush(L, sb - x)
            hq.heappush(R, x - eb)
        else:
            hq.heappop(R)
            hq.heappush(R, x - eb)
            hq.heappush(R, x - eb)
            hq.heappush(L, sb - e)
    return min(pts), max(pts)


WOOD = [[2, 3], [8, 11], [4, 5], [1, 2]]
LO, HI = _sim(WOOD)


def _interval(S):
    lh, rh = S.get('left_heap'), S.get('right_heap')
    if not lh or not rh:
        return None
    return -lh[0] + S.get('start_bias', 0), rh[0] + S.get('end_bias', 0)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴：黄条 = f[i] 取最小值的区间 [start, end]；蓝点 = left 堆，粉点 = right 堆', 21, T['muted'], bold=True)
    lo, hi = LO - 1, HI + 1
    X0, X1 = x0 + 100, x1 - 50
    sc = (X1 - X0) / (hi - lo)

    def px(v):
        return X0 + (v - lo) * sc
    wood = S['wood']
    idx = S.get('index', -1)
    # 木头本身
    for k, (a, b) in enumerate(wood):
        yy = y0 + 46 + k * 18
        cur = k == idx
        cv.rect((px(a), yy, px(b), yy + 12), fill=T['orange'] if cur else T['border'], r=5)
        cv.text((px(a) - 8, yy + 6), f'wood[{k}]', 16, T['orange'] if cur else T['dim'], anchor='rm', bold=cur)
    ya = y0 + 46 + len(wood) * 18 + 62
    cv.line([(X0 - 10, ya), (X1 + 10, ya)], T['border'], 3)
    step = 1 if hi - lo <= 22 else 2
    v = lo
    while v <= hi:
        cv.line([(px(v), ya - 5), (px(v), ya + 5)], T['border'], 2)
        cv.text((px(v), ya + 10), v, 17, T['dim'], anchor='mt', mono=True)
        v += step
    iv = _interval(S)
    if iv:
        s, e = iv
        cv.rect((px(s) - 4, ya - 14, px(e) + 4, ya + 2), fill=T['yellow'], r=7, alpha=210)
        cv.text(((px(s) + px(e)) / 2, ya - 22), f'最优区间 [{s}, {e}]', 21, T['yellow'], anchor='mb', bold=True)
    if idx >= 0 and 'x' in S:
        cv.tri_up(px(S['x']), ya + 38, 10, T['orange'])
        cv.text((px(S['x']), ya + 52), f"x = {S['x']}", 19, T['orange'], anchor='mt', bold=True)
    sb, eb = S.get('start_bias', 0), S.get('end_bias', 0)
    for hp, bias, sign, col, row in ((S.get('left_heap') or [], sb, -1, T['blue'], 0), (S.get('right_heap') or [], eb, 1, T['pink'], 1)):
        for val, c in sorted(_C(sign * h + bias for h in hp).items()):
            xx, yy = px(val), ya + 86 + row * 30
            cv.rect((xx - 11, yy, xx + 11, yy + 24), fill=col, r=12)
            if c > 1:
                cv.text((xx + 15, yy + 12), f'×{c}', 18, col, anchor='lm', bold=True)
    cv.text((x0 + 18, ya + 86 + 12), 'left', 19, T['blue'], anchor='lm', bold=True)
    cv.text((x0 + 18, ya + 86 + 42), 'right', 19, T['pink'], anchor='lm', bold=True)


def _cmp(S, B, ret):
    s, e = _interval(S)
    x = S.x
    if x < s:
        return f'`x = {x} < now_start = {s}`：新木头的起点落在最优区间==左边==，必须多花 `{s} − {x}`'
    if x <= e:
        return f'`{s} ≤ x = {x} ≤ {e}`：x 就落在最优区间内 → ==不用多花操作=='
    return f'`x = {x} > now_end = {e}`：新木头的起点落在最优区间==右边==，必须多花 `{x} − {e}`'


CONFIG = dict(
    num='LCP 59', title='搭桥过河', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='凸函数 · 双堆维护拐点',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def buildBridge(self, num, wood):

        left_heap = []
        right_heap = []
        res = 0
        start_bias = 0
        end_bias = 0

        n = len(wood)
        for index in range(n):
            x, y = wood[index]
            if index == 0:
                left_heap.append(-x)
                right_heap.append(x)
            else:
                now_length = y - x
                last_length = wood[index - 1][1] - wood[index - 1][0]
                start_bias -= now_length
                end_bias += last_length

                now_start = -left_heap[0] + start_bias
                now_end = right_heap[0] + end_bias

                if x < now_start:
                    heapq.heappop(left_heap)
                    heapq.heappush(left_heap, start_bias - x)
                    heapq.heappush(left_heap, start_bias - x)
                    heapq.heappush(right_heap, now_start - end_bias)
                    res += now_start - x
                elif now_start <= x <= now_end:
                    heapq.heappush(left_heap, start_bias - x)
                    heapq.heappush(right_heap, x - end_bias)
                else:
                    heapq.heappop(right_heap)
                    heapq.heappush(right_heap, x - end_bias)
                    heapq.heappush(right_heap, x - end_bias)
                    heapq.heappush(left_heap, start_bias - now_end)
                    res += x - now_end

        return res
''',
    call='Solution().buildBridge(0, [[2,3],[8,11],[4,5],[1,2]])',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=350),
        dict(type='heap', var='left_heap', label='left_heap（存 start_bias − 坐标）', top_color='blue', h=90),
        dict(type='heap', var='right_heap', label='right_heap（存 坐标 − end_bias）', top_color='pink', h=90),
    ],
    watch=[('index', 'index', 'blue'), ('x', 'x', 'orange'), ('start_bias', 'start_bias', 'cyan'),
           ('end_bias', 'end_bias', 'pink'), ('res', 'res', 'green')],
    skip=[5, 6, 8, 10, 12, 17, 18],
    captions={
        'left_heap = []': '`left`（大顶堆）存最优区间的左端 `start` 及其左边的拐点；`right`（小顶堆）存右端 `end` 及其右边的拐点',
        'start_bias = 0': '两个偏移量：整体平移时不用动堆，只改偏移就行',
        'if index == 0': lambda S, B, r: (f'第一段木头 `[{S.x}, {S.y}]`：`f[0][j] = |x − j|`，是个 V 字形，最优点就是 `x`' if S.index == 0 else
                                          f'第 {S.index} 段木头 `[{S.x}, {S.y}]`（`x` 是原来的起点）：先把上一轮的最优区间向两边撑开'),
        'left_heap.append(-x)': '左堆放 `-x`（取负当大顶堆）',
        'right_heap.append(x)': '右堆放 `x`：最优区间 `[{x}, {x}]`，累计操作 0',
        'start_bias -= now_length': '`start` 向左偏移 `now_length = {now_length}`：本段木头更长，起点可以更靠左仍与上一段重叠 → `start_bias = {start_bias}`',
        'end_bias += last_length': '`end` 向右偏移 `last_length = {last_length}`：上一段木头的长度 → `end_bias = {end_bias}`',
        'now_start = ': lambda S, B, r: f'堆顶还原坐标：`now_start = {-S.left_heap[0]} + ({S.start_bias}) = {S.now_start}`',
        'now_end = ': '`now_end = {right_heap[0]} + {end_bias} = {now_end}`：最优区间被撑成 `[{now_start}, {now_end}]`',
        'if x < now_start': _cmp,
        'elif now_start <= x <= now_end': lambda S, B, r: (f'`{S.now_start} ≤ {S.x} ≤ {S.now_end}`：成立 → x 在最优区间内' if S.now_start <= S.x <= S.now_end
                                                      else f'`x = {S.x}` 不在 `[{S.now_start}, {S.now_end}]` 内 → 一定在右边'),
        'heapq.heappop(left_heap)': '弹出 left 堆顶（旧的 `start`）：斜率为 −1 的那段被新的 V 形盖住了',
        'heapq.heappush(right_heap, now_start - end_bias)': '旧 `start` 变成斜率 +1 折线的起点 → 移到 right 堆',
        'res += now_start - x': '`res += {now_start} − {x}` → =={res}==',
        'heapq.heappop(right_heap)': '弹出 right 堆顶（旧的 `end`）：被新的 V 形盖住',
        'heapq.heappush(left_heap, start_bias - now_end)': '旧 `end` 变成斜率 −1 折线的终点 → 移到 left 堆',
        'res += x - now_end': '`res += {x} − {now_end}` → =={res}==',
        27: '把 `x = {x}` 放进 left 堆（存 `start_bias − x`）',
        28: '再放一次：构造一条长度为 0 的线段，避免斜率脱节',
        32: '左右两个堆各放一个 `x = {x}`：新的最优区间缩成 `[{x}, {x}]`',
        36: '把 `x = {x}` 放进 right 堆（存 `x − end_bias`）',
        37: '再放一次：同样构造长度为 0 的线段',
        'return res': '最少总操作次数 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='f 是凸函数：双堆记住最优区间两端，新木头落在哪边就多花多少',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['有若干段木头 `wood[i] = [起点, 终点]`，每段可以整体平移，平移 1 格算 1 次操作',
                 '要求相邻两段木头至少有一个公共点（题解的建模）；求最少总操作数',
                 '本视频：`[[2,3],[8,11],[4,5],[1,2]]` → `7`'],
        quote='若wood[i][0] < start……start左侧所有的折线斜率都要减上1……需要将start从left移动到right……将wood[i][0]加入到left中两次。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` = 第 i 段起点放在 j 的最小操作数，是==凸函数==：绝对值累加',
              '`[start, end]` 是最小值所在的区间；每轮先按相邻重叠的约束撑开：`start − 本段长`，`end + 上段长`',
              'x 在区间内：最小值不变；在左边 / 右边：答案 += 距离，并把旧端点挪到另一个堆'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '偏移量 `start_bias / end_bias` 记录整体平移，堆里存的是去掉偏移后的值',
                 '三种情况：`x < start`（左）、在区间内、`x > end`（右），左右对称',
                 '参数 `num` 在这份解法里没有用到；原文代码在 Python 3 下无需修改',
                 '同一思路的简化版见 2263：只有一边需要维护'],
    ),
)
