CONFIG = dict(
    num=1839, title='所有元音按顺序排布的最长子字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · 哈希表收集字符',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1580'],
    code='''
class Solution(object):
    def longestBeautifulSubstring(self, word):

        char_set = set()
        start = None
        last = None
        res = 0

        for index, char in enumerate(word):
            if start is None:
                start = index
            elif char < last:
                if len(char_set) == 5:
                    res = max(res, index - start)
                start = index
                char_set = set()
            
            last = char
            char_set.add(char)
            
        if len(char_set) == 5:
            res = max(res, len(word) - start)
        
        return res
''',
    call='Solution().longestBeautifulSubstring("aeiaaeiioouu")',
    expect=9, max_steps=80,
    views=[
        dict(type='text', fn=lambda S: (f"当前子串从 `{S['start']}` 开始，已收集 ==`{len(S['char_set'])}`== 种字符" if S.get('start') is not None else ''), size=30),
        dict(type='string', var='word', cell=60, h=240, pointers={'start': 'blue', 'index': 'pink'},
             window=('start', 'index'),
             dim=lambda S, i, v: S.get('start') is not None and 'index' in S and i > S['index']),
        dict(type='set', var='char_set', label='char_set（当前子串出现过的字符）', h=200),
    ],
    watch=[('start', 'start', 'blue'), ('index', 'index', 'pink'), 'char', 'last', ('res', 'res', 'green')],
    captions={
        'char_set = set()': lambda S, B, r: ('哈希表清空：`char_set = set()`，重新收集' if 'index' in S else '`char_set` 收集当前子串里出现过的字符'),
        'start = None': '`start` 记录当前子串的起点，还没开始',
        'last = None': '`last` 是上一个字符，用来比较相邻字符的大小',
        'res = 0': '`res` 记录最长美丽子串长度',
        'start = index': lambda S, B, r: (f'第一个字符，子串从 `{S.index}` 开始' if B.start is None else f'`{S.char} < {S.last}`：下降了，单调性被打破，新子串从 `{S.index}` 开始'),
        'elif char < last': '`{char} < {last}` 吗？{"是 → 比上一个字符小，上一个子串结束了" if char < last else "否 → 没有下降，继续往后"}',
        'if len(char_set) == 5': '哈希表里有 `{len(char_set)}` 种字符 → {"五种齐全，用上一个子串长度更新答案" if len(char_set) == 5 else "不齐全，这个子串不美丽"}',
        'res = max(res, index - start)': '`res = max({B.res}, {index - start}) = {res}`',
        'last = char': '`last` 更新为 `{last}`',
        'char_set.add(char)': '`{char}` 加入哈希表，现在有 `{len(char_set)}` 种',
        'res = max(res, len(word) - start)': '遍历结束，最后一段也要检查：`res = max({B.res}, {len(word) - start}) = {res}`',
        'return res': '最长美丽子串长度 `{res}`',
    },
    cards=dict(
        one_liner='相邻字符不下降就继续，一降就结算上一段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['只含元音的字符串，美丽子串：==五个元音都出现且按字典序升序==',
                 '求最长美丽子串长度，没有则 `0`',
                 '本视频：`aeiaaeiioouu` → `9`'],
        quote='若其小于上一个字符word[index - 1]，那么说明上一个子字符串已经结束，此时需要检测哈希表中是否有全部五种字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['子串必须单调不降，所以==只比较相邻字符==即可',
              '用哈希表收集字符种类：数到 5 种，就说明五个元音齐了',
              '遇到下降：先结算上一段，再清空哈希表从当前字符重新开始'],
        summary=['时间 `O(n)`，空间 `O(1)`（哈希表至多 5 个字符）',
                 '易错：循环结束后，最后一段也要检查一次',
                 '单调不降 + 恰好 5 种字符 ⇒ 必然是 a→e→i→o→u 的顺序',
                 '对比灵神：灵神按「一组相同字母」跳着走，对照 `vowel[cur]`；yiduobo 逐字符比较大小'],
    ),
)
