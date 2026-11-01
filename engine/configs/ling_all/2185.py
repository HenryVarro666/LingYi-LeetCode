CONFIG = dict(
    num=2185, title='统计包含给定前缀的字符串', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='遍历 + startswith（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def prefixCount(self, words: List[str], pref: str) -> int:
        ans = 0
        for word in words:
            if word.startswith(pref):
                ans += 1
        return ans
''',
    call='Solution().prefixCount(["pay", "attention", "practice", "attend"], "at")',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: f"前缀 `pref = \"{S['pref']}\"`，已统计 =={S.get('ans', 0)}== 个", size=30),
        dict(type='array', var='words', label='words（绿 = 以 pref 开头）', cell=150, h=240,
             pointers={'words.index(word)': 'blue'}, pointer_labels={'words.index(word)': 'word'},
             color=lambda S, i, v: 'green' if 'word' in S and S['words'].index(S['word']) >= i and v.startswith(S['pref']) else None),
    ],
    watch=[('word', 'word', 'blue'), ('pref', 'pref', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '计数器 `ans` 从 0 开始',
        'for word in words': lambda S, B, ret: (f'取出 `word = "{S.word}"`' if S.get('word') != B.get('word') else '所有单词都看完了'),
        'if word.startswith': lambda S, B, ret: (f'`"{S.word}"` 以 `"{S.pref}"` 开头 → ==计入答案==' if S.word.startswith(S.pref)
                                                 else f'`"{S.word}"` 不以 `"{S.pref}"` 开头 → 跳过'),
        'ans += 1': '又找到一个，`ans` → {ans}',
        'return ans': '共有 `{ans}` 个字符串以前缀开头',
    },
    cards=dict(
        one_liner='逐个判断是否以 pref 开头，是就计数',
        complexity='时间 `O(n·m)`，空间 `O(1)`，`m = len(pref)`',
        problem=['返回 `words` 中以 `pref` 作为==前缀==的字符串数目',
                 '示例：`words = ["pay","attention","practice","attend"]`，`pref = "at"` → `2`'],
        quote='func prefixCount(words []string, pref string) (ans int) { for _, word := range words { if strings.HasPrefix(word, pref) { ans++ } } return }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['遍历每个字符串，用内置的前缀判断 `startswith` 检查', '满足就把答案加一，没有任何技巧，直接模拟'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`strings.HasPrefix` → `startswith`）',
                 '时间 `O(n·m)`，空间 `O(1)`',
                 '易错：是==前缀==不是子串，不要用 `in`'],
    ),
)
