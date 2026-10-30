NUMS = [2, 7, 1, 19, 18, 3, 5, 4, 6]


def _counted(S):
    """已经计入答案的下标（0-based）"""
    if 'i' not in S:
        return set()
    n, i, ln = S['n'], S['i'], S.get('_line')
    out = set()
    for d in range(1, i + 1):
        if n % d:
            continue
        cur = d == i
        if not cur or ln in (6, 7, 8):
            out.add(d - 1)
        if d * d < n and (not cur or ln == 8):
            out.add(n // d - 1)
    return out


def _color(S, idx, v):
    c = _counted(S)
    if idx in c:
        return 'green'
    return None


def _p_small(S):
    return S['i'] - 1 if 'i' in S and S.get('_line') in (5, 6, 7, 8) else None


def _p_big(S):
    if 'i' in S and S.get('_line') in (6, 7, 8) and S['n'] % S['i'] == 0 and S['i'] * S['i'] <= S['n']:
        return S['n'] // S['i'] - 1
    return None


def show(S):
    if 'n' not in S:
        return ''
    n = S['n']
    pairs = [f'{d}×{n // d}' for d in range(1, int(n ** 0.5) + 1) if n % d == 0]
    s = f"`n = {n}` 的因子成对出现：`{'，'.join(pairs)}`；只需枚举 `i ≤ √n = {int(n ** 0.5)}`"
    return s


CONFIG = dict(
    num=2778, title='特殊元素平方和', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='枚举因子 · 只枚举到 √n',
    tags=['字节30天'],
    code='''
class Solution:
    def sumOfSquares(self, nums: List[int]) -> int:
        ans, n = 0, len(nums)
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                ans += nums[i - 1] ** 2  # 注意数组的下标还是从 0 开始的
                if i * i < n:  # 避免重复统计
                    ans += nums[n // i - 1] ** 2
        return ans
''',
    call=f'Solution().sumOfSquares({NUMS})',
    expect=41,
    views=[
        dict(type='array', var='nums', label='nums（题目下标从 1 开始，第 k 个数是 nums[k-1]；绿 = 已计入）', cell=96,
             pointers={_p_small: 'blue', _p_big: 'pink'},
             pointer_labels={_p_small: '第 i 个', _p_big: '第 n/i 个'}, color=_color, h=245),
        dict(type='text', fn=show, size=26, h=90, lines=2),
        dict(type='text', fn=lambda S: (f"答案 `ans = {S['ans']}`" if 'ans' in S else ''), size=30, h=70),
    ],
    watch=[('n', 'n'), ('i', 'i', 'blue'), ('n // i', lambda S: S['n'] // S['i'] if 'i' in S else None, 'pink'),
           ('ans', 'ans', 'green')],
    captions={
        'ans, n = 0, len(nums)': '`n = {n}`：第 `k` 个数是特殊元素 ⇔ `k` 是 `n` 的因子',
        'for i in range(1, isqrt(n) + 1)': lambda S, B, ret: (
            f'枚举 `i = {S.i}`（只到 `isqrt({S.n}) = {int(S.n ** 0.5)}`）' if S.i != B.get('i') else '枚举结束'),
        'if n % i == 0': lambda S, B, ret: (f'`{S.n} % {S.i} = {S.n % S.i}` → 不是因子' if S.n % S.i else
                                            f'`{S.n} % {S.i} == 0` → `{S.i}` 是因子，`{S.n} // {S.i} = {S.n // S.i}` ==也是因子=='
                                            if S.i * S.i != S.n else
                                            f'`{S.n} % {S.i} == 0` → `{S.i}` 是因子，配对的 `{S.n} // {S.i}` 就是它自己'),
        'ans += nums[i - 1] ** 2': '第 `{i}` 个数 `nums[{i - 1}] = {nums[i - 1]}`：`ans += {nums[i - 1]}²` → `{ans}`（==下标还是从 0 开始==）',
        'if i * i < n': lambda S, B, ret: (f'`{S.i}×{S.i} < {S.n}` → 另一个因子 `{S.n // S.i}` 和 `{S.i}` 不同，也要统计'
                                           if S.i * S.i < S.n else
                                           f'`{S.i}×{S.i} == {S.n}`：另一个因子就是 `{S.i}` 自己 → ==避免重复统计=='),
        'ans += nums[n // i - 1] ** 2': '第 `{n // i}` 个数 `nums[{n // i - 1}] = {nums[n // i - 1]}`：`ans += {nums[n // i - 1]}²` → `{ans}`',
        'return ans': '所有因子都统计完：返回 =={ret}==',
    },
    cards=dict(
        one_liner='i 是 n 的因子时 n/i 也是，只需枚举到 √n',
        complexity='时间 `O(√n)`，空间 `O(1)`',
        problem=['数组 `nums` ==下标从 1 开始==，长度为 `n`',
                 '若 `n % i == 0`，则 `nums[i]` 是特殊元素；返回所有特殊元素的==平方和==',
                 '示例：`[2,7,1,19,18,3]` → `2² + 7² + 1² + 3² = 63`；本视频用 `n = 9` 的数组'],
        quote='根据题意，`i` 是 `n` 的因子，此时 `n/i` 也是 `n` 的因子，那么==只需要枚举 √n 以内的 i==，就可以得到大于 √n 的另一个因子了。',
        quote_src='—— 灵茶山艾府题解「算法二：枚举」',
        idea=['因子成对出现：`i × (n/i) = n`，较小的那个一定 `≤ √n`',
              '枚举到 `i` 时，同时统计第 `i` 个和第 `n/i` 个数',
              '`i × i == n` 时两个因子是同一个，只统计一次'],
        result='`n = 9` 的因子是 `1, 3, 9`：`2² + 1² + 6² = 41` ✓',
        summary=['时间 `O(√n)`，空间 `O(1)`',
                 '易错 1：题目下标从 1 开始，代码里要写 `nums[i - 1]`',
                 '易错 2：完全平方数时 `i == n / i`，不判断 `i * i < n` 会重复统计',
                 '算法一（遍历）：枚举每个下标 `i` 判断 `n % i == 0`，`O(n)`'],
    ),
)
