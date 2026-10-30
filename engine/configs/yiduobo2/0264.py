N = 6   # 前 6 个丑数：1 2 3 4 5 6
MUL = [2, 3, 5]


def _sel(S):
    return S.get('_line') in (20, 21)


def q_view(k):
    def color(S, i, v):
        pos = S.get('pos') or [0, 0, 0]
        if _sel(S) and S.get('index') == k and i == pos[k]:
            return 'yellow'
        if S.get('_line') == 24 and S.get('next_pos') == k and i == pos[k] - 1:
            return 'green'
        return None

    return dict(type='array', var=lambda S: S['num_list'][k] if 'num_list' in S else None,
                label=f'×{MUL[k]} 队列（灰 = 已用掉，箭头 = 队首）', cell=72, h=178,
                pointers={f'pos[{k}]': 'blue'}, pointer_labels={f'pos[{k}]': f'pos[{k}]'},
                dim=lambda S, i, v: 'pos' in S and i < S['pos'][k], color=color)


def done(S):
    if 'num_list' not in S:
        return '按从小到大的顺序生成丑数'
    q, p = S['num_list'], S['pos']
    got = sorted([1] + q[0][:p[0]] + q[1][:p[1]] + q[2][:p[2]])
    return '已确定的丑数：' + '，'.join(f'`{x}`' for x in got) + f'（共 {len(got)} 个）'


def cap_outer(S, B, ret):
    k = sum(S.pos)          # 已经选出了 k 个（不含 1）
    if k == S.n - 1:
        return f'已经选出第 `{S.n}` 个丑数，循环结束'
    return (f'当前最小的丑数 `now = {S.now}`：用它乘 2、3、5 生成新丑数' if k == 0 else f'用 `now = {S.now}` 生成新丑数')


def cap_gen(S, B, ret):
    v = S.now * S.multi
    if v in B.num_set:
        return f'`{S.now}×{S.multi} = {v}` ==已经在集合里== → 别的队列已有，跳过（防止重复）'
    return f'`{S.now}×{S.multi} = {v}` 没出现过 → 记入集合，放进 ×{S.multi} 队列末尾'


def cap_cmp(S, B, ret):
    i = S.index
    h = S.num_list[i][S.pos[i]]
    if B.now is None:
        return f'×{MUL[i]} 队首 `{h}`：还没有候选 → 先选它'
    if B.now > h:
        return f'×{MUL[i]} 队首 `{h}` < 当前候选 `{B.now}` → ==换成它=='
    return f'×{MUL[i]} 队首 `{h}` ≥ 当前候选 `{B.now}` → 不换'


CONFIG = dict(
    num=264, title='丑数II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='三个递增队列 + 集合判重',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def nthUglyNumber(self, n):
        if n == 1:
            return 1

        num_list = [[], [], []]
        pos = [0, 0, 0]
        num_set = set()

        now = 1
        for index in range(1, n):
            for index, multi in enumerate([2, 3, 5]):
                if now * multi not in num_set:
                    num_set.add(now * multi)
                    num_list[index].append(now * multi)

            now = None
            next_pos = None
            for index in range(3):
                if now is None or now > num_list[index][pos[index]]:
                    now = num_list[index][pos[index]]
                    next_pos = index

            pos[next_pos] += 1

        return now
''',
    call=f'Solution().nthUglyNumber({N})',
    expect=6,
    views=[q_view(0), q_view(1), q_view(2),
           dict(type='text', fn=done, size=26, h=90)],
    watch=[('now', 'now', 'green'), ('multi', 'multi'), ('next_pos', 'next_pos'),
           ('num_set', 'sorted(num_set)', 'purple')],
    skip=['for index, multi', 'for index in range(3)', 'num_set.add', 'num_list[index].append', 'next_pos = None', 'next_pos = index'],
    captions={
        'if n == 1': '`n = {n}` 不是 1，开始生成',
        'num_list = [[], [], []]': '三个队列：分别存 ==×2、×3、×5== 的结果',
        'pos = [0, 0, 0]': '`pos[i]` 是第 i 个队列的队首下标（不真正出队）',
        'num_set = set()': '`num_set` 记录进过队列的数，用来判重',
        'now = 1': '第 1 个丑数是 `1`',
        'for index in range(1, n)': cap_outer,
        'if now * multi not in num_set': cap_gen,
        'now = None': lambda S, B, ret: ('按从小到大用丑数生成 → ==三个队列都递增==；三个队首的最小值就是下一个丑数'
                                         if sum(S.pos) == 0 else '比较三个队首，选最小的'),
        'if now is None or now >': cap_cmp,
        'now = num_list[index][pos[index]]': '当前候选 `now = {now}`（来自 ×{[2,3,5][index]} 队列）',
        'pos[next_pos] += 1': lambda S, B, ret: (f'选出 `{S.now}`：它是第 =={sum(S.pos) + 1}== 个丑数；'
                                                 f'×{MUL[S.next_pos]} 队列队首后移'),
        'return now': '第 `{n}` 个丑数是 =={ret}==',
    },
    max_steps=72,
    cards=dict(
        one_liner='×2、×3、×5 各一个递增队列，每次取三个队首的最小值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['丑数：只含质因数 `2`、`3`、`5` 的正整数（`1` 也算）',
                 '求第 `n` 个丑数',
                 '示例：`n = 10` → `12`（`1,2,3,4,5,6,8,9,10,12`）',
                 '本视频用 `n = 6` → `6`'],
        quote='一个很自然的想法就是使用三个队列，分别将乘2，乘3以及乘5的结果保存起来。如果我们是按照从小到大的顺序使用丑数生成新的丑数，那么这三个队列一定是单调递增的。',
        quote_src='—— yiduobo 知乎题解',
        idea=['难点：`A<B` 时只知道 `A×2<B×2`、`A×2<A×3`，但 `A×3` 和 `B×2` 谁大不确定',
              '把 ×2、×3、×5 的结果分开放进三个队列，每个队列都递增',
              '三个队首的最小值就是下一个丑数；再用它乘 2、3、5，==用 set 跳过重复=='],
        result='第 6 个丑数 `6` ✓（`1,2,3,4,5,6`）',
        summary=['时间 `O(n)`：每个丑数最多进队一次、做三次乘法；空间 `O(n)`',
                 '易错：`6 = 2×3 = 3×2` 会被生成两次，必须判重，否则答案里出现重复',
                 '用下标 `pos` 代替出队，三个队列就是三个数组',
                 '与“三指针 DP”本质相同：三个队列里的数就是 `dp[p2]×2`、`dp[p3]×3`、`dp[p5]×5`',
                 '原文为 Python 2 风格，已删去文档字符串，代码未改'],
    ),
)
