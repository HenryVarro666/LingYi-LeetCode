def _rng(S):
    return list(range(S['left'], S['right'] + 1)) if 'left' in S else []


def _info(S):
    if 'cnt2' not in S:
        return '先准备：2 的个数、5 的个数、末 5 位 `suf`、判断位数用的 `mul`'
    mul = S['mul']
    return (f"因子 2 共 ==`{S['cnt2']}`== 个，因子 5 共 ==`{S['cnt5']}`== 个 · "
            f"`suf` = {S['suf']:05d} · `mul` = {'超过 10 位' if mul == -1 else mul}")


CONFIG = dict(
    num=2117, title='一个区间内所有数乘积的缩写', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='拆因子 2/5 求末尾零与后 5 位，高精度截断求前 5 位（Go 原文转写）',
    tags=['灵神题单', '数学算法', '难度分 2477'],
    code='''
lim = int('9' * 200)
div = int('1' + '0' * 100)

class Solution:
    def abbreviateProduct(self, left: int, right: int) -> str:
        cnt2 = cnt5 = 0
        suf = mul = 1
        def update(x):
            nonlocal suf, mul
            suf = suf * x % 10 ** 5
            if mul != -1:
                mul *= x
                if mul >= 10 ** 10:  # 长度超过 10
                    mul = -1

        pre = 1
        for i in range(left, right + 1):
            pre *= i
            if pre > lim:  # 超过一定位数就截断
                pre //= div
            x = i
            tz = (x & -x).bit_length() - 1  # 因子 2 的个数
            cnt2 += tz
            x >>= tz
            while x % 5 == 0:
                cnt5 += 1  # 因子 5 的个数
                x //= 5
            update(x)
        cnt10 = min(cnt2, cnt5)
        for i in range(cnt10, cnt2):
            update(2)  # 补上多拆出来的 2
        for i in range(cnt10, cnt5):
            update(5)  # 补上多拆出来的 5

        if mul != -1:  # 不需要缩写
            return f"{mul}e{cnt10}"
        return f"{str(pre)[:5]}...{suf:05d}e{cnt10}"
''',
    call='Solution().abbreviateProduct(1003, 1006)',
    expect='10181...34236e1',
    views=[
        dict(type='text', fn=_info),
        dict(type='array', var=_rng, label='[left, right] 里的数', h=150,
             color=lambda S, k, v: ('blue' if S.get('_inner', {}).get('i') == v and S.get('_line', 0) <= 28 else 'green' if S.get('_line', 0) <= 28 and 'i' in S and v < S['i'] else None)),
        dict(type='text', fn=lambda S: (f"高精度乘积 `pre` = =={S['pre']}==" if 'pre' in S else '')),
        dict(type='text', fn=lambda S: (f"当前 `x` = {S['x']}（去掉 2 和 5 后）" if 'x' in S and 'tz' in S and S.get('_line', 0) <= 28 else '')),
    ],
    skip=[10, 11, 12, 13],
    max_steps=100,
    watch=[('i', 'i', 'blue'), 'cnt2', 'cnt5', ('suf', 'suf', 'cyan'), ('mul', 'mul', 'yellow')],
    captions={
        'lim = ': '`lim` = 200 个 9：`pre` 超过它就要截断',
        'div = ': '`div` = 10^100：截断时一次砍掉 100 位',
        'cnt2 = cnt5': '`cnt2`、`cnt5`：乘积里因子 2 和因子 5 的个数',
        'suf = mul = 1': '`suf` 保留末 5 位；`mul` 判断去掉 2 和 5 后是否到 10 位',
        'suf = suf * x': '`suf = suf * {x} % 10^5 = {suf}`：只留末 5 位',
        'mul *= x': '`mul` 乘上 `{x}` → {mul}',
        'mul = -1': '`mul` 已经 ≥ 10^10 → 记为 -1：==需要缩写==',
        'pre = 1': '`pre` 用来算前 5 位，直接用大整数连乘',
        'pre *= i': '`pre` 乘上 `{i}`，现在是 `{pre}`',
        'if pre > lim': lambda S, B, r: ('`pre` 超过 200 位 → 砍掉末 100 位，前面的数位不变（前 5 位不受影响）' if S.pre > 0 and B.pre > S.lim else '`pre` 还没超过 200 位，不用截断'),
        'tz = ': '`{x}` 的二进制末尾有 `{tz}` 个 0 → 含 `{tz}` 个因子 2',
        'cnt2 += tz': '`cnt2` → =={cnt2}==',
        'x >>= tz': '去掉所有因子 2：`x` → {x}',
        'while x % 5': lambda S, B, r: (f'`x = {S.x}` 还能被 5 整除，继续拆 5' if S.x % 5 == 0 else f'`x = {S.x}` 不再含因子 5'),
        'cnt5 += 1': '`cnt5` → =={cnt5}==',
        'x //= 5': '去掉一个因子 5：`x` → {x}',
        'update(x)': '把去掉 2 和 5 的 `x = {x}` 乘进 `suf`（取模，只留末 5 位）和 `mul`（累乘，看有没有到 10 位）',
        'cnt10 = min': '每个 10 = 2 × 5：末尾零个数 `cnt10 = min({cnt2}, {cnt5})` = =={cnt10}==',
        'for i in range(cnt10, cnt2)': '补 2 的循环：`i = {i}`（共要补 `cnt2 - cnt10` 个 2）',
        'for i in range(cnt10, cnt5)': '补 5 的循环：`i = {i}`',
        'update(2)': '多拆出来的因子 2 要补回去（只有成对的才是末尾零）',
        'update(5)': '多拆出来的因子 5 要补回去',
        35: lambda S, B, r: ('`mul` 不是 -1：去掉末尾零后不足 10 位，直接输出' if S.mul != -1 else '`mul == -1`：超过 10 位，需要 前5位...后5位 的缩写'),
        'return f"{mul}': '不用缩写：`{mul}` + `e{cnt10}`',
        'return f"{str(pre)': '前 5 位取 `str(pre)[:5]`，后 5 位用 `suf`（补零到 5 位），再加 `e{cnt10}`',
    },
    cards=dict(
        one_liner='末尾零看因子 2 和 5，后 5 位取模，前 5 位用大数截断',
        complexity='时间 `O(n)`，n = right - left，空间 `O(1)`',
        problem=['求 `[left, right]` 内所有整数的乘积，把它缩写成 `前5位...后5位eC`',
                 '`C` 是末尾 0 的个数，去掉末尾零后若不超过 10 位则不缩写',
                 '示例：`left=2, right=11` → `"399168e2"`；本视频：`1003~1006` → `"10181...34236e1"`'],
        quote='将每个数字的所有因子 2 和 5 去掉，然后将剩下的数字相乘，由于我们只取末 5 位，所以在乘法的过程中需要对 10^5 取模。',
        quote_src='—— 灵茶山艾府题解',
        idea=['末尾零个数 = min(因子 2 的个数, 因子 5 的个数)',
              '后 5 位：每个数拆掉 2、5 后连乘并对 10^5 取模，最后把多拆的 2 或 5 补回来',
              '前 5 位：用大整数连乘，超过 200 位就砍掉末 100 位',
              '`mul` 判断去掉末尾零后是否超过 10 位'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（取其最后一种「高精度修复」写法；big.Int 用 Python 大整数）',
                 '题解还有两种写法：直接大数乘 `MulRange`；以及用 log10 求前 5 位（有精度坑）',
                 'Go 自带的 `min` 在这里用 Python 内置 `min`，`1e5` 写成 `10 ** 5`',
                 '易错点：末 5 位要补零（`%05d`）；多拆出来的 2 或 5 要乘回去',
                 '本视频示例范围较小，`pre` 没触发截断，数据大时才会'],
    ),
)
