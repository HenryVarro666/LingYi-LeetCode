CONFIG = dict(
    num=3396, title='使数组元素互不相同所需的最少操作次数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='哈希表计数 · 模拟删除',
    tags=[],
    code='''
class Solution(object):
    def minimumOperations(self, nums):
        
        cnt = {}
        same = 0
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            if cnt[v] == 2:
                same += 1
        
        res = 0
        p = 0
        while same > 0:
            res += 1
            for index in range(p, min(p + 3, len(nums))):
                v = nums[index]
                cnt[v] -= 1
                if cnt[v] == 1:
                    same -= 1
            p += 3
        
        return res
''',
    call='Solution().minimumOperations([1, 2, 3, 4, 2, 3, 3, 5, 7])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue', 'p': 'pink'}, h=240,
             color=lambda S, i, v: 'red' if 'p' in S and 'res' in S and i < S['p'] and S.get('_line', 0) >= 14 else None,
             label='nums（红色 = 已被移除的前缀）'),
        dict(type='map', var='cnt', fmt=lambda k, v: f'{k}: {v}', h=200),
        dict(type='text', fn=lambda S: f'重复元素种数 `same = {S["same"]}`，已操作 `res = {S["res"]}` 次' if 'same' in S and 'res' in S else '', size=28, h=80),
    ],
    watch=[('same', 'same', 'orange'), ('res', 'res', 'green'), ('p', 'p', 'pink'), ('index', 'index', 'blue')],
    captions={
        'cnt = {}': '`cnt` 统计每个数出现的次数',
        'same = 0': '`same` 记录当前有多少种数是重复的',
        'for v in nums': '先整体扫一遍，当前 `v = {v}`',
        'cnt[v] = cnt.get': '`cnt[{v}] = {cnt[v]}`',
        'if cnt[v] == 2': '`cnt[{v}] == 2`？{"是：它刚变成重复" if cnt[v] == 2 else "否"}',
        'same += 1': '`{v}` 刚刚变成重复，`same = {same}`',
        'res = 0': '接下来模拟操作：`res` 是操作次数',
        'p = 0': '`p` 是下一次要删除的起点',
        'while same > 0': '`same = {same}`：{"还有重复，继续删" if same > 0 else "没有重复了，停止"}',
        'res += 1': '再做一次操作，`res = {res}`',
        'for index in range': '这次删除下标 `[{p}, {min(p+3, len(nums))})` 的元素，当前 `index = {index}`',
        'v = nums[index]': '删掉 `{v}`',
        'cnt[v] -= 1': '`cnt[{v}]` 减为 `{cnt[v]}`',
        'if cnt[v] == 1': '`cnt[{v}] == 1`？{"是：它不再重复" if cnt[v] == 1 else "否，还是重复或已清零"}',
        'same -= 1': '`{v}` 不再重复，`same = {same}`',
        'p += 3': '起点后移 3，`p = {p}`',
        'return res': '共操作 `{res}` 次',
    },
    cards=dict(
        one_liner='先数出重复的数，再一轮轮删前 3 个直到没有重复',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次操作移除数组开头 3 个元素（不足 3 个就全移除）',
                 '求使元素互不相同的最少操作次数',
                 '示例：`[1,2,3,4,2,3,3,5,7]` → `2`'],
        quote='使用哈希表cnt记录每种元素出现的次数，另外使用一个变量same记录nums中重复元素的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历：`cnt[v]` 从 1 变 2 时，`same` 加 1',
              '再按题意模拟：每轮删 3 个，`cnt[v]` 从 2 变 1 时 `same` 减 1',
              '`same` 变成 0，已执行的轮数就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`cnt` 从 2 变 1 才让 `same` 减 1，从 3 变 2 仍是重复',
                 '`min(p + 3, len(nums))` 处理最后不足 3 个的情况',
                 '对比灵神：灵神倒着找最长无重复后缀，一趟 `O(n)`；这里是正向模拟'],
    ),
)
