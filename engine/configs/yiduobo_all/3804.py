CONFIG = dict(
    num=3804, title='中心子数组的数量', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举起点 + 逐点扩展终点',
    tags=[],
    code='''
class Solution(object):
    def centeredSubarrays(self, nums):
        
        n = len(nums)
        res = 0
        for left in range(n):
            nums_set = set()
            s = 0
            for right in range(left, n):
                nums_set.add(nums[right])
                s += nums[right]
                if s in nums_set:
                    res += 1
        
        return res
''',
    call='Solution().centeredSubarrays([-1, 1, 0])',
    expect=5,
    views=[
        dict(type='array', var='nums', h=230, cell=90,
             pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'),
             label='nums（框 = 子数组 [left, right]）'),
        dict(type='set', var='nums_set', h=170, fmt=lambda x: str(x), label='nums_set'),
        dict(type='text', size=32, fn=lambda S: (f"和 `s = {S['s']}`，`{S['s']} in nums_set` → =={'是' if S['s'] in S['nums_set'] else '否'}==" if 's' in S and S.get('nums_set') and S['_line'] in (11, 12, 13) else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('s', 's', 'yellow'), ('res', 'res', 'green')],
    captions={
        'nums_set = set()': '固定起点 `left = {left}`：集合和子数组和从空开始',
        'range(left, n)': lambda S, B, r: f'终点 `right = {S.right}`：在 `[{S.left}, {S.right - 1}]` 的基础上再加一个数' if S.right > S.left else f'终点从 `left = {S.left}` 开始，先看单个元素',
        'nums_set.add': '集合加入 `nums[{right}] = {nums[right]}`：现在是 `{sorted(nums_set)}`',
        8: '子数组和 `s` 清零，重新累加',
        's += nums[right]': '子数组和在上一个终点基础上加 `{nums[right]}` → =={s}==',
        'if s in nums_set': lambda S, B, r: (f'`{S.s}` 在集合里：和等于某个元素 → 中心子数组' if S.s in S.nums_set
                                             else f'`{S.s}` 不在集合 `{sorted(S.nums_set)}` 里 → 不是'),
        'res += 1': '计数加一：`res` = =={res}==',
    },
    cards=dict(
        one_liner='不要每个子数组重算：终点右移时在上一个子数组上增量更新',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['若子数组之和恰好等于其中某个元素，就是中心子数组',
                 '求 `nums` 中中心子数组的数量，长度不超过 500',
                 '示例：`[-1,1,0]` → `5`'],
        quote='枚举起点和终点，然后一趟遍历计算的时间复杂度为O(n^3)，更常见的处理方式是枚举起点left，然后在此基础上枚举终点right……将时间复杂度降低到O(n^2)。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模不大，直接暴力枚举所有子数组',
              '每个子数组单独遍历是 `O(n^3)`，太慢',
              '固定 `left`，以 `right` 结尾的集合和子数组和，都来自 `right - 1` 再添加 `nums[right]`'],
        summary=['时间 `O(n²)`，空间 `O(n)`',
                 '每换一个 `left`，`nums_set` 和 `s` 都要重新初始化',
                 '原文为 Python 2 风格 `class Solution(object)`，代码无需改动',
                 '对比灵神：灵神用 `for x in nums[i:]` 直接取元素，这里用下标 `left/right` 标出子数组'],
    ),
)
