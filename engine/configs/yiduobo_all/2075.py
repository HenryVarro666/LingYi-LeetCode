CONFIG = dict(
    num=2075, title='解码斜向换位密码', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按列枚举斜线起点', tags=[],
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
    call="Solution().decodeCiphertext('ch   ie   pr', 3)",
    expect='cipher',
    views=[
        dict(type='grid', label='二维矩阵（黄 = 当前读取的格子 (i, i+j)）', cell=96, h=330,
             var=lambda S: [list(S['encodedText'][r * S['cols']:(r + 1) * S['cols']]) for r in range(S['rows'])] if 'cols' in S else None,
             cursors=[('i if _line in (8, 9) and "i" in _inner else None', 'i + j', 'yellow')]),
        dict(type='array', var=lambda S: S.get('res'), label='res（已读出的字符）', cell=60, h=150),
    ],
    watch=[('j', 'j', 'pink'), ('i', 'i', 'blue'), 'cols'],
    captions={
        'cols = n': '`cols = n // rows = {n} // {rows} = {cols}`',
        'for j in range': lambda S, B, r: ('列都枚举完了，接下来清理后缀空格' if 'j' in B and B['j'] == S['j'] else f"第 `{S['j']}` 列的首字符开启一条斜线"),
        'for i in range': '这条斜线最多走 `min(rows, cols - j) = {min(rows, cols - j)}` 格，碰到下边或右边就停',
        'res.append': '第 `{i}` 行、第 `{i + j}` 列 → `encodedText[{i}*{cols}+{i}+{j}]` = `{res[-1]!r}`',
        'while res': lambda S, B, r: ('末尾是空格 → 删掉' if S.res and S.res[-1] == ' ' else '末尾不是空格，停止删除'),
        'res.pop': '删去一个末尾空格',
        'return': '拼接得到 ==`{ret!r}`==',
    },
    cards=dict(
        one_liner='斜线的首字符就是每一列的首字符，逐列往右下走',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['矩阵按行拼成 `encodedText`，原文是沿斜线读出来的',
                 '给定 `encodedText` 和 `rows`，还原原文，不能有后缀空格',
                 '示例：`"ch   ie   pr"`，`rows = 3` → `"cipher"`'],
        quote='每一条斜线的首字符恰好也是每一列的首字符，那么可以遍历每一列，然后从首字符开始顺着右斜线向下遍历每个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cols = n // rows`；第 `j` 列的斜线再走 `cols - 1 - j` 步到右边界',
              '所以行数最多 `min(rows, cols - j)`',
              '格子 `(i, i+j)` 对应 `encodedText[i*cols + i + j]`，依次加入答案'],
        summary=['原文为 Python 2 写法，`n / rows` 已改为 `n // rows`',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：行数上限是 `min(rows, cols - j)`，否则越过右边界',
                 '要从末尾删除后缀空格，但前面的空格保留'],
    ),
)
