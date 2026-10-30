CONFIG = dict(
    num=1708, title='长度为K的最大子数组', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='找开头最大值',
    tags=['字符串'],
    code='''
class Solution(object):
    def largestSubarray(self, nums, k):

        start_pos = 0
        for index in range(1, len(nums) - k + 1):
            if nums[index] > nums[start_pos]:
                start_pos = index
            
        return nums[start_pos : start_pos + k]
''',
    call='Solution().largestSubarray([1,4,5,2,3], 3)',
    expect=[5, 2, 3],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = start_pos，粉 = index；灰 = 开头不可选）', cell=100, h=230,
             pointers={'start_pos': 'blue', 'index': 'pink'},
             dim=lambda S, i, v: i > len(S['nums']) - S['k'],
             color=lambda S, i, v: 'blue' if i == S.get('start_pos') else None),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"开头只能选下标 `0 ~ {len(S['nums']) - S['k']}`（共 n−k+1 个），再往后凑不满 `{S['k']}` 个"),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"目前最佳 = `nums[{S['start_pos']}:{S['start_pos'] + S['k']}]` = =={S['nums'][S['start_pos']:S['start_pos'] + S['k']]}==" if 'start_pos' in S else '')),
    ],
    watch=['k', ('start_pos', 'start_pos', 'blue'), ('index', 'index', 'pink')],
    captions={
        'start_pos = 0': '先假设从下标 0 开头，`start_pos = 0`',
        'for index in range': '开头只能在 `0 ~ n-k`，所以 `index` 从 1 扫到 `{len(nums) - k}`',
        'if nums[index] > nums[start_pos]': '`nums[{index}] = {nums[index]}` 对比当前最大开头 `nums[{start_pos}] = {nums[start_pos]}`：=={"更大" if nums[index] > nums[start_pos] else "不更大"}==',
        'start_pos = index': '开头更大 → 字典序更大，`start_pos` 更新为 =={start_pos}==',
        'return': '取 `nums[{start_pos}:{start_pos + k}]`，返回 =={ret}==',
    },
    cards=dict(
        one_liner='数字互不相同：字典序最大，就看谁的开头最大',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回的切片）',
        problem=['数组 `nums` 元素互不相同，求长度为 `k` 的、==字典序最大==的连续子数组',
                 '比较两个子数组：从左到右第一个不同的位置，数字大的更大',
                 '示例：`nums=[1,4,5,2,3], k=3` → `[5,2,3]`'],
        quote='字典序最大的子数组必然就是以数组中最大值开头的子数组，不过在这里还需要注意子数组的长度必须达到k，因此这个开头的下标只能在0到n - k之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['元素各不相同 → 开头一旦更大，后面不用再比',
              '开头下标只能取 `0 ~ n-k`，在这一段里找最大值的下标 `start_pos`',
              '答案就是 `nums[start_pos : start_pos + k]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：范围是 `range(1, n-k+1)`，不能扫到数组末尾，否则凑不满 k 个',
                 '这个结论依赖「元素互不相同」，有重复就要继续比后面的数字',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
