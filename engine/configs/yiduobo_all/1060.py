CONFIG = dict(
    num=1060, title='有序数组中的缺失元素', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分 + 缺失数量公式', tags=[],
    code='''
class Solution(object):
    def missingElement(self, nums, k):

        n = len(nums)
        if k > (nums[-1] - nums[0] + 1 - n):
            k -= (nums[-1] - nums[0] + 1 - n)
            return nums[-1] + k
        
        left = 0
        right = n - 1
        while left < right:
            mid = (left + right + 1) // 2
            cnt = nums[mid] - nums[0] + 1 - (mid + 1)
            if cnt < k:
                left = mid
            else:
                right = mid - 1

        return nums[left] + k - (nums[left] - nums[0] + 1 - (left + 1))
''',
    call='Solution().missingElement([1,3,6,9,10,14], 5)',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: (f"`nums[{S['mid']}]` 之前缺 `{S['nums'][S['mid']]} − {S['nums'][0]} + 1 − {S['mid']+1}` = ==`{S['cnt']}`== 个，目标 `k = {S['k']}`" if 'cnt' in S else f"整段 `[{S['nums'][0]}, {S['nums'][-1]}]` 共缺 `{S['nums'][-1]-S['nums'][0]+1-len(S['nums'])}` 个，要找第 `{S['k']}` 个")),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}, window=('left', 'right'), h=330,
             label='nums（有序、不重复）'),
    ],
    watch=['k', ('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', 'cnt'],
    captions={
        'n = len(nums)': '`n = {n}`',
        'if k > (nums[-1]': '整段缺失总数 = `{nums[-1]} − {nums[0]} + 1 − {n}` = `{nums[-1]-nums[0]+1-n}`；`k = {k}` 不超过它 → 答案在 `nums[0]` 和 `nums[-1]` 之间',
        'left = 0': '二分「缺失数量 < k」的最后一个下标 p：`left = 0`',
        'right = n - 1': '`right = {right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：继续二分' if S.left < S.right else f'`left = right = {S.left}`：找到 p'),
        'mid = (left': '取上中位数 `mid = {mid}`（`left = mid` 的写法要 +1 防死循环）',
        'cnt = nums[mid]': '`nums[0]` 到 `nums[{mid}]` 理想应有 `{nums[mid]-nums[0]+1}` 个，实际 `{mid+1}` 个 → 缺 `cnt = {cnt}`',
        'if cnt < k': lambda S, B, r: (f'`cnt = {S.cnt} < k = {S.k}`：第 k 个缺失还在 mid 右边' if S.cnt < S.k else f'`cnt = {S.cnt} ≥ k = {S.k}`：第 k 个缺失已经出现在 mid 之前或此处'),
        'left = mid': '`left = mid = {left}`',
        'right = mid - 1': '`right = mid - 1 = {right}`',
        'return nums[left] +': '从 `nums[{left}] = {nums[left]}` 往后数：它之前缺 `{nums[left]-nums[0]+1-(left+1)}` 个，还差 `k − 缺失 = {k-(nums[left]-nums[0]+1-(left+1))}` 个 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='缺失数量 = 理想个数 − 实际个数，用它来二分',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['严格递增数组 `nums` 和整数 `k`，找出 `nums` 最左端起、没出现的第 `k` 个整数',
                 '示例：`[4,7,9,10]`，`k=3` → `8`（缺 5、6、8、…）',
                 '本视频：`[1,3,6,9,10,14]`，`k=5` → `8`'],
        quote='最终缺失的元素数量就是nums[n - 1] - nums[0] + 1 - n。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[0]` 到 `nums[p]` 理想应有 `nums[p]−nums[0]+1` 个，实际 `p+1` 个，差值就是缺失数',
              '`k` 超过总缺失数 → 答案在最右边外面：`nums[-1] + (k − 总缺失)`',
              '否则二分最大的 p 使缺失数 `< k`，答案 = `nums[p] + (k − p 之前缺失数)`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`mid = (left + right + 1) / 2` 已改为 `//`',
                 '`left = mid` 配上中位数要 `+1`，否则死循环',
                 '答案公式里 `nums[p]` 之前缺的数量是 `nums[p]−nums[0]+1−(p+1)`，别漏了 `+1`'],
    ),
)
