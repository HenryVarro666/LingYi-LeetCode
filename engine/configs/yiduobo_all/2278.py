CONFIG = dict(
    num=2278, title='字母在字符串中的百分比', difficulty='Easy', category='字符串',
    author='yiduobo', technique='遍历计数',
    tags=[],
    code='''
class Solution(object):
    def percentageLetter(self, s, letter):

        cnt = 0
        for char in s:
            if char == letter:
                cnt += 1
        
        return cnt * 100 // len(s)
''',
    call='Solution().percentageLetter("foobarbaz", "o")',
    expect=22,
    views=[
        dict(type='string', var='s', label='s（绿 = 等于 letter 的字符）', cell=90, h=250,
             color=lambda S, i, v: 'green' if v == S['letter'] else None),
        dict(type='text', h=100, size=30, fn=lambda S: f"已数到 `{S.get('cnt', 0)}` 个 `'{S['letter']}'`"),
    ],
    watch=[('cnt', 'cnt', 'green'), ('char', 'char', 'blue'), ('letter', 'letter', 'orange')],
    captions={
        'cnt = 0': '`cnt` 用来统计 `{letter!r}` 出现的次数，从 0 开始',
        'for char in s': '取下一个字符 `char = {char!r}`',
        'if char == letter': lambda S, B, r: (f"`{S.char!r} == {S.letter!r}` → ==是目标字母==" if S.char == S.letter else f"`{S.char!r} ≠ {S.letter!r}` → 跳过"),
        'cnt += 1': '计数加一：`cnt = {cnt}`',
        'return': '一共 `{cnt}` 个，`{cnt} × 100 // {len(s)}` = =={cnt * 100 // len(s)}==（先乘 100 再整除，向下取整）',
    },
    cards=dict(
        one_liner='一趟遍历数出个数，乘 100 再除以长度',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['返回 `s` 中等于 `letter` 的字符所占百分比，==向下取整==',
                 '示例：`s = "foobar"`，`letter = "o"` → `33`',
                 '本视频：`s = "foobarbaz"`，`letter = "o"` → `22`'],
        quote='一趟遍历统计指定字母出现的次数，然后乘以100后除以字符串的长度就是百分比了。',
        quote_src='—— yiduobo 题解原文',
        idea=['手写循环：遇到 `letter` 就 `cnt += 1`',
              '循环结束后 `cnt * 100` 除以 `len(s)` 就是百分比'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，最后的 `/` 是整数除法，已改为 `//`',
                 '易错：要向下取整，Python 3 的 `/` 会得到小数',
                 '对比灵神：他直接用 `s.count(letter)` 一行完成统计'],
    ),
)
