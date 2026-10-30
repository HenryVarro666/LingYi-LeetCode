def _cur(S):
    ch = S.get('ch')
    if ch is None or 'cnt' not in S:
        return '`cnt[x]` = 刚发出 x 声音的青蛙数；青蛙按 c→r→o→a→k 接力'
    pre = S.get('pre')
    return f'当前字母 ==`{ch}`==，它的上一个字母是 `{pre}`' if pre else f'当前字母 ==`{ch}`=='


CONFIG = dict(
    num=1419, title='数青蛙', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='哈希表 · 按上一个字母接力',
    tags=[],
    code='''
# 预处理每个字母在 "croak" 中的上一个字母
PREVIOUS = dict(pairwise("croakc"[::-1]))

class Solution:
    def minNumberOfFrogs(self, croakOfFrogs: str) -> int:
        cnt = defaultdict(int)
        for ch in croakOfFrogs:
            pre = PREVIOUS[ch]  # pre 为 ch 在 "croak" 中的上一个字母
            if cnt[pre]:  # 如果有青蛙发出了 pre 的声音
                cnt[pre] -= 1  # 复用一只
            elif ch != 'c':  # 否则青蛙必须从 'c' 开始蛙鸣
                return -1  # 不符合要求
            cnt[ch] += 1  # 发出了 ch 的声音
        if any(cnt[ch] for ch in "croa"):
            return -1  # 有发出其它声音的青蛙，不符合要求
        return cnt['k']  # 最后青蛙们都发出了 'k' 的声音
''',
    call='Solution().minNumberOfFrogs("crcoakroak")',
    expect=2,
    views=[
        dict(type='string', var='croakOfFrogs', label='croakOfFrogs', cell=80, h=170),
        dict(type='text', h=90, size=30, fn=_cur),
        dict(type='map', var='cnt', label='cnt：刚发出某字母声音的青蛙数', fmt=lambda k, v: f"'{k}': {v}", h=200, font=34),
    ],
    watch=['ch', 'pre', ('cnt', "dict(cnt)", 'green')],
    captions={
        'pre = PREVIOUS': '`{ch}` 的上一个字母是 `{pre}`：它得接在发出 `{pre}` 的青蛙后面',
        'if cnt[pre]': lambda S, B, r: (f'`cnt[{S.pre!r}] = {S.cnt[S.pre]}` > 0：有青蛙刚发出 `{S.pre}` → 成立，可以接力'
                                       if S.cnt[S.pre] else f'`cnt[{S.pre!r}] = 0`：没有青蛙能接力 → 不成立'),
        'cnt[pre] -= 1': '复用一只青蛙：`cnt[{pre!r}]` 减一 → {cnt[pre]}',
        'elif ch != ': lambda S, B, r: (f'没有青蛙可接，但 `{S.ch}` 不是 c，青蛙不能从中间开叫 → 成立' if S.ch != 'c'
                                       else '没有可复用的青蛙，但是 c：==新来一只青蛙==开叫'),
        'return -1  # 不符合': '蛙鸣顺序不合法 → 返回 `-1`',
        'cnt[ch] += 1': '这只青蛙现在停在 `{ch}`：`cnt[{ch!r}]` = =={cnt[ch]}==',
        'any(cnt[ch]': lambda S, B, r: ('c/r/o/a 里还有青蛙没叫完 → 不合法' if r else 'c/r/o/a 都是 0：每只青蛙都叫完了整句 croak'),
        "return cnt['k']": '所有青蛙都停在 k，==数量就是最少需要的青蛙数== `{ret}`（青蛙叫完会复用，不会重复计数）',
    },
    cards=dict(
        one_liner='青蛙按 croak 接力：消耗上一个字母，产生当前字母',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`，|Σ| = 5',
        problem=['`croakOfFrogs` 是多只青蛙的 "croak" 蛙鸣混合而成，求最少需要几只青蛙；不合法返回 `-1`',
                 '青蛙必须依序发出 c、r、o、a、k',
                 '示例："crcoakroak" → `2`'],
        quote='需要消耗一个 c，产生一个 r。这启发我们使用一个哈希表（数组）cnt 来维护这 5 种青蛙的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把青蛙按「刚发出哪个字母」分成 5 类，`cnt` 记个数',
              '遇到 `ch`：有青蛙刚发出上一个字母就==复用==它，没有则必须是 c，==新来一只==',
              '用 `PREVIOUS` 字典记每个字母的上一个字母，省掉一堆 if-else'],
        summary=['时间 `O(n)`，空间 `O(1)`（只有 5 个字母）',
                 '非 c 字母找不到上一类青蛙 → 立刻返回 `-1`',
                 '遍历完要检查 c/r/o/a 的 cnt 全为 0，否则有青蛙没叫完',
                 '`cnt[k]` 即答案：叫完的青蛙复用为 c，所以峰值青蛙数就是 k 的计数'],
    ),
)
