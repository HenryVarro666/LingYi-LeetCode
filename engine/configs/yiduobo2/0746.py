COST = [2, 7, 3, 9, 1, 8, 4]   # 取值互不相同，便于从 w 反查下标 k


def _f_all(cost):
    f = [cost[0], cost[1]]
    for w in cost[2:]:
        f.append(min(f[-1], f[-2]) + w)
    return f


F = _f_all(COST)
N = len(COST)


def _line(S):
    return CODE.strip('\n').split('\n')[S['_line'] - 1].strip()


def _ended(S, B):
    return _line(S).startswith('for') and 'w' in B and B['w'] == S.get('w')


def _pos(S, B):
    """变量 a/b/c 此刻代表 f 的哪一格"""
    ln = _line(S)
    if 'w' not in S:
        out = {}
        if 'a' in S:
            out['a'] = 0
        if 'b' in S:
            out['b'] = 1
        return out
    if _ended(S, B) or ln.startswith('return'):
        return {'a': N - 2, 'b': N - 1}
    k = COST.index(S['w'])
    if ln.startswith('for'):
        return {'a': k - 2, 'b': k - 1}
    if ln.startswith('c = min'):
        return {'a': k - 2, 'b': k - 1, 'c': k}
    return {'a': k - 1, 'b': k, 'c': k}


def _cur_k(S, B):
    if 'w' not in S or _ended(S, B) or _line(S).startswith('return'):
        return None
    return COST.index(S['w'])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pos = _pos(S, B)
    hi = max(pos.values()) if pos else -1
    k = _cur_k(S, B)
    width = x1 - x0 - 140
    cell = min(112, width / (N + 1))
    sx = x0 + 120
    ch = cell * 0.8
    ycost = y0 + 80
    yf = ycost + ch + 170
    cv.text((x0 + 18, y0 + 4), 'cost 与 f（f[i]：站上第 i 级最少花多少，含 cost[i]；? = 还没算）', 24, T['muted'], bold=True)
    cv.text((sx - 16, ycost + ch / 2), 'cost', 24, T['muted'], anchor='rm', bold=True, mono=True)
    cv.text((sx - 16, yf + ch / 2), 'f', 26, T['muted'], anchor='rm', bold=True, mono=True)
    fin = 'w' in S and (_ended(S, B) or _line(S).startswith('return'))
    for i in range(N + 1):
        X = sx + i * cell
        if i == N:
            c = T['yellow'] if fin else T['panel2']
            cv.rect((X + 4, ycost, X + cell - 4, yf + ch), fill=c, r=10, outline=T['border'])
            cv.text((X + cell / 2, (ycost + yf + ch) / 2), '楼顶', 24, T['bg'] if fin else T['muted'], anchor='mm', bold=True)
            continue
        cc = T['pink'] if i == k else T['panel2']
        cv.rect((X + 4, ycost, X + cell - 4, ycost + ch), fill=cc, r=8, outline=T['border'])
        cv.text((X + cell / 2, ycost + ch / 2), COST[i], 30, T['bg'] if i == k else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ycost + ch + 6), i, 18, T['dim'], anchor='mt', mono=True)
        names = sorted(n for n, p in pos.items() if p == i)
        known = i <= hi
        fill = T['panel2']
        if names:
            fill = {'a': T['blue'], 'b': T['purple'], 'c': T['green']}[names[0]]
        elif known:
            fill = (52, 60, 72)
        cv.rect((X + 4, yf, X + cell - 4, yf + ch), fill=fill, r=8, outline=T['border'])
        txt = str(F[i]) if known else '?'
        cv.text((X + cell / 2, yf + ch / 2), txt, 30, T['bg'] if names else (T['muted'] if known else T['dim']),
                anchor='mm', bold=True)
        for r, nm in enumerate(names):
            cl = {'a': T['blue'], 'b': T['purple'], 'c': T['green']}[nm]
            cv.text((X + cell / 2, yf + ch + 8 + r * 26), nm, 24, cl, anchor='mt', bold=True, mono=True)
        if k is not None and i == k and 'c' in pos:
            cv.arrow((X + cell / 2, ycost + ch + 34), (X + cell / 2, yf - 46), T['pink'], 3, 12)
            cv.text((X + cell / 2 + 10, (ycost + ch + yf) / 2 - 6), f'+ cost[{k}]', 20, T['pink'], anchor='lm', bold=True)
            # f[k] 来自 f[k-1]、f[k-2] 的较小者
            for src in (k - 1, k - 2):
                if src < 0:
                    continue
                good = F[src] == min(F[k - 1], F[k - 2])
                p0 = (sx + src * cell + cell / 2, yf - 6)
                p1 = (X + cell / 2 - 4, yf - 6)
                cv.arc_arrow(p0, p1, 18 + 22 * (k - src), T['green'] if good else T['dim'], 3, 11)
    if fin:
        a, b = F[N - 2], F[N - 1]
        cv.text((x0 + 18, y1 - 60), f'最后一步：从第 {N - 2} 级跨 2 级（{a}）或从第 {N - 1} 级跨 1 级（{b}）→ 取 {min(a, b)}',
                24, T['yellow'], bold=True)


