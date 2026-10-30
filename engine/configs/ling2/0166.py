CODE = '''
class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        sign = '-' if numerator * denominator < 0 else ''
        numerator = abs(numerator)  # 保证下面的计算过程不产生负数
        denominator = abs(denominator)

        # 计算整数部分 q 和初始余数 r
        q, r = divmod(numerator, denominator)
        if r == 0:  # 没有小数部分
            return sign + str(q)

        ans = [sign + str(q) + '.']
        r_to_pos = {r: 1}  # 初始余数对应小数点后第一位
        while r:
            # 计算小数点后的数字 q，更新 r
            q, r = divmod(r * 10, denominator)
            ans.append(str(q))
            if r in r_to_pos:  # 有循环节
                pos = r_to_pos[r]  # 循环节的开始位置
                return f"{''.join(ans[:pos])}({''.join(ans[pos:])})"
            r_to_pos[r] = len(ans)  # 记录余数对应位置
        return ''.join(ans)  # 有限小数
'''
_LINES = CODE.strip('\n').split('\n')
L_RET = next(i + 1 for i, l in enumerate(_LINES) if 'return f"' in l)
L_POS = next(i + 1 for i, l in enumerate(_LINES) if 'pos = r_to_pos[r]' in l)
L_DIV = next(i + 1 for i, l in enumerate(_LINES) if 'divmod(r * 10' in l)


def _ans_color(S, i, v):
    pos = S.get('pos')
    if S.get('_line') in (L_POS, L_RET) and isinstance(pos, int):
        return 'pink' if i >= pos else None
    a = S.get('ans') or []
    if i == len(a) - 1 and i > 0 and S.get('_line') not in (L_POS, L_RET):
        return 'yellow'
    return None


def _map_fmt(k, v):
    return f'r={k} → 第{v}位'


def _formula(S, B):
    if 'ans' not in S:
        if 'q' in S and 'r' in S:
            return f"整数部分 `{S['numerator']} // {S['denominator']}` = {S['q']}，初始余数 `r` = =={S['r']}=="
        return '长除法：==余数 × 10 再除以分母==，商就是下一位小数'
    if 'pos' in S:
        a = S['ans']
        return f"余数 `{S['r']}` 第 {S['pos']} 位就出现过 → 循环节是 `{''.join(a[S['pos']:])}`"
    if S.get('_line') == L_DIV:
        return f"`{B['r']} × 10 = {B['r'] * 10}`，`{B['r'] * 10} ÷ {S['denominator']}` = 商 =={S['q']}== 余 =={S['r']}=="
    return f"当前余数 `r` = {S.get('r')}；已得到 `{''.join(S['ans'])}`"


CONFIG = dict(
    num=166, title='分数到小数', difficulty='Medium', category='哈希',
    author='灵茶山艾府', technique='模拟长除法 · 哈希表记余数位置',
    tags=['字节3个月', '字节6个月'],
    code=CODE,
    call='Solution().fractionToDecimal(3, 14)',
    expect='0.2(142857)',
    views=[
        dict(type='array', var='ans', label='ans（ans[0] 是整数部分和小数点；粉 = 循环节）', cell=96, h=210, color=_ans_color),
        dict(type='map', var='r_to_pos', label='r_to_pos：余数 → 它对应小数点后第几位', fmt=_map_fmt, h=230),
        dict(type='text', fn=_formula, size=27, h=80),
    ],
    watch=[('q', 'q', 'blue'), ('r', 'r', 'pink'), ('pos', 'pos', 'green'), 'denominator'],
    captions={
        "sign = '-'": '先确定符号：`{B.numerator} × {B.denominator}` ≥ 0 → 结果非负，`sign` 为空',
        'numerator = abs': '取绝对值，保证下面的计算过程不产生负数',
        'denominator = abs': '分母也取绝对值',
        'q, r = divmod(numerator': '整数部分 `q = {numerator} // {denominator}` = {q}，初始余数 `r` = {r}',
        'if r == 0': '`r = {r}` ≠ 0 → 有小数部分，继续做长除法',
        "ans = [sign": '`ans[0]` = 整数部分加小数点 `{ans[0]}`；之后每一位小数追加一项',
        'r_to_pos = {r: 1}': '哈希表记录==余数第一次出现时在算第几位小数==：初始余数 {r} 对应第 1 位',
        'while r:': lambda S, B, ret: f'余数 `r = {B.r}` ≠ 0：还没除尽，继续算下一位',
        'q, r = divmod(r * 10': '`{B.r} × 10 = {B.r * 10}`，除以 {denominator}：这一位小数是 =={q}==，新余数 `r` = {r}',
        'ans.append(str(q))': '把这一位 `{q}` 追加到答案：`{"".join(ans)}`',
        'if r in r_to_pos': lambda S, B, ret: (f'余数 `{B.r}` ==出现过==！再算下去会重复，找到循环节' if B.r in B.r_to_pos
                                              else f'余数 `{B.r}` 没出现过，还没进入循环'),
        'pos = r_to_pos[r]': '余数 `{r}` 上次对应第 {pos} 位 → 循环节从 `ans[{pos}]` 开始',
        'return f"': '循环节之前是 `{"".join(ans[:pos])}`，循环节 `{"".join(ans[pos:])}` 括起来：=={ret}==',
        'r_to_pos[r] = len(ans)': '记录：余数 {r} 对应第 {len(ans)} 位小数（`len(ans)`）',
    },
    cards=dict(
        one_liner='长除法逐位算小数，余数重复出现 = 找到循环节',
        complexity='时间 `O(N)`，空间 `O(N)`，`N = min(|分母|, 10^4)`',
        problem=['给分子 `numerator`、分母 `denominator`，以字符串返回小数',
                 '循环部分用括号括起来；有限小数直接返回',
                 '示例：`1/2` → `"0.5"`；`4/333` → `"0.(012)"`；`3/14` → `"0.2(142857)"`'],
        quote='用一个哈希表记录，哈希表的 key 是余数 r，value 是这个余数对应着第几位小数。如果 r 在哈希表中，说明有循环节。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每一步：商 `= r×10 // 分母` 是下一位小数，余数更新为 `r×10 % 分母`',
              '下一位只由当前余数决定 → ==余数重复，后面的数字就会重复==',
              '`r = 0` 说明除尽，是有限小数'],
        summary=['时间/空间 `O(N)`：至多 `|分母|` 种不同余数',
                 '先处理符号再取绝对值：`numerator * denominator < 0` 才加负号',
                 '`r_to_pos` 记的是「余数 → 位置」，循环节从该位置到末尾',
                 '`r == 0` 的整除情况要提前返回，不能带小数点'],
    ),
)
