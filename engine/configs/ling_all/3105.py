CONFIG = dict(
    num=3105, title='最长的严格递增或递减子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def longestMonotonicSubarray(self, a: List[int]) -> int:
        ans = 1
        i, n = 0, len(a)
        while i < n - 1:
            if a[i + 1] == a[i]:
                i += 1  # 直接跳过
                continue
            i0 = i  # 记录这一组的开始位置
            inc = a[i + 1] > a[i]  # 定下基调：是严格递增还是严格递减
            i += 2  # i 和 i+1 已经满足要求，从 i+2 开始判断
            while i < n and a[i] != a[i - 1] and (a[i] > a[i - 1]) == inc:
                i += 1
            # 从 i0 到 i-1 是满足题目要求的（并且无法再延长的）子数组
            ans = max(ans, i - i0)
            i -= 1
        return ans
''',
    call='Solution().longestMonotonicSubarray([1,4,3,2,2,5,6,7,8])',
    expect=5,
    views=[
        dict(type='array', var='a', pointers={'i': 'blue', 'i0': 'pink'}, window=('i0', 'i - 1'), h=300,
             label='a（粉 = 这一组起点 i0，蓝 = i，框 = 当前组）'),
        dict(type='text', fn=lambda S: (f"当前组 `[{S['i0']}, {S['i'] - 1}]`，{'严格递增' if S.get('inc') else '严格递减'}，长度 `{S['i'] - S['i0']}`" if 'i0' in S and 'inc' in S and S['i'] > S['i0'] else '')),
    ],
    watch=[('i', 'i', 'blue'), ('i0', 'i0', 'pink'), ('inc', 'inc', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = 1': '单个元素本身就是长度 1 的单调子数组，所以 `ans` 至少是 1',
        'i, n = 0': '`i` 从 0 开始，`n = {n}`',
        'while i < n - 1:': '外层循环：每轮处理一组',
        'if a[i + 1] == a[i]': '`a[{i+1}] = {a[i+1]}`，`a[{i}] = {a[i]}`：{"相等 → 既不增也不减，起不了头" if a[i+1] == a[i] else "不相等 → 可以作为一组的开头"}',
        '直接跳过': '相等，直接跳过：`i` → {i}',
        'i0 = i': '记下这一组起点 `i0 = {i0}`',
        'inc = a[i + 1]': '定基调：`a[{i0+1}] > a[{i0}]` 为 `{inc}` → ==本组严格{"递增" if inc else "递减"}==',
        'i += 2': '`i0` 和 `i0+1` 已满足，从 `i = {i}` 开始检查',
        'while i < n and a[i]': lambda S, B, r: (
            '`i` 到末尾 → 这一组结束' if S.i >= S.n else
            (f'`a[{S.i}] = {S.a[S.i]}` 和 `a[{S.i-1}] = {S.a[S.i-1]}` 方向仍是{"递增" if S.inc else "递减"} → 延长'
             if S.a[S.i] != S.a[S.i-1] and (S.a[S.i] > S.a[S.i-1]) == S.inc else
             f'`a[{S.i}] = {S.a[S.i]}` 和 `a[{S.i-1}] = {S.a[S.i-1]}` 相等或方向反了 → 这一组结束')),
        'i += 1': '继续延长，`i` → {i}',
        'ans = max': '这组 `[{i0}, {i-1}]` 长 `{i} - {i0} = {i - i0}`；`ans = max({B.ans}, {i - i0}) = {ans}`',
        'i -= 1': '==回退一格==：这一组的最后一个元素，可能是下一组（反方向）的第一个元素，两组重叠一个元素。`i` → {i}',
        'return ans': '答案 `{ans}`',
    },
    cards=dict(
        one_liner='分组循环：定下增减基调，吃到不能吃，回退一格再来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求最长的严格递增或严格递减子数组的长度',
                 '单个元素也算（长度 1）',
                 '示例：`[1,4,3,3,2]` → `2`；`[3,2,1]` → `3`'],
        quote='第一个单调序列末尾和第二个单调序列开头，有一个元素是重叠的，所以下面代码在外层循环末尾要把 i 减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['组头 `a[i+1] != a[i]`，并用 `inc` 记下是增还是减',
              '内层：只要仍不相等且方向与 `inc` 相同就延长',
              '例如 `[1,4,3,2]`：`[1,4]` 与 `[4,3,2]` 共用元素 4，所以外层末尾 `i -= 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`：`i` 回退次数是 `O(n)`',
                 '易错点：忘了 `i -= 1`，会漏掉与上一组重叠的那个元素',
                 '`ans` 初始 1：全相等的数组答案是 1',
                 '同类题：2765、978、845、2110'],
    ),
)
