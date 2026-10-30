def _cap_if(S, B, ret):
    idx, num, n = S.index, S.num, S.n
    pre = f'放入 `num = {num}`：index ==从大到小==枚举。' if idx == n else ''
    if S.f[idx - num]:
        return pre + f'`f[{idx - num}]` 为真 → 能凑出 {idx - num}，再选 `{num}` 正好凑出 {idx}'
    k = idx - num
    if k - num >= 0 and S.f[k - num]:
        return pre + f'`f[{k}]` 为假（它稍后才会因 `{num}` 变真）→ ==倒序保证读到旧值==，`{num}` 不会被用两次'
    return pre + f'`f[{k}]` 为假 → 凑不出 {k}，`f[{idx}]` 不变'


def _text(S):
    if 'index' not in S:
        return '`f[j]`：能否从 nums 中选出和==刚好==为 `j` 的子集'
    idx, num = S['index'], S['num']
    tf = lambda b: 'T' if b else 'F'
    return f"若 `f[{idx} - {num}]` = `f[{idx - num}]` 为真 → `f[{idx}]` 为真　（当前 `f[{idx - num}]` = {tf(S['f'][idx - num])}）"


CONFIG = dict(
    num=416, title='分割等和子集', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='背包 DP（滚动数组，倒序枚举）',
    code='''
class Solution(object):
    def canPartition(self, nums):
        n = sum(nums)
        if n & 1:
            return False

        n //= 2
        f = [False] * (n + 1)
        f[0] = True

        for num in nums:
            for index in range(n, num - 1, -1):
                if f[index - num]:
                    f[index] = True

        return f[n]
''',
    call='Solution().canPartition([3, 1, 2, 4])',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums（黄 = 当前 num，暗 = 已放入）', cell=96,
             color=lambda S, k, v: 'yellow' if 'index' in S and v == S['num'] else None,
             dim=lambda S, k, v: 'index' in S and k < S['nums'].index(S['num'])),
        dict(type='array', var='f', label='f[j]（黄 = 当前 index，蓝 = 依赖的 index-num；index 从右往左走 ←）',
             cell=110, h=250, pointers={'index': 'yellow', 'index - num': 'blue'},
             pointer_labels={'index - num': 'index-num'},
             color=lambda S, k, v: 'yellow' if 'index' in S and k == S['index'] else
                                   ('blue' if 'index' in S and k == S['index'] - S['num'] else ('green' if v else None))),
    ],
    watch=[('num', 'num', 'yellow'), ('index', 'index', 'yellow'), ('index-num', 'index - num', 'blue'), ('n', 'n', 'green')],
    skip=['for num in nums', 'for index in range'],
    captions={
        'n = sum': '先算所有数的和 `sum = {n}`',
        'if n & 1': lambda S, B, ret: (f'`{S.n}` 是奇数 → 显然无法达成' if S.n & 1 else
                                       f'`{S.n}` 是偶数 → 需要选出一部分数，和为 `{S.n // 2}`'),
        'n //= 2': '目标和 `n = {n}`：题目转化为==经典的背包问题==',
        'f = [False]': '`f[i][j]` 可以滚动 → 只留一维 `f[j]`：能否选出和==刚好==为 j 的子集',
        'f[0] = True': '`f[0] = True`：什么都不选，和就是 0',
        'if f[index - num]': _cap_if,
        'f[index] = True': lambda S, B, ret: (f'`f[{S.index}] = True`' + ('（本来就是 True）' if B.f[S.index] else '')
                                              + f'：和为 {S.index} ==可以凑出=='),
        'return f[n]': '`f[{n}]` = =={ret}==：能选出和为 `{n}` 的子集（如 `1 + 4`、`3 + 2`）',
    },
    cards=dict(
        one_liner='凑出 sum/2 就是背包；滚动成一维后 j 从大到小',
        complexity='时间 `O(n·sum)`，空间 `O(sum)`',
        problem=['只含正整数的非空数组 `nums`，能否分成==元素和相等==的两个子集？',
                 '示例：`[1,5,11,5]` → `true`（`[1,5,5]` 和 `[11]`）',
                 '演示：`[3,1,2,4]` → `true`（`[3,2]` 和 `[1,4]`）'],
        quote='令f[i][j]表示对nums中前i个数中能否选取出和刚好为j的子集，于是就有==当f[i - 1][j - nums[i]]为真时，就有f[i][j]为真==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`sum` 为奇数显然不行；偶数则要从 nums 里选出和为 `sum/2` 的数 → ==背包==',
              '前 `i-1` 个数能凑出 `j - nums[i]`，选上第 i 个数，和就正好是 `j`',
              '`f[i][j]` 符合滚动形式 → 省掉 i 这一维，但 ==j 要从大到小迭代=='],
        after=[dict(heading='为什么 j 要从大到小？', lines=[
            '倒序时，读到的 `f[index - num]` 还是==上一轮==（还没放 num）的值',
            '若正序：比如 `num = 1`，先令 `f[1] = True`，接着 `f[2]` 又由 `f[1]` 推出',
            '→ 同一个 `1` 被用了两次，变成了完全背包，答案就错了',
        ])],
        summary=['时间 `O(sum · n)`；每个数 ≤ 100，最坏约 `O(50 · n²)`（作者原话）',
                 '原文为 Python 2 写法：`n /= 2` 已改为 `n //= 2`，并删掉 docstring',
                 '注意：这里的 `n` 是元素和，不是数组长度',
                 '对比灵神：先写二维 `f[i+1][j]` 再空间优化，还给了 bitset 写法'],
    ),
)
