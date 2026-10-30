CONFIG = dict(
    num=1935, title='可以输入的最大单词数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='集合 + 逐词检查',
    tags=[],
    code='''
class Solution(object):
    def canBeTypedWords(self, text, brokenLetters):

        borken_set = set()
        for char in brokenLetters:
            borken_set.add(char)
        
        res = 0
        for word in text.split(' '):
            flag = True
            for char in word:
                if char in borken_set:
                    flag = False
                    break
            
            if flag:
                res += 1
        
        return res
''',
    call="Solution().canBeTypedWords('leet code go', 'lt')",
    expect=2,
    views=[
        dict(type='set', var='borken_set', label='borken_set（损坏的键）', h=150),
        dict(type='text', fn=lambda S: f"当前单词 `{S['word']}`" + ('' if 'flag' not in S else '，能打出' if S['flag'] else '，打不出') if 'word' in S else '', h=70),
    ],
    watch=['word', ('char', 'char', 'blue'), ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    captions={
        'borken_set.add': '坏键 `{char}` 加入集合',
        'flag = True': '先假设 `{word}` 能打出',
        'if char in borken_set': '`{char}` {"在" if char in borken_set else "不在"}坏键集合里 → {"==打不出=="  if char in borken_set else "这个字母没问题"}',
        'flag = False': '`flag = False`',
        'break': '已经确定打不出，==不用再看后面的字母==，直接换下一个单词',
        'if flag': '`flag = {flag}` → {"所有字母都完好，答案加 1" if flag else "这个单词不计数"}',
        'res += 1': '`res` → {res}',
        'return res': '共 `{res}` 个单词能打出',
    },
    cards=dict(
        one_liner='坏键放进集合，每个单词里只要有一个字母在集合里就淘汰',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`brokenLetters` 里的字母键坏了，统计 `text` 中能完整打出的单词数',
                 '示例：`text = "hello world"`，`brokenLetters = "ad"` → `1`',
                 '本视频：`"leet code go"`，坏键 `"lt"` → `2`'],
        quote='对于当前的单词，若某个字母出现在损坏的集合中，那么说明该单词无法被输入，直接考虑下一个单词；若没有字母出现在损坏的集合中，那么就将答案加1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用集合统计损坏的按键', '对每个单词逐字母检查，碰到坏键立刻 `break`', '整个单词没碰到坏键才让答案加 1'],
        summary=['时间 `O(n)`，空间 `O(1)`（集合最多 26 个字母）',
                 '原文变量名 `borken_set` 拼写如此，照搬未改',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：灵神把集合压成位掩码，yiduobo 用 `set`，思路相同'],
    ),
)
