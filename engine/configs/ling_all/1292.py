def _sq(S, i, j, v):
    if 'ans' not in S or 'i' not in S or 'j' not in S or S.get('_line') is None:
        return None
    a = S['ans']
    if S['i'] <= i <= S['i'] + a and S['j'] <= j <= S['j'] + a:
        return 'yellow'
    if S['i'] <= i < S['i'] + a and S['j'] <= j < S['j'] + a:
        return 'green'
    return None


def _txt(S):
    if 'ans' not in S or 'i' not in S or 'j' not in S:
        return ''
    a = S['ans']
    i, j = S['i'], S['j']
    if i + a < S['m'] and j + a < S['n'] and 's' in S:
        q = S['s'][i + a + 1][j + a + 1] - S['s'][i + a + 1][j] - S['s'][i][j + a + 1] + S['s'][i][j]
        return f"试 左上角 `({i},{j})`、边长 `{a + 1}` 的正方形：元素和 =={q}== （阈值 `{S['threshold']}`）"
    return f"左上角 `({i},{j})`：再变大就出界了，当前 ans = `{a}`"


CONFIG = dict(
    num=1292, title='元素和小于等于阈值的正方形的最大边长', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='二维前缀和 + ans 只增不减',
    tags=['二维前缀和', '难度分 1735'],
    code='''
class Solution:
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        m, n = len(mat), len(mat[0])
        s = [[0] * (n + 1) for _ in range(m + 1)]
        for i, row in enumerate(mat):
            for j, x in enumerate(row):
                s[i + 1][j + 1] = s[i + 1][j] + s[i][j + 1] - s[i][j] + x

        # 返回左上角在 (r1, c1)，右下角在 (r2, c2) 的子矩阵元素和
        def query(r1: int, c1: int, r2: int, c2: int) -> int:
            return s[r2 + 1][c2 + 1] - s[r2 + 1][c1] - s[r1][c2 + 1] + s[r1][c1]

        ans = 0
        for i in range(m):
            for j in range(n):
                # 边长为 ans+1 的正方形，左上角在 (i, j)，右下角在 (i+ans, j+ans)
                while i + ans < m and j + ans < n and query(i, j, i + ans, j + ans) <= threshold:
                    ans += 1
        return ans
''',
    call='Solution().maxSideLength([[1,1,3],[1,1,3],[1,1,3]], 4)',
    expect=2,
    views=[
        dict(type='grid', var='mat', cursors=[('i', 'j', 'yellow', '')], color=_sq, h=200, label='mat（黄=在试的正方形）'),
        dict(type='table', var='s', h=250, label='s 二维前缀和（多一行一列 0）'),
        dict(type='text', fn=_txt, size=26),
    ],
    watch=['i', 'j', ('ans', 'ans', 'green'), 'threshold'],
    skip=['m, n = len', 's = [[0]', 'for j, x in enumerate'],
    captions={
        's[i + 1][j + 1] =': '`s[{i+1}][{j+1}] = 左 {s[i+1][j]} + 上 {s[i][j+1]} − 左上 {s[i][j]} + 格子 {x}` = =={s[i+1][j+1]}==（容斥：左上角被加了两次，减一次）',
        'return s[r2 + 1]': '查询 `({r1},{c1})~({r2},{c2})`：大块 − 左边多的 − 上边多的 + 左上被减两次要加回 = =={ret}==',
        'ans = 0': '`ans = 0`：目前还没找到合法正方形',
        'while i + ans': lambda S, B, ret: (f"边长 `{S['ans']+1}` 会出界 → 条件不成立，换下一个左上角；ans 保持 `{S['ans']}`，==不从 1 重新枚举==" if (S['i'] + S['ans'] >= S['m'] or S['j'] + S['ans'] >= S['n']) else f"试边长 `{S['ans']+1}`：不出界，再看元素和是否 `≤ {S['threshold']}`"),
        'ans += 1': '合法 → 答案 +1，变成 `{ans}`；继续试更大的一圈（枚举 ans+1 才有意义）',
        'return ans': '没有任何位置能让 ans 再变大，最大边长 =={ans}==',
    },
    max_steps=75,
    cards=dict(
        one_liner='先建二维前缀和，再枚举左上角，边长只从 ans+1 开始试',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['矩阵 `mat` 和阈值 `threshold`，找元素和 `≤ threshold` 的正方形的最大边长，没有则为 0',
                 '示例：`[[1,1,3,2],...3 行]`，`threshold = 4`',
                 '边长 2 的左上角 2×2 和为 4，合法 → 答案 `2`'],
        quote='最内层循环，从 ans+1 开始枚举。比如现在 ans=3，那么枚举正方形的边长为 1,2,3 是毫无意义的，不会让答案变得更大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用二维前缀和，让任意子矩阵的和 ==O(1) 查询==',
              '暴力是三重循环：左上角 × 边长。改进：边长 ==从 ans+1 开始试==',
              'ans 最多涨到 `min(m,n)` 次，所以三重循环总共只有 `O(mn)`'],
        summary=['复杂度：`ans += 1` 总共不超过 `min(m,n)` 次，整体 `O(mn)`',
                 '易错点：前缀和数组开 `(m+1)×(n+1)`，查询时下标要 `+1`',
                 '另一种做法：枚举对角线上做不定长滑动窗口，也是 `O(mn)`',
                 '外层循环可改成 `i+ans<m`，实测提升不明显'],
    ),
)
