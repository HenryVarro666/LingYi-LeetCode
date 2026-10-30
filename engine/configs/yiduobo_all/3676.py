CONFIG = dict(
    num=3676, title='碗子数组的数目', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='枚举中间最大值 · 前后缀最大值',
    tags=['灵神题单·单调栈', '难度分 1848'],
    code='''
class Solution(object):
    def bowlSubarrays(self, nums):
        
        n = len(nums)
        left = [False] * n
        ma = nums[0]
        for index in range(1, n):
            if nums[index] < ma:
                left[index] = True
            else:
                ma = nums[index]
        
        ma = nums[-1]
        res = 0
        for index in range(n - 1, 0, -1):
            if nums[index] < ma:
                if left[index]:
                    res += 1
            else:
                ma = nums[index]
        
        return res
''',
    call='Solution().bowlSubarrays([2,5,3,1,4])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=170, label='nums',
             color=lambda S, i, v: 'blue' if i == S.get('index', -1) else None),
        dict(type='array', var='left', h=170, label='left：左侧是否有更大的数',
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=lambda S: f"当前最大值 `ma = {S['ma']}`，已找到 `res = {S['res']}`" if 'res' in S else (f"正序扫描，左侧最大值 `ma = {S['ma']}`" if 'ma' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('ma', 'ma', 'yellow'), ('res', 'res', 'green')],
    captions={
        'left = [False]': '`left[i]` 记录 i 左边==有没有更大的数==',
        'ma = nums[0]': '`ma = {ma}`：正序扫描时，左侧的最大值',
        'if nums[index] < ma:': lambda S, B, r: (
            f'`nums[{S.index}] = {S.nums[S.index]}` < `ma = {S.ma}`：左边有更大的数' if S.nums[S.index] < S.ma
            else f'`nums[{S.index}] = {S.nums[S.index]}` 不小于 `ma = {S.ma}`：它自己成为新的最大值'),
        'left[index] = True': '标记 `left[{index}] = True`：它可以做某个碗的中间最大值',
        'ma = nums[index]': '更新 `ma = {ma}`',
        'for index in range(n - 1': lambda S, B, r: (
            '倒序扫描从 `index = n - 1` 开始' if B.get('index') == S.index == len(S.nums) - 1
            else '倒序扫描结束' if B.get('index') == S.index else f'倒序取下一个：`index = {S.index}`'),
        'ma = nums[-1]': '倒序扫描，`ma = {ma}`：右侧的最大值（从最后一个数开始）',
        'if left[index]:': lambda S, B, r: (
            f'左边有更大的数（`left[{S.index}] = True`），右边也有 → ==两侧都有更大元素==' if S.left[S.index]
            else f'`left[{S.index}] = False`：左边没有更大的数，不行'),
        'res += 1': '以 `nums[{index}]` 为中间最大值能构成碗：`res` = =={res}==',
        'return res': '一共 `{res}` 个碗',
    },
    max_steps=90,
    cards=dict(
        one_liner='换个角度：只看中间最大值，两侧都有更大的数就是一个碗',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找长度 >= 3 的子数组，满足两端的较小值严格大于中间最大值',
                 '元素互不相同，数一数有多少个',
                 '本视频示例：`[2,5,3,1,4]` → `3`'],
        quote='对于数组中的某个元素nums[index]，若其是某个碗子数组的中间部分的最大值，那么这个碗的左边界只能index左侧的第一个更大元素对应的下标，而右边界则只能是index右侧的第一个更大元素对应的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['不必知道碗的具体边界，只要 `nums[index]` ==左右都有更大的数==',
              '正序扫一遍：用 `ma` 记录左侧最大值，标出 `left`',
              '倒序再扫一遍：右侧最大值更大，且 `left` 为真，就计一个'],
        summary=['时间 `O(n)`，扫两遍；空间 `O(n)`（`left` 数组）',
                 '每个中间最大值恰好对应一个碗：边界取左右第一个更大的数',
                 '`ma` 只在当前数不小于它时更新，所以它是前缀最大值，不是栈',
                 '对比灵神：灵神用单调栈直接数端点，yiduobo 用前后缀最大值数中间点'],
    ),
)
