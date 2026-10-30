def _fmt(S, B):
    a, b = B.get('a'), B.get('b')
    if a is None or b is None:
        return '`dfs(a, b)` = 汤 A 剩 a、汤 B 剩 b 时，目标事件的概率'
    return f'当前状态 `dfs({a}, {b})`：A 剩 {a} 毫升，B 剩 {b} 毫升'


CONFIG = dict(
    num=808, title='分汤', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索 + n 过大直接返回 1',
    tags=['概率 DP、期望 DP', '难度分 2397'],
    code='''
class Solution:
    def soupServings(self, n: int) -> float:
        if n >= 4451:
            return 1

        @cache  # 缓存装饰器，避免重复计算 dfs（一行代码实现记忆化）
        def dfs(a: int, b: int) -> float:
            if a <= 0 and b <= 0:
                return 0.5
            if a <= 0:  # 此时 b > 0
                return 1.0
            if b <= 0:  # 此时 a > 0
                return 0.0
            return (dfs(a - 100, b) + dfs(a - 75, b - 25) + dfs(a - 50, b - 50) + dfs(a - 25, b - 75)) / 4

        return dfs(n, n)
''',
    call='Solution().soupServings(100)',
    expect=0.71875,
    max_steps=90,
    views=[
        dict(type='text', fn=_fmt, size=26, h=60),
        dict(type='calls', h=520),
    ],
    watch=[('n', 'n', 'blue'), ('a', 'a', 'blue'), ('b', 'b', 'pink')],
    captions={
        'if n >= 4451': '`n = {n}`：n 很大时 A 先取完的概率 ≥ 1 − 1e-5，==直接返回 1==；这里 n 小，继续',
        'return dfs(n, n)': '从 `dfs({n}, {n})` 开始递归；算过的状态被 `@cache` 记住，再遇到直接复用（所以下面有些分支不再展开）',
        'return 0.5': '`dfs({a}, {b})`：两种汤同一回合取完 → 按题意只算一半 ==0.5==',
        'return 1.0': '`dfs({a}, {b})`：A 先取完、B 还有剩 → 目标事件必然发生，==概率 1==',
        'return 0.0': '`dfs({a}, {b})`：B 先取完、A 还有剩 → 目标事件不会发生，==概率 0==',
        'return (dfs': '`dfs({B.a}, {B.b})` 等概率选四种操作：先递归算 `dfs(a-100,b)`、`dfs(a-75,b-25)`、`dfs(a-50,b-50)`、`dfs(a-25,b-75)`，再取平均',
    },
    cards=dict(
        one_liner='n 大于 4450 答案当作 1；小的 n 用记忆化搜索求平均',
        complexity='时间 `O((min(n,4450)/25)^2)`，空间同阶',
        problem=['汤 A、B 各 `n` 毫升，每轮等概率选一种操作：(A,B) 取 (100,0)、(75,25)、(50,50)、(25,75)',
                 '任一汤取完即停；求 ==A 先取完的概率 + 同时取完概率的一半==',
                 '示例：`n = 100` → `0.71875`'],
        quote='每回合 A 比 B 期望减少 25 毫升。n 越大，A 先取完的概率越大。编程计算发现，当 n≥4451 时，正确答案 ≥ 1−10^-5，此时可以直接返回 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子问题：`dfs(a, b)` = 两种汤剩 a、b 毫升时目标事件的概率',
              '四种操作互斥且等概率 → 取四个后续状态的==平均值==',
              '边界：都空 0.5；A 空 B 不空 1；A 不空 B 空 0',
              '`@cache` 去掉重复状态，如 `dfs(a-100, b-100)` 会被多条路径到达'],
        summary=['时间 `O((min(n,U)/L)^2)`，`U=4450`，`L=25`',
                 '易错：边界先判 `a、b 都 ≤ 0`，再判单个；同时取完只算 0.5',
                 '`n ≥ 4451` 直接返回 1 才能应对 `n` 到 `10^9`',
                 '灵神还提到可把毫升除以 25 按「份」做，Python 直接 `@cache` 即可'],
    ),
)
