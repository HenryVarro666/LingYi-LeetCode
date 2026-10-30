def _c(z):
    re, im = round(z.real, 1) + 0.0, round(z.imag, 1) + 0.0
    if abs(im) < 0.05:
        return f'{re:g}'
    return f'{re:g}{im:+g}i'


def _show(S):
    p = S.get('p')
    if not isinstance(p, list):
        return []
    return [_c(z) if isinstance(z, complex) else z for z in p]


def _stage(S):
    if 'start' in S and 'n' in S and 24 <= S['_line'] <= 32 and 'root_w' in S:
        return (f"当前层：每 `{S['n']}` 个一组合并，组内蝶形运算 `x ± w·y`（`w` 是单位根旋转因子）")
    if 'pos' in S and S['_line'] <= 22:
        return '`pos` 是 0..m-1 的二进制位反转顺序，让迭代版 FFT 不用递归'
    return ''


CONFIG = dict(
    num=3549, title='两个多项式相乘', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='FFT：系数 → 点值 → 逐点相乘 → 逆变换',
    tags=['卷积'],
    code='''
class Solution(object):
    def multiply(self, poly1, poly2):
        
        m = 1
        while m < len(poly1) + len(poly2) - 1:
            m <<= 1

        n = m >> 1
        pos = [0] * m
        rnd = 0
        while n:
            v = 0
            for start in range(0, m, n):
                for index in range(start, start + n):
                    pos[index] |= (v << rnd)
                v ^= 1
            n >>= 1
            rnd += 1

        def fft(p, rev=1):
            p = [p[pos[index]] for index in range(m)]
            n = 2
            while n <= m:
                root_w = complex(cos(2 * pi / n), rev * sin(2 * pi / n))
                for start in range(0, m, n):
                    w = complex(1.0)
                    for index in range(start, start + (n >> 1)):
                        x = p[index]
                        y = w * p[index + (n >> 1)]
                        p[index] = x + y
                        p[index + (n >> 1)] = x - y
                        w *= root_w

                n <<= 1
            
            if rev == -1:
                for index in range(m):
                    p[index] /= m
            
            return p

        p1 = [complex(x) for x in poly1] + [complex(0)] * (m - len(poly1))
        p1 = fft(p1)
        p2 = [complex(x) for x in poly2] + [complex(0)] * (m - len(poly2))
        p2 = fft(p2)
        
        p = [x * y for x, y in zip(p1, p2)]
        p = fft(p, -1)
        
        while len(p) > len(poly1) + len(poly2) - 1:
            p.pop()

        return [int(round(x.real)) for x in p]
''',
    setup='from math import cos, sin, pi',
    call='Solution().multiply([1, 2], [3, 4])',
    expect=[3, 10, 8],
    views=[
        dict(type='text', h=70, fn=lambda S: f"`poly1 = {S['poly1']}`，`poly2 = {S['poly2']}`，补零长度 `m = {S['m']}`" if 'm' in S and 'poly1' in S else ''),
        dict(type='array', var=lambda S: S['pos'] if 'pos' in S else [], label='pos（位反转下标）', h=170, cell=80),
        dict(type='array', var=_show,
             label='p（FFT 工作数组；复数显示为 实部±虚部i）', h=200, cell=110),
        dict(type='text', h=70, fn=_stage),
    ],
    watch=['m', 'n', 'rev', 'start', 'index'],
    skip=['rnd = 0', 'rnd += 1', 'n = m >> 1', 'n >>= 1', 'v = 0', 'v ^= 1', 'm <<= 1', 'n = 2', 'n <<= 1',
          'w = complex(1.0)', 'x = p[index]', 'w *= root_w', 'y = w * p[index', 'p[index + (n >> 1)] = x - y', 'p.pop()', 'p[index] /= m', 'for start in range', 'for index in range', 'while n',
          'while m <', 'm = 1', 'pos = [0]', 'while len(p)'],
    max_steps=70,
    captions={
        'pos[index] |= (v << rnd)': '`pos` 逐位构造位反转：第 `{rnd}` 位，这一块 `v = {v}`，补上 `v << {rnd}`，`pos[{index}]` → =={pos[index] | (v << rnd)}==',
        'p = [p[pos[index]]': '按 `pos` 重排输入：这样每一层只需相邻分组做蝶形运算，不用递归',
        'root_w = complex': '这一层的单位根 `root_w = e^(rev·2πi/{n})`，`rev = {rev}`（1 = 正变换，-1 = 逆变换）',
        'p[index] = x + y': lambda S, B, r: (f"`x = {_c(S.x)}`，`y = w × p[{S.index + (S.n >> 1)}]` = {_c(S.y)}；"
                                             f"`p[{S.index}] = x + y` = =={_c(S.x + S.y)}==，`p[{S.index + (S.n >> 1)}] = x − y` = =={_c(S.x - S.y)}=="),
        'if rev == -1': lambda S, B, r: ('逆变换（`rev = -1`）：每项除以 `m`，还原系数' if S.rev == -1 else '正变换（`rev = 1`）：不需要除以 `m`'),
        'return p': lambda S, B, r: ('逆变换完成：得到系数 `' + str([round(z.real, 1) for z in S.p]) + '`（尾部是补零多出来的）' if S.rev == -1
                                     else '得到 `m` 个单位根处的点值：`' + str([_c(z) for z in S.p]) + '`'),
        'p1 = [complex(x) for x in poly1]': '把 `poly1` 补零到长度 `m`，再 FFT 得到它在 `m` 个单位根处的点值',
        'p2 = [complex(x) for x in poly2]': '`poly2` 同样补零并做 FFT',
        'p = [x * y for x, y': '点值相乘：`(A·B)(ω) = A(ω)·B(ω)`，一趟逐点乘就完成多项式乘法',
        'p = fft(p, -1)': '用共轭单位根（`rev = -1`）做逆 FFT，把点值变回系数',
        'return [int': '取实部并四舍五入：结果系数 =={[int(round(x.real)) for x in p]}==',
    },
    cards=dict(
        one_liner='系数相乘是卷积；变成点值后逐点相乘，再逆变换回来',
        complexity='时间 `O(m log m)`，空间 `O(m)`，`m` 为补齐后的 2 的幂',
        problem=['`poly1[i]`、`poly2[i]` 是多项式第 `i` 次项的系数',
                 '返回乘积多项式的系数数组，长度可达 `10^5`，朴素 `O(n^2)` 会超时',
                 '本视频：`[1,2]`（1+2x）乘 `[3,4]`（3+4x）→ `[3,10,8]`'],
        quote='对于这个问题，朴素的算法就是逐项相乘计算，时间复杂度为O(n^2)。但是本题中两个多项式的长度都可达10^5，需要进行优化。',
        quote_src='—— yiduobo 题解原文',
        idea=['点值表示下，两个多项式相乘 = 在同一组点上逐点相乘',
              '取 `m` 个单位根作为点：折半后恰好成对相反，可用分治 / 蝶形 `O(m log m)` 求值',
              '逆变换 = 换成共轭单位根再除以 `m`；迭代版用位反转 `pos` 代替递归'],
        summary=['时间 `O(m log m)`，`m` 是不小于 `n1+n2-1` 的最小 2 的幂',
                 '最后要 `round` 取整，并裁掉补零多出的尾部',
                 '原文第一份递归版会超时，这里用的是原文第二份非递归写法',
                 '库里缺 `cos / sin / pi`：在 `setup` 里 `from math import cos, sin, pi`',
                 '浮点误差随长度增大；系数很大时需注意精度'],
    ),
)
