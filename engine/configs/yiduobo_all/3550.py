CONFIG = dict(
    num=3550, title='数位和等于下标的最小下标', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 模 10 除 10 求数位和',
    tags=[],
    code='''
class Solution(object):
    def smallestIndex(self, nums):
        
        for index, v in enumerate(nums):
            s = 0
            while v:
                s += v % 10
                v //= 10
            
            if s == index:
                return index
        
        return -1
''',
    call='Solution().smallestIndex([9,23,12,5,4])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前下标 index）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"`v = {S['v']}`，已累加数位和 `s = {S['s']}`，目标 `index = {S['index']}`" if 'v' in S and 's' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), 'v', ('s', 's', 'yellow')],
    captions={
        'enumerate': lambda S, B, r: f'遍历到 `index = {S.index}`，`nums[{S.index}]` = `{S.v}`',
        's = 0': '为当前元素准备数位和 `s = 0`',
        'while v': lambda S, B, r: (f'`v = {S.v}` 非 0，还有数位' if S.v else '`v` 变成 0：数位取完了'),
        's += v % 10': '`v % 10 = {B.v % 10}` 是个位，累加：`s = {s}`',
        'v //= 10': '`v //= 10` 去掉个位，`v` = {v}',
        'if s == index': lambda S, B, r: (f'`s = {S.s}` 等于 `index = {S.index}`，直接返回' if S.s == S.index else f'`s = {S.s}` 不等于 `index = {S.index}`，继续下一个'),
        'return index': '这是第一个合法下标，也就是最小的：返回 `{index}`',
        'return -1': '遍历完都没有合法下标，返回 `-1`',
    },
    cards=dict(
        one_liner='一趟遍历，边算数位和边和下标比',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['返回满足 `nums[index]` 的数位和恰好等于 `index` 的最小下标',
                 '不存在则返回 `-1`',
                 '本视频：`[9,23,12,5,4]` → `4`'],
        quote='直接一趟遍历，对于当前遍历到的元素nums[index]，通过模10除10的方法计算其数位和s。若s与index相等，则直接返回index。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标从小到大走，第一个命中的就是最小下标',
              '每个元素内部：不断 `v % 10` 累加、`v //= 10` 去尾',
              '全部走完都没命中，返回 `-1`'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '直接修改循环变量 `v` 求数位和，不影响 `nums`',
                 '原文为 Python 2 风格，`class Solution(object)` 照常运行，代码无需改动',
                 '对比灵神：灵神额外指出数位和最大 27，只需枚举前 28 个'],
    ),
)
