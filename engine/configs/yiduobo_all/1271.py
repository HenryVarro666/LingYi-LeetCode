CONFIG = dict(
    num=1271, title='十六进制魔术数字', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模拟进制转换',
    tags=[],
    code='''
class Solution(object):
    def toHexspeak(self, num):

        res = []
        num = int(num)
        while num:
            now = num % 16
            num //= 16
            if 2 <= now <= 9:
                return 'ERROR'
            
            if now == 0:
                res.append('O')
            elif now == 1:
                res.append('I')
            else:
                res.append(chr(now + 55))
        
        res.reverse()
        return ''.join(res)
''',
    call="Solution().toHexspeak('257')",
    expect='IOI',
    views=[
        dict(type='text', size=34, h=70, fn=lambda S: f"当前 `num` = =={S['num']}==" if 'num' in S else ''),
        dict(type='array', var='res', label='res（低位在前）', h=200, cell=96),
    ],
    watch=[('num', 'num', 'blue'), ('now', 'now', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 用来存转换后的字符，低位先进',
        'num = int': '输入是字符串，先转成整数：`num` = =={num}==',
        'while num': lambda S, B, r: (f'`num = {S.num}` 不为 0，继续转下一位' if S.num else '`num` 为 0：十六进制每一位都转完了'),
        'now = num % 16': '`{B.num} % 16` = =={now}==：当前最低的一位十六进制数字',
        'num //= 16': '`num` 除以 16：{B.num} → =={num}==',
        'if 2 <= now <= 9': lambda S, B, r: (f'`now = {S.now}` 在 2~9 之间：没有对应字母 → 直接返回 ERROR' if 2 <= S.now <= 9 else f'`now = {S.now}` 不在 2~9：可以转成字母'),
        'if now == 0': lambda S, B, r: ('`now = 0` → 写成字母 O' if S.now == 0 else '`now` 不是 0，继续判断'),
        'elif now == 1': lambda S, B, r: ('`now = 1` → 写成字母 I' if S.now == 1 else '`now` 是 10~15 → 对应 A~F'),
        "res.append('O')": '加入 `O` → {res}',
        "res.append('I')": '加入 `I` → {res}',
        'chr(now + 55)': '`chr({now} + 55)`：10~15 对应 `A`~`F` → {res}',
        'res.reverse': '低位在前，反转成高位在前：{res}',
        "return ''.join": '拼成字符串，返回 `{ret!r}`',
    },
    cards=dict(
        one_liner='不断模 16 取位，遇到 2~9 就报错，其余换成字母',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['把十进制数字字符串 `num` 转成大写十六进制，再把 `0` 换成 `O`、`1` 换成 `I`',
                 '结果只能含 `A B C D E F I O`，否则返回 `"ERROR"`',
                 '示例：`"257"` → 十六进制 `101` → `"IOI"`'],
        quote='直接按照不断模16除以16的方式来进行num的进制转换，若过程中出现了2到9，那么直接返回false，否则按照题目要求将0、1以及10到15转化为字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num % 16` 取出最低一位，`num //= 16` 去掉它',
              '2~9 没有合法字母，立刻返回 `ERROR`',
              '0→`O`，1→`I`，10~15 用 `chr(now + 55)` 变成 `A`~`F`；最后反转'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '易错：`chr(55 + 10) = "A"`；循环里先判错再转字母；最后别忘了反转',
                 '原文为 Python 2 写法，整数除法 `num /= 16` 已改为 `num //= 16`；原文里的 false 实际返回 `ERROR`'],
    ),
)
