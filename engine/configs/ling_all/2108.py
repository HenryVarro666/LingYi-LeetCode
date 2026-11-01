CONFIG = dict(
    num=2108, title='找出数组中的第一个回文字符串', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='逐个判断回文（Go 原文转写）', tags=[],
    code='''
class Solution:
    def firstPalindrome(self, words: List[str]) -> str:
        for w in words:
            n = len(w)
            for i in range(n // 2):
                if w[i] != w[n - 1 - i]:
                    break
            else:
                return w
        return ""
''',
    call='Solution().firstPalindrome(["abc","car","ada","racecar","cool"])',
    expect='ada',
    views=[
        dict(type='array', var='words', label='words（粉 = 当前枚举的 w）', cell=120, h=170,
             color=lambda S, i, v: 'pink' if 'w' in S and S['words'][i] == S['w'] and i == S['words'].index(S['w']) else None),
        dict(type='string', var='w', label='w（蓝 = i，粉 = n-1-i，对称位置比较）', cell=84, h=200,
             pointers={'i': 'blue', 'n - 1 - i': 'pink'}),
        dict(type='text', fn=lambda S: (f"比较 `w[{S['i']}]` 和 `w[{S['n']-1-S['i']}]`：`{S['w'][S['i']]}` 与 `{S['w'][S['n']-1-S['i']]}`" if 'i' in S and 'n' in S and S['i'] < S['n'] // 2 else ''), size=26),
    ],
    watch=[('w', 'w', 'pink'), ('n', 'n'), ('i', 'i', 'blue')],
    captions={
        'for w in words': '换下一个单词：`w` = `{w}`',
        'n = len(w)': '`n = len(w) = {n}`，只需比较前 `n // 2 = {n // 2}` 对字符',
        'for i in range': '检查第 `{i}` 对：`w[{i}]` 对 `w[{n - 1 - i}]`',
        'if w[i] !=': '`w[{i}] = {w[i]}`，`w[{n - 1 - i}] = {w[n - 1 - i]}` → ' + '{"不同" if w[i] != w[n - 1 - i] else "相同"}',
        'break': '有一对不同 → ==不是回文==，对应原文 `continue next`，直接看下一个单词',
        'return w': '内层循环没有 break：==所有对称位置都相同== → `{w}` 是第一个回文，返回',
        'return ""': '所有单词都不是回文，返回空串',
    },
    cards=dict(
        one_liner='对称位置逐对比较，全部相同就是回文，找到即返回',
        complexity='时间 `O(L)`（L 为所有单词总长），空间 `O(1)`',
        problem=['给定字符串数组 `words`，返回==第一个回文串==，没有则返回 `""`',
                 '示例：`["abc","car","ada","racecar","cool"]` → `"ada"`'],
        quote='func firstPalindrome(words []string) string { next: for _, w := range words { ... continue next ... return w }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['枚举每个单词，比较 `w[i]` 与 `w[n-1-i]`，只需比到一半',
              '任意一对不等 → 原文用 `continue next` 跳到下一个单词',
              '一对都没不等 → 直接 `return w`，后面的单词不用看了'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`continue next` 用 `break` + `for ... else` 表达',
                 '时间 `O(L)`，空间 `O(1)`',
                 '易错点：比较到 `n // 2` 为止；中间字符（奇数长度）不用比',
                 '找不到时别忘了返回 `""`'],
    ),
)
