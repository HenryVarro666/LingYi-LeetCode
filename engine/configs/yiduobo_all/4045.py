CONFIG = dict(
    num=4045, title='统计机器人组数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='先合并 + 倒序遍历',
    tags=['栈', '邻项消除', '难度分 1888'],
    code='''
class Solution(object):
    def countGroups(self, position, speed, distance):
        
        r = [(position[0], speed[0])]
        for p, s in zip(position[1:], speed[1:]):
            if p - r[-1][0] <= distance:
                r[-1] = (p, s)
            else:
                r.append((p, s))
        
        res = 1
        s = r[-1][1]
        for index in range(len(r) - 2, -1, -1):
            if r[index][1] <= s:
                res += 1
                s = r[index][1]
        
        return res
''',
    call='Solution().countGroups([1,2,3,10,12,20,21], [5,1,4,3,2,9,6], 2)',
    expect=2,
    views=[
        dict(type='array', var='r', fmt=lambda v: f'{v[0]}:{v[1]}', label='r（位置:速度）', pointers={'index': 'blue'}, cell=150, h=200),
        dict(type='text', fn=lambda S: (f"当前基准速度 `s = {S['s']}`，已确定的组数 `res = {S['res']}`" if 'res' in S else '先把 t=0 就相邻合并的机器人并成一组（保留最右侧）'), size=30),
    ],
    watch=[('p', 'p', 'cyan'), ('s', 's', 'pink'), ('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'r = [(': '`r` 存合并后每组「最右侧」的 `(位置, 速度)`，先放第一个机器人',
        'if p - r[-1][0] <= distance': lambda S, B, ret: (f'`{S.p} - {S.r[-1][0]} = {S.p - S.r[-1][0]}` ≤ `{S.distance}`：距离够近，t=0 合并' if S.p - S.r[-1][0] <= S.distance
                                                         else f'`{S.p} - {S.r[-1][0]} = {S.p - S.r[-1][0]}` > `{S.distance}`：不合并，新开一组'),
        'r[-1] = (p, s)': '合并后保留右侧的位置和速度：`r[-1] = ({p}, {s})`',
        'r.append': '新的一组：`r` 长度 → {len(r)}',
        'res = 1': '最右侧的组速度永远不变，先算 1 组',
        's = r[-1][1]': '以最右组速度 `s = {s}` 为基准，向左看',
        'for index in range': lambda S, B, ret: ('倒序遍历结束，没有更靠左的组了' if B.get('index') == S.index else f'倒序遍历 `r`：当前看第 `{S.index}` 组'),
        'if r[index][1] <= s': lambda S, B, ret: (f'`{S.r[S.index][1]} <= {S.s}`：不比右边快，追不上 → 独立成组' if S.r[S.index][1] <= S.s
                                                   else f'`{S.r[S.index][1]} > {S.s}`：比右边快，会追上并合并，等于被移除'),
        'res += 1': '这一组不会被合并：`res` → {res}',
        's = r[index][1]': '以它的速度 `s = {s}` 作为新基准继续向左',
        'return res': '一共 `{res}` 组',
    },
    cards=dict(
        one_liner='右边速度定了才能判断左边：从后往前数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['机器人向右匀速跑，距离 `<= distance` 就合并，合并后继承最右侧的位置和速度',
                 '求最终剩下几组',
                 '示例：`position=[1,5,6,20]`，`speed=[4,3,2,3]`，`distance=1` → `2`'],
        quote='只有当确定了右侧机器人的速度已经固定下来后，才能判断是否会发生合并。基于这一点，从后往前遍历就是很自然的想法了。',
        quote_src='—— yiduobo 题解原文',
        idea=['右边的机器人可能被更右的合并而变慢，所以先固定右侧，再看左侧',
              '追上右侧 = 被移除；追不上 = 独立成组，并以它的速度为新基准',
              '开头要先遍历一次，执行 t=0 时的合并'],
        summary=['时间 `O(n)`，空间 `O(n)`（存合并后的 `r`）',
                 '易错：倒序前必须先做 t=0 的合并',
                 '速度相等也追不上，所以条件是 `<=`',
                 '对比灵神：灵神一次正序遍历 + 栈，这里是先合并再倒序'],
    ),
)
