def _f(n):
    f = [0] * (n + 1)
    best = [None] * (n + 1)
    for x in range(2, n + 1):
        f[x] = min(f[y] + f[x - y] + y * (x - y) for y in range(1, x))
        best[x] = [y for y in range(1, x // 2 + 1) if f[y] + f[x - y] + y * (x - y) == f[x]]
    return f, best


NN = 7
F, BEST = _f(NN)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '先算小的：f[x] = min(f[y] + f[x−y] + y×(x−y))，观察规律', 24, T['muted'], bold=True)
    cols = [('x', 90), ('f[x]（枚举所有拆法）', 330), ('x(x−1)//2', 220), ('最优的第一步拆成', 340)]
    X = x0 + 40
    yh = y0 + 70
    xs = []
    for name, w in cols:
        xs.append(X)
        cv.text((X, yh), name, 24, T['muted'], bold=True)
        X += w
    for x in range(1, NN + 1):
        y = yh + 50 + (x - 1) * 62
        cv.rect((x0 + 24, y - 4, x1 - 24, y + 50), fill=T['panel2'], r=8)
        cv.text((xs[0], y + 4), x, 30, T['text'], bold=True, mono=True)
        cv.text((xs[1], y + 4), F[x], 30, T['green'], bold=True, mono=True)
        cv.text((xs[2], y + 4), x * (x - 1) // 2, 30, T['yellow'], bold=True, mono=True)
        b = '—' if x == 1 else '、'.join(f'{a}+{x - a}' for a in BEST[x])
        cv.text((xs[3], y + 4), b, 26, T['blue'], mono=True)
    cv.text((x0 + 40, yh + 50 + NN * 62 + 8), '每一行两列相等；而且每一种拆法算出来都一样（最优拆法不止一种）', 24, T['orange'], bold=True)


CONFIG = dict(
    num=3857, title='拆分到 1 的最小总代价', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='先 DP 找规律 · 归纳证明',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def minCost(self, n):
        
        return n * (n - 1) // 2
''',
    call='Solution().minCost(6)',
    expect=15,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['n'],
    captions={
        'return': '推出的结论：`f[n] = n(n-1)/2`，代入 `n = {n}`：`{n} * ({n} - 1) // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='先写 DP，算几个小值找规律，再归纳证明 f[n] = n(n-1)/2',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把整数 `x` 拆成 `a + b`，代价 `a * b`',
                 '求把 `n`（1 到 500）拆成 `n` 个 `1` 的最小总代价',
                 '本视频：`n = 6` → `15`'],
        quote='对于f[n]，不妨设其第一步的最优做法是拆分为a和b，那么就有 f[n] = f[a] + f[b] + a * b = a * (a - 1) // 2 + b * (b - 1) // 2 + a * b',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 不大，可以 DP：`f[x] = min(f[y] + f[x-y] + x*y)`（原文写法）',
              '先算小的：`f[1]=0`，`f[2]=1`，`f[3]=3`…… 都等于 `x(x-1)//2`',
              '归纳：假设 `x < n` 都成立，第一步拆成 `a + b`',
              '`a(a-1)/2 + b(b-1)/2 + ab = (a+b)(a+b-1)/2 = n(n-1)/2`，与怎么拆无关'],
        result='`6 * 5 // 2 = 15` ✓',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文最后的代码就是公式，DP 只用来发现规律、不必提交',
                 '易错：`n^2` 展开后 `a^2 + b^2 + 2ab = n^2`，别漏掉 `2ab` 里的系数',
                 '对比灵神：灵神用“断开完全图的边”解释，这里用小值找规律 + 归纳'],
    ),
)
