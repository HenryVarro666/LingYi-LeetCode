N, M = 6, 2
GROUP = [-1, 0, 1, 0, 1, -1]
BEFORE = [[], [3], [1], [], [2], [4]]


def _txt(S):
    if 'item_q' not in S:
        return ''
    gq = S.get('group_q', [])
    parts = '　'.join(f'组{g}:{S["item_q"][g]}' for g in range(len(S['item_q'])))
    return f'每组的任务队列 `item_q`　{parts}'


def _txt2(S):
    if 'res' not in S:
        return ''
    return f"组队列 `group_q` = =={S.get('group_q', [])}==　答案 `res` = =={S['res']}=="


CONFIG = dict(
    num=1203, title='项目管理', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='任务拓扑 + 组拓扑',
    tags=['图论算法', '拓扑排序'],
    code='''
class Solution(object):
    def sortItems(self, n, m, group, beforeItems):

        item_cnt = [0] * m
        for index in range(n):
            if group[index] == -1:
                group[index] = m
                item_cnt.append(1)
                m += 1
            else:
                item_cnt[group[index]] += 1
        
        g = {x:set() for x in range(n)}
        ind_item = [0] * n
        ind_group = [0] * m
        

        for index in range(n):
            for before in beforeItems[index]:
                ind_item[index] += 1
                g[before].add(index)

                if group[before] != group[index]:
                    ind_group[group[index]] += 1

        group_q = []
        item_q = [[] for _ in range(m)]
        

        for index in range(n):
            if ind_item[index] == 0:
                item_q[group[index]].append(index)

        for index in range(m):
            if ind_group[index] == 0:
                group_q.append(index)
        
        res = []
        group_l = 0
        group_r = len(group_q)
        while group_l < group_r:
            now_group = group_q[group_l]
            group_l += 1
            item_l = 0
            while item_l < len(item_q[now_group]):
                now_item = item_q[now_group][item_l]
                item_l += 1
                res.append(now_item)
                for next_item in g[now_item]:
                    ind_item[next_item] -= 1
                    if ind_item[next_item] == 0:
                        item_q[group[next_item]].append(next_item)
                    
                    if group[next_item] != now_group:
                        ind_group[group[next_item]] -= 1
                        if ind_group[group[next_item]] == 0:
                            group_q.append(group[next_item])
                            group_r += 1

            if len(item_q[now_group]) != item_cnt[now_group]:
                return []
        
        if group_r != m:
            return []

        return res
''',
    call=f'Solution().sortItems({N}, {M}, {GROUP}, {BEFORE})',
    expect=[3, 1, 0, 2, 4, 5],
    views=[
        dict(type='array', var='group', label='group[i]（任务 i 所在组，-1 已改成新组）', h=150,
             pointers={'index': 'blue', 'now_item': 'pink'},
             color=lambda S, i, v: 'pink' if S.get('now_item') == i else None),
        dict(type='array', var='ind_item', label='ind_item[i]（任务入度）', h=150,
             pointers={'next_item': 'yellow'},
             color=lambda S, i, v: 'green' if v == 0 and S.get('_line', 0) > 40 else None),
        dict(type='array', var='ind_group', label='ind_group[g]（组入度）', h=150,
             color=lambda S, i, v: 'green' if v == 0 and S.get('_line', 0) > 40 else None),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='text', fn=_txt2, size=26, h=70),
    ],
    watch=['now_group', 'now_item', ('res', 'res', 'green'), 'group_l', 'group_r'],
    captions={
        'group[index] = m': '任务 `{index}` 没有组 → 给它==新建一个组== `{m}`，这样每个任务都有组',
        'item_cnt[group[index]] += 1': '组 `{group[index]}` 的任务数 +1，之后用来检查组内是否全部完成',
        'ind_item[index] += 1': '任务 `{before}` 必须在 `{index}` 之前：`{index}` 入度 +1，边 `{before}→{index}`',
        'ind_group[group[index]] += 1': '`{before}` 和 `{index}` ==不在同一组== → 组 `{group[before]}` 要排在组 `{group[index]}` 前，组入度 +1',
        'item_q[group[index]].append(index)': '任务 `{index}` 入度为 0，放进它所在组 `{group[index]}` 的队列',
        'group_q.append(index)': '组 `{index}` 入度为 0，可以先做，加入组队列',
        'now_group = group_q[group_l]': '取出一个入度为 0 的组 `{now_group}`：它的任务==连续做完==',
        'now_item = item_q': '组内取出任务 `{now_item}`',
        'res.append(now_item)': '任务 `{now_item}` 放进答案 `res = {res}`',
        'ind_item[next_item] -= 1': '后继任务 `{next_item}` 入度 -1 → `{ind_item[next_item]}`',
        'item_q[group[next_item]].append': '任务 `{next_item}` 前置都完成了 → 进入它所在组 `{group[next_item]}` 的队列',
        'ind_group[group[next_item]] -= 1': '后继在别的组：组 `{group[next_item]}` 入度 -1 → `{ind_group[group[next_item]]}`',
        'group_q.append(group[next_item])': '组 `{group[next_item]}` 入度为 0，加入组队列，之后整组连续做',
        'len(item_q[now_group]) != item_cnt': lambda S, B, r: (f'组内做完 `{len(S.item_q[S.now_group])}` 个，组共 `{S.item_cnt[S.now_group]}` 个'
                                                              + (' → 有任务做不了（环），返回空' if len(S.item_q[S.now_group]) != S.item_cnt[S.now_group] else ' → 一致，这组完成')),
        'group_r != m': lambda S, B, r: f'处理了 `{S.group_r}` 个组，总共 `{S.m}` 个组 → ' + ('有组被环卡住，返回空' if S.group_r != S.m else '全部处理完'),
        'return res': '全部合法：返回 `{res}`',
    },
    skip=['group_l = 0', 'item_l = 0', 'item_l += 1', 'group_l += 1', 'group_r += 1', 'group_r = len', 'item_cnt.append',
          'm += 1', 'item_cnt = [0]', 'g = {x', 'ind_item = [0]', 'ind_group = [0]', 'g[before].add', 'res = []',
          'group_q = []', 'item_q = [[]',
          'for index in range', 'for before in', 'if group[before] != group[index]', 'if ind_item[index] == 0',
          'if ind_group[index] == 0', 'for next_item', 'while item_l', 'if group[next_item] != now_group',
          'if ind_item[next_item] == 0', 'if group[index] == -1', 'if ind_group[group[next_item]] == 0'],
    max_steps=110,
    cards=dict(
        one_liner='任务拓扑排序 + 组拓扑排序，组内任务连续做完',
        complexity='时间 `O(n + 边数)`，空间 `O(n + 边数)`',
        problem=['`n` 个任务分属 `m` 个组（`-1` 表示无组），`beforeItems[i]` 是 `i` 的前置任务',
                 '要求：前置任务先做，==同组任务必须相邻==',
                 '返回满足要求的任务顺序，不存在返回 `[]`',
                 '本视频：`n=6, m=2`，`group=[-1,0,1,0,1,-1]`'],
        quote='若某一组的拓扑排序完成后其执行的任务数小于该组的总任务数，那么说明该组中有任务无法完成，应当返回空。',
        quote_src='—— yiduobo 题解原文',
        idea=['先给无组任务各分一个新组，题目就统一了',
              '任务 a 在 b 之前、且组不同 → 组与组之间也连边，组入度 +1',
              '先对组做拓扑；轮到某组时，在它自己的队列里把任务全做完'],
        summary=['时间空间都是 `O(n + 边数)`',
                 '易错：任务拓扑和组拓扑==两个环都要判断==：组内任务数不够、组数不够都返回空',
                 '同组的前置边不增加组入度，只有跨组边才算',
                 '原文是 Python 2 风格，只删去了类型说明，逻辑未改'],
    ),
)
