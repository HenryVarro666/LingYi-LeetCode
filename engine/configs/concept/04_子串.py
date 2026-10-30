def _pre(S):
    if 'nums' not in S:
        return None
    out, s = [0], 0
    upto = S['j'] + 1 if 'j' in S else 0
    for x in S['nums'][:upto]:
        s += x
        out.append(s)
    return out


def _pre_color(S, i, v):
    if 'j' not in S:
        return 'pink' if i == 0 else None
    if i == S['j'] + 1:
        return 'pink'                                  # 当前前缀和 s[j+1]
    if v == S['s'] - S['k']:
        return 'green'                                 # 能和当前配对的左端
    return None


def _formula(S):
    if 'j' not in S:
        return '子数组 `nums[i..j]` 的和 = `s[j+1] - s[i]`：变成 ==两个前缀和的配对== 问题'
    need = S['s'] - S['k']
    return f"当前前缀和 =={S['s']}==，要找左边的 `s − k = {need}`（绿色）"


def _ans_cap(S, B, ret):
    add = S.ans - B.ans
    if not add:
        return f'左边没有前缀和等于 `{S.s - S.k}` → 以 `j = {S.j}` 结尾的子数组都凑不出 {S.k}'
    pre = _pre(S)
    subs = '、'.join(f'`nums[{i}..{S.j}]`' for i in range(S.j + 1) if pre[i] == S.s - S.k)
    return f'左边有 =={add} 个== 前缀和等于 `{S.s - S.k}` → 找到 {subs}，`ans = {S.ans}`'


CONFIG = dict(
    num=None, title='子串 · 通用思想与模板', author='概念讲解', category='子串',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def subarray_sum(nums, k):         # 560. 和为 K 的子数组
    cnt = defaultdict(int)         # 前缀和 → 出现次数
    cnt[0] = 1                     # s[0] = 0：空前缀也要算
    ans = s = 0
    for j, x in enumerate(nums):   # 枚举右端点 j
        s += x                     # s = nums[0..j] 的和
        ans += cnt[s - k]          # 左边有几个前缀和 = s - k
        cnt[s] += 1                # 先查再存
    return ans
''',
    call='subarray_sum([1, 2, -1, 1, 2, -2, 3, 1, -1], 3)',
    expect=10,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var='nums', label='nums', pointers={'j': 'blue'}, cell=80,
             dim=lambda S, i, v: 'j' in S and i > S['j'], h=170),
        dict(type='array', var=_pre, label='前缀和 s（s[0] = 0；粉 = 当前，绿 = 能配对的左端）', cell=80,
             min_slots=10, color=_pre_color, h=150),
        dict(type='map', var=lambda S: {a: b for a, b in S['cnt'].items() if b} if 'cnt' in S else None,
             label='cnt：前缀和 → 出现次数', fmt=lambda a, b: f's={a}: {b}次', font=26, h=130),
    ],
    watch=[('j', 'j', 'blue'), 'x', ('s', 's', 'pink'), ('s - k', 's - k', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt` 记录 ==每个前缀和出现了几次==——这就是「维护左」',
        'cnt[0] = 1': '先放入 `s[0] = 0`：否则从下标 0 开始的子数组会被漏掉',
        'ans = s = 0': '`s` 是滚动的前缀和，`ans` 是和为 `k = {k}` 的子数组个数',
        'for j, x': lambda S, B, ret: (f'枚举右端点：`j = {S.j}`，`x = {S.x}`' if B.get('j') != S.j
                                       else 'nums 遍历完，循环结束'),
        's += x': '`s` 加上 `{x}` → 前缀和 `s = {s}`',
        'ans += cnt': _ans_cap,
        'cnt[s] += 1': '再把 `s = {s}` 存进去：`cnt[{s}] = {cnt[s]}`，给右边的 j 配对用',
        'return ans': '返回 `{ret}`：一次遍历 ==O(n)==，暴力要枚举 `O(n²)` 个子数组',
    },
    cards=dict(
        one_liner='子数组和 = 两个前缀和之差，再用哈希表「枚举右，维护左」',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem_heading='什么时候用？',
        problem=['求 ==连续== 子数组的和 / 个数，且数组 ==有负数==（滑窗失效）',
                 '「和为 k」「和被 k 整除」「0 和 1 一样多」→ 前缀和之差',
                 '窗口内的最大 / 最小值 → 单调队列（239）',
                 '包含某些字符的最短子串 → 不定长滑窗 + 计数（76）'],
        before=[dict(heading='核心概念：子数组和 = 前缀和之差', lines=[
            '定义 `s[0] = 0`，`s[i] = nums[0] + … + nums[i-1]`',
            '`nums[i..j-1]` 的和 = `s[j] - s[i]`：子数组 → ==两个前缀和配对==',
            '枚举右端 `s[j]`，哈希表数一数左边有几个 `s[i] = s[j] - k`',
            '`cnt[0] = 1` 不能少：它对应「从头开始」的子数组',
            '先 `ans += cnt[s-k]` 再 `cnt[s] += 1`：`k = 0` 时反过来会错']),
        ],
        idea_heading='两位作者怎么说',
        quote='问题转化为：s 中有多少对下标 (i,j) 满足 0≤i<j≤n 且 s[j] − s[i] = k？写成 s[j] + (−s[i]) = k 就能看得更明白，==这是梦开始的地方——1. 两数之和==。',
        quote_src='—— 灵茶山艾府 · 560. 和为 K 的子数组',
        idea=['灵神：保留「外层枚举 j」，内层用哈希表优化成 `O(1)`，所以不重不漏',
              'yiduobo：看到子数组和就联想前缀和，并提醒 ==前缀和直接等于 k== 也是解',
              '239 两人同一结论：窗口里 ==左边更小的数永远当不了最大值=='],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`560` 和为 K 的子数组：前缀和 + 哈希，`cnt[0] = 1`',
                 '`239` 滑动窗口最大值：单调队列——右边入、左边出、队首即答案',
                 '`76` 最小覆盖子串：不定长滑窗 + 计数，覆盖了就收缩左端',
                 '易错：有负数不能用滑窗；先查 `cnt[s-k]` 再存 `s`'],
    ),
)
