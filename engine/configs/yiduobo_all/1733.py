def _hl_f(S, i, v):
    return 'yellow' if S['_line'] >= 9 and S['_line'] <= 21 and 'x' in S and 'y' in S and v == [S['x'] + 1, S['y'] + 1] else None


def _txt(S):
    L = S['_line']
    if L <= 6:
        return '`learned_set[k]`：会第 `k+1` 门语言的用户集合（用户编号从 0）'
    if L <= 21:
        if 'language' in S and 'flag' in S and not S['flag'] is None:
            return f'检查第 `{S["language"] + 1}` 门语言：用户 {S["x"]} 和 {S["y"]} 是否都会'
        return f'检查好友 ({S["x"]}, {S["y"]})（已减一）：有没有一门两人都会的语言'
    return f'`user_set` = {sorted(S["user_set"])}：这些人必须学新语言；`language_cnt` 统计他们各自已会的语言'


CONFIG = dict(
    num=1733, title='需要教语言的最少人数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='枚举好友 + 哈希统计',
    tags=['贪心与思维', '难度分 1984'],
    code='''
class Solution(object):
    def minimumTeachings(self, n, languages, friendships):

        learned_set = [set() for _ in range(n)]
        for user_id, user_language in enumerate(languages):
            for language in user_language:
                learned_set[language - 1].add(user_id)
        
        user_set = set()
        for x, y in friendships:
            x -= 1
            y -= 1
            flag = False
            for language in range(n):
                if x in learned_set[language] and y in learned_set[language]:
                    flag = True
                    break
            
            if not flag:
                user_set.add(x)
                user_set.add(y)

        language_cnt = {}
        for user in user_set:
            for language in languages[user]:
                language_cnt[language] = language_cnt.get(language, 0) + 1

        if not language_cnt:
            return 0

        return len(user_set) - max(language_cnt.values())
''',
    call='Solution().minimumTeachings(2, [[1],[2],[1,2]], [[1,2],[1,3],[2,3]])',
    expect=1,
    views=[
        dict(type='array', var='languages', label='languages[i]：第 i 位用户会的语言', cell=110, h=150),
        dict(type='array', var='learned_set', label='learned_set[k]：会第 k+1 门语言的用户（编号从 0）', cell=150, h=150,
             pointers={'language': 'blue'}),
        dict(type='set', var='user_set', label='user_set：必须学新语言的人', fmt=lambda x: str(x), h=100),
        dict(type='map', var='language_cnt', label='language_cnt：user_set 里会各语言的人数', fmt=lambda k, v: f'语言 {k}: {v} 人', h=130),
        dict(type='text', h=100, size=26, fn=_txt),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('language', 'language', 'cyan'), ('flag', 'flag', 'yellow')],
    captions={
        'learned_set = [': '为每门语言建一个集合，装「会这门语言的用户」',
        'for user_id, user_language': lambda S, B, ret: '所有用户都登记完了' if B.get('user_id') == S['user_id'] else '看用户 `%d`，他会语言 `%s`' % (S['user_id'], S['user_language']),
        'for language in user_language': lambda S, B, ret: '这个用户的语言都登记完了' if S['user_id'] in S['learned_set'][S['language'] - 1] else '他会语言 `%d`' % S['language'],
        'learned_set[language - 1].add': '用户 `{user_id}` 会语言 `{language}` → 加进 `learned_set[{language - 1}]`',
        'user_set = set': '`user_set` 收集「和某个朋友没有共同语言」的人',
        'x -= 1': '好友编号从 1 开始，减一：`x = {x}`',
        'y -= 1': '好友编号从 1 开始，减一：`y = {y}`',
        'flag = False': '先假设这对好友 `({x}, {y})` 没有共同语言',
        'for language in range': lambda S, B, ret: '这对好友的所有语言都查完了，没有共同语言' if (S['language'] == S['n'] - 1 and B.get('language') == S['language']) else '检查第 `%d` 门语言' % (S['language'] + 1),
        'if x in learned_set': '用户 {x} 和 {y} 是否都会第 {language + 1} 门语言：{"==都会，有共同语言==" if (x in learned_set[language] and y in learned_set[language]) else "不是都会，换下一门"}',
        'flag = True': '找到共同语言，`flag = True`，这对好友不用额外学习',
        'break': '不用再找了，跳出语言循环',
        'if not flag': '{"==没有任何共同语言==，两人都要学" if not flag else "这对好友已经能沟通，跳过"}',
        'user_set.add(x)': '用户 `{x}` 必须学习新语言 → 加入 `user_set`',
        'user_set.add(y)': '用户 `{y}` 必须学习新语言 → 加入 `user_set`',
        'language_cnt = {}': '接着统计：`user_set` 里的人各会哪些语言，各有多少人',
        'for user in user_set': lambda S, B, ret: '`user_set` 里的人都统计完了' if sum(S['language_cnt'].values()) == sum(len(S['languages'][u]) for u in S['user_set']) else '看 `user_set` 里的用户 `%d`，他会 `%s`' % (S['user'], S['languages'][S['user']]),
        'for language in languages[user]': lambda S, B, ret: ('这个用户的语言都统计完了' if sum(S['language_cnt'].values()) == sum(len(S['languages'][u]) for u in list(S['user_set'])[:list(S['user_set']).index(S['user']) + 1]) else '他会语言 `%d`' % S['language']),
        'language_cnt[language] =': '语言 `{language}` 又多一个人会 → `{language_cnt[language]}`',
        'if not language_cnt': '{"`language_cnt` 空 → 没有人需要学，直接返回 0" if not language_cnt else "`language_cnt` 不空，继续"}',
        'return len': '人数最多的语言有 `{max(language_cnt.values())}` 人已会；`user_set` 共 `{len(user_set)}` 人 → 教 `{len(user_set)} - {max(language_cnt.values())}` = =={ret}== 人',
    },
    cards=dict(
        one_liner='找出沟通不了的人，教他们里最多人会的那门语言',
        complexity='时间 `O(f·n + m)`，空间 `O(n·m)`',
        problem=['`n` 种语言，每位用户会一些语言，只有共同语言才能沟通',
                 '可以选 ==一门== 语言教给一些用户，让所有好友都能沟通',
                 '好友关系没有传递性；示例：`n=2` → `1`'],
        quote='如果没有一种语言是两个人都会的，那么这两个人就需要学习额外的语言，在这里可以使用一个集合user_set来记录所有需要额外学习语言的人。',
        quote_src='—— yiduobo 题解',
        idea=['每对好友枚举每种语言，借 `learned_set` 哈希集合判断两人是否都会',
              '没有共同语言的两人都放进 `user_set`',
              '再让他们学其中会的人最多的语言：答案 = `len(user_set) - max_user`'],
        summary=['时间 `O(f·n + m·n)`，空间 `O(n·m)`（`f` 好友对数，`m` 用户数）',
                 '易错点：编号从 1 开始，要先 `-= 1`',
                 '易错点：`user_set` 为空要返回 0（否则 `max` 空序列报错）',
                 '只能教一门语言：所以统计「哪门语言已会的人最多」'],
    ),
)
