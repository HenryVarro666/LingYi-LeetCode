def _letters(x):
    return ''.join(chr(97 + i) for i in range(26) if x >> i & 1)


def _top(S):
    if 'word' not in S or 'mask' not in S:
        return '位运算：用一个整数的 26 位表示“有哪些字母”'
    return f"当前 `{S['word']!r}` 的字母集合 `mask` = =={_letters(S['mask'])}==（{S['mask']}）"


CONFIG = dict(
    num=2135, title='统计追加字母可以获得的单词数', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='位掩码 + 哈希集合 · 枚举去掉一个字符',
    tags=[],
    code='''
class Solution:
    def wordCount(self, startWords: List[str], targetWords: List[str]) -> int:
        s = set()
        for word in startWords:
            mask = 0
            for ch in word:
                mask |= 1 << (ord(ch) - ord('a'))
            s.add(mask)
        ans = 0
        for word in targetWords:
            mask = 0
            for ch in word:
                mask |= 1 << (ord(ch) - ord('a'))
            for ch in word:
                if mask ^ (1 << (ord(ch) - ord('a'))) in s:  # 去掉这个字符
                    ans += 1
                    break
        return ans
''',
    call='Solution().wordCount(["ant","tack","act"], ["tack","act","acti"])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=28, h=60),
        dict(type='array', var='startWords', label='startWords', cell=110, h=190),
        dict(type='array', var='targetWords', label='targetWords', cell=110, h=190,
             pointers={'targetWords.index(word) if word in targetWords else -1': 'blue'} if False else {}),
        dict(type='set', var='s', label='s（startWords 的字母集合）', fmt=lambda x: f'{_letters(x)}', h=130, font=34),
    ],
    watch=[('word', 'word', 'blue'), ('ch', 'ch'), ('mask', 'mask', 'purple'), ('ans', 'ans', 'green')],
    captions={
        's = set()': '`s` 存 startWords 每个单词的==字母集合==',
        'mask = 0': '`mask = 0`：空集合',
        'mask |= 1 <<': '字母 `{ch}` 对应第 `{ord(ch) - 97}` 位，置 1 → `mask` = {mask}',
        's.add(mask)': '`{word}` 的集合 =={_letters(mask)}== 入集合 `s`',
        'ans = 0': '开始统计 targetWords',
        'for word in targetWords': lambda S, B, ret: (f'检查目标单词 `{S.word}`' if 'word' in S and S.word != B.get('word') else '全部检查完'),
        'if mask ^': lambda S, B, ret: (f"去掉 `{S.ch}` 后得到 =={_letters(S.mask ^ (1 << (ord(S.ch) - 97)))}==，在 `s` 中 → ==有对应的起始单词，追加 {S.ch} 即可=="
                                        if S.mask ^ (1 << (ord(S.ch) - 97)) in S.s
                                        else f"去掉 `{S.ch}` 后得到 =={_letters(S.mask ^ (1 << (ord(S.ch) - 97)))}==，不在 `s` 中"),
        'ans += 1': '`{word}` 可由某个起始单词追加一个字母得到：`ans` → {ans}',
        'break': '已经找到一种，不用再试其他字符',
        'return ans': '共有 `{ans}` 个目标单词可以得到',
    },
    cards=dict(
        one_liner='重排不影响，只看字母集合：去掉一个字母，能否还原成起始单词',
        complexity='时间 `O(L)`（L 为所有字符总数），空间 `O(n)`',
        problem=['对 `startWords` 的某个单词追加一个新字母并任意重排，能否得到 `targetWords` 中的单词',
                 '返回 `targetWords` 中能得到的单词个数',
                 '示例：`["ant","act","tack"]`，`["tack","act","acti"]` → `2`'],
        quote='代码实现时，我们并不需要排序每个字符串，而是记录每个字符是否出现过，这可以用位运算实现。',
        quote_src='—— 灵茶山艾府题解',
        idea=['任意重排 + 无重复字母 → 单词等价于它的==字母集合==，用 26 位整数表示',
              '把 startWords 的集合都放进哈希集合',
              '对每个目标单词，枚举去掉哪个字母（异或该位），看结果在不在集合里'],
        summary=['时间 `O(L)`，空间 `O(n)`',
                 '关键前提：每个单词内字母不重复，所以异或去掉一位恰好是“去掉这个字母”',
                 '`act` 在 startWords 中但不能直接匹配 `act`：必须追加一个字母，所以要去掉一位再查',
                 '题解里也提到另一种思路：排序后哈希，掩码写法更快'],
    ),
)
