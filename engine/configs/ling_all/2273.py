CONFIG = dict(
    num=2273, title='移除字母异位词后的结果数组', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='原地修改 · 保留连续异位词最左边的',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1295'],
    code='''
class Solution:
    def removeAnagrams(self, words: List[str]) -> List[str]:
        k = 1
        for s, t in pairwise(words):
            if sorted(s) != sorted(t):
                words[k] = t
                k += 1
        del words[k:]
        return words
''',
    call="Solution().removeAnagrams(['abba','baba','bbaa','cd','cd'])",
    expect=['abba', 'cd'],
    views=[
        dict(type='text', fn=lambda S: (f"`{S['s']}` 排序 = `{''.join(sorted(S['s']))}`，`{S['t']}` 排序 = `{''.join(sorted(S['t']))}`" if 's' in S and 't' in S else '')),
        dict(type='array', var='words', pointers={'k': 'pink'}, h=300, cell=150,
             color=lambda S, i, v: 'green' if 'k' in S and i < S['k'] else None,
             dim=lambda S, i, v: 'k' in S and i >= S['k'] and v in S.get('words', [])[:S['k']] and False),
    ],
    watch=[('s', 's', 'blue'), ('t', 't', 'cyan'), ('k', 'k', 'pink')],
    captions={
        'k = 1': '`words[0]` 一定保留，所以结果长度 `k` 从 1 开始',
        'for s, t in pairwise': lambda S, B, r: (lambda: '没有下一对了，循环结束' if (getattr(B, 't', None) == S.t and getattr(B, 's', None) == S.s and getattr(B, 't', None) is not None) else f'取相邻一对：`s = {S.s}`，`t = {S.t}`')(),
        'if sorted(s) != sorted(t)': '排序后 `{"".join(sorted(s))}` 和 `{"".join(sorted(t))}`：{"不同 → 不是异位词，t 要保留" if sorted(s) != sorted(t) else "相同 → t 是 s 的异位词，删掉 t"}',
        'words[k] = t': '把 `{t}` 写到 `words[{k}]`（原地覆盖）',
        'k += 1': '保留数量 `k` → {k}',
        'del words[k:]': '`k` 之后的都是多余的，删掉，只剩前 {k} 个',
        'return words': '返回 `{words}`',
    },
    cards=dict(
        one_liner='连续的异位词只留最左边的一个，和第 26 题一样',
        complexity='时间 `O(nL log L)`，空间 `O(L)`',
        problem=['`words` 里相邻两个单词若是字母异位词，就删掉后一个，直到不能删',
                 '示例：`["abba","baba","bbaa","cd","cd"]` → `["abba","cd"]`',
                 '字母异位词：两个串每种字母出现次数相同'],
        quote='连续相同的字母异位词，只保留其中最左边的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`abba, baba, bbaa` 互为异位词，只留 `abba`；`cd, cd` 只留第一个',
              '用 `pairwise` 比较相邻两个：和前一个不是异位词，说明是新一段的开头，保留',
              '判断异位词：两个串排序后相同'],
        summary=['时间 `O(nL log L)`，空间 `O(L)`，`L ≤ 10`',
                 '`k` 从 1 开始，因为第一个单词一定保留',
                 '比较的是原相邻两个词，不是和结果里的最后一个；异位词关系可传递，所以等价',
                 '另一种写法：用 `Counter(s) != Counter(t)` 判断，免排序'],
    ),
)
