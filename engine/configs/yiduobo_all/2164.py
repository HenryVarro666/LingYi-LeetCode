CONFIG = dict(
    num=2164, title='对奇偶下标分别排序', difficulty='Easy', category='模拟',
    author='yiduobo', technique='按奇偶收集 · 分别排序 · 交替填回',
    code='''
class Solution(object):
    def sortEvenOdd(self, nums):

        odd = []
        even = []
        n = len(nums)
        for index in range(n):
            if index % 2 == 1:
                odd.append(nums[index])
            else:
                even.append(nums[index])
        
        sorted_odd = sorted(odd, reverse=True)
        sorted_even = sorted(even)
        res = []
        for index in range(n):
            if index % 2 == 1:
                res.append(sorted_odd[index // 2])
            else:
                res.append(sorted_even[index // 2])
        
        return res
''',
    call='Solution().sortEvenOdd([4,1,2,3,7,6])',
    expect=[2, 6, 4, 3, 7, 1],
    views=[
        dict(type='array', var='nums', h=215, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
        dict(type='array', var='even', h=130, label='even（偶数下标的值）'),
        dict(type='array', var='odd', h=130, label='odd（奇数下标的值）'),
        dict(type='array', var='sorted_even', h=130, label='sorted_even（升序）'),
        dict(type='array', var='sorted_odd', h=130, label='sorted_odd（降序）'),
        dict(type='array', var='res', h=130, label='res'),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'if index % 2 == 1': lambda S, B, r: f'下标 `{S.index}` 是' + ('奇数' if S.index % 2 == 1 else '偶数') + '下标',
        'odd.append': '奇数下标：`nums[{index}] = {nums[index]}` 放进 `odd`',
        'even.append': '偶数下标：`nums[{index}] = {nums[index]}` 放进 `even`',
        'sorted_odd =': '奇数下标要非递增 → 降序 `{sorted_odd}`',
        'sorted_even =': '偶数下标要非递减 → 升序 `{sorted_even}`',
        'res = []': '开始按下标交替填回答案',
        'res.append(sorted_odd': '奇数下标 `{index}`：取 `sorted_odd[{index}//2]`，第 {index//2} 个 → `{res[-1]}`',
        'res.append(sorted_even': '偶数下标 `{index}`：取 `sorted_even[{index}//2]`，第 {index//2} 个 → `{res[-1]}`',
        'return res': '结果：`{res}`',
    },
    cards=dict(
        one_liner='奇偶分开排，再按下标交替取回来',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['奇数下标的值按非递增排，偶数下标的值按非递减排',
                 '返回重排后的数组',
                 '示例：`[4,1,2,3]` → `[2,3,4,1]`；本视频用 `[4,1,2,3,7,6]`'],
        quote='依照题目要求分别按下标奇偶收集数组中的数据，排序后再按奇偶交替填充到答案数组中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历一遍，把奇数下标、偶数下标的值分别收集',
              '奇数组降序、偶数组升序',
              '下标 `i` 对应的是组里第 `i // 2` 个'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '奇数下标降序、偶数下标升序，别写反',
                 '下标 `i` 取 `sorted_xxx[i // 2]`',
                 '原文为 Python 2 写法，`index / 2` 为整数除法，已改为 `index // 2`'],
    ),
)
