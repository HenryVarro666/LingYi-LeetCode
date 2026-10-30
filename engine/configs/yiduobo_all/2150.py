CONFIG = dict(
    num=2150, title='找出数组中的所有孤独数字', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表计数',
    code='''
class Solution(object):
    def findLonely(self, nums):

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        res = []
        for num in num_dict:
            if num_dict.get(num - 1, 0) == 0 and num_dict.get(num + 1, 0) == 0 and num_dict[num] == 1:
                res.append(num)
        
        return res
''',
    call='Solution().findLonely([10,6,5,8,3,3])',
    expect=[10, 8],
    views=[
        dict(type='array', var='nums', h=170,
             color=lambda S, i, v: 'yellow' if 'num' in S and S['num'] == v and 'res' not in S else None),
        dict(type='map', var='num_dict', h=250, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='array', var='res', label='res（孤独数字）', h=150),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'num_dict = {}': '先建一个哈希表，记录每个数出现的次数',
        'num_dict[num] = num_dict': '`{num}` 的出现次数变成 `{num_dict[num]}`',
        'res = []': '统计完了，开始逐个检查哈希表里的数',
        'if num_dict.get(num - 1': lambda S, B, r: (
            f"检查 `{S.num}`：次数 `{S.num_dict[S.num]}`，`{S.num-1}` 出现 `{S.num_dict.get(S.num-1, 0)}` 次，`{S.num+1}` 出现 `{S.num_dict.get(S.num+1, 0)}` 次 → "
            + ('==三个条件都满足，是孤独数字==' if S.num_dict.get(S.num-1, 0) == 0 and S.num_dict.get(S.num+1, 0) == 0 and S.num_dict[S.num] == 1
               else '有邻居或重复，不是孤独数字')),
        'res.append': '`{num}` 加入答案',
        'return res': '孤独数字：`{res}`',
    },
    cards=dict(
        one_liner='先数一遍，再看每个数的左右邻居在不在',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数字 `x` 只出现一次，且 `x-1`、`x+1` 都不在数组里，就是孤独数字',
                 '返回所有孤独数字，顺序任意',
                 '示例：`[10,6,5,8]` → `[10,8]`；本视频用 `[10,6,5,8,3,3]`'],
        quote='使用哈希表统计数组中每个数字出现的次数，接下来遍历哈希表中的所有数……',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：用哈希表数出每个数的出现次数',
              '第二趟：遍历哈希表里的键，要求次数恰好为 1',
              '再用 `get(x ± 1, 0)` 查邻居，没出现就是 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '遍历的是哈希表的键，重复的数只检查一次',
                 '用 `get(key, 0)` 查邻居，不会因缺键报错',
                 '原文为 Python 2 风格，本题代码无需改动，直接运行'],
    ),
)
