def _i(S):
    if 'base' in S and 'cnt' in S and S['base'] in S['cnt']:
        return S['cnt'].index(S['base'])
    return None


def _txt(S):
    if 'mx' not in S:
        return ''
    if S['_line'] < 11:
        return f"保留的最小次数 `base = {S['base']}`，最大允许 `mx = base + k = {S['mx']}`"
    return f"保留总数 = 不变部分 `s = {S['s']}` + `{S['mx']} × {len(S['cnt']) - S['right']}` = {S['s'] + S['mx'] * (len(S['cnt']) - S['right'])}"


CONFIG = dict(
    num=3085, title='成为 K 特殊字符串需要删除的最少字符数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='枚举最小次数 + 滑动窗口',
    tags=['灵神题单', '贪心算法', '难度分 1765'],
    code='''
class Solution:
    def minimumDeletions(self, word: str, k: int) -> int:
        cnt = sorted(Counter(word).values())
        max_save = s = right = 0
        for base in cnt:
            mx = base + k
            while right < len(cnt) and cnt[right] <= mx:
                s += cnt[right]
                right += 1
            # 现在 s 表示出现次数不变的字母个数之和
            # 再加上出现次数减少为 mx 的 len(cnt)-right 种字母，即为保留的字母总数
            max_save = max(max_save, s + mx * (len(cnt) - right))
            # 下一轮循环 base 全删
            s -= base
        return len(word) - max_save
''',
    call="Solution().minimumDeletions('dabdcbdcdcd', 2)",
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=30, h=90),
        dict(type='array', var='cnt', h=300, label='cnt（各字母出现次数，升序）',
             pointers={'right': 'pink'},
             color=lambda S, i, v: ('blue' if i == _i(S) else 'green' if _i(S) is not None and _i(S) < i < S.get('right', 0) else None),
             dim=lambda S, i, v: _i(S) is not None and i < _i(S)),
    ],
    watch=[('base', 'base', 'blue'), ('mx', 'mx', 'yellow'), ('right', 'right', 'pink'), ('s', 's'), ('max_save', 'max_save', 'green')],
    captions={
        'cnt = sorted': '统计每种字母的出现次数并排序：`cnt = {cnt}`',
        'max_save = s': '`max_save` 最多保留几个字母；`s` 窗口内次数之和；`right` 窗口右端',
        'for base in cnt': lambda S, B, r: ('所有 base 都枚举完' if B.get('base') == S.get('base') and 'base' in B else f"枚举 `base = {S.base}`：假设删完后最少的字母出现 `{S.base}` 次（这种字母没被删过）"),
        'mx = base + k': '次数差不能超过 `k`，所以最多保留 `mx = {base} + {k}` = =={mx}==',
        'while right < len': lambda S, B, r: (f"`cnt[{S.right}] = {S.cnt[S.right]}` {'<=' if S.cnt[S.right] <= S.mx else '>'} `mx = {S.mx}` → {'次数不变，纳入窗口' if S.cnt[S.right] <= S.mx else '超过 mx，要被削减，窗口停下'}" if S.right < len(S.cnt) else '`right` 到头了，窗口停下'),
        's += cnt[right]': '这种字母一个不用删：`s` = =={s}==',
        'right += 1': '窗口右端 `right` → {right}',
        'max_save = max': '保留总数 = `{s}` + `{mx}×{len(cnt) - right}` = {s + mx * (len(cnt) - right)}；`max_save` = =={max_save}==',
        's -= base': '下一轮 `base` 更大，这种次数 `{base}` 的字母要全删，从 `s` 里去掉：`s` = {s}',
        'return len(word)': '`len(word) - max_save = {len(word)} - {max_save}` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举「删完后最少的次数」，其余的削到 base+k',
        complexity='时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
        problem=['`freq(x)` 是字符出现次数；要求任意两个字符的次数差 `<= k`',
                 '求最少删除多少个字符，让 `word` 成为 k 特殊字符串',
                 '示例：`word = "dabdcbdcdcd", k = 2` → `2`'],
        quote='删除字母后，在所有出现次数最少的字母中，一定存在没被删除过的字母。',
        quote_src='—— 灵茶山艾府题解（猜想）',
        idea=['猜想成立：最少的那种字母不会被删，所以枚举 `cnt[i]` 作最小次数',
              '次数 `< base` 全删；在 `[base, base+k]` 不变；更多的削到 `base+k`',
              '次数排序后用滑动窗口维护「不变」的字母，复杂度更低'],
        after=[dict(heading='优化前的写法', lines=['每个 `base` 暴力算 `sum(min(c, base+k) for c in cnt[i:])`',
                                              '时间 `O(n + |Σ|²)`；字符集大时会超时，所以改成窗口'])],
        summary=['时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
                 '`cnt` 要先排序，窗口才能单调右移',
                 '易错：下一轮前 `s -= base`，因为小于新 base 的字母要全删',
                 '相似题：2171 拿出最少数目的魔法豆'],
    ),
)
