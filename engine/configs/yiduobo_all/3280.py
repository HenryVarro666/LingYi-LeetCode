CONFIG = dict(
    num=3280, title='将日期转换为二进制表示', difficulty='Easy', category='位运算',
    author='yiduobo', technique='手写除 2 取余',
    tags=[],
    code='''
class Solution(object):
    def convertDateToBinary(self, date):

        res = []
        for part in date.split('-'):
            v = int(part)
            digits = []
            while v:
                digits.append(str(v % 2))
                v //= 2
            digits.reverse()
            res.append(''.join(digits))
        
        return '-'.join(res)
''',
    call='Solution().convertDateToBinary("1900-01-01")',
    expect='11101101100-1-1',
    views=[
        dict(type='text', fn=lambda S: (f"正在转换 `{S['part']}`，当前 `v = {S['v']}`" if 'part' in S and 'v' in S else ''), size=28),
        dict(type='array', var='digits', label='digits（低位在前，最后要反转）', cell=64),
        dict(type='array', var='res', label='res（已转好的各段）', cell=300),
    ],
    watch=[('part', 'part', 'blue'), ('v', 'v', 'pink'), ('digits', 'digits', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for part': lambda S, B, ret: ('三段都转完了，循环结束' if 'part' in B and S.part == B.part else f'取出一段 `"{S.part}"`'),
        'digits = []': '准备一个空列表，存这一段的每一位',
        'v = int': '`int` 去掉前导零：`v = {v}`',
        'while v': lambda S, B, ret: (f"`v = {S.v}` 非 0，继续取最低位" if S.v else '`v = 0`，这一段的位都取完了'),
        'digits.append': '`v % 2 = {v % 2}` 是当前最低位，先存进 `digits`',
        'v //= 2': '右移一位：`v` 变成 `{v}`',
        'digits.reverse': '先取到的是低位，反转后高位在前：`{digits}`',
        'res.append': '这一段的二进制是 =={\'\'.join(digits)}==，加入 `res`',
        'return': '用 `-` 连接各段：`"{ret}"`',
    },
    cards=dict(
        one_liner='把年月日拆开，各自除 2 取余转二进制',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`date` 形如 `yyyy-mm-dd`，把年、月、日分别转成二进制',
                 '二进制不带前导零，仍用 `-` 连接',
                 '示例：`"1900-01-01"` → `"11101101100-1-1"`'],
        quote='按照题目要求，将年、月、日分离出来，逐项转换成二进制表示，然后拼接在一起就行了。',
        quote_src='—— yiduobo 题解',
        idea=['`split(\'-\')` 把三段分离出来，`int` 转成数',
              '不用 `bin`：不断 `v % 2` 取最低位，`v //= 2` 右移',
              '低位先出，所以最后要 `digits.reverse()`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：取出的是低位在前，别忘了反转',
                 '题目保证月、日 ≥ 1，所以 `while v` 不会得到空串'],
    ),
)
