def _hl_f(S, i, v):
    return 'yellow' if S['_line'] <= 10 and 'u' in S and 'v' in S and v == [S['u'], S['v']] else None


def _txt(S):
    if 'cnt' in S and 'x' in S:
        return '`todo` 里每个人会的每种语言 `x`，`cnt[x]` 加一'
    if 'cnt' in S:
        return '`cnt[x]` = 无法沟通的人中，会语言 `x` 的人数'
    if 'todo' in S:
        return f'已找出 {len(S["todo"])} 个必须学习的人'
    return '先看谁和朋友没有共同语言'


CONFIG = dict(
    num=1733, title='需要教语言的最少人数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='计数 · 少数服从多数',
    tags=['贪心与思维', '难度分 1984'],
    code='''
class Solution:
    def minimumTeachings(self, n: int, languages: List[List[int]], friendships: List[List[int]]) -> int:
        learned = list(map(set, languages))

        todo = set()  # 需要学语言的人
        for u, v in friendships:
            # u 和 v 减一，下标从 0 开始
            if learned[u - 1].isdisjoint(learned[v - 1]):  # 无交集
                todo.add(u - 1)
                todo.add(v - 1)

        cnt = [0] * (n + 1)
        for u in todo:
            for x in languages[u]:
                cnt[x] += 1

        return len(todo) - max(cnt)
''',
    call='Solution().minimumTeachings(3, [[2],[1,3],[1,2],[3]], [[1,4],[1,2],[3,4],[2,3]])',
    expect=2,
    views=[
        dict(type='array', var='languages', label='languages[i]（第 i 位用户会的语言，下标从 0）', cell=110, h=170),
        dict(type='array', var='friendships', label='friendships（黄 = 当前这对好友，编号从 1）', cell=130, h=170,
             color=_hl_f, index=False),
        dict(type='set', var='todo', label='todo（必须学语言的人，下标从 0）', fmt=lambda x: str(x), h=100),
        dict(type='array', var='cnt', label='cnt[x]：无法沟通的人里，会语言 x 的人数', cell=70, h=185,
             pointers={'x': 'blue'}),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    watch=[('u', 'u', 'blue'), ('v', 'v', 'pink'), ('x', 'x', 'cyan'), ('todo 人数', 'len(todo)', 'yellow')],
    captions={
        'learned = list': '把每个人会的语言转成集合，方便判断两人有没有共同语言',
        'todo = set': '`todo` 收集「和某个朋友没有共同语言」的人',
        'for u, v in friendships': lambda S, B, ret: ('好友都检查完了' if (B.get('u'), B.get('v')) == (S['u'], S['v']) else '看这一对好友：`%d` 号和 `%d` 号（编号从 1 开始）' % (S['u'], S['v'])),
        'if learned': '两人语言集合 `{learned[u - 1]}` 与 `{learned[v - 1]}` {"==无交集，沟通不了=="  if learned[u - 1].isdisjoint(learned[v - 1]) else "有交集，已经能沟通，不用管"}',
        'todo.add(u - 1)': '`{u}` 号必须学新语言，加入 `todo`',
        'todo.add(v - 1)': '`{v}` 号必须学新语言，加入 `todo`',
        'cnt = [0]': '`cnt[x]`：无法沟通的人里，有多少人已经会语言 `x`',
        'for u in todo': lambda S, B, ret: ('`todo` 里的人都统计完了' if B.get('u') == S['u'] and 'x' in B else '看 `todo` 里的 %d 号（下标从 0）：他会 %s' % (S['u'], S['languages'][S['u']])),
        'cnt[x] += 1': '这个人会语言 `{x}` → `cnt[{x}]` 变成 =={cnt[x]}==',
        'return len(todo)': '选 `cnt` 最大的语言：`max(cnt) = {max(cnt)}` 个人已会，其余 `{len(todo)} - {max(cnt)}` = =={ret}== 个人要教',
    },
    cards=dict(
        one_liner='先找出沟通不了的人，再教他们里会的人最多的那门语言',
        complexity='时间 `O(nm+nf)`，空间 `O(nm)`',
        problem=['`n` 种语言，每个用户会一些语言，好友之间要有共同语言才能沟通',
                 '只能选 ==一门== 语言教给一些用户，使所有好友都能沟通',
                 '求最少教多少人；好友关系没有传递性'],
        quote='比如有 10 个人无法沟通，其中说中文的人最多，有 8 个，那么只需教剩下的 10-8=2 个人中文（少数服从多数）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只关心 `friendships` 里的每对好友：语言集合无交集才有问题',
              '这样的两个人都进 `todo`（总数记 total）',
              '统计 `todo` 里每种语言有多少人会，选最多的 `max(cnt)`，其余人学'],
        summary=['时间 `O(nm+nf)`，空间 `O(nm)`',
                 '易错点：只能选一门语言，不能给不同的人教不同的语言',
                 '易错点：`u`、`v` 从 1 开始，要减一',
                 '灵神还给了「枚举教哪门语言」的暴力写法，本题选计数写法'],
    ),
)
