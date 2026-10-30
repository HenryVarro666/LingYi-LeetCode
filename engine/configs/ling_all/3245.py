def _ends(S):
    sl = S.get('sl')
    return None if sl is None else list(sl)


def _fen(S):
    t = S.get('t')
    if t is None:
        return None
    return ['—'] + [f'{c},{s}' for c, s in t.t[1:]]


CONFIG = dict(
    num=3245, title='交替组 III', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='有序集合 + 树状数组',
    tags=['难度分 2740'],
    setup='''
class SortedList(list):  # 演示用的最小实现，行为同 sortedcontainers.SortedList（本题只用到 add / remove / bisect_left / 下标 / len）
    def add(self, x):
        bisect.insort(self, x)

    def bisect_left(self, x):
        return bisect.bisect_left(self, x)
''',
    code='''
class FenwickTree:
    def __init__(self, n: int):
        self.t = [[0, 0] for _ in range(n + 1)]

    # op=1，添加一个 size
    # op=-1，移除一个 size
    def update(self, size: int, op: int) -> None:
        i = len(self.t) - size
        while i < len(self.t):
            self.t[i][0] += op
            self.t[i][1] += op * size
            i += i & -i

    # 返回 >= size 的元素个数，元素和
    def query(self, size: int) -> (int, int):
        cnt = s = 0
        i = len(self.t) - size
        while i > 0:
            cnt += self.t[i][0]
            s += self.t[i][1]
            i &= i - 1
        return cnt, s

class Solution:
    def numberOfAlternatingGroups(self, a: List[int], queries: List[List[int]]) -> List[int]:
        n = len(a)
        sl = SortedList()
        t = FenwickTree(n)

        # op=1，添加一个结束位置 i
        # op=-1，移除一个结束位置 i
        def update(i: int, op: int) -> None:
            idx = sl.bisect_left(i)
            pre = sl[idx - 1]
            nxt = sl[idx % len(sl)]

            t.update((nxt - pre - 1) % n + 1, -op)  # 移除/添加旧长度
            t.update((i - pre) % n, op)
            t.update((nxt - i) % n, op)  # 添加/移除新长度

        # 添加一个结束位置 i
        def add(i: int) -> None:
            if not sl:
                t.update(n, 1)
            else:
                update(i, 1)
            sl.add(i)

        # 移除一个结束位置 i
        def remove(i: int) -> None:
            sl.remove(i)
            if not sl:
                t.update(n, -1)
            else:
                update(i, -1)

        for i, c in enumerate(a):
            if c == a[(i + 1) % n]:
                add(i)  # i 是一个结束位置

        ans = []
        for q in queries:
            if q[0] == 1:
                if not sl:
                    ans.append(n)  # 每个长为 size 的子数组都符合要求
                else:
                    cnt, s = t.query(q[1])
                    ans.append(s - cnt * (q[1] - 1))
            else:
                i, c = q[1], q[2]
                if a[i] == c:  # 无影响
                    continue
                pre, nxt = (i - 1) % n, (i + 1) % n
                # 修改前，先去掉结束位置
                if a[pre] == a[i]:
                    remove(pre)
                if a[i] == a[nxt]:
                    remove(i)
                a[i] = c
                # 修改后，添加新的结束位置
                if a[pre] == a[i]:
                    add(pre)
                if a[i] == a[nxt]:
                    add(i)
        return ans
''',
    call='Solution().numberOfAlternatingGroups([0,0,1,0,1,1], [[1,3],[2,2,0],[1,3]])',
    expect=[2, 0],
    views=[
        dict(type='array', var='a', label='a（环，下标 n-1 与 0 相邻）', pointers={'i': 'pink'}, h=170,
             color=lambda S, i, v: 'blue' if v == 1 else None),
        dict(type='array', var=_ends, label='sl：结束位置（a[i] == a[i+1] 的 i），有序', h=130, cell=70),
        dict(type='array', var=_fen, label='树状数组 t：每格 = 个数,元素和（按长度从大到小编号）', h=130, cell=88),
    ],
    watch=['size', 'op', 'pre', 'nxt', ('cnt', 'cnt', 'cyan'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    skip=['n = len(a)', 'sl = SortedList()', 'for i, c in enumerate(a)', 'i = len(self.t) - size', 'while i < len(self.t)',
          'self.t[i][0] += op', 'self.t[i][1] += op * size', 'i += i & -i', 'cnt = s = 0', 'while i > 0', 'i &= i - 1', 'idx = sl.bisect_left(i)',
          'pre = sl[idx - 1]', 'ans = []', 'for q in queries', 'i, c = q[1], q[2]', 'q[0] == 1', 'cnt += self.t[i][0]', 'pre, nxt = (i - 1) % n'],
    max_steps=100,
    captions={
        'self.t = [[0, 0]': '树状数组每格存 `[个数, 元素和]`：统计「长度 >= size」的交替段。下标反着排：长度越大越靠前',
        'if c == a[(i + 1) % n]': lambda S, B, ret: ('`a[{}] = {}`，`a[{}] = {}`：相等 → ==i = {} 是结束位置==（交替段到这里断开）'.format(S.i, S.c, (S.i + 1) % S.n, S.a[(S.i + 1) % S.n], S.i)
                                                      if S.c == S.a[(S.i + 1) % S.n] else '`a[{}] ≠ a[{}]`：颜色交替，不是结束位置'.format(S.i, (S.i + 1) % S.n)),
        43: lambda S, B, ret: ('还没有结束位置：环只有这一个断点，==整个环是一个长为 n 的交替段==' if not S.sl else '已有结束位置：用有序集合找 `i` 前后相邻的结束位置'),
        64: lambda S, B, ret: ('没有任何结束位置：环上每个相邻瓷砖都交替' if not S.sl else '有结束位置：用树状数组统计长度 >= size 的段'),
        'sl.add(i)': '把 `{i}` 加入有序集合 `sl`：`{list(sl)}`',
        'sl.remove(i)': '把结束位置 `{i}` 从 `sl` 里移除：`{list(sl)}`',
        'nxt = sl[idx % len(sl)]': '`i = {i}` 前后相邻的结束位置：`pre = {pre}`，`nxt = {nxt}`（环形：取模、绕回）',
        't.update((nxt - pre - 1) % n + 1, -op)': '{"旧段 `pre→nxt`（长 " + str((nxt - pre - 1) % n + 1) + "）被 i 拆开 → 树状数组里移除它" if op == -1 else "两段合并成 `pre→nxt`（长 " + str((nxt - pre - 1) % n + 1) + "）→ 树状数组里加上它"}',
        't.update((i - pre) % n, op)': '{"新增" if op == 1 else "去掉"}长度 `{(i - pre) % n}` 的段（`pre→i`）',
        't.update((nxt - i) % n, op)': '{"新增" if op == 1 else "去掉"}长度 `{(nxt - i) % n}` 的段（`i→nxt`）',
        't.update(n, 1)': '树状数组里加入一个长为 `n = {n}` 的段',
        't.update(n, -1)': '最后一个结束位置没了：去掉长 n 的段',
        'cnt, s = t.query': '查询 `size = {q[1]}`：要统计所有长度 >= size 的交替段的「个数」和「长度之和」',
        's += self.t[i][1]': '累加得到 `个数 = {cnt}`，`长度之和 = {s}`',
        'return cnt, s': '长度 >= size 的段：`{cnt}` 个，总长 `{s}`',
        'ans.append(n)': '没有结束位置 → 环上任意 size 个相邻瓷砖都交替 → 答案 `n`',
        'ans.append(s - cnt * (q[1] - 1))': '每段贡献 `长度 − (size−1)` 个 → `{s} − {cnt}×({q[1]}−1)` = =={s - cnt * (q[1] - 1)}==',
        'if a[i] == c': lambda S, B, ret: ('修改 `a[{}]` → {}：颜色没变，直接跳过'.format(S.i, S.c) if S.a[S.i] == S.c else '修改 `a[{}]`：`{}` → `{}`，会影响结束位置 `{}` 和 `{}`'.format(S.i, S.a[S.i], S.c, (S.i - 1) % S.n, S.i)),
        75: lambda S, B, ret: '修改前：`a[pre] == a[i]`（`{}` vs `{}`）{}'.format(S.a[S.pre], S.a[S.i], '成立 → 旧结束位置 `pre` 要去掉' if S.a[S.pre] == S.a[S.i] else '不成立，`pre` 本来就不是结束位置'),
        77: lambda S, B, ret: '修改前：`a[i] == a[nxt]`（`{}` vs `{}`）{}'.format(S.a[S.i], S.a[S.nxt], '成立 → 旧结束位置 `i` 要去掉' if S.a[S.i] == S.a[S.nxt] else '不成立，`i` 本来就不是结束位置'),
        81: lambda S, B, ret: '修改后：`a[pre] == a[i]`（`{}` vs `{}`）{}'.format(S.a[S.pre], S.a[S.i], '成立 → `pre` 成为新的结束位置' if S.a[S.pre] == S.a[S.i] else '不成立'),
        83: lambda S, B, ret: '修改后：`a[i] == a[nxt]`（`{}` vs `{}`）{}'.format(S.a[S.i], S.a[S.nxt], '成立 → `i` 成为新的结束位置' if S.a[S.i] == S.a[S.nxt] else '不成立'),
        'remove(pre)': '修改前，先把旧的结束位置 `{pre}` 去掉',
        'remove(i)': '修改前，先把旧的结束位置 `{i}` 去掉',
        'a[i] = c': '真正修改：`a[{i}] = {c}`',
        'add(pre)': '添加新的结束位置 `{pre}`：先拆段更新树状数组，再放进 `sl`',
        'add(i)': '添加新的结束位置 `{i}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='交替段的个数和总长，用树状数组维护；结束位置用有序集合找邻居',
        complexity='时间 `O((n+q) log n)`，空间 `O(n)`',
        problem=['环形数组 `colors`（0/1）。查询 `[1, size]`：长度为 `size` 的交替组有几个',
                 '查询 `[2, i, c]`：把 `colors[i]` 改成 `c`',
                 '本视频：`[0,0,1,0,1,1]`，查询 `[1,3]` `[2,2,0]` `[1,3]` → `[2, 0]`'],
        quote='这启发我们维护长度 ≥ size 的交替段的个数以及元素和。考虑到后续要执行修改操作，用树状数组维护。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长为 `k` 的交替段里恰有 `k − (size−1)` 个长为 `size` 的交替子数组',
              '所以只要知道长度 `>= size` 的段的==个数 cnt== 和==总长 s==：答案 `s − cnt×(size−1)`',
              '改一个格子只影响结束位置 `i-1` 和 `i`：先移除旧的，改完再添加新的；有序集合找前后邻居，段的拆分/合并只改 3 个长度'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`',
                 '环形：长度要 `(nxt - pre - 1) % n + 1` 修正成 `[1, n]`；`pre`/`nxt` 不存在时绕回',
                 '没有结束位置时，任何 size 的答案都是 `n`',
                 '颜色不变的修改直接 `continue`',
                 '原文用 sortedcontainers.SortedList，视频里用等价的小 SortedList 代替；已删去 import 行'],
    ),
)
