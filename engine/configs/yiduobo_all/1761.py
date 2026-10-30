def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    n = S['n']
    d = S.get('d')
    res = S.get('res')
    I, J, K = S.get('i'), S.get('j'), S.get('k')
    line = S.get('_line', 0)
    has = d is not None and res is not None and I is not None
    cv.text((x0 + 18, y0 + 4), '图（黄 = i，蓝 = j，粉 = k；找到的三元组三条边加粗）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 14
    R = min((x1 - x0) / 2 - 90, (y1 - y0) / 2 - 62)
    pos = {}
    for t in range(n):
        a = -math.pi / 2 + 2 * math.pi * t / n
        pos[t] = (cx + R * math.cos(a), cy + R * math.sin(a))
    sel = [v for v in (I, J, K) if v is not None] if has else []
    f = S.get('f')
    for a, b in S['edges']:
        a -= 1
        b -= 1
        tri = len(sel) == 3 and a in sel and b in sel
        pair = len(sel) >= 2 and a in sel and b in sel
        cv.line([pos[a], pos[b]], T['green'] if tri else (T['yellow'] if pair else T['border']), 7 if tri else (5 if pair else 3))
    cols = {I: 'yellow', J: 'blue', K: 'pink'}
    for v in range(n):
        X, Y = pos[v]
        if has and v in sel:
            cv.rect((X - 38, Y - 38, X + 38, Y + 38), outline=T[cols[v]], width=5, r=38)
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=T['panel2'], outline=T['border'], width=2, r=30)
        cv.text((X, Y), v + 1, 30, T['text'], anchor='mm', bold=True)
        if d is not None:
            cv.text((X, Y + 52), f'度 {d[v]}', 20, T['orange'], anchor='mm', bold=True)


_JC = {}


def _last_j(S):
    # i 只剩一个 j 时，第 1 次经过 for j 是进入，第 2 次才是结束
    if S.i != S.n - 3:
        return True
    _JC[S.i] = _JC.get(S.i, 0) + 1
    return _JC[S.i] % 2 == 0


def _txt(S):
    I, J, K = S.get('i'), S.get('j'), S.get('k')
    d, res = S.get('d'), S.get('res')
    if d is None or res is None or I is None or J is None or S.get('f') is None:
        return ''
    if S.get('_line') in (21, 22, 23) and K is not None and S['f'][I][K] and S['f'][J][K]:
        return f'三元组 ({I+1},{J+1},{K+1})：`{d[I]} + {d[J]} + {d[K]} − 6` = =={d[I]+d[J]+d[K]-6}=='
    return f'当前最小 `res = {res}`'


