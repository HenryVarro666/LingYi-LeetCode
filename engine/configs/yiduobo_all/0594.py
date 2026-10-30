CONFIG = dict(
    num=594, title='最长和谐子序列', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='字典计数 · 看 x 与 x-1',
    tags=[],
    code='''
class Solution(object):
    def findLHS(self, nums):

        count_dict = {}
        for num in nums:
            count_dict[num] = count_dict.get(num, 0) + 1
        res = 0
        for num in count_dict:
            if num - 1 in count_dict:
                res = max(res, count_dict[num] + count_dict[num - 1])
        return res
''',
    call='Solution().findLHS([1,3,2,2,5,2,3,7])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', h=170),
        dict(type='map', var='count_dict', label='count_dict（数字 → 次数）', fmt=lambda k, v: f'{k}: {v}', h=200, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"`{S['num']}` 与 `{S['num']-1}`：{S['count_dict'][S['num']]} + {S['count_dict'][S['num']-1]} = =={S['count_dict'][S['num']] + S['count_dict'][S['num']-1]}==" if S['_line'] >= 9 and 'res' in S and S['num'] in S['count_dict'] and S['num'] - 1 in S['count_dict'] else '')),
    ],
    watch=[('num', 'num', 'blue'), ('res', 'res', 'green')],
    captions={
        'count_dict = {}': '`count_dict` 记录每个数字出现的次数',
        'for num in nums': lambda S, B, r: ('统计完毕' if sum(S.count_dict.values()) == len(S.nums) else f'读到 `{S.num}`'),
        'count_dict[num] =': '`count_dict[{num}]` = 旧次数 + 1 = `{count_dict[num]}`（`get(num, 0)` 保证第一次从 0 开始）',
        'res = 0': '`res` 记录最大的总次数，没有和谐对就是 0',
        'for num in count_dict': lambda S, B, r: ('遍历结束' if B.get('num') == S.num else f'遍历每个不同的数字：`num = {S.num}`'),
        'if num - 1 in count_dict': lambda S, B, r: (f'`{S.num - 1}` 也出现过：{S.num} 和 {S.num - 1} 可组成和谐子序列' if S.num - 1 in S.count_dict
                                                     else f'`{S.num - 1}` 没出现过：{S.num} 凑不成和谐对，跳过'),
        'res = max': '`{num}` 与 `{num - 1}` 的总次数 `{count_dict[num]} + {count_dict[num - 1]} = {count_dict[num] + count_dict[num - 1]}`，`res = max({B.res}, …) = {res}`',
        'return res': '最大总次数 =={res}==',
    },
    cards=dict(
        one_liner='数一数每个数出现几次，相邻两数的次数相加取最大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['和谐数组：最大值与最小值之差==正好是 1==',
                 '求最长和谐子序列的长度（子序列可以不连续）',
                 '示例：`[1,3,2,2,5,2,3,7]` → `5`，`[1,1,1,1]` → `0`'],
        quote='统计每个数字出现的次数，然后遍历每个数字x，计算x和x - 1出现的总次数，选择总次数最大的x即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用字典 `count_dict` 数出每个数字的次数',
              '再遍历每个数字 `num`，只要 `num - 1` 也出现过，就把两者次数相加',
              '所有相加结果里取最大值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`num - 1` 必须真的在字典里才算，否则 `[1,1,1,1]` 会错成 4',
                 '原文为 Python 2 风格，但本题代码在 Python 3 下可直接运行，未改动',
                 '对比灵神：灵神向上找 `x+1`，yiduobo 向下找 `x-1`，结果相同'],
    ),
)
