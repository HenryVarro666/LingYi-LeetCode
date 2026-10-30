def _txt(S):
    if 'res' not in S:
        return '先算出 `p[m]`：以某个字母开头、长度为 m 的开心字符串个数'
    return f"已确定 `res` = ==`{S['res']}`==，还需 `n = {S['n']}` 位，当前 `k = {S['k']}`（在剩余范围内排第几）"


def _cand(S, w):
    o = [c for c in 'abc' if c != S.last]
    pick = o[1] if w == '大' else o[0]
    return f'上一位是 `{S.last}`，候选字母是 `{o[0]}`、`{o[1]}`，较{w}的是 ==`{pick}`=='


CONFIG = dict(
    num=1415, title='长度为 n 的开心字符串中字典序第 k 小的字符串', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='按开头分块计数，k 落在哪块就选谁',
    tags=['灵神核心路线', '灵神题单·位运算'],
    code='''
class Solution(object):
    def getHappyString(self, n, k):

        p = [1, 1]
        for index in range(2, n + 1):
            p.append(p[-1] + p[-1])

        last = ''
        if p[n] * 3 < k:
            res = ""
        else:
            if k > p[n] + p[n]:
                res = 'c'
                last = 'c'
                k -= p[n] + p[n]
            elif k > p[n]:
                res = 'b'
                last = 'b'
                k -= p[n]
            else:
                res = 'a'
                last = 'a'

            n -= 1
            while n > 0:
                if k > p[n]:
                    if last == 'c':
                        res += 'b'
                        last = 'b'
                    else:
                        res += 'c'
                        last = 'c'
                    k -= p[n]
                else:
                    if last == 'a':
                        res += 'b'
                        last = 'b'
                    else:
                        res += 'a'
                        last = 'a'
                
                n -= 1
        
        return res
''',
    call='Solution().getHappyString(4, 13)',
    expect='bcab',
    views=[
        dict(type='array', var='p', label='p[m]：以固定字母开头、长度为 m 的开心字符串个数', cell=90, h=200,
             pointers={'n': 'blue'}, pointer_labels={'n': 'n'}),
        dict(type='text', fn=_txt, size=30),
    ],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'pink'), ('last', 'last', 'orange'), ('res', 'res', 'green')],
    skip=['last = ', "res = ''", 'last = \'\''],
    captions={
        'p = [1, 1]': '`p[m]`：开头字母固定、长度为 m 的开心字符串个数。`p[1] = 1`（`p[0]` 占位）',
        'p.append': '`p[{index}] = p[{index}-1] × 2 = {p[-1]}`：上一层每个串后面都有 2 种接法',
        'if p[n] * 3 < k': '共 `3 × p[{n}] = {p[n] * 3}` 个，`k = {k}` 没超过 → 答案存在',
        'if k > p[n] + p[n]': lambda S, B, ret: f'`k = {S.k}` 与三块比较：a 开头 `1~{S.p[S.n]}`，b 开头 `{S.p[S.n] + 1}~{2 * S.p[S.n]}`，c 开头 `{2 * S.p[S.n] + 1}~{3 * S.p[S.n]}`',
        'elif k > p[n]': '`k = {k}` 落在 b 的区间 `{p[n] + 1}~{2 * p[n]}` 吗？',
        'res = \'c\'': 'k 在最后一块 → 首字母是 `c`',
        'res = \'b\'': 'k 在中间一块 → 首字母是 `b`',
        'res = \'a\'': 'k 在第一块 → 首字母是 `a`',
        'k -= p[n] + p[n]': '去掉前两块：`k` → {k}',
        'k -= p[n]\n': '去掉前一块：`k` → {k}',
        'n -= 1': lambda S, B, ret: (f'还剩 `{S.n}` 位要确定' if S.n > 0 else '每一位都确定了'),
        'while n > 0': lambda S, B, ret: (f'`n = {S.n} > 0`，继续确定下一位：此时每个候选字母各有 `p[{S.n}] = {S.p[S.n]}` 种' if S.n > 0 else '`n = 0` → 结束'),
        'if k > p[n]': lambda S, B, ret: (f'`k = {S.k} > p[{S.n}] = {S.p[S.n]}` → 选两个候选里==较大的==，并扣掉前一块' if S.k > S.p[S.n]
                                         else f'`k = {S.k} ≤ p[{S.n}] = {S.p[S.n]}` → 选两个候选里==较小的==，k 不变'),
        'if last == \'c\'': lambda S, B, ret: _cand(S, '大'),
        'if last == \'a\'': lambda S, B, ret: _cand(S, '小'),
        'res += \'b\'': '`res` → `{res}`',
        'res += \'c\'': '`res` → `{res}`',
        'res += \'a\'': '`res` → `{res}`',
        'return res': '答案 `{ret}`',
    },
    cards=dict(
        one_liner='先数每块有多少个，k 落进哪块就选哪个字母，然后在块内继续',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['仅含 `a b c`、相邻字母不同的串是开心字符串',
                 '长为 `n` 的所有开心字符串按字典序排，返回第 `k` 个，不够 `k` 个返回空串',
                 '本视频：`n = 4, k = 13` → `"bcab"`'],
        quote='以a、b、c开头的开心字符串的数目是一样多的……对f[n]*3中开心字符串按字典序排列，以a开头的顺序为1到f[n]，以b开头为f[n]+1到f[n]+f[n]，以c开头则是f[n]+f[n]+1到f[n]*3。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p[m] = 2 × p[m-1]`：每个串末尾都有 2 种接法，`p[1] = 1`',
              '首字母：看 `k` 落在 a、b、c 三块的哪一块，并扣掉前面的块',
              '之后每位只有 2 个候选，同样的方法：`k > p[n]` 选大的，否则选小的'],
        result='得到 "bcab" ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：选了「较大」候选要 `k -= p[n]`，选「较小」时不变',
                 '候选字母由上一位 `last` 决定：排除自己后剩下的两个',
                 '对比灵神：灵神把 k-1 的二进制位直接对应每一位的选择，空间 `O(1)`'],
    ),
)
