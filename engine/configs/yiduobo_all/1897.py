CONFIG = dict(
    num=1897, title='重新分配字符使所有字符串都相等', difficulty='Easy', category='字符串',
    author='yiduobo', technique='字符计数 · 次数整除 n',
    tags=[],
    code='''
class Solution:
    def makeEqual(self, words):

        cnt_dict = {}
        for word in words:
            for char in word:
                cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        for cnt in cnt_dict.values():
            if cnt % len(words) != 0:
                return False
        
        return True
''',
    call='Solution().makeEqual(["abc", "aabc", "bc"])',
    expect=True,
    views=[
        dict(type='array', var='words', label='words（共 n 个字符串）', cell=150, h=170,
             pointers={'words.index(word)': 'blue'}, pointer_labels={'words.index(word)': 'word'}),
        dict(type='string', var='word', label='当前字符串 word', cell=90, h=170, pointers={'word.index(char)': 'pink'}),
        dict(type='map', var='cnt_dict', label='cnt_dict（每种字符的总次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
        dict(type='text', size=28, h=80, fn=lambda S: (
            f"`n = len(words) = {len(S['words'])}`：每种字符的次数都必须是 {len(S['words'])} 的倍数"
            if 'cnt' not in S else
            f"检查 `cnt = {S['cnt']}`：`{S['cnt']} % {len(S['words'])} = {S['cnt'] % len(S['words'])}`")),
    ],
    watch=[('word', 'word', 'blue'), ('char', 'char', 'pink'), ('cnt', 'cnt', 'orange'), ('n', 'len(words)')],
    captions={
        'cnt_dict = {}': '先准备一个字典，统计所有字符串里每种字符的==总次数==',
        'for word in words': '取下一个字符串 `word`',
        'for char in word': '逐个看 `word` 里的字符 `char`',
        'cnt_dict[char]': '`char = {char!r}` 的总次数加一 → `cnt_dict[{char!r}] = {cnt_dict[char]}`',
        'for cnt in cnt_dict.values()': '统计完了，逐种字符检查它的总次数 `cnt`',
        'if cnt % len(words)': lambda S, B, ret: (
            f'`{S.cnt} % {len(S.words)} = {S.cnt % len(S.words)}` ≠ 0 → 这种字符==无法平均分==给每个字符串，返回 False'
            if S.cnt % len(S.words) != 0 else
            f'`{S.cnt} % {len(S.words)} = 0` → 可以平均分给 {len(S.words)} 个字符串，继续检查'),
        'return False': '有字符分不匀，不可能让所有字符串相等 → `False`',
        'return True': '每种字符的次数都是 n 的倍数，平均分配后所有字符串相等 → `True`',
    },
    max_steps=60,
    cards=dict(
        one_liner='每种字符的总次数都是 n 的倍数，就能分匀',
        complexity='时间 `O(L)`（L 为字符总数），空间 `O(26)`',
        problem=['可以把任一字符串的任一字符移到别的字符串的任意位置',
                 '问：能否让 `words` 中所有字符串变得==完全相同==',
                 '示例：`["abc","aabc","bc"]` → `true`；`["ab","a"]` → `false`'],
        quote='由于题目可以任意调整字符串的构成，那么只需要每种字符出现的次数都是n的倍数，就可以将当前字符平均分配到各个字符串上的同一位置，从而使得所有字符串都相等。',
        quote_src='—— yiduobo 题解',
        idea=['移动字符不改变字符的==总次数==，所以只看总次数',
              '每种字符平均分给 `n` 个字符串，每个字符串各得 `cnt / n` 个',
              '分不匀（`cnt % n != 0`）就一定做不到'],
        summary=['时间 `O(L)`，空间 `O(26)`',
                 '易错：`n` 是字符串个数 `len(words)`，不是字符串长度',
                 '只有一个字符串时 `n = 1`，任何次数都整除，必为 True',
                 '同类题：统计频次再判断整除性'],
    ),
)
