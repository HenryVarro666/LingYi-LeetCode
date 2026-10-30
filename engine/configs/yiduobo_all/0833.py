CONFIG = dict(
    num=833, title='字符串中的查找与替换', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按下标排序后模拟',
    code='''
class Solution(object):
    def findReplaceString(self, S, indexes, sources, targets):

        res = ''
        now = 0
        for pos, source, target in sorted(zip(indexes, sources, targets), key=lambda d:d[0]):
            res += S[now:pos]
            flag = True
            for index, char in enumerate(source):
                if S[pos + index] != char:
                    flag = False
                    break
            
            if flag:
                res += target
                now = pos + index + 1
            else:
                now = pos
        
        res += S[now:]
        return res
''',
    call='Solution().findReplaceString("abcdef", [4, 0, 2], ["ef", "ab", "ec"], ["g", "eee", "ffff"])',
    expect='eeecdg',
    views=[
        dict(type='string', var='S', label='S（蓝 = now，粉 = pos）', cell=84, pointers={'now': 'blue', 'pos': 'pink'}, h=220,
             color=lambda S, k, v: 'green' if 'now' in S and k < S['now'] else None),
        dict(type='text', size=28, h=80, fn=lambda S: f"`res` = ==`{S['res']}`==" if 'res' in S else ''),
        dict(type='text', size=26, h=80, fn=lambda S: (f"当前匹配：`source = {S['source']}`，已比较到第 `{S['index']}` 个字符" if 'index' in S and 'source' in S else '')),
    ],
    watch=['now', 'pos', 'source', ('res', 'res', 'green')],
    captions={
        'res = ': '`res` 保存答案；`now` 表示原串已经处理到哪里',
        'now = 0': '`now = 0`：从头开始',
        'for pos, source, target': lambda S, B, r: (f"按下标从小到大取下一个操作：`pos = {S.pos}`，`source = {S.source}`，`target = {S.target}`" if 'pos' in S and S.pos != B.get('pos', -1) or 'pos' not in B else '所有操作处理完了'),
        'res += S[now:pos]': '`now..pos-1` 这一段不会被替换，原样加入：`S[{now}:{pos}]` → `res = {res}`',
        'flag = True': '先假设 `source` 能匹配上',
        'for index, char': lambda S, B, r: ('`source` 的字符都比完了，没有发现不同' if B.get('index') == S.index == len(S.source) - 1 and S.flag else f"比较第 `{S.index}` 个字符：`S[{S.pos + S.index}] = {S.S[S.pos + S.index]}` 对 `{S.char}`"),
        'if S[pos + index]': lambda S, B, r: (f"`S[{S.pos + S.index}] = {S.S[S.pos + S.index]}` ≠ `{S.char}` → ==不匹配==" if S.S[S.pos + S.index] != S.char else f"`S[{S.pos + S.index}] = {S.char}` 相等，继续比下一个"),
        'flag = False': '有一个字符不同，这次替换作废',
        'break': '直接退出比较',
        'if flag': lambda S, B, r: ('`flag` 为真：整个 `source` 都匹配' if S.flag else '`flag` 为假：不替换'),
        'res += target': '匹配成功：把 `{target}` 加入答案 → `res = {res}`',
        'now = pos + index + 1': '`now` 跳到被替换段之后：`{pos} + {index} + 1 = {now}`',
        'now = pos': '没替换：`now` 回到 `pos = {now}`，这一段稍后当作普通字符加入',
        'res += S[now:]': '最后把 `now` 到末尾的剩余部分加入 → `{res}`',
        'return': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='把操作按下标排序，边走边拼：没替换的原样搬，匹配上的换成 target',
        complexity='时间 `O(k log k + L)`，空间 `O(L)`',
        problem=['给 `S` 和 `k` 组 `(indexes, sources, targets)`：从 `indexes[i]` 起若等于 `sources[i]` 就换成 `targets[i]`',
                 '替换同时发生，互不重叠',
                 '本视频：`abcdef`，`[4,0,2]`，`["ef","ab","ec"]`，`["g","eee","ffff"]` → `eeecdg`'],
        quote='首先将source和target按indexes从小到大进行排序，然后维护一个变量now表示当前处理到S中now这个位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['排好序后，相邻两个 `pos` 之间的字符一定不会被替换，先原样加入',
              '逐字符比较 `source`：全部相同才替换，并把 `now` 移到替换段之后',
              '不匹配时 `now = pos`，这个位置的字符留给下一轮当普通字符加入'],
        summary=['排序后只需一遍扫描，不用修改 `S`',
                 '易错：循环结束后要把 `S[now:]` 的尾巴补上',
                 '`now = pos + index + 1` 依赖 `index` 是 `source` 最后一个下标',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
