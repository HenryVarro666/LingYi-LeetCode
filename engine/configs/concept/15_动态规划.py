def _tab(S):
    return S['memo'] if 'memo' in S else S.get('f')


def _color(S, k, v):
    if 'memo' in S:
        if k <= 1:
            return 'cyan'                     # 递归边界，不用存
        return 'green' if v else None         # 已经算过、存进 memo
    if 'f' in S:
        return 'green' if v else None
    return None


def _formula(S):
    if 'memo' in S and 'i' in S:
        i = S['i']
        if i <= 1:
            return f'`dfs({i}) = 1`：递归边界'
        return f'`dfs({i}) = dfs({i - 1}) + dfs({i - 2})`：最后一步爬 1 级，或者爬 2 级'
    if 'f' in S and 'i' in S:
        i = S['i']
        return f"`f[{i}] = f[{i - 1}] + f[{i - 2}]`　←　翻译自 `dfs({i}) = dfs({i - 1}) + dfs({i - 2})`"
    if 'f' in S:
        return '递推：去掉「递」，只保留「归」，==从小到大== 算'
    return '记忆化搜索：==递归 + 记录返回值==，每个状态只算一次'


CONFIG = dict(
    num=None, title='动态规划 · 通用思想与模板', author='概念讲解', category='动态规划',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def climb_memo(n):                   # 写法一：记忆化搜索（自顶向下）
    memo = [0] * (n + 1)             # 0 表示还没算过
    def dfs(i):                      # dfs(i)：爬到第 i 级的方法数
        if i <= 1:                   # 递归边界
            return 1
        if memo[i]:                  # 之前算过，直接返回
            return memo[i]
        memo[i] = dfs(i - 1) + dfs(i - 2)
        return memo[i]
    return dfs(n)

def climb_dp(n):                     # 写法二：1:1 翻译成递推（自底向上）
    f = [0] * (n + 1)                # f[i] 和 dfs(i) 含义相同
    f[0] = f[1] = 1                  # 翻译自递归边界
    for i in range(2, n + 1):
        f[i] = f[i - 1] + f[i - 2]   # 翻译自 dfs 的式子
    return f[n]                      # 翻译自递归入口 dfs(n)
''',
    call='''
a = climb_memo(5)
b = climb_dp(5)
(a, b)
''',
    expect=(8, 8),
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var=_tab, label='memo / f（下标 = 台阶数；青 = 边界，绿 = 已算出）', pointers={'i': 'pink'},
             color=_color, h=190),
        dict(type='calls', label='递归调用栈（只有写法一才有）', h=280),
    ],
    watch=[('i', 'i', 'pink'), ('n', 'n')],
    captions={
        'memo = [0] * (n + 1)': '写法一：`memo[i]` 记录 `dfs(i)` 的结果；方案数都是正数，所以 ==0 可以表示「还没算」==',
        'if i <= 1': lambda S, B, ret: (f'`i = {S.i}` 是递归边界' if S.i <= 1 else f'`i = {S.i}` 不是边界'),
        'return 1': '`dfs({i}) = 1`：从 0 爬到 0 或 1 都只有一种方法',
        'if memo[i]': lambda S, B, ret: (f'`memo[{S.i}] = {S.memo[S.i]}` 已经算过 → ==直接返回，不再递归==' if S.memo[S.i]
                                         else f'`memo[{S.i}]` 还没算 → 拆成子问题'),
        7: '返回记忆的结果 `dfs({i}) = {ret}`：省掉了一整棵递归子树',
        'memo[i] = dfs(i - 1)': lambda S, B, ret: (f'`dfs({B.i}) = dfs({B.i - 1}) + dfs({B.i - 2})`：先递归算 `dfs({B.i - 1})`'),
        9: '`dfs({i})` 算完：`memo[{i}] = {ret}`，记下来，以后直接用',
        'return dfs(n)': '递归入口：答案是 `dfs({n})`',
        'f = [0] * (n + 1)': '写法二：去掉「递」，只保留「归」——数组 `f` 代替 `memo`',
        'f[0] = f[1] = 1': '初始值翻译自递归边界：`f[0] = f[1] = 1`',
        'for i in range(2': lambda S, B, ret: (f'从小到大算 `f[{S.i}]`' if B.get('i') != S.i else 'f 全部算完'),
        'f[i] = f[i - 1]': '`f[{i}] = f[{i - 1}] + f[{i - 2}] = {f[i - 1]} + {f[i - 2]} = {f[i]}`',
        'return f[n]': '答案 `f[{n}] = {ret}`：和记忆化搜索一样，但 ==没有递归开销==',
    },
    cards=dict(
        one_liner='找到「最后一步」的子问题，记忆化避免重复，再 1:1 翻译成递推',
        complexity='状态个数 × 单个状态的转移时间，爬楼梯 `O(n)`',
        problem_heading='什么时候用？',
        problem=['求方案数、最大 / 最小值、能否做到，且 ==子问题会重复==',
                 '最后一步有几种可能 → 「选或不选」或「枚举选哪个」',
                 '暴力递归是指数级，但不同的参数只有 `O(n)` / `O(nm)` 种',
                 '选一些数凑出目标和 → 背包（279、322、416）'],
        before=[dict(heading='核心概念：从记忆化搜索到递推', lines=[
            '三步：定义 `dfs(i)` → 按最后一步拆成子问题 → 写递归边界',
            '递归 + 记录返回值 = 记忆化搜索：每个状态只算一次',
            '1:1 翻译：`dfs(i)` → `f[i]`，边界 → 初始值，入口 → 答案',
            '时间复杂度 = 状态个数 × 单个状态的计算时间']),
        ],
        idea_heading='两位作者怎么说',
        quote='我们可以去掉递归中的「递」，只保留「归」的部分，即自底向上计算……相当于之前是用递归去计算每个状态，==现在是枚举并计算每个状态==。',
        quote_src='—— 灵茶山艾府 · 70. 爬楼梯',
        idea=['灵神：先写递归找子问题 → 记忆化 → ==1:1 翻译成递推== → 空间优化',
              'yiduobo 直接定义状态：「==设 f[i] 表示 s 的前 i 位怎么怎么样==」（139）',
              '198 / 300 两人都对 ==最后一步== 分类讨论：偷不偷第 i 家、接在谁后面'],
        after=[dict(heading='本类 Hot100 题目 & 学习顺序（1/2）', chapter='④ 小结', lines=[
            '`70` 爬楼梯：`f[i] = f[i-1] + f[i-2]`',
            '`118` 杨辉三角：每个数 = 左上 + 右上',
            '`198` 打家劫舍：选或不选，`max(f[i-1], f[i-2] + x)`',
            '`279` 完全平方数：完全背包，求最少个数',
            '`322` 零钱兑换：完全背包，恰好凑满'])],
        summary_heading='本类 Hot100 题目 & 学习顺序（2/2）',
        summary=['`139` 单词拆分：枚举最后一个单词的起点',
                 '`300` 最长递增子序列：枚举选哪个 / 贪心 + 二分',
                 '`152` 乘积最大子数组：同时维护最大和最小',
                 '`416` 分割等和子集：0-1 背包，倒序枚举容量',
                 '`32` 最长有效括号：栈 / 左右各扫一遍计数',
                 '易错：memo 初值别和合法结果冲突；0-1 背包滚动要倒序'],
    ),
)
