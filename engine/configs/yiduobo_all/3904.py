CONFIG = dict(
    num=3904, title='最小稳定下标 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='预处理后缀最小值 + 边遍历边维护前缀最大值',
    tags=['灵神题单', '动态规划', '难度分 1352'],
    code='''
class Solution(object):
    def firstStableIndex(self, nums, k):
        
        n = len(nums)
        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(min(suffix[-1], nums[index]))
        
        suffix.reverse()
        ma = nums[0]
        v = ma - suffix[0]
        if v <= k:
            return 0
        for index in range(1, n):
            ma = max(ma, nums[index])
            v = ma - suffix[index]
            if v <= k:
                return index
        return -1
''',
    call='Solution().firstStableIndex([5,0,1,4,6,7], 3)',
    expect=3,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"下标 `{S['index']}`：不稳定值 `v = {S['ma']} − {S['suffix'][S['index']]}` = =={S['v']}==（k = {S['k']}）"
                                                 if S['_line'] >= 11 and 'ma' in S and 'v' in S else '先从后往前，把后缀最小值依次放进 suffix')),
        dict(type='array', var='nums', label='nums', pointers={'index if _line >= 11 else -1': 'blue'}, pointer_labels={'index if _line >= 11 else -1': 'index'}, h=200,
             color=lambda S, i, v: 'green' if S['_line'] >= 11 and 'ma' in S and i <= S['index'] else None),
        dict(type='array', var='suffix',
             label='suffix（reverse 之后 suffix[i] = nums[i:] 的最小值）',
             pointers={'index if _line >= 11 else -1': 'pink'}, pointer_labels={'index if _line >= 11 else -1': 'index'}, h=200),
    ],
    watch=['index', 'k', ('ma', 'ma', 'orange'), ('v', 'v', 'green')],
    captions={
        'suffix = [nums[-1]]': '先放进最后一个数 `{nums[-1]}`：它自己就是最短后缀的最小值',
        'for index in range(n - 2': lambda S, B, r: (f'从倒数第二个往前扫，`index = {S.index}`' if len(S.suffix) < S.n else '后缀最小值都收集完了'),
        'suffix.append': '`suffix` 末尾追加 `min(上一个最小值, nums[{index}])` = =={suffix[-1]}==',
        'suffix.reverse': '翻转后 `suffix[i]` 就对应 `nums[i:]` 的最小值：{suffix}',
        'ma = nums[0]': '`ma` 维护前缀最大值，先从 `nums[0] = {ma}` 开始',
        'v = ma - suffix[0]': '下标 0 的不稳定值 `{ma} − {suffix[0]}` = =={v}==',
        'if v <= k': '`v = {v}` 与 `k = {k}` 比 → {"==稳定==" if v <= k else "不稳定，继续往右"}',
        'for index in range(1, n)': '往右枚举下标，`index = {index}`',
        'ma = max': '把 `nums[{index}] = {nums[index]}` 并入前缀：`ma` = =={ma}==',
        'v = ma - suffix[index]': '`v = {ma} − {suffix[index]}` = =={v}==',
        'return 0': '下标 0 就稳定，直接返回 `0`',
        'return index': '第一个稳定下标：=={index}==',
        'return -1': '每个下标都不稳定 → `-1`',
    },
    cards=dict(
        one_liner='后缀最小值预处理，前缀最大值边走边算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['下标 `index` 的不稳定值 = 前缀 `[0..index]` 的最大值 − 后缀 `[index..n-1]` 的最小值',
                 '不稳定值 `<= k` 就是稳定下标，求最小的；没有返回 `-1`',
                 '本视频：`nums=[5,0,1,4,6,7], k=3` → `3`'],
        quote='对于前缀最大值，可以随着index的遍历进行计算，而对于后缀最小值，则可以进行预处理，从后往前遍历一遍，计算出每个后缀中的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['要最小的下标，自然从前往后枚举，逐个检测是否稳定',
              '前缀最大值随枚举顺手更新；后缀最小值得先倒着算好一份',
              '第一次 `v <= k` 就能返回，不用再往后看'],
        summary=['时间 `O(n)`，空间 `O(n)`（`suffix` 数组）',
                 '`suffix` 是倒着追加的，==必须 reverse== 之后才能按下标取',
                 '下标 0 单独处理，循环从 1 开始；两种情况都要判断 `v <= k`',
                 '原文代码无需改动，已是 Python 3 可运行'],
    ),
)
