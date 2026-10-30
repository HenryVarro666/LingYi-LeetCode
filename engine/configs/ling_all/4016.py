MAT = [[0, 1], [1, 0]]


def _info(S):
    ln = S.get('_line', 0)
    if 'suf_max' in S and 'pre_max' not in S:
        return f"下半部分最大正方形边长 `suf_max = {S['suf_max']}`（`suf_max[i]` = 第 i 行及以下）"
    if 'pre_max' in S:
        return f"上半 `pre_max = {S['pre_max']}`，下半 `suf_max = {S['suf_max']}`，`ans = {S['ans']}`（边长）"
    return ''


CONFIG = dict(
    num=4016, title='两个不重叠子正方形的最大面积', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 + 最大正方形 DP · 转置复用',
    tags=['灵神题单·单调栈', '灵神题单·动态规划', '难度分 1959'],
    code='''
class Solution:
    def calc(self, mat: list[list[int]]) -> int:
        m, n = len(mat), len(mat[0])

        # 221. 最大正方形（空间优化写法）
        # 计算 mat 下半部分的最大正方形的边长
        suf_max = [0] * (m + 1)
        f = [0] * (n + 1)
        for i in range(m - 1, 0, -1):
            last = 0
            for j, x in enumerate(mat[i]):
                if x:
                    tmp = f[j + 1]
                    f[j + 1] = min(last, f[j + 1], f[j]) + 1
                    last = tmp
                else:
                    f[j + 1] = 0
                    last = 0
            suf_max[i] = max(suf_max[i + 1], max(f))

        # 计算 mat 上半部分的最大正方形的边长
        ans = pre_max = 0
        f = [0] * (n + 1)
        for i, row in enumerate(mat):
            last = 0
            for j, x in enumerate(row):
                if x:
                    tmp = f[j + 1]
                    f[j + 1] = min(last, f[j + 1], f[j]) + 1
                    last = tmp
                else:
                    f[j + 1] = 0
                    last = 0
            if suf_max[i + 1] <= ans:
                break  # 最优性优化：继续循环不会让 ans 变大
            pre_max = max(pre_max, max(f))
            ans = max(ans, min(pre_max, suf_max[i + 1]))  # 题目要求两个正方形的边长相等

        return ans * ans

    def maxArea(self, mat: list[list[int]]) -> int:
        return max(self.calc(mat), self.calc(list(zip(*mat))))
''',
    call=f'Solution().maxArea({MAT})',
    expect=1,
    views=[
        dict(type='grid', var='mat', h=200, cell=64, label='mat（当前处理的 calc：行 i 蓝色）',
             cursors=[('i', 'j', 'blue', '(i,j)')]),
        dict(type='array', var='f', label='f（最大正方形 DP，f[j+1] = 以当前行第 j 列为右下角的边长）', h=170,
             pointers={'j+1': 'blue'}),
        dict(type='array', var='suf_max', label='suf_max（第 i 行及以下的最大边长）', h=150),
        dict(type='text', fn=_info, size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('pre_max', 'pre_max', 'cyan'), ('ans', 'ans', 'green')],
    skip=['last = 0', 'tmp = f[j + 1]', 'last = tmp', 'for j, x in enumerate'],
    captions={
        'm, n = len(mat)': '`calc` 只处理“一上一下”两个正方形；一左一右把 `mat` 转置再调用一次',
        'suf_max = [0] * (m + 1)': '`suf_max[i]`：行 `i..m-1` 里最大正方形的边长，末尾 0 是哨兵',
        'f = [0] * (n + 1)': lambda S, B, r: ('`f[j+1]`：以当前行第 `j` 列为右下角的最大正方形边长（221 题空间优化写法）' if 'pre_max' not in S else '`f` 清零，再从上往下算上半部分的 221'),
        'for i in range(m - 1, 0, -1)': '从下往上扫，算每个后缀的最大边长；第 0 行不用算，上方至少要留一行',
        'if x:': lambda S, B, r: f"`mat[行][{S.j}] = {S.x}` → " + ('是 1，能当正方形右下角' if S.x else '是 0，不能'),
        'f[j + 1] = min(last': '`f[j+1] = min(左上 {B.last}, 上 {B.f[j+1]}, 左 {f[j]}) + 1` = =={f[j+1]}==：三面都撑得住才能扩大',
        'f[j + 1] = 0': '`x = 0`：这格不能当右下角，`f[j+1] = 0`',
        'suf_max[i] = max': '`suf_max[{i}] = max(suf_max[{i+1}], max(f))` = =={suf_max[i]}==：第 {i} 行及以下最大边长',
        'ans = pre_max = 0': '`pre_max` 是上半部分最大边长，`ans` 是目前最优边长',
        'if suf_max[i + 1] <= ans': lambda S, B, r: (
            f"下半最大边长 `{S.suf_max[S.i + 1]}` ≤ `ans = {S.ans}` → ==继续也不会让 ans 变大==，提前结束"
            if S.suf_max[S.i + 1] <= S.ans else f"下半最大边长 `{S.suf_max[S.i + 1]}` > `ans = {S.ans}`，还有提升空间，继续"),
        'pre_max = max': '上半（行 `0..{i}`）最大边长 `pre_max = {pre_max}`',
        'ans = max(ans': '两个正方形边长要相等 → 取 `min(上半 {pre_max}, 下半 {suf_max[i+1]})`，`ans` → =={ans}==',
        'return ans * ans': '边长 `{ans}` → 面积 =={ret}==',
        'return max(self.calc': lambda S, B, r: ('一上一下与一左一右（转置）两种情况取较大者' if r is None else f'两种情况取较大者 =={r}=='),
    },
    cards=dict(
        one_liner='两个正方形必有一条分割线：上下分，或左右分（转置）',
        complexity='时间 `O(mn)`，空间 `O(mn)`（不转置可做到 `O(m+n)`）',
        problem=['`m×n` 的 0/1 矩阵，选两个==边长相同、不共享格子==的全 1 正方形',
                 '返回单个正方形的最大面积，选不出两个则返回 `0`',
                 '示例：`[[1,1,1,0],[1,1,1,1],[0,0,1,1]]` → `4`',
                 '本视频：`[[0,1],[1,0]]` → `1`（示例 2）'],
        quote='两个不重叠的正方形，要么一左一右，要么一上一下。……代码实现时，可以直接把 mat 转置，从而复用同一段代码。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举水平分割线：上半部分和下半部分各算一次 221 最大正方形',
              '取两边较小的边长（题目要求两个正方形边长相等）',
              '前后缀分解：先算 `suf_max`，再从上往下算 `pre_max`，一左一右转置后再来一遍'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（转置占用）',
                 '依据：有边长 `k` 的正方形，就一定有更小边长的正方形，所以取 `min` 是对的',
                 '易错：`suf_max` 的循环到 `1` 为止（上半至少要留一行）',
                 '`ans` 是边长，最后才平方；`if suf_max[i+1] <= ans: break` 是最优性剪枝',
                 '221 题还可用单调栈或二分答案 + 二维前缀和'],
    ),
)