def _cap_for(S, B, ret):
    if 'w' in B and B.w == S.w:
        return f'`cost[2:]` 遍历完：`a = f[{N - 2}] = {S.a}`，`b = f[{N - 1}] = {S.b}`'
    k = COST.index(S.w)
    return f'下一级台阶 `w = cost[{k}] = {S.w}`；此时 `a = f[{k - 2}]`，`b = f[{k - 1}]`'


def _cap_c(S, B, ret):
    k = COST.index(S.w)
    src = k - 1 if S.b <= S.a else k - 2
    return (f'`f[{k}] = min(f[{k - 2}], f[{k - 1}]) + cost[{k}]` = `min({S.a}, {S.b}) + {S.w}` = =={S.c}=='
            f'：从第 {src} 级上来更省')


CODE = '''
class Solution(object):
    def minCostClimbingStairs(self, cost):
        a = cost[0]
        b = cost[1]
        for w in cost[2:]:
            c = min(a, b) + w
            a, b = b, c

        return min(a, b)
'''

CONFIG = dict(
    num=746, title='使用最小花费爬楼梯', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='f[i] 含本级花费 · 三变量滚动',
    tags=['字节30天'],
    code=CODE,
    call=f'Solution().minCostClimbingStairs({COST})',
    expect=10,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('w', 'w', 'pink'), ('a', 'a', 'blue'), ('b', 'b', 'purple'), ('c', 'c', 'green')],
    captions={
        'a = cost[0]': '边界 `f[0] = cost[0] = {a}`：站上第 0 级，要付它的钱（离开时才能往上爬）',
        'b = cost[1]': '边界 `f[1] = cost[1] = {b}`：也可以直接从第 1 级出发',
        'for w in': _cap_for,
        'c = min(a, b)': _cap_c,
        'a, b = b, c': '只和前两级有关 → ==三个变量倒一倒==：`a ← b = {a}`，`b ← c = {b}`',
        'return min': '楼顶在最后一级之外：最后一步可走 1 级或 2 级 → `min(f[-2], f[-1]) = min({a}, {b})` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i] 表示走到第 i 级的最小花费，每级从前一级或前两级走上来',
        complexity='时间 `O(n)`，空间 `O(1)`（`cost[2:]` 切片另占 `O(n)`）',
        problem=['`cost[i]` 是从第 `i` 级台阶向上爬要付的钱，付完可以爬 ==1 级或 2 级==',
                 '可以从下标 0 或 1 出发，求爬到==楼顶（最后一级之外）==的最小花费',
                 '示例：`[10,15,20]` → `15`；本视频：`[2,7,3,9,1,8,4]` → `10`'],
        quote='设f[i]表示走到第i级台阶最少需要花费的体力……有 `f[i] = min(f[i - 1], f[i - 2]) + cost[i]`。边界条件为f[0] = cost[0], f[1] = cost[1]。最终答案为min(f[-1]，f[-2])。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 把第 `i` 级自己的 `cost[i]` 也算进去：站上来就得付',
              '楼顶在数组外，最后一步从倒数第 1 或第 2 级跨上去 → 答案取 `min(f[-1], f[-2])`',
              '每一轮只用前两轮 → 用 `a, b, c` 三个变量滚动，不开数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：这里 `f[i]` ==含 cost[i]==，所以最后要再取一次 `min(a, b)`，不能直接返回 `b`',
                 '对比灵神：灵神的 `f[i]` 是「爬到 i、还没付 cost[i]」，楼顶就是 `f[n]`，边界是 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
