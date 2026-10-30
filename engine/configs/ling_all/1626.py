SC0, AG0 = [4, 5, 6, 5, 2], [2, 1, 2, 1, 3]


def _top(S):
    sc, ag = S.get('score'), S.get('age')
    if sc is None:
        return '`t[x]` 存的是树状数组里“年龄 ≤ x 这一段”的最大得分和'
    return f'当前球员：分数 `{sc}`，年龄 `{ag}`（按分数从小到大处理）'


def _tcol(S, k, v):
    i = S.get('i')
    if i is None or k != i:
        return None
    ln = S.get('_line_text', '')
    return 'blue'


def _cq(S, B, r):
    return None


CONFIG = dict(
    num=1626, title='无矛盾的最佳球队', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='排序 + 树状数组优化 LIS',
    tags=['灵神题单', '动态规划', '难度分 2027'],
    code='''
class Solution:
    def bestTeamScore(self, scores: List[int], ages: List[int]) -> int:
        u = max(ages)
        t = [0] * (u + 1)

        # 返回 max(max_sum[:i+1])
        def query(i: int) -> int:
            mx = 0
            while i:
                mx = max(mx, t[i])
                i &= i - 1
            return mx

        # 更新 max_sum[i] 为 mx
        def update(i: int, mx: int) -> None:
            while i < len(t):
                t[i] = max(t[i], mx)
                i += i & -i

        for score, age in sorted(zip(scores, ages)):
            update(age, query(age) + score)
        return query(u)
''',
    call=f'Solution().bestTeamScore({SC0}, {AG0})',
    expect=16,
    skip=['for score, age in', 'while i:', 'while i < len(t)', 'mx = 0'],
    max_steps=80,
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='array', var='t', label='树状数组 t（蓝 = 当前访问的下标，t[0] 不用）', h=230, cell=100,
             pointers={'i': 'blue'}),
        dict(type='text', fn=lambda S: (f"`query` 在累计前缀最大值 `mx = {S['mx']}`" if 'mx' in S and 'i' in S and S.get('_line') in (9, 10, 11, 12)
                                       else ''), size=24, h=60),
    ],
    watch=['score', 'age', 'i', 'mx'],
    captions={
        'u = max(ages)': '年龄的最大值 `u = {u}`，树状数组下标是 ==年龄==（值域）',
        't = [0] * (u + 1)': '`t` 长 `u + 1`，下标 0 不用；`mx` 从 0 开始统计前缀最大值',
        'mx = 0': '`mx = 0`：开始统计前缀最大值',
        'mx = max(mx, t[i])': '`mx = max({B.mx}, t[{i}] = {t[i]})` = =={mx}==',
        'i &= i - 1': lambda S, B, r: f'`i &= i - 1` 去掉最低位的 1：`i` → {S.i}' + ('（跳到前一段）' if S.i else '，前缀查完了'),
        'return mx': '返回前缀最大值 =={ret}==（年龄不超过查询值的最大总分）',
        't[i] = max(t[i], mx)': '`t[{i}] = max({B.t[i]}, {mx})` = =={t[i]}==',
        'i += i & -i': lambda S, B, r: f'`i += i & -i` 加上最低位：`i` → {S.i}' + ('（跳到包含它的下一段）' if S.i < len(S.t) else '，越界，更新完毕'),
        'update(age, query(age) + score)': '球员（分 `{score}`，龄 `{age}`）：先 `query({age})` 查年龄 ≤ {age} 的最大总分，加上 `{score}`，再 `update` 写回',
        'return query(u)': '所有球员处理完：答案 = 整个值域的前缀最大值 `query({u})`',
    },
    cards=dict(
        one_liner='按分数排序后，就是求年龄的“带权最长不降子序列”，前缀最大值交给树状数组',
        complexity='时间 `O(n log n + n log U)`，空间 `O(n + U)`',
        problem=['球员分数 `scores[i]`、年龄 `ages[i]`：年龄小的分数严格大于年龄大的，就有矛盾',
                 '选一支==无矛盾==的球队，使总分最大',
                 '示例：`scores = [4,5,6,5]`，`ages = [2,1,2,1]` → `16`'],
        quote='循环中计算的是 maxSum 的前缀最大值，这可以用树状数组（或者线段树）优化至 O(log U)。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['先按分数从小到大排序（同分按年龄），这样只需要看年龄不下降',
              '`max_sum[x]`：年龄最大值恰好为 `x` 的球队的最大总分',
              '转移要的是 `max_sum[1..age]` 的前缀最大值 → 用树状数组 `query` / `update` 做到 `O(log U)`'],
        summary=['时间 `O(n log n + n log U)`，空间 `O(n + U)`',
                 '易错：排序要先分数后年龄，同分的年龄小的要排前面',
                 '易错：树状数组下标从 1 开始，年龄正好可以当下标；`update` 取 max，不是累加',
                 '灵神另有两种写法：`O(n^2)` 的 LIS 式 DP、按值域直接取前缀最大值',
                 '同类题：300 最长递增子序列、354 俄罗斯套娃、1691 堆叠长方体'],
    ),
)
