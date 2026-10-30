CONFIG = dict(
    num=2640, title='一个数组所有前缀的分数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='先求 conver 数组再求前缀和', tags=[],
    code='''
class Solution(object):
    def findPrefixScore(self, nums):

        ma = 0
        conver = []
        for v in nums:
            ma = max(ma, v)
            conver.append(v + ma)
        
        res = []
        for v in conver:
            if not res:
                res.append(v)
            else:
                res.append(res[-1] + v)
        
        return res
''',
    call='Solution().findPrefixScore([2,3,7,5,10])',
    expect=[4, 10, 24, 36, 56],
    views=[
        dict(type='array', var='nums', label='nums', h=165,
             color=lambda S, i, v: 'blue' if 'conver' in S and i == len(S['conver']) - 1 and 'res' not in S else None),
        dict(type='array', var='conver', label='conver（第一遍：arr[i] + 前缀最大值）', h=165,
             color=lambda S, i, v: 'orange' if i == len(S['conver']) - 1 and 'res' not in S else None),
        dict(type='array', var='res', label='res（第二遍：conver 的前缀和）', h=165,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('v', 'v', 'blue'), ('ma', 'ma', 'orange'), ('res', 'res', 'green')],
    captions={
        'ma = max': '更新前缀最大值：`ma = max({B.ma}, {v}) = {ma}`',
        'conver.append': '`conver[i] = {v}` + `ma`（{ma}）= =={conver[-1]}==',
        'if not res': lambda S, B, r: ('`res` 还是空的 → 第一个前缀和就是它自己' if not S.res
                                       else f'`res` 非空 → 用上一个前缀和 `{S.res[-1]}` 加上 `{S.v}`'),
        'res.append(v)': '第一个前缀和 = `{v}`',
        'res.append(res[-1] + v)': '前缀和 `{res[-2]} + {v} = =={res[-1]}==`',
        'return res': '`res` 就是每个前缀的分数：`{res}`',
    },
    cards=dict(
        one_liner='两趟遍历：先造 conver，再对它求前缀和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`conver[i] = arr[i] + max(arr[0..i])`，分数是 conver 的和',
                 '返回每个前缀的分数',
                 '示例：`[2,3,7,5,10]` → `[4,10,24,36,56]`'],
        quote='按照题目描述对nums进行一趟遍历，计算出conver数组，然后再对conver数组一趟遍历，计算出该数组的前缀和作为最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍严格照题意：边走边记最大值 `ma`，得到 `conver`',
              '第二遍对 `conver` 做前缀和，第 `i` 项就是前缀 `i` 的分数',
              '思路直白，多用一个 `conver` 数组'],
        summary=['时间 `O(n)`，空间 `O(n)`（多一个 conver）',
                 '`ma` 初值 0 可行，因为 `nums[i] >= 1`',
                 '第一个前缀和要单独处理（`res` 为空时）',
                 '对比灵神：灵神一趟遍历合并两步，空间 `O(1)`'],
    ),
)
