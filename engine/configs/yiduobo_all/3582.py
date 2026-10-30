CONFIG = dict(
    num=3582, title='为视频标题生成标签', difficulty='Easy', category='字符串',
    author='yiduobo', technique='模拟 · 逐字符拼接到 100 位',
    tags=[],
    setup='''
lower = str.lower
upper = str.upper
''',
    code='''
class Solution(object):
    def generateTag(self, caption):
        
        res = ['#']
        for word in caption.split():
            for index, char in enumerate(word):
                if index == 0:
                    if len(res) == 1:
                        res.append(lower(char))
                    else:
                        res.append(upper(char))
                else:
                    res.append(lower(char))

                if len(res) == 100:
                    break
            
            if len(res) == 100:
                break
        
        return ''.join(res)
''',
    call="Solution().generateTag('go Big NOW')",
    expect='#goBigNow',
    views=[
        dict(type='string', var='caption', label='caption', cell=64, h=160),
        dict(type='text', size=28, h=110, fn=lambda S: (
            f"第 `{S['word_i']}` 个单词 ==`{S['word']}`==，当前字符 `index = {S['index']}`：`'{S['char']}'`" if 'char' in S and 'word' in S and 'word_i' in S
            else (f"当前单词 ==`{S['word']}`==" if 'word' in S else '先 `split()` 分出单词，再逐字符放进 `res`'))),
        dict(type='array', var='res', label='res（字符列表，长度到 100 就停）', cell=60, h=200, color=lambda S, i, v: 'green' if i == len(S['res']) - 1 and len(S['res']) > 1 else None),
    ],
    watch=[('word', 'word', 'blue'), ('index', 'index', 'pink'), ('char', 'char'), ('len(res)', 'len(res)', 'green')],
    captions={
        "res = ['#']": '`res` 先放入 `#`，所以此时长度为 1',
        'for word in caption.split()': lambda S, B, r: (f"取下一个单词 `{S.word}`" if S.get('word') != B.get('word') or 'word' not in B else '单词都处理完了'),
        'for index, char in enumerate(word)': lambda S, B, r: (f"处理 `{S.word}` 的第 {S.index} 个字符 `'{S.char}'`" if S.get('index') != B.get('index') or S.get('char') != B.get('char') or 'index' not in B
                                                              else f"单词 `{S.word}` 处理完了"),
        'if index == 0': lambda S, B, r: ('`index == 0`：这是单词的首字母' if S.index == 0 else '`index != 0`：不是首字母，一律小写'),
        'if len(res) == 1:': lambda S, B, r: ('`len(res) == 1`：还只有 `#`，说明是==第一个单词==，首字母保持小写' if len(S.res) == 1
                                             else f'`len(res) = {len(S.res)}`：不是第一个单词，首字母要==大写=='),
        'res.append(lower(char))': "放入小写 `'{res[-1]}'`，`len(res) = {len(res)}`",
        'res.append(upper(char))': "放入大写 `'{res[-1]}'`，`len(res) = {len(res)}`",
        'if len(res) == 100:': '`len(res) = {len(res)}`：还没到 100，继续',
        'break': '长度到 100 了，不再添加',
        "return ''.join(res)": '把 `res` 拼成字符串：=={ret}==',
    },
    max_steps=100,
    cards=dict(
        one_liner='逐个字符放进答案，只在单词首字母处决定大小写',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把标题 `caption` 变成视频标签：单词连成驼峰，前面加 `#`，最长 100 个字符',
                 '除第一个单词外，每个单词首字母大写、其余小写',
                 '本视频：`"go Big NOW"` → `"#goBigNow"`'],
        quote='题目保证caption中没有空格以外的其他非英文字母的字符，因此可以直接通过split分离其中的单词，接下来初始化答案字符串为\'#\'，然后遍历这些单词，将其中的字符逐个添加到答案字符串中，直到遍历完所有的单词或者答案字符串的长度到达100。',
        quote_src='—— yiduobo 题解原文',
        idea=['`caption` 只有字母和空格，`split()` 就能拿到所有单词',
              '`res` 一开始只有 `#`：`len(res) == 1` 说明还在第一个单词',
              '单词首字母：第一个单词小写，其余大写；非首字母一律小写',
              '长度到 100 立刻 `break` 两层循环'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文用到了 `lower(char)` / `upper(char)`，Python 中并不存在这两个函数；这里在 `setup` 里补上 `lower = str.lower`、`upper = str.upper`，作者代码一字未改',
                 '易错：要跳出两层循环，所以内外层各判断一次 `len(res) == 100`',
                 '判断“是不是第一个单词”靠 `len(res) == 1`，因为 `#` 已占一位'],
    ),
)
