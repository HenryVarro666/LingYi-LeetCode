ARR = [[3, 1, 4], [2, 6, 5], [7, 1, 2]]

CONFIG = dict(
    num=1289, title='下降路径最小和 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='逐行 DP · 只保留最小与次小',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def minFallingPathSum(self, arr):

        n = len(arr)
        f = arr[0][:]

        for i in range(1, n):
            m1 = m2 = None
            p = None
            for j, num in enumerate(f):
                if m1 is None:
                    m1 = num
                    p = j
                elif m1 > num:
                    m2 = m1
                    m1 = num
                    p = j
                elif m2 is None or m2 > num:
                    m2 = num

            g = arr[i][:]
            for j in range(n):
                if j != p:
                    g[j] += m1
                else:
                    g[j] += m2
            
            f = g[:]

        return min(f)
''',
    call=f'Solution().minFallingPathSum({ARR})',
    expect=4,
    skip=['for i in range', 'for j, num in', 'for j in range', 'n = len', 'm1 = m2 = None', 'p = None'],
    views=[
        dict(type='grid', var='arr', label='arr（蓝框 = 上一行最小值的位置 p）', cell=80, h=250,
             cursors=[('i - 1', 'p', 'blue')]),
        dict(type='array', var='f', label='f（上一行：以第 j 列结尾的最小和；蓝 = 最小值位置 p）', cell=90, h=160,
             pointers={'p': 'blue', 'j': 'pink'}),
        dict(type='array', var='g', label='g（当前行）', cell=90, h=150),
        dict(type='text', fn=lambda S: (f"最小 `m1 = {S.get('m1')}`（第 {S.get('p')} 列），次小 `m2 = {S.get('m2')}`" if 'm1' in S else ''), size=24, h=50),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'pink'), ('m1', 'm1', 'blue'), ('m2', 'm2', 'orange'), ('p', 'p', 'blue')],
    captions={
        'n = len': '`n = {n}`：方阵，行列数相同',
        'f = arr[0][:]': '第 0 行：`f` = 第 0 行本身 {f}',
        'if m1 is None': lambda S, B, r: ('第一个数：先当最小值' if S.m1 is None else f'`m1 = {S.m1}` 已有，不是第一个数'),
        'elif m1 > num': lambda S, B, r: (f'`m1 = {B.m1} > {S.num}`：更小的数出现 → 旧最小退为次小 `m2 = {B.m1}`，新最小 `m1 = {S.num}`，`p = {S.j}`'
                                          if B.m1 > S.num else f'`m1 = {B.m1} ≤ {S.num}`：不是新最小，看是不是次小'),
        'elif m2 is None': lambda S, B, r: (f'次小还没有或 `m2 = {B.m2}` > `{S.num}` → 次小更新为 `{S.num}`' if (B.m2 is None or B.m2 > S.num)
                                            else f'`m2 = {B.m2} ≤ {S.num}`：不更新'),
        'm2 = num': '`m2 = {m2}`',
        'g = arr[i][:]': '本行 `g` 先复制 `arr[{i}]`，再各自加上「上一行不同列的最小值」',
        'if j != p': lambda S, B, r: (f'列 `{S.j}` ≠ 最小值所在列 `p = {S.p}` → 可以接最小值 `m1 = {S.m1}`' if S.j != S.p
                                      else f'列 `{S.j}` = `p`：不能同列 → 只能接次小值 `m2 = {S.m2}`'),
        'g[j] += m1': '`g[{j}] = {arr[i][j]} + {m1}` = =={g[j]}==',
        'g[j] += m2': '`g[{j}] = {arr[i][j]} + {m2}` = =={g[j]}==（避开同一列）',
        'f = g[:]': '滚动：`f` ← `g` = {f}',
        'return min(f)': '最后一行取最小：`min(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='上一行只需记住最小和次小：同列时改用次小',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n x n` 整数方阵，每行选一个数，==相邻两行选的数不能在同一列==',
                 '求选出的数之和的最小值',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]` → `13`（`1 + 5 + 7`）',
                 '本视频：`[[3,1,4],[2,6,5],[7,1,2]]` → `4`'],
        quote='若上一层最小的位置就是j，此时就应当从上一层次小的位置转移过来。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[j]`：选到当前行第 `j` 列时的最小和',
              '转移应取上一行==最小值==；但如果最小值恰好在同一列，就取==次小值==',
              '所以每行只需保留最小、次小和最小的位置，一遍扫描 `O(n)`'],
        summary=['时间 `O(n^2)`，空间 `O(n)`（滚动数组）',
                 '易错：最小值所在列 `p` 只对 `p` 这一列特殊，其他列都接 `m1`',
                 '易错：`n = 1` 时没有第二行，直接返回唯一的数；`m2` 保持 `None` 不会被用到',
                 '题面库里缺失，题意按 yiduobo 文章和 LeetCode 原题补写'],
    ),
)
