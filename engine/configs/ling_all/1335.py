A0 = [7, 1, 7, 1, 7]


def _fmt(t):
    return f'a[{t[0]}]={A0[t[0]]} · min={t[1]}'


CONFIG = dict(
    num=1335, title='工作计划的最低难度', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 单调栈优化',
    tags=['灵神题单', '动态规划', '难度分 2035'],
    code='''
class Solution:
    def minDifficulty(self, a: List[int], d: int) -> int:
        n = len(a)
        if n < d:
            return -1

        f = [[inf] * n for _ in range(d)]
        f[0] = list(accumulate(a, max))
        for i in range(1, d):
            st = []  # (下标 j，从 f[i-1][left[j]] 到 f[i-1][j-1] 的最小值)
            for j in range(i, n):
                mn = f[i - 1][j - 1]  # 只有 a[j] 一项工作
                while st and a[st[-1][0]] <= a[j]:  # 向左一直计算到 left[j]
                    mn = min(mn, st.pop()[1])
                f[i][j] = mn + a[j]  # 从 a[left[j]+1] 到 a[j] 的最大值是 a[j]
                if st:  # 如果这一段包含 <=left[j] 的工作，那么这一段的最大值必然不是 a[j]
                    f[i][j] = min(f[i][j], f[i][st[-1][0]])  # 答案和 f[i][left[j]] 是一样的
                st.append((j, mn))  # 注意这里保存的不是 f[i][j]
        return f[-1][-1]
''',
    call=f'Solution().minDifficulty({A0}, 3)',
    expect=15,
    views=[
        dict(type='array', var='a', label='a（工作难度）', h=210, cell=80, pointers={'j': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('j') else ('yellow' if S.get('st') and k == S['st'][-1][0] else None)),
        dict(type='table', var='f', label='f[i][j]：用 i+1 天完成 a[0..j] 的最小难度', h=250, cell=72,
             rows=lambda S: [f'第{k + 1}天' for k in range(len(S['f']))], cols=lambda S: [f'a{k}' for k in range(len(S['a']))],
             cursors=[('i', 'j', 'yellow', '')]),
        dict(type='stack', var='st', label='单调栈 st（栈内 a 单调递减）', h=170, fmt=_fmt),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'blue'), 'mn', ('f[i][j]', 'f[i][j]', 'green')],
    captions={
        'if n < d': '`n = {n}`，`d = {d}`：每天至少一项工作，`n < d` 就排不满 → 返回 -1',
        'f = [[inf]': '`f[i][j]`：用 `i+1` 天完成 `a[0..j]` 的最小难度，先全设成无穷大',
        'f[0] = list': '只有一天：必须做完前 `j+1` 项，难度就是前缀最大值 → `f[0] = {f[0]}`',
        'for i in range': '`i = {i}`：开始算用 `{i+1}` 天的状态，它只依赖 `f[{i-1}]`',
        'st = []': '每一天重新建栈：栈里放 (下标, 最后一段起点候选里的最小 `f`)',
        'mn = f[i - 1][j - 1]': '最后一段只有 `a[{j}]={a[j]}`：前面 `{i}` 天做完 `a[0..{j-1}]`，`mn = {mn}`',
        'while st and': lambda S, B, r: (f'栈顶 `a[{S.st[-1][0]}]={S.a[S.st[-1][0]]} <= a[{S.j}]={S.a[S.j]}`：它不会是最后一段的最大值 → 弹出并合并，`mn` 取更小者'
                                         if S.st and S.a[S.st[-1][0]] <= S.a[S.j] else
                                         ('栈空：`a[j]` 是目前最大，最后一段可以一直延伸到最左' if not S.st else f'栈顶 `a[{S.st[-1][0]}]={S.a[S.st[-1][0]]} > a[{S.j}]={S.a[S.j]}`：停止，它就是 left[j]')),
        'mn = min(mn, st.pop()': '弹出的段并入：`mn = {mn}`（保存的是更长范围内 `f[i-1]` 的最小值）',
        'f[i][j] = mn + a[j]': '最后一段最大值就是 `a[{j}]={a[j]}` → `f[{i}][{j}] = {mn} + {a[j]}` = =={f[i][j]}==',
        'if st:': lambda S, B, r: (f'栈非空：还有更大的 `a[{S.st[-1][0]}]` 在左边，最后一段若延伸到它，最大值就不是 `a[j]`' if S.st else '栈空，没有更大的元素，跳过'),
        'f[i][j] = min(f[i][j], f[i][st': '若最后一段含 `left[j]`，答案同 `f[{i}][{st[-1][0]}] = {f[i][st[-1][0]]}` → `f[{i}][{j}]` = =={f[i][j]}==',
        'st.append': '入栈 `({j}, {mn})`：注意存的是 `mn`，不是 `f[i][j]`',
        'return f[-1][-1]': '答案 `f[d-1][n-1]` = =={ret}==',
    },
    skip=['for j in range'],
    cards=dict(
        one_liner='把数组分成 d 段，每段取最大值，总和最小；单调栈把转移降到均摊 O(1)',
        complexity='时间 `O(dn)`，空间 `O(dn)`',
        problem=['`d` 天做完 `jobDifficulty` 的所有工作，必须按顺序，==每天至少一项==',
                 '一天的难度 = 当天工作的最大难度；求总难度最小，做不到返回 -1',
                 '示例：`[7,1,7,1,7]`，`d = 3` → `15`'],
        quote='这相当于把数组 a 分割成 d 段（每一段都不能为空），我们需要求出每一段的最大值，并把这些最大值相加。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['`f[i][j]` 枚举最后一段起点 `k`，`f[i-1][k-1]` 加上区间最大值，这是 `O(n^2 d)`',
              '方法二：用单调栈找 `a[j]` 左侧最近更大元素 `left[j]`',
              '`left[j]` 右边的段最大值是 `a[j]`；段若包含 `left[j]` 就等价于 `f[i][left[j]]`'],
        summary=['方法一是 `O(dn^2)` 的递推，方法二用单调栈优化到 `O(dn)`，这里演示方法二',
                 '栈里存的是 `(下标, mn)`，不是 `f[i][j]`，别写错',
                 '弹栈条件用 `<=`，相等的元素也要合并',
                 '`j` 从 `i` 开始：前 `i` 天至少要留 `i` 项工作',
                 '同类题：1043. 分隔数组以得到最大和'],
    ),
)
