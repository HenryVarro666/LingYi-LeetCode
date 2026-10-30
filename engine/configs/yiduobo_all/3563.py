S0 = 'bcdaxe'


def _fc(S, r, c, v):
    st, en = S.get('start'), S.get('end')
    if st is not None and en is not None and r == st and c == en and S.get('_line', 0) < 30 and en < len(S0):
        return 'yellow'
    return 'green' if v is True else None


def _gc(S, k, v):
    return 'yellow' if k == S.get('index') and S.get('_line', 0) >= 30 else None


def _cons(S):
    return abs(ord(S['s'][S['start']]) - ord(S['s'][S['end']]))


CONFIG = dict(
    num=3563, title='移除相邻字符后字典序最小的字符串', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP 判可删 + 后缀 DP 取最小',
    tags=['灵神题单', '动态规划', '难度分 2585'],
    code='''
class Solution(object):
    def lexicographicallySmallestString(self, s):
        
        n = len(s)
        f = [[None] * n for _ in range(n)]
        for length in range(2, n + 1, 2):
            for start in range(n):
                end = start + length - 1
                if end >= n:
                    break
                
                diff = abs(ord(s[start]) - ord(s[end]))
                if length == 2:
                    if diff == 1 or diff == 25:
                        f[start][end] = True
                    else:
                        f[start][end] = False
                
                else:
                    f[start][end] = False

                    if (diff == 1 or diff == 25) and f[start + 1][end - 1]:
                        f[start][end] = True
                    else:
                        for cut_pos in range(start + 1, end, 2):
                            if f[start][cut_pos] and f[cut_pos + 1][end]:
                                f[start][end] = True
                                break
                    
        g = [""] * (n + 1)
        for index in range(n - 1, -1, -1):
            g[index] = s[index] + g[index + 1]
            for cut_pos in range(index + 1, n, 2):
                if f[index][cut_pos]:
                    g[index] = min(g[index], g[cut_pos + 1])

        return g[0]
''',
    call=f'Solution().lexicographicallySmallestString({S0!r})',
    expect='baxe',
    skip=['n = len(s)', 'for start in range', 'for cut_pos in range', 'break', 'else:', 'if end >= n', 'if length == 2', 'if diff == 1 or diff == 25:', 'end = start'],
    views=[
        dict(type='string', var='s', label='s（蓝 = start / index，粉 = end）', h=215, cell=80,
             pointers={'start': 'blue', 'end': 'pink'}),
        dict(type='table', var='f', label='f[start][end]：s[start..end] 能否移除（绿 = 能，黄 = 正在算）', h=320, cell=54,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_fc, values=False),
        dict(type='array', var='g', label='g[index]：后缀 s[index:] 的最小字典序字符串', h=190, cell=110,
             pointers={'index': 'blue'}, color=_gc),
    ],
    watch=[('length', 'length', 'orange'), ('start', 'start', 'blue'), ('end', 'end', 'pink'), ('index', 'index', 'blue')],
    captions={
        'f = [[None]': '`f[start][end]`：`s[start..end]` 能否移除，先留空',
        'for length in range': lambda S, B, r: (f'`length = {S.length}`：==先短后长==，算长区间前，短区间必须已经算好；长度必为偶数'
                                                if S.get('length') != B.get('length') else '各种长度都算完了'),
        'end = start': '`end = start + length - 1 = {end}`',
        'diff = abs': lambda S, B, r: f'区间 `[{S.start}, {S.end}]`：两端 `{S.s[S.start]}`、`{S.s[S.end]}` 的 ASCII 差 `diff = {S.diff}`' + ('，==连续==' if S.diff in (1, 25) else '，不连续（差 1 或 25 才算）'),
        'if length == 2': '区间长度 `{length}`：' + '两个字符直接相邻，只看它们是否连续',
        'if diff == 1 or diff == 25': lambda S, B, r: ('`diff = %d`' % S.diff) + (' → 连续' if S.diff in (1, 25) else ' → 不连续'),
        'f[start][end] = True': '`f[{start}][{end}] = True`：==可以移除==',
        'f[start][end] = False': lambda S, B, r: (f'两个字符不连续：`f[{S.start}][{S.end}] = False`' if S.length == 2 else f'先假定 `f[{S.start}][{S.end}] = False`，下面再找能移除的理由'),
        'if (diff == 1': lambda S, B, r: (f'第一种：两端 `{S.diff}` ' + ('连续' if S.diff in (1, 25) else '不连续') + f'，且中间 `f[{S.start+1}][{S.end-1}]` = {S.f[S.start+1][S.end-1]}'
                                         + (' → 两端配对移除' if S.diff in (1, 25) and S.f[S.start + 1][S.end - 1] else ' → 不成立，试试切成两段')),
        'if f[start][cut_pos]': '第二种：在 `cut_pos={cut_pos}` 切开，`f[{start}][{cut_pos}]` = {f[start][cut_pos]}，`f[{cut_pos+1}][{end}]` = {f[cut_pos+1][end]}',
        'g = [': '`g[index]` = 后缀 `s[index:]` 的最小串，`g[n]` 是空串',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：==倒序==，越靠前的位置对字典序影响越大'
                                               if S.get('index') != B.get('index') or S.index != 0 or S.g[0] == '' else '后缀全算完，答案是 `g[0]`'),
        'g[index] = s[index] + g[index + 1]': '方案一：保留 `s[{index}]`，`g[{index}]` = `{s[index]!r}` + `g[{index+1}]` = =={g[index]!r}==',
        'if f[index][cut_pos]': lambda S, B, r: (f'方案二：`s[{S.index}..{S.cut_pos}]` ' + ('==可移除==，剩下 `g[%d]`' % (S.cut_pos + 1) if S.f[S.index][S.cut_pos] else '不可移除，跳过')),
        'g[index] = min': '移除后剩 `g[{cut_pos+1}]` = {g[cut_pos+1]!r}，和保留方案取小：`g[{index}]` = =={g[index]!r}==',
        'return g[0]': '最终答案 `g[0]` = =={ret!r}==',
    },
    cards=dict(
        one_liner='先用区间 DP 判断哪段能删光，再倒着选「留」或「删」',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['每次删掉一对相邻且连续的字符（字母表相邻，`a` 和 `z` 也算），可以操作任意次',
                 '问能得到的==字典序最小==的字符串；样例 3 说明并非都该删',
                 '本视频：`"bcdaxe"` → `"baxe"`'],
        quote='越靠前的位置对字典序的影响越大，这一点与基数排序需要从低位到高位执行时一个道理。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[start][end]`：区间能否删光。两端连续且中间能删光，或能切成两段都能删光',
              '实现上==枚举区间长度==，再枚举起点，保证短区间先算',
              '`g[index]`：倒序计算；保留 `s[index]`，或删掉 `s[index..cut_pos]` 接 `g[cut_pos+1]`'],
        summary=['时间 `O(n^3)`，空间 `O(n^2)`',
                 '`length` 从 2 起、步长 2：能删光的区间长度必为偶数',
                 '`g` 要倒序：只有后缀已知，前面的选择才能比较',
                 '原文已是可直接运行的写法，代码未做修改',
                 '对比灵神：灵神把「删光」类比括号匹配，yiduobo 先枚举长度再推导'],
    ),
)
