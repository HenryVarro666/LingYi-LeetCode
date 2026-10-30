def _counts(S):
    if 'word' not in S:
        return None
    return dict(sorted(Counter(S['word']).items()))


CONFIG = dict(
    num=2423, title='删除字符使频率相同', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论：次数至多两种',
    tags=['灵神题单'],
    code='''
class Solution:
    def equalFrequency(self, word: str) -> bool:
        cnt = sorted(Counter(word).values())  # 出现次数从小到大排序
        # 只有一种字符 or 去掉次数最少的 or 去掉次数最多的
        return len(cnt) == 1 or \\
               cnt[0] == 1 and len(set(cnt[1:])) == 1 or \\
               cnt[-1] == cnt[-2] + 1 and len(set(cnt[:-1])) == 1
''',
    call='Solution().equalFrequency("aabbccc")',
    expect=True,
    views=[
        dict(type='string', var='word', label='word', h=170),
        dict(type='map', var=_counts, label='每个字母出现次数 Counter(word)', fmt=lambda k, v: f"'{k}': {v}", h=170, font=32),
        dict(type='array', var='cnt', label='cnt = 次数从小到大排序', h=190,
             color=lambda S, i, v: 'pink' if i == len(S['cnt']) - 1 else ('blue' if i == 0 else None)),
    ],
    watch=['cnt', ('len(cnt)', 'len(cnt)', 'cyan')],
    captions={
        'cnt = sorted': '统计每个字母的出现次数并排序：`cnt = {cnt}`',
        'return len(cnt) == 1': lambda S, B, r: ('三种情形用 `or` 连接，一个为真就返回 `True`；前面的仍为 False，继续算下一个' if r is None
                                                else f'`{S.cnt[-1]} == {S.cnt[-2]} + 1` 且其余次数 `{sorted(set(S.cnt[:-1]))}` 都相同 → 去掉次数最多的那个字母一次即可，返回 =={r}=='),
        'cnt[0] == 1 and': lambda S, B, r: (f'①只有一种字符？`len(cnt) = {len(S.cnt)}` → 不是；'
                                            f'②去掉次数最少的：`cnt[0] = {S.cnt[0]}` 不是 1，不成立'
                                            if S.cnt[0] != 1 else '②最少的恰好 1 次，且其余次数是否都相同？'),
        'cnt[-1] == cnt[-2] + 1': '③去掉次数最多的：`{cnt[-1]} == {cnt[-2]} + 1` 吗？其余次数 `{sorted(set(cnt[:-1]))}` 是否只有一种？',
    },
    cards=dict(
        one_liner='次数至少三种就一定不行，只需讨论至多两种',
        complexity='时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
        problem=['字符串 `word`（小写字母），==恰好删除一个字符==',
                 '问删完后每个字母出现次数是否都相同',
                 '示例：`"abcc"` → `true`；`"aazz"` → `false`'],
        quote='如果有至少三种不同的出现次数，无论去掉哪个字符，剩下的出现次数仍然至少有两种。所以只需要讨论出现次数至多两种的情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力：枚举删哪个字符，再统计次数，`O(n^2)`；这里用方法二',
              '把次数排序成 `cnt`：只有一种字符，删谁都行',
              '去掉次数最少的：它必须恰好是 1，其余次数相同',
              '去掉次数最多的：它恰好比次多的多 1，其余次数相同'],
        summary=['时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
                 '必须恰好删一个：`"aabbcc"` 次数全 2，却不行',
                 '每个字符都只出现一次（如 `"abcde"`）：删谁都行，落在「最少的恰好是 1」里',
                 '方法一暴力枚举删除位置，`Counter(word[:i] + word[i+1:])`，本视频演示方法二',
                 '相似题：1224 最大相等频率'],
    ),
)
