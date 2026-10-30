LEFT, RIGHT, LAST = 4, 1000, 13

# 演示用：真实代码会枚举 first_part = 1 ~ 99999；这里只让 range(1, 100000) 跑到 13
# （right = 1000 时 x ≤ 31，first_part ≥ 4 之后造出的回文数平方都 > 1000 或不是回文，不影响答案）
SETUP = f'''
import builtins as _b
def range(*a):
    if a == (1, 100000):
        return _b.range(1, {LAST + 1})
    return _b.range(*a)
'''


def _found():
    out = []
    for fp in range(1, LAST + 1):
        first = str(fp)
        l = len(first)
        if l > 1 and any(c >= '3' for c in first):
            continue
        for num in (first + first[::-1], first[:l - 1] + first[::-1]):
            p = int(num) ** 2
            if LEFT <= p <= RIGHT and str(p) == str(p)[::-1]:
                out.append(f'{num}²={p}')
    return out


FOUND = _found()


def _build(S):
    if 'first' not in S or S.get('_line', 0) < 17 or 'num' not in S:
        if 'first' in S:
            f = S['first']
            return f'`first = "{f}"`：偶数位 `{f + f[::-1]}`，奇数位 `{f[:-1] + f[::-1]}`'
        return '枚举回文数 x 的==前半部分== first，拼出偶数位和奇数位两种 x'
    f, l = S['first'], len(S['first'])
    if S['_line'] <= 20:
        return f'偶数位：`"{f}" + "{f[::-1]}"` → `x = {S["num"]}`，`x² = {S["power"]}`' if S['_line'] >= 18 else \
            f'偶数位：`"{f}" + "{f[::-1]}"` → `x = {S["num"]}`'
    return (f'奇数位：`"{f[:l - 1]}" + "{f[::-1]}"` → `x = {S["num"]}`' +
            (f'，`x² = {S["power"]}`' if S['_line'] >= 23 else ''))


def _check(S, B, ret):
    p = S.power
    if not (S.left <= p):
        return f'`x² = {p} < left = {S.left}` → 不在区间里'
    if not (p <= S.right):
        return f'`x² = {p} > right = {S.right}` → 超出区间'
    if str(p) != str(p)[::-1]:
        return f'`x² = {p}` 在区间里，但==不是回文== → 不算'
    return f'`x² = {p}` 在 `[{S.left}, {S.right}]` 里，且是回文 → ==超级回文数=='


def _for(S, B, ret):
    if 'first_part' in B and B.first_part == S.first_part:
        return '枚举结束'
    return f'枚举前半部分 `first_part = {S.first_part}`'


def _char(S, B, ret):
    c = S.char
    if c >= '3':
        return f'数字 `{c!r} ≥ \'3\'`：x² 里会产生==进位==（多位数时会破坏回文）→ 标记 `flag`'
    return f'数字 `{c!r} < \'3\'`，没问题'


def _skip(S, B, ret):
    if S.l > 1 and S.flag:
        return f'`first = "{S.first}"` 不是个位数，且有 ≥3 的数字 → ==剪枝跳过=='
    if S.flag:
        return f'`first = "{S.first}"` 是个位数 → 不剪枝（`3² = 9` 就是超级回文数）'
    return f'`first = "{S.first}"` 每一位都 ≤ 2 → 继续'


