def _nn(L):
    return ['-' if x is None else x for x in L]


CONFIG = dict(
    num=3814, title='预算下的最大总容量', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 前缀最大值/次大值 + 双指针',
    tags=['滑动窗口与双指针', '单调栈', '难度分 1796'],
    code='''
class Solution(object):
    def maxCapacity(self, costs, capacity, budget):
        
        info = sorted(zip(costs, capacity))
        first = [info[0][1]]
        second = [None]

        for _, ca in info[1:]:
            if ca > first[-1]:
                second.append(first[-1])
                first.append(ca)
            elif second[-1] is None or ca > second[-1]:
                first.append(first[-1])
                second.append(ca)
            else:
                first.append(first[-1])
                second.append(second[-1])
        
        p = len(info) - 1
        res = 0
        for index, (co, ca) in enumerate(info):
            if co >= budget:
                break
            res = max(res, ca)
            while p > index and info[p][0] + co >= budget:
                p -= 1

            if p > index:
                if first[p] != ca:
                    res = max(res, first[p] + ca)
                else:
                    res = max(res, second[p] + ca)
        
        return res
''',
    call='Solution().maxCapacity([2,3,2,5,4,3], [6,2,4,3,5,6], 6)',
    expect=12,
    views=[
        dict(type='array', var=lambda S: [x[0] for x in S['info']] if 'info' in S else [], label='成本（排序后）',
             pointers={'index': 'blue', 'p': 'pink'}, h=170,
             color=lambda S, i, v: ('blue' if i == S.get('index') else 'pink' if i == S.get('p') else None)),
        dict(type='array', var=lambda S: [x[1] for x in S['info']] if 'info' in S else [], label='容量', h=150,
             color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='array', var=lambda S: S['first'], label='first[i]：前缀最大容量', h=150,
             color=lambda S, i, v: 'pink' if i == S.get('p') and 'index' in S else None),
        dict(type='array', var=lambda S: _nn(S['second']), label='second[i]：前缀次大容量（- 表示没有）', h=150,
             color=lambda S, i, v: 'pink' if i == S.get('p') and 'index' in S else None),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'info = sorted': '先按成本从小到大排序：`{info}`',
        'first = [info[0][1]]': '`first[i]`：前 `i+1` 台里最大的容量；先放第 0 台',
        'second = [None]': '`second[i]`：次大容量。只有 1 台时还没有次大 → `None`',
        'if ca > first[-1]': lambda S, B, ret: (f'`ca = {S.ca}` > 当前最大 `{S.first[-1]}`' if S.ca > S.first[-1] else f'`ca = {S.ca}` 没超过当前最大 `{S.first[-1]}`'),
        'second.append(first[-1])': '新的最大诞生：原来的最大退居次大 → `second` 末尾 = {second[-1]}',
        'first.append(ca)': '`first` 末尾 = {first[-1]}',
        'elif second[-1] is None': lambda S, B, ret: ('次大还空着，或者 `ca` 比次大还大 → 它成为新的次大' if (S.second[-1] is None or S.ca > S.second[-1]) else f'`ca = {S.ca}` 连次大 `{S.second[-1]}` 都不超过 → 前缀信息不变'),
        'second.append(ca)': '最大不变，次大更新为 `{ca}`',
        'second.append(second[-1])': '两个都不变，照抄',
        'p = len(info) - 1': '`p` 指向最贵的机器，配对时只会往左缩：`p = {p}`',
        'if co >= budget': lambda S, B, ret: (f'`co = {S.co}` >= `{S.budget}`：一台都买不起，后面更贵 → 结束' if S.co >= S.budget else f'`co = {S.co}` < `{S.budget}`：这台能买'),
        'res = max(res, ca)': '先考虑只买这一台：`res = max({B.res}, {ca}) = {res}`',
        'while p > index': lambda S, B, ret: (f'`p` 处成本 `{S.info[S.p][0]}` + `{S.co}` >= `{S.budget}`：太贵 → `p` 左移到 {S.p - 1}' if (S.p > S.index and S.info[S.p][0] + S.co >= S.budget) else (f'`p = {S.p}`：成本 `{S.info[S.p][0]}` + `{S.co}` < `{S.budget}`，配对上限确定' if S.p > S.index else f'`p = {S.p}` 已经碰到 `index`：右边没有可配对的机器')),
        'p -= 1': '`p` → {p}。index 变大后 p 只会往左，不会回头',
        'if p > index': lambda S, B, ret: (f'`p = {S.p} > index = {S.index}`：[0..p] 里还有别的机器可配' if S.p > S.index else f'`p = {S.p}` <= `index`：没有可配对的机器'),
        'if first[p] != ca': lambda S, B, ret: (f'前缀最大 `{S.first[S.p]}` != 自己的 `{S.ca}` → 可以直接配最大' if S.first[S.p] != S.ca else f'前缀最大 `{S.first[S.p]}` 就是自己 → ==不能选自己两次==，改用次大'),
        'res = max(res, first[p] + ca)': '`res = max({B.res}, {first[p]} + {ca}) = =={res}==`',
        'res = max(res, second[p] + ca)': '`res = max({B.res}, {second[p]} + {ca}) = =={res}==`',
        'return res': '最大总容量 `{res}`',
    },
    cards=dict(
        one_liner='排序后配对上限 p 只减不增，前缀最大 + 次大避免选到自己',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['最多选两台机器，总成本 ==严格小于== `budget`，求最大总容量',
                 '可以只选一台，也可以选两台',
                 '本视频：`costs=[2,3,2,5,4,3]`，`capacity=[6,2,4,3,5,6]`，`budget=6` → `12`'],
        quote='对于两数之和不大于指定数的问题，一种经典做法是先将这些数从小到大进行排序，……随着index的增大，其对应的p是单调不增的。',
        quote_src='—— yiduobo 题解原文',
        idea=['按成本排序后，每台机器 `index` 能配的最贵搭档下标 `p` 随 `index` 增大而左移',
              '`[0..p]` 里容量最大的是最好搭档，但可能就是自己 → 另存==次大==',
              '先一趟扫出 `first/second` 前缀，再用双指针配对'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：前缀最大等于自己的容量时，要换成次大；`while p > index` 保证不选同一台',
                 '单选一台的情况要单独用 `ca` 更新答案；`co >= budget` 直接 break',
                 '对比灵神：灵神用 `pre_max` 一个数组并在 l 增长时累积，yiduobo 先预处理最大/次大再单向移动 p'],
    ),
)
