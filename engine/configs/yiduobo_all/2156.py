def _lo(S):
    return S.get('index')


def _hi(S):
    i = S.get('index')
    if i is None:
        return None
    n = len(S['s'])
    return n - 1 if 'res' not in S else min(i + S['k'] - 1, n - 1)


def _info(S):
    if 'now' not in S:
        return '先算最后一个窗口的哈希，再从后往前滚动'
    f = '' if 'pow_k' not in S else f'，`power^k = {S["pow_k"]}`'
    return f'`now = {S["now"]}`（目标 `{S["hashValue"]}`）' + f


CONFIG = dict(
    num=2156, title='查找给定哈希值的子串', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='反向 rk 哈希 · 从后往前滚动',
    tags=['字符串', '难度分 2063'],
    code='''
class Solution(object):
    def subStrHash(self, s, power, modulo, k, hashValue):

        n = len(s)
        p = n - k
        now = 0
        pow_k = 1

        for index in range(n - 1, p - 1, -1):
            now = (now * power + ord(s[index]) - 96) % modulo
            pow_k = pow_k * power % modulo

        res = n - 1
        if now == hashValue:
            res = p
        
        for index in range(p - 1, -1, -1):
            now = (now * power - (ord(s[index + k]) - 96) * pow_k % modulo + modulo + ord(s[index]) - 96) % modulo
            if now == hashValue:
                res = index
        
        return s[res : res + k]
''',
    call="Solution().subStrHash('leetcode', 7, 20, 2, 0)",
    expect='ee',
    views=[
        dict(type='string', var='s', label='s（框 = 当前窗口，从后往前）', cell=100, h=230,
             pointers={'index': 'blue'}, window=(_lo, _hi)),
        dict(type='text', h=90, size=30, fn=_info),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"`res = {S['res']}`：目前最靠前的命中位置" if 'res' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'orange'), ('pow_k', 'pow_k', 'cyan'), ('res', 'res', 'green')],
    captions={
        'n = len(s)': '`n = {n}`',
        'p = n - k': '`p = n - k = {p}`：最后一个窗口的起点',
        'now = 0': '`now` 保存当前窗口的哈希',
        'pow_k = 1': '`pow_k` 将算出 `power^k`，用来删掉窗口外的那一项',
        'for index in range(n - 1, p - 1, -1)': lambda S, B, r: (f'先处理最后一个窗口：`index = {S.index}`' if not ('index' in B and S.index == B.index and S.index == S.p)
                                                                  else '最后一个窗口的哈希算完了'),
        'now = (now * power + ord': '`now = (now × {power} + val({s[index]!r})) % {modulo} = {now}`：从后往前加入：越靠后的字母乘的 power 越多，次数越高',
        'pow_k = pow_k * power': '`pow_k = {pow_k}`（这一步累乘 `power`，共 `k` 次）',
        'res = n - 1': '先给 `res` 一个初值，后面一定会被覆盖',
        'if now == hashValue': lambda S, B, r: (f'`now = {S.now}` 等于目标 `{S.hashValue}`：窗口 `{S.s[S.index:S.index+S.k]!r}` 命中，==记下位置=='
                                                if S.now == S.hashValue else f'`now = {S.now} ≠ {S.hashValue}`，没命中'),
        'res = p': '最后一个窗口命中：`res = {res}`',
        'res = index': '`res = {res}`：从后往前扫，后写入的更靠前，会==覆盖==旧答案',
        'for index in range(p - 1, -1, -1)': lambda S, B, r: (f'窗口左端点往前挪一格：`index = {S.index}`' if not ('index' in B and S.index == B.index and S.index == 0)
                                                               else '扫描结束'),
        'now = (now * power -': ('`h1 = h2 × p − val(s[{index}+{k}]) × p^k + val(s[{index}])`：乘 `p` 让旧项升一次幂，'
                                 '减去滑出的 `{s[index+k]!r}`，加上新进的 `{s[index]!r}`，`now = {now}`'),
        'return s[res': '返回 `s[{res}:{res}+{k}]` = =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='h1 = h2 × p − 滑出项 + 新进项，从后往前滚',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['哈希 `= Σ val(s[j])·power^j mod m`（`val(a)=1`）',
                 '求 `s` 里==第一个==长为 `k`、哈希等于 `hashValue` 的子串',
                 '示例：`s="leetcode", power=7, mod=20, k=2, hashValue=0` → `"ee"`'],
        quote='题目描述的是经典的字符串哈希算法rk算法的反向计算版。……h1 = (h2 * p - val(s[i + k]) * p^k + val(s[i])) % m',
        quote_src='—— yiduobo 题解原文',
        idea=['i 到 i+k-1 的哈希 h1 和 i+1 到 i+k 的哈希 h2 相差很小',
              'h2 乘 `p`，去掉多出的最后一项，再补上 `val(s[i])` 就是 h1',
              '所以从后往前扫一遍，所有窗口的哈希都能 `O(1)` 滚出来'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先单独算最后一个窗口，同时顺手算出 `power^k`',
                 '易错：减法后要 `+ modulo` 再取模，防止出现负数',
                 '从后往前遇到命中就覆盖 `res`，最终得到最靠前的答案',
                 '对比灵神：灵神每步先进后出，用 `power^(k-1)`；原文直接用 `power^k`'],
    ),
)
