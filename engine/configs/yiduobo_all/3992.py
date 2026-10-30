CONFIG = dict(
    num=3992, title='重新排列字符串以避免字符对', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · 只计数 x 和 y', tags=['灵神题单'],
    code='''
class Solution(object):
    def rearrangeString(self, s, x, y):
        
        cnt_x = 0
        cnt_y = 0
        res = []
        for c in s:
            if c == x:
                cnt_x += 1
            elif c == y:
                cnt_y += 1
            else:
                res.append(c)
        
        res.append(y * cnt_y)
        res.append(x * cnt_x)
        return ''.join(res)
''',
    call='Solution().rearrangeString("xaxbycyd", "x", "y")',
    expect='abcdyyxx',
    views=[
        dict(type='string', var='s', h=260,
             label='s（黄 = x，青 = y，蓝框 = 当前字符 c）',
             color=lambda S, i, v: ('blue' if 'c' in S and len(S['res']) + S['cnt_x'] + S['cnt_y'] - (1 if S['_line'] in (9, 11, 13) else 0) == i and i < len(S['s']) else None)
                                    or ('yellow' if v == S['x'] else ('cyan' if v == S['y'] else None))),
        dict(type='array', var='res', h=240, label='res（其他字符按原顺序放入）'),
        dict(type='text', size=28, fn=lambda S: (f"`x` 出现 =={S['cnt_x']}== 次，`y` 出现 =={S['cnt_y']}== 次" if 'cnt_y' in S else '')),
    ],
    watch=[('cnt_x', 'cnt_x', 'yellow'), ('cnt_y', 'cnt_y', 'cyan'), ('c', 'c', 'blue')],
    captions={
        'cnt_x = 0': '`cnt_x`：x 出现了几次，只计数，不放进答案',
        'cnt_y = 0': '`cnt_y`：y 出现了几次',
        'res = []': '`res` 存放既不是 x 也不是 y 的字符，保持原顺序',
        'for c in s': lambda S, B, r: (f'取出字符 `{S.c}`' if len(S.res) + S.cnt_x + S.cnt_y < len(S.s) else '字符全部处理完毕，退出循环'),
        'if c == x': lambda S, B, r: (f'`{S.c}` 就是 x，不放进去，只计数' if S.c == S.x else f'`{S.c}` 不是 x，继续看是不是 y'),
        'cnt_x += 1': '`cnt_x` → =={cnt_x}==',
        'elif c == y': lambda S, B, r: (f'`{S.c}` 就是 y，只计数' if S.c == S.y else f'`{S.c}` 既不是 x 也不是 y'),
        'cnt_y += 1': '`cnt_y` → =={cnt_y}==',
        'res.append(c)': '`{c}` 原样放进 `res`',
        'res.append(y * cnt_y)': '先把 `{cnt_y}` 个 y 一次性接上：`{y * cnt_y!r}`',
        'res.append(x * cnt_x)': '最后接 `{cnt_x}` 个 x：`{x * cnt_x!r}`，y 全在 x 前面',
        'return': '拼接得到 `{ret!r}`',
    },
    cards=dict(
        one_liner='x、y 只数个数，其他字符照搬，最后先 y 后 x 补上',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `s` 和两个不同字母 `x`、`y`',
                 '重排 `s`，要求所有 `y` 都在所有 `x` 左边，返回任意合法结果',
                 '示例：`"aabc", x="a", y="c"` → `"cbaa"`'],
        quote='对于其中的x和y，仅统计出现次数，分别记为cnt_x以及cnt_y，而对于其他的字符，则按原顺序添加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目只要求任意合法答案，方案很多',
              'x、y 之间的相对顺序不重要，只要 y 都在 x 前',
              '遍历完成后先接 `cnt_y` 个 y，再接 `cnt_x` 个 x'],
        summary=['时间 `O(n)`，空间 `O(n)`（新建了 `res`）',
                 '循环里 x、y 不进 `res`，别漏掉最后两次 `append`',
                 '顺序是先 y 后 x，反了就不合题意',
                 '对比灵神：灵神原地双指针交换，空间 `O(1)`；这里换成计数再拼接'],
    ),
)
