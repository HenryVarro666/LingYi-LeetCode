CONFIG = dict(
    num=2284, title='最多单词数的发件人', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · split 统计', tags=[],
    code='''
class Solution(object):
    def largestWordCount(self, messages, senders):

        cnt_dict = {}
        for index in range(len(messages)):
            cnt_dict[senders[index]] = cnt_dict.get(senders[index], 0) + len(messages[index].split(' '))

        res = None
        max_cnt = 0
        for user, cnt in cnt_dict.items():
            if cnt > max_cnt or (cnt == max_cnt and user > res):
                max_cnt, res = cnt, user
        
        return res
''',
    call='Solution().largestWordCount(["Hi all","Go now","Yo you","So fun"], ["Amy","bob","Amy","bob"])',
    expect='bob',
    views=[
        dict(type='text', fn=lambda S: ('第 ' + str(S['index']) + ' 条：`' + S['messages'][S['index']] + '`，发件人 ==' + S['senders'][S['index']] + '==') if 'index' in S and S.get('_line') in (6, 7) else '', h=80),
        dict(type='map', var='cnt_dict', h=250, label='cnt_dict：发件人 → 单词数'),
        dict(type='text', fn=lambda S: ('当前答案 `res` = ==' + repr(S['res']) + '==，最大单词数 `max_cnt` = ' + str(S['max_cnt'])) if 'res' in S else '', h=80),
    ],
    watch=['index', 'user', 'cnt', ('max_cnt', 'max_cnt', 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt_dict = {}': '字典记录每个发件人发出的总单词数',
        'cnt_dict[senders[index]] =': '`"{messages[index]}"` `split(" ")` 得 `{len(messages[index].split(" "))}` 个词 → `{senders[index]}` 累计 `{cnt_dict[senders[index]]}`',
        'res = None': '`res` 记最优发件人，`max_cnt` 记目前最大单词数',
        'if cnt > max_cnt': lambda S, B, r: (f'`{S.user}` 有 {S.cnt} 词，当前最大 {S.max_cnt} → ' + ('更多，更新' if S.cnt > S.max_cnt else ('并列，且 `' + S.user + '` 字典序更大，更新' if S.cnt == S.max_cnt and S.user > S.res else '不更新'))),
        'max_cnt, res = cnt, user': '换人：`max_cnt = {max_cnt}`，`res = {res!r}`',
        'return res': '返回 `{ret!r}`',
    },
    cards=dict(
        one_liner='split 数词，字典累加，再按「词数、字典序」选最优',
        complexity='时间 `O(L)`，空间 `O(n)`',
        problem=['`messages[i]` 由 `senders[i]` 发出，单词用单个空格隔开',
                 '返回总单词数最多的发件人，并列取字典序最大',
                 '示例：Amy 与 bob 各 4 词并列 → `"bob"`'],
        quote='得到哈希表后，对哈希表中的发件人和消息数目进行一趟遍历，按题目要求找出最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`split(" ")` 得到的列表长度就是这条信息的单词数',
              '第一趟：哈希表按发件人累加单词数',
              '第二趟：更多就换人；并列且名字字典序更大也换人'],
        summary=['时间 `O(L)`，空间 `O(n)`',
                 '易错点：并列时取字典序最大；大写小于小写，`"bob" > "Amy"`',
                 '`max_cnt` 初值为 0，所有人单词数都 ≥ 1，所以 `res` 不会一直是 None',
                 '原文本身可在 Python 3 直接运行，未做修改（原文的 `res = None` 也不会参与字符串比较）'],
    ),
)
