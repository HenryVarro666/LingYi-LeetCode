def _txt(S):
    if 'num_set' in S:
        return f"`s = {S['s']}`：" + ('在集合里 ==继续往上找==' if S['s'] in S['num_set'] else '不在集合里 ==就是答案==')
    if 'index' in S:
        return f"当前前缀和 `s = {S['s']}`，看下标 `{S['index']}` 是否接上前一项"
    return f"`s = nums[0] = {S['s']}`"


def _col(S, i, v):
    if 'num_set' in S:
        return 'yellow' if v == S['s'] else None
    if 'index' not in S:
        return 'green' if i == 0 else None
    k = S['index']
    broke = S['_line'] == 10
    if i < k:
        return 'green'
    if i == k:
        return 'pink' if (S['nums'][k] != S['nums'][k - 1] + 1) else 'green'
    return None


CONFIG = dict(
    num=2996, title='大于等于顺序前缀和的最小缺失整数', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 + 向上找缺失值',
    code='''
class Solution(object):
    def missingInteger(self, nums):

        s = nums[0]
        for index in range(1, len(nums)):
            if nums[index] == nums[index - 1] + 1:
                s += nums[index]
            else:
                break
        
        num_set = set(nums)
        while s in num_set:
            s += 1
        
        return s
''',
    call='Solution().missingInteger([1,2,3,2,5,6])',
    expect=7,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={'index': 'blue'}, color=_col, h=230),
        dict(type='set', var='num_set', h=200, fmt=lambda x: str(x)),
    ],
    watch=[('s', 's', 'green'), 'index'],
    captions={
        's = nums[0]': '先把第一个数当作前缀：`s = {s}`',
        'for index in range': '下标从 1 开始，每次和前一个数比',
        'if nums[index] ==': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` 等于 `{S.nums[S.index-1]} + 1` → ==顺序前缀延长=='
                                              if S.nums[S.index] == S.nums[S.index-1] + 1 else
                                              f'`nums[{S.index}] = {S.nums[S.index]}` 不等于 `{S.nums[S.index-1]} + 1` → 顺序断了'),
        's += nums[index]': '前缀和累加：`s = {s}`',
        'break': '最长顺序前缀到此为止，前缀和 `s = {s}`',
        'num_set = set': '数据规模小，把数组放进集合，方便判断「出没出现过」',
        'while s in num_set': lambda S, B, r: (f'`{S.s}` 在数组中 → 继续向上' if S.s in S.num_set
                                               else f'`{S.s}` 不在数组中 → ==停止，向上遍历结束=='),
        's += 1': '`s` 加 1 → {s}',
        'return s': '最小缺失整数：`{s}`',
    },
    cards=dict(
        one_liner='一趟遍历求前缀和，再从前缀和向上找第一个没出现的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['顺序前缀：每个数都是前一个数 `+1`',
                 '返回 ==没出现过== 且 ==≥ 最长顺序前缀和== 的最小整数',
                 '本视频：`[1,2,3,2,5,6]` → 前缀和 6，6 在数组里，7 不在 → `7`'],
        quote='只需从头开始向后一趟遍历，找出最长的顺序前缀，同时计算前缀之和s，然后再从s开始向上遍历，直到当前遍历的值没有出现在数组中为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模很小，不需要花哨的方法，直接两步走',
              '第一步：遇到 `nums[index] != nums[index-1] + 1` 就 break',
              '第二步：`set` 判断存在性，从 `s` 往上一个个试'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串（代码本身 Python 3 可直接运行）',
                 '易错：前缀至少含 `nums[0]`，所以 `s` 从 `nums[0]` 起步',
                 '与灵神对比：灵神用 `pairwise` 取相邻对，yiduobo 用下标比较'],
    ),
)
