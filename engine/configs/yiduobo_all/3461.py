CONFIG = dict(
    num=3461, title='判断操作后字符串中的数字是否相等 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='杨辉三角系数 · 因子 2、5 分离求组合数模 10', tags=[],
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
    call='Solution().hasSameDigits("34789")',
    expect=False,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前 index）', cell=90, h=150, pointers={'index': 'blue'}),
        dict(type='array', var='f', label='f[x] = x! 去掉因子 2、5 后模 10', cell=80, h=130),
        dict(type='text', h=110, size=28, fn=lambda S: (
            f"left = ==`{S['left']}`==" + (f"，right = ==`{S['right']}`==" if 'right' in S else '') if 'left' in S else
            (f"阶乘表：p2 = `{S['p2']}`，p5 = `{S['p5']}`" if 'p2' in S else ''))),
    ],
    watch=['v', 'index', 'c', 'left', 'right'],
    captions={
        'p2 = [0]': '`p2[x]`：`x!` 里因子 2 的个数',
        'p5 = [0]': '`p5[x]`：`x!` 里因子 5 的个数',
        'f = [1]': '`f[x]`：`x!` 去掉所有 2 和 5 之后模 10 的结果',
        'for v in range': '处理 `v = {v}`：分离它的因子 2 和 5',
        'p2[-1] += 1': '`v` 含因子 2：`p2` 末项 +1，`v` 除以 2',
        'p5[-1] += 1': '`v` 含因子 5：`p5` 末项 +1，`v` 除以 5',
        'f.append': '`f` 追加 `f[-1] * v % 10`：这一项只剩 1、3、7、9 型的因子，可以求逆元',
        'inv = {': '10 不是质数；去掉 2、5 后只剩 1、3、7、9，它们在模 10 下的逆元是 1、7、3、9',
        'p2_mod = ': '`2^t` 模 10 按 2、4、8、6 循环',
        'left = int': '`left` 是最后左边那个数：`s[0]` 的系数是 1',
        'right = int': '`right` 是最后右边那个数：`s[-1]` 的系数是 1',
        'c = f[n - 2] * inv[f[index]]': '组合数 `C(n-2, index)` 去掉 2、5 的部分：`c = {c}`',
        'c = f[n - 2] * inv[f[index - 1]]': '右侧系数是 `C(n-2, index-1)` 去掉 2、5 的部分：`c = {c}`',
        'sp2 = ': '分子分母里因子 2 的净个数 `sp2 = {sp2}`',
        'sp5 = ': '分子分母里因子 5 的净个数 `sp5 = {sp5}`',
        'if sp2 > 0': lambda S, B, r: f'`sp2 = {S.sp2}`，`sp5 = {S.sp5}`：' + ('2 和 5 都有 → 是 10 的倍数，`c = 0`' if S.sp2 > 0 and S.sp5 > 0 else '只剩因子 2，乘上 `2^sp2` 模 10' if S.sp2 > 0 else '只剩因子 5，乘上 5' if S.sp5 > 0 else '没有 2 和 5，`c` 保持不变'),
        'c *= p2_mod': '乘上 `2^sp2 % 10`：`c = {c}`',
        'c *= 5': '5 的任意次方模 10 都是 5：`c = {c}`',
        'c = 0': '`c = 0`',
        'left += int': '`left += s[{index}] * c`：`{B.left}` + `{s[index]}` × `{c}` → 取模前累加',
        'left %= 10': '`left` 模 10 = =={left}==',
        'right += int': '`right += s[{index}] * c`：`{B.right}` + `{s[index]}` × `{c}`',
        'right %= 10': '`right` 模 10 = =={right}==',
        'return left == right': '`left = {left}`，`right = {right}`，{"相同" if left == right else "不同"} → =={ret}==',
    },
    cards=dict(
        one_liner='每个数字最终的系数是杨辉三角的组合数，对 10 取模',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数字串 `s`，反复把相邻两数之和模 10，直到剩 2 个数',
                 '剩下两个数相同返回 `true`，否则 `false`',
                 '示例：`"3902"` → `true`，`"34789"` → `false`'],
        quote='观察最左侧这一列可以发现，每次迭代被累加到这一列中的元素的系数恰好是按照[1]、[1, 1]、[1, 2, 1]、[1, 3, 3, 1]、...，这样排布下来的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先不取模，写出每一轮：每个数的系数是杨辉三角，即 `C(n-2, k)`',
              '10 不是质数，阶乘不能直接求逆元：先分离因子 2 和 5，剩下的数只会是 1、3、7、9',
              '剩余部分用逆元，2、5 的个数之差 `sp2`、`sp5` 单独处理'],
        summary=['本题 `n` 很小，直接模拟也能过；yiduobo 用组合数推导，同样适用于第 II 题（`n` 到 `10^5`）',
                 '`left` 用 `C(n-2, index)`，`right` 用 `C(n-2, index-1)`，两侧对称',
                 '`sp2 > 0` 且 `sp5 > 0` 时系数必为 10 的倍数，结果 0',
                 '时间 `O(n)`，空间 `O(n)`；原文已是 Python 3 可运行写法，仅保留代码'],
    ),
)
