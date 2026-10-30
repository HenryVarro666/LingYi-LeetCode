CODE = '''
class Solution(object):
    def fractionToDecimal(self, numerator, denominator):
        flag = 1

        if numerator < 0:
            flag *= -1
            numerator = -numerator

        if denominator < 0:
            flag *= -1
            denominator = -denominator

        int_part = numerator // denominator
        numerator %= denominator

        if numerator == 0:
            return str(flag * int_part)

        rest_dict = {}
        cycle = ''

        rest_dict[numerator] = 0
        while numerator:
            numerator *= 10
            cycle += str(numerator // denominator)
            numerator %= denominator
            if numerator in rest_dict:
                cycle_pos = rest_dict[numerator]
                break
            else:
                rest_dict[numerator] = len(cycle)

        if flag < 0:
            res = '-'
        else:
            res=  ''

        res += str(int_part)

        if not numerator:
            res += '.' + cycle
        else:
            res += '.' + cycle[:cycle_pos] + '(' + cycle[cycle_pos:] + ')'
        return res
'''
_LINES = CODE.strip('\n').split('\n')
L_MUL = next(i + 1 for i, l in enumerate(_LINES) if 'numerator *= 10' in l)
L_CYC = next(i + 1 for i, l in enumerate(_LINES) if 'cycle += str' in l)
L_MOD = next(i + 1 for i, l in enumerate(_LINES) if 'numerator %= denominator' in l and l.startswith(' ' * 12))


def _cyc_color(S, i, v):
    cp = S.get('cycle_pos')
    if isinstance(cp, int):
        return 'pink' if i >= cp else None
    c = S.get('cycle') or ''
    if i == len(c) - 1 and S.get('_line') in (L_CYC, L_MOD):
        return 'yellow'
    return None


def _formula(S, B):
    ln = S.get('_line')
    if 'cycle' not in S:
        if 'int_part' in S:
            return f"整数部分 `{S['int_part']}`，余数 `{S['numerator']}`（之后 `numerator` 就当余数用）"
        return '竖式除法：==余数 × 10 ÷ 除数==，商是下一位，余数继续往下除'
    if ln == L_MUL:
        return f"余数 `{B['numerator']}` 乘上 10 → 被除数 =={S['numerator']}=="
    if ln == L_CYC:
        return f"`{S['numerator']} ÷ {S['denominator']}` 商 =={S['cycle'][-1]}==，已算出的商 `{S['int_part']}.{S['cycle']}`"
    if ln == L_MOD:
        return f"`{B['numerator']} % {S['denominator']}` = 余 =={S['numerator']}=="
    if 'cycle_pos' in S:
        return f"被除数 `{S['numerator'] * 10}` 又出现了 → 循环节从 `cycle[{S['cycle_pos']}]` 开始"
    return f"已算出的商 `{S['int_part']}.{S['cycle']}`，当前余数 `{S['numerator']}`"


