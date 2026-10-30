def _frac(S):
    if 'num' not in S:
        return ''
    if 'int_part' not in S or 'multi' not in S:
        return f'解析 `{S["num"]}`：先按小数点拆成整数部分和小数部分'
    if S.get('parts') and len(S['parts']) == 2 and 'int_part' in S:
        pass
    return f'目前：`{S["int_part"]}` / `{S["multi"]}`'


def _cmp(S):
    if 'int_s' in S and 'int_t' in S:
        return (f'`{S["s"]}` = =={S["int_s"]}/{S["mutli_s"]}==，`{S["t"]}` = =={S["int_t"]}/{S["multi_t"]}==；'
                f'交叉相乘 `{S["int_s"] * S["multi_t"]}` vs `{S["int_t"] * S["mutli_s"]}`')
    if 'int_s' in S:
        return f'`{S["s"]}` 已转成分数 =={S["int_s"]}/{S["mutli_s"]}=='
    return '把两个数都化成 分子/分母，再交叉相乘比较'


CONFIG = dict(
    num=972, title='相等的有理数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='化成分数 · 交叉相乘',
    tags=[],
    code='''
class Solution(object):
    def isRationalEqual(self, s, t):

        int_s, mutli_s = self.parse(s)
        int_t, multi_t = self.parse(t)

        #print int_s, mutli_s
        #print int_t, multi_t

        return int_s * multi_t == int_t * mutli_s

    def parse(self, num):
        parts = num.split('.')
        if len(parts) == 1:
            return int(parts[0]), 1

        int_part, float_part = parts
        int_part = int(int_part)
        multi = 1

        parts = float_part.replace(')', '').split('(')
        if parts[0] != '':
            multi = 10 ** (len(parts[0]))
            int_part = int_part * multi + int(parts[0])

        if len(parts) == 1:
            return int_part, multi
        
        return int_part * (10 ** (len(parts[1])) - 1) + int(parts[1]), multi * (10 ** (len(parts[1])) - 1)
''',
    call="Solution().isRationalEqual('0.(52)', '0.5(25)')",
    expect=True,
    setup='',
    views=[
        dict(type='text', fn=_cmp, size=28, h=120),
        dict(type='text', fn=lambda S: (f'小数部分拆成：非循环 `{S["parts"][0] or "空"}`' + (f'，循环节 `{S["parts"][1]}`' if len(S['parts']) > 1 else '，没有循环节')) if 'parts' in S and S.get('_line', 0) >= 21 else '', size=28, h=90),
        dict(type='text', fn=_frac, size=34, h=110),
    ],
    watch=['num', 'int_part', 'multi'],
    captions={
        'int_s, mutli_s = self.parse(s)': '把 `s = {s}` 转成分数（分子，分母）',
        'int_t, multi_t = self.parse(t)': lambda S, B, r: f'`s` 已经是 `{S.int_s}/{S.mutli_s}`；现在把 `t = {S.t}` 也转成分数',
        'parts = num.split': '以小数点切开 `{num}`：{parts}',
        14: lambda S, B, r: '没有小数点：是整数' if len(S.parts) == 1 else '有小数点：有限小数或循环小数，继续拆',
        'return int(parts[0]), 1': '整数 `x` → 分数 `x / 1`',
        'int_part, float_part = parts': '整数部分 `{int_part}`，小数部分 `{float_part}`',
        'int_part = int(int_part)': '整数部分转成数字 `{int_part}`',
        19: '分母先记 1',
        'parts = float_part': '去掉右括号再按 `(` 切：前面是==非循环部分==，后面是==循环节==：{parts}',
        'if parts[0] != ': lambda S, B, r: (f'非循环部分 `{S.parts[0]}` 非空 → 成立，要乘 `10^{len(S.parts[0])}`' if S.parts[0] != ''
                                           else '非循环部分为空 → 不成立，跳过'),
        23: '非循环部分长 `{len(parts[0])}` 位：分母 `multi = 10^{len(parts[0])}` = {multi}',
        'int_part = int_part * multi': '整数部分 ×`{multi}` 再加上小数 `{parts[0]}`，得到分子 `{int_part}`',
        26: lambda S, B, r: ('只有非循环部分：有限小数，分数就是 `{}/{}`'.format(S.int_part, S.multi) if len(S.parts) == 1
                                              else f'还有循环节 `{S.parts[1]}`，需要消掉循环'),
        'return int_part, multi': '有限小数：`{int_part} / {multi}`',
        'return int_part * (10': lambda S, B, r: (f'循环节长 `m = {len(S.parts[1])}`：`x\'×10^m − x\'` 消掉循环 → ==`{r[0]}/{r[1]}`=='),
        'return int_s * multi_t': '`a×d = {int_s} × {multi_t} = {int_s * multi_t}`，`b×c = {int_t} × {mutli_s} = {int_t * mutli_s}` → ==相等：{ret}==，不需要约分',
    },
    cards=dict(
        one_liner='整数、有限小数、循环小数统统化成分数，再交叉相乘',
        complexity='时间 `O(L)`（`L` 为字符串长度），空间 `O(1)`',
        problem=['`s`、`t` 是两个非负有理数的字符串，可含括号表示的循环节',
                 '判断两个数是否相等：`0.1(6)`、`0.1666(6)`、`0.166(66)` 都是 1/6',
                 '示例：`s = "0.(52)"`，`t = "0.5(25)"` → `True`'],
        quote='设x = 0.(52)，那么100x = 52.(52)，后者减去前者，可得100x - x = 52，解得x = 52 / 99。',
        quote_src='—— yiduobo 题解原文',
        idea=['整数 `x` = `x/1`；有限小数乘 `10^l` 再除 `10^l`',
              '循环小数：乘 `10^m` 后与原数相减，把循环节消掉，如 `0.(52) = 52/99`',
              '得到 `a/b`、`c/d` 后只比较 `a×d == b×c`，不用约分'],
        summary=['时间 `O(L)`，空间 `O(1)`',
                 '`0.5(25)`：分子 `5×99 + 25 = 520`，分母 `10×99 = 990`',
                 '易错：分母要同时乘 `10^(非循环位数)` 与 `10^m − 1`',
                 '交叉相乘比较避免了约分，也避免了浮点误差'],
    ),
)
