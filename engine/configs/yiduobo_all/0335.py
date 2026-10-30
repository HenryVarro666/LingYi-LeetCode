X0 = [1, 1, 2, 2, 3, 1, 1]
DIRS = [(0, 1), (-1, 0), (0, -1), (1, 0)]   # 上、左、下、右（逆时针）


def _pts(xs):
    p = [(0, 0)]
    for k, d in enumerate(xs):
        dx, dy = DIRS[k % 4]
        p.append((p[-1][0] + dx * d, p[-1][1] + dy * d))
    return p


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '路线：上→左→下→右（粉 = 当前段，黄 = 要比较的前几段）', 22, T['muted'], bold=True)
    P = _pts(X0)
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    area = (x0 + 70, y0 + 90, x1 - 110, y1 - 40)
    sc = min((area[2] - area[0]) / max(w, 1), (area[3] - area[1]) / max(h, 1))
    ox = area[0] + ((area[2] - area[0]) - w * sc) / 2 - min(xs) * sc
    oy = area[3] - ((area[3] - area[1]) - h * sc) / 2 + min(ys) * sc

    def pt(q):
        return (ox + q[0] * sc, oy - q[1] * sc)

    for a in range(len(P) - 1):   # 整条路线淡淡画出
        cv.line([pt(P[a]), pt(P[a + 1])], (52, 60, 72), 3)
    if 'index' not in S:
        return
    idx = S['index']
    hit = S.get('_hit')
    for a in range(0, idx + 1):
        col = T['blue']
        wd = 5
        if a == idx:
            col, wd = T['pink'], 8
        elif idx - 5 <= a <= idx - 1 and S['_line'] >= 6:
            col = T['yellow'] if a >= idx - 4 else T['blue']
        cv.line([pt(P[a]), pt(P[a + 1])], col, wd)
        mx, my = pt(((P[a][0] + P[a + 1][0]) / 2, (P[a][1] + P[a + 1][1]) / 2))
        cv.text((mx + 12, my - 12), f'x[{a}]={X0[a]}', 18, T['text'] if a == idx else T['muted'], anchor='lb', bold=True)
    cv.arrow(pt(P[idx]), pt(P[idx + 1]), T['pink'], 6, 16)
    cv.text(pt(P[0]), 'O', 20, T['text'], anchor='rt', bold=True)


