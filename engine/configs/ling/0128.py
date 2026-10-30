def _order(S):
    return list(S['st']) if 'st' in S else None


def _xi(S):
    if 'x' not in S or 'st' not in S:
        return None
    return list(S['st']).index(S['x'])


def _yi(S):
    if not _chain_ok(S) or S['y'] not in S['st']:
        return None
    return list(S['st']).index(S['y'])


def _chain_ok(S):
    st, x, y = S.get('st'), S.get('x'), S.get('y')
    if st is None or x is None or y is None or x - 1 in st:
        return False
    return x < y and all(v in st for v in range(x, y))


def _color(S, i, v):
    if 'x' not in S:
        return None
    st, x = S['st'], S['x']
    if _chain_ok(S) and x <= v < S['y']:
        return 'green'
    if v == x:
        return 'purple' if x - 1 in st else 'blue'
    return None


def _chain_text(S):
    st, x = S.get('st'), S.get('x')
    if st is None or x is None:
        return '遍历哈希集合，只从==序列起点==开始往后数'
    if x - 1 in st:
        return f"`x = {x}`：`x − 1 = {x - 1}` 在集合中 → ==不是起点，跳过=="
    if not _chain_ok(S):
        return f"`x = {x}`：`x − 1 = {x - 1}` 不在集合中 → ==x 是起点=="
    y = S['y']
    chain = ' '.join(f'`{v}`' for v in range(x, y))
    tail = f'`{y}` 在集合中，继续' if y in st else f'`{y}` ==不在==，序列断了'
    return f"从 `{x}` 往后数：{chain}  → 查 {tail}"


def _skip_q(S, B, ret):
    x, st = S.x, S.st
    if x - 1 in st:
        return f'`{x - 1}` 在集合里：以 `{x - 1}` 为起点的序列一定更长 → `{x}` ==不是起点=='
    return f'`{x - 1}` 不在集合里 → `{x}` 是一段连续序列的==起点=='


CONFIG = dict(
    num=128, title='最长连续序列', difficulty='Medium', category='哈希',
    author='灵茶山艾府', technique='哈希集合 + 只从起点枚举',
    code='''
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        st = set(nums)  # 把 nums 转成哈希集合
        ans = 0
        for x in st:  # 遍历哈希集合
            if x - 1 in st:  # 如果 x 不是序列的起点，直接跳过
                continue
            # x 是序列的起点
            y = x + 1
            while y in st:  # 不断查找下一个数是否在哈希集合中
                y += 1
            # 循环结束后，y-1 是最后一个在哈希集合中的数
            ans = max(ans, y - x)  # 从 x 到 y-1 一共 y-x 个数
        return ans
''',
    call='Solution().longestConsecutive([100, 4, 200, 1, 3, 2])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=170, cell=80, label='nums（原数组，无序）'),
        dict(type='array', var=_order, pointers={_xi: 'blue', _yi: 'yellow'}, pointer_labels={_xi: 'x', _yi: 'y'}, color=_color, h=230, cell=96,
             label='st（哈希集合，按遍历顺序；紫 = 非起点，绿 = 当前连续段）'),
        dict(type='text', fn=_chain_text, size=30),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'st = set(nums)': '把 `nums` 转成==哈希集合==：`O(1)` 判断一个数在不在，顺便去重',
        'ans = 0': '`ans` 记录最长连续序列的长度',
        'for x in st': lambda S, B, r: ('遍历结束' if 'x' in B and B.x == S.x else
                                        f'遍历==哈希集合==（不是 nums）：`x = {S.x}`' if 'x' not in B else f'下一个：`x = {S.x}`'),
        'if x - 1 in st': _skip_q,
        'continue': lambda S, B, r: ('直接跳过：避免从序列中间开始的大量重复计算' if S.x == sorted(v for v in S.st if v - 1 in S.st)[0] else '跳过'),
        'y = x + 1': '`{x}` 是起点：从 `y = {y}` 开始往后找',
        'while y in st': lambda S, B, r: (f'`{S.y}` 在集合中 → 序列还能延长' if S.y in S.st
                                          else f'`{S.y}` 不在集合中 → 序列到 `{S.y - 1}` 为止'),
        'y += 1': '下一个数：`y` → {y}',
        'ans = max': '从 `{x}` 到 `{y - 1}` 一共 `y − x = {y - x}` 个数：`ans = max({B.ans}, {y - x}) = {ans}`',
        'return ans': '返回最长长度 `{ans}`',
    },
    cards=dict(
        one_liner='只从序列起点往后数，每个数至多被访问两次',
        complexity='时间 `O(n)`，空间 `O(m)`（m 为不同元素个数）',
        problem=['未排序整数数组 `nums`，求==数值连续==的最长序列长度（不要求在原数组中相邻）',
                 '要求 `O(n)` 时间，所以==不能排序==',
                 '示例：`[100,4,200,1,3,2]` → `4`（最长是 `1,2,3,4`）'],
        quote='如果 x−1 在哈希集合中，则不以 x 为起点。为什么？因为==以 x−1 为起点计算出的序列长度，一定比以 x 为起点计算出的序列长度要长==！这样可以避免大量重复计算。',
        quote_src='—— 灵茶山艾府题解「关键优化 2」',
        idea=['优化一：把数都放进==哈希集合==，`O(1)` 判断 `x+1` 在不在',
              '优化二：`x−1` 在集合里就跳过 —— 每条连续段只从起点数一次',
              '⚠ 遍历集合而不是 nums：重复的起点多时会退化成 `O(n²)`'],
        summary=['时间 `O(n)`：每个数在外层循环、内层循环中各至多遍历一次',
                 '易错：遍历 `nums` 而不是 `st`，大量重复元素时会超时',
                 '`y` 停在第一个==不在==集合的数，长度是 `y − x`，不是 `y − x + 1`',
                 '小优化：若 `ans * 2 >= m`，不可能再有更长的段，可直接 `break`'],
    ),
)
