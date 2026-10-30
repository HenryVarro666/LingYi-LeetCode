from fractions import Fraction

_RET_LINE = 21


def _fr(v):
    if v == 0:
        return '0'
    f = Fraction(v).limit_denominator(1 << 14)
    return str(f.numerator) if f.denominator == 1 else f'{f.numerator}/{f.denominator}'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S['f']
    N = len(f[0])
    ln = S.get('_line', 0)
    live = 'now' in S and 'i' in S and ln == 19
    srcs = set()
    if live:
        srcs = {(S['i'] + a, S['j'] + b) for a, b in zip(S['dx'], S['dy'])
                if 0 <= S['i'] + a < N and 0 <= S['j'] + b < N}
    if 'now' in S:
        last_i, now_i = S['last'] if 'last' in S else 1 - S['now'], S['now']
    else:
        last_i, now_i = 0, 1
    layers = [(last_i, '上一轮 f[last]（读）'), (now_i, '本轮 f[now]（写）')]
    gap = 60
    cell = max(40, min(110, ((x1 - x0 - 40 - gap) / 2) / N, (y1 - y0 - 150) / N))
    gw = cell * N
    total = gw * 2 + gap
    sx0 = x0 + 20 + ((x1 - x0 - 40) - total) / 2
    oy = y0 + 100
    done = ln >= _RET_LINE
    for li, (ly, title) in enumerate(layers):
        ox = sx0 + li * (gw + gap)
        cv.text((ox + gw / 2, oy - 48), title if 'now' in S else (f'f[{ly}]：走 0 步，全 1' if ly == 0 else 'f[1]：暂时全 0'), 22, T['muted'], anchor='mm', bold=True)
        for c in range(N):
            cv.text((ox + c * cell + cell / 2, oy - 6), str(c), 18, T['dim'], anchor='mb', mono=True)
            cv.text((ox - 8, oy + c * cell + cell / 2), str(c), 18, T['dim'], anchor='rm', mono=True)
        for i in range(N):
            for j in range(N):
                v = f[ly][i][j]
                X, Y = ox + j * cell, oy + i * cell
                fill, tc = T['panel2'], T['text']
                if live and li == 1 and (i, j) == (S['i'], S['j']):
                    fill, tc = T['yellow'], T['bg']
                elif live and li == 0 and (i, j) in srcs:
                    fill, tc = T['blue'], T['bg']
                elif done and ly == S['K'] & 1 and (i, j) == (S['r'], S['c']):
                    fill, tc = T['green'], T['bg']
                cv.rect((X + 1, Y + 1, X + cell - 1, Y + cell - 1), fill=fill, outline=T['border'], width=1, r=6)
                s = _fr(v)
                cv.text((X + cell / 2, Y + cell / 2), s, 26 if len(s) <= 3 else 20, tc, anchor='mm', bold=True)


def _formula(S):
    ln = S.get('_line', 0)
    if 'now' not in S or 'i' not in S or ln != 19:
        return '`f[k][i][j]` = 从 `(i,j)` 出发跳 `k` 轮后仍在棋盘上的概率；只留 `f[now]` 和 `f[last]` 两层'
    i, j = S['i'], S['j']
    tot = sum(S['f'][S['last']][i + a][j + b] for a, b in zip(S['dx'], S['dy'])
              if 0 <= i + a < len(S['f'][0]) and 0 <= j + b < len(S['f'][0]))
    return f'`({i},{j})`：棋盘内的落点概率之和 `{_fr(tot)}`，再 ÷ 8 = ==`{_fr(tot / 8)}`=='


def _cap_div(S, B):
    i, j, N = S.i, S.j, len(S.f[0])
    ins = [(i + a, j + b) for a, b in zip(S.dx, S.dy) if 0 <= i + a < N and 0 <= j + b < N]
    tot = S.f[S.last]
    sm = sum(tot[x][y] for x, y in ins)
    return (f'`({i},{j})` 的 8 种跳法里有 `{len(ins)}` 个落点在棋盘内（蓝），上一轮概率之和 `{_fr(sm)}`；'
            f'出界的贡献 0，÷ 8 → =={_fr(S.f[S.now][i][j])}==')


