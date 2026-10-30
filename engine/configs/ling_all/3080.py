CONFIG = dict(
    num=3080, title='执行操作标记数组中的元素', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='下标排序 + 指针 j · 置 0 当标记',
    tags=[],
    code='''
class Solution:
    def unmarkedSumArray(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        s = sum(nums)
        ids = sorted(range(n), key=lambda i: nums[i])  # 稳定排序
        ans = []
        j = 0
        for i, k in queries:
            s -= nums[i]
            nums[i] = 0  # 标记
            while j < n and k:
                i = ids[j]
                if nums[i]:  # 没有被标记
                    s -= nums[i]
                    nums[i] = 0
                    k -= 1
                j += 1
            ans.append(s)
        return ans
''',
    call='Solution().unmarkedSumArray([1,2,2,1,2,3,1], [[1,2],[3,3],[4,2]])',
    expect=[8, 3, 0],
    views=[
        dict(type='array', var='nums', h=190, label='nums（0 = 已标记）',
             color=lambda S, i, v: 'green' if 'ids' in S and v == 0 else None,
             dim=lambda S, i, v: 'ids' in S and v == 0),
        dict(type='array', var='ids', h=190, label='ids（按 nums 稳定排序后的下标）', pointers={'j': 'blue'},
             dim=lambda S, i, v: 'j' in S and i < S['j']),
        dict(type='array', var='ans', h=130, label='ans'),
    ],
    watch=[('s', 's', 'pink'), ('j', 'j', 'blue'), 'k', ('ans', 'ans', 'green')],
    captions={
        's = sum': '`s` = 未标记元素的和，初始为全部元素之和 `{s}`',
        'ids = sorted': '不能直接给 nums 排序（要按下标标记），所以排下标：`ids = {ids}`。==稳定排序==保证同值时下标小的在前',
        'j = 0': '`j` 指向 `ids` 里下一个候选；==只增不减==，所以所有询问加起来只扫一遍',
        'for i, k in queries': '第 {queries.index([i, k])+1} 个询问：下标 `{i}`，再标记 `{k}` 个最小的',
        'nums[i] = 0': '把 `nums[{i}]` 置 0 = 标记它（题目保证元素为正，0 不会和未标记混淆）',
        'while j < n': '判断 `j < n and k`（`{j} < {n}`，`k = {k}`）→ {"继续找最小的未标记元素" if (j < n and k) else "标记够了或没有元素了，结束"}',
        'i = ids[j]': '按 `ids` 顺序取下一个最小的：下标 `{i}`，值 `{nums[i]}`',
        'if nums[i]': '`nums[{i}] = {nums[i]}` → {"==没被标记==，可以标记" if nums[i] else "已标记过（为 0），跳过"}',
        's -= nums[i]': '`s` 减去 `nums[{i}]`，剩余和 `s = {s}`',
        'k -= 1': '又标记了一个，还需要 `k = {k}` 个',
        'j += 1': '`j` 后移到 {j}：这个位置以后不会再看了（已标记或刚刚被标记）',
        'ans.append': '本轮结束，未标记元素和 `s = {s}`，加入答案',
    },
    cards=dict(
        one_liner='给下标排序，用一个只增不减的指针 j 找最小未标记数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次操作：先标记 `index`，再标记 `k` 个最小的未标记元素（同值取下标小的）',
                 '返回每次操作后未标记元素的和',
                 '示例：`[1,2,2,1,2,3,1]`，操作 `[[1,2],[3,3],[4,2]]` → `[8,3,0]`'],
        quote='不能直接对数组排序（因为有对特定 index 的标记），我们可以创建一个 ids 数组，其中 ids[i]=i，然后对该数组按照 nums[ids[i]] 从小到大排序。注意要使用稳定排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排下标而不是排数组，原数组还能按下标标记',
              '把 `nums[i]` 置 0 当作标记，同时维护未标记和 `s`',
              '`j` 沿 `ids` 只往前走，遇到 0 就跳过，总共 `O(n)`'],
        summary=['时间 `O(n log n)`（排序），之后所有询问共扫 `ids` 一遍，空间 `O(n)`',
                 '==必须稳定排序==，否则同值时不保证下标小的先标记',
                 '内层 `while` 里复用了变量名 `i`，不影响外层 for 的下一次取值',
                 '`j += 1` 放在 `if` 外面：标记过的和刚标记的都不用再看']),
)
