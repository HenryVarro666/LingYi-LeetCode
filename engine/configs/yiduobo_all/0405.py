def _nl(S):
    nl = S.get('num_list')
    return nl


CONFIG = dict(
    num=405, title='数字转换为十六进制数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='模 16 取数位 · 负数取反加一',
    tags=[],
    code='''
class Solution(object):
    def toHex(self, num):
        
        if num == -2147483648:
            return '80000000'
        if num == 0:
            return '0'

        neg_flag = False
        if num < 0:
            neg_flag = True
            num = -num

        num_list = [0] * 8
        pos = -1
        while num:
            num_list[pos] = num % 16
            num //= 16
            pos -= 1

        if neg_flag:
            num_list = [15 - x for x in num_list]
            num_list[-1] += 1
            pos = -1
            while num_list[pos] == 16:
                num_list[pos] -= 16
                num_list[pos - 1] += 1
                pos -= 1

        zero_flag = True
        char_list = []
        for x in num_list:
            if zero_flag and x == 0:
                continue
            zero_flag = False
            if x < 10:
                char_list.append(str(x))
            else:
                char_list.append(chr(x + 87))
        
        return ''.join(char_list)
''',
    call='Solution().toHex(-26)',
    expect='ffffffe6',
    views=[
        dict(type='text', fn=lambda S: '`num = %d`，取负标记 `%s`' % (S['num'], S['neg_flag']) if 'neg_flag' in S else '', size=32, h=60),
        dict(type='array', var='num_list', label='num_list（8 个十六进制位，下标 -1 是最低位）',
             pointers={'pos + 8': 'blue'}, h=180,
             color=lambda S, i, v: 'green' if S.get('pos') is not None and False else None),
        dict(type='array', var='char_list', label='char_list（输出的字符）', h=170),
    ],
    watch=[('num', 'num', 'blue'), ('pos', 'pos', 'pink'), ('neg_flag', 'neg_flag', 'orange'), ('x', 'x', 'green')],
    captions={
        '== -2147483648': '`-2147483648` 取负会超出 32 位，单独特判，答案固定 `80000000`',
        'if num == 0': '`0` 直接返回 `"0"`，免得后面去前导零后变空串',
        'num = -num': '负数：先按正数算十六进制，记下 `neg_flag`，`num` 变成 `{num}`',
        'num_list = [0] * 8': '32 位 = 8 个十六进制位，先全填 0',
        'num_list[pos] = num % 16': '`num % 16 = {num_list[pos]}` 是当前最低位，存到下标 `{pos}`',
        'num /= 16': '`num //= 16`：去掉已处理的最低位，剩 `{num}`',
        'num //= 16': '`num //= 16`：去掉已处理的最低位，剩 `{num}`',
        'pos -= 1': '`pos` 往高位移一格：`{pos}`',
        '15 - x': '取反：每一位 `15 - x`，得到 `{num_list}`',
        'num_list[-1] += 1': '补码 = 取反 + 1：最低位加 1 → `{num_list[-1]}`',
        'while num_list[pos] == 16': lambda S, B, r: (f'`num_list[{S.pos}] = 16`，要进位' if S.num_list[S.pos] == 16 else f'`num_list[{S.pos}] = {S.num_list[S.pos]}`，不需要进位了'),
        'num_list[pos] -= 16': '这一位满 16 → 清零，向更高位进 1',
        'num_list[pos - 1] += 1': '更高位加 1：`{num_list}`',
        'zero_flag and x == 0': lambda S, B, r: (f'`x = 0` 且仍在前导零 → 跳过' if S.zero_flag and S.x == 0 else f'`x = {S.x}`，不是前导零 → 输出'),
        'zero_flag = False': lambda S, B, r: ('遇到第一个非零位，之后的 0 都要保留' if not S.char_list else '前导零已经结束，继续输出'),
        'x < 10': lambda S, B, r: (f'`{S.x} < 10` → 直接写数字' if S.x < 10 else f'`{S.x} >= 10` → 用字母'),
        'chr(x + 87)': '`chr({x} + 87)`：`10→a`…`15→f`，得 `{char_list[-1]}`',
        'str(x)': '写入数字 `{char_list[-1]}`',
        'return ': '拼接得到 =={ret}==',
    },
    cards=dict(
        one_liner='不断模 16 取数位；负数先算正数，再取反加一',
        complexity='时间 `O(1)`（固定 8 位），空间 `O(1)`',
        problem=['把整数转成十六进制，负数用补码，字母小写，无前导零',
                 '示例：`26` → `"1a"`，`-1` → `"ffffffff"`',
                 '本视频：`-26` → `"ffffffe6"`'],
        quote='比较基础的题目，不断模16然后将10到15转化为a到f即可。对于负数来说，则是先计算正数的十六进制表示，然后取反取补。',
        quote_src='—— yiduobo 题解原文',
        idea=['`26` 的 8 位十六进制是 `0000001a`',
              '负数补码 = 按位取反再 `+1`：每位 `15 - x`，最低位加 1 并处理进位',
              '最后跳过前导零，`10~15` 用 `chr(x + 87)` 变成 `a~f`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`num /= 16` 已改为 `num //= 16`（整数除法），其余不变',
                 '易错点：`-2147483648` 取负会溢出，要特判；`0` 要特判返回 `"0"`',
                 '补码加 1 后可能连续进位，所以用 `while` 处理 `16`',
                 '对比灵神：灵神一行 `num & 0xFFFFFFFF` 直接得到补码，这里手动取反加一'],
    ),
)
