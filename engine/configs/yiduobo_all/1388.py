SL = [1, 2, 3, 4, 5, 6]
N = len(SL)
K = N // 3


def _pass(S):
    return 2 if 'res' in S else 1


def _range(S):
    return (0, N - 2) if _pass(S) == 1 else (1, N - 1)


def _txt(S):
    p = _pass(S)
    lo, hi = _range(S)
    return f'第 {p} 遍：只用 `slices[{lo}..{hi}]`（' + ('==强制不选最后一块==）' if p == 1 else '==强制不选第一块==）')


def _cell(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if ci is None or cj is None or S['_line'] not in range(16, 30):
        return None
    if (i, j) == (ci, cj):
        return 'yellow'
    if j == cj and i == ci - 1:
        return 'blue'
    if j == cj - 1 and i == ci - 2:
        return 'green'
    return None


def _acolor(S, i, v):
    lo, hi = _range(S)
    if S.get('i') is not None and i == S['i'] and 'f' in S:
        return 'yellow'
    return None


CONFIG = dict(
    num=1388, title='3n 块披萨', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='环形拆成两遍 · 不相邻选 k 个',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def maxSizeSlices(self, slices):

        n = len(slices)

        f = [[0] * (n // 3 + 1) for _ in range(n)]
        f[0][1] = slices[0]
        f[1][1] = max(slices[0], slices[1])
        for i in range(2, n - 1):
            for j in range(1, n // 3 + 1):
                f[i][j] = f[i - 1][j]
                if j == 1:
                    f[i][j] = max(f[i][j], slices[i])
                elif f[i - 2][j - 1] is not None:
                    f[i][j] = max(f[i][j], f[i - 2][j - 1] + slices[i])
        res = f[n - 2][n // 3]

        f = [[0] * (n // 3 + 1) for _ in range(n)]
        f[1][1] = slices[1]
        f[2][1] = max(slices[1], slices[2])
        for i in range(3, n):
            for j in range(1, n // 3 + 1):
                f[i][j] = f[i - 1][j]
                if j == 1:
                    f[i][j] = max(f[i][j], slices[i])
                elif f[i - 2][j - 1] is not None:
                    f[i][j] = max(f[i][j], f[i - 2][j - 1] + slices[i])
        
        res = max(res, f[n - 1][n // 3])

        return res
''',
    call=f'Solution().maxSizeSlices({SL})',
    expect=10,
    skip=['for j in range', 'n = len(slices)', 'for i in range'],
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var='slices', label='slices（黄 = 正在考虑的这块披萨）', cell=84, h=200,
             pointers={'i': 'blue'}, color=_acolor,
             dim=lambda S, i, v: not (_range(S)[0] <= i <= _range(S)[1])),
        dict(type='table', var='f', label='f[i][j]：前 i+1 块里选 j 块的最大和（黄 = 正在算，蓝 = f[i-1][j]，绿 = f[i-2][j-1]）',
             cell=80, h=420, rows=lambda S: [f'{k}:{SL[k]}' for k in range(N)], cols=lambda S: [str(k) for k in range(K + 1)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = [[0] * (n // 3 + 1)': lambda S, B, r: (f'`f` 有 {N} 行（披萨）、`{K + 1}` 列（选 0..{K} 块），初值都是 0' if 'res' not in B
                                                  else '第二遍：==换一张新表==，这次强制不选第一块'),
        'f[0][1] = slices[0]': '前 1 块里选 1 块：只能选 `slices[0] = {slices[0]}`',
        'f[1][1] = max(slices[0], slices[1])': '前 2 块里选 1 块（相邻，二选一）：取大的 =={f[1][1]}==。第一遍 `i` 只到 `n-2`：==强制不选最后一块==',
        'f[i][j] = f[i - 1][j]': '不选 `slices[{i}]`：`f[{i}][{j}] = f[{i-1}][{j}]` = {f[i][j]}',
        'if j == 1': lambda S, B, r: (f'`j = 1`：只选一块，`slices[{B.i}]` 前面没有别的块要避开' if B.j == 1
                                    else f'`j = {B.j}`：已经选过别的块，选 `slices[{B.i}]` 就要避开 `slices[{B.i - 1}]`'),
        'f[i][j] = max(f[i][j], slices[i])': '`max({B.f[i][j]}, slices[{i}] = {slices[i]})` → =={f[i][j]}==',
        'elif f[i - 2][j - 1] is not None': '选 `slices[{i}]`：它前一块不能选，只能接在 `f[{i-2}][{j-1}] = {f[i-2][j-1]}` 后面',
        'f[i][j] = max(f[i][j], f[i - 2][j - 1] + slices[i])': '`max({B.f[i][j]}, {f[i-2][j-1]} + {slices[i]})` → =={f[i][j]}==：选与不选取大的',
        'res = f[n - 2][n // 3]': '第一遍答案：前 `n-1` 块里选 `n/3 = {n // 3}` 块 → `res = {res}`',
        'f[1][1] = slices[1]': '第一块不能用了：前两块（从 `slices[1]` 起）选一块只能是 `slices[1] = {slices[1]}`',
        'f[2][1] = max(slices[1], slices[2])': '`slices[1]`、`slices[2]` 相邻二选一 → =={f[2][1]}==。第二遍 `i` 到 `n-1`，但 ==不选第一块==',
        'res = max(res, f[n - 1][n // 3])': '两遍取大：`max({B.res}, {f[n-1][n//3]})` = =={res}==',
        'return res': '最多能吃到 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='环形不能同时选首尾：拆成「去掉最后一块」和「去掉第一块」两遍线性 DP',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['一个披萨切成 `3n` 块，按顺时针排成环，你先选一块，然后朋友们依次选走相邻的两块',
                 '问你自己==最多能吃到的总大小==。等价于：在环上选 `n/3` 块、互不相邻，和最大',
                 '本视频：`[1,2,3,4,5,6]` → `10`（选 4 和 6）'],
        quote='披萨是一个圆，也就是说我们是不能同时选择第一块和最后一块披萨的，一个简单的处理方法是我们强制不选择最后一块，即只对前n - 1块披萨执行动态规划，计算出第一种结果，然后强制不选择第一块，即只对后n - 1块披萨执行动态规划，计算出第二种结果，然后取二者的较大值作为答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：前 `i` 块披萨里选了 `j` 块能得到的最大和',
              '不选第 `i` 块：`f[i-1][j]`；选第 `i` 块：前一块不能选，接在 `f[i-2][j-1]` 后面，再加 `slices[i]`',
              '首尾相邻 → 拆成两个线性问题：去掉最后一块、去掉第一块，各跑一遍取大'],
        summary=['时间 `O(n^2)`：两遍，每遍 `n × n/3` 个状态，转移 `O(1)`',
                 '易错：第一遍 `i` 只到 `n-2`，第二遍从下标 1 开始，别把首尾同时放进去',
                 '易错：`j == 1` 单独处理，因为 `f[i-2][0]` 没有意义',
                 '原文为 Python 2 写法，其中 `n / 3` 是整数除法，已改为 `n // 3`',
                 '作者还讨论了贪心：最大块要么选它，要么选它两边那两块，但没给出证明'],
    ),
)
