CONFIG = dict(
    num=2680, title='最大或值', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前缀或 + 后缀或 · 枚举左移的数',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def maximumOr(self, nums, k):

        prefix = []
        suffix = []

        n = len(nums)
        for index in range(n):
            prefix.append(nums[index])
            if index > 0:
                prefix[-1] |= prefix[-2]
        
        for index in range(n - 1, -1, -1):
            suffix.append(nums[index])
            if index < n - 1:
                suffix[-1] |= suffix[-2]
        
        suffix.reverse()

        res = 0
        for index in range(n):
            v = nums[index] << k
            if index > 0:
                v |= prefix[index - 1]
            if index < n - 1:
                v |= suffix[index + 1]
        
            res = max(res, v)
        
        return res
''',
    call='Solution().maximumOr([6,4,5], 1)',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}),
        dict(type='array', var='prefix', label='prefix（前缀或）'),
        dict(type='array', var='suffix', label='suffix（后缀或）'),
        dict(type='text', fn=lambda S: (f"当前候选 `v = {S['v']}`　最大 `res = {S['res']}`" if 'v' in S and 'res' in S else ''), size=36),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'purple'), ('res', 'res', 'green')],
    captions={
        'prefix = []': '`prefix[i]` 记 `nums[0..i]` 的 OR',
        'suffix = []': '`suffix[i]` 记 `nums[i..n-1]` 的 OR',
        'n = len': '`n = {n}`',
        'for index in range(n):': lambda S, B, r: ('从左往右扫，算前缀或' if S['_line'] == 8 else '枚举哪个数作为被左移的那个'),
        'for index in range(n - 1': '再从右往左扫（下标 `n-1` 到 `0`），算后缀或',
        'prefix.append(nums[index])': '先放入 `nums[{index}]`',
        'prefix[-1] |= prefix[-2]': '和上一个前缀或再 OR：`prefix[{index}]` = {prefix[-1]}',
        'suffix.append(nums[index])': '从右往左，先放入 `nums[{index}]`',
        'suffix[-1] |= suffix[-2]': '和右边的后缀或再 OR：得到 {suffix[-1]}',
        'suffix.reverse()': '后缀或是从右往左存的，==反转==后下标就和 `nums` 对齐了：{suffix}',
        'res = 0': '`res` 记最大的或值',
        'v = nums[index] << k': '假设把 `nums[{index}]` 左移 `{k}` 位（==操作集中在一个数上==）：`v = {v}`',
        'v |= prefix[index - 1]': '并上它左边所有数的 OR：`v` → {v}',
        'v |= suffix[index + 1]': '并上它右边所有数的 OR：`v` → {v}',
        'res = max(res, v)': '这个数左移后整体或值是 `{v}`，`res` → {res}',
        'return res': '不一定移最大的数，枚举所有数后最大是 `{ret}`',
    },
    cards=dict(
        one_liner='操作全放在同一个数上，枚举它，前缀或 | 后缀或 O(1) 拼出结果',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次可把一个数左移（乘 2），最多 `k` 次',
                 '求数组所有数按位或的最大值',
                 '示例：`[8,1,2], k=2` → `35`；本视频：`[6,4,5], k=1` → `15`'],
        quote='这些左移操作都应该集中在同一个数字上，因为这样才能使得某个1被推到更高的数位上，从而使得最终结果最大。但是需要注意的是，在这里并不一定是选择最大的数进行左移操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['6=110 与 4=100：移 6 得 1100，低位的 1 被浪费；移 4 得 1000 | 110 = 1110',
              '无法直接判断移谁，就一趟遍历枚举',
              '先正反两遍预处理前缀或、后缀或，枚举时三者取或'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`suffix` 是倒着 append 的，别忘了 `reverse()`',
                 '边界：第一个数没有前缀、最后一个数没有后缀，所以有 `index > 0` 等判断',
                 '对比灵神：灵神只预处理后缀，前缀边遍历边算'],
    ),
)
