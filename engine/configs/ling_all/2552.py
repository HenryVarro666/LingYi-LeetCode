NUMS = [1, 3, 2, 4, 5]


def _pat(S):
    if 'l' not in S:
        return '1324 模式：`nums[i] < nums[k] < nums[j] < nums[l]`。枚举右边的 ==4==（下标 `l`），左边维护 132 的个数'
    j = S.get('j')
    nums, l = S['nums'], S['l']
    head = f"枚举 4 = `nums[{l}] = {nums[l]}`；`cnt2` = 已见的 12 模式数 = =={S['cnt2']}=="
    if j is None or S.get('_line') not in (8, 9, 10, 11, 12, 13):
        return head
    return head + f"；当前 3 = `nums[{j}] = {nums[j]}`"


CONFIG = dict(
    num=2552, title='统计上升四元组', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右维护左 · 逐层累加 12→132→1324',
    tags=['动态规划', '难度分 2433'],
    code='''
class Solution:
    def countQuadruplets(self, nums: List[int]) -> int:
        cnt4 = 0
        cnt3 = [0] * len(nums)
        for l in range(2, len(nums)):
            cnt2 = 0
            for j in range(l):
                if nums[j] < nums[l]:  # 3 < 4
                    cnt4 += cnt3[j]
                    # 把 j 当作 i，把 l 当作 k，现在 nums[i] < nums[k]，即 1 < 2
                    cnt2 += 1
                else:  # 把 l 当作 k，现在 nums[j] > nums[k]，即 3 > 2
                    cnt3[j] += cnt2
        return cnt4
''',
    call=f'Solution().countQuadruplets({NUMS})',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 j，粉 l；绿 = 比 nums[l] 小，橙 = 比它大）', h=250, cell=90,
             pointers={'j': 'blue', 'l': 'pink'},
             color=lambda S, i, v: (None if 'l' not in S or 'j' not in S or i >= S['l'] else
                                    ('green' if i < S['l'] and S['nums'][i] < S['nums'][S['l']] else 'orange')) if i != S.get('j') and i != S.get('l') else None,
             dim=lambda S, i, v: 'l' in S and i > S['l']),
        dict(type='array', var='cnt3', label='cnt3[j]：以 nums[j] 当 3 的 132 模式个数', h=230, cell=90,
             pointers={'j': 'blue'}, color=lambda S, i, v: 'yellow' if v > 0 else None),
        dict(type='text', h=80, size=28, fn=_pat),
    ],
    watch=[('l', 'l', 'pink'), ('j', 'j', 'blue'), ('cnt2', 'cnt2', 'cyan'), ('cnt4', 'cnt4', 'green')],
    captions={
        'cnt4 = 0': '`cnt4`：已经找到的 1324 四元组个数',
        'cnt3 = [0]': '`cnt3[j]`：把 `nums[j]` 当作 ==3== 时，左边已有多少个 132 模式',
        'for l in range': lambda S, B, ret: (f'枚举右边的 ==4==：`l = {S.l}`，`nums[l] = {S.nums[S.l]}`，左边的 `j` 依次扮演 3 或 1'
                                             if 'l' not in B or S.l != B.l else '`l` 枚举完了，结束'),
        'cnt2 = 0': '每换一个 4，`cnt2`（左边 12 模式数）重新从 0 数起',
        'if nums[j] < nums[l]': lambda S, B, ret: (
            f'`nums[{S.j}] = {S.nums[S.j]} < nums[{S.l}] = {S.nums[S.l]}`：满足 3 < 4' if S.nums[S.j] < S.nums[S.l]
            else f'`nums[{S.j}] = {S.nums[S.j]} > nums[{S.l}] = {S.nums[S.l]}`：不能当 3，但能让 `l` 当 2（3 > 2）'),
        'cnt4 += cnt3[j]': '`j` 当 3，左边已有 `cnt3[{j}] = {cnt3[j]}` 个 132 → 都能配上 4：`cnt4` = =={cnt4}==',
        'cnt2 += 1': '`j` 当 1、`l` 当 2（`nums[j] < nums[l]`）→ 又多一个 12 模式：`cnt2 = {cnt2}`',
        'cnt3[j] += cnt2': '`l` 当 2、`j` 当 3：前面 `cnt2 = {cnt2}` 个 12 接上它，成为 132 → `cnt3[{j}] = {cnt3[j]}`',
        'return cnt4': '一共 `{cnt4}` 个上升四元组',
    },
    skip=['for j in range'],
    max_steps=90,
    cards=dict(
        one_liner='枚举右边的 4，左边维护 12 → 132 的个数',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`nums` 是 1 到 n 的排列，数 `i<j<k<l` 且 `nums[i] < nums[k] < nums[j] < nums[l]` 的四元组',
                 '把它叫做「1324 模式」',
                 '示例：`[1,3,2,4,5]` → `2`；本视频：`[1,3,2,4,5]` → `2`'],
        quote='我们并不需要单独计算 12 模式的个数，而是把 12 模式的计算过程整合到 132 模式的计算过程中。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['「枚举右，维护左」：固定 4 的位置 `l`，只看它左边',
              '`j` 比 4 小 → 它能当 3，把 `cnt3[j]` 加进答案；同时它能当 1，`cnt2` 加一',
              '`j` 比 4 大 → 它不能当 3，但 4 这个位置可以当 2：`cnt3[j] += cnt2`'],
        summary=['时间 `O(n^2)`，空间 `O(n)`（只有 `cnt3` 一个数组）',
                 '易错：同一轮里 ==先用 cnt2 更新 cnt3，再让 cnt2 变大==的顺序由 if / else 决定，不能混',
                 '`cnt2` 每换一个 `l` 要清零，`cnt3` 则跨轮累积',
                 '方法一（枚举 3 和 2，用 great / less 表）是 `O(n^2)` 空间；利用排列性质可省掉 less',
                 '同类：456 题 132 模式、枚举中间的题'],
    ),
)
