def _col(S, i, v):
    if 'start' in S and 'i' in S and S['start'] <= i < S['i']:
        return 'green'
    if 'start' in S and 'i' in S and i < S['start']:
        return None
    return None


def _txt(S):
    if 'k' not in S or 'start' not in S:
        return ''
    c = S['i'] - S['start']
    if S['_line'] in (10, 11):
        return f"第 `{S['k']}` 小的数 `{S['a'][S['start']]}` 共 `{c}` 个 → 贡献 `{c} × {S['k']} = {c * S['k']}`"
    return f"正在数第 `{S['k']}` 小的这一组：目前 `{c}` 个相同的数"


CONFIG = dict(
    num=1887, title='使数组元素相等的减少操作次数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 分组循环（Go 原文转写）',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1428'],
    code='''
class Solution:
    def reductionOperations(self, a: List[int]) -> int:
        ans = 0
        a.sort()
        i, k, n = 0, 0, len(a)
        while i < n:
            start = i
            while i < n and a[i] == a[start]:
                i += 1
            ans += (i - start) * k  # [start, i) 区间内的数都是第 k 小的
            k += 1
        return ans
''',
    call='Solution().reductionOperations([5, 1, 3, 3, 1])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='a', label='a（排序后；绿 = 当前这一组相同的数）', cell=96,
             pointers={'start': 'blue', 'i': 'pink'}, color=_col),
    ],
    watch=[('k', 'k', 'yellow'), ('start', 'start', 'blue'), ('i', 'i', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计总操作次数',
        'a.sort()': '==排序==：相同的数挨在一起，第几组就是第几小',
        'i, k, n = 0, 0, len(a)': '`k` 表示当前这组是第几小的数（最小的是第 `0` 小）',
        6: lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还有一组没算' if S.i < S.n else f'`i = {S.i} == n`：所有组都算完了'),
        'start = i': '这一组从 `start = {start}` 开始',
        8: lambda S, B, r: (
            f'`a[{S.i}] = {S.a[S.i]}` == `a[{S.start}]` → 同一组，继续' if S.i < S.n and S.a[S.i] == S.a[S.start]
            else (f'`i = n`，数组走完，这一组结束' if S.i >= S.n
                  else f'`a[{S.i}] = {S.a[S.i]}` ≠ `{S.a[S.start]}` → 这一组结束，`[{S.start}, {S.i})`')),
        'i += 1': '`i` → `{i}`',
        'ans += (i - start) * k': '这一组有 `{i - start}` 个数，都是第 `{k}` 小 → 每个要减 `{k}` 次：`ans += {i - start} × {k}` → =={ans}==',
        'k += 1': '下一组更大一档：`k` → `{k}`',
        'return ans': '总操作数 `{ans}`',
    },
    cards=dict(
        one_liner='每个数要减几次？取决于它是第几小',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计排序）',
        problem=['每次把最大值（多个取最左）减到次大值，直到所有数相等',
                 '求操作次数',
                 '示例：`[5,1,3]` → `3`；`[1,1,2,2,3]` → `4`'],
        quote='相当于求出每个数在数组中是第几小的，排序后遍历一遍即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一个数想变成最小值，要一级一级往下减：==第 k 小的数要减 k 次==',
              '排序后相同的数连成一段，用分组循环找出每一段 `[start, i)`',
              '这一段的每个数都贡献 `k` 次，累加 `(i - start) * k`，再 `k += 1`'],
        result='`[1,1,3,3,5]`：`2×0 + 2×1 + 1×2 = 4` ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.Ints` → `a.sort()`，命名返回值 `ans` 显式初始化）',
                 '时间 `O(n log n)`（排序），空间 `O(1)`（不计排序）',
                 '`k` 是「第几小」，最小的一组 `k = 0` 贡献为 0',
                 '分组循环：内层 while 停下时 `i` 已是下一组开头',
                 '同类题：分组循环模板，参见 1869'],
    ),
)
