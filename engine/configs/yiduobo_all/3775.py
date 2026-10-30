CONFIG = dict(
    num=3775, title='反转元音数相同的单词', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='模拟 · split + 元音计数函数',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1392'],
    code='''
class Solution(object):
    def reverseWords(self, s):
        
        words = s.split()
        res = [words[0]]

        vowel = set(['a', 'e', 'i', 'o', 'u'])

        def count(w):
            v = 0
            for c in w:
                if c in vowel:
                    v += 1
            return v

        cnt = count(words[0])

        for w in words[1:]:
            if count(w) == cnt:
                res.append(w[::-1])
            else:
                res.append(w)
        
        return ' '.join(res)
''',
    call='Solution().reverseWords("book is nice moon")',
    expect='book is ecin noom',
    views=[
        dict(type='array', var='words', label='words = s.split()', cell=110, h=190,
             color=lambda S, k, v: 'pink' if S.get('w') == v and S.get('_line', 0) >= 18 else None),
        dict(type='array', var='res', label='res（答案：反转过的单词或原样单词）', cell=110, h=190,
             color=lambda S, k, v: 'green' if S.get('_line') in (20, 22) and k == len(S['res']) - 1 else None),
        dict(type='set', var='vowel', label='元音集合', h=110),
    ],
    watch=[('cnt', 'cnt', 'green'), ('w', 'w', 'pink'), ('v', 'v', 'yellow')],
    captions={
        'words = s.split': '`s.split()` 分出各个单词：`{words}`',
        'res = [words[0]]': '第一个单词不管怎样都原样进答案：`res = {res}`',
        'vowel = set': '用集合存元音，判断 `c in vowel` 很快',
        'v = 0': lambda S, B, r: f"开始数 `{S.w}` 里的元音，`v = 0`",
        'for c in w': '取 `{w}` 的下一个字母（取完就结束循环）',
        'if c in vowel': '这个字母是元音吗？在 `vowel` 集合里才算',
        'v += 1': '元音数 `v` → ==`{v}`==',
        'return v': '`{w}` 的元音数是 ==`{ret}`==',
        'cnt = count': '第一个单词 `{words[0]}` 的元音数：`cnt = {cnt}`',
        'for w in words': lambda S, B, r: (f"检查后续单词 `{S.w}`" if 'w' in S and ('w' not in B or S.w != B.w) else '所有后续单词都处理完了'),
        'res.append(w[::-1])': lambda S, B, r: f"`{S.w}` 元音数 {sum(ch in 'aeiou' for ch in S.w)} == `cnt = {S.cnt}` → ==相同，反转==后加入：`{S.res}`",
        'res.append(w)': lambda S, B, r: f"`{S.w}` 元音数 {sum(ch in 'aeiou' for ch in S.w)} ≠ `cnt = {S.cnt}` → 原样加入：`{S.res}`",
        'return \'': '用空格连起来：`{ret}`',
    },
    cards=dict(
        one_liner='split 分词，数元音，相同的反转后放进答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 由小写单词组成，单词间一个空格；元音为 `a e i o u`',
                 '求==第一个单词==的元音数；后面的单词元音数相同则反转，否则不变',
                 '示例：`"cat and mice"` → `"cat dna mice"`；本视频：`"book is nice moon"`'],
        quote='直接按照题目要求模拟计算即可。先对字符串进行split操作，分离出各个单词。接下来遍历第一个单词，统计其中元音字母的数量v。',
        quote_src='—— yiduobo 题解原文',
        idea=['`split()` 之后，`count(w)` 统计单词里的元音',
              '第一个单词原样放进 `res`，并记下它的元音数 `cnt`',
              '对 `words[1:]` 逐个比较：相同就 `w[::-1]` 加入，不同就原样加入'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：第一个单词要先放入 `res`，再遍历 `words[1:]`',
                 '元音存入 `set`，查找是 `O(1)`',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神直接在 `a` 上原位替换，yiduobo 另建结果列表 `res`'],
    ),
)
