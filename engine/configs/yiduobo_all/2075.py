CONFIG = dict(
    num=2075, title='解码斜向换位密码', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 逐列沿斜线读取',
    code='''
class Solution(object):
    def decodeCiphertext(self, encodedText, rows):

        n = len(encodedText)
        cols = n // rows
        res = []
        for j in range(cols):
            for i in range(min(rows, cols - j)):
                res.append(encodedText[i * cols + i + j])
        
        while res and res[-1] == ' ':
            res.pop()
        return ''.join(res)
''',
    call='Solution().decodeCiphertext("ch   ie   pr", 3)',
    expect='cipher',
    views=[
        dict(type='grid', h=250, label='encodedText 按行排成矩阵（黄 = 当前读取）', var=lambda S: [list(S['encodedText'][r*S['cols']:(r+1)*S['cols']]) for r in range(S['rows'])] if 'cols' in S else [],
             color=lambda S, r, c, v: 'yellow' if 'i' in S and 'j' in S and r == S['i'] and c == S['i'] + S['j'] else None),
        dict(type='string', var='res', h=150, label='res（已解码字符）'),
    ],
    watch=['n', 'cols', ('j', 'j', 'blue'), ('i', 'i', 'pink')],
    captions={
        'n = len': '`n = {n}`',
        'cols = n': '总长 `{n}` ÷ 行数 `{rows}` = 列数 `{cols}`（原文写 `/`，已改为 `//`）',
        'res = []': '`res` 存解码出的字符',
        'for j in range': '第 `{j}` 列的首字符，就是一条右斜线的起点',
        'for i in range': '这条斜线最多向下走 `min(rows, cols - j) = {min(rows, cols - j)}` 格，再走就出矩阵了',
        'res.append': '读第 `{i}` 行第 `{i + j}` 列，即 `encodedText[{i * cols + i + j}]` = `{encodedText[i * cols + i + j]!r}`',
        'while res': lambda S, B, r: ('末尾 `' + repr(S.res[-1]) + '` 是空格，后缀空格不允许 → 删掉') if S.res and S.res[-1] == ' ' else '末尾不是空格，停止删除',
        'res.pop': '删掉一个后缀空格',
        'return': '拼起来得到 `{ret!r}`',
    },
    cards=dict(
        one_liner='每列首字符是一条斜线的起点，顺着右下读到边界',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['原文按斜线填入 `rows` 行的矩阵，再按行读出得到 `encodedText`',
                 '给定 `encodedText` 和 `rows`，还原原字符串（无后缀空格）',
                 '示例：`"ch   ie   pr", rows=3` → `"cipher"`'],
        quote='每一条斜线的首字符恰好也是每一列的首字符，那么可以遍历每一列，然后从首字符开始顺着右斜线向下遍历每个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['列数 `cols = n // rows`',
              '第 `j` 列再往右走 `cols-1-j` 步到边界，所以行数上限 `min(rows, cols-j)`',
              '格子 `(i, i+j)` 对应 `encodedText[i*cols + i + j]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '最后要删掉后缀空格，前置空格要保留',
                 '行数循环上限是 `min(rows, cols - j)`，不是 `rows`'],
    ),
)
