CONFIG = dict(
    num=2670, title='找出不同元素数目差数组', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='两趟遍历 · 答案数组原地相减',
    tags=[],
    code='''
class Solution(object):
    def distinctDifferenceArray(self, nums):

        n = len(nums)
        res = [0] * n
        
        num_set = set()
        for index in range(n):
            num_set.add(nums[index])
            res[index] = len(num_set)
        
        num_set = set()
        for index in range(n - 1, 0, -1):
            num_set.add(nums[index])
            res[index - 1] -= len(num_set)
        
        return res
''',
    call='Solution().distinctDifferenceArray([3,2,3,4,2])',
    expect=[-2, -1, 0, 2, 3],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, cell=90, h=150),
        dict(type='set', var='num_set', label='num_set（前缀 / 后缀的不同元素）', fmt=lambda x: str(x), h=110),
        dict(type='array', var='res', label='res（先放前缀数，再减后缀数）', pointers={'index': 'blue'}, cell=90, h=150),
    ],
    watch=[('index', 'index', 'blue'), ('len(num_set)', 'len(num_set)', 'orange')],
    captions={
        'res = [0] * n': '`res` 先拿来存「前缀不同元素数」，之后再原地减去后缀的',
        'num_set = set()': '新建一个空集合，重新开始统计',
        'num_set.add(nums[index])': '加入 `nums[{index}] = {nums[index]}`，集合现在有 `{len(num_set)}` 个不同元素',
        'for index in range(n - 1': '反向遍历 `index = n-1 … 1`，当前 `index = {index}`：集合里装的是后缀 `nums[{index}:]`',
        'res[index] = len': '正向：前缀 `nums[0..{index}]` 有 `{len(num_set)}` 个不同元素 → `res[{index}] = {res[index]}`',
        'res[index - 1] -=': '反向：后缀 `nums[{index}:]` 有 `{len(num_set)}` 个不同元素，从上一位 `res[{index-1}]` 里减掉：{B.res[index-1]} → =={res[index-1]}==',
        'return res': '两趟下来 `res` 就是答案 `{res}`',
    },
    cards=dict(
        one_liner='前缀、后缀分开算，正向累加、反向减掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`diff[i]` = 前缀 `nums[0..i]` 不同元素数 − 后缀 `nums[i+1..]` 不同元素数',
                 '返回整个 `diff` 数组',
                 '示例：`[3,2,3,4,2]` → `[-2,-1,0,2,3]`'],
        quote='首先正向一趟遍历，使用哈希表计算当前前缀中不同元素的数目，并将其累加到答案数组的对应下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['拆开算：先正向遍历，把前缀的不同元素数写进 `res`',
              '再反向遍历，集合里是后缀 `nums[index:]` 的不同元素',
              '后缀从 `index` 开始，对应答案位置是 `index - 1`，所以减在 `res[index - 1]` 上'],
        summary=['时间 `O(n)`，空间 `O(n)`，没有额外的后缀数组',
                 '反向循环到 `index = 1` 为止：对应 `res[0]` 减去 `nums[1:]` 的不同数',
                 '易错：减的位置是 `index - 1`，不是 `index`',
                 '对比灵神：灵神单独开 `suf` 数组，yiduobo 直接在答案上原地相减'],
    ),
)
