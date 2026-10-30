def _cnt_txt(S):
    q, w = S.get('query'), S.get('word')
    if q is None or w is None:
        return '两两枚举 query 和 word，统计不同字母数 `cnt`'
    i = S.get('index', -1)
    return f"`{q}` 对 `{w}`：不同字母 `cnt` = =={S.get('cnt', 0)}=="


CONFIG = dict(
    num=2452, title='距离字典两次编辑以内的单词', difficulty='Medium', category='字符串',
    author='yiduobo', technique='暴力枚举 · 逐位计数提前退出',
    tags=[],
    code='''
class Solution(object):
    def twoEditWords(self, queries, dictionary):

        res = []
        for query in queries:
            flag = False
            for word in dictionary:
                cnt = 0
                for index in range(len(query)):
                    if query[index] != word[index]:
                        cnt += 1
                    if cnt > 2:
                        break
                
                if cnt <= 2:
                    flag = True
                    break
            
            if flag:
                res.append(query)
        
        return res
''',
    call='Solution().twoEditWords(["cat","dog","ant"], ["car","bug"])',
    expect=["cat", "dog"],
    views=[
        dict(type='text', fn=_cnt_txt, size=28, h=80),
        dict(type='string', var='query', label='query', cell=110, h=170, pointers={'index': 'blue'},
             color=lambda S, i, v: (None if S.get('index') is None else 'blue' if i == S['index'] and S['_line'] == 9 else ('pink' if S['word'][i] != v else 'green') if i <= S['index'] else None)),
        dict(type='string', var='word', label='word（和 query 对应位置比）', cell=110, h=170, pointers={'index': 'blue'}),
        dict(type='array', var='res', label='res', cell=130, h=150, color=lambda S, i, v: 'green'),
    ],
    watch=[('query', 'query', 'blue'), ('word', 'word', 'pink'), ('cnt', 'cnt', 'orange'), ('flag', 'flag'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 保存满足条件的 query',
        'for query in queries': lambda S, B, r: ('queries 全部处理完' if S.query == B.get('query') else f'取下一个 `query = {S.query!r}`'),
        'flag = False': '`flag` 记录：这个 query 是否已在字典里找到 ≤ 2 处不同的单词',
        'for word in dictionary': lambda S, B, r: ('字典看完了，没有合适的单词' if S.word == B.get('word') and S.word == S.dictionary[-1] else f'和字典里的 `word = {S.word!r}` 比较'),
        'cnt = 0': '不同字母数清零',
        'for index in range': lambda S, B, r: ('三位都比完了' if S.index == B.get('index') and S.index == len(S.query) - 1 else f'比较下标 `{S.index}`'),
        'if query[index] != word[index]': lambda S, B, r: (
            f"`{S.query[S.index]!r} ≠ {S.word[S.index]!r}` → 这一位要改" if S.query[S.index] != S.word[S.index]
            else f"`{S.query[S.index]!r} == {S.word[S.index]!r}` → 这一位相同"),
        'cnt += 1': '又多一处不同：`cnt = {cnt}`',
        'if cnt > 2': lambda S, B, r: (f'`cnt = {S.cnt} > 2`：已经超过两次编辑，==不用再比后面了==' if S.cnt > 2
                                       else f'`cnt = {S.cnt}` 还没超过 2，继续'),
        'break': '提前跳出逐位比较',
        'if cnt <= 2': lambda S, B, r: (f'`cnt = {S.cnt} ≤ 2` → 两次编辑内能变成 `{S.word}`' if S.cnt <= 2
                                        else f'`cnt = {S.cnt} > 2` → 这个 word 不行，看字典下一个'),
        'flag = True': '找到了：`{query!r}` 能行',
        'if flag': lambda S, B, r: ('`flag` 为真 → 这个 query 入答案' if S.flag else '`flag` 为假：字典里没有合适的单词 → 不入答案'),
        'res.append(query)': '`res = {res}`',
        'return res': '返回 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='两两枚举单词对，数不同字母，不超过 2 个就算',
        complexity='时间 `O(q·d·n)`，空间 `O(1)`（返回值不计）',
        problem=['一次编辑可把 query 的一个字母改成任意字母',
                 '求能在 ==不超过两次编辑== 内变成字典中某个单词的 query，保持原顺序',
                 '本视频：`["cat","dog","ant"]`，字典 `["car","bug"]` → `["cat","dog"]`'],
        quote='数据规模较小，直接暴力枚举然后比较是完全可行的。两两枚举queries和dictionary中的单词对，统计其中不同字母的数目。若不超过两个，那么这个query对应的答案就是true。',
        quote_src='—— yiduobo 题解原文',
        idea=['没有更巧的办法，数据小就 ==暴力==',
              '用 `cnt` 统计一对单词不同的位置数，超过 2 就 `break` 省时间',
              '用 `flag` 标记这个 query 是否成功，最后统一加入 `res`'],
        summary=['时间 `O(q·d·n)`，空间 `O(1)`',
                 '`cnt > 2` 立即退出内层循环，是个小优化',
                 '内层 `break` 后还要靠 `cnt <= 2` 判断，不能只看循环是否结束',
                 '原文为 Python 2 风格，仅需空行整理，无其它改动',
                 '对比灵神：灵神用 `sum(...) <= 2` 一行完成，并直接 `append` + `break`'],
    ),
)
