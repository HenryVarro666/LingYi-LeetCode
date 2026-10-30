NUMS = [1, 2, 3, 1, 1, 3]


def J(S):
    """代码里没有 j：当前 x 是 nums[j]，而 j 左边的数都已记进 cnt → j = cnt 里的总次数"""
    c = S.get('cnt')
    if c is None or 'x' not in S:
        return None
    j = sum(c.values()) - (1 if S.get('_line') == 9 else 0)  # 第 9 行 cnt[x] += 1 之后要减掉自己
    return j if j < len(NUMS) else None


def _cell_color(S, i, v):
    j = J(S)
    if j is None:
        return None
    if i == j:
        return 'blue'
    if i < j and v == NUMS[j]:
        return 'green'
    return None


def _found(S):
    """按发现顺序列出所有好数对，取前 ans 个（ans 就是目前找到的个数）"""
    if 'ans' not in S:
        return None
    allp = [f'({i},{k})' for k in range(len(NUMS)) for i in range(k) if NUMS[i] == NUMS[k]]
    return set(allp[:S['ans']])


def _pairs(S):
    j = J(S)
    if j is None:
        return ''
    left = [i for i in range(j) if NUMS[i] == NUMS[j]]
    if not left:
        return f'`j = {j}`，`x = {NUMS[j]}`：左边没有 `{NUMS[j]}`，凑不出好数对'
    ps = ' '.join(f'({i},{j})' for i in left)
    return f'`j = {j}`，`x = {NUMS[j]}`：左边有 =={len(left)}== 个 `{NUMS[j]}` → 新增好数对 `{ps}`'


CONFIG = dict(
    num=1512, title='好数对的数目', difficulty='Easy', category='哈希',
    author='灵茶山艾府', technique='枚举右，维护左',
    tags=['List.md'],
    code='''
class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        ans = 0
        cnt = defaultdict(int)
        for x in nums:  # x = nums[j]
            # 此时 cnt[x] 表示之前遍历过的 x 的个数，加到 ans 中
            # 如果先执行 cnt[x] += 1，再执行 ans += cnt[x]，就把 i=j 这种情况也统计进来了，算出的答案会偏大
            ans += cnt[x]
            cnt[x] += 1
        return ans
''',
    call=f'Solution().numIdenticalPairs({NUMS})',
    expect=4,
    views=[
        dict(type='array', var=lambda S: NUMS, label='nums（蓝 = 当前 j，绿 = 左边和它相等的 i）', cell=84,
             pointers={J: 'blue'}, pointer_labels={J: 'j'}, color=_cell_color,
             dim=lambda S, i, v: J(S) is not None and i > J(S)),
        dict(type='text', h=60, fn=_pairs, size=26),
        dict(type='map', var='cnt', label='cnt（左边每个数出现了几次）', h=130, font=28, fmt=lambda k, v: f'{k} 出现 {v} 次'),
        dict(type='set', var=_found, label='已找到的好数对 (i, j)（黄框 = 这一步新增）', h=130, font=28),
    ],
    watch=[('j', J, 'blue'), ('x', 'x', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计好数对 `(i, j)` 的个数',
        'cnt = defaultdict': '`cnt[x]`：==j 左边== `x` 出现的次数（维护左）',
        'for x in nums': lambda S, B, ret: (f'枚举右：`j = {J(S)}`，`x = nums[{J(S)}] = {S.x}`'
                                            if J(S) is not None else '枚举完毕'),
        'ans += cnt[x]': lambda S, B, ret: (
            f'左边有 `cnt[{S.x}] = {B.cnt.get(S.x, 0)}` 个 `{S.x}`，==每个都能和 j 配对== → `ans = {B.ans} + {B.cnt.get(S.x, 0)} = {S.ans}`'
            if B.cnt.get(S.x, 0) else f'左边还没有 `{S.x}`（`cnt[{S.x}] = 0`）→ `ans` 不变，仍为 `{S.ans}`'),
        'cnt[x] += 1': lambda S, B, ret: f'==再==把 `x = {S.x}` 记进左边：`cnt[{S.x}] = {S.cnt[S.x]}`，留给后面的 j 使用',
        'return ans': '一共 =={ret}== 组好数对',
    },
    cards=dict(
        one_liner='遍历到 x 时，答案加上左边已经出现过的 x 的个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你整数数组 `nums`，若 `nums[i] == nums[j]` 且 `i < j`，`(i, j)` 就是==好数对==',
                 '返回好数对的数目',
                 '示例：`[1,2,3,1,1,3]` → `4`：`(0,3) (0,4) (3,4) (2,5)`'],
        before=[dict(heading='暴力思路', lines=[
            '写个二重循环：枚举 `j`，统计左边（因为要求 `i < j`）有多少个数等于 `nums[j]`',
            '这需要 `O(n^2)` 的时间',
            '能不能不回头数？==边走边记==左边每个数出现了几次'])],
        quote='一般地，遍历到元素 x 时，==把答案增加之前遍历过的 x 的个数==。我们可以在遍历的过程中，用一个哈希表（或者数组）统计每个元素的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['==枚举右==：把 `x = nums[j]` 当成数对的右端点',
              '==维护左==：`cnt[x]` 记录左边 `x` 的个数，每个都能和 `j` 组成好数对',
              '所以 `ans += cnt[x]`，然后 `cnt[x] += 1`，把 `x` 也变成“左边”'],
        result='运行结束，返回 `4`：`(0,3) (0,4) (3,4) (2,5)`',
        summary=['时间 `O(n)`，空间 `O(n)`（值域小也可以用数组代替哈希表）',
                 '易错：==先更新答案，再更新 cnt==；反过来会把 `i = j` 也算进去，答案偏大',
                 '「枚举右，维护左」是两数之和、好数对这类 `i < j` 配对问题的通用模板',
                 '更多相似题目见灵神数据结构题单「§0.1 枚举右，维护左」'],
    ),
)
