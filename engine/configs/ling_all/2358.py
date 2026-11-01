CONFIG = dict(
    num=2358, title='分组的最大数量', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 模拟分组（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1503'],
    code='''
class Solution:
    def maximumGroups(self, grades: List[int]) -> int:
        ans = 0
        grades.sort()
        i = pre_sum = k = 0
        n = len(grades)
        while i + k < n:
            i0, sum = i, 0  # i0 保存本次循环的起始下标
            while i < n and (sum <= pre_sum or i <= i0 + k):  # 必须满足题目的两个要求
                sum += grades[i]
                i += 1
            if sum <= pre_sum:  # 未能满足要求
                break
            pre_sum, k = sum, i - i0
            ans += 1
        return ans
''',
    call='Solution().maximumGroups([10,6,12,7,3,5])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"本组 `[{S['i0']}, {S['i']})`：人数 `{S['i'] - S['i0']}`，总分 `{S['sum']}`；上一组：人数 `{S['k']}`，总分 `{S['pre_sum']}`" if 'i0' in S and 'sum' in S else '先排序：小的放前面，前面的组才容易"总分更小"'), size=26),
        dict(type='array', var='grades', pointers={'i0': 'blue', 'i': 'pink'}, h=300,
             color=lambda S, idx, v: 'green' if 'i0' in S and 'i' in S and S['i0'] <= idx < S['i'] and S['_line'] in (11, 12, 13, 14, 15, 16) else None,
             dim=lambda S, idx, v: 'i0' in S and 'i' in S and idx < S['i0']),
    ],
    watch=[('i', 'i', 'pink'), ('i0', 'i0', 'blue'), 'sum', 'pre_sum', 'k', ('ans', 'ans', 'green')],
    captions={
        'grades.sort()': '排序后 `{grades}`：元素都是正数，后面的组总分自然更大',
        'i = pre_sum = k': '`i` 是下一个还没分的人；`pre_sum` / `k` 是上一组的总分 / 人数，第一组前都是 0',
        'while i + k < n': lambda S, B, r: (f'`i + k = {S.i + S.k} < n = {S.n}`：剩下的人够凑一个更大的组 → 继续' if S.i + S.k < S.n else f'`i + k = {S.i + S.k} >= n = {S.n}`：剩下的人不够比上一组多 1 人 → 结束'),
        'i0, sum = i': '新开一组，从下标 `{i0}` 开始，总分清零',
        'while i < n and (sum': lambda S, B, r: (f'`sum = {S.sum}`，`pre_sum = {S.pre_sum}`，`i = {S.i}`，`i0 + k = {S.i0 + S.k}` → ==还没满足两个要求，继续拿人==' if (S.i < S.n and (S.sum <= S.pre_sum or S.i <= S.i0 + S.k)) else (f'`i = {S.i} == n`，没人可拿了' if S.i >= S.n else f'`sum = {S.sum} > pre_sum = {S.pre_sum}` 且 人数 `{S.i - S.i0}` > `{S.k}` → ==两个要求都满足，本组结束==')),
        'sum += grades[i]': '把 `grades[{i}] = {grades[i]}` 加入本组：`sum` → {sum}',
        'i += 1': '`i` → {i}',
        'if sum <= pre_sum': lambda S, B, r: (f'`sum = {S.sum} <= pre_sum = {S.pre_sum}`：人拿光了总分还是不够 → ==凑不出新组，break==' if S.sum <= S.pre_sum else f'`sum = {S.sum} > pre_sum = {S.pre_sum}` → 本组合格'),
        'pre_sum, k =': '记下这一组：总分 `pre_sum = {pre_sum}`，人数 `k = {k}`，下一组要比它大',
        'ans += 1': '组数 `ans` → =={ans}==',
        'return ans': '最多分成 `{ans}` 组',
    },
    cards=dict(
        one_liner='排序后从小到大分组，每组刚好比上一组多一个人',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`',
        problem=['给正整数数组 `grades`，把所有学生分成有序的若干组',
                 '后一组的总成绩、人数都要严格大于前一组，求最多分几组',
                 '示例：`[10,6,12,7,3,5]` → `3`'],
        quote='由于元素都是正数，第一个组的元素越小越好。那么排序后，我们可以按照题目要求模拟。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，先分的组用最小的数，后面的组天然总分更大',
              '内层循环不断拿人，直到总分和人数都超过上一组',
              '内外层共用同一个 `i`，所以两重循环总共只扫一遍数组'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n log n)`，空间 `O(1)`；二重循环共用 `i`，是线性的',
                 '易错点：第 `x` 组人数其实就是 `x`，所以答案满足 `x(x+1)/2 <= n`，可直接用 `sqrt` 公式（原文后两种写法）',
                 '最后一组不够大时直接 break，那些人并进前一组'],
    ),
)
