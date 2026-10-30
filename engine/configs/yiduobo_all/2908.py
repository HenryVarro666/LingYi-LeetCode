CONFIG = dict(
    num=2908, title='元素和最小的山形三元组 I', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='前缀最小 + 后缀最小',
    tags=[],
    code='''
class Solution(object):
    def minimumSum(self, nums):

        n = len(nums)
        prefix = [nums[0]]
        for index in range(1, n):
            prefix.append(min(prefix[-1], nums[index]))
        
        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(min(suffix[-1], nums[index]))
        suffix.reverse()

        res = -1
        for index in range(1, n - 1):
            if prefix[index - 1] < nums[index] and suffix[index + 1] < nums[index]:
                if res == -1 or res > prefix[index - 1] + nums[index] + suffix[index + 1]:
                    res = prefix[index - 1] + nums[index] + suffix[index + 1]
        
        return res
''',
    call='Solution().minimumSum([5,4,8,7,10,2])',
    expect=13,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'pink'}, h=150,
             color=lambda S, i, v: 'pink' if S['_line'] >= 17 and i == S['index'] else None),
        dict(type='array', var='prefix', label='prefix（前缀最小值）', h=150,
             color=lambda S, i, v: 'blue' if S['_line'] >= 17 and i == S['index'] - 1 else None),
        dict(type='array', var='suffix', label='suffix（后缀最小值，反转后与下标对齐）', h=150,
             color=lambda S, i, v: 'green' if S['_line'] >= 17 and S.get('index') is not None and i == S['index'] + 1 else None),
    ],
    watch=[('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'prefix = [nums[0]]': '前缀最小值从 `nums[0] = {nums[0]}` 开始',
        'prefix.append': '`prefix` 新增 `min(前一个, nums[{index}])` = =={prefix[-1]}==',
        'suffix = [nums[-1]]': '后缀最小值从最右边 `nums[-1] = {nums[-1]}` 开始，从右往左算',
        'suffix.append': '`suffix` 新增 `min(前一个, nums[{index}])` = =={suffix[-1]}==',
        'suffix.reverse': '倒着算出来的，反转一下，`suffix[i]` 就是 `nums[i..]` 的最小值',
        'if prefix[index - 1]': lambda S, B, ret: f"枚举山顶 `nums[{S['index']}]` = {S['nums'][S['index']]}：左边最小 {S['prefix'][S['index']-1]}、右边最小 {S['suffix'][S['index']+1]}，" + ('都比它小 → ==能当山顶==' if S['prefix'][S['index']-1] < S['nums'][S['index']] and S['suffix'][S['index']+1] < S['nums'][S['index']] else '至少一边不比它小 → 当不了山顶'),
        'if res == -1': '还没有答案，或新三元组和更小？`res = {res}`，新和 = {prefix[index-1] + nums[index] + suffix[index+1]}',
        'res = prefix': '更新答案：`{prefix[index-1]} + {nums[index]} + {suffix[index+1]}` = =={res}==',
        'return res': '返回 =={res}==（-1 表示没找到山形）',
    },
    cards=dict(
        one_liner='枚举山顶，左右两边各取最小，用前后缀数组秒查',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['下标 `i<j<k`，`nums[i]` 和 `nums[k]` 都小于 `nums[j]`，求三数之和最小值',
                 '找不到返回 `-1`',
                 '示例：`[5,4,8,7,10,2]` → `13`（下标 1,3,5）'],
        quote='若 nums[0] 到 nums[j - 1] 之间最小值小于 nums[j]，那么就应该选择这个数作为 nums[i] 才能使得最终答案最小。',
        quote_src='—— yiduobo 题解',
        idea=['目标是和最小，条件是两边都更小，刚好都选区间最小值',
              '前缀最小：左边有没有比 `nums[j]` 小的数；后缀最小：右边同理',
              '正反两趟算出 `prefix`、`suffix`，再枚举 j 一次判断'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '==后缀数组是倒着建的，要 `reverse`==，否则下标对不上',
                 '答案用 `-1` 兼当“未找到”，所以比较前要先判 `res == -1`',
                 '数据更大的 2909 题同样适用，暴力三重循环则过不了'],
    ),
)
