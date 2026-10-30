def _digits(v):
    if v is None:
        return None
    return list(str(v))


def _fact(S, B):
    line = S.get('_line')
    if 'k' not in S:
        return 'Python：`-123 // 10 = -13`（向下取整），`-123 % 10 = 7`（补成正数）'
    x, k = S['x'], S['k']
    bx = B.get('x')
    if line == 9:  # k = x % 10
        return f'`{bx} % 10 = {k}`' + ('：负数取模被补成了正数' if bx < 0 and k else '')
    if line == 10:  # x //= 10
        return f'`{bx} // 10 = {x}`' + ('：负数向下取整，多减了 1' if bx < 0 and bx % 10 else '')
    if line == 13:
        return f'还原真正的末位：`k = {B["k"]} − 10` = =={k}=='
    if line == 14:
        return f'补回多减的 1：`x = {bx} + 1` = =={x}=='
    if line == 21:
        return f'`y = {B["y"]} × 10 + ({k})` = =={S["y"]}=='
    return f'`x = {x}`，`k = {k}`，`y = {S["y"]}`'


def _cap_while(S, B, ret):
    if B.x != 0:
        return f'`x = {B.x} ≠ 0`：还有数字没搬完 → 继续'
    return '`x = 0`：所有数字都搬到了 y → 结束'


def _cap_check(S, B, ret):
    return (f'==先判断再乘==：`y = {S.y}` 不小于 `min_bound`，也不等于它 → 乘 10 加 `{S.k}` 不会越界'
            if not (S.y < S.min_bound or (S.y == S.min_bound and S.k < -8)) else '会越界 → 返回 0')


CONFIG = dict(
    num=7, title='整数反转', difficulty='Medium', category='数学',
    author='yiduobo', technique='逐位取模 · 先判边界再乘 10',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def reverse(self, x):
        max_bound = 214748364
        min_bound = -214748364

        negative_flag = x < 0
        y = 0
        while x != 0:
            k = x % 10
            x //= 10
            if negative_flag:
                if k != 0:
                    k -= 10
                    x += 1
                if y < min_bound or (y == min_bound and k < -8):
                    return 0
            else:
                if y > max_bound or (y == max_bound and k > 7):
                    return 0

            y = y * 10 + k
        return y
''',
    call='Solution().reverse(-123)',
    expect=-321,
    views=[
        dict(type='text', fn=_fact, h=60),
        dict(type='string', var=lambda S: _digits(S.get('x')), label='x（原数：每次从尾巴取下一位）', cell=96, index=False, h=150),
        dict(type='array', var=lambda S: [S['k']] if 'k' in S else None, label='k（这一轮取下的末位）', cell=96, index=False, h=150,
             color=lambda S, i, v: 'orange'),
        dict(type='string', var=lambda S: _digits(S.get('y')), label='y（结果：每次接到尾巴上）', cell=96, index=False, h=150,
             color=lambda S, i, v: 'green' if S.get('y') and i == len(str(S['y'])) - 1 else None),
        dict(type='text', fn=lambda S: f"边界：`max_bound = 214748364`（个位 ≤ 7），`min_bound = -214748364`（个位 ≥ -8）", h=56, size=24),
    ],
    watch=[('x', 'x', 'blue'), ('k', 'k', 'orange'), ('y', 'y', 'green'), 'negative_flag'],
    captions={
        'max_bound = 214748364': '`2^31 − 1 = 2147483647`，去掉个位 → `max_bound = 214748364`（个位是 ==7==）',
        'min_bound = -214748364': '`−2^31 = −2147483648`，去掉个位 → `min_bound = −214748364`（个位是 ==8==）',
        'negative_flag = x < 0': '`x = {x}` 是负数 → `negative_flag = True`，后面要特殊处理取模',
        'y = 0': '`y` 存反转结果，从 0 开始',
        'while x != 0': _cap_while,
        'k = x % 10': lambda S, B, r: (f'取最后一位：`{B.x} % 10 = {S.k}`，Python 把负数的模==补成了正数=='
                                       if B.x < 0 and S.k else f'取最后一位：`{B.x} % 10 = {S.k}`'),
        'x //= 10': lambda S, B, r: (f'去掉最后一位：`{B.x} // 10 = {S.x}`，负数==向下取整多减了 1=='
                                     if B.x < 0 and B.x % 10 else f'去掉最后一位：`{B.x} // 10 = {S.x}`'),
        'if negative_flag': '`x` 原本是负数 → 走负数分支',
        'if k != 0': lambda S, B, r: (f'`k = {S.k} ≠ 0`：说明取模被补了 10、整除被多减了 1，要修正' if S.k != 0
                                      else '`k = 0`：刚好整除，取模和整除都没有偏差，不用修正'),
        'k -= 10': '`k = {B.k} − 10 = {k}`：还原成真正的末位（负数）',
        'x += 1': '`x = {B.x} + 1 = {x}`：补回向下取整多减的 1',
        'if y < min_bound': _cap_check,
        'y = y * 10 + k': '`y = {B.y} × 10 + ({k})` = =={y}==：把这一位接到 y 的尾巴',
        'return y': '`x` 变成 0，反转完成：返回 =={ret}==',
    },
    cards=dict(
        one_liner='每次 mod 10 取末位接到 y 后面；乘 10 之前先和“边界 ÷ 10”比',
        complexity='时间 `O(log|x|)`，空间 `O(1)`',
        problem=['给一个 32 位有符号整数 `x`，返回把它的==数字部分反转==后的结果',
                 '反转后超出 `[−2^31, 2^31 − 1]` 就返回 `0`；假设环境不能存 64 位整数',
                 '示例：`123 → 321`，`-123 → -321`，`120 → 21`'],
        quote='每次取模之后都考虑此时y是否==大于边界除以10==，或者y等于边界除以10且k在边界个位数的范围之外。不选择直接计算y然后判断是否越界的原因是==计算y可能已经导致了越界==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`y = y × 10 + k` 之前判断：`y > 214748364`，或 `y == 214748364` 且 `k > 7` → 越界',
              'Python 负数：`-123 // 10 = -13`（多减 1），`-123 % 10 = 7`（补成正数）',
              '所以负数且 `k ≠ 0` 时：`k -= 10`、`x += 1` 修正回来'],
        result='`-123` 反转得到 ==-321==，与示例一致',
        summary=['时间 `O(log|x|)`：每轮去掉一位，空间 `O(1)`',
                 '易错：先判断 `y` 与 `边界 ÷ 10` 的关系，再乘 10，避免计算过程本身溢出',
                 '易错：Python 的 `//` 向下取整、`%` 结果非负，负数要手动修正',
                 '原文为 Python 2 写法：整除 `x /= 10` 已改为 `x //= 10`，并删去了文档字符串'],
    ),
)
