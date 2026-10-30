WORDS = ["apple", "apply", "banana", "bandit", "a", "cat"]
K = 2


def _wcolor(S, i, v):
    k = S.get('k')
    if k is None or len(v) < k:
        return None
    cnt = S.get('cnt')
    if cnt is not None and cnt.get(v[:k], 0) > 1:
        return 'green'
    return None


def _wdim(S, i, v):
    return S.get('k') is not None and len(v) < S['k']


def _txt(S):
    cnt = S.get('cnt')
    if cnt is None:
        return '把每个单词只看前 `k` 个字母，同前缀的就是一组'
    big = [p for p, c in cnt.items() if c > 1]
    return f"出现次数 ≥ 2 的前缀：{'、'.join(repr(p) for p in big) if big else '无'}　共 =={len(big)}== 组"


CONFIG = dict(
    num=3839, title='前缀连接组的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 统计前缀出现次数',
    tags=[],
    code='''
class Solution:
    def prefixConnected(self, words: List[str], k: int) -> int:
        cnt = Counter(w[:k] for w in words if len(w) >= k)
        return sum(c > 1 for c in cnt.values())
''',
    call=f'Solution().prefixConnected({WORDS!r}, {K})',
    expect=2,
    views=[
        dict(type='array', var='words', label='words（灰 = 长度不足 k，被忽略；绿 = 前缀出现 ≥ 2 次）', cell=150, h=240,
             dim=_wdim, color=_wcolor),
        dict(type='map', var='cnt', label='cnt（前缀 → 出现次数）', fmt=lambda k, v: f"{k!r}: {v}", h=190, font=34),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('k', 'k', 'blue'), ('cnt', 'cnt', 'orange')],
    captions={
        'cnt = Counter': lambda S, B, r: f'跳过长度小于 `k = {S.k}` 的单词，其余取前 `k` 个字母计数：`{dict(S.cnt)}`',
        'return sum': lambda S, B, r: f'次数 `> 1` 的前缀有 `{r}` 个：每个前缀就是一个至少两个单词的连接组 → 返回 `{r}`',
    },
    max_steps=40,
    cards=dict(
        one_liner='前 k 个字母相同就是一组：哈希表数一数出现次数 ≥ 2 的前缀',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['前 `k` 个字母相同的两个单词是「前缀连接」的，连成一个组',
                 '长度小于 `k` 的单词忽略；重复的单词算不同的单词',
                 '求至少含两个单词的组数；示例 `["apple","apply","banana","bandit"], k = 2` → `2`'],
        quote='说人话就是：统计 words[i][..k]（长为 k 的前缀）的出现次数，有多少个出现次数 ≥ 2 的不同前缀？用哈希表统计即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['题意绕，转成：数前缀 `w[:k]` 出现几次',
              '`Counter` 一行统计，`if len(w) >= k` 跳过太短的单词',
              '次数大于 1 的前缀个数 = 答案'],
        summary=['时间 `O(nk)`（每个切片 `O(k)`），空间 `O(nk)`',
                 '易错：长度不足 `k` 的单词不能参与，否则 `w[:k]` 会得到更短的串',
                 '重复单词算不同单词，所以 `"bat"`、`"bat"` 能成一组',
                 '本视频小例子：`["apple","apply","banana","bandit","a","cat"], k = 2` → `2`'],
    ),
)
