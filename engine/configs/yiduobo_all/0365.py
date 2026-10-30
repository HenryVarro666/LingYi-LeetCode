def _t(S):
    x, y, z = S['x'], S['y'], S['z']
    if 'tmp' in S:
        return f"辗转相除求 gcd：`x = {x}`，`y = {y}`，`tmp = x % y`" + (f"，y 为 0 → ==gcd = {x}==" if y == 0 else '')
    return f"两个水壶 `x`、`y`，目标 `z = {z}`：能量出的水量都形如 `a·x + b·y`"


def _g(S):
    x, y, z = S['x'], S['y'], S['z']
    return f"总容量 `{x} + {y} = {x + y}`，目标 `z = {z}`"


CONFIG = dict(
    num=365, title='水壶问题', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='裴蜀定理 · gcd 整除判断',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def canMeasureWater(self, x, y, z):

        if x + y < z:
            return False

        if z == 0:
            return True

        if x == 0:
            if y == z:
                return True
            else:
                return False
        if y == 0:
            if x == z:
                return True
            else:
                return False
        
        if x < y:
            x, y = y, x
        while y != 0:
            tmp = x % y
            x = y
            y = tmp
        return z % x == 0
''',
    call='Solution().canMeasureWater(3, 5, 4)',
    expect=True,
    views=[
        dict(type='text', fn=_g, h=100, size=34),
        dict(type='text', fn=_t, h=140, size=34),
        dict(type='text', fn=lambda S: '`a·x + b·y` 能凑出 `z` ⇔ `z` 是 `gcd(x, y)` 的倍数（x、y 都不为 0 时）', h=100),
    ],
    watch=['x', 'y', 'z', 'tmp'],
    captions={
        'x + y < z': lambda S, B, r: (f'总容量 `{S.x} + {S.y} = {S.x + S.y}` 小于 `z = {S.z}`：两个壶加起来都装不下 → False' if S.x + S.y < S.z
                                      else f'总容量 `{S.x + S.y}` ≥ `z = {S.z}`，不能直接否定，继续'),
        'if z == 0': lambda S, B, r: '`z = 0`：什么都不倒就是 0 → True' if S.z == 0 else '`z = {}` 不为 0，继续'.format(S.z),
        'if x == 0': lambda S, B, r: ('`x = 0`：只剩 y 壶，只能量出 0 或 y，所以要求 `y == z`' if S.x == 0 else '`x ≠ 0`，继续'),
        'if y == 0': lambda S, B, r: ('`y = 0`：只剩 x 壶，只能量出 0 或 x，所以要求 `x == z`' if S.y == 0 else '`y ≠ 0`：两个壶都能用，进入一般情形'),
        'if x < y': lambda S, B, r: f'`x = {S.x}`，`y = {S.y}`：保证 x 是大的一个，方便辗转相除（交换不影响 gcd）',
        'x, y = y, x': '交换后 `x = {x}`，`y = {y}`',
        'while y != 0': '`y = {y}`：不为 0 就继续辗转相除',
        'tmp = x % y': '`tmp = {x} % {y} = {tmp}`',
        'x = y': '`x` 变成原来的 `y`：`x = {x}`',
        'y = tmp': '`y = {y}`：即 `gcd(x, y) = gcd(y, x % y)`',
        'return z % x == 0': '`y = 0`，`gcd = {x}`；`z % gcd = {z} % {x} = {z % x}` → ==z 是 gcd 的倍数 {z % x == 0}==',
    },
    cards=dict(
        one_liner='能量出的水量恰是 gcd(x, y) 的倍数，且不超过总容量',
        complexity='时间 `O(log min(x, y))`，空间 `O(1)`',
        problem=['有容量为 `x`、`y` 升的两个水壶，水无限多，可以灌满、倒空、互相倒',
                 '问能否恰好量出 `z` 升水（可分布在两个壶里的总和）',
                 '示例：`x = 3`，`y = 5`，`z = 4` → `True`'],
        quote='此时必然是形如ax + by的形式。不妨设x和y的最大公约数为k……若z不为k的倍数，那么必然是False。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理边界：`x + y < z`、`z = 0`、有一个壶容量为 0',
              '一般情形：能量出的水量 `a·x + b·y = k(a·p + b·q)`，其中 `k = gcd(x, y)`',
              '`p`、`q` 互质，由扩展欧几里得总能凑出 1 → 只要 `z` 是 `k` 的倍数就行'],
        summary=['时间 `O(log min(x, y))`，空间 `O(1)`',
                 '易错：`z > x + y` 必须先判掉，否则 gcd 整除也不可能',
                 '易错：容量为 0 的壶会让取模出错，要单独处理',
                 '原文已是可直接运行的写法，没有改动'],
    ),
)
