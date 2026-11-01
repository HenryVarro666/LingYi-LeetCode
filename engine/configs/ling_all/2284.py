CONFIG = dict(
    num=2284, title='最多单词数的发件人', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数 · 数空格（Go 原文转写）', tags=[],
    code='''
class Solution:
    def largestWordCount(self, messages: List[str], senders: List[str]) -> str:
        ans = ""
        cnt = Counter()
        for i, msg in enumerate(messages):
            cnt[senders[i]] += msg.count(" ") + 1
        for s, c in cnt.items():
            if c > cnt[ans] or c == cnt[ans] and s > ans:
                ans = s
        return ans
''',
    call='Solution().largestWordCount(["Hi all","Go now","Yo you","So fun"], ["Amy","bob","Amy","bob"])',
    expect='bob',
    views=[
        dict(type='text', fn=lambda S: ('第 ' + str(S['i']) + ' 条：`' + S['msg'] + '`，发件人 ==' + S['senders'][S['i']] + '==') if 'msg' in S and 'i' in S and S.get('_line') in (6, 7) else '', h=80),
        dict(type='map', var='cnt', h=250, label='cnt：发件人 → 单词数'),
        dict(type='text', fn=lambda S: ('当前答案 `ans` = ==' + repr(S['ans']) + '==') if 'ans' in S else '', h=80),
    ],
    watch=['s', 'c', ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter()': '哈希表 `cnt` 记录每个发件人的单词数',
        'ans = ""': '答案先设为空串；`cnt` 里查不到的人次数当 0',
        'cnt[senders[i]] +=': '空格数 + 1 = 单词数：`"{msg}"` 有 `{msg.count(" ") + 1}` 个词 → `{senders[i]}` 累计 `{cnt[senders[i]]}`',
        'if c > cnt[ans]': lambda S, B, r: (f'`{S.s}` 有 {S.c} 词，当前最多 `{S.ans!r}` 有 {S.cnt[S.ans]} 词 → ' + ('更多，更新' if S.c > S.cnt[S.ans] else ('并列，且 `' + S.s + '` 字典序更大（小写 > 大写），更新' if S.c == S.cnt[S.ans] and S.s > S.ans else '不更新'))),
        'ans = s': '`ans` 换成 `{ans!r}`',
        'return ans': '单词数最多（并列取字典序最大）的发件人：`{ret!r}`',
    },
    cards=dict(
        one_liner='空格数加一就是单词数，哈希表累加，再取最大',
        complexity='时间 `O(L)`，空间 `O(n)`（L 为所有信息的总长度）',
        problem=['`messages[i]` 是 `senders[i]` 发的信息，单词由单个空格隔开',
                 '返回发出单词数最多的发件人，并列取字典序最大',
                 '示例：Amy 与 bob 各 4 词并列 → `"bob"`（小写 > 大写）'],
        quote='空格个数加一即为单词个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不用 `split`：数一下空格，`count(" ") + 1` 就是单词数',
              '哈希表 `cnt` 累加每个发件人的单词数',
              '遍历时 `c > cnt[ans]` 或（相等且 `s > ans`）就更新答案，一遍搞定最大值和字典序'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`map[string]int` → `Counter`（缺失键读出 0，和 Go 一致）',
                 '复杂度：时间 `O(L)`，空间 `O(n)`',
                 '易错点：并列时取字典序最大；大写字母小于小写字母，`"bob" > "Amy"`',
                 '开头 `ans = ""` 配合 `cnt[""] = 0`，让第一个发件人一定能更新答案'],
    ),
)
