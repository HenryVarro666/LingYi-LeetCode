def _maxr(S):
    return S.get('max_r')


CONFIG = dict(
    num=2584, title='分割数组使乘积互质', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='质因子区间 · 类似跳跃游戏',
    tags=['贪心与思维', '难度分 2159'],
    code='''
class Solution:
    def findValidSplit(self, nums: List[int]) -> int:
        left = {}  # left[p] 表示质数 p 首次出现的下标
        right = [0] * len(nums)  # right[i] 表示左端点为 i 的区间的右端点的最大值

        def f(p: int, i: int) -> None:
            if p in left:
                right[left[p]] = i  # 记录左端点 l 对应的右端点的最大值
            else:
                left[p] = i  # 第一次遇到质数 p

        for i, x in enumerate(nums):
            d = 2
            while d * d <= x:  # 分解质因数
                if x % d == 0:
                    f(d, i)
                    x //= d
                    while x % d == 0:
                        x //= d
                d += 1
            if x > 1: f(x, i)

        max_r = 0
        for l, r in enumerate(right):
            if l > max_r:  # 最远可以遇到 max_r
                return max_r  # 也可以写 l-1
            max_r = max(max_r, r)
        return -1
''',
    call='Solution().findValidSplit([4, 7, 8, 15, 3, 5])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在分解的 i）', pointers={'i': 'blue'}, cell=100, h=190,
             color=lambda S, i, v: ('green' if 'max_r' in S and S.get('l') is not None and i <= S['max_r'] else None)),
        dict(type='map', var='left', label='left：质数 → 首次出现的下标', fmt=lambda k, v: f'{k}: {v}', h=130, font=30),
        dict(type='array', var='right', label='right[l]：以 l 为左端点的区间，右端点最大值（粉 = l）', pointers={'l': 'pink'}, cell=100, h=190,
             color=lambda S, i, v: ('yellow' if 'max_r' in S and S.get('l') is not None and i == S['max_r'] else None)),
        dict(type='text', h=80, size=30, fn=lambda S: (f"目前最远可达 `max_r = {S['max_r']}`" if 'max_r' in S else '')),
    ],
    watch=['i', 'x', 'd', ('l', 'l', 'pink'), ('max_r', 'max_r', 'green')],
    captions={
        'left = {}': '`left[p]`：质数 `p` ==第一次==出现的下标',
        'right = [0]': '`right[i]`：左端点为 `i` 的区间，右端点最大值。==质因子 p 的区间 [首次, 末次]== 内不能切',
        'while d * d <= x': lambda S, B, r: (f'`d = {S.d}`：`d*d = {S.d*S.d} ≤ x = {S.x}` → 继续试除' if S.d * S.d <= S.x
                                            else f'`d*d = {S.d*S.d} > x = {S.x}`：试除结束'),
        'if x % d == 0': lambda S, B, r: (f'`{S.x} % {S.d} == 0`：`{S.d}` 是质因子' if S.x % S.d == 0
                                         else f'`{S.x} % {S.d} != 0`：不是因子'),
        'f(d, i)': '质因子 `{d}` 出现在下标 `{i}`：交给 `f` 记录',
        'x //= d': '把质因子 `{d}` 除干净：`x` → {x}',
        'd += 1': '`d` → {d}',
        'if x > 1': lambda S, B, r: (f'剩下 `x = {S.x} > 1`，它本身是一个大质因子 → 记录' if S.x > 1 else '`x = 1`：分解完毕'),
        'if p in left': lambda S, B, r: (f'质数 `{S.p}` 之前出现过（首次在下标 `{S.left[S.p]}`）' if S.p in S.left
                                       else f'质数 `{S.p}` 是第一次出现'),
        'right[left[p]] = i': '更新区间：`right[{left[p]}] = {i}`，从 `{left[p]}` 到 `{i}` 都被 `{p}` 连起来，不能切',
        'left[p] = i': '第一次遇到 `{p}`：`left[{p}] = {i}`',
        'max_r = 0': '`max_r`：从 0 出发，被区间连通后最远能到的右端点',
        'if l > max_r': lambda S, B, r: (f'`l = {S.l} > max_r = {S.max_r}`：左端点超过了最远右端点，前面的区间都封口 → ==可以在这里切==' if S.l > S.max_r
                                        else f'`l = {S.l} ≤ max_r = {S.max_r}`：还在某个区间内，不能切'),
        'return max_r': '答案 =={max_r}==：下标 `{max_r}` 之前所有质因子都不会再出现',
        'max_r = max': '`max_r = max({B.max_r}, {r}) = {max_r}`：区间向右延伸',
        'return -1': '一直连通到末尾，==不存在有效分割==',
    },
    cards=dict(
        one_liner='每个质因子画一个区间，答案就是第一个不被盖住的缝',
        complexity='时间 `O(n√U)`，空间 `O(n + U/log U)`',
        problem=['在下标 `i` 切开，前缀乘积与后缀乘积要==互质==',
                 '返回最小的有效切点 `i`，没有就返回 `-1`',
                 '示例：`[4,7,8,15,3,5]` → `2`；`[4,7,15,8,3,5]` → `-1`'],
        quote='对于一个质因子 p，设它在数组中的最左和最右的位置为 left 和 right。那么答案是不能在区间 [left, right) 中的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['互质 = 没有公共质因子 → 同一质因子的==首尾位置不能被切开==',
              '分解每个数，记录质因子首次出现的位置和最远的右端点',
              '像 55 题「跳跃游戏」：从 0 出发，看最远能被区间连到哪'],
        summary=['时间 `O(n√U)`，空间 `O(n + U/log U)`',
                 '区间 `[left, right)` 内不能切，右端点本身可以是答案',
                 '分解时每个质因子只记录一次（把 `d` 除干净）；循环后 `x > 1` 是剩下的大质因子',
                 '同类：55 跳跃游戏、45 跳跃游戏 II、56 合并区间'],
    ),
    skip=['d = 2'],
    max_steps=120,
)
