from math import isqrt


def _grp(S):
    n, i = S['n'], S['i']
    return [i * t * t for t in range(1, isqrt(n // i) + 1)]


def _txt(S):
    if 'i' not in S or 'n' not in S:
        return '下标从 1 开始：枚举 core 值 `i`，把下标 `i×j²` 的元素加起来'
    g = _grp(S)
    return f"core = {S['i']} 这一组的下标（从 1 数）：`{'、'.join(map(str, g))}`；已加到 `s = {S.get('s', 0)}`"


CONFIG = dict(
    num=2862, title='完全子集的最大元素和', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='按 core 值分组 · 枚举 i·j²',
    tags=['灵神题单', '数学算法', '难度分 2292'],
    code='''
class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        ans = 0
        n = len(nums)
        for i in range(1, n + 1):
            s = 0
            for j in range(1, isqrt(n // i) + 1):
                s += nums[i * j * j - 1]  # -1 是因为数组下标从 0 开始
            ans = max(ans, s)
        return ans
''',
    call='Solution().maximumSum([8,10,3,8,1,13,7,9,4])',
    expect=20,
    views=[
        dict(type='text', h=90, fn=_txt),
        dict(type='array', var='nums', h=260, label='nums（下标从 0 数，对应题目的 1..n）',
             color=lambda S, i, v: (('yellow' if 'j' in S and S['_line'] >= 8 and i == S['i'] * S['j'] ** 2 - 1 else
                                     'green' if (i + 1) in _grp(S) and 'j' in S and (i + 1) <= S['i'] * S['j'] ** 2 else None)
                                    if 'i' in S and 'n' in S and S.get('j') else None),
             dim=lambda S, i, v: 'i' in S and 'n' in S and (i + 1) not in _grp(S)),
        dict(type='text', h=70, fn=lambda S: f"当前 `s = {S['s']}`，目前最大 `ans = {S['ans']}`" if 's' in S and 'ans' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('s', 's', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'for i in range': lambda S, B, r: ('`i` 枚举完了，退出循环' if B.get('i') == S.i else f'枚举 core 值 `i = {S.i}`：这一组的下标是 `i×1², i×2², i×3², …`，和 `s` 从 0 开始'),
        'for j in range': lambda S, B, r: (f'`j = {S.j}`（上限 `isqrt({S.n}//{S.i}) = {isqrt(S.n // S.i)}`，保证 `i×j² ≤ n` 不越界）' if S.s == 0 else f'`j` 取下一个：`j = {S.j}`，下标 `{S.i}×{S.j}² = {S.i * S.j * S.j}`' if B.get('j') != S.j else f'`j` 用完了（到上限 `{isqrt(S.n // S.i)}`），这一组的和 `s = {S.s}`'),
        's += nums': '下标 `{i}×{j}² = {i * j * j}`（从 1 数），元素 `{nums[i * j * j - 1]}` 加入这一组：`s = {B.s} + {nums[i * j * j - 1]} = {s}`',
        'ans = max': '`ans = max({B.ans}, {s}) = {ans}`：==这一组的和能否刷新答案==',
        'return ans': '所有 core 组都枚举过 → 最大元素和 `{ans}`',
    },
    skip=['s = 0'],
    max_steps=90,
    cards=dict(
        one_liner='下标 core 值相同的元素分一组，答案是组内和的最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['下标从 1 开始，选一组下标，要求任意两个下标的乘积都是 ==完全平方数==',
                 '求被选中元素的最大和',
                 '示例：`[8,10,3,8,1,13,7,9,4]` → `20`（选下标 1、4、9）'],
        quote='同一组内的数字下标的 core 值必须都一样。那么按照下标的 core 值分组，累加同一组的元素和，最大元素和即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`core(n)` 是 n 去掉完全平方因子后的结果，如 `core(8) = 2`',
              '两下标乘积是完全平方数 ⇔ 它们的 core 相同，所以同 core 的下标成一组',
              '方法二：枚举 `i`，这组下标就是 `i×j²`；就算 `i` 不是 core 也没关系，因为它是真 core 那一组的子集，不会超过它'],
        summary=['方法二每个 `i` 只循环 `√(n/i)` 次，调和型求和得 `O(n)`',
                 '易错点：下标从 1 数，取数组时要 `-1`',
                 '灵神另给两种写法：方法一对每个下标分解出 core 再分组（`O(n√n)`），方法三预处理 core 表；这里演示方法二'],
    ),
)
