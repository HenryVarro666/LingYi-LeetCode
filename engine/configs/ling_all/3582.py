CONFIG = dict(
    num=3582, title='为视频标题生成标签', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='模拟 · title() 驼峰 + 截断',
    tags=[],
    code='''
class Solution:
    def generateTag(self, caption: str) -> str:
        s = caption.title().replace(' ', '')
        if not s:
            return '#'
        return '#' + s[0].lower() + s[1:99]
''',
    call="Solution().generateTag('can I Go There')",
    expect='#canIGoThere',
    views=[
        dict(type='string', var='caption', label='caption', cell=60, h=170),
        dict(type='string', var='s', label='s = title() 去空格：每个单词首字母大写，其余小写', cell=60, h=190,
             color=lambda S, i, v: 'green' if i == 0 else None),
        dict(type='text', size=28, h=120, fn=lambda S: (
            '最终标签 = `#` + ==首字母小写== + `s[1:99]`（总长不超过 100）' if 's' in S else '')),
    ],
    watch=[('s', 's', 'green')],
    captions={
        'caption.title()': "`title()` 让每个单词首字母大写、其余小写，再去掉空格：`s = '{s}'`",
        'if not s': lambda S, B, r: ('`s` 非空，继续' if S.s else '`s` 为空，只有 `#`'),
        "return '#'": "`'#'` + 首字母小写 `'{s[0].lower()}'` + `s[1:99]` = =={ret}==（`#` 占 1 位，所以只取 `s[1:99]`，总长 ≤ 100）",
    },
    cards=dict(
        one_liner='title() 一步搞定大小写，首字母再单独小写',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把标题 `caption` 变成视频标签：单词连成驼峰，前面加 `#`，最长 100 个字符',
                 '除第一个单词外，每个单词首字母大写、其余小写',
                 '示例：`"can I Go There"` → `"#canIGoThere"`'],
        quote='模拟题：把 caption 按照空格，分割成若干个单词。把每个单词的字母全部小写。把除了第一个单词以外的单词，首字母大写。在单词列表前面加个井号。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`str.title()` 恰好是“每个单词首字母大写，其余小写”',
              '去掉空格后，只需把整体的第一个字母改回小写',
              '`#` 占一位，所以 `s[1:99]` 保留 98 个字符，加上 `#` 和首字母共 100'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`caption` 可能以空格开头，先 `title().replace` 再取首字母；全空时只剩 `#`',
                 '切片越界不报错，所以 `s[1:99]` 不用先判断长度',
                 '写法二：`split()` 后第一个单词 `lower()`，其余 `capitalize()`，`join` 后取前 100 个字符'],
    ),
)