CONFIG = dict(
    num=1761, title='一个图中连通三元组的最小度数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='暴力枚举三元组 · 度数相加减 6',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minTrioDegree(self, n, edges):

        if n < 3:
            return -1

        d = [0] * n
        f = [[False] * n for _ in range(n)]
        for x, y in edges:
            x -= 1
            y -= 1
            d[x] += 1
            d[y] += 1
            f[x][y] = f[y][x] = True
            
        res = n * 3
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                if f[i][j] and d[i] + d[j] - 4 < res:
                    for k in range(j + 1, n):
                        if f[i][k] and f[j][k] and d[i] + d[j] + d[k] - 6 < res:
                            res = min(d[i] + d[j] + d[k] - 6, res)

        if res == n * 3:
            res = -1
        
        return res
''',
    call='Solution().minTrioDegree(5, [[1,2],[1,3],[2,3],[3,4],[4,5]])',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='array', var='d', pointers={'i': 'yellow', 'j': 'blue', 'k': 'pink'}, label='d（各点度数，下标从 0 起）', h=190),
        dict(type='text', fn=_txt, h=60, size=28),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'blue'), ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        'if n < 3': '连通三元组至少要 3 个点',
        'd = [0] * n': '`d[x]` = 点 x 的度数（先全记 0）',
        'f = [[False]': '`f[x][y]` 表示 x、y 之间有没有边（邻接矩阵）',
        'f[x][y] = f[y][x]': '边 `{x+1}`-`{y+1}`：两个点度数各 +1，`d = {d}`，矩阵两个方向都标 True',
        'res = n * 3': '`res` = 当前最小度数，先设成一个不可能达到的大数 `{res}`（每点度数 < n，三点和 ≤ 3n）',
        'for i in range': lambda S, B, r: ('`i` 全部枚举完' if getattr(B, 'i', None) == S.i == S.n - 3 else f'枚举三元组里的最小点 `i = {S.i}`'),
        'for j in range': lambda S, B, r: (f'`i = {S.i}` 的所有 `j` 都试完了' if getattr(B, 'j', None) == S.j == S.n - 2 and getattr(B, 'i', None) == S.i and _last_j(S) else f'枚举第二个点 `j = {S.j}`（`j > i`，避免重复）'),
        'if f[i][j] and': lambda S, B, r: (
            f'`i={S.i}, j={S.j}`：{"==有边==" if S.f[S.i][S.j] else "没有边"}'
            + (f'；剪枝 `d[i]+d[j]−4 = {S.d[S.i]+S.d[S.j]-4}` {"<" if S.d[S.i]+S.d[S.j]-4 < S.res else "≥"} `res = {S.res}`'
               + ('，值得继续' if S.d[S.i]+S.d[S.j]-4 < S.res else '，再加第三个点也不会更小，跳过') if S.f[S.i][S.j] else '，三元组不成立，跳过')),
        'for k in range': lambda S, B, r: (f'`(i,j) = ({S.i},{S.j})` 的所有 `k` 都试完了' if getattr(B, 'k', None) == S.k == S.n - 1 and getattr(B, 'j', None) == S.j and getattr(B, 'i', None) == S.i and B.get('_line') != 18 else f'枚举第三个点 `k = {S.k}`'),
        'if f[i][k] and f[j][k]': lambda S, B, r: (
            f'`k={S.k}`：与 i {"有" if S.f[S.i][S.k] else "无"}边，与 j {"有" if S.f[S.j][S.k] else "无"}边'
            + (f' → 三点两两相连！度数和 `{S.d[S.i]}+{S.d[S.j]}+{S.d[S.k]}−6 = {S.d[S.i]+S.d[S.j]+S.d[S.k]-6}`'
               + (' < res，更新' if S.d[S.i]+S.d[S.j]+S.d[S.k]-6 < S.res else '，不比 res 小')
               if S.f[S.i][S.k] and S.f[S.j][S.k] else ' → 不是三角形')),
        'res = min': '三点度数相加会把三角形内部的 3 条边各算两次（共 6），要减掉 → `res = {res}`',
        'if res == n * 3': lambda S, B, r: ('`res` 没变过 → 图里==没有三角形==，应返回 -1' if S.res == S.n * 3 else f'`res = {S.res}` 被更新过，说明存在三元组'),
        'return res': '最小度数 `{ret}`',
    },
    skip=['for x, y in edges', 'x -= 1', 'y -= 1', 'd[x] += 1', 'd[y] += 1'],
    max_steps=100,
    cards=dict(
        one_liner='三点两两相连才算三元组，度数 = 三点度数和 − 6',
        complexity='时间 `O(n³)`，空间 `O(n²)`',
        problem=['无向图 `n` 个点（编号 1~n），`edges` 为边',
                 '连通三元组 = 三个点两两有边；其度数 = 一端在三元组内、另一端在外的边数',
                 '返回所有连通三元组度数的最小值，没有则 `-1`',
                 '示例：`n=5, edges=[[1,2],[1,3],[2,3],[3,4],[4,5]]` → `1`'],
        quote='数据规模有限，因此可以直接暴力求解。枚举三个点i、j、k，若三者两两相连，那么最终度数就等于d[i] + d[j] + d[k] - 6',
        quote_src='—— yiduobo 题解原文',
        idea=['先统计每个点的度数 `d`，再建邻接矩阵 `f` 以 O(1) 判断两点有没有边',
              '三点内部 3 条边，每条边给两个端点各记 1 度，共 6，所以外向度数 = 和 − 6',
              '枚举 `i<j<k`；`d[i]+d[j]-4` 是 k 至少还要加上的下界，已不小于 res 就剪枝'],
        summary=['时间 `O(n³)`（有剪枝），空间 `O(n²)`',
                 '易错：边端点从 1 开始，要先 `-1`；没有三角形时返回 -1，不是 0',
                 '`res` 初值 `3n` 作为「没找到」标记，最后换成 -1',
                 '原文可直接在 Python 3 运行，未做修改',
                 '同类：三角形计数、最小度数三元组的位运算 / 排序度数优化'],
    ),
)
