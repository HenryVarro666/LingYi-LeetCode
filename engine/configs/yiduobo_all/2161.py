CONFIG = dict(
    num=2161, title='根据给定数字划分数组', difficulty='Medium', category='模拟',
    author='yiduobo', technique='两个填充指针 · 先数小于等于的个数',
    code='''
class Solution(object):
    def pivotArray(self, nums, pivot):

        n = len(nums)
        res = [pivot] * n
        l = r = 0
        for num in nums:
            if num <= pivot:
                r += 1
        
        for num in nums:
            if num < pivot:
                res[l] = num
                l += 1
            elif num > pivot:
                res[r] = num
                r += 1
        
        return res
''',
    call='Solution().pivotArray([9,12,5,10,14,3,10], 10)',
    expect=[9, 5, 3, 10, 10, 12, 14],
    views=[
        dict(type='array', var='nums', h=170, label='nums'),
        dict(type='array', var='res', h=200, label='res（初始全是 pivot）', pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, i, v: 'blue' if 'l' in S and i == S['l'] else 'pink' if 'r' in S and i == S['r'] else None),
    ],
    watch=['num', ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'res = [pivot] * n': '答案先全部填 `pivot`：等于 pivot 的数最后不用再填',
        'l = r = 0': '`l` 填小于 pivot 的数，`r` 之后要改成大于区的起点',
        9: '`{num} <= {pivot}`：它属于左边或中间 → `r` 后移，`r = {r}`，`r` 最终 = `cnt`',
        'if num <= pivot': lambda S, B, r: (f'数一数 `<= pivot` 的个数：`{S.num} <= {S.pivot}` ' + ('成立' if S.num <= S.pivot else '不成立（大于区的数，不计）')),
        'if num < pivot': lambda S, B, r: f'`{S.num} < {S.pivot}`' + (' 成立 → 填到 l 位置' if S.num < S.pivot else ' 不成立'),
        'res[l] = num': '小于 pivot：写到 `res[{l}]`，保持原有相对顺序',
        'l += 1': '`l` → {l}',
        'elif num > pivot': lambda S, B, r: f'`{S.num} > {S.pivot}`' + (' 成立 → 填到 r 位置' if S.num > S.pivot else ' 不成立：等于 pivot，跳过（res 里本来就是 pivot）'),
        'res[r] = num': '大于 pivot：写到 `res[{r}]`，从 `cnt` 开始按顺序放',
        17: '`r` → {r}',
        'return res': '划分完成：`{res}`',
    },
    cards=dict(
        one_liner='先数出小于等于的个数，大于区的起点就定下来了',
        complexity='时间 `O(n)`，空间 `O(n)`（答案数组）',
        problem=['把 `nums` 重排：小于 `pivot` 的在前，等于的在中间，大于的在后',
                 '小于区、大于区内部的==相对顺序不变==（稳定）',
                 '示例：`[9,12,5,10,14,3,10]`，`pivot=10` → `[9,5,3,10,10,12,14]`'],
        quote='不适用两端直接向中间扫描的做法了。先进行一趟遍历，找出数组中小于等于pivot的数的个数cnt，那么大于pivot的数在答案数组中的下标就必然是从cnt开始。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：数出 `<= pivot` 的个数 `cnt`，让 `r = cnt`',
              '第二趟：小的写到 `l`，大的写到 `r`，各自后移',
              '答案先全填 `pivot`，等于区自动正确'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '两端向中间的快排分区不稳定，本题不能用',
                 '第一趟 `l` 与 `r` 同时为 0，计数时只增加 `r`',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
