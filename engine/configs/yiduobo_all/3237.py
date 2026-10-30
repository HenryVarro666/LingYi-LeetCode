CONFIG = dict(
    num=3237, title='Alt和Tab模拟', difficulty='Medium', category='模拟',
    author='yiduobo', technique='倒序遍历 queries + 哈希集合',
    code='''
class Solution(object):
    def simulationResult(self, windows, queries):

        vis = set()
        res = []
        for q in queries[::-1]:
            if q not in vis:
                res.append(q)
                vis.add(q)
        
        for v in windows:
            if v not in vis:
                res.append(v)
                vis.add(v)

        return res
''',
    call='Solution().simulationResult([1,2,3,4,5,6], [3,5,3,2])',
    expect=[2, 3, 5, 1, 4, 6],
    views=[
        dict(type='array', var='windows', label='windows（初始顺序，前面的在最前）', h=200,
             color=lambda S, i, v: 'green' if v in S.get('vis', ()) else None),
        dict(type='array', var='queries', label='queries（依次切到最前）', h=200,
             color=lambda S, i, v: 'blue' if S.get('q') == v else None),
        dict(type='array', var='res', label='res（最终顺序，已确定的前缀）', h=200, color=lambda S, i, v: 'yellow'),
        dict(type='set', var='vis', label='vis（已放进 res 的窗口）', h=160),
    ],
    watch=[('q', 'q', 'blue'), ('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'vis = set()': '`vis` 记录哪些窗口已经放进答案',
        'res = []': '`res` 保存最终的窗口顺序',
        'for q in queries[::-1]': '倒序看 queries：==越靠后的切换，窗口越靠前==。取 `q = {q}`',
        'if q not in vis': lambda S, B, r: (f'`{S.q}` 不在 `vis` 里：它是倒序的首次出现，也就是正序的==最后一次切换=='
                                            if S.q not in S.vis else f'`{S.q}` 已在 `vis` 里：更早的切换被后来的覆盖，跳过'),
        'res.append(q)': '`{q}` 加入答案：`res = {res}`',
        'vis.add(q)': '标记 `{q}` 已出现',
        'for v in windows': '再顺序看 windows，取 `v = {v}`',
        'if v not in vis': lambda S, B, r: (f'`{S.v}` 没被切换过 → 保持原相对顺序，排在已切换窗口后面'
                                            if S.v not in S.vis else f'`{S.v}` 切换过，已经在答案里，跳过'),
        'res.append(v)': '`{v}` 加入答案：`res = {res}`',
        'vis.add(v)': '标记 `{v}` 已出现',
        'return res': '最终窗口顺序 ==`{ret}`==',
    },
    cards=dict(
        one_liner='倒着看切换记录：最后切到的窗口排最前',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['`windows` 是 1~n 的排列，表示窗口从前到后的顺序',
                 '`queries[i]` 表示把该窗口切换到最前面，依次执行',
                 '本视频：`windows=[1..6]`，`queries=[3,5,3,2]` → `[2,3,5,1,4,6]`'],
        quote='对于queries中的窗口，最后一次切换越靠后的，在windows中的位置就越靠前。',
        quote_src='—— yiduobo 题解原文',
        idea=['被切换过的窗口都在前面，没切换过的保持原顺序排在后面',
              '倒序遍历 `queries`，每个窗口只取==第一次遇到==的（正序的最后一次）',
              '再顺序遍历 `windows`，把没出现过的接在后面'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '易错：倒序里的首次 = 正序里的最后一次，重复切换只算一次',
                 '没切换过的窗口保持原来的相对顺序',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
