CONFIG = dict(
    num=405, title='数字转换为十六进制数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='模 16 + 负数取反取补',
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
        dict(type='text', fn=lambda S: (f"`num_list` 共 8 位十六进制，从低位（右）往高位填；当前 `num = {S['num']}`" if 'num' in S and 'num_list' in S else ''), size=26),
        dict(type='array', var='num_list', label='num_list（8 位，每格 0~15）', cell=90,
             pointers={'pos % 8': 'pink'}),
        dict(type='array', var='char_list', label='char_list（结果字符）', cell=90),
    ],
    skip=['zero_flag = True', 'char_list = []', 'neg_flag = False', 'pos = -1'],
    watch=['num', 'neg_flag', 'pos', ('zero_flag', 'zero_flag', 'cyan')],
    captions={
        'num == -2147483648': '`-2^31` 取反会超出 32 位，单独特判，答案是 `80000000`',
        'num == 0': '`0` 的十六进制就是 `0`，不然下面的循环一次都不进',
        'neg_flag = True': '负数：记下 `neg_flag = True`，先当正数算，再取反取补',
        'num_list = [0] * 8': '32 位整数最多 8 位十六进制，先全填 0',
        'num_list[pos] = num % 16': '`num % 16 = {num_list[pos]}` 是最低位，填进 `num_list[{pos}]`（从右往左填）',
        'num = -num': '`num` 取相反数 → `{num}`，下面按正数取每一位',
        'for x in num_list': '从高位到低位取下一位，当前 `x = {x}`',
        'num //= 16': '`num` 除以 16 去掉最低位 → {num}（原文 `/` 在 Python 2 是整除，这里改为 `//`）',
        'pos -= 1': '`pos` 左移一位 → {pos}',
        'while num:': lambda S, B, r: (f'`num = {S.num}` 还不为 0，继续取下一位' if S.num else '`num` 为 0，正数的十六进制位都填好了'),
        'num_list = [15 - x': '每一位都用 `15 - x` 取反：=={num_list}==',
        'num_list[-1] += 1': '补码 = 取反 + 1：最低位加一 → `{num_list[-1]}`',
        'while num_list[pos] == 16': lambda S, B, r: (f'`num_list[{S.pos}] = 16` 溢出，需要进位' if S.num_list[S.pos] == 16 else '最低位没溢出，不用进位'),
        'num_list[pos] -= 16': '这一位 16 → 0',
        'num_list[pos - 1] += 1': '向高位进 1：`num_list[{pos - 1}]` → {num_list[pos - 1]}',
        'if zero_flag and x == 0': lambda S, B, r: (f'`x = {S.x}` 是前导零 → ==跳过==' if S.x == 0 and S.zero_flag else f'`x = {S.x}`，不是前导零，要输出'),
        'zero_flag = False': '遇到第一个非零位，之后的 0 都要保留',
        'char_list.append(str(x))': '`x < 10` 直接写数字 `{x}`',
        'char_list.append(chr(x + 87))': '`x >= 10` 转成字母：`chr({x} + 87)` = `{chr(x + 87)}`（`a` 的编码是 97 = 10 + 87）',
        'return': '拼成 `"{ret}"`',
    },
    cards=dict(
        one_liner='不断模 16 取出每一位；负数先算正数再取反加一',
        complexity='时间 `O(1)`（最多 8 位），空间 `O(1)`',
        problem=['把整数转成十六进制字符串，负数用补码，字母小写、无前导零',
                 '不许用库函数直接转换',
                 '示例：`26` → `"1a"`，`-1` → `"ffffffff"`；本视频演示 `-26` → `"ffffffe6"`'],
        quote='不断模16然后将10到15转化为a到f即可。对于负数来说，则是先计算正数的十六进制表示，然后取反取补。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num % 16` 是最低位，`num //= 16` 去掉它，从右往左填满 8 个格子',
              '负数：对 `26` 的 `0000001a` 每位取 `15 - x` 再 +1，就是 32 位补码',
              '最后跳过前导零，`10~15` 用 `chr(x + 87)` 变成 `a~f`'],
        summary=['时间、空间都是常数（固定 8 位）',
                 '易错：`-2^31` 取反溢出要特判；`0` 要特判；进位要一路传到高位',
                 '原文为 Python 2 写法，整数除法 `num /= 16` 已改为 `num //= 16`',
                 '更常见的写法是直接用 `num & 0xffffffff` 当无符号数处理'],
    ),
)
