N = 5
PAIRS = [[1, 2], [2, 5], [3, 5]]   # 示例 2 → 12


def _show(S):
    if 'now' not in S:
        return 'first[y]：以 y 为右端点时最大的"不能取的左边界" +1；second[y] 是删掉一个冲突对后的备选'
    ln = S.get('_line', 0)
    s = f"不删冲突对时合法子数组 `now = {S['now']}`\nsf = {S['sf']}，ss = {S['ss']}（first / second 的前缀和）"
    if 'p' in S and ln >= 36:
        s += f"\n删除后最多 `res = {S['res']}`"
    return s


CONFIG = dict(
    num=3480, title='删除一个冲突对后最大子数组数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='first/second + 前缀和，算删除带来的增量',
    tags=['枚举右，维护左', '难度分 2764'],
    code='''
class Solution(object):
    def maxSubarrays(self, n, conflictingPairs):
        
        first = [1] * (n + 1)
        second = [1] * (n + 1)
        for x, y in conflictingPairs:
            if x > y:
                x, y = y, x
            if x + 1 > first[y]:
                first[y], second[y] = x + 1, first[y]
            elif x + 1 > second[y]:
                second[y] = x + 1
        
        sf = [0] * (n + 1)
        ss = [0] * (n + 1)
        now = 0

        for y in range(1, n + 1):
            if first[y - 1] > first[y]:
                second[y] = max(first[y], second[y - 1])
                first[y] = first[y - 1]
            elif first[y - 1] > second[y]:
                second[y] = first[y - 1]
        
            sf[y] = sf[y - 1] + first[y]
            ss[y] = ss[y - 1] + second[y]
            now += y - first[y] + 1
        
        p = [n] * (n + 1)
        for y in range(n - 1, 0, -1):
            if first[y] == first[y + 1]:
                p[y] = p[y + 1]
            else:
                p[y] = y

        res = now
        for x, y in conflictingPairs:
            if x > y:
                x, y = y, x
            
            if x + 1 == first[y]:
                res = max(res, now + (sf[p[y]] - sf[y - 1]) - (ss[p[y]] - ss[y - 1]))
        
        return res
''',
    call=f'Solution().maxSubarrays({N}, {PAIRS!r})',
    expect=12,
    skip=['sf = [0]', 'ss = [0]', 'now = 0', 'sf[y] = ', 'ss[y] = ', 'if x > y', 'x, y = y, x'],
    views=[
        dict(type='array', var='first', label='first[y]：最大的 x+1（左端点至少要 ≥ 它）', cell=110,
             pointers={'y': 'blue'}, h=250),
        dict(type='array', var='second', label='second[y]：不算 first 那个冲突对时的备选', cell=110, h=200),
        dict(type='array', var='p', label='p[y]：first 相同的这一段延伸到哪', cell=110, h=170),
        dict(type='text', fn=_show, size=26, h=120),
    ],
    watch=[('y', 'y', 'blue'), ('now', 'now', 'green'), ('res', 'res', 'orange')],
    captions={
        'first = [1]': '`first[y]` 先设成 1：没有冲突时左端点最小是 1',
        'second = [1]': '`second[y]` 同样从 1 开始',
        'if x + 1 > first[y]': lambda S, B, r: (f'冲突对 `({S.x}, {S.y})`：`x + 1 = {S.x + 1}` 比当前最大值 `first[{S.y}] = {S.first[S.y]}` 大 → ==成为新的 first，旧值退为 second=='
                                                 if S.x + 1 > S.first[S.y] else f'`x + 1 = {S.x + 1}` 不比 `first[{S.y}] = {S.first[S.y]}` 大，看能不能更新 second'),
        'first[y], second[y] = x + 1, first[y]': '`first[{y}] = {first[y]}`，`second[{y}] = {second[y]}`',
        'elif x + 1 > second[y]': lambda S, B, r: (f'`x + 1 = {S.x + 1}` 比 `second[{S.y}] = {S.second[S.y]}` 大 → 更新 second'
                                                    if S.x + 1 > S.second[S.y] else '也不比 second 大，忽略'),
        'second[y] = x + 1': '`second[{y}] = {second[y]}`',
        'for y in range(1, n + 1)': lambda S, B, r: (f'从左到右处理右端点 `y = {S.y}`：左边的限制会传给右边' if S.y <= N
                                                      else '处理完毕'),
        'if first[y - 1] > first[y]': lambda S, B, r: (
            f'`first[{S.y - 1}] = {S.first[S.y - 1]}` > `first[{S.y}]`：左边限制更严 → ==first 继承左边，原 first 候选进 second=='
            if S.first[S.y - 1] > B.first[S.y] else f'`first[{S.y - 1}] = {S.first[S.y - 1]}` 不比 `first[{S.y}]` 大，first 不变'),
        'second[y] = max(first[y]': '`second[{y}] = {second[y]}`：取原 first 与左边 second 的较大者',
        'first[y] = first[y - 1]': '`first[{y}] = {first[y]}`',
        'elif first[y - 1] > second[y]': lambda S, B, r: (f'`first[{S.y - 1}] = {S.first[S.y - 1]}` 比 `second[{S.y}] = {S.second[S.y]}` 大 → 抬高 second'
                                                          if S.first[S.y - 1] > S.second[S.y] else 'second 也不用动'),
        'second[y] = first[y - 1]': '`second[{y}] = {second[y]}`',
        'now += ': '右端点 `y = {y}` 有 `y − first[y] + 1` = {y - first[y] + 1} 个合法子数组 → `now = {now}`；同时累加前缀和 `sf`、`ss`',
        'p = [n]': '`p[y]`：从 y 往右，`first` 值相同的这一段能延伸到哪',
        'for y in range(n - 1': lambda S, B, r: f'从右往左算 `p`，`y = {S.y}`' if S.y < N else '算完了',
        'if first[y] == first[y + 1]': lambda S, B, r: (f'`first[{S.y}] == first[{S.y + 1}]`：同一段 → 沿用 `p[{S.y + 1}]`'
                                                         if S.first[S.y] == S.first[S.y + 1] else f'`first[{S.y}] != first[{S.y + 1}]`：段到 y 为止'),
        'p[y] = p[y + 1]': '`p[{y}] = {p[y]}`',
        'p[y] = y': '`p[{y}] = {p[y]}`',
        'res = now': '先假设删了没好处：`res = now = {res}`',
        'for x, y in conflictingPairs': lambda S, B, r: ('先把每个冲突对 `(x, y)` 放进 `first / second`' if S.get('_line') == 6
                                                          else '枚举每个冲突对，试试删掉它'),
        'if x + 1 == first[y]': lambda S, B, r: (f'`x + 1 = {S.x + 1} == first[{S.y}]`：删它会让 `first[{S.y}]` 退成 `second[{S.y}]`，右边同段也跟着变'
                                                  if S.x + 1 == S.first[S.y] else f'`x + 1 = {S.x + 1} != first[{S.y}] = {S.first[S.y]}`：它不是最严的限制，删了不影响'),
        'res = max(res, now': '增量 = first 的区间和 − second 的区间和（`y..p[y]`）→ `res = {res}`',
        'return res': '最多能得到 =={ret}== 个合法子数组',
    },
    cards=dict(
        one_liner='first/second 记下最严与次严的限制，删除的收益用前缀和 O(1) 算',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['`nums = [1..n]`，给若干冲突对 `[a, b]`，==恰好删一个==',
                 '数不含任何剩余冲突对两端的子数组个数，求最大值',
                 '示例：`n = 5, [[1,2],[2,5],[3,5]]` → `12`',
                 '本视频用示例 2'],
        quote='枚举数组中的每个下标index，计算以index为右边界的合法子数组的数目，累加起来即为最终答案。……将f[y]改写为两个数组first和second。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举右端点 `y`，`first[y]` = 最小合法左端点，该右端点有 `y − first[y] + 1` 个子数组',
              '`first[y]` 要取左边所有 `first` 的最大（前面的限制会往后传）',
              '再记一个 `second[y]`：删掉最严的冲突对后，左端点能放宽到哪',
              '`p[y]` 记 first 相同的一段延伸到哪，一段一起变 → 用前缀和 `sf/ss` 算增量'],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '易错：删掉某个冲突对，右边 `first` 相同的一整段都会跟着变，所以要 `p[y]` 和前缀和',
                 '只有 `x + 1 == first[y]` 的冲突对才值得删',
                 '原文为 Python 2 风格，本题没有需要改动的写法，代码照原文',
                 '对比灵神：灵神倒着枚举左端点，用最小/次小 b 和 extra 累加；yiduobo 正着枚举右端点'],
    ),
)
