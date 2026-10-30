def _txt(S):
    if 'st' not in S:
        return ''
    parts = ' '.join(f'{p[0]}×{p[1]}' for p in S['st'][1:]) or '空'
    return f"栈中（值×次数）：{parts}，共 `size = {S['size']}` 个，`ans = {S['ans']}`"


CONFIG = dict(
    num=4054, title='统计影子数对 I', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调栈 + 栈中记录出现次数',
    tags=[],
    code='''
class Solution:
    def shadowPairs(self, nums: list[int]) -> int:
        st = [[0, 0]]  # 栈底哨兵
        size = 0  # 栈的大小（出现次数之和）
        ans = 0
        for x in nums:
            while st[-1][0] > x:
                size -= st.pop()[1]  # 栈顶永远无法构成影子对
            ans += size
            if st[-1][0] == x:
                # 恰好等于 x 的 nums[i] 不能构成影子对，要减掉
                ans -= st[-1][1]
                st[-1][1] += 1
            else:
                st.append([x, 1])
            size += 1
        return ans
''',
    call='Solution().shadowPairs([3, 1, 4, 1, 5])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝色 = 当前枚举的 x = j）', cell=100, h=200,
             color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] else None),
        dict(type='stack', var='st', label='st（每项 [值, 出现次数]；第一项是哨兵）', h=200, font=28,
             fmt=lambda p: f'{p[0]}×{p[1]}'),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=[('x', 'x', 'blue'), ('size', 'size', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'st = [[0, 0]]': '栈里存 `[值, 出现次数]`；`[0, 0]` 是栈底哨兵，所有 nums 都 ≥ 1，不会被弹出',
        'size = 0': '`size` = 栈里所有出现次数之和（有多少个候选 i）',
        'for x in nums': lambda S, B, r: (f'枚举 `j`，当前 `x = nums[j] = {S.x}`' if 'x' not in B or B.x != S.x else '所有元素都枚举完了'),
        'while st[-1][0] > x': lambda S, B, r: (f'栈顶 `{S.st[-1][0]}` > `x = {S.x}`：x 就是那个更小的 `nums[k]` → 栈顶永远无法构成影子对'
                                                 if S.st[-1][0] > S.x else f'栈顶 `{S.st[-1][0]}` ≤ `x = {S.x}`：停止弹出，栈从底到顶保持递增'),
        'size -= st.pop()[1]': '弹出 `{B.st[-1][0]}`（共 `{B.st[-1][1]}` 个），`size` 减掉它们 → {size}',
        'ans += size': '栈中剩下的 `{size}` 个数都 ≤ x，先全部算作影子对：`ans` → =={ans}==',
        'if st[-1][0] == x': lambda S, B, r: (f'栈顶 `{S.st[-1][0]}` == `x`：这些相等的数不满足 `nums[i] < nums[j]`' if S.st[-1][0] == S.x
                                              else f'栈顶 `{S.st[-1][0]}` < `x`：{S.size} 个数都能与 x 组成影子对，保留'),
        'ans -= st[-1][1]': '相等的 `{B.st[-1][1]}` 个不算，从 `ans` 减掉 → =={ans}==',
        'st[-1][1] += 1': '栈顶的出现次数加 1 → `{st[-1][1]}`（不用逐个存，避免 O(n²)）',
        'st.append([x, 1])': '`x` 是新值：入栈 `[{x}, 1]`',
        'size += 1': '`size` 加 1 → {size}',
        'return ans': '全部枚举完，影子对一共 =={ret}== 个',
    },
    cards=dict(
        one_liner='右边出现更小的数，左边的它就彻底出局 → 单调栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`(i, j)` 满足 `i < j`、`nums[i] < nums[j]`，且中间没有 `nums[k] < nums[i]`',
                 '数出所有影子对的个数',
                 '示例：`[3,1,4,1,5]` → `(1,2) (1,4) (3,4)`，答案 `3`'],
        quote='枚举 j，同时维护左边能与 nums[j] 构成影子对的 nums[i]。一旦 nums[i] 右边出现比 nums[i] 小的数，那么 nums[i] 无法构成影子对。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用栈保存还可能构成影子对的数；x 比栈顶小，栈顶永远出局，弹出',
              '栈内递增（允许相等），栈里比 x 小的都能和 x 配对',
              '相等的数不能配：栈里存 `(值, 次数)`，用 `size` 记总数，相等时减去该次数'],
        summary=['时间 `O(n)`：每个元素最多入栈、出栈各一次',
                 '易错：栈顶等于 `x` 时要 `ans -= 次数`，因为要求 `nums[i] < nums[j]` 严格小于',
                 '不用逐个数栈里相同元素，否则退化成 `O(n²)`',
                 '同类技巧：1209. 删除字符串中的所有相邻重复项 II'],
    ),
)
