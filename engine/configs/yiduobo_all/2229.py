CONFIG = dict(
    num=2229, title='检查数组是否连贯', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='集合去重 + 最大最小值之差',
    tags=[],
    code='''
class Solution(object):
    def isConsecutive(self, nums):

        vis = set(nums)
        return max(nums) - min(nums) + 1 == len(vis) == len(nums)
''',
    call='Solution().isConsecutive([4,2,5,3])',
    expect=True,
    views=[
        dict(type='array', var='nums', h=230, label='nums'),
        dict(type='set', var='vis', h=200, label='vis（去重后的集合）'),
        dict(type='text', fn=lambda S: (f"`max − min + 1 = {max(S['nums'])} − {min(S['nums'])} + 1 = ` =={max(S['nums'])-min(S['nums'])+1}==，`len(vis) = {len(S['vis'])}`，`len(nums) = {len(S['nums'])}`" if 'vis' in S else '')),
    ],
    watch=[('len(nums)', 'len(nums)', 'blue'), ('len(vis)', 'len(vis)', 'green')],
    captions={
        'vis = set': '把所有数放进集合：有重复的话，`len(vis)` 会 ==小于== `len(nums)` → `vis` = {sorted(vis)}',
        'return max': '三者相等才连贯：`{max(nums)} - {min(nums)} + 1 = {max(nums)-min(nums)+1}`，`len(vis) = {len(vis)}`，`len(nums) = {len(nums)}` → =={ret}==',
    },
    cards=dict(
        one_liner='不重复，且最大值减最小值恰好是长度减 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定整数数组 `nums`，判断它排序后是否是连续整数（每个数比前一个大 1）',
                 '示例：`[1,3,4,2]` → `True`；`[1,3,5]` → `False`',
                 '本视频：`[4,2,5,3]` → `True`'],
        quote='若数组不重复且连贯，那么数组中的最大值与最小值之差必然为数组长度减1，那么只需检测数组最大值和最小值之差是否恰好等于数组长度减1即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用集合判重：`len(vis) != len(nums)` 说明有重复，直接不连贯',
              '无重复时，`n` 个互不相同的整数要塞进 `max−min+1` 个位置',
              '恰好塞满（`max−min+1 == n`）就说明中间一个空位都没有'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：只比较最大最小值之差而不判重，`[1,1,3]` 会误判',
                 '链式比较 `a == b == c` 等价于 `a == b and b == c`',
                 '原文无需改动即可在 Python 3 运行'],
        after=[dict(heading='反例：为什么要判重', lines=['`[1,1,3]`：最大 3，最小 1，`3−1+1 = 3 = len(nums)`', '只看最大最小值会误判为连贯', '但 `len(vis) = 2 ≠ 3`，判重后正确返回 `False`'])],
    ),
)
