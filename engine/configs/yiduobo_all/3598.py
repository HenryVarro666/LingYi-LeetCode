def _gl(a, b):
    for k in range(min(len(a), len(b))):
        if a[k] != b[k]:
            return k
    return min(len(a), len(b))


CONFIG = dict(
    num=3598, title='相邻字符串之间的最长公共前缀', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='f / g 预处理 + 前三大',
    tags=['灵神题单', '动态规划', '难度分 1655'],
    code='''
class Solution(object):
    def longestCommonPrefix(self, words):
        
        n = len(words)
        if n == 1:
            return [0]

        f = [0] * n
        g = [0] * n

        def get_length(w1, w2):
            for index in range(min(len(w1), len(w2))):
                if w1[index] != w2[index]:
                    return index
            
            return min(len(w1), len(w2))

        for index in range(1, n):
            f[index] = get_length(words[index - 1], words[index])

            if index > 1:
                g[index] = get_length(words[index - 2], words[index])
        
        first, second, third = 0, 0, 0
        for index in range(1, n):
            if f[index] > first:
                first, second, third = f[index], first, second
            elif f[index] > second:
                second, third = f[index], second
            elif f[index] > third:
                third = f[index]

        res = []
        for index in range(n):
            if index == 0:
                if f[index + 1] == first:
                    res.append(second)
                else:
                    res.append(first)
            
            elif index == n - 1:
                if f[index] == first:
                    res.append(second)
                else:
                    res.append(first)
            
            else:
                if max(f[index], f[index + 1]) == first:
                    if min(f[index], f[index + 1]) == second:
                        res.append(max(third, g[index + 1]))
                    else:
                        res.append(max(second, g[index + 1]))
                else:
                    res.append(max(first, g[index + 1]))
        
        return res
''',
    call="Solution().longestCommonPrefix(['jump','run','run','jump','run'])",
    expect=[3, 0, 0, 3, 3],
    skip=['for index in range(min(len(w1)', 'if w1[index] != w2[index]', 'return index', 'return min(len(w1)', 'def get_length', 'f = [0] * n', 'g = [0] * n', 'n = len(words)'],
    views=[
        dict(type='array', var='words', pointers={'index': 'blue'}, h=215, cell=110, label='words'),
        dict(type='array', var='f', h=185, cell=110, label='f[i]：words[i-1] 与 words[i] 的 LCP'),
        dict(type='array', var='g', h=185, cell=110, label='g[i]：words[i-2] 与 words[i] 的 LCP'),
        dict(type='text', h=70, fn=lambda S: (f"前三大：`first = {S['first']}`，`second = {S['second']}`，`third = {S['third']}`" if 'first' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('first', 'first', 'green'), ('second', 'second', 'orange'), ('third', 'third', 'pink'), ('res', 'res', 'cyan')],
    captions={
        'if n == 1': '只有一个字符串，删掉后没有相邻对 → 直接 `[0]`',
        'for index in range(1, n)': lambda S, B, r: (f'`index = {S.index}`' if 'first' not in S else f'`index = {S.index}`：看 `f[{S.index}] = {S.f[S.index]}` 能不能挤进前三大'),
        'f[index] = get_length': lambda S, B, r: f"`{S.words[S.index-1]}` 与 `{S.words[S.index]}` 的最长公共前缀 `f[{S.index}]` = =={_gl(S.words[S.index-1], S.words[S.index])}==",
        'g[index] = get_length': lambda S, B, r: f"`{S.words[S.index-2]}` 与 `{S.words[S.index]}` 的最长公共前缀 `g[{S.index}]` = =={_gl(S.words[S.index-2], S.words[S.index])}==：删掉中间那个后它们会相邻",
        'first, second, third = 0': '前三大的相邻 LCP 都先设为 0：一次删除可能同时拆掉最大和次大，所以要留到第三',
        'if f[index] > first': '`f[{index}] = {f[index]}` 对比最大 `first = {first}`',
        'first, second, third = f': '成为新的最大：名次依次后移 → `{first}, {second}, {third}`',
        'elif f[index] > second': '`f[{index}] = {f[index]}` 对比次大 `second = {second}`',
        'second, third = f': '成为新的次大：`{second}, {third}`',
        'elif f[index] > third': '`f[{index}] = {f[index]}` 对比第三大 `third = {third}`',
        'third = f[index]': '成为第三大 `{third}`',
        'for index in range(n)': '删除 `words[{index}]`',
        'if index == 0': lambda S, B, r: ('删第一个：只会拆掉 `f[1]`，不会产生新相邻对' if S.index == 0 else ('删最后一个：只会拆掉 `f[n-1]`' if S.index == len(S.words) - 1 else '删中间的：会拆掉 `f[index]` 和 `f[index+1]` 两对，新增 `g[index+1]`')),
        'if f[index + 1] == first': lambda S, B, r: (f"`f[1] = {S.f[1]}` 就是最大值 → 最大被拆掉，用次大 `{S.second}`" if S.f[1] == S.first else f"`f[1] = {S.f[1]}` 不是最大 → 最大还在 `{S.first}`"),
        'elif index == n - 1': lambda S, B, r: ('是最后一个' if S.index == len(S.words) - 1 else '不是最后一个，走中间的情况'),
        'if f[index] == first': lambda S, B, r: (f"`f[{S.index}] = {S.f[S.index]}` 就是最大值 → 最大被拆掉，用次大 `{S.second}`" if S.f[S.index] == S.first else f"`f[{S.index}] = {S.f[S.index]}` 不是最大 → 最大还在 `{S.first}`"),
        'if max(f[index], f[index + 1]) == first': lambda S, B, r: (f"被拆的两对里有最大值 `{S.first}`，还要看次大是否也被拆" if max(S.f[S.index], S.f[S.index+1]) == S.first else f"被拆的两对 `{S.f[S.index]}`、`{S.f[S.index+1]}` 都不是最大 → 最大 `{S.first}` 保留"),
        'if min(f[index], f[index + 1]) == second': lambda S, B, r: (f"另一对 `{min(S.f[S.index], S.f[S.index+1])}` 正是次大 → 最大、次大同时被拆，只剩第三大" if min(S.f[S.index], S.f[S.index+1]) == S.second else f"另一对 `{min(S.f[S.index], S.f[S.index+1])}` 不是次大 → 次大 `{S.second}` 保留"),
        'res.append(max(third': '最大、次大都没了：`max(third, g[{index+1}]) = max({third}, {g[index+1]})` = =={res[-1]}==',
        'res.append(max(second': '次大还在：`max(second, g[{index+1}]) = max({second}, {g[index+1]})` = =={res[-1]}==',
        'res.append(max(first': '最大还在：`max(first, g[{index+1}]) = max({first}, {g[index+1]})` = =={res[-1]}==',
        'res.append(second)': '`res` 加入次大 `{second}`',
        'res.append(first)': '`res` 加入最大 `{first}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='删一个字符串只拆两对、补一对：留住前三大的相邻 LCP 就够了',
        complexity='时间 `O(L)`，空间 `O(n)`',
        problem=['依次删除 `words[index]`，求删除后所有相邻字符串对的最长公共前缀长度的最大值',
                 '没有相邻对或没有公共前缀时为 `0`',
                 '本视频：`["jump","run","run","jump","run"]` → `[3,0,0,3,3]`'],
        quote='选出三个值的理由是一次删除操作中可能会同时移除掉first和second，因此还需要保留一个third。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：`words[i-1]` 与 `words[i]` 的 LCP；`g[i]`：`words[i-2]` 与 `words[i]` 的 LCP',
              '删 `index`：`f[index]`、`f[index+1]` 两对消失，新增 `g[index+1]` 一对',
              '从 `f` 里选出前三大 `first/second/third`，分三种情况取剩下的最大值'],
        summary=['时间 `O(L)`，空间 `O(n)`（`f`、`g` 两个数组）',
                 '三种情况：最大没被拆 / 只拆最大 / 最大次大同时被拆（用 `third`）',
                 '首尾元素要单独处理：它们没有 `g`，删掉只拆一对',
                 '对比灵神：灵神只维护前二大并证明第三大用不上，yiduobo 稳妥地保留了前三大',
                 '原文本身就是 Python 3 可运行的写法，未做修改'],
    ),
)
