def _bin(S):
    n = S['num'] & 0xFFFFFFFF
    b = format(n, '032b')
    return ' '.join(b[i:i + 4] for i in range(0, 32, 4))


def _hex(S):
    n = S['num'] & 0xFFFFFFFF
    return ' '.join(f'{c}' for c in format(n, '08x'))


CONFIG = dict(
    num=405, title='数字转换为十六进制数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='转 uint32 再转 16 进制（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def toHex(self, num: int) -> str:
        return format(num & 0xFFFFFFFF, 'x')
''',
    call='Solution().toHex(-26)',
    expect='ffffffe6',
    views=[
        dict(type='text', fn=lambda S: '`num = %d`' % S['num'] if 'num' in S else '', size=40, h=70),
        dict(type='text', fn=lambda S: ('补码 32 位（每 4 位一组）：`' + _bin(S) + '`') if 'num' in S else '', size=34, h=70),
        dict(type='text', fn=lambda S: ('每 4 位 = 1 个十六进制数字：`' + _hex(S) + '`') if 'num' in S else '', size=34, h=70),
        dict(type='text', fn=lambda S: '`num & 0xFFFFFFFF = %d`' % (S['num'] & 0xFFFFFFFF) if 'num' in S else '', size=34, h=70),
    ],
    watch=[('num', 'num', 'blue'), ('num & 0xFFFFFFFF', 'num & 0xFFFFFFFF', 'green')],
    captions={
        'return format': '`num & 0xFFFFFFFF` 把负数按 32 位补码看成无符号数 `{num & 0xFFFFFFFF}`，再转 16 进制 =={ret}==',
    },
    cards=dict(
        one_liner='负数先转成 32 位无符号数，再直接转 16 进制',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把整数转成十六进制字符串，负数用补码，字母小写，无前导零',
                 '示例：`26` → `"1a"`，`-1` → `"ffffffff"`',
                 '本视频：`-26` → `"ffffffe6"`'],
        quote='func toHex(num int) string { return strconv.FormatUint(uint64(uint32(num)), 16) }',
        quote_src='—— 灵茶山艾府题解（Go）',
        idea=['补码的十六进制，就是把这个数当成 ==32 位无符号数== 来写',
              'Go 里 `uint32(num)` 做这件事；Python 用 `num & 0xFFFFFFFF`',
              '无符号数转 16 进制：Go 用 `FormatUint(…, 16)`，Python 用 `format(…, "x")`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '`uint32(num)` → `num & 0xFFFFFFFF`；`strconv.FormatUint(x, 16)` → `format(x, "x")`',
                 '时间 `O(1)`（固定 32 位），空间 `O(1)`',
                 '易错点：Python 整数无限长，不掩码的话负数会变成 `-1a`',
                 '`0` 输出 `"0"`，格式化自带无前导零'],
    ),
)
