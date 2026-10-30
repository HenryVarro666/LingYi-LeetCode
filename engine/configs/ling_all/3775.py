CONFIG = dict(
    num=3775, title='反转元音数相同的单词', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='按题意模拟 · 统计元音数',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1392'],
    code='''
def count_vowel(s: str) -> int:
    return sum(c in "aeiou" for c in s)

class Solution:
    def reverseWords(self, s: str) -> str:
        a = s.split()
        cnt0 = count_vowel(a[0])
        for i in range(1, len(a)):
            if count_vowel(a[i]) == cnt0:
                a[i] = a[i][::-1]
        return ' '.join(a)
''',
    call='Solution().reverseWords("book is nice moon")',
    expect='book is ecin noom',
    views=[
        dict(type='text', fn=lambda S: (f"第一个单词元音数 `cnt0 = {S['cnt0']}`" + (f"；`{S['a'][S['i']]}` 的元音数 = {sum(c in 'aeiou' for c in S['a'][S['i']])}" if 'i' in S and S['_line'] in (9, 10) else '')) if 'cnt0' in S else '', size=28),
        dict(type='array', var='a', label='a = s.split()（粉箭头 = 当前单词，元音数相同的会被原位反转）', cell=130, pointers={'i': 'pink'},
             h=260),
        dict(type='text', fn=lambda S: ('元音字母：`a e i o u`，其余字母不算'), size=24),
    ],
    watch=[('i', 'i', 'pink'), ('cnt0', 'cnt0', 'green'), ('a', 'a')],
    captions={
        'return sum': '数 `{s}` 里属于 `aeiou` 的字母 → 共 ==`{ret}`== 个',
        'a = s.split': '按空格切成单词：`a = {a}`',
        'cnt0 = count_vowel': '第一个单词 `{a[0]}` 有 ==`{cnt0}`== 个元音，后面的单词和它比',
        'for i in range': lambda S, B, r: (f"检查第 `{S.i}` 个单词 `{S.a[S.i]}`" if 'i' in S and ('i' not in B or S.i != B.i or S.get('_line') != B.get('_line')) else '单词都检查完了'),
        'if count_vowel': lambda S, B, r: (f"`{S.a[S.i]}` 的元音数 {sum(c in 'aeiou' for c in S.a[S.i])} == `cnt0 = {S.cnt0}` → ==相同，反转它==" if sum(c in 'aeiou' for c in S.a[S.i]) == S.cnt0 else f"`{S.a[S.i]}` 的元音数 {sum(c in 'aeiou' for c in S.a[S.i])} ≠ `cnt0 = {S.cnt0}` → 保持不变"),
        'a[i] = a[i][::-1]': '`{B.a[i]}` 反转成 ==`{a[i]}`==',
        "return ' '.join": '用空格拼回去：`{ret}`',
    },
    cards=dict(
        one_liner='先数第一个单词的元音，再逐个比较，相同就反转',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 是由单个空格隔开的小写单词，元音为 `a e i o u`',
                 '先数出==第一个单词==的元音数，后面的单词元音数与它相同就反转，否则不变',
                 '示例：`"book is nice"` → `"book is ecin"`；本视频加了 `moon`'],
        quote='按照题意模拟即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`count_vowel` 用生成器求和，`c in "aeiou"` 为真就加 1',
              '`cnt0` 只算一次；从下标 1 起逐个单词比较',
              '相等就 `a[i][::-1]` 原位替换，最后 `join` 回去'],
        summary=['时间 `O(n)`，空间 `O(n)`（可原地改则 `O(1)`）',
                 '易错：循环从 `1` 开始，第一个单词本身不反转',
                 '易错：元音只有 5 个小写字母，`y` 不算',
                 '题目里的 `parivontel` 变量只是干扰提示，不影响解法'],
    ),
)
