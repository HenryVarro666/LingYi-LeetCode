W = ['abca', 'aabb']
TG = 'aba'
M = len(W[0])


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') not in (15, 17, 19, 20, 21):
        return None
    if r == i and c == j:
        return 'yellow'
    if S.get('_line') in (19, 21):
        if (r, c) == (i, j - 1):
            return 'blue'
        if i > 0 and (r, c) == (i - 1, j - 1):
            return 'green'
    return None


def _info(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 14:
        c = S.get('cnt_list')
        return '`cnt_list[j][ch]`：words 第 j 列上字母 ch 出现的次数' if c is None else '预处理好每一列的字母计数；接着算 `f[i][j]`'
    ch = S['char']
    k = S['cnt_list'][j].get(ch, 0)
    return f"`target[{i}] = {ch}`，第 {j} 列里 `{ch}` 有 `{k}` 个：`cnt_list[{j}][{ch}] = {k}`"


CONFIG = dict(
    num=1639, title='通过给定词典构造目标字符串的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前 i 个字符 × 前 j 列 的线性 DP',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numWays(self, words, target):

        m = len(words[0])
        n = len(target)
        cnt_list = [{} for _ in range(m)]
        for word in words:
            for index, char in enumerate(word):
                cnt_list[index][char] = cnt_list[index].get(char, 0) + 1
        
        mod = 10 ** 9 + 7
        f = [[0] * m for _ in range(n)]
        for i, char in enumerate(target):
            for j in range(m):
                if i == 0:
                    if j == 0:
                        f[i][j] = cnt_list[0].get(char, 0)
                    else:
                        f[i][j] = f[i][j - 1] + cnt_list[j].get(char, 0)
                elif i <= j:
                    f[i][j] = (f[i][j - 1] + f[i - 1][j - 1] * cnt_list[j].get(char, 0)) % mod

        return f[-1][-1]
''',
    call=f'Solution().numWays({W!r}, {TG!r})',
    expect=5,
    skip=['if i == 0', 'for word in words', 'for index, char', 'for j in range', 'm = len', 'n = len', 'mod =', 'else:', 'if j == 0'],
    max_steps=80,
    views=[
        dict(type='array', var=lambda S: S.get('words'), label='words（每个单词的第 j 位 = 第 j 列）', h=140, cell=100),
        dict(type='string', var='target', label='target（i 指向正在构造的字符）', h=150, cell=70, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') and S.get('_line', 0) >= 14 else None),
        dict(type='text', fn=_info, size=24, h=80),
        dict(type='table', var='f', label='f[i][j]：用前 j+1 列构造 target[:i+1] 的方案数（黄 = 正在算）', h=300, cell=90,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(TG)], cols=lambda S: [f'列{k}' for k in range(M)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('char', 'char', 'blue'), ('f[i][j]', 'f[i][j]', 'green')],
    captions={
        'cnt_list = [{}': '先对 `words` 预处理：每一列一个字典，统计各字母出现次数 `cnt_list[j]`',
        'cnt_list[index][char] =': '第 `{index}` 列字母 `{char}` 的计数 +1',
        'f = [[0]': '`f[i][j]`：`target` 前 `i+1` 个字符，用 words 的前 `j+1` 列构造，有多少方案；初始全是 0',
        'f[i][j] = cnt_list[0]': '`i = 0, j = 0`：只能用第 0 列选 `{char}`，有 `cnt_list[0][{char}]` = =={f[i][j]}== 种',
        'f[i][j] = f[i][j - 1] + cnt': '`i = 0`：`{char}` 要么在前面的列选了 `f[0][{j-1}] = {f[i][j-1]}`，要么就在第 `{j}` 列选（{cnt_list[j].get(char, 0)} 种）→ =={f[i][j]}==',
        'elif i <= j': lambda S, B, r: (f'`i = {S.i} <= j = {S.j}`：前 {S.j + 1} 列够选出 {S.i + 1} 个字符，才可能有方案' if S.i <= S.j else
                                         f'`i = {S.i} > j = {S.j}`：要选 {S.i + 1} 个字符，却只有 {S.j + 1} 列 → 不可能，保持 0'),
        'f[i][j] = (f[i][j - 1] +': '两种情况相加：不用第 `{j}` 列 `f[{i}][{j-1}] = {f[i][j-1]}`；用第 `{j}` 列选 `{char}`：`f[{i-1}][{j-1}] × cnt = {f[i-1][j-1]} × {cnt_list[j].get(char, 0)}` → `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[-1][-1]': '答案：`target` 全部构造完、用满所有列：`f[-1][-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='用过第 k 列，前 k 列就不能再用 → 前 i 个字符 × 前 j 列',
        complexity='时间 `O(m·n + 总字符数)`，空间 `O(m·n)`',
        problem=['`words` 里每个单词长度相同；从中构造 `target`',
                 '选 `target[i]` 时，可用任一单词的第 `k` 个字母（等于它）；用过第 `k` 列，==前 `k` 列都不能再用==',
                 '求构造方案数，结果对 `10^9+7` 取模',
                 '示例：`words=["acca","bbbb","caca"], target="aba"` → `6`；视频里用 `["abca","aabb"], "aba"` → `5`'],
        quote='题目非常贴心地设定了一旦用过第k列上的字符，前k列的字符就不能再用了这样一个规则，那么摆明了就是前i前j这种形式的动态规划。',
        quote_src='—— yiduobo 题解',
        idea=['先预处理：每列各字母出现多少次，记 `cnt_list`',
              '`f[i][j]`：`target` 前 `i` 个字符、用 `words` 前 `j` 列构造的方案数',
              '`i = 0`：在第 `j` 列选，或在更早的列选 → 累加',
              '`i > 0`：`i > j` 时列不够，为 0；否则 `f[i][j-1]` + `f[i-1][j-1]` × 第 j 列的个数'],
        summary=['时间 `O(m·n)` 填表，预处理 `O(总字符数)`',
                 '易错：乘法要取模 `% mod`；`i = 0` 那行的累加没取模（这份代码如此）',
                 '易错：`i > j` 的格子保持 0，不能参与转移',
                 '第 `i` 行只依赖第 `i-1` 行，可以滚动数组'],
    ),
)
