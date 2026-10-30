CONFIG = dict(
    num=504, title='七进制数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模 7 除 7 · 记录符号',
    code='''
class Solution(object):
    def convertToBase7(self, num):

        if num == 0:
            return "0"

        neg_flag = False
        if num < 0:
            neg_flag = True
            num = -num
        res = []
        while num:
            res.append(str(num % 7))
            num //= 7
        res.reverse()
        if neg_flag:
            return "-" + ''.join(res)
        else:
            return ''.join(res)
''',
    call='Solution().convertToBase7(-100)',
    expect='-202',
    views=[
        dict(type='text', size=34, fn=lambda S: (f"`num` = =={S['num']}=={'（已取绝对值）' if S.get('neg_flag') else ''}" if 'num' in S else '')),
        dict(type='array', var='res', h=170, label='res（先得到的是低位，最后要反转）',
             color=lambda S, i, v: 'green' if S['_line'] == 15 else None),
        dict(type='text', size=28, fn=lambda S: ('符号：负数，最后补 `-`' if S.get('neg_flag') else '符号：非负' if 'neg_flag' in S else '')),
    ],
    watch=[('num', 'num', 'blue'), ('neg_flag', 'neg_flag', 'pink'), ('res', 'res', 'green')],
    captions={
        'if num == 0': '0 要单独处理：下面的 `while num` 一次都不会进，会得到空串',
        'neg_flag = True': '`num` 是负数：==记下符号==，后面只转换绝对值',
        'num = -num': '`num` 变成正数 `{num}`：Python 2 里负数取模有差别，所以先去掉符号',
        'res.append': '`{B.num} % 7 = {B.num % 7}`：这是当前最低位 → `res = {res}`',
        'num //= 7': '`{B.num} // 7 = {num}`：去掉最低位，剩下的继续转换' ,
        'while num': lambda S, B, r: (f'`num = {S.num}` 非 0，还有高位要转' if S.num else '`num = 0`：所有位都取完了'),
        'res.reverse': '先取到的是低位，所以反转：`res = {res}`',
        "return \"-\"": '负数：拼上 `-` → =={ret}==',
        "return ''.join": '拼成字符串 =={ret}==',
        'if neg_flag': lambda S, B, r: '`neg_flag` 为真：结果前面要加负号' if S.neg_flag else '`neg_flag` 为假：直接返回',
    },
    cards=dict(
        one_liner='不断模 7 除 7，低位先出，最后反转',
        complexity='时间 `O(log num)`，空间 `O(log num)`',
        problem=['给定整数 `num`，返回它的七进制字符串',
                 '示例：`100` → `"202"`，`-7` → `"-10"`',
                 '本视频：`-100` → `"-202"`'],
        quote='比较基础的题目，直接仿照转二进制的方法，不断模七除以七即可。需要注意在使用python2时对负数取模稍有差别，因此需要记录符号转换成正数来做。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num % 7` 是最低位，`num // 7` 去掉最低位',
              '循环到 `num` 为 0，得到的数字顺序是反的，所以最后 reverse',
              '负数先记符号、取绝对值，最后在前面补 `-`'],
        summary=['时间 `O(log num)`，空间 `O(log num)`',
                 '`num == 0` 必须单独返回 `"0"`',
                 '原文为 Python 2 写法，`num /= 7` 已改为 `num //= 7`（整数除法）',
                 '同类：十进制转二进制、十六进制（第 405 题）'],
    ),
)
