
def _txt(S):
    if 'l' not in S or 'index' not in S or S.get('_line') != 9:
        return '`f` 存的是「最高位在前」的分布：`f[t]` = 恰好看到 `n−t` 根（或当前 `l+1` 根里的 `l+1−t` 根）的排列数'
    f, l, i = S['f'], S['l'], S['index']
    return f'`f[{i}] += f[{i-1}] × {l}` = =={f[i]}==　（插入最短的木棍：放别处 ×{l}，不增加可见数）'


CONFIG = dict(
    num=1866, title='恰有 K 根木棍可以看到的排列数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='插入最短木棍 · 一维滚动',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2333'],
    code='''
class Solution(object):
    def rearrangeSticks(self, n, k):

        f = [1]
        mod = 10 ** 9 + 7
        for l in range(1, n):
            f.append(0)
            for index in range(l, 0, -1):
                f[index] += f[index - 1] * l
                f[index] %= mod
            
        return f[n - k]
''',
    call='Solution().rearrangeSticks(5, 2)',
    expect=50,
    skip=['for index in range', 'f[index] %= mod'],
    views=[
        dict(type='text', fn=_txt, size=26, h=80),
        dict(type='array', var='f', label='f（下标 t = 少看到的根数，f[t] = 方案数）', h=240, cell=110,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('yellow' if i == S.get('index') and S.get('_line') == 9 else
                                    'green' if i == S.get('index', 0) - 1 and S.get('_line') == 9 else None)),
        dict(type='text', fn=lambda S: ('' if 'l' not in S else f'已处理 `{S["l"]}` 根木棍的分布，正在加入第 `{S["l"]+1}` 根（最短的）'), size=26, h=60),
    ],
    watch=[('l', 'l', 'blue'), ('index', 'index', 'pink'), ('n', 'n'), ('k', 'k')],
    captions={
        'f = [1]': '一根木棍只有一种排列、能看到 1 根：`f = [1]`（最高位在前）',
        'mod =': '结果取模 `10^9+7`',
        'for l in range': '`l = {l}`：已有 {l} 根较长的，现在==插入一根最短的==，得到 {l+1} 根的分布',
        'f.append(0)': '末尾补 0：相当于最短的==放最前面==，原分布整体多看到 1 根→ `f = {f}`',
        'f[index] += f[index - 1] * l': lambda S, B, r: (f'`f[{S.index}] += f[{S.index-1}] × {S.l}`：最短的放在{S.l}个非开头位置，'
                                                         f'可见数不变 → `{B.f[S.index]}` + `{B.f[S.index-1]} × {S.l}` = =={S.f[S.index]}=='),
        'f[index] %= mod': '取模（数小时不变）：`f[{index}]` = {f[index]}',
        'return f[n - k]': '倒着存，所以看到 `k` 根对应下标 `n − k = {n-k}`：答案 =={ret}==',
    },
    cards=dict(
        one_liner='往已有排列里插入最短的木棍：放最前多看到一根，放别处看不到',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`1..n` 的木棍排成一排，从左往右看，左边没有更长木棍的才==看得到==',
                 '求恰好看到 `k` 根的排列数，对 `10^9+7` 取余',
                 '示例：`n = 3, k = 2` → `3`；本视频：`n = 5, k = 2` → `50`'],
        quote='考虑新加入一根长度为1的木棍……插入到排列的最前方时，就相当于可以额外多看到一根木棍……插入到其他任何位置，这个1都不可能被看到。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 `n` 较小找规律：`2 3 4` 的排列看到 1/2/3 根的方案是 `2 3 1`',
              '再插入最短的 `1`：放最前 → 分布右移一位；放别处 → 原分布复制 `3` 份',
              '数组倒着存，右移变成「末尾补 0」，再加上 `f[index-1] * l`'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`index` 从大到小，保证用到的 `f[index-1]` 还是旧值',
                 '易错：倒着存，答案在 `f[n - k]` 而不是 `f[k]`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（本题无其他改动）',
                 '对比灵神：他用第一类斯特林数二维表，这里是同一递推压成一维'],
    ),
)
