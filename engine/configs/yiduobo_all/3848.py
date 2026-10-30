CONFIG = dict(
    num=3848, title='阶数数字排列', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='数位阶乘和 · 排序比较',
    code='''
class Solution(object):
    def isDigitorialPermutation(self, n):
        
        fact = [1]
        for v in range(1, 10):
            fact.append(fact[-1] * v)
        
        d = []
        s = 0
        while n:
            d.append(n % 10)
            s += fact[d[-1]]
            n //= 10
        
        ds = []
        while s:
            ds.append(s % 10)
            s //= 10
        
        return sorted(d) == sorted(ds)
''',
    call='Solution().isDigitorialPermutation(541)',
    expect=True,
    views=[
        dict(type='array', var='fact', label='fact[v] = v!', h=170, cell=70),
        dict(type='array', var='d', label='d：n 的各个数位', h=170, cell=70),
        dict(type='array', var='ds', label='ds：s 的各个数位', h=170, cell=70),
        dict(type='text', fn=lambda S: f"阶乘之和 `s` = =={S['s']}==" if 's' in S and 'ds' not in S else '', size=34),
    ],
    watch=['n', 's', 'd', 'ds'],
    captions={
        'fact = [1]': '`fact[v]` 存 `v!`，先放 `0! = 1`',
        'fact.append': '`fact[{v}] = {fact[-1]}`',
        'd.append(n % 10)': '分离出最低位 `{d[-1]}`，放进 `d`',
        's += fact[d[-1]]': '加上 `{d[-1]}! = {fact[d[-1]]}` → `s` = =={s}==',
        'n //= 10': '`n` 去掉最低位 → {n}',
        'ds.append(s % 10)': '把 `s` 也分离数位：最低位 `{ds[-1]}`',
        's //= 10': '`s` 去掉最低位 → {s}',
        'return sorted': lambda S, B, r: (f'`sorted(d) = {sorted(S.d)}` 与 `sorted(ds) = {sorted(S.ds)}` ==相同== → 能重排，返回 True' if r
                                         else f'`sorted(d) = {sorted(S.d)}` ≠ `sorted(ds) = {sorted(S.ds)}` → 返回 False'),
    },
    cards=dict(
        one_liner='n 的数位不变，阶乘和就不变：比较 n 与 s 的数位多重集',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['若一个数的各位数字阶乘之和等于它本身，称为阶数数字',
                 '问 `n` 重新排列后能否得到阶数数字',
                 '本视频：`n = 541` → `true`'],
        quote='无论n如何排列，其中的数位不会产生变化，因此这些数的阶乘之和也不会变化。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `n` 的数位分离出来，边分离边累加阶乘得到 `s`',
              '反过来想：能把 `n` 排成 `s`，就能把 `s` 排回 `n`',
              '再把 `s` 的数位分离出来，两个数位列表排序后比较'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '原文代码在 Python 3 下可直接运行，未作改动',
                 '对比灵神：灵神用一个 `cnt` 数组加减抵消；这里是排序后比较'],
    ),
)
