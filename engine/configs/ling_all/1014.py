CONFIG = dict(
    num=1014, title='最佳观光组合', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左',
    tags=['灵神题单', '难度分 1730'],
    code='''
class Solution:
    def maxScoreSightseeingPair(self, values: List[int]) -> int:
        ans = mx = 0  # mx 表示 j 左边的 values[i] + i 的最大值
        for j, v in enumerate(values):
            ans = max(ans, mx + v - j)
            mx = max(mx, v + j)
        return ans
''',
    call='Solution().maxScoreSightseeingPair([8,1,5,2,6])',
    expect=11,
    views=[
        dict(type='array', var='values', label='values（蓝箭头 = 当前 j）', pointers={'j': 'blue'}, h=200, cell=100,
             dim=lambda S, i, v: 'j' in S and i > S['j'],
             color=lambda S, i, v: 'blue' if S.get('j') == i else None),
        dict(type='text', size=30, h=120,
             fn=lambda S: (f"左边最优：`mx = {S['mx']}`（= 某个 v_i + i）；"
                           f"得分 = `mx + v_j − j` = `{S['mx']} + {S['values'][S['j']]} − {S['j']}` = =={S['mx'] + S['values'][S['j']] - S['j']}=="
                           if 'j' in S else '得分 = (v_i + i) + (v_j − j)，拆成两个互不相干的部分')),
    ],
    watch=[('j', 'j', 'blue'), ('v', 'v'), ('mx', 'mx', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = mx = 0': '`ans`、`mx` 都从 0 开始：`mx` 记录 ==j 左边 v_i + i 的最大值==（v ≥ 1，初始化成 0 不会出错）',
        'for j, v': lambda S, B, r: (f'枚举右端点 `j = {S.j}`，`v = {S.v}`' if 'j' in S and ('j' not in B or S.j != B.j) else '遍历结束'),
        'ans = max': '用左边最优配 j：`mx + v − j = {mx} + {v} − {j} = {mx + v - j}`，`ans = max({B.ans}, {mx + v - j}) = {ans}`',
        'mx = max': '==先更新答案，再更新 mx==：现在才把 `v + j = {v + j}` 并入，`mx` = {mx}（供后面的 j 使用）',
        'return ans': '最高得分 `{ans}`',
    },
    cards=dict(
        one_liner='把得分拆成 (v_i + i) + (v_j − j)，枚举 j，维护左边的最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`values[i]` 是景点评分，一对 `i < j` 的得分 = `values[i] + values[j] + i - j`',
                 '求最高得分',
                 '示例：`[8,1,5,2,6]` → `11`（i=0, j=2）'],
        quote='可以变形为 (v_i + i) + (v_j - j)。我们可以枚举 j，同时维护在 j 左边的 v_i + i 的最大值 mx，用 mx + v_j - j 更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['式子拆开后，i 的部分和 j 的部分互不相干',
              '枚举右边的 j，左边只要一个最大的 `v_i + i`',
              '==先更新答案，再更新 mx==，保证 mx 只来自 j 左边'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：先算答案再更新 `mx`，否则会拿 j 自己配对',
                 '`mx` 初始化成 0 在本题可行：v ≥ 1 且至少两个数，答案不会比 v0 小',
                 '同类题：枚举右，维护左（121 买卖股票、2905、3584）'],
    ),
)