CONFIG = dict(
    num=335, title='路径交叉', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='只看最近 6 条线段 · 三种相交情形',
    tags=['贪心算法', '思维题'],
    code='''
class Solution(object):
    def isSelfCrossing(self, x):

        if len(x) <= 3:
            return False

        for index in range(3, len(x)):
            if x[index] >= x[index - 2] and x[index - 3] >= x[index - 1]:
                return True

            if index >= 4:
                if x[index - 1] == x[index - 3] and x[index] - x[index - 2] + x[index - 4] >= 0:
                    return True

            if index >= 5:
                if x[index - 2] >= x[index - 4] and x[index] - x[index - 2] + x[index - 4] >= 0 and x[index - 1] <= x[index - 3] and x[index - 1] - x[index - 3] + x[index - 5] >= 0:
                    return True

        return False
''',
    call=f'Solution().isSelfCrossing({X0})',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='array', var='x', pointers={'index': 'pink'}, h=210, label='x（每一步走的距离）',
             dim=lambda S, i, v: 'index' in S and i > S['index']),
    ],
    watch=['index', ('x[index]', "x[index]", 'pink')],
    captions={
        'if len(x) <= 3': '`len(x) = {len(x)}`：少于 4 段不可能自交（至少要 4 段才能回头碰第一段）',
        'for index in range': '逐段往后走，考察第 `index = {index}` 段与它前面最近几段是否相交',
        'if x[index] >= x[index - 2] and x[index - 3]': lambda S, B, r: (f"情形 1（第 4 段碰第 1 段）：`x[{S.index}] = {S.x[S.index]}` ≥ `x[{S.index - 2}] = {S.x[S.index - 2]}`（够长，伸得过去）且 `x[{S.index - 3}] = {S.x[S.index - 3]}` ≥ `x[{S.index - 1}] = {S.x[S.index - 1]}`（前面在内缩）→ " + ('==相交==' if S.x[S.index] >= S.x[S.index - 2] and S.x[S.index - 3] >= S.x[S.index - 1] else '不相交')),
        'if index >= 4': '`index = {index}`：' + '{"够 5 段，可以检查情形 2（形成长方形 / d 字型）" if index >= 4 else "不足 5 段，跳过情形 2"}',
        'if x[index - 1] == x[index - 3] and': lambda S, B, r: (f"情形 2（第 5 段碰第 1 段）：`x[{S.index - 1}] = {S.x[S.index - 1]}` == `x[{S.index - 3}] = {S.x[S.index - 3]}`（刚好在 y 轴上）且 `x[{S.index}] - x[{S.index - 2}] + x[{S.index - 4}] = {S.x[S.index] - S.x[S.index - 2] + S.x[S.index - 4]}` ≥ 0 → " + ('==相交==' if S.x[S.index - 1] == S.x[S.index - 3] and S.x[S.index] - S.x[S.index - 2] + S.x[S.index - 4] >= 0 else '不相交')),
        'if index >= 5': '`index = {index}`：' + '{"够 6 段，可以检查情形 3（阶梯收拢）" if index >= 5 else "不足 6 段，跳过情形 3"}',
        'if x[index - 2] >= x[index - 4] and': lambda S, B, r: (lambda x, i: f"情形 3（第 6 段碰第 1 段）：往外扩 `x[{i - 2}] ≥ x[{i - 4}]` → {x[i - 2] >= x[i - 4]}；回收长度 `x[{i}] - x[{i - 2}] + x[{i - 4}] = {x[i] - x[i - 2] + x[i - 4]}` ≥ 0 → {x[i] - x[i - 2] + x[i - 4] >= 0}；`x[{i - 1}] ≤ x[{i - 3}]` → {x[i - 1] <= x[i - 3]}；`x[{i - 1}] - x[{i - 3}] + x[{i - 5}] = {x[i - 1] - x[i - 3] + x[i - 5]}` ≥ 0 → {x[i - 1] - x[i - 3] + x[i - 5] >= 0}" + ('，四个都成立 → ==相交==' if (x[i - 2] >= x[i - 4] and x[i] - x[i - 2] + x[i - 4] >= 0 and x[i - 1] <= x[i - 3] and x[i - 1] - x[i - 3] + x[i - 5] >= 0) else '，有不成立的 → 不相交'))(S.x, S.index),
        'return True': '==路线自交了==，返回 `True`',
        'return False': '所有线段都检查完，没有相交 → `False`',
    },
    cards=dict(
        one_liner='只看最近 6 条线段：第 4、5、6 段可能碰到第 1 段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从原点出发，依次向北、西、南、东……走 `x[0], x[1], x[2], …` 步（每走完一段逆时针转 90 度）',
                 '判断路径是否与自己相交（包括端点接触）',
                 '本视频：`[1,1,2,2,3,1,1]` → `True`'],
        quote='对于任意一些连续的线段，如果旋转坐标轴并平移这些线段的话，都可以看成是从原点开始，按上左下右的顺序画出来的。',
        quote_src='—— yiduobo 题解原文',
        idea=['设第一次相交时较早的线段是第 `k` 段，把它放到 y 轴上，坐标就好写了',
              '后面能碰到它的只有第 4、5、6 段，三种情形各写成一个不等式',
              '第 7 段及以后若碰到第 1 段，必定先碰到别的段，归结为前三种'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '情形 1：第 4 段碰第 1 段；情形 2：第 5 段（长方形 / d 字型）；情形 3：第 6 段（阶梯收拢）',
                 '`index >= 4`、`index >= 5` 的判断是防止下标越界',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动',
                 '作者自己说：这是画图得到的结论，不太好严格推导'],
    ),
)
