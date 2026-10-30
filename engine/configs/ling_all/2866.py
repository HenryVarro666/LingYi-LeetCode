def _fmt_st(S):
    a, n = S['a'], len(S['a'])
    return lambda j: '哨兵' if (j == n or j == -1) else f'{j}:{a[j]}'


CONFIG = dict(
    num=2866, title='美丽塔 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 + 单调栈优化',
    tags=['灵神题单·单调栈', '灵神题单·动态规划', '难度分 2072'],
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
    call='Solution().maximumSumOfHeights([5,3,4,1,1])',
    expect=13,
    views=[
        dict(type='bars', var='a', pointers={'i': 'blue'}, h=250, label='maxHeights',
             color=lambda S, i, v: 'blue' if i == S.get('i', -99) else None),
        dict(type='stack', var='st', h=120, fmt=lambda j: '哨兵' if (j < 0 or j >= 5) else f'下标{j}'),
        dict(type='array', var='suf', h=150, label='suf[i]：a[i..n-1] 形成递减段的最大和',
             color=lambda S, i, v: 'green' if i == S.get('i', -99) and S.get('_line', 0) <= 14 else None),
        dict(type='text', fn=lambda S: (f"右→左：`suf[{S['i']}]` 的和 `s = {S['s']}`" if S.get('_line', 0) <= 14 and 'i' in S
                                         else (f"左→右：`pre = {S['pre']}`，`pre + suf[i+1]` = {S['pre'] + S['suf'][S['i'] + 1]}" if 'pre' in S and 'i' in S else ''))),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'cyan'), ('s', 's', 'yellow'), ('pre', 'pre', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'suf = [0]': '`suf[i]`：以 `a[i]` 开头的递减段，元素和最大是多少（`suf[n] = 0`）',
        'st = [n]': '单调栈存下标，栈中元素值从底到顶 ==严格递增==；`n` 是哨兵',
        7: lambda S, B, r: (f'从右往左，处理 `i = {S.i}`' if S.i != B.get('i') else '右边算完了'),
        9: lambda S, B, r: (
            f'`x = {S.x}` <= 栈顶高度 `{S.a[S.st[-1]]}`：栈顶那座塔不能比 x 高，要压到 x → 撤销它之前加的' if len(S.st) > 1 and S.x <= S.a[S.st[-1]]
            else ('栈里只剩哨兵：右边没有更矮的塔了，停止撤销' if len(S.st) == 1 else f'`x = {S.x}` > 栈顶高度 `{S.a[S.st[-1]]}`：右边的塔不用压低，停止撤销')),
        10: '弹出下标 `{j}`，它管着 `[{j}, {st[-1]})` 这一段，高度原来是 `{a[j]}`',
        11: '撤销：`s -= {a[j]} × ({st[-1]} − {j})` → `s = {s}`',
        12: '`{i}` 到 `{st[-1] - 1}` 共 `{st[-1] - i}` 座塔都取 `{x}`：`s += {x} × {st[-1] - i}` → `s = {s}`',
        13: '`suf[{i}] = {s}`',
        16: '`suf[0] = {s}`：山峰在最左边时的答案，作为初始 `ans`',
        17: '再从左往右算 `pre`，哨兵换成 `-1`',
        19: lambda S, B, r: (f'从左往右，处理 `i = {S.i}`，`x = {S.x}`' if not (B.get('i') == S.i == len(S.a) - 1) else '左边也算完了'),
        20: lambda S, B, r: (
            f'`x = {S.x}` <= 栈顶高度 `{S.a[S.st[-1]]}`：左边那座塔不能比 x 高，要压到 x → 撤销它之前加的' if len(S.st) > 1 and S.x <= S.a[S.st[-1]]
            else ('栈里只剩哨兵：左边没有更矮的塔了，停止撤销' if len(S.st) == 1 else f'`x = {S.x}` > 栈顶高度 `{S.a[S.st[-1]]}`：左边的塔不用压低，停止撤销')),
        21: '弹出下标 `{j}`，它管着 `({st[-1]}, {j}]` 这一段，高度原来是 `{a[j]}`',
        22: '撤销：`pre -= {a[j]} × ({j} − {st[-1]})` → `pre = {pre}`',
        23: '`{st[-1] + 1}` 到 `{i}` 共 `{i - st[-1]}` 座塔都取 `{x}`：`pre += {x} × {i - st[-1]}` → `pre = {pre}`',
        24: '山峰在 `i = {i}`：左边 `pre = {pre}` + 右边 `suf[{i + 1}] = {suf[i + 1]}` = {pre + suf[i + 1]} → `ans = {ans}`',
        26: '最大高度和 `{ans}`',
    },
    skip=['x = a[i]', 'st.append(i)', 'n = len(a)'],
    max_steps=110,
    cards=dict(
        one_liner='左右各用一个单调栈，高度被压低的那段一次性撤销再重算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一个 `maxHeights`，造山脉形状的塔，第 `i` 座高度在 `1..maxHeights[i]`',
                 '山脉：先不降再不增；求高度和的最大值',
                 '示例：`[5,3,4,1,1]` → `13`，方案 `[5,3,3,1,1]`'],
        quote='用单调栈，元素值从栈底到栈顶严格递增。以 suf 为例，我们从右往左遍历 a，设当前得到的元素和为 sum。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pre[i]`、`suf[i]` 分别是左侧递增段、右侧递减段的最大和',
              '`a[i]` 比栈顶大：直接加；否则把栈里比它高的段==撤销==，整段改成 `a[i]`',
              '答案 = `pre[i] + suf[i+1]` 的最大值，枚举山峰位置'],
        summary=['时间 `O(n)`：每个下标最多入栈出栈各一次',
                 '`s` 里存的是当前这一侧的总和；弹栈时要先==撤销==旧高度，再按 `x` 补上整段',
                 '哨兵：右侧是 `n`，左侧是 `-1`，用 `len(st) > 1` 判断栈是否只剩哨兵',
                 '比较用 `<=`：相等高度合并，与题解的严格递增栈一致'],
    ),
)
