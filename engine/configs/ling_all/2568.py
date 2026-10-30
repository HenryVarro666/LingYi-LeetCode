def _b(x, w=6):
    return format(x & ((1 << w) - 1), 'b').zfill(w)


def _fn(S):
    if 'mask' not in S:
        return ''
    m = S['mask']
    s = f"mask = `{_b(m)}`（记录出现过的 2 的幂次）"
    if m < 0:
        s += f"　取反后 `{_b(m)}`，lowbit = `{_b(m & -m)}` = {m & -m}"
    return s


CONFIG = dict(
    num=2568, title='最小无法得到的或值', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='mask 记 2 的幂次 + lowbit',
    tags=['灵神题单·位运算', '灵神题单·贪心与思维', '难度分 1754'],
    code='''
class Solution:
    def minImpossibleOR(self, nums: List[int]) -> int:
        mask = 0
        for x in nums:
            if (x & (x - 1)) == 0:  # x 是 2 的幂次
                mask |= x
        mask = ~mask
        return mask & -mask  # lowbit
''',
    call='Solution().minImpossibleOR([2,1,7,4,3])',
    expect=8,
    views=[
        dict(type='text', fn=_fn, size=30, h=90),
        dict(type='array', var='nums', label='nums', h=190,
             color=lambda S, i, v: ('yellow' if v == S['x'] else None) if 'x' in S else None,
             dim=lambda S, i, v: bool(v & (v - 1)) and 'mask' in S),
    ],
    watch=[('x', "S.get('x')", 'yellow'), ('mask', "S.get('mask')", 'green')],
    captions={
        'mask = 0': '`mask` 的第 `i` 位为 1，表示 `2^i` 在 `nums` 中出现过',
        'for x in nums': lambda S, B, r: ('所有数都看完了，退出循环' if B.get('x') == S.x else f'看 `x = {S.x}`，二进制 `{format(S.x, "b")}`'),
        'if (x & (x - 1)) == 0': lambda S, B, r: (f'`x & (x-1) = 0`：`{S.x}` 只有一个比特 1，是 2 的幂次 → 记下来' if S.x & (S.x - 1) == 0
                                                   else f'`x & (x-1) = {S.x & (S.x - 1)}` ≠ 0：`{S.x}` 有多个 1，不是 2 的幂次 → 不用管（它只会重复拼出已有的数）'),
        'mask |= x': '把这一位记进 `mask`：`mask` = `{format(mask, "b")}`',
        'mask = ~mask': '取反：现在 1 表示 ==没出现== 的 2 的幂次。最低的那个 1 就是答案',
        'return mask & -mask': '`mask & -mask` 取最低的 1 → ==`{mask & -mask}`==：这个 2 的幂次不在 `nums` 里，拼不出来',
    },
    cards=dict(
        one_liner='1,2,4,… 都在，才能拼出之前所有数：答案是第一个缺失的 2 的幂',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `nums`，选一些元素做 OR 得到的数叫「可表达的」',
                 '求最小的 ==不可表达的正整数==',
                 '示例：`[2,1]` → `4`；`[5,3,2]` → `1`'],
        quote='如果 4 不是答案，说明 4 在 nums 中。那么 5,6,7 肯定不是答案，因为 1,2,4 都在 nums 中，它们可以通过或运算组成 1 到 7 中的任意数字。',
        quote_src='—— 灵茶山艾府题解',
        idea=['1 不是答案 → 1 在 `nums` 里；2 不是答案 → 2 在；这样 3 自然可表达',
              '只有 2 的幂次需要真的出现在数组里，其他数都能由它们拼出',
              '用 `mask` 记录出现过的 2 的幂，取反后的 lowbit 就是最小缺失的幂'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '基础写法：`set(nums)` 里依次判断 `1<<i` 在不在，第一个不在的就是答案',
                 '`~mask` 在 Python 里是负数，`& -` 取 lowbit 依然正确',
                 '同类优化：2154. 将找到的值乘以 2'],
    ),
)
