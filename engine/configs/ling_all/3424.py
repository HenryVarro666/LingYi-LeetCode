CONFIG = dict(
    num=3424, title='将数组变相同的最小代价', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序配对 · 交换论证',
    tags=['贪心算法', '思维题', '难度分 1503'],
    code='''
class Solution:
    def minCost(self, a: List[int], b: List[int], k: int) -> int:
        ans2 = sum(abs(x - y) for x, y in zip(a, b))
        if ans2 <= k:
            return ans2

        a.sort()
        b.sort()
        ans1 = sum(abs(x - y) for x, y in zip(a, b)) + k
        return min(ans1, ans2)
''',
    call='Solution().minCost([-7,9,5], [7,-2,-5], 2)',
    expect=13,
    views=[
        dict(type='array', var='a', h=200, label='a', color=lambda S, i, v: 'blue'),
        dict(type='array', var='b', h=200, label='b', color=lambda S, i, v: 'pink'),
        dict(type='text', h=130, fn=lambda S: (
            f"不重排：`|a−b|` 之和 ans2 = ==" + str(S['ans2']) + '==' if 'ans2' in S and 'ans1' not in S and not S.get('_sorted') else '')
            + (f"　排序配对：ans1 = `Σ|a−b| + k` = ==" + str(S['ans1']) + '==' if 'ans1' in S else '')),
    ],
    watch=['k', ('ans2', 'ans2', 'blue'), ('ans1', 'ans1', 'pink')],
    captions={
        'ans2 =': '不用操作一：逐位 `|a[i] − b[i]|` 求和，`ans2 = {ans2}`',
        'if ans2 <= k': lambda S, B, r: (f'`ans2 = {S.ans2} ≤ k = {S.k}` → 重排的代价已经不比它小，直接返回' if S.ans2 <= S.k else f'`ans2 = {S.ans2} > k = {S.k}` → 值得考虑重排（花 `k`），继续'),
        'a.sort()': '重排用掉 `k`，就把 `a` 拆成单个元素任意排：先排序 → `a = {a}`',
        'b.sort()': '`b` 也排序 → `b = {b}`：最小配最小、次小配次小，由交换论证得最优',
        'ans1 =': '排序后逐位求差再加 `k`：`ans1 = {ans1}`',
        'return min': '`min(ans1, ans2) = min({ans1}, {ans2})` = =={ret}==',
    },
    cards=dict(
        one_liner='要么不重排；要么全拆开任意排，排序后一一配对',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['操作一：把 `arr` 切成连续段并任意重排，代价 `k`',
                 '操作二：某个元素加减 `x`，代价 `x`',
                 '示例：`arr=[-7,9,5], brr=[7,-2,-5], k=2` → `13`'],
        quote='如果使用操作一，那么直接把 a 分成 n 个长为 1 的子数组，这样 a 就可以随意排了。最优配对方式是最小的 a[i] 与最小的 b[i] 一对，次小的 a[i] 与次小的 b[i] 一对。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不用操作一：答案是 `Σ|a[i] − b[i]|`',
              '用操作一：分成 `n` 个长 1 的段，随便排，只花一次 `k`，排序配对最优（交换论证）',
              '优化：`ans2 ≤ k` 时重排不可能更优，直接返回，省掉排序'],
        summary=['时间 `O(n log n)`，空间 `O(1)`（`sort` 原地排序，会改动输入）',
                 '重排最多用一次：分成单元素后已经能得到任意排列',
                 '`k` 很大时，代码先返回 `ans2`，不进入排序',
                 '同类：交换论证法（§1.7）、从最小/最大开始贪心（§1.1）'],
    ),
)
