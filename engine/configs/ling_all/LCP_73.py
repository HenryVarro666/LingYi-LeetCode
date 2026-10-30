A = ["gate->lake", "gate->lake->cave->hill", "", "hill->pine->lake->pine->fox"]


def _rec(S):
    if 'i' not in S:
        return '探险记录：' + '　'.join(f'[{k}] `{x or "空"}`' for k, x in enumerate(S['a']))
    i = S['i']
    a = S['a'][i]
    if a == '':
        return f'第 `{i}` 次探险：空记录，没有任何营地'
    parts = a.split('->')
    t = S.get('t')
    show = ' → '.join(f'=={p}==' if (p == t and S.get('_line') in (8, 9, 10, 11)) else p for p in parts)
    return f'第 `{i}` 次探险：{show}'


def _cnt(S):
    if 'ans' not in S:
        return ''
    c = S.get('cnt', 0) if 'i' in S else 0
    return f'本次新发现 `cnt = {c}`　历史最多 `max_cnt = {S["max_cnt"]}`　答案 `ans = {S["ans"]}`'


CONFIG = dict(
    num='LCP 73', title='探险营地', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 边遍历边记录已知营地',
    code='''
class Solution:
    def adventureCamp(self, a: List[str]) -> int:
        vis = set(a[0].split('->'))  # 这样可能会把空串插入，但是没有关系
        max_cnt, ans = 0, -1
        for i in range(1, len(a)):
            if a[i] == "": continue
            cnt = 0
            for t in a[i].split('->'):
                if t not in vis:
                    vis.add(t)
                    cnt += 1
            if cnt > max_cnt:
                max_cnt, ans = cnt, i
        return ans
''',
    call=f'Solution().adventureCamp({A!r})',
    expect=1,
    views=[
        dict(type='text', size=27, h=90, fn=_rec),
        dict(type='set', var='vis', label='vis（已经到访 / 已知的营地）', fmt=lambda x: str(x), h=230, font=28),
        dict(type='text', size=28, h=70, fn=_cnt),
    ],
    watch=[('i', 'i', 'blue'), ('t', 't', 'pink'), ('cnt', 'cnt', 'orange'), ('max_cnt', 'max_cnt', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'vis = set': '`a[0]` 里的营地都是已知的，放进 `vis`（空串混进去也无所谓）',
        'max_cnt, ans = 0, -1': '`max_cnt` 记新发现最多的数量，`ans = -1` 表示还没有任何发现',
        'for i in range': lambda S, B, r: ('所有探险都看完了' if 'i' in B and B.i == S.i and S.i == len(S.a) - 1 else f'看第 `{S.i}` 次探险'),
        'if a[i] == ""': lambda S, B, r: ('空记录，没有营地 → ==跳过== `continue`' if S.a[S.i] == '' else f'记录非空，继续统计'),
        'cnt = 0': '这次探险新发现的营地数清零',
        'for t in a[i]': lambda S, B, r: (f'这次探险的营地都看完了，新发现 `{S.cnt}` 处' if 't' in B and B.t == S.t == S.a[S.i].split('->')[-1] else f'到访营地 `{S.t}`'),
        'if t not in vis': lambda S, B, r: (f'`{S.t}` ==不在== vis 里 → 是新发现' if S.t not in S.vis else f'`{S.t}` 已经在 vis 里 → 不算新发现'),
        'vis.add(t)': '登记 `{t}`，以后再遇到就不算新的了',
        'cnt += 1': '新发现 +1 → `cnt = {cnt}`',
        'if cnt > max_cnt': lambda S, B, r: (f'`cnt = {S.cnt}` > `max_cnt = {S.max_cnt}` → ==更多==，更新答案' if S.cnt > S.max_cnt else f'`cnt = {S.cnt}` ≤ `max_cnt = {S.max_cnt}`：==严格大于才更新==，并列保留编号小的'),
        'max_cnt, ans = cnt, i': '`max_cnt = {max_cnt}`，`ans = {ans}`',
        'return ans': '返回 =={ret}==（`-1` 表示没有任何新发现）',
    },
    cards=dict(
        one_liner='用集合记住已知营地，每次只数「第一次见到」的',
        complexity='时间 `O(L)`，空间 `O(L)`（L 为所有字符串长度之和）',
        problem=['`expeditions[i]` 是第 i 次探险，营地用 `->` 连接',
                 '`expeditions[0]` 是已知营地；之后每次探险新出现的营地算新发现',
                 '返回新发现最多、且索引最小的那次；没有新发现返回 `-1`',
                 '本视频：4 条记录 `[…, "", …]` → `1`'],
        quote='`vis = set(a[0].split(\'->\'))  # 这样可能会把空串插入，但是没有关系`',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`vis` 先装下初始营地，探险过程中不断把新营地加进去',
              '同一次探险里重复到访的营地：第一次算新发现，登记后第二次就不算',
              '`cnt > max_cnt` 用严格大于，==数量并列时保留靠前的探险=='],
        summary=['时间 `O(L)`，空间 `O(L)`',
                 '空记录要先 `continue`，否则 `"".split("->")` 会得到 `[\'\']`，把空串当营地',
                 '`a[0]` 为空时 `vis` 里有空串，无害，因为后面非空记录里不会出现空串',
                 '必须边遍历边更新 `vis`：后面的探险要和前面所有探险比较'],
    ),
)
