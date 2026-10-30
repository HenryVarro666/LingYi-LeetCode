def _dv(S):
    if 'ans' not in S:
        return f"被除数 `{S['dividend']}` ÷ 除数 `{S['divisor']}`：不能用除法，只能用加减"
    return f"还剩 dividend = ==`{S['dividend']}`==，已凑出商 ans = ==`{S['ans']}`=="


def _stop(S, B, r):
    pos, f, d = S.pos, S.f, S.dividend
    return f'`f[{pos}] = {f[pos]}`：`dividend - f[pos]` = `{d - f[pos]}` {">=" if d - f[pos] >= f[pos] else "<"} `f[pos]` = `{f[pos]}` → ' + \
        (f'==成立==，还能翻倍，加入 `{2 * f[pos]}`' if d - f[pos] >= f[pos] else '==不成立==，再翻倍就超过被除数了，停')


CONFIG = dict(
    num=29, title='两数相除', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='倍增 + 二进制还原',
    tags=[],
    code='''
class Solution(object):
    def divide(self, dividend, divisor):

        max_int = 2147483647
        min_int = -2147483648

        if dividend == min_int and divisor == -1:
            return max_int

        negative = False
        sign = False
        if dividend > 0 and divisor < 0:
            negative = True
            sign = True
            dividend = -dividend
        elif dividend < 0 and divisor > 0:
            negative = True
            sign = True
            divisor = -divisor
        elif dividend < 0 and divisor < 0:
            negative = True

        f = [0, divisor]
        pos = 1
        while (negative and min_int - f[pos] <= f[pos] and dividend - f[pos] <= f[pos]) or (not negative and max_int - f[pos] >= f[pos] and dividend - f[pos] >= f[pos]):
            f.append(f[pos] + f[pos])
            pos += 1

        weight = [0, 1]
        for index in range(2, len(f)):
            weight.append(weight[index -1] + weight[index - 1])
        
        ans = 0
        while dividend != 0:
            for index in range(len(f) - 1, -1, -1):
                if (negative and f[index] >= dividend) or (not negative and f[index] <= dividend):
                    break

            if index == 0:
                break

            ans += weight[index]
            dividend -= f[index]

        if sign:
            ans = -ans
        return ans
''',
    call='Solution().divide(100, 7)',
    expect=14,
    views=[
        dict(type='text', fn=_dv, size=30, h=90),
        dict(type='array', var='f', label='f[i] = 2^i × 除数（除数的倍增表）', h=210, cell=110,
             pointers={'pos': 'blue', 'index': 'pink'},
             color=lambda S, i, v: 'green' if S.get('_line') in (42, 43) and i == S.get('index') else None),
        dict(type='array', var='weight', label='weight[i] = 2^i（对应的商）', h=190, cell=110,
             pointers={'index': 'pink'},
             color=lambda S, i, v: 'green' if S.get('_line') in (42, 43) and i == S.get('index') else None),
    ],
    watch=['dividend', 'divisor', ('pos', 'pos', 'blue'), ('index', 'index', 'pink'), ('ans', 'ans', 'green')],
    skip=[37, 'max_int = ', 'min_int = ', 'sign = False', 'negative = False'],
    captions={
        'if dividend == min_int and divisor == -1': '唯一会溢出的情况：`-2^31 ÷ -1`，直接返回 `max_int`。本例不是，继续',
        'if dividend > 0 and divisor < 0': '判断符号：正 ÷ 负？本例两个都是正数，不成立',
        'elif dividend < 0 and divisor > 0': '负 ÷ 正？不成立',
        'elif dividend < 0 and divisor < 0': '负 ÷ 负？不成立 → `negative` 保持 False：两数都按正数处理',
        'f = [0, divisor]': '倍增表从 `f[1] = divisor = {divisor}` 开始，`f[0] = 0` 占位',
        'pos = 1': '`pos` 指向表里最后一项',
        'while (negative': _stop,
        'f.append': '`f` 末尾加入翻倍的 `{f[-1]}`（= `f[pos] + f[pos]`）',
        'pos += 1': '`pos` → {pos}',
        'weight = [0, 1]': '`weight[i]` 记录 `f[i]` 对应的商 `2^i`',
        'for index in range(2, len(f))': '逐项翻倍：`weight[index] = weight[index-1] × 2`',
        'weight.append': '`weight` 末尾加入 `{weight[-1]}`',
        'ans = 0': '`ans` 累计商，从 0 开始',
        'while dividend != 0': lambda S, B, r: (f'`dividend = {S.dividend}` ≠ 0：还没减完，继续' if S.dividend != 0 else '`dividend = 0`：正好减完，结束'),
        'for index in range(len(f) - 1': '从最大的倍数往小找：找第一个 `f[index] <= dividend`',
        'if (negative and f[index]': lambda S, B, r: ((f'`f[{S.index}] = {S.f[S.index]} <= dividend = {S.dividend}` → ==成立==，能减，停下' if S.index else '到了 `index = 0`：`f[0] = 0` 只是占位，说明没有能减的倍数了，停下') if S.f[S.index] <= S.dividend else f'`f[{S.index}] = {S.f[S.index]} > dividend = {S.dividend}` → 太大，找小一档的'),
        'if index == 0': lambda S, B, r: ('`index = 0`：连 `f[1]` 也减不动，剩下的不够一个除数 → 结束' if S.index == 0 else f'`index = {S.index} ≠ 0` → 有可减的倍数'),
        'ans += weight[index]': '商加上 `weight[{index}] = {weight[index]}`：`ans = {B.ans} + {weight[index]}` = =={ans}==',
        'dividend -= f[index]': '被除数减掉 `f[{index}] = {f[index]}`：还剩 =={dividend}==',
        'break': '`index = 0`，跳出外层 `while`',
        'if sign': '`sign` 为 False，不用变号',
        'return ans': '商是 `{ans}`',
    },
    cards=dict(
        one_liner='用倍增表逼近：每次减掉最大的 2^i 倍除数',
        complexity='时间 `O(log^2 n)`，空间 `O(log n)`',
        problem=['不用乘、除、取余，求 `dividend ÷ divisor`，向零取整',
                 '结果超出 32 位整数时按边界截断：`-2^31 ÷ -1` 返回 `2^31 - 1`',
                 '本视频：`100 ÷ 7` → `14`'],
        quote='对于n/k，每次减k的话效率太低，例如100000000/1这种情况，需要做一亿次，减到猴年马月都减不完，于是在这里可以利用倍增的思路。',
        quote_src='—— yiduobo 题解原文',
        idea=['把商 `ans` 写成二进制：`n = k×(1·p0 + 2·p1 + 4·p2 + …) + m`',
              '先预处理 `f[i] = 2^i × k`，`weight[i] = 2^i`',
              '从大到小：`f[i]` 减得动就减，同时 `ans` 加上 `weight[i]`'],
        summary=['时间 `O(log^2 n)`，空间 `O(log n)`',
                 '`-2^31 ÷ -1` 会溢出，要先单独处理',
                 '负数不取绝对值（`-2^31` 取反会溢出）：用 `negative` 让比较方向反过来，`sign` 决定最后是否变号',
                 '原文已是 Python 3 可运行写法，未作改动'],
    ),
)
