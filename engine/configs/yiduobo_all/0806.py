W = [4] + [10] * 25
S_ = 'bbbcccdddaaa'


def _line_txt(S):
    if 'now' not in S:
        return ''
    return f"第 `{S['line']}` 行已用宽度 `{S['now']}` / 100"


CONFIG = dict(
    num=806, title='写字符串需要的行数', difficulty='Easy', category='模拟',
    author='yiduobo', technique='模拟 · 记录当前行宽度',
    code='''
class Solution:
    def numberOfLines(self, widths, s):

        now = 0
        line = 1
        for char in s:
            width = widths[ord(char) - 97]
            if now + width <= 100:
                now += width
            else:
                line += 1
                now = width
        
        return [line, now]
''',
    call=f'Solution().numberOfLines({W!r}, {S_!r})',
    expect=[2, 4],
    views=[
        dict(type='string', var='s', label='s', cell=80, h=220,
             ),
        dict(type='text', h=80, size=30, fn=_line_txt),
    ],
    watch=[('char', 'char', 'blue'), ('width', 'width', 'orange'), ('line', 'line', 'pink'), ('now', 'now', 'green')],
    captions={
        'now = 0': '`now`：当前行已经用掉的宽度，一开始是 0',
        'line = 1': '`line`：行数，从第 1 行开始写',
        'for char in s': '取 `s` 里的下一个字符（用完就结束）',
        'width = widths': '`{char}` 的宽度是 `widths[{ord(char) - 97}]` = =={width}==',
        'if now + width <= 100': lambda S, B, r: (f"`{S.now} + {S.width} = {S.now + S.width} <= 100` → 这一行还放得下" if S.now + S.width <= 100
                                                    else f"`{S.now} + {S.width} = {S.now + S.width} > 100` → ==放不下==，要换行"),
        'now += width': '写在当前行，`now` → =={now}==',
        'line += 1': '另起一行，`line` → =={line}==',
        'now = width': '新的一行从这个字符开始，`now = {width}`',
        'return': '一共 `{line}` 行，最后一行宽 `{now}`，返回 `[{line}, {now}]`',
    },
    cards=dict(
        one_liner='按规则模拟：放不下就换行，宽度重新从当前字符算',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`widths[i]` 是第 `i` 个小写字母的像素宽度，每行最多 100 像素',
                 '按顺序把 `s` 写下来，放不下就换行，返回 `[行数, 最后一行宽度]`',
                 '本视频：`a` 宽 4，其余字母宽 10，`s = "bbbcccdddaaa"` → `[2, 4]`'],
        quote='直接按照题目设定来模拟计算，使用一个变量now来记录当前行已经使用的宽度。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每个字符先查宽度 `widths[ord(char) - 97]`',
              '`now + width <= 100`：写在当前行，`now` 加上 `width`',
              '否则 `line += 1`，并让 `now = width`（这个字符是新一行的第一个）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：恰好 100 也能放下，条件是 `<=`',
                 '易错：换行时 `now` 是 `width`，不是 0',
                 '原文为 Python 2 风格（`class Solution(object)`），这里只改成 `class Solution`'],
    ),
)
