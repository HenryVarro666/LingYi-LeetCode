CONFIG = dict(
    num=2942, title='查找包含给定字符的单词', difficulty='Easy', category='字符串',
    author='yiduobo', technique='遍历 · find 判断',
    code='''
class Solution(object):
    def findWordsContaining(self, words, x):

        res = []
        for i, w in enumerate(words):
            if w.find(x) != -1:
                res.append(i)
        
        return res
''',
    call='Solution().findWordsContaining(["abc","bcd","aaaa","cbc"], "a")',
    expect=[0, 2],
    views=[
        dict(type='array', var='words', label='words（蓝箭头 = i，绿 = 已确定包含 x）', pointers={'i': 'blue'}, cell=170,
             color=lambda S, i, v: 'green' if i in S['res'] else ('blue' if i == S.get('i') else None), h=230),
        dict(type='text', fn=lambda S: f"`res` = =={S['res']}==", h=80),
    ],
    watch=['x', 'i', 'w', ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 保存包含 `x` 的单词下标',
        'for i, w in enumerate': '看第 `{i}` 个单词 `{w}`',
        'if w.find(x) != -1': lambda S, B, r: (f"`'{S.w}'.find('{S.x}')` = {S.w.find(S.x)}，不是 -1 → ==包含=="
                                               if S.w.find(S.x) != -1 else f"`'{S.w}'.find('{S.x}')` = -1 → 不包含，跳过"),
        'res.append(i)': '记下下标 `{i}`：`res` = =={res}==',
        'return res': '遍历结束，返回 ==`{res}`==',
    },
    cards=dict(
        after=[dict(heading='find 的返回值', lines=['`w.find(x)` 返回 `x` 第一次出现的下标', '找不到返回 `-1`，所以用 `!= -1` 判断', '下标 `0` 也算找到，不能写成 `> 0`']),],
        one_liner='一趟遍历，find 不是 -1 就记下',
        complexity='时间 `O(L)`，空间 `O(1)`',
        problem=['给字符串数组 `words` 和字符 `x`，返回包含 `x` 的单词下标',
                 '示例：`["abc","bcd","aaaa","cbc"]`，`x = "a"` → `[0,2]`'],
        quote='比较基础的题目，一趟遍历，检测每个单词中是否包含指定字符即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每个单词 `w`', '`w.find(x)` 找不到返回 `-1`，不是 `-1` 就说明包含', '包含则把下标 `i` 追加到 `res`'],
        summary=['时间 `O(L)`，空间 `O(1)`', '`find` 返回 -1 表示没找到，不要写成 `> 0`（下标 0 也算找到）',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
