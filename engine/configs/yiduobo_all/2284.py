MSG = ["Hey Alice there", "Hi Bob", "Yo Alice", "Go Bob now", "Hey Tom"]
SND = ["Alice", "Bob", "Alice", "Bob", "Tom"]


def _txt(S):
    d = S.get('cnt_dict')
    if d is None:
        return '把每个发件人发的单词数累加到哈希表，再找最大（并列取字典序大的）'
    if 'user' in S:
        return f"当前最大 `max_cnt = {S['max_cnt']}`，发件人 `{S['res']}`"
    return ''


CONFIG = dict(
    num=2284, title='最多单词数的发件人', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表统计 · 并列取字典序大',
    tags=[],
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
    call=f'Solution().largestWordCount({MSG!r}, {SND!r})',
    expect='Bob',
    views=[
        dict(type='array', var='messages', label='messages（每条消息的单词数 = 空格数 + 1）', cell=170, h=230,
             pointers={'index': 'pink'}, font=22,
             color=lambda S, i, v: 'pink' if 'index' in S and 'user' not in S and i == S['index'] else None),
        dict(type='array', var='senders', label='senders', cell=170, h=200, font=26, index=False,
             color=lambda S, i, v: 'pink' if 'index' in S and 'user' not in S and i == S['index'] else None),
        dict(type='map', var='cnt_dict', label='cnt_dict（发件人 → 单词数）', fmt=lambda k, v: f'{k}: {v}', h=190, font=32),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'pink'), ('user', 'user', 'blue'), ('cnt', 'cnt', 'orange'), ('max_cnt', 'max_cnt', 'green'), ('res', 'res', 'green')],
    captions={
        'cnt_dict = {}': '`cnt_dict` 记录每个发件人发出的总单词数',
        'for index in range(len(messages))': '处理第 `{index}` 条消息：`{messages[index]!r}`，发件人 `{senders[index]!r}`',
        'cnt_dict[senders[index]]': '`split(\' \')` 得到 `{len(messages[index].split(\' \'))}` 个单词 → `{senders[index]}` 累计 =={cnt_dict[senders[index]]}== 个',
        'res = None': '`res` 记录当前答案（发件人），先设为空',
        'max_cnt = 0': '`max_cnt` 记录当前最大单词数，从 0 开始',
        'for user, cnt in': '检查发件人 `{user}`，单词数 `{cnt}`',
        'if cnt > max_cnt or': lambda S, B, r: (
            f'`{S.cnt} > {S.max_cnt}` → ==更多单词，成为新答案==' if S.cnt > S.max_cnt
            else (f'`{S.cnt} == {S.max_cnt}` 并列，比字典序：`{S.user!r} > {S.res!r}` → ==字典序更大，替换==' if S.cnt == S.max_cnt and S.user > S.res
                  else f'`{S.cnt}` 不超过 `{S.max_cnt}`（并列时字典序也不更大）→ 不更新')),
        'max_cnt, res = cnt, user': '更新：`max_cnt = {max_cnt}`，`res = {res!r}`',
        'return res': '单词数最多的发件人是 `{res}`',
    },
    cards=dict(
        one_liner='哈希表累加每人的单词数，并列时取字典序大的',
        complexity='时间 `O(n·L)`，空间 `O(k)`（k 个发件人）',
        problem=['`messages[i]` 是 `senders[i]` 发的消息，单词用单个空格隔开',
                 '返回发出单词数==最多==的发件人；并列时返回==字典序最大==的名字',
                 '大写字母小于小写字母，`"Alice"` 和 `"alice"` 是不同的人',
                 '本视频：Bob 和 Alice 都是 5 个单词 → `"Bob"`（字典序更大）'],
        quote='此时就可以使用哈希表统计每个发件人发送的单词数了。得到哈希表后，对哈希表中的发件人和消息数目进行一趟遍历，按题目要求找出最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：`split(\' \')` 得到单词列表，长度就是单词数，按发件人累加',
              '第二趟：遍历哈希表，单词数更大就换人',
              '单词数相同，再比较名字，字典序大的留下：`user > res`'],
        summary=['时间 `O(总字符数)`，空间 `O(发件人数)`',
                 '易错：并列要取字典序==更大==，不是更小；`res` 初始为 `None`，只在 `cnt == max_cnt` 时才比较，此时 `res` 已有值（`max_cnt` 初始 0，消息至少 1 个单词）',
                 '原文为 Python 2 风格（`items()` 等在 Python 3 同样可用），代码无需改动',
                 '对比灵神：他的思路是「空格个数 + 1 = 单词数」'],
    ),
)