CONFIG = dict(
    num=688, title='骑士在棋盘上的概率', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='概率 DP · 滚动数组',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def knightProbability(self, N, K, r, c):

        f = [[[1] * N for _ in range(N)], [[0] * N for _ in range(N)]]
        dx = [2, 1, -1, -2, -2, -1, 1, 2]
        dy = [1, 2, 2, 1, -1, -2, -2, -1]

        for k in range(1, K + 1):
            now = k & 1
            last = now ^ 1
            for i in range(N):
                for j in range(N):
                    f[now][i][j] = 0.0
                    for index in range(8):
                        next_i = i + dx[index]
                        next_j = j + dy[index]
                        if next_i >= 0 and next_i < N and next_j >= 0 and next_j < N:
                            f[now][i][j] += f[last][next_i][next_j]
                    f[now][i][j] /= 8.0
        
        return f[K & 1][r][c]
''',
    call='Solution().knightProbability(3, 2, 0, 0)',
    expect=0.0625,
    skip=['for i in range(N)', 'for j in range(N)', 'f[now][i][j] = 0.0', 'for index in range(8)',
          'next_i = i + dx[index]', 'next_j = j + dy[index]', 'if next_i >= 0', 'f[now][i][j] +='],
    max_steps=100,
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('k', 'k', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('now', 'now', 'green')],
    captions={
        'f = [[[1]': '`f[0]` 全是 1：走 0 步仍在棋盘上，概率 1；`f[1]` 先放 0。每一轮只依赖上一轮，所以==只用两层，轮流读写==',
        'dx = [': '8 种跳法的行偏移 `dx`',
        'dy = [': '8 种跳法的列偏移 `dy`，和 `dx` 同下标配对',
        'for k in range': lambda S, B, r: (f'第 `{S.k}` 轮：算跳 `{S.k}` 次后仍在棋盘上的概率' if S.get('k') != B.get('k') else '`K` 轮都算完了'),
        'now = k & 1': '`now = k & 1` = `{now}`：本轮把结果写进 `f[{now}]`',
        'last = now ^ 1': '`last = {last}`：上一轮的结果在 `f[{last}]`，从那里读',
        'f[now][i][j] /= 8.0': lambda S, B, r: _cap_div(S, B),
        'return f[K & 1][r][c]': lambda S, B, r: f'`f[K & 1] = f[{S.K & 1}]` 里起点 `({S.r},{S.c})` 的值 = =={_fr(r)}==',
    },
    cards=dict(
        one_liner='f[k][i][j] = 8 个落点 f[k-1] 之和 ÷ 8，只留两层滚动',
        complexity='时间 `O(K·N^2)`，空间 `O(N^2)`',
        problem=['`N x N` 棋盘，骑士从 `(r, c)` 出发，每步等概率选 8 种走法之一（可以走出棋盘）',
                 '走了 `K` 步或出界就停下，求停下时仍在棋盘上的概率',
                 '本视频：`N=3, K=2, (0,0)` → `0.0625`'],
        quote='设f[k][i][j]表示从棋盘上的(i, j)开始起跳，经过k轮之后仍在棋盘上的概率……枚举下一步可能跳到的位置，若这个位置在棋盘内，那么f[k][i][j] += f[k - 1][next_i][next_j]。在枚举完所有的八种跳法之后，将f[k][i][j]除以8。',
        quote_src='—— yiduobo 题解原文',
        idea=['出界的落点概率为 0，所以只累加棋盘内的落点',
              '第 `k` 轮只看第 `k-1` 轮 → 把 `k` 这一维变成 0/1，两层交替使用',
              '最后答案就是 `f[K & 1][r][c]`'],
        summary=['时间 `O(K·N^2)`，空间 `O(N^2)`',
                 '`f[0]` 初始全 1；`f[1]` 初始值会在第 1 轮被整格覆盖',
                 '每格要先清零再累加（`= 0.0`），因为 `f[now]` 里是两轮前的旧值',
                 '对比灵神：灵神把棋盘外扩两圈补 0 省掉 `if`；yiduobo 用 `if` 判断是否在棋盘内',
                 '视频里省略了每个方向的越界判断细节，只显示棋盘内的落点累加'],
    ),
)
