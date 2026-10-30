CONFIG = dict(
    num=3991, title='使用前缀反转对数组进行排序', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='康托展开 + BFS',
    tags=[],
    code='''
class Solution(object):
    def sortArray(self, nums, pre):
        
        n = len(nums)
        fac = [1]
        for v in range(1, n + 1):
            fac.append(fac[-1] * v)

        def cantor(nums):
            used = set()
            st = 0
            for index, v in enumerate(nums):
                cnt = v
                for x in range(v):
                    if x in used:
                        cnt -= 1
                st += cnt * fac[n - index - 1]
                used.add(v)
            return st

        def rev_cantor(st):
            f = []
            used = set()
            for index in range(n):
                v = st // fac[n - index - 1]
                st %= fac[n - index - 1]
                cnt = 0
                for x in range(n):
                    if x in used:
                        continue
                    if v == cnt:
                        f.append(x)
                        used.add(x)
                        break
                    else:
                        cnt += 1

            return f

        st = cantor(nums)
        if st == 0:
            return 0
        vis = set([st])
        print(st)
        q = [st]
        head, tail = 0, 1
        res = 0
        while head < tail:
            res += 1
            for st in q[head : tail]:
                now = rev_cantor(st)
                for p in pre:
                    left, right = 0, p - 1
                    while left < right:
                        now[left], now[right] = now[right], now[left]
                        left += 1
                        right -= 1
                    
                    nxt_st = cantor(now)
                    if nxt_st == 0:
                        return res
                    if nxt_st not in vis:
                        vis.add(nxt_st)
                        q.append(nxt_st)

                    left, right = 0, p - 1
                    while left < right:
                        now[left], now[right] = now[right], now[left]
                        left += 1
                        right -= 1
            
            head, tail = tail, len(q)
        
        return -1
''',
    call='Solution().sortArray([1, 2, 0], [2, 3])',
    expect=2,
    views=[
        dict(type='array', var='now', label='now（由序号还原出的排列，正在做前缀反转）', cell=70, h=150, pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right')),
        dict(type='array', var='q', label='q（BFS 队列，存的是排列的康托序号）', cell=70, h=190, pointers={'head': 'blue', 'tail': 'pink'}),
        dict(type='set', var='vis', label='vis（已出现的序号）', h=110),
        dict(type='text', h=70, fn=lambda S: f"已操作 `res` = =={S['res']}== 次；目标序号是 `0`（升序排列）" if 'res' in S else ''),
    ],
    watch=['res', 'st', 'nxt_st', ('head', 'head', 'blue'), ('tail', 'tail', 'pink'), 'p'],
    captions={
        'fac.append': '`fac` 存阶乘：`fac = {fac}`，康托展开要用',
        'cnt = v': '`v = {v}`：先假设比 `v` 小的数有 `v` 个都在后面',
        'cnt -= 1': '`{x}` 已经用过（在前面），排在它前面的数少一个 → `cnt = {cnt}`',
        'st += cnt': '这一位贡献 `{cnt} × {fac[n - index - 1]}`，`st` = {st}',
        'return st': '康托序号 = =={st}==（每位 = 比它小且还没用过的数的个数 × 阶乘，升序排列恰好是 0）',
        'v = st //': '第 `{index}` 位：序号 // `{fac[n - index - 1]}` = ==第 {v} 小的没用过的数==',
        'f.append(x)': '找到：未用过的数里第 `{v}` 小是 `{x}`，放进排列',
        'return f': '逆运算：序号还原成排列 `{f}`（第 k 位取剩余数里第 k 小）',
        'st = cantor(nums)': '把初始排列 `{nums}` 编码成序号 `{st}`',
        'if st == 0': lambda S, B, r: ('序号是 0，已经有序 → 0 步' if S.st == 0 else f'`st = {S.st} ≠ 0`，还没排好 → 开始 BFS'),
        'vis = set': '`vis` 记下已经出现过的排列序号，避免重复搜索',
        'q = [st]': '队列放入起点序号 `{st}`',
        'res += 1': '新一轮 BFS：这一轮的所有状态各做一次翻转 → 步数 `res = {res}`',
        'now = rev_cantor(st)': '把序号 `{st}` 还原成排列（康托展开的逆运算）',
        'for p in pre': '尝试翻转前缀长度 `p = {p}`',
        'nxt_st = cantor(now)': '翻转后排列 `{now}`，再编码成序号',
        'if nxt_st == 0': lambda S, B, r: (f'序号 `{S.nxt_st}` = 0：排好序了！当前轮次 `{S.res}` 就是答案' if S.nxt_st == 0
                                         else f'`{S.nxt_st}` ≠ 0，还没排好'),
        'if nxt_st not in vis': lambda S, B, r: (f'`{S.nxt_st}` 没见过 → 新状态，入队' if S.nxt_st not in B.vis else f'`{S.nxt_st}` 见过了，不重复入队'),
        'vis.add(nxt_st)': '标记 `{nxt_st}` 已访问',
        'q.append(nxt_st)': '`{nxt_st}` 入队，下一轮再展开：`q = {q}`',
        'left, right = 0, p - 1': '准备反转前 `{p}` 个元素：`left = 0`，`right = {p - 1}`',
        'now[left], now[right]': '交换 `now[{left}]` 和 `now[{right}]`',
        'head, tail = tail': '这一轮结束：队列窗口移到下一轮 `[{head}, {tail})`',
        'return res': '翻转 `{res}` 次后得到升序 → 返回 =={res}==',
    },
    skip=['cnt = v', 'st += cnt', 'cnt -= 1', 'v = st //', 'f.append(x)', 'used = set()', 'used.add', 'f = []', 'st = 0', 'cnt = 0', 'for index', 'for x in', 'if x in used', 'continue', 'if v == cnt', 'else:', 'left += 1', 'right -= 1',
          'while left < right', 'print(', 'for v in range', 'st %=', 'cnt += 1', 'break'],
    max_steps=75,
    cards=dict(
        one_liner='n ≤ 8 只有 40320 种排列：康托展开编号，再 BFS',
        complexity='时间 `O(n! · |pre| · n²)`，空间 `O(n!)`',
        problem=['`nums` 是 `0..n-1` 的排列（`n ≤ 8`），`pre` 里是允许的前缀长度',
                 '每次选一个 `x`，把 `nums` 前 `x` 个元素翻转；求变成升序的最少次数，不行返回 `-1`',
                 '本视频：`nums=[1,2,0]`，`pre=[2,3]` → `2`'],
        quote='由于n的长度不超过8，也就意味着总的排列数不会超过8! = 40320种，因此在这里可以先通过康拓展开将nums转化为其在所有排列中的序，然后基于这个顺序执行bfs。',
        quote_src='—— yiduobo 题解原文',
        idea=['把「排列」当图的点，一次前缀翻转 = 一条边，求最短路 = BFS',
              '康托展开：排列 ↔ 序号 `0..n!-1`，用整数做 `vis` 和队列',
              '每轮：序号还原排列 → 试每个 `p` 翻转 → 再编码 → 没见过就入队；出现序号 0 就返回'],
        summary=['最多 `n!` 个状态，每个状态试 `|pre|` 种翻转，编码/解码各 `O(n²)`',
                 '翻转后要再翻转一次还原 `now`，才能继续试下一个 `p`',
                 '用 `q[head:tail]` 分层，`res` 就是 BFS 的层数',
                 '原文为 Python 2 写法，`print st` 已改为 `print(st)`（该输出与算法无关）'],
    ),
)
