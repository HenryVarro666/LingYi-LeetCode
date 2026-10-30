def _top(S):
    if 'v' not in S or 'start' not in S:
        return ''
    return f"当前子串 `s[{S['start']}:{S['start'] + S['length']}] = {S['s'][S['start']:S['start'] + S['length']]}` → `v = {S['v']}`"


def _prime_cap(S, B, r):
    if S.flag:
        return f'`x×x > {S.v}` 之前都没有因子 → `{S.v}` 是质数，用它更新前三大'
    return f'`{S.v}` 不是质数，丢弃'


CONFIG = dict(
    num=3556, title='最大质数子字符串之和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='暴力枚举子串 + 手动维护前三大',
    tags=['灵神题单', '难度分 1440'],
    code='''
class Solution(object):
    def sumOfLargestPrimes(self, s):
        

        primes = [0] * 3
        for length in range(1, len(s) + 1):
            for start in range(len(s) - length + 1):
                v = int(s[start :start + length])
                if v == 0 or v == 1:
                    continue

                flag = True
                x = 2
                while x * x <= v:
                    if v % x == 0:
                        flag = False
                        break
                    x += 1
                
                if flag:
                    if v > primes[0]:
                        primes[0], primes[1], primes[2] = v, primes[0], primes[1]
                    elif v != primes[0] and v > primes[1]:
                        primes[1], primes[2] = v, primes[1]
                    elif v != primes[0] and v != primes[1] and v > primes[2]:
                        primes[2] = v
        
        return sum(primes)
''',
    call='Solution().sumOfLargestPrimes("232")',
    expect=28,
    max_steps=75,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（蓝 = 当前子串）', cell=110, window=('start', 'start + length - 1'),
             color=lambda S, i, c: 'blue' if 'start' in S and S['start'] <= i < S['start'] + S['length'] else None, h=220),
        dict(type='array', var='primes', label='primes（降序保存目前最大的三个不同质数，0 = 空位）', cell=110, h=210,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=lambda S: (f"试除 `x = {S['x']}`，`x×x = {S['x'] * S['x']}`，`v = {S['v']}`"
                                         if 'x' in S and 'v' in S and S.get('_line') in range(13, 20) else ''), size=26),
    ],
    watch=['v', 'x', 'flag'],
    captions={
        'primes = [0] * 3': '`primes` 降序存最大的三个==不同==质数，用 0 占位',
        'for length in range': '子串长度 `length = {length}`',
        'for start in range': '起点 `start = {start}`',
        'v = int(s[start': '子串转成整数：`v = {v}`',
        'if v == 0 or v == 1': lambda S, B, r: (f'`v = {S.v}`：0 和 1 不是质数 → 跳过' if S.v in (0, 1)
                                                else f'`v = {S.v}` 不是 0 或 1，需要判断质数'),
        'flag = True': '先假定 `v` 是质数',
        'x = 2': '从 `x = 2` 开始试除',
        'while x * x <= v': lambda S, B, r: (f'`x×x = {S.x * S.x} <= {S.v}`：继续试除' if S.x * S.x <= S.v
                                              else f'`x×x = {S.x * S.x} > {S.v}`：不会再有因子，结束试除'),
        'if v % x == 0': '`{v} % {x} = {v % x}` → {"==整除，不是质数==" if v % x == 0 else "不整除"}',
        'flag = False': '找到因子 `{x}` → `flag = False`',
        'x += 1': '`x` → {x}',
        'if flag': _prime_cap,
        'if v > primes[0]': lambda S, B, r: (f'`v = {S.v} > primes[0] = {S.primes[0]}`：成为新的最大值，原来的整体后移'
                                             if S.v > S.primes[0] else f'`v = {S.v}` 不比最大值 `{S.primes[0]}` 大，看第二名'),
        'primes[0], primes[1], primes[2] = v': '`primes` → `{primes}`（旧的第一、二名顺延成第二、三名）',
        'elif v != primes[0] and v > primes[1]': lambda S, B, r: (
            f'`v = {S.v}` ≠ 第一名 `{S.primes[0]}` 且 `> primes[1] = {S.primes[1]}`：成为第二名'
            if S.v != S.primes[0] and S.v > S.primes[1] else f'`v = {S.v}`：与第一名重复或不大于第二名，看第三名'),
        'primes[1], primes[2] = v': '`primes` → `{primes}`',
        'elif v != primes[0] and v != primes[1] and v > primes[2]': lambda S, B, r: (
            f'`v = {S.v}` 与前两名都不同且 `> primes[2] = {S.primes[2]}`：成为第三名'
            if S.v != S.primes[0] and S.v != S.primes[1] and S.v > S.primes[2]
            else f'`v = {S.v}` ：==与已有质数重复==或太小，==丢弃=='),
        'primes[2] = v': '`primes` → `{primes}`',
        'return sum(primes)': '三个最大的不同质数之和：`{primes}` → =={ret}==',
    },
    cards=dict(
        one_liner='子串很少，直接暴力枚举；边找质数边维护前三大并去重',
        complexity='时间 `O(10^{n/2})` 量级，空间 `O(1)`',
        problem=['字符串 `s`（长度 ≤ 10）的所有子串转成整数后，找==三个最大的不同质数==求和',
                 '不足三个就求所有不同质数之和；子串转整数时忽略前导零',
                 '示例：`"12234"` → `1469`；本视频用 `"232"` → `23 + 3 + 2 = 28`'],
        quote='对于长度n的字符串，其一共有n * (n - 1) / 2个子字符串。本题中s的长度不超过10，那么就可以直接暴力枚举s的所有子串，然后检测这些子串对应的数是否为质数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['按长度、起点两层循环枚举子串，`int(...)` 转成整数',
              '`0`、`1` 直接跳过；其余用 `x*x <= v` 试除判质数',
              '`primes` 只存三个数：比第一名大就整体后移；否则要==先确认不与已有重复==再插入第二、三名'],
        summary=['时间主要花在最长子串的试除上，约 `O(10^{n/2})`，空间 `O(1)`',
                 '易错：==去重==靠 `v != primes[0]` 等比较，漏写会把同一个质数算多次',
                 '前导零：`int("07") = 7`，`v == 0` 要跳过（`"00"`）',
                 '原文代码已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神用集合去重再 `sorted(...)[-3:]`，这里不排序，手动保持前三名有序'],
    ),
)
