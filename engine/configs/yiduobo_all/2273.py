CONFIG = dict(
    num=2273, title='移除字母异位词后的结果数组', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='字母计数 dict 比较',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1295'],
    code='''
class Solution(object):
    def removeAnagrams(self, words):

        def get_char_dict(word):
            char_dict = {}
            for char in word:
                char_dict[char] = char_dict.get(char, 0) + 1
            return char_dict
        
        last_char_dict = get_char_dict(words[0])
        last_word = words[0]
        res = []
        for index in range(1, len(words)):
            now_char_dict = get_char_dict(words[index])
            if last_char_dict != now_char_dict:
                res.append(last_word)
                last_char_dict = now_char_dict
                last_word = words[index]
        
        res.append(last_word)
        return res
''',
    call="Solution().removeAnagrams(['abba','baba','bbaa','cd','cd'])",
    expect=['abba', 'cd'],
    views=[
        dict(type='array', var='words', pointers={'index': 'blue'}, h=250, cell=130),
        dict(type='map', var='last_char_dict', label='last_char_dict（上一段的字母计数）', h=130),
        dict(type='map', var='now_char_dict', label='now_char_dict（当前单词的字母计数）', h=130),
        dict(type='array', var='res', label='res（答案）', h=170, cell=130),
    ],
    watch=[('index', 'index', 'blue'), ('last_word', 'last_word', 'yellow')],
    captions={
        'last_char_dict = get_char_dict': '先统计第一个单词的字母次数：`{last_char_dict}`',
        'last_word = words[0]': '`last_word` 记录这一段异位词的代表：`{last_word}`',
        'for index in range': lambda S, B, r: ('单词都检查完了，循环结束' if getattr(B, 'index', None) == S.index else f'检查第 `{S.index}` 个单词 `{S.words[S.index]}`'),
        'for char in word': '读下一个字母（读完就结束）',
        'char_dict = {}': '新建空的计数 dict',
        'now_char_dict = get_char_dict': '统计 `{words[index]}` 的字母次数：`{now_char_dict}`',
        'if last_char_dict != now_char_dict': '`{last_char_dict}` 与 `{now_char_dict}`：{"次数不同 → 新的一段开始" if last_char_dict != now_char_dict else "完全相同 → 是异位词，当前单词直接删去"}',
        'res.append(last_word)': '上一段结束，把代表 `{last_word}` 放进答案',
        'last_char_dict = now_char_dict': '`last_char_dict` 换成当前单词的计数',
        'last_word = words[index]': '`last_word` 更新为 `{words[index]}`',
        'char_dict[char] =': '`{char}` 的次数 → {char_dict[char]}',
        'return char_dict': '计数完成：`{char_dict}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='把每个单词变成字母计数 dict，计数相同就是异位词',
        complexity='时间 `O(nL)`，空间 `O(L)`',
        problem=['相邻两个单词是字母异位词时，删去后一个，直到不能再删',
                 '示例：`["abba","baba","bbaa","cd","cd"]` → `["abba","cd"]`',
                 '`abba` 的计数 `{a:2, b:2}`，`baba` 也是'],
        quote='统计单词中各个字母出现的次数形成dict，然后通过判断dict是否相同来判断两个单词是否为字母异位词。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，`last_word` 记上一段的代表，`last_char_dict` 记它的计数',
              '当前单词计数不同：上一段结束，把 `last_word` 放进 `res`，再换成当前单词',
              '计数相同：当前单词是异位词，直接略过'],
        summary=['时间 `O(nL)`，空间 `O(L)`（不计结果）',
                 '遍历结束后，最后一段的 `last_word` 还没放进答案，要补一次 `res.append`',
                 '原文本身已兼容 Python 3，无需修改',
                 '对比灵神：灵神原地覆盖并用排序比较，yiduobo 新建 `res` 并用计数 dict'],
    ),
)
