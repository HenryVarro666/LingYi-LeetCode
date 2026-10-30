CONFIG = dict(
    num=1436, title='旅行终点站', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 一次遍历',
    tags=[],
    code='''
class Solution:
    def destCity(self, paths: List[List[str]]) -> str:
        set_a = set()
        set_b = set()
        for a, b in paths:
            set_b.discard(a)  # a 一定不是答案
            if b not in set_a:  # b 有可能是答案
                set_b.add(b)
            set_a.add(a)
        return set_b.pop()
''',
    call='Solution().destCity([["B","C"],["D","B"],["C","A"]])',
    expect='A',
    views=[
        dict(type='text', h=100, size=30,
             fn=lambda S: f"当前线路 ==`{S['a']} → {S['b']}`==" if 'a' in S and 'b' in S else '每条线路 `a → b`；终点没有出边，不会出现在任何 a 里'),
        dict(type='set', var='set_a', label='set_a：有出边的城市', fmt=lambda x: str(x), h=170, font=34),
        dict(type='set', var='set_b', label='set_b：可能是终点的城市', fmt=lambda x: str(x), h=170, font=34),
    ],
    watch=['a', 'b', ('set_a', 'sorted(set_a)', 'blue'), ('set_b', 'sorted(set_b)', 'green')],
    captions={
        'set_b.discard': '`{a}` 有出边 `{a} → {b}`，不可能是终点：从 `set_b` 里删掉（没有也无妨）',
        'if b not in set_a': lambda S, B, r: (f'`{S.b}` 没出现在 set_a（还没发现它有出边）→ 成立，可能是终点' if S.b not in S.set_a
                                              else f'`{S.b}` 已在 set_a：之前见过它有出边 → 不成立，不是终点'),
        'set_b.add(b)': '`{b}` 加入 `set_b` 作为候选终点',
        'set_a.add(a)': '记下 `{a}` 有出边：`set_a` = {sorted(set_a)}',
        'return set_b.pop()': '题目保证只剩一个候选，它就是终点站 `{ret}`',
    },
    cards=dict(
        one_liner='终点站只进不出：它不会出现在任何线路的起点里',
        complexity='时间 `O(nm)`，空间 `O(nm)`，m ≤ 10 为字符串长度',
        problem=['`paths[i] = [A, B]` 表示从 A 直接前往 B，线路无环且连成一条链',
                 '求没有任何出边的终点站',
                 '示例：`[["B","C"],["D","B"],["C","A"]]` → `"A"`'],
        quote='再次遍历 paths，如果发现 cityB 不在 setA 中，则立刻返回 cityB。……在方法一的基础上，额外维护一个哈希集合 setB，用来存储那些「可能是答案」的 cityB。',
        quote_src='—— 灵茶山艾府题解',
        idea=['题目相当于一条链上的有向边，终点就是==没有出边的点==',
              '`set_a` 记有出边的城市，`set_b` 记候选终点',
              '遇到 `a → b`：`a` 肯定不是答案，从 `set_b` 删；`b` 还没出现在 `set_a` 才加入候选'],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '`discard` 不用先检查是否存在',
                 '先 discard(a) 再 add(b)，顺序保证了先被当终点后来又有出边的城市会被移除',
                 '方法一（两次遍历）：先收集所有起点，再找第一个不在其中的 `cityB`'],
    ),
)