CONFIG = dict(
    num=166, title='分数到小数', difficulty='Medium', category='哈希',
    author='yiduobo', technique='竖式除法 · 记录出现过的余数',
    tags=['字节3个月', '字节6个月'],
    code=CODE,
    call='Solution().fractionToDecimal(20, 7)',
    expect='2.(857142)',
    views=[
        dict(type='string', var='cycle', label='cycle：小数部分（粉 = 循环节；变量 numerator 复用为余数）', cell=96, h=200, color=_cyc_color),
        dict(type='map', var='rest_dict', label='rest_dict：余数 → 它产生的那一位在 cycle 中的下标',
             fmt=lambda k, v: f'余{k} → cycle[{v}]', h=230),
        dict(type='text', fn=_formula, size=27, h=80),
    ],
    watch=[('numerator', 'numerator', 'pink'), ('int_part', 'int_part', 'blue'),
           ('cycle_pos', 'cycle_pos', 'green'), ('res', 'res', 'green'), ('flag', 'flag')],
    captions={
        'flag = 1': '`flag` 记录答案符号：先确定符号，再把计算变成正数除以正数',
        'if numerator < 0': '分子 `{B.numerator}` 不是负数，不用翻转',
        'if denominator < 0': '分母 `{B.denominator}` 不是负数，不用翻转',
        'int_part = numerator // denominator': '整数部分 `{numerator} // {denominator}` = =={int_part}==',
        'numerator %= denominator': lambda S, B, ret: (
            f'`numerator` 复用为余数：`{B.numerator} % {S.denominator}` = =={S.numerator}=='
            if 'cycle' not in S else
            f'新余数 `{B.numerator} % {S.denominator}` = =={S.numerator}=='),
        'if numerator == 0': '余数 `{numerator}` ≠ 0 → 有小数部分，开始竖式除法',
        'rest_dict = {}': '`rest_dict` 记下每个出现过的余数（被除数），用来发现循环',
        "cycle = ''": '`cycle` 存小数点后已经算出的各位商',
        'rest_dict[numerator] = 0': '初始余数 `{numerator}` 产生小数点后第一位（`cycle[0]`）',
        'while numerator': lambda S, B, ret: f'余数 `{B.numerator}` ≠ 0：没除尽，算下一位',
        'numerator *= 10': '小数点后下一位：余数 `{B.numerator}` 乘上 10，变成 {numerator}',
        'cycle += str': '`{numerator} // {denominator}` = =={cycle[-1]}==，此时商为 `{int_part}.{cycle}`',
        'if numerator in rest_dict': lambda S, B, ret: (
            f'余数 `{B.numerator}` ==之前出现过==！又回到了 `{B.numerator}×10` 的情况' if B.numerator in B.rest_dict
            else f'余数 `{B.numerator}` 没出现过，继续往下除'),
        'cycle_pos = rest_dict': '它当初产生的是 `cycle[{cycle_pos}]` → 循环节从下标 {cycle_pos} 开始',
        'break': '找到循环节，跳出循环',
        'rest_dict[numerator] = len(cycle)': '记录：余数 `{numerator}` 将产生 `cycle[{len(cycle)}]`',
        'if flag < 0': '`flag = {flag}` > 0，答案不带负号',
        "res=  ''": '`res` 从空串开始',
        'res += str(int_part)': '拼上整数部分 `{int_part}`',
        'if not numerator': '余数 `{numerator}` ≠ 0：是==循环小数==，要加括号',
        "res += '.' + cycle[:cycle_pos]": '`cycle[:{cycle_pos}]` 是不循环部分，`cycle[{cycle_pos}:]` = `{cycle[cycle_pos:]}` 括起来 → `{res}`',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='按竖式除法一位位地算，被除数重复出现就找到了循环节',
        complexity='时间 `O(分母)`，空间 `O(分母)`',
        problem=['给分子 `numerator`、分母 `denominator`，以字符串返回小数',
                 '循环部分用括号括起来；有限小数直接返回',
                 '示例：`1/2` → `"0.5"`；`20/7` → `"2.(857142)"`'],
        quote='每次记录下当前位的被除数与商，然后继续往下做除法。如果除尽了或者出现过了原来出现过的被除数，那么就找到了答案。',
        quote_src='—— yiduobo 题解',
        idea=['以 `20÷7` 为例：商 2 余 6；`60÷7` 商 8 余 4；`40÷7` 商 5 余 5……',
              '算到 `20÷7` 时又余 6，==又变成了 6 乘上 10 的情况== → 循环节 `857142`',
              'Python 2 里负数取模会得到正数，所以先定符号，再按正数除以正数做'],
        summary=['时间/空间 `O(分母)`：余数只有 `0 ~ 分母−1` 这几种',
                 '`rest_dict[余数]` = 该余数产生的那一位在 `cycle` 中的下标',
                 '`numerator` 被复用为余数；整除时直接返回 `str(flag * int_part)`',
                 '原文为 Python 2 写法：整数除法 `/` 已改为 `//`，删去文档字符串'],
    ),
)
