CONFIG = dict(
    num=2788, title='按分隔符拆分字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='split 后过滤空串',
    tags=[],
    code='''
class Solution(object):
    def splitWordsBySeparator(self, words, separator):

        res = []
        for w in words:
            for part in w.split(separator):
                if part:
                    res.append(part)
        
        return res
''',
    call='Solution().splitWordsBySeparator(["a.b.c", "d..e", ".f"], ".")',
    expect=['a', 'b', 'c', 'd', 'e', 'f'],
    views=[
        dict(type='text', fn=lambda S: f"分隔符 `separator = '{S['separator']}'`" + (f"　　当前单词 `w = \"{S['w']}\"`" if 'w' in S else ''), size=26),
        dict(type='text', fn=lambda S: (f"`\"{S['w']}\".split('{S['separator']}')` = `{S['w'].split(S['separator'])}`" if 'w' in S else ''), size=24),
        dict(type='array', var='words', label='words', cell=100,
             color=lambda S, i, v: 'blue' if S.get('w') == v else None),
        dict(type='array', var='res', label='res（只收非空片段）', cell=84, color=lambda S, i, v: 'green'),
    ],
    watch=[('w', 'w', 'blue'), ('part', 'part'), ('len(res)', 'len(res)', 'green')],
    captions={
        'res = []': '`res` 存放所有拆出来的非空片段',
        'for w in words': '处理单词 `w = "{w}"`',
        'for part in w.split': '`"{w}".split("{separator}")` 得到 `{w.split(separator)}`，逐个看每个片段 `part = "{part}"`',
        'if part': lambda S, B, r: (f'`part = "{S.part}"` 非空 → 保留' if S.part else '`part` 是空串（连续分隔符或首尾分隔符留下的）→ ==丢弃=='),
        'res.append(part)': '加入答案：`res = {res}`',
        'return res': '全部单词处理完，返回 `{ret}`',
    },
    cards=dict(
        one_liner='每个单词先 split，再把非空片段依次放进答案',
        complexity='时间 `O(L)`，空间 `O(L)`，`L` 为所有字符总数',
        problem=['给字符串数组 `words` 和一个分隔符 `separator`',
                 '把每个单词按分隔符拆开，==丢掉空字符串==，保持原顺序',
                 '本视频：`["a.b.c","d..e",".f"]`，分隔符 `.` → `[a,b,c,d,e,f]`'],
        quote='有原生split函数的语言可以直接通过split分割每个单词，然后将不为空的部分依次加入到答案数组中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['Python 有现成的 `split`，直接拆每个单词',
              '`d..e` 和 `.f` 会拆出空串，所以用 `if part` 过滤',
              '没有 split 的语言：用 p、q 两指针找分隔符，截取 `p..q-1`'],
        summary=['时间 `O(L)`，空间 `O(L)`',
                 '易错：必须过滤空串，首尾或连续分隔符会产生 `""`',
                 '原文为 Python 2 风格，在 Python 3 下可直接运行，未做修改'],
    ),
)
