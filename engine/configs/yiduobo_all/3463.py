def _brute(s):
    a = [int(x) for x in s]
    while len(a) > 2:
        a = [(a[i] + a[i + 1]) % 10 for i in range(len(a) - 1)]
    return a[0] == a[1]


EXP = _brute("347891")


def _text(S):
    ln = S.get('_line', 0)
    if 'left' not in S:
        return '先把阶乘里的因子 2 和 5 分离出来：余下的数与 10 互质，才有模 10 的逆元'
    if 'right' in S and ln >= 44:
        return f'右边：系数 `C(n-2, index-1)`，累加到 `right = {S["right"]}`（左边算出 `left = {S["left"]}`）'
    return f'左边：系数 `C(n-2, index)`，累加到 `left = {S["left"]}`'


CONFIG = dict(
    num=3463, title='判断操作后字符串中的数字是否相等 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='杨辉三角系数 + 分离因子 2、5',
    tags=['灵神题单', '难度分 2286'],
    code='''
class Solution(object):
    def hasSameDigits(self, s):
        
        p2 = [0]
        p5 = [0]
        num = [1]
        f = [1]

        n = len(s)
        for v in range(1, n - 1):
            p2.append(p2[-1])
            p5.append(p5[-1])
            while v % 2 == 0:
                p2[-1] += 1
                v //= 2
            while v % 5 == 0:
                p5[-1] += 1
                v //= 5
            num.append(v)
            f.append(f[-1] * v % 10)
        
        inv = {1: 1, 3: 7, 7: 3, 9: 9}
        p2_mod = [2, 4, 8, 6]

        left = int(s[0])
        for index in range(1, n - 1):
            c = f[n - 2] * inv[f[index]] * inv[f[n - 2 - index]] % 10
            sp2 = p2[n - 2] - p2[index] - p2[n - 2 - index]
            sp5 = p5[n - 2] - p5[index] - p5[n - 2 - index]
            if sp2 > 0:
                if sp5 > 0:
                    c = 0
                else:
                    c *= p2_mod[(sp2 - 1) % 4]
                    c %= 10
            elif sp5 > 0:
                c *= 5
                c %= 10
            
            left += int(s[index]) * c
            left %= 10
        
        right = int(s[-1])
        for index in range(1, n - 1):
            c = f[n - 2] * inv[f[index - 1]] * inv[f[n - 1 - index]] % 10
            sp2 = p2[n - 2] - p2[index - 1] - p2[n - 1 - index]
            sp5 = p5[n - 2] - p5[index - 1] - p5[n - 1 - index]
            if sp2 > 0:
                if sp5 > 0:
                    c = 0
                else:
                    c *= p2_mod[(sp2 - 1) % 4]
                    c %= 10
            elif sp5 > 0:
                c *= 5
                c %= 10
            
            right += int(s[index]) * c
            right %= 10
        
        return left == right
''',
    call='Solution().hasSameDigits("347891")',
    expect=EXP,
    views=[
        dict(type='text', fn=_text, size=26),
        dict(type='string', var='s', pointers={'index': 'blue'}, h=250, cell=90, label='s'),
        dict(type='array', var=lambda S: S.get('f', []), label='f[x]：x! 去掉因子 2、5 后模 10', h=150, cell=80),
        dict(type='array', var=lambda S: S.get('p2', []), label='p2[x]：x! 中因子 2 的个数', h=150, cell=80),
        dict(type='array', var=lambda S: S.get('p5', []), label='p5[x]：x! 中因子 5 的个数', h=150, cell=80),
    ],
    watch=[('v', 'v', 'purple'), ('index', 'index', 'blue'), ('c', 'c', 'yellow'), ('sp2', 'sp2', 'orange'), ('sp5', 'sp5', 'pink'),
           ('left', 'left', 'green'), ('right', 'right', 'cyan')],
    skip=['p2.append(p2[-1])', 'p5.append(p5[-1])', 'num.append', 'left %= 10', 'right %= 10', 'p2 = [0]', 'p5 = [0]', 'num = [1]', 'f = [1]', 'p2_mod = ', 'sp5 = p5[', 'int(s[0])', 'int(s[-1])', 'c %= 10', 'for v in range', 46, 48, 49, 54],
    captions={
        'n = len(s)': '`n = {n}`：每轮少一个数，共 `n - 2 = {n - 2}` 轮后剩两个；每一项的系数是 `C(n-2, k)`',
        'while v % 2': lambda S, B, ret: (f'`v = {S["v"]}` 还能被 2 整除 → 拿出一个因子 2' if S['v'] % 2 == 0 else f'`v = {S["v"]}`：因子 2 拿完了'),
        'while v % 5': lambda S, B, ret: (f'`{S["v"]}` 还能被 5 整除 → 拿出一个因子 5' if S['v'] % 5 == 0 else '`v` 里已经没有因子 5 了'),
        'p2[-1] += 1': '`v!` 里的 2 的个数加 1：`p2[{v0}] = {p2[-1]}`'.replace('{v0}', '-1'),
        'f.append': '`f` 只乘去掉 2、5 后的 `v`，所以只会出现 1、3、7、9',
        'inv = ': '去掉 2、5 的数模 10 只可能是 1、3、7、9，手算逆元：==1→1，3→7，7→3，9→9==',
        'for index in range': lambda S, B, ret: ('这一遍的 `index` 都走完了' if 'index' in B and B.index == S['index'] else f'`index = {S["index"]}`：这一项的系数是组合数'),
        'c = f[n - 2]': '分子乘 `f[n-2]`、分母乘逆元：去掉 2、5 后的部分 `c = {c}`',
        'sp2 = p2': '分子里 2 的个数 − 分母里 2 的个数 = `sp2 = {sp2}`',
        'if sp2 > 0': '`sp2 = {sp2}`：{"还剩因子 2" if sp2 > 0 else "没有多余的因子 2"}',
        'if sp5 > 0': '`sp5 = {sp5}`：{"还剩因子 5" if sp5 > 0 else "没有多余的因子 5"}',
        'c *= p2_mod': lambda S, B, ret: ('右边同样判断出 `sp2 = %d`：' % S['sp2'] if S['_line'] > 44 else '') + '2 的幂模 10 按 2,4,8,6 循环：`p2_mod[(sp2-1) %% 4]` 乘回去 → `c = %d`' % S['c'],
        'c = 0': '同时有因子 2 和 5 → 一定是 10 的倍数 → `c = 0`',
        'c *= 5': '5 的任意次幂模 10 都是 5 → `c = {c}`',
        'left += ': '`left += s[{index}] * {c}` → `{left}`（再模 10）',
        'right += ': '`right += s[{index}] * {c}` → `{right}`（再模 10）',
        'return left == right': '`left = {left}`，`right = {right}`：{"相等" if left == right else "不相等"} → 返回 `{left == right}`',
    },
    cards=dict(
        one_liner='系数是杨辉三角；模 10 拆开 2 和 5',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数字串 `s` 每轮把相邻两数之和模 10，直到剩两位',
                 '两位相同返回 `true`，否则 `false`；`s` 最长 `10^5`，不能暴力',
                 '示例：`"3902"` → `true`；`"34789"` → `false`'],
        quote='观察最左侧这一列可以发现，每次迭代被累加到这一列中的元素的系数恰好是按照[1]、[1, 1]、[1, 2, 1]、[1, 3, 3, 1]……这样排布的。',
        quote_src='—— yiduobo 题解',
        idea=['不模 10 先写出每一轮：第 k 项在 `s[0]` 位置的系数是 `C(n-2, k)`',
              '最左 `left` 和最右 `right` 各算一遍，最后比较是否相等',
              '10 不是质数：把阶乘里的 2、5 分离，余下的数只会是 1、3、7、9，逆元手算',
              '再按 `sp2`、`sp5` 把 2、5 的影响乘回来'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`left` 的系数是 `C(n-2, index)`，`right` 是 `C(n-2, index-1)`，别写混',
                 '`sp2 > 0` 且 `sp5 > 0` 时直接为 0；只有 2 时查 `p2_mod`，只有 5 时乘 5',
                 '原文已是 Python 3 兼容写法，代码未改动；同类题：2221'],
    ),
    max_steps=110,
)
