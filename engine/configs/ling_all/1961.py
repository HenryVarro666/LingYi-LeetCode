CONFIG = dict(
    num=1961, title='检查字符串是否为数组前缀', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='累加长度 · 相等才比较（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def isPrefixString(self, s: str, words: List[str]) -> bool:
        sum = 0
        for i, word in enumerate(words):
            sum += len(word)
            if sum > len(s):
                return False
            if sum == len(s):
                return "".join(words[:i + 1]) == s
        return False
''',
    call='Solution().isPrefixString("iloveleetcode", ["i","love","leetcode","apples"])',
    expect=True,
    views=[
        dict(type='string', var='s', label='s', cell=40, h=170),
        dict(type='array', var='words', label='words（绿 = 已累加的单词）', cell=150, h=250, pointers={'i': 'blue'},
             color=lambda S, k, v: 'green' if 'i' in S and k <= S['i'] else None),
        dict(type='text', fn=lambda S: f"已累加长度 `sum = {S['sum']}`，`len(s) = {len(S['s'])}`" if 'sum' in S else '', h=80),
    ],
    watch=['i', ('word', 'word', 'blue'), ('sum', 'sum', 'green')],
    captions={
        'sum = 0': '`sum` 记录前缀单词的总长度',
        'for i, word': '看第 {i} 个单词 `word = "{word}"`',
        'sum += len': '加上 `len("{word}") = {len(word)}`：`sum` {B.sum} → =={sum}==',
        'if sum > len': lambda S, B, ret: (f"`sum = {S.sum}` > `len(s) = {len(S.s)}`：已经比 `s` 长，不可能拼出 → ==False==" if S.sum > len(S.s)
                                           else f"`sum = {S.sum}` ≤ `len(s) = {len(S.s)}`：还没超，继续"),
        'if sum == len': lambda S, B, ret: (f"`sum = {S.sum}` == `len(s)`：长度刚好 → ==这时才值得比较内容==" if S.sum == len(S.s)
                                            else f"`sum = {S.sum}` < `len(s) = {len(S.s)}`：长度不够，继续往后加"),
        'return "".join': lambda S, B, ret: f"拼接前 {S.i + 1} 个单词，与 `s` 比较 → ==`{ret}`==",
        'return False': '单词用完仍不到 `len(s)` → `False`',
    },
    cards=dict(
        one_liner='前缀长度恰好等于 len(s) 时，才拼接比较一次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断 `s` 能否由 `words` 的前 `k` 个单词按序拼成（`k ≥ 1`）',
                 '示例：`"iloveleetcode"`，`["i","love","leetcode","apples"]` → `true`'],
        quote='仅当 words 前缀累加的长度等于 s 的长度时才去比较。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先只累加长度，不拼字符串',
              '长度超过 `len(s)` → 不可能，直接 `False`',
              '长度恰好相等才 `join` 比较一次，结果就是答案'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，`n = len(s)`；空间 `O(n)`（只在最后拼一次）',
                 '易错：必须是==整个单词==拼成，长度不等就不能停',
                 '`k` 必须为正数，所以空前缀不算'],
    ),
)
