def _top(S):
    if 'ch' not in S:
        return ''
    return f"候选：删掉下标 `{S['i']}` 的 `{S['ch']}`" if S['ch'] == S['digit'] else f"`{S['ch']}` 不是 `{S['digit']}`，跳过"


CONFIG = dict(
    num=2259, title='移除指定数字得到的最大结果', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='枚举删除位置 · 取最大',
    tags=['灵神题单', '贪心算法'],
    code='''
class Solution:
    def removeDigit(self, s: str, digit: str) -> str:
        return max(s[:i] + s[i + 1:] for i, ch in enumerate(s) if ch == digit)
''',
    call='Solution().removeDigit("1231", "1")',
    expect='231',
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（蓝 = 当前枚举的位置）', cell=84,
             pointers={'i': 'blue'},
             color=lambda S, k, v: ('blue' if S.get('i') == k else ('yellow' if v == S.get('digit') else None))),
        dict(type='text', fn=lambda S: '所有候选：' + '，'.join(f"删下标{k}→`{S['s'][:k] + S['s'][k+1:]}`" for k, c in enumerate(S['s']) if c == S['digit']), size=26),
        dict(type='text', fn=lambda S: '字符串长度相同，直接比较字典序就是比较数值大小；`max` 取最大的结果', size=24),
    ],
    watch=['digit', ('i', 'i', 'blue'), ('ch', 'ch')],
    captions={
        'return max': lambda S, B, r: (f"枚举每个等于 `{S.digit}` 的位置，删掉它，取字典序最大的结果 → `{r}`" if 'ch' not in S or r is not None
                                       else f"枚举：`i = {S.i}`，`ch = {S.ch}`"),
    },
    cards=dict(
        one_liner='枚举每个等于 digit 的位置删掉，取最大的结果',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['字符串 `number` 表示正整数，字符 `digit` 在其中至少出现一次',
                 '==恰好删除一个==等于 `digit` 的字符，使结果最大',
                 '示例：`"1231"`，`digit = "1"` → `"231"`'],
        quote='max(s[:i] + s[i + 1:] for i, ch in enumerate(s) if ch == digit)',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['`s[:i] + s[i + 1:]` 就是删掉下标 `i` 的字符',
              '删除后长度都一样，所以比较字典序等价于比较数值',
              '数据很小（长度 ≤ 100），直接暴力枚举即可',
              '生成器里每个候选算一次，`max` 在字符串之间比较字典序'],
        after=[dict(heading='更快的做法', lines=[
            '从左到右找第一个 `s[i] == digit` 且 `s[i] < s[i+1]` 的位置，删掉它',
            '删掉它后高位变大，比删任何更靠后的位置都好',
            '找不到就删最后一个 digit：损失最小，时间 `O(n)`'])],
        summary=['时间 `O(n^2)`：最多 n 个候选，每个拼接 `O(n)`',
                 '长度相同的数字串，字典序 = 数值大小',
                 '更快做法：删第一个「后面比它大」的 digit，否则删最后一个'],
    ),
)
