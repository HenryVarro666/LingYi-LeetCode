CONFIG = dict(
    num=792, title='匹配子序列的单词数', difficulty='Medium', category='字符串',
    author='yiduobo', technique='贪心 + 下一位置表',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def numMatchingSubseq(self, S, words):

        n = len(S)
        next_pos = [{S[-1] : n - 1}]
        for index in range(n - 2, -1, -1):
            next_pos.append(next_pos[-1].copy())
            next_pos[-1][S[index]] = index
    
        next_pos.reverse()

        res = 0
        for word in words:
            now = 0
            flag = True
            for char in word:
                if now == n or char not in next_pos[now]:
                    flag = False
                    break
                else:
                    now = next_pos[now][char] + 1
            
            if flag:
                res += 1
        
        return res
''',
    call="Solution().numMatchingSubseq('abcde', ['a', 'bb', 'acd', 'ace'])",
    expect=3,
    views=[
        dict(type='string', var='S', label='S', pointers={'now': 'blue'}, h=170),
        dict(type='text', h=70, size=30,
             fn=lambda S: (f"当前单词：==`{S['word']}`==　正在匹配：`{S['char']}`" if 'char' in S and 'word' in S else
                           (f"当前单词：==`{S['word']}`==" if 'word' in S else ''))),
        dict(type='map', var=lambda S: S['next_pos'][S['now']] if 'now' in S and 'next_pos' in S and S['now'] < len(S['S']) else {},
             label='next_pos[now]：从 now 起每个字母最早出现的下标', fmt=lambda k, v: f"'{k}': {v}", h=140, font=32),
    ],
    watch=[('now', 'now', 'blue'), ('word', 'word', 'pink'), ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'next_pos = [': '最后一位的表：只有 `S[-1]` 出现在下标 `{n-1}`',
        'next_pos.append': '复制右边那一位的表：右边最早出现的位置先继承下来',
        'next_pos[-1][S[index]]': '`{S[index]}` 在 `{index}` 更靠前 → ==覆盖==成 `{index}`',
        'next_pos.reverse': '建表时是从后往前追加的，翻转后 `next_pos[i]` 对应从下标 i 起',
        'now = 0': '新单词：从 `S` 的开头匹配',
        'flag = True': '先假设能匹配',
        'if now == n or': lambda S, B, r: ('`now == n`：S 已用完，后面的字母没处可匹配 → ==失败=='
                                           if S.now == S.n else
                                           (f"`'{S.char}'` 在 `next_pos[{S.now}]` 里" if S.char in S.next_pos[S.now]
                                            else f"`'{S.char}'` 不在 `next_pos[{S.now}]` → 后面再没有它 → ==失败==")),
        'flag = False': '这个单词不是子序列',
        'now = next_pos[now][char] + 1': '贪心：用最靠前的 `{char}`（下标 `{now-1}`），下一个从 `{now}` 开始',
        'res += 1': '整个单词都匹配上了：`res` = {res}',
        'return res': '一共 `{res}` 个单词是 S 的子序列',
    },
    cards=dict(
        one_liner='贪心：每个字母都用最靠前的匹配，查表一跳到位',
        complexity='时间 `O(n·26 + Σ|word|)`，空间 `O(26n)`',
        problem=['给字符串 `S` 和单词列表 `words`',
                 '统计有多少个单词是 `S` 的子序列',
                 '本视频：`S=abcde`，`words=[a,bb,acd,ace]` → `3`'],
        quote='对于B[index]，若A[p]与A[q]都能与之匹配，且p < q，那么若这里选择q能形成最终的完全匹配，那么在这里选择p也必然可以，反过来则不一定。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心：每个字符都尽量用 `S` 里靠前的，给后面留最多的空间',
              '预处理 `next_pos[i]`：从 i 起每个字母最早出现的下标',
              '匹配时不再逐个扫描，而是查表一次跳到下一个位置'],
        summary=['`now = n` 时必须先判断，否则 `next_pos[now]` 会越界',
                 '建表从后往前，后写的覆盖先写的，保证记录的是最早下标',
                 '同一单词用 dict 复制每位的表，空间 `O(26n)`',
                 '原文为 Python 2 风格，代码无需修改'],
    ),
)
