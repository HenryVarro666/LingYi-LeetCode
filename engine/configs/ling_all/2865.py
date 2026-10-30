CONFIG = dict(
    num=2865, title='美丽塔 I', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='前后缀分解 + 单调栈',
    tags=[],
    code='''
class Solution:
    def maximumSumOfHeights(self, a: List[int]) -> int:
        n = len(a)
        suf = [0] * (n + 1)
        st = [n]  # 哨兵
        s = 0
        for i in range(n - 1, -1, -1):
            x = a[i]
            while len(st) > 1 and x <= a[st[-1]]:
                j = st.pop()
                s -= a[j] * (st[-1] - j)  # 撤销之前加到 s 中的
            s += x * (st[-1] - i)  # 从 i 到 st[-1]-1 都是 x
            suf[i] = s
            st.append(i)

        ans = s
        st = [-1]  # 哨兵
        pre = 0
        for i, x in enumerate(a):
            while len(st) > 1 and x <= a[st[-1]]:
                j = st.pop()
                pre -= a[j] * (j - st[-1])  # 撤销之前加到 pre 中的
            pre += x * (i - st[-1])  # 从 st[-1]+1 到 i 都是 x
            ans = max(ans, pre + suf[i + 1])
            st.append(i)
        return ans
''',
    call='Solution().maximumSumOfHeights([6,5,3,9,2,7])',
    expect=22,
    views=[
        dict(type='text', size=26, fn=lambda S: (
            ('右侧递减段：从右往左，`suf[i]` = 以 i 为峰右边的最大和' if S['_line'] < 17 else '左侧递增段：从左往右，`pre` = 以 i 为峰左边的最大和，答案 = `pre + suf[i+1]`')
            if 'st' in S else '')),
        dict(type='array', var='a', label='a（蓝 = 当前 i）', pointers={'i': 'blue'}, h=170,
             color=lambda S, k, v: 'blue' if S.get('i') == k else None),
        dict(type='array', var='suf', label='suf[i]（右侧最大和）', h=170),
        dict(type='stack', var='st', label='单调栈（存下标，栈底 → 栈顶严格递增）', h=200,
             fmt=lambda x: f'{x}(哨)' if x in (-1, 6) else str(x)),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'green'), ('pre', 'pre', 'cyan'), ('ans', 'ans', 'orange')],
    captions={
        'suf = [0]': '`suf[i]`：从 `a[i]` 到末尾形成递减段的最大和，多开一位 `suf[n] = 0`',
        'st = [n]': '栈里只存下标，先放哨兵 `n`，免去判空',
        'while len(st) > 1 and x <= a[st[-1]]': lambda S, B, r: (
            f'`a[{S.i}] = {S.x}` ≤ 栈顶值 `{S.a[S.st[-1]]}`：栈顶那些更高的塔会被压到 `{S.x}` → 要撤销' if len(S.st) > 1 and S.x <= S.a[S.st[-1]]
            else f'`{S.x}` 大于栈顶（或栈空）→ 不用撤销，直接加'),
        's -= a[j]': '撤销 `a[{j}] × ({st[-1]} − {j})`：这段本来按 `{a[j]}` 算，现在 `s` = {s}',
        's += x * (st[-1] - i)': '下标 `{i}` 到 `{st[-1] - 1}` 都取 `{x}`：`s += {x} × {st[-1] - i}` → =={s}==',
        'suf[i] = s': '记下 `suf[{i}] = {s}`',
        'st.append(i)': '`{i}` 入栈，栈：`{st}`',
        'ans = s': '`ans` 先取整个右侧递减段（峰在下标 0）：`{ans}`',
        'for i, x in enumerate(a)': lambda S, B, r: (f'开始遍历：`i = {S.i}`，`x = {S.x}`' if len(S.st) == 1 else
                                                     ('遍历结束' if S.i == B.i else f'下一个：`i = {S.i}`，`x = {S.x}`')),
        'st = [-1]': '再从左往右，哨兵换成 `-1`',
        'pre -= a[j]': '撤销 `a[{j}] × ({j} − {st[-1]})`，`pre` = {pre}',
        'pre += x': '下标 `{st[-1] + 1}` 到 `{i}` 都取 `{x}`：`pre` → =={pre}==',
        'ans = max': '峰在 `{i}`：`pre + suf[{i + 1}] = {pre} + {suf[i + 1]} = {pre + suf[i + 1]}`，`ans = max({B.ans}, {pre + suf[i + 1]})` = =={ans}==',
        'return ans': '最大高度和 =={ret}==',
    },
    skip=['pre = 0', 'x = a[i]', 'n = len(a)', 'j = st.pop()'],
    cards=dict(
        one_liner='枚举山峰，左右两段各用单调栈 O(1) 摊还求最大和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`maxHeights[i]` 是第 `i` 座塔的高度上限，只能削低', '要排成先不降、后不增的山形，求高度和的最大值',
                 '示例：`[6,5,3,9,2,7]` → `22`，即 `[3,3,3,9,2,2]`'],
        quote='计算从 a[i] 到 a[n-1] 形成山状数组的右侧递减段，元素和最大是多少，记到数组 suf[i] 中。那么答案就是 pre[i]+suf[i+1] 的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['前后缀分解：峰在 `i` 时，答案 = 左段最大和 + 右段最大和',
              '单调栈（严格递增）：遇到更矮的 `x`，把栈里更高的塔「撤销」，统一压成 `x`',
              '栈里只存下标，用 `st[-1] - i` 直接算出被 `x` 覆盖的长度'],
        summary=['时间 `O(n)`（每个下标最多入栈出栈一次），空间 `O(n)`',
                 '易错：`while` 里是 `x <= a[st[-1]]`，相等也要弹出；撤销的长度是 `st[-1] - j`',
                 '哨兵 `n` 和 `-1` 让栈永不为空，所以循环条件是 `len(st) > 1`',
                 '同类题：42 接雨水、2866 美丽塔 II（同一套写法，数据更大）'],
    ),
)
