def _lp(names, txt, end):
    def f(S, B, r):
        if all(n in B and B[n] == S[n] for n in names):
            return end
        return txt(S)
    return f


def _in(S, r, c):
    i, j, k = S.get('i'), S.get('j'), S['k']
    if i is None or j is None:
        return False
    return i <= r < i + k and j <= c < j + k


def _diff(S):
    if S.get('_line') in (15, 16, 17, 18) and 'diff' in S:
        return f"相邻差 `diff = {S['diff']}`，当前最小 `mi = {S['mi']}`（0 表示还没有）"
    return '`mi = 0` 表示还没找到合法差；差为 0 的相邻对要跳过'


CONFIG = dict(
    num=3567, title='子矩阵的最小绝对差', difficulty='Medium', category='网格图',
    author='yiduobo', technique='暴力收集子矩阵 · 排序后遍历相邻差',
    tags=[],
    code='''
class Solution(object):
    def minAbsDiff(self, grid, k):
        
        m = len(grid)
        n = len(grid[0])
        res = []
        for i in range(m - k + 1):
            res.append([])
            for j in range(n - k + 1):
                nums = []
                for x in range(i, i + k):
                    for y in range(j, j + k):
                        nums.append(grid[x][y])
                nums.sort()
                mi = 0
                for index in range(1, len(nums)):
                    diff = nums[index] - nums[index - 1]
                    if diff == 0:
                        continue
                    if mi == 0 or mi > diff:
                        mi = diff
                res[-1].append(mi)

        return res
''',
    call='Solution().minAbsDiff([[4,1,4],[2,4,7]], 2)',
    expect=[[1, 3]],
    skip=['m = len', 'n = len', 'res = []'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（蓝框 = 当前 k×k 子矩阵）', h=230, cell=90,
             color=lambda S, r, c, v: 'blue' if _in(S, r, c) else ('yellow' if (r, c) == (S.get('x'), S.get('y')) and S.get('_line') == 13 else None),
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
        dict(type='array', var='nums', label='nums（收集到的元素）', h=170, cell=80,
             color=lambda S, i, v: 'pink' if S.get('_line') in (17, 18, 19, 20, 21) and S.get('index') in (i, i + 1) else None),
        dict(type='text', h=90, size=28, fn=_diff),
        dict(type='text', h=90, size=28, fn=lambda S: f"已得结果 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=['i', 'j', ('mi', 'mi', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for i in range': _lp(['i'], lambda S: f'枚举子矩阵左上角的行 `i = {S.i}`', '所有行都枚举完了，循环结束'),
        'res.append([])': '给结果新开一行',
        'for j in range': _lp(['j'], lambda S: f'枚举左上角的列 `j = {S.j}`', '这一行的列都枚举完了，回到外层'),
        'nums = []': '准备收集 `({i},{j})` 开始的 `{k}×{k}` 子矩阵',
        'for x in range': _lp(['x'], lambda S: f'行 `x = {S.x}`', '`k` 行都收集完了'),
        'for y in range': _lp(['y'], lambda S: f'列 `y = {S.y}`', '这一行的 `k` 个数收集完了'),
        'nums.append': '收集 `grid[{x}][{y}] = {grid[x][y]}`：`nums = {nums}`',
        'nums.sort()': '排序：差最小的两数一定相邻 `{nums}`',
        'mi = 0': '`mi = 0` 代表还没找到合法差',
        'for index in range': _lp(['index'], lambda S: f'比较 `nums[{S.index}-1]` 和 `nums[{S.index}]`', '相邻差都看完了，`mi` 定下来'),
        'diff = nums': '`diff = {nums[index]} - {nums[index - 1]} = {diff}`',
        'if diff == 0': lambda S, B, r: ('`diff = 0`：两数相同，不能算，`continue`' if S.diff == 0 else f'`diff = {S.diff}` ≠ 0：可以参与比较'),
        'if mi == 0 or': lambda S, B, r: (f'`mi = {S.mi}`：还没有或比 `diff = {S.diff}` 大 → 更新' if (S.mi == 0 or S.mi > S.diff) else f'`mi = {S.mi}` 已经不大于 `diff = {S.diff}`，不更新'),
        'mi = diff': '`mi = {mi}`',
        'res[-1].append': '这个子矩阵的答案 `{mi}` 放进结果的最后一行：`res = {res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='数据规模小：收集、排序、一趟扫相邻差',
        complexity='时间 `O((m-k)(n-k)k²logk)`，空间 `O(k²)`',
        problem=['给 `m×n` 矩阵和整数 `k`，对每个 `k×k` 子矩阵求任意两个不同值的最小绝对差',
                 '全部相同则答案为 `0`',
                 '本视频：`[[4,1,4],[2,4,7]], k=2` → `[[1,3]]`'],
        quote='题目的数据规模较小，因此可以直接暴力枚举每个k * k的子矩阵，将其中的元素收集起来，排序后一趟遍历，计算相邻元素间的差值并记录最小差即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['双重循环 `x, y` 把子矩阵元素收进 `nums`',
              '排序后只比较相邻两项，差为 0 就 `continue`',
              '用 `mi = 0` 表示“还没有”，第一个合法差直接赋给 `mi`'],
        summary=['时间 `O((m-k)(n-k)k²logk)`，空间 `O(k²)`',
                 '`mi == 0` 既当“未设置”用：因为合法差必为正，所以不会冲突',
                 '全相同则 `mi` 始终为 `0`，正好是答案',
                 '原文已是 Python 3 可运行写法，只删去了类型说明注释',
                 '对比灵神：灵神用 `pairwise` 和 `inf`，yiduobo 用 `mi=0` 当标记'],
    ),
)
