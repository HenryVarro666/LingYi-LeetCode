CONFIG = dict(
    num=171, title='Excel表列序号', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='26 进制转换（1 到 26）', tags=[],
    code='''
class Solution(object):
    def titleToNumber(self, s):

        res = 0
        for char in s:
            res = res * 26 + ord(char) - 64

        return res
''',
    call="Solution().titleToNumber('ZYA')",
    expect=18227,
    views=[
        dict(type='string', var='s', label='列名 s', pointers={}, h=170,
             color=lambda S, i, v: 'blue' if v == S.get('char') and i == S.get('_i', i) else None),
        dict(type='text', size=32, h=100, fn=lambda S: f"`ord('{S['char']}') − 64` = =={ord(S['char'])-64}==（A=1, B=2, …, Z=26）" if 'char' in S else ''),
        dict(type='text', size=32, h=100, fn=lambda S: f"res = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('char', 'char', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '从 0 开始累计',
        'for char in s': '从左到右读到字母 `{char}`',
        'res = res * 26': '`{B.res} × 26 + {ord(char)} − 64` = `{B.res*26} + {ord(char)-64}` = =={res}==：先把已有的数进一位，再加上当前字母的值',
        'return res': '列名 `{s}` 对应序号 `{res}`',
    },
    cards=dict(
        one_liner='把列名当成 26 进制数，字母 A 到 Z 对应 1 到 26',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['Excel 列名 `A, B, …, Z, AA, AB, …`，求列名对应的序号',
                 '`A → 1`，`Z → 26`，`AA → 27`',
                 '本视频：`ZYA` → `18227`'],
        quote='与168题相反，但是本质依然是26进制转换。同样需要注意这里的26进制是从1到26而不是0到25，另外依然可以运用大写A的ascii码是65来方便进制转换。',
        quote_src='—— yiduobo 题解原文',
        idea=['每读一个字母：`res = res * 26 + 字母值`，和十进制读数一样',
              '字母值 = `ord(char) − 64`，因为 `ord("A") = 65`',
              '注意是 1 到 26，没有 0，所以减 64 而不是 65'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：减 64 不是 65',
                 '与第 168 题（序号转列名）互为逆运算',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
