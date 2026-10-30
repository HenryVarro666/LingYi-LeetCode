ACC = [["John", "a@m", "b@m"], ["Mary", "c@m"], ["John", "a@m", "d@m"]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    acc = S.get('accounts')
    if acc is None:
        return
    vis = S.get('vis')
    es = S.get('email_set') or set()
    cv.text((x0 + 18, y0 + 4), 'accounts（绿 = 已访问账户，黄 = 已收集的邮箱，蓝框 = 当前账户）', 22, T['muted'], bold=True)
    rh = min(70, (y1 - y0 - 50) / max(1, len(acc)))
    cur = S.get('_inner', {}).get('i') if 9 <= S.get('_line', 0) <= 16 else None
    for i, a in enumerate(acc):
        Y = y0 + 44 + i * rh
        seen = bool(vis and vis[i])
        cv.rect((x0 + 18, Y, x1 - 18, Y + rh - 8), fill=T['panel2'], r=8)
        if seen:
            cv.rect((x0 + 18, Y, x0 + 26, Y + rh - 8), fill=T['green'], r=3)
        if cur == i:
            cv.rect((x0 + 18, Y, x1 - 18, Y + rh - 8), outline=T['blue'], width=4, r=8)
        cv.text((x0 + 40, Y + (rh - 8) / 2), f'{i}: {a[0]}', 26, T['text'], anchor='lm', bold=True)
        X = x0 + 230
        for e in a[1:]:
            col = T['yellow'] if e in es else T['muted']
            cv.text((X, Y + (rh - 8) / 2), e, 26, col, anchor='lm', bold=e in es, mono=True)
            X += 130


CONFIG = dict(
    num=721, title='账户合并', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='邮箱建图 · DFS 求连通块',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        email_to_idx = defaultdict(list)
        for i, account in enumerate(accounts):
            for email in account[1:]:
                email_to_idx[email].append(i)

        def dfs(i: int) -> None:
            vis[i] = True
            for email in accounts[i][1:]:  # 遍历 i 的所有邮箱地址
                if email in email_set:
                    continue
                email_set.add(email)
                for j in email_to_idx[email]:  # 遍历所有包含该邮箱地址的账户下标 j
                    if not vis[j]:  # j 没有访问过
                        dfs(j)

        ans = []
        vis = [False] * len(accounts)
        for i, b in enumerate(vis):
            if not b:  # i 没有访问过
                email_set = set()  # 用于收集 DFS 中访问到的邮箱地址
                dfs(i)
                ans.append([accounts[i][0]] + sorted(email_set))
        return ans
''',
    call=f'Solution().accountsMerge({ACC!r})',
    expect=[["John", "a@m", "b@m", "d@m"], ["Mary", "c@m"]],
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='map', var='email_to_idx', label='email_to_idx（邮箱 → 含它的账户下标）', fmt=lambda k, v: f'{k}: {v}', h=140, font=26),
        dict(type='array', var='vis', label='vis', h=170),
        dict(type='calls', h=180),
    ],
    watch=[('i', 'i', 'blue'), ('email', 'email'), ('j', 'j', 'pink'), ('email_set', 'email_set', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'email_to_idx[email].append(i)': '邮箱 `{email}` 出现在账户 `{i}` → `email_to_idx[{email!r}] = {email_to_idx[email]}`',
        'vis[i] = True': '账户 `{i}` 标记为已访问',
        'for email in accounts[i][1:]': lambda S, B, ret: (f'账户 `{S._inner["i"]}` 的邮箱看完了，回到上一层' if 'email' in B._inner and B._line != 9 and S._inner['email'] == B._inner['email']
                                                           else f'逐个看账户 `{S._inner["i"]}` 的邮箱：`{S._inner["email"]}`'),
        'if email in email_set': lambda S, B, ret: (f'`{S.email}` 已经收集过 → 它的相邻账户早处理了，跳过' if S.email in S.email_set
                                                    else f'`{S.email}` 还没收集过，继续'),
        'continue': '跳过这个邮箱，避免重复遍历',
        'email_set.add(email)': '收集邮箱 `{email}` → `{email_set}`',
        'for j in email_to_idx[email]': lambda S, B, ret: (f'`{S.email}` 出现在账户 `{S.email_to_idx[S.email]}`：这些账户是同一个人，逐个检查 `j = {S.j}`'
                                                           if 'j' not in B._inner or S._inner['j'] != B._inner['j'] else '含该邮箱的账户都检查完了'),
        'if not vis[j]': lambda S, B, ret: (f'账户 `{S.j}` 没访问过 → ==连通块要扩过去==' if not S.vis[S.j]
                                            else f'账户 `{S.j}` 已访问过，不用再走'),
        'dfs(j)': '从账户 `{j}` 继续 DFS：把同一连通块的邮箱都收进 `email_set`',
        'vis = [False]': '`vis` 全为 False：还没访问任何账户',
        'for i, b in enumerate(vis)': '枚举账户 `{i}`，`vis[{i}] = {b}`',
        'if not b': lambda S, B, ret: (f'账户 `{S.i}` 没访问过 → ==新的连通块==，从它开始 DFS' if not S.b
                                       else f'账户 `{S.i}` 已被前面的 DFS 合并掉，跳过'),
        'email_set = set()': '新建空集合，专门收集这个连通块的邮箱',
        'ans.append': 'DFS 结束：名字 `{accounts[i][0]}` + 排序后的邮箱 → `{ans[-1]}`',
        'return ans': '返回 `{ans}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='账户和邮箱连成二分图，一个连通块就是一个人',
        complexity='时间 `O(L log M)`，空间 `O(L)`',
        problem=['每个账户 = 名字 + 若干邮箱；有共同邮箱的账户属于同一个人，要合并',
                 '合并后邮箱按字典序排列，名字放最前面，账户顺序随意',
                 '本视频：账户 0、2 共有 `a@m` → 合并成 `John`；`Mary` 独立（邮箱已缩短）'],
        quote='把每个账户用其在 accounts 中的下标表示……同时，把每个账户的邮箱地址，也视作节点。我们在账户下标与其邮箱地址之间连边，得到一个无向图（二分图）。题目相当于求出这个图的每个连通块，这可以用 DFS 解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先建 `email_to_idx`：邮箱 → 含它的账户下标列表',
              '没访问的账户 `i` 开一个新块；DFS 时邮箱收进 `email_set`，再跳到共享该邮箱的账户 `j`',
              '一个块 DFS 完，`sorted(email_set)` 加上名字就是一个合并后的账户'],
        summary=['时间 `O(L log M)`，瓶颈在排序；空间 `O(L)`',
                 '邮箱已在 `email_set` 就 `continue`，保证每个邮箱只展开一次',
                 '`email_set` 每个连通块要重新 `set()`，不能放在循环外',
                 '同名不代表同一人，只能靠共同邮箱合并',
                 '并查集也能做（题单「七、并查集」同一道题）'],
    ),
)
