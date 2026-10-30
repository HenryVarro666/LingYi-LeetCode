def _ph2(S):
    return 'f' in S


def _w0(S):
    if not _ph2(S):
        return S['i']
    return S['cut_pos'] if 'cut_pos' in S and S['j'] > 1 else 0


def _w1(S):
    return S['i'] if _ph2(S) else S['j']


def _dis_color(S, r, c, v):
    if 'i' not in S or 'j' not in S:
        return None
    if not _ph2(S):
        if (r, c) == (S['i'], S['j']):
            return 'yellow'
        if (r, c) == (S['i'] + 1, S['j'] - 1):
            return 'blue'
        return None
    if S['j'] == 1:
        return 'yellow' if (r, c) == (0, S['i']) else None
    if 'cut_pos' in S and (r, c) == (S['cut_pos'], S['i']):
        return 'yellow'
    return None


def _formula(S):
    if not _ph2(S):
        return '`dis[i][j]`：一个邮筒管 `i..j`，放中位数，==累加外圈=='
    j = S['j']
    return f'`f[i]`：前 i+1 栋用 {j} 个邮筒；`g`：上一轮（{j - 1} 个）'


def _cap_dis_else(S, B, ret):
    h = S.houses
    return (f'外圈一对：`houses[{S.j}] − houses[{S.i}] = {h[S.j] - h[S.i]}`，'
            f'再加里面 `dis[{S.i + 1}][{S.j - 1}] = {S.dis[S.i + 1][S.j - 1]}` → `dis[{S.i}][{S.j}]` = =={S.dis[S.i][S.j]}==')


def _cap_f_cut(S, B, ret):
    cand = S.g[S.cut_pos - 1] + S.dis[S.cut_pos][S.i]
    return (f'最后一个邮筒管 `[{S.cut_pos}..{S.i}]`：前面 `g[{S.cut_pos - 1}] = {S.g[S.cut_pos - 1]}`'
            f' + `dis[{S.cut_pos}][{S.i}] = {S.dis[S.cut_pos][S.i]}` = =={cand}==')


def _cap_better(S, B, ret):
    return f'`f[{S.i}]` 更新为 =={S.f[S.i]}==（更小的划分）'


CONFIG = dict(
    num=1478, title='安排邮筒', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 dis 预处理 + 划分型 DP',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def minDistance(self, houses, k):

        houses = sorted(houses)
        n = len(houses)
        dis = [[None] * n for _ in range(n)]
        for l in range(n):
            for i in range(n):
                j = i + l
                if j > n - 1:
                    break
                if i == j:
                    dis[i][j] = 0
                elif i == j - 1:
                    dis[i][j] = houses[j] - houses[i]
                else:
                    dis[i][j] = dis[i + 1][j - 1] + houses[j] - houses[i]

        for j in range(1, k + 1):
            f = [None] * n
            for i in range(n):
                if j == 1:
                    f[i] = dis[0][i]
                elif j >= i + 1:
                    f[i] = 0
                else:
                    for cut_pos in range(j - 1, i + 1):
                        if f[i] is None or f[i] > g[cut_pos - 1] + dis[cut_pos][i]:
                            f[i] = g[cut_pos - 1] + dis[cut_pos][i]

            g = f[:]

        return f[-1]
''',
    call='Solution().minDistance([7, 4, 6, 1], 2)',
    expect=3,
    skip=[7, 8, 9, 10, 11, 12, 14, 16, 20, 21, 22, 24, 26, 27, 30, 31],
    views=[
        dict(type='text', fn=_formula, size=22, h=50),
        dict(type='array', var='houses', label='houses（排序后）', window=(_w0, _w1), h=120, cell=56, index=False),
        dict(type='table', var='dis', label='dis[l][r]', color=_dis_color, h=240, cell=52),
        dict(type='array', var='g', label='g（上一轮）', pointers={'cut_pos - 1': 'pink'}, h=165, cell=56),
        dict(type='array', var='f', label='f（本轮）', pointers={'i': 'blue'}, h=165, cell=56),
    ],
    watch=[('l', 'l', 'purple'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), 'cut_pos'],
    captions={
        4: '先把房子按位置排序：`{houses}`',
        6: '`dis[l][r]`：一个邮筒管 `l..r` 这些房子的最小距离，先建空表',
        13: '`i = j = {i}`：只有一栋房子 → 邮筒就建在它上面，距离 ==0==',
        15: '`i = {i}, j = {j}` 两栋房子：邮筒放中间任何位置都一样 → `dis[{i}][{j}] = {houses[j]} − {houses[i]}` = =={dis[i][j]}==',
        17: _cap_dis_else,
        19: lambda S, B, r: (f'第 `{S.j}` 轮：用 `{S.j}` 个邮筒，`g` 记着 `{S.j - 1}` 个邮筒的结果' if B.get('j') != S.j else '`k` 轮都做完了，`f` 就是最终一轮的结果'),
        23: '只有 1 个邮筒：管前 `{i + 1}` 栋 → `f[{i}] = dis[0][{i}]` = =={f[i]}==',
        25: '邮筒数 `{j}` ≥ 房子数 `{i + 1}` → 每栋房子一个邮筒，`f[{i}] = 0`',
        28: _cap_f_cut,
        29: _cap_better,
        33: '最后一轮 `f[-1]`：全部房子、`k` 个邮筒的最小总距离 = =={ret}==',
    },
    cards=dict(
        one_liner='邮筒放中位数；再枚举最后一个邮筒管哪一段',
        complexity='时间 `O(n²·k)`，空间 `O(n²)`',
        problem=['一条街上有若干房子 `houses[i]`（坐标），要建 `k` 个邮筒（建在房子上）',
                 '每栋房子到最近邮筒的距离之和要最小，求这个最小值',
                 '示例：`houses=[1,4,8,10,20], k=3` → `5`；本视频：`[7,4,6,1], k=2` → `3`'],
        quote='令f[i][j]表示前i栋房子，安排j个邮筒的最小距离总和。',
        quote_src='—— yiduobo 题解原文',
        idea=['先预处理 `dis[l][r]`：一个邮筒管 `l..r`，放在==中位数==，总距离 = 外圈一对的间距 + 里圈的 `dis`',
              '再做划分：最后一个邮筒管 `[cut_pos..i]`，前面交给 `j-1` 个邮筒',
              '`j` 这一维只依赖上一轮，用 `g` 滚动掉'],
        summary=['时间 `O(n²·k)`（dis 是 `O(n²)`，DP 是 `O(n·k·n)`），空间 `O(n²)`',
                 '一定要先排序；`dis[l][r] = dis[l+1][r-1] + houses[r] − houses[l]`，按区间长度从小到大填',
                 '邮筒数 `≥` 房子数时答案是 `0`，别漏这个边界',
                 '原文为 Python 2 风格，本题无需改动（代码已兼容 Python 3），只是去掉了空行里的空格'],
    ),
)
