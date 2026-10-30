CONFIG = dict(
    num=2138, title='将字符串拆分为若干长度为 k 的组', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='列表推导式 · 切片 + 补 fill',
    tags=[],
    code='''
class Solution:
    def divideString(self, s: str, k: int, fill: str) -> List[str]:
        n = len(s)
        return [s[i: i + k] + fill * (k - n + i) for i in range(0, n, k)]
''',
    call='Solution().divideString("abcdefghij", 3, "x")',
    expect=['abc', 'def', 'ghi', 'jxx'],
    views=[
        dict(type='string', var='s', label='s', cell=84, h=190),
        dict(type='text', size=30, h=120, fn=lambda S: '切分：' + ' | '.join(S['s'][i:i + S['k']] + ('==' + S['fill'] * (S['k'] - len(S['s']) + i) + '==' if S['k'] - len(S['s']) + i > 0 else '') for i in range(0, len(S['s']), S['k'])) if 's' in S and 'fill' in S else ''),
    ],
    watch=[('n', 'n'), ('k', 'k'), ('i', 'i', 'blue'), ('fill', 'fill')],
    captions={
        'n = len(s)': '`n = len(s) = {n}`',
        'return [': lambda S, B, ret: (f"每隔 `k = {S.k}` 个字符切一组：`s[i: i + k]`；最后一组不足就补 `fill * (k - n + i)`" if 'i' not in S
                                       else f"`i = {S.i}`：取 `s[{S.i}:{S.i + S.k}]` = `{S.s[S.i:S.i + S.k]}`，补 `{max(0, S.k - S.n + S.i)}` 个 `{S.fill}`"),
    },
    cards=dict(
        one_liner='每 k 个字符切一组，最后一组用 fill 补到 k 个',
        complexity='时间 `O(max(n,k))`，空间 `O(1)`（返回值不计）',
        problem=['把 `s` 按顺序每 `k` 个字符分为一组',
                 '最后一组不足 `k` 个时，用字符 `fill` 补满',
                 '示例：`s="abcdefghij"`，`k=3`，`fill="x"` → `["abc","def","ghi","jxx"]`'],
        quote='return [s[i: i + k] + fill * (k - n + i) for i in range(0, n, k)]',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['`range(0, n, k)` 枚举每组的起点 `i`',
              '切片 `s[i: i + k]` 越界时自动截断，只取到末尾',
              '这一组实际长度 `n - i`，还差 `k - (n - i) = k - n + i`；非最后一组为负数，`fill * 负数` 是空串'],
        after=[dict(heading='对照：为什么不用补的组也能写对？', lines=[
            '前面的组：`k - n + i` ≤ 0，`fill * 负数` 为空串',
            '最后一组：`n - i < k`，恰好补 `k - (n - i)` 个',
            '`n` 恰为 `k` 的倍数时，最后一组 `n - i = k`，补 0 个，不会多补'])],
        summary=['时间 `O(max(n,k))`：`fill * (k-n+i)` 最多补 k 个',
                 '易错：`fill * 负数` 得到空串，所以不用单独判断是否为最后一组',
                 '切片越界不会报错，这是 Python 的特性'],
    ),
)
