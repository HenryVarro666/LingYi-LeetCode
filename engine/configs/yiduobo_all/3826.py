def _t(S):
    if S.get('_line', 0) < 14 or 'mid' not in S.get('_inner', {}):
        return '`f[i]`：前 i 个元素分成 j 段的最小分数；`g` 是上一层的 `f`'
    I = S['_inner']
    return (f"区间 `[{I['x']}, {I['y']}]` 的中点 `mid = {I['mid']}`，决策点只在 `[{I['left']}, {I['right']}]` 里找；"
            f"当前最优 `p = {I['mi_p']}`，分数 = =={I['mi']}==")


def _cell(S, i, v):
    I = S.get('_inner', {})
    if 'mid' in I and i == I['mid']:
        return 'yellow'
    return None


CONFIG = dict(
    num=3826, title='最小分割分数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='划分型 DP + 决策单调性（分治优化）',
    tags=['动态规划', '难度分 2345'],
    code='''
class Solution(object):
    def minPartitionScore(self, nums, k):

        n = len(nums)
        s = [0]
        for v in nums:
            s.append(s[-1] + v)

        def calc(x, y, left, right):
            mid = (x + y) // 2
            mi = None
            mi_p = None
            for p in range(left, right + 1):
                if g[p] is not None:
                    cost = g[p] + (s[mid] - s[p]) * (s[mid] - s[p] + 1) // 2
                    if mi is None or mi > cost:
                        mi = cost
                        mi_p = p

            f[mid] = mi
            if x < mid:
                calc(x, mid - 1, left, mi_p)
            if mid < y:
                calc(mid + 1, y, mi_p, right)

        f = [None] * (n + 1)
        f[0] = 0
        for _ in range(k):
            g = f[:]
            f = [-1] * (n + 1)

            calc(1, n, 0, n - 1)

        return f[-1]
''',
    call='Solution().minPartitionScore([5,1,2], 2)',
    expect=21,
    views=[
        dict(type='array', var='s', label='s（前缀和）', h=165, cell=80,
             color=lambda S, i, v: _cell(S, i, v)),
        dict(type='array', var='g', label='g（上一层 f，-1 / None 无效）', h=165, cell=80,
             color=lambda S, i, v: 'blue' if S.get('_inner', {}).get('p') == i else None),
        dict(type='array', var='f', label='f（分成 j 段的最小分数）', h=165, cell=80,
             color=lambda S, i, v: _cell(S, i, v)),
        dict(type='calls', h=130),
        dict(type='text', fn=_t, size=24, h=60),
    ],
    watch=['mid', ('p', 'p', 'blue'), ('cost', 'cost', 'yellow'), ('mi', 'mi', 'green'), ('mi_p', 'mi_p', 'pink')],
    skip=['n = len', 's = [0]', 's.append', 'for v in nums', 'def calc', 'for _ in range(k)', 'f = [None]', 'f[0] = 0',
          'mi = None', 'mi_p = None', 'for p in range', 'if g[p] is not None', 'mi_p = p', 'if mi is None', 'if x < mid', 'if mid < y'],
    captions={
        'mid = (x + y)': '先算区间 `[{x}, {y}]` 的中点 `mid = {mid}`，暴力找它的最优决策点；决策点范围只有 `[{left}, {right}]`',
        'if g[p] is not None': '枚举最后一段的起点 `p + 1`，`p = {p}`：`g[{p}]` {"可用" if g[p] is not None else "不存在（分不成这么多段），跳过"}',
        'cost = g[p]': '`cost = g[{p}] + (s[{mid}] − s[{p}])·(…+1)//2` = =={cost}==',
        'mi = cost': '比之前更小 → 记下最优决策点 `mi_p = {p}`，`mi = {cost}`',
        'f[mid] = mi': '`f[{mid}] = {mi}`：前 `{mid}` 个元素的最优分割，最后一段从 `{mi_p}` 之后开始',
        'calc(x, mid - 1': '决策点单调：`mid` 左边的位置，最优决策点只会 ≤ `{mi_p}` → 递归 `[{x}, {mid-1}]`，范围缩成 `[{left}, {mi_p}]`',
        'calc(mid + 1': '`mid` 右边的位置，最优决策点只会 ≥ `{mi_p}` → 递归 `[{mid+1}, {y}]`，范围缩成 `[{mi_p}, {right}]`',
        'g = f[:]': '进入下一层（多分一段）：把当前的 `f` 复制成 `g`，`f` 重新清空',
        'return f[-1]': '分成 `k` 段的最小分数 = =={ret}==',
    },
    cards=dict(
        one_liner='最优决策点随 i 单调不减：每次只找中点，其余分治',
        complexity='时间 `O(n·k·log n)`，空间 `O(n)`',
        problem=['把 `nums` 分成恰好 `k` 段，每段的值是 `sum·(sum+1)/2`，求总分最小',
                 '示例：`nums=[5,1,2,1]`，`k=2` → `25`（`[5]` 和 `[1,2,1]`）',
                 '本视频：`nums=[5,1,2]`，`k=2` → `21`'],
        quote='f[i + 1][j]对应的最优决策点p\'必然大于等于f[i][j]的最优决策点p。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j] = min(f[p][j-1] + cost(p+1, i))`，前缀和 `s` 算 `cost`，朴素是 `O(n²k)`',
              '反证可得：`i` 变大，最优 `p` 不会变小（决策单调性），简单的单调队列用不了',
              '对每个 `j`：枚举区间中点的全部决策点，左半区间只看 `≤ p`，右半区间只看 `≥ p`，递归'],
        summary=['时间 `O(n·k·log n)`，空间 `O(n)`',
                 '`g[p]` 为 `None` 表示前 `p` 个元素分不成 `j-1` 段，必须跳过',
                 '每层 `j` 都新建 `f`，旧值留在 `g` 里；第 2 层起 `g[0]` 是 -1（原文遗留），这个无效起点不会比合法分割更优，答案不受影响',
                 '原文已是 Python 3 兼容写法，代码未改动；灵神的斜率优化是 `O((n−k)k)`，这里是更好想的分治优化'],
    ),
)
