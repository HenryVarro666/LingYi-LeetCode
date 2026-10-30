CONFIG = dict(
    num=2108, title='找出数组中的第一个回文字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='相向双指针判回文',
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
    call='Solution().firstPalindrome(["abc","car","ada","racecar"])',
    expect='ada',
    views=[
        dict(type='array', var='words', label='words（蓝 = 正在检查，灰 = 已排除）', cell=150, h=200, font=30,
             color=lambda S, i, v: ('green' if S.get('flag') else 'blue') if S.get('word') == v and i == S['words'].index(v) else None,
             dim=lambda S, i, v: 'word' in S and i < S['words'].index(S['word'])),
        dict(type='string', var='word', label='word（左右指针向中间靠拢）', cell=84, h=230,
             pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, i, v: 'green' if (S.get('flag') and S.get('l', 0) > S.get('r', 0)) else None),
        dict(type='text', h=70, size=28,
             fn=lambda S: '`flag = %s`：%s' % (S['flag'], '到目前为止两侧字符都相同' if S['flag'] else '发现不同，不是回文')
             if 'flag' in S else ''),
    ],
    watch=[('word', 'word', 'blue'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('flag', 'flag', 'yellow')],
    captions={
        'for word in words': lambda S, B, r: (f'检查第 `{S.words.index(S.word)}` 个字符串 `{S.word}`'
                                              if S.get('word') != B.get('word') or 'word' not in B else '遍历完了'),
        'flag = True': '先假设 `word` 是回文：`flag = True`',
        'l = 0': '`l` 从最左边出发',
        'r = len(word) - 1': '`r` 从最右边出发，`r = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，还没相遇，继续比较' if S.l < S.r
                                        else f'`l = {S.l} ≥ r = {S.r}`：两指针相遇，全部配对成功'),
        'if word[l] != word[r]': lambda S, B, r: (
            f"`word[{S.l}] = '{S.word[S.l]}'` ≠ `word[{S.r}] = '{S.word[S.r]}'` → ==不同=="
            if S.word[S.l] != S.word[S.r] else f"`word[{S.l}] = '{S.word[S.l]}'` == `word[{S.r}] = '{S.word[S.r]}'` → 这一对相同"),
        'flag = False': '有一对字符不同 → `flag = False`，不是回文',
        'break': '不用再比了，跳出 while，检查下一个字符串',
        'l += 1': '`l` 右移 → {l}',
        'r -= 1': '`r` 左移 → {r}',
        'if flag': lambda S, B, r: (f'`flag = True`：`{S.word}` 是回文 → 它就是第一个' if S.flag
                                    else f'`flag = False`：`{S.word}` 不是回文，看下一个'),
        'return word': '返回第一个回文字符串 `{word}`',
    },
    cards=dict(
        one_liner='从左往右逐个检查，两个指针从两侧往中间扫',
        complexity='时间 `O(L)`（L 为所有字符总数），空间 `O(1)`',
        problem=['返回 `words` 中第一个回文字符串，没有就返回 `""`',
                 '示例：`["abc","car","ada","racecar","cool"]` → `"ada"`',
                 '本视频：`["abc","car","ada","racecar"]` → `"ada"`'],
        quote='具体的判断方法可以使用两个指针从两侧往中间同步扫，若某一时刻指向的字符不同，说明该字符串不是回文串。若直到两个指针相遇都没有出现字符不同的情况，则说明这个字符串是回文字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层 `for` 从左往右，所以找到的第一个回文就是答案',
              '内层 `l`、`r` 相向而行，比较对称位置的字符',
              '`flag` 记录有没有出现不同，不同就 `break`'],
        summary=['时间 `O(L)`，空间 `O(1)`',
                 '`while l < r`：中间那个字符不用和自己比',
                 '一旦 `flag` 为真立刻 `return`，保证返回的是第一个',
                 '都不是回文时返回空串 `""`，不是 `None`',
                 '原文为 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