CONFIG = dict(
    num=906, title='超级回文数', difficulty='Hard', category='数学',
    author='yiduobo', technique='枚举回文的前半部分 · 数位 ≤ 2 剪枝',
    tags=['字节30天'],
    code='''
class Solution(object):
    def superpalindromesInRange(self, left, right):
        res = 0
        left = int(left)
        right = int(right)
        for first_part in range(1, 100000):
            first = str(first_part)
            l = len(first)
            flag = False
            for char in str(first):
                if char >= '3':
                    flag = True
                    break
            if l > 1 and flag:
                continue

            num = first + first[::-1]
            power = int(num) ** 2
            if left <= power and power <= right and str(power) == str(power)[::-1]:
                res += 1

            num = first[:l - 1] + first[::-1]
            power = int(num) ** 2
            if left <= power and power <= right and str(power) == str(power)[::-1]:
                res += 1

        return res
''',
    setup=SETUP,
    call='Solution().superpalindromesInRange("4", "1000")',
    expect=4,
    skip=['first = str(first_part)', 'l = len(first)', 'flag = False', 'for char in str(first)'],
    views=[
        dict(type='text', size=24, h=96, lines=2,
             fn=lambda S: f'`left = "4"`，`right = "1000"`　（演示只枚举 `first_part = 1~{LAST}`；'
                          f'真实代码到 99999，right 只有 1000，后面不会再有答案）'),
        dict(type='text', size=30, h=80, fn=_build),
        dict(type='text', size=28, h=110, lines=2,
             fn=lambda S: '已找到：' + ('　'.join(f'`{x}`' for x in FOUND[:S.get('res', 0)]) if S.get('res') else '（暂无）')),
        dict(type='text', size=24, h=120, lines=3,
             fn=lambda S: 'x 和 x² 都是回文 → x ≤ `10^9`，只需枚举前半部分（≤ `10^5`）\n'
                          '多位数的 first 里出现 ==≥ 3 的数字== 就跳过'),
    ],
    watch=[('first_part', 'first_part', 'cyan'), ('flag', 'flag', 'red'), ('num', lambda S: S['num'] if S['_line'] >= 17 else None, 'blue'),
           ('power', lambda S: S['power'] if S['_line'] >= 18 else None, 'purple'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计超级回文数的个数',
        'left = int(left)': '区间端点是字符串，先转成整数：`left = {left}`',
        'right = int(right)': '`right = {right}`：x² ≤ right → x ≤ `{int(right ** 0.5)}`',
        'for first_part in range': _for,
        "if char >= '3'": _char,
        'flag = True': '标记 `flag = True`',
        'break': '有一个就够了，`break`',
        'if l > 1 and flag': _skip,
        'continue': '跳过这个 first，枚举下一个',
        17: '偶数位的 x：`first` + 反转 → `"{num}"`',
        18: '`x = {num}`，`x² = {power}`',
        19: _check,
        20: '`res += 1` → {res}',
        22: '奇数位的 x：`first[:l-1]` + 反转（中间那位共用）→ `"{num}"`',
        23: '`x = {num}`，`x² = {power}`',
        24: _check,
        25: '`res += 1` → {res}',
        'return res': '区间 `[4, 1000]` 里共有 =={res}== 个超级回文数',
    },
    max_steps=48,
    cards=dict(
        one_liner='x 和 x² 都回文：枚举 x 的前半部分，数字超过 2 就剪掉',
        complexity='枚举 `10^5` 个前半部分，每个 `O(log x)`，空间 `O(1)`',
        problem=['如果 `x` 是回文数，且 `x²` 也是回文数，就称 `x²` 是==超级回文数==',
                 '给定字符串 `left`、`right`（≤ `10^18`），求区间内超级回文数的个数',
                 '示例：`left = "4"`，`right = "1000"` → `4`（4、9、121、484）'],
        quote='注意到这里r最大为10^18，那么就意味着x最大也就10^9。由于x本身也必须是一个回文数，那么我们可以==枚举x的前半部分==，此时枚举的范围就进一步缩小到10^5了。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一个 first 能拼出两个回文：如 `122` → `122221`（偶数位）和 `12221`（奇数位）',
              '多位数的 first 里每一位都不能大于 2，否则 x² 中将产生进位，破坏回文',
              '拼出 x 后判断 `x²` 是否在 `[left, right]` 内且是回文'],
        summary=['时间：枚举 `10^5` 个 first，剪枝后实际计算的更少；空间 `O(1)`',
                 '易错：个位数 first 不剪枝（`3² = 9` 也是超级回文数）',
                 '易错：别忘了奇数位的情况，`first[:l-1] + first[::-1]` 共用中间一位',
                 '原文为 Python 2 写法：只删去了类型说明文档字符串；演示中只让枚举跑到 first_part = 13'],
    ),
)
