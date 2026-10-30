CONFIG = dict(
    num=3767, title='选择 K 个任务的最大总分数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先全选技巧 2，再选 diff 最大的', tags=['灵神题单', '贪心与思维', '难度分 1704'],
    code='''
class Solution(object):
    def maxPoints(self, technique1, technique2, k):
        
        diff = sorted([x - y for x, y in zip(technique1, technique2)], reverse=True)
        res = sum(technique2) + sum(diff[:k])
        p = k
        while p < len(diff) and diff[p] > 0:
            res += diff[p]
            p += 1
        
        return res
''',
    call='Solution().maxPoints([5,2,10,4,7,3], [10,3,8,9,1,6], 1)',
    expect=45,
    views=[
        dict(type='array', var='technique1', label='technique1', h=150),
        dict(type='array', var='technique2', label='technique2', h=150),
        dict(type='array', var=lambda S: S['diff'] if 'diff' in S else [], label='diff = t1 − t2（从大到小）', h=210,
             pointers={'p': 'blue'}, window=('0', 'k - 1'),
             color=lambda S, i, v: ('green' if v > 0 and i >= S['k'] and 'p' in S and i < S['p'] else None)),
        dict(type='text', fn=lambda S: (f"当前总分 `res` = =={S['res']}==" if 'res' in S else '先看每个任务：技巧 1 比技巧 2 多得几分？')),
    ],
    watch=['k', ('p', 'p if "p" in dir() else None', 'blue'), ('res', 'res if "res" in dir() else None', 'green')],
    captions={
        'diff = sorted': '先全选技巧 2，改成技巧 1 的得分变化是 `t1 − t2`，从大到小排：`diff = {diff}`',
        'res = sum': '必须有 `k={k}` 个改成技巧 1：选 diff 最大的 `k` 个 `{diff[:k]}`；`res = sum(t2) + {sum(diff[:k])}` = =={res}==',
        'p = k': '`p = {k}`：从第 `k` 个往后，看剩下的还有没有正数',
        'while p < len': '`p = {p}`：{"diff[p] = " + str(diff[p]) + " > 0，改成技巧 1 还能赚 → 加上" if p < len(diff) and diff[p] > 0 else "没有可加的正数了 → 停"}',
        'res += diff[p]': '再加上正的 `diff[{p}] = {diff[p]}`：`res` → =={res}==',
        'p += 1': '`p` → {p}',
        'return res': '最大总分 =={res}==',
    },
    cards=dict(
        one_liner='二选一：先全选一边，再看改选的差值',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个任务用技巧 1 得 `technique1[i]`，用技巧 2 得 `technique2[i]`',
                 '至少 `k` 个任务要用技巧 1，求最大总分',
                 '示例：`[5,2,10],[10,3,8],k=2` → `22`'],
        quote='对于这类二选一的问题，一种常用的处理方法是初始状态下全部选择一边，然后计算每种选择的得分之差数组diff。',
        quote_src='—— yiduobo 题解原文',
        idea=['“至少 k 个用技巧 1”：==先全部选技巧 2==，再把一些改成技巧 1',
              '`diff[i] = t1[i] − t2[i]`，从大到小排，==前 k 个必须改==',
              'k 之后还有 diff 为正的，改了更赚，一并加上；遇到非正就停'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：前 k 个即使 diff 为负也必须选（题目要求至少 k 个）',
                 '易错：k 之后只加正的，排序后遇到非正就能停',
                 '对比灵神：灵神先全选技巧 1，撤销至多 n−k 个；yiduobo 先全选技巧 2，补足 k 个',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
