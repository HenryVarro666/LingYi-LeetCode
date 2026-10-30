ACC = [["John", "a@m", "b@m"], ["Mary", "c@m"], ["John", "b@m"]]


def _emails(S):
    el = S.get('email_list')
    if not el:
        return '邮箱编号：（还没有）'
    return '邮箱编号：' + '　'.join(f'`{i}`={e}' for i, (e, o) in enumerate(el))


def _col(S, i, v):
    return ['blue', 'pink', 'green', 'purple'][(v - 1) % 4] if v else None


CONFIG = dict(
    num=721, title='账户合并', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='邮箱当节点 · 染色求连通',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def accountsMerge(self, accounts):

        email_dict = {}
        email_list = []
        g = {}
        for account in accounts:
            owner = account[0]
            for email in account[1:]:
                if email not in email_dict:
                    email_dict[email] = len(email_list)
                    email_list.append([email, owner])
        
            for email_a in account[1:]:
                num_a = email_dict[email_a]
                if num_a not in g:
                    g[num_a] = []
                for email_b in account[1:]:
                    num_b = email_dict[email_b]
                    if num_a != num_b:
                        g[num_a].append(num_b)

        color = [0] * len(email_dict)

        now = 1
        for index in range(len(email_dict)):
            if color[index] == 0:
                self.dfs(index, now, color, g)
                now += 1
        
        res = {}
        for index, [email, owner] in enumerate(email_list):
            if color[index] not in res:
                res[color[index]] = [owner]
            res[color[index]].append(email)

        return [[x[0]] + sorted(x[1:]) for x in res.values()]

    def dfs(self, num, now, color, g):
        color[num] = now
        for next in g[num]:
            if color[next] == 0:
                self.dfs(next, now, color, g)
''',
    call=f'Solution().accountsMerge({ACC!r})',
    expect=[["John", "a@m", "b@m"], ["Mary", "c@m"]],
    views=[
        dict(type='text', fn=_emails, h=70, size=28),
        dict(type='map', var='g', label='g（邮箱编号 → 同一账户里的其他邮箱编号）', fmt=lambda k, v: f'{k}: {v}', h=150, font=28),
        dict(type='array', var='color', label='color（0 = 未染色，相同数字 = 同一个人）', h=170,
             color=lambda S, i, v: _col(S, i, v)),
        dict(type='calls', h=170),
    ],
    watch=[('now', 'now', 'orange'), ('index', 'index', 'blue'), ('num', 'num', 'blue'), ('next', 'next', 'pink'), ('res', 'res', 'green')],
    captions={
        'email_dict[email] = len': '新邮箱 `{email}` 编号 `{email_dict[email]}`（邮箱是唯一的，当图中的点）',
        'email_list.append': '记下 `{email_list[-1]}`：邮箱和它的主人',
        'num_a = email_dict': '邮箱 `{email_a}` 的编号是 `{num_a}`',
        'g[num_a] = []': '给点 `{num_a}` 准备邻接表',
        'num_b = email_dict': '同账户的另一个邮箱 `{email_b}`，编号 `{num_b}`',
        'g[num_a].append(num_b)': lambda S, B, ret: f'同一账户的邮箱两两连边：`{S.num_a}` — `{S.num_b}` → `g[{S.num_a}] = {S.g[S.num_a]}`',
        'for account in accounts': lambda S, B, ret: ('所有账户处理完，图建好了：`b@m` 把账户 0 和 2 的邮箱连在一起' if 'account' in B and S.account == B.account
                                                      else '处理账户 `%s`：邮箱编号，同账户邮箱两两连边（已有编号的邮箱直接复用）' % S.account),
        'color = [0]': '`color` 全 0：所有邮箱还没染色',
        'now = 1': '`now` 是当前要用的颜色，从 1 开始',
        'for index in range': lambda S, B, ret: f'看邮箱 `{S.index}` 是否已染色',
        'if color[index] == 0': lambda S, B, ret: (f'`color[{S.index}] = 0`：没染过 → ==新的一个人==，用颜色 {S.now} 去染' if S.color[S.index] == 0
                                                   else f'`color[{S.index}] = {S.color[S.index]}`：已被染过，跳过'),
        'self.dfs(index': '从 `{index}` 出发 DFS，把相连的点都染成 `{now}`',
        'now += 1': '这个人染完了，下一个人换颜色 → `now = {now}`',
        'color[num] = now': '点 `{num}` 染成颜色 `{now}`',
        'for next in g[num]': lambda S, B, ret: f'看 `{S.num}` 的邻居 `{S.next}`',
        'if color[next] == 0': lambda S, B, ret: (f'邻居 `{S.next}` 还没染色 → 它和 `{S.num}` 是同一个人，继续染' if S.color[S.next] == 0
                                                  else f'邻居 `{S.next}` 已经染成 {S.color[S.next]}，不用再走'),
        'self.dfs(next': '递归到邻居 `{next}`',
        'res = {}': '`res` 按颜色收集：颜色 → [主人, 邮箱…]',
        'for index, [email, owner]': '处理邮箱 `{email}`，颜色 `{color[index]}`',
        'if color[index] not in res': lambda S, B, ret: (f'颜色 {S.color[S.index]} 第一次出现 → 先放名字 `{S.owner}`' if S.color[S.index] not in S.res
                                                         else f'颜色 {S.color[S.index]} 已有，直接加邮箱'),
        'res[color[index]].append(email)': '`{email}` 归入颜色 `{color[index]}` → `{res[color[index]]}`',
        'return [[x[0]]': '同色邮箱合成一个账户：名字 + `sorted(邮箱)` → `{ret}`',
    },
    skip=['num_a = email_dict', 'num_b = email_dict', 'email_list.append', 'g[num_a] = []', 'email_dict[email] = len', 'for email in account', 'owner = account', 'if email not in email_dict', 'for email_a in account', 'if num_a not in g', 'for email_b in', 'if num_a != num_b'],
    max_steps=110,
    cards=dict(
        one_liner='把邮箱当点，同账户邮箱两两连边，染色即合并',
        complexity='时间 约 `O(L·k + L log L)`（k 为账户邮箱数 ≤ 10），空间 `O(L)`',
        problem=['每个账户 = 名字 + 邮箱；有共同邮箱的账户是同一个人，要合并',
                 '合并后邮箱按字符顺序排序，账户顺序任意',
                 '本视频：账户 0、2 共有 `b@m` → 合并 `John`，`Mary` 独立（邮箱已缩短）'],
        quote='由于题目中的email都是独一无二的，因此可以将每个email视为图中的一个点，对于同一个用户下的email，将这些email两两之间用边连起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['点是==邮箱==（不是账户）；同一账户内的邮箱两两连边',
              '共有邮箱把两个账户的邮箱连到一起 → 连通 = 同一个人',
              '对每个未染色的点 DFS，染上新颜色；最后按颜色分组、排序'],
        summary=['同账户邮箱两两连边，边数较多，但每账户邮箱 ≤ 10，可接受',
                 '`now` 每处理完一个连通块才加一',
                 '最后输出前要 `sorted(x[1:])`，名字 `x[0]` 放最前',
                 '原文代码在 Python 3 下无需改动',
                 '对比灵神：灵神以账户为点、邮箱为桥做 DFS；这里直接以邮箱为点'],
    ),
)
