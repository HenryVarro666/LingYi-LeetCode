CONFIG = dict(
    num=3280, title='将日期转换为二进制表示', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='split + bin',
    tags=[],
    code='''
class Solution:
    def convertDateToBinary(self, date: str) -> str:
        a = date.split('-')
        for i in range(len(a)):
            a[i] = bin(int(a[i]))[2:]
        return '-'.join(a)
''',
    call='Solution().convertDateToBinary("2080-02-29")',
    expect='100000100000-10-11101',
    views=[
        dict(type='text', fn=lambda S: (f"第 `{S['i']}` 段：=={S['a'][S['i']]}==" if 'i' in S else ''), size=28),
        dict(type='array', var='a', label='a（年、月、日三段）', cell=300,
             color=lambda S, idx, v: 'blue' if 'i' in S and idx == S['i'] else None,
             pointers={'i': 'pink'}),
    ],
    watch=[('i', 'i', 'pink'), ('a', 'a', 'green')],
    captions={
        'date.split': '按 `-` 分割：`a = {a}`，三段分别是年、月、日',
        'for i in range': lambda S, B, ret: ('三段都转完了，循环结束' if 'i' in B and S.i == B.i else f'处理第 `{S.i}` 段：`a[{S.i}] = "{S.a[S.i]}"`'),
        'a[i] =': '`int("{B.a[i]}")` 去掉前导零，`bin(...)` 得到 `0b...`，`[2:]` 去掉前缀 `0b` → ==`{a[i]}`==',
        'return': '用 `-` 把三段二进制拼起来：`"{ret}"`',
    },
    cards=dict(
        one_liner='按 - 分割，逐段转二进制，再拼回去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`date` 格式为 `yyyy-mm-dd`',
                 '年、月、日各自转成二进制（不带前导零），仍用 `-` 连接',
                 '示例：`"2080-02-29"` → `"100000100000-10-11101"`'],
        quote='1. 把字符串 date 按照 - 分割。2. 对于每个字符串，首先转成数字。3. 然后转成二进制字符串。4. 最后，用 - 拼接每个二进制字符串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`int("02")` 自动去掉前导零，变成 2',
              '`bin(2)` 是 `"0b10"`，用 `[2:]` 去掉前缀',
              '题解还给了 Py3 一行写法：`\'-\'.join(bin(int(s))[2:] for s in date.split(\'-\'))`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`bin` 的结果带 `0b` 前缀，必须切掉',
                 '必须先 `int` 再 `bin`，才能去掉月、日的前导零'],
    ),
)
