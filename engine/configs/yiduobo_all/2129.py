CONFIG = dict(
    num=2129, title='将标题首字母大写', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 空格下标差判断词长',
    tags=[],
    code='''
class Solution(object):
    def capitalizeTitle(self, title):

        res = []
        last = -1
        for index, char in enumerate(title):
            if char >= 'A' and char <= 'Z':
                char = chr(ord(char) + 32)
            res.append(char)
            if char == ' ':
                if index - last > 3:
                    res[last + 1] = chr(ord(res[last + 1]) - 32)
                last = index
        
        index += 1
        if index - last > 3:
            res[last + 1] = chr(ord(res[last + 1]) - 32)

        return ''.join(res)
''',
    call='Solution().capitalizeTitle("i lOVe")',
    expect='i Love',
    views=[
        dict(type='string', var='title', label='title（蓝 = index 当前字符，粉 = last 上一个空格）', cell=90, pointers={'index': 'blue', 'last': 'pink'}, h=210,
             dim=lambda S, i, v: False),
        dict(type='string', var=lambda S: ''.join(S['res']) if 'res' in S else '', label='res（已经转小写、可能已把首字母改大写）', cell=90,
             pointers={'len(res)-1': 'green'}, pointer_labels={'len(res)-1': 'end'}, h=210),
        dict(type='text', fn=lambda S: (f"`index - last` = {S['index'] - S['last']}：中间的单词长 `{S['index'] - S['last'] - 1}`" if 'index' in S and 'last' in S and S['_line'] in (11, 16) else '词长 = 相邻空格下标之差 − 1，只需长度 `>= 3` 时把首字母 −32 变大写'), size=24),
    ],
    watch=[('index', 'index', 'blue'), ('last', 'last', 'pink'), ('char', 'char', 'yellow')],
    captions={
        'res = []': '`res` 存放答案的每个字符',
        'last = -1': '`last` = 上一个空格的位置，初始 -1（第一个单词从下标 0 开始）',
        'for index, char in enumerate': lambda S, B, ret: (f"取下标 `index = {S.index}` 的字符 `'{S.char}'`" if 'index' not in B or S.index != B.index else '遍历结束，所有字符都放进 `res` 了'),
        "if char >= 'A'": lambda S, B, ret: (f"`'{S.char}'` 是大写字母 → 先统一转成小写" if 'A' <= S.char <= 'Z' else f"`'{S.char}'` 不是大写字母，不用转"),
        'char = chr': "`ord + 32` 把大写变小写，`char` 现在是 `'{char}'`",
        'res.append(char)': '不管是什么字符都先放进 `res`：`res` = `{"".join(res)}`',
        "if char == ' '": lambda S, B, ret: ("遇到空格：一个单词刚好结束，该检查它的长度了" if S.char == ' ' else f"`'{S.char}'` 不是空格，继续往后扫"),
        'if index - last > 3': lambda S, B, ret: (f'`{S.index} - {S.last} = {S.index - S.last} > 3` → 词长 `{S.index - S.last - 1}` >= 3，首字母要大写' if S.index - S.last > 3
                                                  else f'`{S.index} - {S.last} = {S.index - S.last}` 不大于 3 → 词长只有 `{S.index - S.last - 1}`，保持小写'),
        'res[last + 1] = chr(ord(res[last + 1]) - 32)': '首字母下标是 `last + 1 = {last + 1}`，`ord - 32` 变大写 → `res` = `{"".join(res)}`',
        'last = index': '`last` 更新为这个空格的位置 `{last}`',
        'index += 1': '==最后一个单词后面没有空格==：让 `index` 指到字符串末尾之后 `{index}`，当作有个虚拟空格',
        'return': '`res` 拼成字符串返回：`{ret}`',
    },
    cards=dict(
        one_liner='用相邻空格的下标之差，一趟遍历就知道词长',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`title` 由单个空格隔开的单词组成',
                 '词长 1 或 2：全小写；否则==首字母大写、其余小写==',
                 '示例：`"First leTTeR of EACH Word"` → `"First Letter of Each Word"`；本视频：`"i lOVe"` → `"i Love"`'],
        quote='注意到题目保证了单词间仅有一个空格连接，那么完全可以通过相邻空格的下标之差来判断空格之间单词的长度，同时可以通过上一个空格的下标得到该单词首字母在答案中的下标，此时就得到了一种只需一趟遍历的做法。',
        quote_src='—— yiduobo 题解原文',
        idea=['`last` 记上一个空格，扫到下一个空格时，`index - last > 3` 就说明词长 >= 3',
              '字符先全部转小写放进 `res`，长词的首字母下标就是 `last + 1`，再减 32 变大写',
              '最后一个单词后面没有空格，循环结束后要再判断一次'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：==遍历完后别漏掉最后一个单词==，用 `index += 1` 当作虚拟空格',
                 '`index - last > 3` 等价于词长 >= 3（两空格之间字符数 = 差 − 1）',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串，其余代码未改',
                 '对比灵神：他用 `split` + `title()` + `join`，yiduobo 手工按下标一趟完成'],
    ),
)
