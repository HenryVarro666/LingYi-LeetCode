CONFIG = dict(
    num=1014, title='最佳观光组合', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='从后往前扫 · 维护最优终点',
    tags=['灵神题单', '难度分 1730'],
    code='''
class Solution(object):
    def maxScoreSightseeingPair(self, values):

        res = 0
        candidate = values[-1] - len(values) + 1
        for index in range(len(values) - 2, -1, -1):
            res = max(res, values[index] + index + candidate)
            candidate = max(candidate, values[index] - index)
        
        return res
''',
    call='Solution().maxScoreSightseeingPair([8,1,5,2,6])',
    expect=11,
    views=[
        dict(type='array', var='values', label='values（蓝箭头 = 当前起点 index，从右往左）', pointers={'index': 'blue'}, h=200, cell=100,
             dim=lambda S, i, v: 'index' in S and i < S['index'],
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='text', size=30, h=120,
             fn=lambda S: (f"起点 {S['index']}：`(values[i] + i) + candidate` = `{S['values'][S['index']] + S['index']} + {S['candidate']}` = =={S['values'][S['index']] + S['index'] + S['candidate']}=="
                           if 'index' in S else '对起点 i，最优终点只看 values[j] − j 最大的 j（j > i）')),
    ],
    watch=[('index', 'index', 'blue'), ('candidate', 'candidate', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录最高得分',
        'candidate = values[-1]': '`candidate`：起点右边 `values[j] − j` 的最大值；一开始只有最后一个位置：`{candidate}`',
        'for index': lambda S, B, r: (f'从后往前枚举起点 `index = {S.index}`' if 'index' in S and ('index' not in B or S.index != B.index) else '扫描结束'),
        'res = max': '`values[i] + i` 配上右边最好的终点：`{values[index] + index} + {candidate}`，`res = max({B.res}, {values[index] + index + candidate}) = {res}`',
        'candidate = max': '==先算答案，再更新 candidate==：把 `values[i] − i = {values[index] - index}` 并入 → `candidate = {candidate}`',
        'return res': '最高得分 `{res}`',
    },
    cards=dict(
        one_liner='起点定了，最优终点与起点无关：只看 values[j] − j 最大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`values[i]` 是景点评分，`i < j` 的得分 = `values[i] + values[j] + i - j`',
                 '求最高得分',
                 '示例：`[8,1,5,2,6]` → `11`'],
        quote='从i出发时最优的终点与i自身无关，而是要找到从i + 1开始values[j] - j最大的位置j。',
        quote_src='—— yiduobo 题解原文',
        idea=['对起点 i，得分 = `(values[i] + i) + (values[j] − j)`',
              '比较不同终点 p、q，只差 `values[p] − p` 与 `values[q] − q`',
              '所以从后往前扫，边走边维护 `candidate`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：先用 candidate 更新答案，再把当前位置并入 candidate',
                 '对比灵神：灵神从左往右、维护 `v_i + i` 的最大值；yiduobo 从右往左、维护 `v_j − j`',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
