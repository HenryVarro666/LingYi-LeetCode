CONFIG = dict(
    num=1556, title='千位分隔数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='模 1000 取三位',
    code='''
class Solution(object):
    def thousandSeparator(self, n):

        res = []
        while n >= 1000:
            res.append("%03d" % (n % 1000))
            n //= 1000

        res.append(str(n))
        return '.'.join(res[::-1])
''',
    call='Solution().thousandSeparator(1234007)',
    expect='1.234.007',
    views=[
        dict(type='text', fn=lambda S: f"当前 n = =={S['n']}==" if 'n' in S else '', size=34, h=70),
        dict(type='array', var='res', label='res（从低位到高位，每项三位）', cell=140, h=200),
        dict(type='text', fn=lambda S: ('拼接顺序：' + '.'.join(S['res'][::-1])) if S.get('_line') and S['_line'] >= 9 and 'res' in S else '', size=32, h=70),
    ],
    watch=['n', 'res'],
    captions={
        'res = []': '`res` 用来存每一段三位数，先存低位',
        'while n >= 1000': lambda S, B, r: (f'`n = {S.n} >= 1000`：后面还有至少一个逗号 → 继续' if S.n >= 1000 else f'`n = {S.n} < 1000`：剩下的是最高一段，不用补零 → 退出循环'),
        'res.append("%03d"': '取最低三位 `n % 1000`，==用 %03d 补零==（007 不能写成 7）：`res` = {res}',
        'n //= 1000': '已经记下最低三位，去掉它们：`n` → =={n}==',
        'res.append(str(n))': '最高一段原样加入（不补零）：`res` = {res}',
        'return': '`res` 里是从低到高，==倒过来==再用 `.` 连接 → `{ret}`',
    },
    cards=dict(
        one_liner='不断模 1000 取出三位，倒过来用点连接',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['给一个整数 `n`，每三位加一个点 `.` 作为千位分隔符，返回字符串',
                 '示例：`987` → `"987"`，`1234` → `"1.234"`',
                 '本视频：`1234007` → `"1.234.007"`'],
        quote='不断将n模1000并除以1000直到n小于1000，并记录下每次模的结果。这样一来按逗号分割的各个部分的值就计算出来了，整理后输出即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n % 1000` 就是最低的一段三位数，`n // 1000` 去掉这一段',
              '中间的段要补零到三位，所以用 `"%03d"`',
              '段是从低位到高位得到的，输出前 `res[::-1]` 翻转'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '易错点：中间段要补零（如 `007`）；最高一段不能补零',
                 '`n` 小于 1000 时循环不执行，直接返回 `str(n)`',
                 '原文为 Python 2 写法，整数除法 `n /= 1000` 已改为 `n //= 1000`'],
    ),
)
