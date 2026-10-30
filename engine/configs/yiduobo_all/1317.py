CONFIG = dict(
    num=1317, title='将整数转换为两个无零整数的和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='99..9 拆分 · 补 0 位',
    tags=['随机算法', '构造题', '难度分 1278'],
    code='''
class Solution(object):
    def getNoZeroIntegers(self, n):

        tmp = n
        l = 0
        while tmp:
            l += 1
            tmp //= 10
        
        if l == 1:
            return [1, n - 1]
        else:
            x = 10 ** (l - 1) - 1
            y = n - x
            tmp = y
            p = 1
            while tmp:
                if tmp % 10 == 0:
                    y += p
                    x -= p
                p *= 10
                tmp //= 10
            return [x, y]
''',
    call='Solution().getNoZeroIntegers(1100)',
    expect=[989, 111],
    views=[
        dict(type='text', h=100, size=36,
             fn=lambda S: (f"x = ==`{S['x']}`==，y = ==`{S['y']}`==，x + y = `{S['x'] + S['y']}`" if 'y' in S else (f"x = ==`{S['x']}`==（l−1 个 9）" if 'x' in S else (f"n = `{S['n']}`，位数 l = `{S['l']}`" if 'l' in S else '')))),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"正在检查 y 的权重为 `{S['p']}` 的这一位：剩余 `{S['tmp']}` 的个位是 `{S['tmp'] % 10}`" if 'p' in S and 'y' in S else ''),
    ],
    watch=[('l', 'l', 'blue'), ('x', 'x', 'cyan'), ('y', 'y', 'green'), ('p', 'p', 'yellow')],
    captions={
        'tmp = n': '先数 `n` 有几位',
        'l += 1': '位数 `l` = {l}',
        8: lambda S, B, r: f'去掉最低位，剩 `{S.tmp}`' if S.tmp else f'去完了，`n` 一共 `{S.l}` 位',
        22: lambda S, B, r: f'`y` 去掉已检查的最低位，剩 `{S.tmp}`' if S.tmp else '`y` 的每一位都检查完了',
        'if l == 1': lambda S, B, r: ('只有一位：`1` 和 `n-1` 即可' if S.l == 1 else f'`l = {S.l}` 位 > 1，要用 `99..9` 拆分'),
        'x = 10 ** (l - 1) - 1': '`x` 取 `l-1` 个 9：`x = {x}`，它的每一位都非零',
        'y = n - x': '`y = n - x = {y}`：剩下的部分，但 `y` 里可能有 0',
        'tmp = y': '准备从低位到高位检查 `y` 的每一位',
        'p = 1': '`p` 是当前位的权重',
        'if tmp % 10 == 0': lambda S, B, r: (f'`y` 在权重 `{S.p}` 的这一位是 ==0== → 需要修补' if S.tmp % 10 == 0 else f'这一位是 `{S.tmp % 10}`，不是 0，不用动'),
        'y += p': '`y` 这一位 0 → 1：`y = {y}`',
        'x -= p': '`x` 对应位减 1 来补偿，仍然非零（原来是 9 → 8）：`x = {x}`',
        'p *= 10': '看下一位，`p = {p}`',
        'return [x, y]': '`x = {x}`，`y = {y}`，都不含 0，和为 `{x + y}`',
    },
    cards=dict(
        one_liner='先拆成 99..9 加余数，余数里的 0 都换成 1，从 99..9 里扣回去',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['无零整数：十进制里不含数字 `0` 的正整数',
                 '给 `n`，返回 `[a, b]`，两个都是无零整数且 `a + b = n`',
                 '本视频：`n = 1100` → `[989, 111]`'],
        quote='若n的位数大于1，设为l，那么我们可以先将其分解成x = 99...9与y = n - 99...9，这里的x中一共是l - 1个9。接下来，对于y中所有为0的位数，我们将其变为1，同时将x中对应的位数减去1',
        quote_src='—— yiduobo 题解原文',
        idea=['`x` 是 `l-1` 个 9，每位都非零；`y = n - x` 位数不超过 `l`，可能含 0',
              '`y` 某位是 0：这位加 1，同时 `x` 这位减 1，和不变',
              '`x` 这位原来是 9，减 1 变 8，仍非零；`y` 的 0 全部消失'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '一位数特判：`[1, n-1]`',
                 '易错点：`x` 和 `y` 要在同一个权重 `p` 上同时修改，和才不变',
                 '原文为 Python 2 写法，整数除法 `tmp /= 10` 已改为 `tmp //= 10`'],
    ),
)
