CONFIG = dict(
    num=2210, title='统计数组中峰和谷的数量', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 跳过相同值',
    tags=[],
    code='''
class Solution(object):
    def countHillValley(self, nums):

        res = 0
        last = nums[0]
        for index in range(1, len(nums) - 1):
            if nums[index] == last or nums[index] == nums[index + 1]:
                continue
            if (last < nums[index] and nums[index] > nums[index + 1]) or (last > nums[index] and nums[index] < nums[index + 1]):
                res += 1
            
            last = nums[index]
                
        
        return res
''',
    call='Solution().countHillValley([6,6,5,5,7,3,3,4])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=170, pointers={'index': 'blue'},
             color=lambda S, i, v: ('yellow' if i == S['index'] else None) if 'index' in S else None),
        dict(type='text', h=70, fn=lambda S: (f"last=`{S['last']}`  当前=`{S['nums'][S['index']]}`  右边=`{S['nums'][S['index']+1]}`" if 'index' in S and 'last' in S and S['index'] + 1 < len(S['nums']) else '')),
    ],
    watch=['index', ('last', 'last', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计峰和谷的个数',
        'last = nums[0]': '`last`：左边最近的、值不同的元素，先取 `nums[0]`',
        'for index': '看第 `{index}` 个元素 `{nums[index]}`',
        'if nums[index] == last or': '`{nums[index]}` 和 last `{last}` 相等？和右边 `{nums[index + 1]}` 相等？→ {"相等，属于同一段，跳过，只用最外侧两个值判断" if (nums[index] == last or nums[index] == nums[index + 1]) else "都不等，可以判断"}',
        'if (last <': '`last = {last}`，当前 `{nums[index]}`，右边 `{nums[index + 1]}`：{"两边都更小或都更大 → 峰或谷" if ((last < nums[index] and nums[index] > nums[index + 1]) or (last > nums[index] and nums[index] < nums[index + 1])) else "一边高一边低 → 不是"}',
        'res += 1': '找到一个峰或谷：`res` → =={res}==',
        'last = nums[index]': '`last` 更新为 `{last}`（这一段已处理完）',
        'return res': '一共 `{res}` 个峰和谷',
    },
    cards=dict(
        one_liner='相同值只用最外侧两个判断：比两边都高或都低才计数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['峰：最近的不相等邻居都比它小；谷：都比它大',
                 '相等的相邻下标算同一个峰或谷，首尾元素不算',
                 '示例：`[2,4,1,1,6,5]` → `3`；本视频用 `[6,6,5,5,7,3,3,4]` → `3`'],
        quote='相同值将被算成同一个峰或者谷，因此在判断时如果出现了相同值，应该只利用最外侧的两个值进行峰和谷的判断，略过中部的相同值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`last` 保存左侧最近的不同值',
              '当前值等于 `last` 或等于右边值就 `continue`',
              '否则比较 `last`、当前、右边，两边同时更小或更大就是峰或谷'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`last` 只在真正判断后才更新，跳过的元素不动它',
                 '易错：循环范围是 `1 ~ n-2`，首尾没有两侧邻居'],
    ),
)
