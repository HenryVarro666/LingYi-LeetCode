def _alive(S):
    """沿 right 链表从 0 走一遍，得到还没被删除的下标集合"""
    right, n = S.get('right'), len(S['nums'])
    if right is None:
        return set(range(n))
    out, k = set(), 0
    while k < n and k not in out:
        out.add(k)
        k = right[k]
    return out


def _tag(S):
    return 'nums' in S and 'right' in S


def _dec_text(S):
    if 'dec' not in S:
        return ''
    n = len(S['nums'])
    al = sorted(_alive(S))
    cur = [S['nums'][k] for k in al]
    return f"当前数组 `{cur}`，递减的相邻对 `dec` = =={S['dec']}=="


CONFIG = dict(
    num=3510, title='移除最小数对使数组有序 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='懒删除堆 + 数组模拟双向链表',
    tags=['难度分 2608'],
    code='''
class Solution:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        n = len(nums)
        h = []  # (相邻元素和，左边那个数的下标)
        dec = 0  # 递减的相邻对的个数
        for i, (x, y) in enumerate(pairwise(nums)):
            if x > y:
                dec += 1
            h.append((x + y, i))
        heapify(h)
        lazy = defaultdict(int)

        # 每个下标的左右最近的未删除下标
        left = list(range(-1, n))  # 加一个哨兵，防止下标越界
        right = list(range(1, n + 1))

        ans = 0
        while dec:
            ans += 1

            while lazy[h[0]]:
                lazy[heappop(h)] -= 1
            s, i = heappop(h)  # 删除相邻元素和最小的一对

            # (当前元素，下一个数)
            nxt = right[i]
            if nums[i] > nums[nxt]:  # 旧数据
                dec -= 1

            # (前一个数，当前元素)
            pre = left[i]
            if pre >= 0:
                if nums[pre] > nums[i]:  # 旧数据
                    dec -= 1
                if nums[pre] > s:  # 新数据
                    dec += 1
                lazy[(nums[pre] + nums[i], pre)] += 1  # 懒删除
                heappush(h, (nums[pre] + s, pre))

            # (下一个数，下下一个数)
            nxt2 = right[nxt]
            if nxt2 < n:
                if nums[nxt] > nums[nxt2]:  # 旧数据
                    dec -= 1
                if s > nums[nxt2]:  # 新数据（当前元素，下下一个数）
                    dec += 1
                lazy[(nums[nxt] + nums[nxt2], nxt)] += 1  # 懒删除
                heappush(h, (s + nums[nxt2], i))

            nums[i] = s
            # 删除 nxt
            l, r = left[nxt], right[nxt]
            right[l] = r  # 模拟双向链表的删除操作
            left[r] = l

        return ans
''',
    call='Solution().minimumPairRemoval([4,2,5,3,1])',
    expect=3,
    views=[
        dict(type='text', fn=_dec_text, h=55),
        dict(type='array', var='nums', pointers={'pre if 31 <= _line <= 53 and pre >= 0 else None': 'cyan', 'i if 23 <= _line <= 53 else None': 'blue',
                           'nxt if 26 <= _line <= 53 else None': 'pink', 'nxt2 if 41 <= _line <= 53 and nxt2 < n else None': 'purple'},
             pointer_labels={'pre if 31 <= _line <= 53 and pre >= 0 else None': 'pre', 'i if 23 <= _line <= 53 else None': 'i',
                             'nxt if 26 <= _line <= 53 else None': 'nxt', 'nxt2 if 41 <= _line <= 53 and nxt2 < n else None': 'nxt2'}, h=230,
             label='nums（灰 = 已被合并删除）',
             dim=lambda S, i, v: i not in _alive(S),
             color=lambda S, i, v: ('blue' if i == S.get('i') else 'pink' if i == S.get('nxt') else None) if S.get('i') is not None and 23 <= S.get('_line', 0) <= 53 and i in _alive(S) else None),
        dict(type='heap', var='h', label='h 最小堆（(相邻和, 左下标)）', fmt=lambda x: f'{x[0]},{x[1]}', top_color='orange', h=130),
        dict(type='map', var='lazy', label='lazy（待懒删除的 pair → 次数）', fmt=lambda k, v: f'{k}:{v}', h=90),
    ],
    watch=[('ans', 'ans', 'green'), ('dec', 'dec', 'orange'), 's', ('pre', 'pre', 'cyan'), ('i', 'i', 'blue'), ('nxt', 'nxt', 'pink'), ('nxt2', 'nxt2', 'purple')],
    skip=['dec -= 1', 'dec += 1', 'n = len(nums)', 'h = []', 'lazy = defaultdict(int)', 'left = list', 'right = list', 'l, r = left[nxt]', 'left[r] = l'],
    captions={
        'dec = 0': '`dec`：「左边大于右边」的相邻对个数，`dec = 0` 就有序了',
        'for i, (x, y) in enumerate': '遍历每个相邻对 `({x}, {y})`，左边下标 `{i}`',
        'if x > y': lambda S, B, r: ('`{} > {}` → 递减对，`dec` 加一'.format(S.x, S.y) if S.x > S.y else '`{} ≤ {}`，不算递减'.format(S.x, S.y)),
        'h.append': '相邻和 `{x} + {y} = {x + y}`，连同左下标 `{i}` 放进 `h`',
        'heapify(h)': '建最小堆：堆顶 = 和最小的一对（和相同则下标小的优先）',
        'ans = 0': '`left` / `right` 两个数组模拟双向链表：记录每个下标左右最近的未删除下标',
        'while dec': lambda S, B, r: ('`dec = {}` > 0，数组还没有序，继续操作'.format(S.dec) if S.dec else '`dec = 0`，数组已经非递减 → 结束'),
        'ans += 1': '又做一次操作：`ans = {ans}`',
        'while lazy[h[0]]': lambda S, B, r: ('堆顶 `{}` 在 `lazy` 里记过 → 它是失效的旧数据'.format(S.h[0]) if S.lazy[S.h[0]] else '堆顶 `{}` 没被标记 → 是有效的'.format(S.h[0])),
        'lazy[heappop(h)] -= 1': '弹出失效的堆顶，`lazy` 计数减一（==懒删除生效==）',
        's, i = heappop(h)': '弹出和最小的一对：`s = {s}`，左边下标 `i = {i}`',
        'nxt = right[i]': '右边那个数的下标 `nxt = {nxt}`（链表里 `i` 的下一个）',
        'if nums[i] > nums[nxt]': lambda S, B, r: ('合并前 `{} > {}` 是递减对，合并后它消失 → `dec` 减一'.format(S.nums[S.i], S.nums[S.nxt]) if S.nums[S.i] > S.nums[S.nxt] else '合并前 `{} ≤ {}`，不是递减对，`dec` 不变'.format(S.nums[S.i], S.nums[S.nxt])),
        'pre = left[i]': '左边邻居 `pre = {pre}`（-1 表示没有）',
        'if pre >= 0': lambda S, B, r: ('有左邻居，要重新考察 `(pre, i)` 这一对' if S.pre >= 0 else '没有左邻居，跳过'),
        'if nums[pre] > nums[i]': lambda S, B, r: ('旧的 `({}, {})` 递减 → `dec` 减一'.format(S.nums[S.pre], S.nums[S.i]) if S.nums[S.pre] > S.nums[S.i] else '旧的 `({}, {})` 不递减'.format(S.nums[S.pre], S.nums[S.i])),
        'if nums[pre] > s': lambda S, B, r: ('新的 `({}, {})` 递减 → `dec` 加一'.format(S.nums[S.pre], S.s) if S.nums[S.pre] > S.s else '新的 `({}, {})` 不递减'.format(S.nums[S.pre], S.s)),
        'lazy[(nums[pre] + nums[i], pre)] += 1': '堆里旧的 `(nums[pre]+nums[i], pre)` 作废：==不去堆里找，在 `lazy` 里记一笔==',
        'heappush(h, (nums[pre] + s, pre))': '新的相邻和 `{nums[pre] + s}` 压进堆',
        'nxt2 = right[nxt]': '`nxt` 右边的邻居 `nxt2 = {nxt2}`（== n 表示没有）',
        'if nxt2 < n': lambda S, B, r: ('有 `nxt2`，要重新考察 `(i, nxt2)` 这一对' if S.nxt2 < S.n else '没有 `nxt2`，跳过'),
        'if nums[nxt] > nums[nxt2]': lambda S, B, r: ('旧的 `({}, {})` 递减 → `dec` 减一'.format(S.nums[S.nxt], S.nums[S.nxt2]) if S.nums[S.nxt] > S.nums[S.nxt2] else '旧的 `({}, {})` 不递减'.format(S.nums[S.nxt], S.nums[S.nxt2])),
        'if s > nums[nxt2]': lambda S, B, r: ('新的 `({}, {})` 递减 → `dec` 加一'.format(S.s, S.nums[S.nxt2]) if S.s > S.nums[S.nxt2] else '新的 `({}, {})` 不递减'.format(S.s, S.nums[S.nxt2])),
        'lazy[(nums[nxt] + nums[nxt2], nxt)] += 1': '堆里旧的 `(nums[nxt]+nums[nxt2], nxt)` 作废，记入 `lazy`',
        'heappush(h, (s + nums[nxt2], i))': '新的相邻和 `{s + nums[nxt2]}`（左下标 `i`）压进堆',
        'nums[i] = s': '把 `nums[nxt]` 加到 `nums[i]` 上：`nums[{i}] = {s}`',
        'right[l] = r': '`nxt` 从链表中摘掉：`right[{l}] = {r}`',
        'return ans': '一共操作 `{ans}` 次',
    },
    max_steps=150,
    cards=dict(
        one_liner='模拟合并：堆找最小和，链表找邻居，dec 判断何时有序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次选相邻对里==和最小==的一对（并列取最左），用它们的和替换这对',
                 '求让数组变成非递减所需的最少操作次数',
                 '本视频：`[4,2,5,3,1]` → `3`'],
        quote='每次操作，我们需要重新考察 4 个元素值的大小关系，下标从左到右为 pre, i, nxt, nxt2。……用最小堆（懒删除堆）代替维护 pair 的有序集合。用双向链表代替维护下标的有序集合。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三样信息：堆里放 `(相邻和, 左下标)`，两个数组模拟链表，`dec` 数递减对',
              '操作 = `nums[i] += nums[nxt]` 再删除 `nxt`，只影响 `pre, i, nxt, nxt2` 之间的几对',
              '旧的相邻和不去堆里删，在 `lazy` 里记账，弹堆顶时再清掉'],
        summary=['时间 `O(n log n)`，空间 `O(n)`；每次操作堆只增删常数个元素',
                 '`dec` 的更新要同时考虑「旧数据减一」和「新数据加一」，最容易漏一边',
                 '`left` 多留一个哨兵，`right[n] = n` 之外越界用 `nxt2 < n` 判断',
                 '写法一用两个有序集合 SortedList；另有不用 lazy 的版本：直接核对 `right[i]` 与相邻和是否匹配',
                 '`pairwise` 需要 Python 3.10+，视频环境满足'],
    ),
)
