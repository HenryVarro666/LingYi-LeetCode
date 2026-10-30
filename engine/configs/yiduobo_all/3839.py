WORDS = ["apple", "apply", "banana", "bandit", "a", "cat"]
K = 2


def _wcolor(S, i, v):
    k = S.get('k')
    if k is None or len(v) < k:
        return None
    if S.get('w') == v and S.get('prefix') is not None and S['_line'] <= 9:
        return 'blue'
    freq = S.get('freq')
    if S.get('res') is not None and freq is not None and freq.get(v[:k], 0) > 1:
        return 'green'
    return None


def _wdim(S, i, v):
    return S.get('k') is not None and len(v) < S['k']


def _txt(S):
    if S.get('res') is not None:
        return f"`freq[p] > 1` 的前缀数 `res = {S['res']}`"
    if S.get('prefix') is not None:
        return f"`w = {S['w']!r}` → 前缀 `prefix = {S['prefix']!r}`"
    return '每个单词转成前 `k` 个字母的前缀，再数个数'


CONFIG = dict(
    num=3839, title='前缀连接组的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 先转前缀再计数',
    tags=[],
    code='''
class Solution(object):
    def prefixConnected(self, words, k):
        
        freq = {}
        for w in words:
            if len(w) < k:
                continue
            prefix = w[:k]
            freq[prefix] = freq.get(prefix, 0) + 1
        
        res = 0
        for p in freq:
            if freq[p] > 1:
                res += 1
        
        return res
''',
    call=f'Solution().prefixConnected({WORDS!r}, {K})',
    expect=2,
    views=[
        dict(type='array', var='words', label='words（蓝 = 当前单词，灰 = 太短被忽略，绿 = 前缀出现 ≥ 2 次）', cell=150, h=240,
             dim=_wdim, color=_wcolor),
        dict(type='map', var='freq', label='freq（前缀 → 出现次数）', fmt=lambda k, v: f"{k!r}: {v}", h=190, font=34),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('k', 'k', 'blue'), ('w', 'w', 'cyan'), ('prefix', 'prefix', 'orange'), ('res', 'res', 'green')],
    captions={
        'freq = {}': '`freq` 统计每种长度为 `k = {k}` 的前缀出现了几次',
        'for w in words': lambda S, B, r: (f'看下一个单词 `w = {S.w!r}`' if 'w' not in B or S.w != B.w or S.freq != B.freq else '所有单词处理完，`freq` 就是前缀计数'),
        'if len(w) < k': lambda S, B, r: (f'`len({S.w!r}) = {len(S.w)} < k = {S.k}` → 长度不足，==不能加入任何组== → 跳过' if len(S.w) < S.k
                                          else f'`len({S.w!r}) = {len(S.w)} ≥ k = {S.k}` → 可以参与'),
        'continue': '直接看下一个单词',
        'prefix = w[:k]': '只关心前 `k` 个字母：`prefix = {prefix!r}`，不用记原单词',
        'freq[prefix] =': '`freq[{prefix!r}]` 加一 → `{freq[prefix]}`',
        'res = 0': '`res` 数包含至少两个单词的组：即 `freq` 里值大于 1 的前缀',
        'for p in freq': lambda S, B, r: (f'检查前缀 `p = {S.p!r}`，出现 `{S.freq[S.p]}` 次' if 'p' in S and ('p' not in B or S.p != B.p or S.res != B.res) else '前缀检查完毕'),
        'if freq[p] > 1': lambda S, B, r: (f'`freq[{S.p!r}] = {S.freq[S.p]} > 1` → ==至少两个单词，成一组==' if S.freq[S.p] > 1
                                           else f'`freq[{S.p!r}] = {S.freq[S.p]}` 只有一个单词，成不了组'),
        'res += 1': '多一个连接组 → `res = {res}`',
        'return res': '共 `{res}` 个连接组',
    },
    max_steps=70,
    cards=dict(
        one_liner='把单词换成前 k 位前缀，数一数哪些前缀出现不止一次',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['前 `k` 个字母相同的单词必须分在同一组，长度不足 `k` 的忽略',
                 '求至少含两个单词的组数',
                 '本视频：`["apple","apply","banana","bandit","a","cat"], k = 2` → `2`'],
        quote='不需要记录原始单词，于是可以一趟遍历，将每个单词转化为其前k个字符形成的前缀。……最终答案就是哈希表中值大于1的元素数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['前缀连接 = 前 `k` 个字母相同，所以一个前缀对应一个组',
              '遍历单词：太短的 `continue`，否则 `freq[prefix] += 1`',
              '再遍历 `freq`，值 `> 1` 的前缀各算一个组'],
        summary=['时间 `O(nk)`，空间 `O(nk)`',
                 '易错：长度不足 `k` 的单词要先跳过，不能参与计数',
                 '重复单词算不同单词，所以 `freq` 里次数会累加',
                 '对比灵神：灵神用 `Counter` 一行统计，yiduobo 手写 `freq.get(prefix, 0) + 1` 再单独循环计数',
                 '原文为 Python 2 风格 `class ...(object)`，Python 3 直接可运行，代码未改'],
    ),
)
