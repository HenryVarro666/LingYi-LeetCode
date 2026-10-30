CONFIG = dict(
    num='面试题 05.02', title='二进制数转字符串', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='乘 2 取整数位 · 至多 6 次',
    tags=[],
    code='''
class Solution:
    def printBin(self, num: float) -> str:
        s = ["0."]
        for _ in range(6):  # 至多循环 6 次
            num *= 2
            if num < 1:
                s.append('0')
            else:
                s.append('1')
                num -= 1
                if num == 0:
                    return ''.join(s)
        return "ERROR"
''',
    call='[Solution().printBin(0.625), Solution().printBin(0.1)]',
    expect=['0.101', 'ERROR'],
    views=[
        dict(type='text', size=34, h=70, fn=lambda S: (f"`num` = =={S['num']}==" if 'num' in S else '')),
        dict(type='array', var='s', label='s（已拼出的二进制串）', cell=70, h=170,
             color=lambda S, i, v: 'green' if i == len(S['s']) - 1 and i > 0 else None),
        dict(type='text', size=30, h=80, fn=lambda S: '有限位二进制小数 = b / 2^k：0.625 = 5/8 = 0.101(2)'),
    ],
    watch=['num', ('len(s)-1', lambda S: len(S['s']) - 1 if 's' in S else None, 'cyan')],
    skip=['s = ["0."]'],
    captions={
        'for _ in range(6)': '最多循环 `6` 次：十进制最多 6 位小数 → 能精确表示的话二进制也至多 6 位',
        'num *= 2': '`num` 乘 2：`0.b1b2…` 变成 `b1.b2…`，整数位就是 `b1` → `num = {num}`',
        'if num < 1': lambda S, B, r: (f'`num = {S.num} < 1` → 整数位是 ==0==' if S.num < 1
                                       else f'`num = {S.num} ≥ 1` → 整数位是 ==1=='),
        "s.append('0')": '整数位为 0：这一位二进制是 `0`，`s` 变成 `{"".join(s)}`',
        "s.append('1')": '整数位为 1：这一位二进制是 `1`，`s` 变成 `{"".join(s)}`',
        'num -= 1': '减去整数位 1，只留小数部分 → `num = {num}`',
        'if num == 0': lambda S, B, r: ('`num == 0`：小数部分用完了 → ==恰好表示完毕==' if S.num == 0
                                        else f'`num = {S.num} ≠ 0`：还有小数，继续下一位'),
        "return ''.join(s)": '拼接返回 `{ret}`',
        'return "ERROR"': '循环了 6 次 `num` 仍不为 0 → 必定是无限循环小数 → 返回 `ERROR`',
    },
    max_steps=90,
    cards=dict(
        one_liner='小数乘 2：整数位就是下一位二进制',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定 0 到 1 之间的实数 `num`，打印它的二进制表达式',
                 '无法用 32 位以内（含 `0.`）精确表示则返回 `ERROR`',
                 '示例：`0.625` → `0.101`；`0.1` → `ERROR`'],
        quote='当 num 的十进制的小数位数最多只有 6 位时，若 num 能表示为有限位二进制小数，则二进制的小数位数同样至多为 6 位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有限位二进制小数都形如 `b / 2^k`；`a / (2^6·5^6) = b / 2^k` 推出 `k ≤ 6`',
              '把 `0.b1b2…bk` 乘 2 得 `b1.b2…bk`，和 `1` 比较就知道 `b1`',
              '循环 6 次后 `num` 还不为 0，必是无限循环小数 → `ERROR`'],
        result='两次调用：`0.625` → `0.101`，`0.1` → `ERROR`',
        summary=['时间、空间都是 `O(1)`：循环至多 6 次',
                 '易错：只有 `num` 恰好减到 `0` 才算成功，不能只看循环结束',
                 '`num >= 1` 时一定要 `num -= 1`，否则下一轮整数位会错',
                 '思考题：`p` 进制下，要看 `p` 是否包含 10 的所有质因子']),
)
