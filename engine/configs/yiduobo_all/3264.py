CONFIG = dict(
    num=3264, title='K 次乘运算后的最终数组 I', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='暴力模拟（k 很小）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1178'],
    code='''
class Solution(object):
    def getFinalState(self, nums, k, multiplier):

        for rnd in range(k):
            p = 0
            for index in range(1, len(nums)):
                if nums[index] < nums[p]:
                    p = index

            nums[p] *= multiplier
        
        return nums
''',
    call='Solution().getFinalState([3,1,2,4], 4, 2)',
    expect=[6, 4, 4, 4],
    views=[
        dict(type='array', var='nums', pointers={'p': 'pink', 'index': 'blue'}, h=260,
             color=lambda S, i, v: 'pink' if 'p' in S and i == S['p'] else None),
        dict(type='text', fn=lambda S: (f"第 `{S['rnd'] + 1}` 轮：当前最小值 `nums[{S['p']}] = {S['nums'][S['p']]}`" if 'p' in S else ''), h=60),
    ],
    watch=[('rnd', lambda S: S.get('rnd'), 'orange'), ('p', lambda S: S.get('p'), 'pink'), ('index', lambda S: S.get('index'), 'blue')],
    captions={
        'for rnd in range(k)': lambda S, B, r: ('`k` 轮都做完了，退出循环' if B.get('rnd') == S.get('rnd') else f'第 {S.rnd + 1} 轮操作（共 4 轮）：从头扫一遍找最小值'),
        'p = 0': '假设最前面的 `nums[0] = {nums[0]}` 是最小的，`p = 0` 记录最小值的下标',
        'for index in range': lambda S, B, r: ('这一轮扫描结束，`p` 就是最小值的下标' if 'index' in B and B.get('rnd') == S.rnd and B.index == S.index else f'看下一个位置 `index = {S.index}`，值 `{S.nums[S.index]}`'),
        'if nums[index] < nums[p]': lambda S, B, r: (f'`{S.nums[S.index]} < {S.nums[S.p]}` ==严格小于== → 成立，换成更小的' if S.nums[S.index] < S.nums[S.p] else f'`{S.nums[S.index]} < {S.nums[S.p]}` → 不成立：更大或相等都不换，==并列时保留靠前的 p=='),
        'p = index': '更新最小值下标：`p = {p}`，`nums[p] = {nums[p]}`',
        'nums[p] *= multiplier': '把最小值乘以 `multiplier = {multiplier}`：`nums[{p}]` = =={nums[p]}==，数组变为 `{nums}`',
        'return nums': '`k` 轮做完，最终数组 =={ret}==',
    },
    cards=dict(
        one_liner='k 最大才 10，每轮扫一遍找最小值，直接暴力模拟',
        complexity='时间 `O(k·n)`，空间 `O(1)`',
        problem=['每次操作：找出 `nums` 中最小的数（并列取最靠前的），乘以 `multiplier`',
                 '做 `k` 次后返回数组',
                 '示例：`[2,1,3,5,6], k=5, multiplier=2` → `[8,4,6,5,6]`；本视频 `[3,1,2,4], k=4` → `[6,4,4,4]`'],
        quote='第一题中的k最大为10，可以直接暴力模拟。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据范围小：`k <= 10`，`n <= 100`',
              '每轮从头线性扫描，用严格小于 `<` 更新下标 → ==并列时自然保留最靠前的==',
              '找到后原地乘以 `multiplier`'],
        summary=['时间 `O(k·n)`，本题数据下完全够用',
                 '比较用 `<` 而不是 `<=`：并列取下标小的',
                 '原文第二题（3266，k 到 10^9）要用堆 + 快速幂，这里只演示第一题',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动'],
    ),
)
