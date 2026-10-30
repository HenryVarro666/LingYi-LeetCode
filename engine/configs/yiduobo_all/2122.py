CONFIG = dict(
    num=2122, title='还原原数组', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 枚举 k + 单调指针验证',
    tags=['滑动窗口与双指针', '贪心与思维', '难度分 2159'],
    code='''
class Solution(object):
    def recoverArray(self, nums):
        def check(double_k):
            used = set()
            p = 0
            for index in range(len(sorted_nums)):
                if index not in used:
                    if p <= index:
                        p = index + 1
                    while p < len(sorted_nums) and sorted_nums[p] != sorted_nums[index] + double_k:
                        p += 1
                    if p == len(sorted_nums):
                        return False

                    used.add(p)
                    p += 1
                    res.append(sorted_nums[index] + double_k // 2)

            return True

        sorted_nums = sorted(nums)
        for num in sorted_nums[1:]:
            double_k = num - sorted_nums[0]
            res = []
            if double_k % 2 == 0 and double_k > 0 and check(double_k):
                break

        return res
''',
    call='Solution().recoverArray([12, 3, 7, 1, 8, 5])',
    expect=[3, 5, 10],
    skip=['used = set()', 'p = 0', 'res = []', 'if p <= index', 'p = index + 1', 'if p == len(sorted_nums)'],
    max_steps=80,
    views=[
        dict(type='array', var='sorted_nums', label='sorted_nums（紫 = 已配走的 higher）', h=250, cell=84,
             pointers={'index': 'blue', 'p': 'pink'},
             color=lambda S, j, x: ('purple' if S.get('used') is not None and j in S['used'] else None)),
        dict(type='array', var='res', label='res（本轮 k 还原出的原数组元素）', h=170, cell=84, index=False),
        dict(type='text', h=70, size=26,
             fn=lambda S: (f"当前试的 `2k = double_k = {S['double_k']}`" if 'double_k' in S else '')),
    ],
    watch=[('double_k', 'double_k', 'yellow'), ('index', 'index', 'blue'), ('p', 'p', 'pink')],
    captions={
        'sorted_nums = sorted(nums)': '先排序：`sorted_nums[0]` 必然是 `arr[0] − k`',
        'for num in sorted_nums[1:]': '试 `sorted_nums[1:]` 里的每个 `num` 当作 `arr[0] + k`',
        'double_k = num - sorted_nums[0]': '`arr[0]+k − (arr[0]−k) = 2k`，所以 `double_k = {num} − {sorted_nums[0]} = {double_k}`',
        'res = []': '清空上一轮留下的 `res`',
        'if double_k % 2 == 0': lambda S, B, r: ('`2k` 是奇数或 0，`k` 不是正整数 → 这个候选不行' if not (S.double_k % 2 == 0 and S.double_k > 0)
                                                 else f'`double_k = {S.double_k}` 是正偶数，进入 `check` 验证'),
        'def check': '`check(double_k)`：验证能否把所有数两两配成 `x` 和 `x + 2k`',
        'used = set()': '`used` 记录已经当作 higher 配走的下标',
        'p = 0': '`p` 在 `sorted_nums` 里单调右移，找 `x + 2k`',
        'for index in range': lambda S, B, r: (f'看 `sorted_nums[{S.index}] = {S.sorted_nums[S.index]}`' + ('，已被配走' if S.index in S.used else '，还没配')),
        'if index not in used': lambda S, B, r: (f'`{S.index}` 没被配走：它是 lower，要找 `{S.sorted_nums[S.index]} + {S.double_k}`' if S.index not in S.used else f'`{S.index}` 已经是别人的 higher，跳过'),
        'if p <= index': '`p` 不能落在 `index` 或之前，否则配到自己',
        'while p < len(sorted_nums)': lambda S, B, r: (f'`sorted_nums[{S.p}] = {S.sorted_nums[S.p]}` ≠ `{S.sorted_nums[S.index] + S.double_k}`，`p` 右移' if S.p < len(S.sorted_nums) and S.sorted_nums[S.p] != S.sorted_nums[S.index] + S.double_k
                                                       else (f'找到了：`sorted_nums[{S.p}] = {S.sorted_nums[S.p]}`' if S.p < len(S.sorted_nums) else '`p` 走到头也没找到')),
        'if p == len(sorted_nums)': lambda S, B, r: ('找不到对应的 higher → 这个 `k` 不合法，`check` 返回 False' if S.p == len(S.sorted_nums) else '找到了配对，继续'),
        'return False': '验证失败，换下一个 `num`',
        'used.add(p)': '`sorted_nums[{p}]` 被当作 higher 配走',
        'p += 1': '`p` 右移一位，下一个 lower 的 higher 一定在它右边（单调）',
        'res.append': '原数 = lower + k = `{sorted_nums[index]} + {double_k // 2}` = =={res[-1]}==',
        'return True': '全部配对成功，`k` 合法',
        'break': '找到合法的 `k`，退出枚举',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='最小值必是 arr[0]−k，枚举第二小的候选算出 k 再验证',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['原数组 `arr` 与正整数 `k`：`lower[i] = arr[i] − k`，`higher[i] = arr[i] + k`',
                 '给出 `lower` 和 `higher` 混在一起的 `2n` 个数 `nums`，还原 `arr`',
                 '本视频：`[12,3,7,1,8,5]` → `[3,5,10]`'],
        quote='由于题目中所有的数都是正整数，那么必然有sorted_nums[0] = arr[0] - k。……sorted_nums[1] - sorted_nums[0] = arr[0] + k - (arr[0] - k) = 2k，因此可以尝试通过sorted_nums[1] - sorted_nums[0]计算出k，然后在sorted_nums中向后遍历验证k是否合法。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小值只能是 `arr[0] − k`；第二小要么是 `arr[0] + k`，要么是 `arr[1] − k`',
              '依次把后面每个数当作 `arr[0] + k`，算出 `2k`；奇数或验证失败就试下一个',
              '验证时 `x + 2k` 的位置随 `index` 单调右移，`check` 只要 `O(n)`'],
        summary=['时间 `O(n^2)`（最多枚举 `2n` 个候选，每个 `check` 是 `O(n)`），空间 `O(n)`',
                 '原文为 Python 2 写法，`double_k / 2` 是整数除法，已改为 `//`；并删去 `:type` 说明与多余空行',
                 '易错：`p <= index` 时要把 `p` 拉到 `index + 1`，否则会配到自己',
                 '题目保证有解，所以 `for` 一定会 `break`，`return res` 取到的是最后一轮的结果'],
    ),
)
