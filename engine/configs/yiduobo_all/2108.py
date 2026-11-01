CONFIG = dict(
    num=2108, title='找出数组中的第一个回文字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='两端双指针判断回文', tags=[],
    code='''
class Solution(object):
    def firstPalindrome(self, words):

        for word in words:
            flag = True
            l = 0
            r = len(word) - 1
            while l < r:
                if word[l] != word[r]:
                    flag = False
                    break
                l += 1
                r -= 1
            
            if flag:
                return word
        
        return ""
''',
    call='Solution().firstPalindrome(["abc","car","ada","racecar","cool"])',
    expect='ada',
    views=[
        dict(type='array', var=lambda S: list(range(len(S['words']))), label='第几个单词（粉 = 当前）', cell=64, h=130,
             color=lambda S, i, v: 'pink' if 'word' in S and S['words'][i] == S['word'] and i == S['words'].index(S['word']) else None),
        dict(type='string', var='word', label='word（蓝 = l，粉 = r，两端往中间扫）', cell=84, h=200,
             pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, i, v: 'red' if 'l' in S and 'r' in S and i in (S['l'], S['r']) and S['word'][S['l']] != S['word'][S['r']] else None),
        dict(type='text', fn=lambda S: (f"`word[{S['l']}] = {S['word'][S['l']]}`，`word[{S['r']}] = {S['word'][S['r']]}`" if 'l' in S and 'r' in S and 0 <= S['l'] < len(S['word']) and 0 <= S['r'] < len(S['word']) else ''), size=26),
    ],
    watch=[('word', 'word', 'pink'), ('flag', 'flag', 'green'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'for word in words': '从左往右取下一个字符串：`{word}`',
        'flag = True': '先假设 `{word}` 是回文：`flag = True`',
        'l = 0': '左指针 `l` 指向开头',
        'r = len': '右指针 `r = len(word) - 1 = {r}` 指向结尾',
        'while l < r': '`l = {l}`，`r = {r}`：{"两指针还没相遇，继续比较" if l < r else "指针相遇，没发现不同，退出循环"}',
        'if word[l]': '`word[{l}] = {word[l]}` 对 `word[{r}] = {word[r]}` → {"不同" if word[l] != word[r] else "相同"}',
        'flag = False': '字符不同 → ==这个字符串不是回文==：`flag = False`',
        'break': '不用再比了，退出 while',
        'l += 1': '`l` 右移到 {l}',
        'r -= 1': '`r` 左移到 {r}',
        'if flag': '`flag = {flag}` → {"是回文，就是它了" if flag else "不是回文，看下一个"}',
        'return word': '第一个回文串是 `{word}`，直接返回',
        'return ""': '没有回文串，返回空串',
    },
    cards=dict(
        one_liner='从左往右扫单词，两端指针往中间比，全相同就是回文',
        complexity='时间 `O(L)`，空间 `O(1)`',
        problem=['给定字符串数组，返回==第一个回文串==，没有返回 `""`',
                 '示例：`["abc","car","ada","racecar","cool"]` → `"ada"`'],
        quote='可以使用两个指针从两侧往中间同步扫，若某一时刻指向的字符不同，说明该字符串不是回文串。',
        quote_src='—— yiduobo 题解原文',
        idea=['按顺序遍历，第一个满足的直接返回',
              '`l` 从头、`r` 从尾，同步往中间走',
              '出现不同字符，`flag = False` 并 `break`；直到相遇都没不同，就是回文'],
        summary=['时间 `O(L)`，空间 `O(1)`',
                 '`while l < r`：奇数长度的中间字符不用比',
                 '`flag` 要在每个单词开头重置为 `True`',
                 '代码与原文一致，Python 3 下可直接运行（无需修改）'],
    ),
)
