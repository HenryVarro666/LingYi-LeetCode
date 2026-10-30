CONFIG = dict(
    num=1526, title='形成目标数组的子数组最少增加次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='只统计下降段 · 从高往低拉平',
    tags=['难度分 1872'],
    code='''
class Solution(object):
    def minNumberOperations(self, target):

        res = 0
        n = len(target)
        for index in range(n - 1):
            if target[index] > target[index + 1]:           
                res += target[index] - target[index + 1]
        
        res += target[-1]
        return res
''',
    call='Solution().minNumberOperations([3,1,5,4,2])',
    expect=7,
    views=[
        dict(type='bars', var='target', label='target（蓝 = index，粉 = index+1）',
             pointers={'index': 'blue', 'index + 1': 'pink'}, h=380,
             color=lambda S, i, v: ('blue' if 'index' in S and i == S['index'] else 'pink' if 'index' in S and i == S['index'] + 1 else None)),
        dict(type='text', fn=lambda S: (f"下降的落差累计 `res` = =={S['res']}==" if 'res' in S else ''), size=28),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计「必须在这里补的操作」',
        'for index': lambda S, B, r: (f'比较第 `{S.index}` 与第 `{S.index + 1}` 个：`{S.target[S.index]}` 和 `{S.target[S.index + 1]}`' if S.index != B.get('index') or 'res' not in B else '相邻对比较完毕'),
        'if target[index] >': lambda S, B, r: (f'`{S.target[S.index]} > {S.target[S.index + 1]}`：右边更矮 → 左边那段多出的高度要在这里==拉平==' if S.target[S.index] > S.target[S.index + 1] else f'`{S.target[S.index]} <= {S.target[S.index + 1]}`：右边不矮 → 留到处理 `index + 1` 时一起操作，这里不用算'),
        'res += target[index] -': '多出的落差 `{target[index]} - {target[index + 1]} = {target[index] - target[index + 1]}` 次操作 → `res = {res}`',
        'res += target[-1]': '最后一个位置右边没有更矮的，它的高度 `{target[-1]}` 也要靠操作堆出来 → `res = {res}`',
        'return res': '最少操作 `{res}` 次',
    },
    skip=['n = len'],
    cards=dict(
        one_liner='只在「下降」处记账：左边比右边高出多少，就在那里拉平多少',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`initial` 全为 0，每次选一个子数组整体加 `1`',
                 '求变成 `target` 的最少操作次数',
                 '示例：`target = [3,1,5,4,2]` → `7`'],
        quote='对于target[index]而言，若target[index] > target[index + 1]，那么就按思路一的做法进行操作。而target[index] <= target[index + 1]时，则可以等到处理index + 1时再进行操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['思路一：找下一个更小的数，用单调栈 + 区间数据结构，较重',
              '思路二是精简版：只看相邻两个数，==下降多少就补多少==',
              '上升时不用管：留给右边那个位置处理；最后再加上 `target[-1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '别忘了最后的 `res += target[-1]`',
                 '原文是 Python 2 风格，只删去了类型说明文档字符串',
                 '和灵神的差分解法等价：正数之和 = 下降落差之和 + 末尾值'],
    ),
)
