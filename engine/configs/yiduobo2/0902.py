DIGITS = ["1", "3", "5", "7"]
N = 357
SN = str(N)


def _pos(S):
    """外层循环当前位置（外层 for 用的也是 index，第一段循环结束后才有 char）"""
    return S['index'] if 'char' in S else None


def _dcolor(S, i, v):
    if 'char' not in S:
        return None
    c = S['char']
    return 'green' if v < c else ('yellow' if v == c else None)


def _info(S):
    line = S.get('_line', 0)
    if 'char' not in S:
        if line <= 8:
            return f'第一部分：位数比 n 少的数随便填 → `{len(DIGITS)}^1 + … + {len(DIGITS)}^(l-1)`'
    if 'char' in S:
        k = S['index']
        rest = len(SN) - k - 1
        return (f"第 {k} 位 `'{S['char']}'`：比它小的 `cnt = {S.get('cnt', 0)}` 个，"
                f"各让后面 {rest} 位随便填（`{len(DIGITS)}^{rest}` 种）")
    return ''


def _cap_power(S, B, ret):
    k = len(S.power) - 1
    return f'`{k}` 位数：每一位都有 `{len(DIGITS)}` 种选择 → `power[{k}] = {S.power[-1]}` 个'


def _cap_res1(S, B, ret):
    k = len(S.power) - 1
    return f'位数比 n 少的数都 < n：`res += {S.power[-1]}` → `{S.res}`（{k} 位数）'


def _cap_outer(S, B, ret):
    if 'char' in B and B.char == S.char and B.index == S.index:
        return 'n 的每一位都能在 digits 里找到 → 遍历完了'
    return f"看 n 的第 `{S.index}` 位 `char = '{S.char}'`：枚举 digits 里的每个数和它比较"


def _cap_cnt(S, B, ret):
    head = '最高位填它' if S.index == 0 else '前面和 n 相同、这一位填它'
    return f"`'{S.num}' < '{S.char}'`：{head}，后面==随便选==都比 n 小 → `cnt = {S.cnt}`"


def _cap_flag(S, B, ret):
    return f"`'{S.num}' == '{S.char}'`：这一位可以和 n 相同 → `flag = True`，==要继续往后看下一位=="


def _cap_add(S, B, ret):
    k = S.index
    p = S.power[len(SN) - k - 1]
    return f'`res += cnt × power[{len(SN) - k - 1}] = {S.cnt} × {p} = {S.cnt * p}` → `res = {S.res}`'


def _cap_noflag(S, B, ret):
    if not S.flag:
        return f"`'{S.char}'` 不在 digits 里 → 这一位不能和 n 相同，后面不用看了，break"
    return f"`'{S.char}'` 在 digits 里 → 前缀和 n 相同的情况，继续看下一位"


CONFIG = dict(
    num=902, title='最大为 N 的数字组合', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按位计数：位数更少 + 最高位比 n 小 + 相等继续往后',
    tags=['字节30天'],
    code='''
class Solution(object):
    def atMostNGivenDigitSet(self, digits, n):
        l = len(str(n))
        power = [1]
        res = 0
        for index in range(l - 1):
            power.append(power[-1] * len(digits))
            res += power[-1]

        for index, char in enumerate(str(n)):
            cnt = 0
            flag = False
            for num in digits:
                if num == char:
                    flag = True
                elif num < char:
                    cnt += 1
            res += cnt * power[l - index - 1]
            if not flag:
                break

        if flag:
            res += 1

        return res
''',
    call=f'Solution().atMostNGivenDigitSet({DIGITS}, {N})',
    expect=48,
    views=[
        dict(type='text', fn=_info, size=26, h=90),
        dict(type='array', var=lambda S: list(SN), label=f'n = {N} 的各位（蓝 = 当前位 char，紫 = 已经和 n 相同的前缀）', cell=96, h=160,
             color=lambda S, i, v: 'blue' if i == _pos(S) else (None if _pos(S) is None or i > _pos(S) else 'purple')),
        dict(type='array', var='digits', label='digits（绿 = 比 char 小，黄 = 等于 char）', cell=96, h=150,
             color=_dcolor),
        dict(type='array', var='power', label=f'power[k] = {len(DIGITS)}^k（k 位随便填的方案数）', cell=96, h=150),
    ],
    watch=[('l', 'l'), ('char', 'char', 'blue'), ('cnt', 'cnt', 'green'), ('flag', 'flag', 'yellow'), ('res', 'res', 'pink')],
    captions={
        'l = len(str(n))': '`n = {n}` 一共 `l = {l}` 位',
        'power = [1]': '`power[k]` = k 位数字随便填的方案数，`power[0] = 1`',
        'res = 0': '先数==位数比 n 少==的数：它们一定都比 n 小',
        'for index in range(l - 1)': lambda S, B, r: (f'数 `{S.index + 1}` 位数' if S.get('index') != B.get('index')
                                                      else '少于 l 位的都数完了'),
        'power.append': _cap_power,
        'res += power[-1]': _cap_res1,
        'for index, char in enumerate': _cap_outer,
        'flag = True': _cap_flag,
        'cnt += 1': _cap_cnt,
        'res += cnt * power': _cap_add,
        'if not flag': _cap_noflag,
        'if flag:': lambda S, B, r: ('`flag = True`：n 本身也能用 digits 拼出来 → 恰好相等的这 1 个也要算' if S.flag
                                     else 'n 本身拼不出来，不加'),
        'res += 1': '`res += 1` → `{res}`（n 自己）',
        'return res': '一共 =={ret}== 个',
    },
    skip=['cnt = 0', 'flag = False', 'for num in digits', 'if num == char', 'elif num < char'],
    cards=dict(
        one_liner='先数位数更少的，再从最高位起：比 n 这一位小就随便填，相等就继续看下一位',
        complexity='时间 `O(d·log n)`，空间 `O(log n)`',
        problem=['给定按非递减排列的数字字符数组 `digits`，每个数字可以==重复使用任意次==',
                 '返回能写出的、==小于或等于== `n` 的正整数个数',
                 '示例：`digits = ["1","3","5","7"], n = 100` → `20`',
                 f'本视频：`n = {N}` → `48`'],
        quote='若D中有k个数小于n[l - 1]，那么可以提供==k * (len(D) ^ (l - 1))种可行的方案==。另外，若n[l - 1]出现在D中，那么还需要继续向后考虑n[l - 2]。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`x < n` 的最高位：以 `x` 开头的 l 位数都比 n 小，后面 `l-1` 位随便选',
              '`x > n` 的最高位：都比 n 大，不提供答案',
              '`x == n` 的最高位：转化为后面 `l-1` 位的同一个子问题；最后若 n 本身能拼出来再 ==+1=='],
        result='返回 `48`：`4 + 16`（少于 3 位）`+ 1×16 + 2×4 + 3×1 + 1`（n 自己）✓',
        summary=['时间 `O(d·log n)`：n 的每一位扫一遍 digits',
                 '易错：位数比 n 少的那部分别漏了；n 本身由 digits 组成时要 ==+1==',
                 '某一位在 digits 里找不到相等的数，就可以直接 break',
                 '对比灵神：同样是按位考虑；灵神用通用的数位 DP 模板，yiduobo 直接组合计数',
                 '原文为 Python 2 风格：删去了文档字符串，代码未改'],
    ),
)
