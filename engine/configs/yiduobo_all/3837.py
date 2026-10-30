CONFIG = dict(
    num=3837, title='相等元素的延迟计数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='倒序遍历 · 后缀哈希表',
    tags=[],
    code='''
class Solution(object):
    def delayedCount(self, nums, k):
        
        freq = {}
        n = len(nums)
        res = [0] * n
        
        p = n - 1
        for index in range(n - 1, -1, -1):
            while p > index + k:
                freq[nums[p]] = freq.get(nums[p], 0) + 1
                p -= 1
            
            res[index] = freq.get(nums[index], 0)
        
        return res
''',
    call='Solution().delayedCount([3,1,3,2,3,1,3], 1)',
    expect=[3, 1, 2, 0, 1, 0, 0],
    views=[
        dict(type='array', var='nums', label='nums（框 = 后缀 p+1…n-1，已进入 freq）', cell=88, h=230,
             pointers={'index': 'blue', 'p': 'pink'},
             window=(lambda S: S['p'] + 1 if 'p' in S else None, lambda S: len(S['nums']) - 1),
             dim=lambda S, i, v: 'p' in S and i <= S['p'] and i != S.get('index')),
        dict(type='map', var='freq', label='freq（后缀中各值出现次数）', h=170, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='array', var='res', label='res', cell=88, h=170, pointers={'index': 'blue'}),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('k', 'k', 'yellow')],
    captions={
        'freq = {}': '`freq` 记录后缀里每种值出现几次',
        'p = n - 1': '`p` 是后缀的起点指针，从最右边开始；后缀 = `p+1 … n-1`',
        'for index': lambda S, B, r: '`index` 已枚举完 → 循环结束' if 'index' in B and B['index'] == S.index else f'倒着枚举 `index = {S.index}`，需要它右边下标 `> index + k = {S.index + S.k}` 的后缀',
        'while p > index + k': lambda S, B, r: (f'`p = {S.p} > index + k = {S.index + S.k}`：`nums[p]` 还没进后缀 → 继续吸收'
                                              if S.p > S.index + S.k else f'`p = {S.p} ≤ {S.index + S.k}`：后缀刚好是下标 `> index + k` 的部分 → 停止'),
        'freq[nums[p]] =': '把 `nums[{p}]={nums[p]}` 计入 `freq` → `freq[{nums[p]}] = {freq[nums[p]]}`',
        'p -= 1': '`p` 左移到 {p}，后缀向前扩一格',
        'res[index] =': '后缀里等于 `nums[{index}]={nums[index]}` 的个数：`freq.get({nums[index]}, 0)` = =={res[index]}==',
    },
    cards=dict(
        one_liner='index 往前走，后缀起点 p 也往前走，哈希表同步更新',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 和整数 `k`，对每个下标 `index`',
                 '数出下标 ==严格大于 index + k== 的元素里，恰好等于 `nums[index]` 的个数',
                 '示例：`[3,1,3,2,3,1,3]`，`k = 1` → `[3,1,2,0,1,0,0]`'],
        quote='可以从后往前一趟遍历，使用一个下标p记录当前下标对应的特定后缀的起点位置，另外使用一个哈希表freq记录从p开始的后缀中每种元素出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个下标要的是一个==后缀==，起点是 `index + k + 1`',
              'index 递减，后缀起点只会左移 → `p` 单调不回头',
              'p 每左移一格就把那个数加进 `freq`，查询只要 `freq.get`'],
        summary=['时间 `O(n)`：`p` 总共只走 `n` 步，每步 `O(1)`',
                 '`while p > index + k`：严格大于，所以后缀起点是 `index + k + 1`',
                 '`freq.get(x, 0)`：没出现过的值要当 0',
                 '`k` 很大时后缀为空，答案全 0'],
    ),
)
