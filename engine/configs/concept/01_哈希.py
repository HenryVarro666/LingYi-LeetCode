def _pal(k):
    return ['blue', 'pink', 'green', 'purple', 'cyan', 'orange'][k % 6]


def _arr_color(S, i, v):
    if 'idx' in S:                       # 模板①：j 左边的数都已进哈希表
        if 'j' in S and i < S['j']:
            return 'purple'
        return None
    if 'd' in S:                         # 模板②：已分好组的串按组上色
        for k, grp in enumerate(S['d'].values()):
            if v in grp:
                return _pal(k)
    return None


def _formula(S):
    if 'idx' in S and 'x' in S:
        need = S['target'] - S['x']
        hit = need in S['idx']
        return (f"右 `x = {S['x']}`，在左边找 `target − x = {need}` → "
                + (f"==找到，下标 {S['idx'][need]}==" if hit else '不在哈希表'))
    if 'd' in S and 'key' in S:
        return f"`'{S['s']}'` 排序 → key = =={S['key']}==，同 key 的串放进同一组"
    if 'd' in S:
        return '模板②：哈希分组——设计一个 ==同组必相同== 的 key'
    return '模板①：枚举右，维护左——哈希表存「左边见过的数」'


CONFIG = dict(
    num=None, title='哈希 · 通用思想与模板', author='概念讲解', category='哈希',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def two_sum(nums, target):
    idx = {}                       # 左边出现过的数 → 它的下标
    for j, x in enumerate(nums):   # 枚举右：x = nums[j]
        if target - x in idx:      # 左边有没有 target - x？
            return [idx[target - x], j]
        idx[x] = j                 # 维护左：先查再存
    return []

def group(strs):
    d = defaultdict(list)          # key → 同一组的字符串
    for s in strs:
        key = ''.join(sorted(s))   # 异位词排序后一定相同
        d[key].append(s)           # 放进 key 对应的组
    return list(d.values())
''',
    call='''
a = two_sum([3, 6, 1, 8, 2, 7], 13)
b = group(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
(a, b)
''',
    expect=([1, 5], [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]),
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var=lambda S: S['nums'] if 'nums' in S else S.get('strs'), label='输入',
             pointers={'j': 'blue'}, color=_arr_color, h=190),
        dict(type='map', var=lambda S: S['idx'] if 'idx' in S else S.get('d'), label='哈希表',
             fmt=lambda k, v: f"{k} → {','.join(v)}" if isinstance(v, list) else f'{k} → {v}', font=28, h=220),
    ],
    watch=[('j', 'j', 'blue'), 'x', ('target - x', 'target - x', 'yellow'), 's', ('key', 'key', 'green')],
    captions={
        'idx = {}': '模板① 两数之和：哈希表 `idx` 记录 ==j 左边每个数 → 下标==，一开始为空',
        'for j, x': lambda S, B, ret: (f'枚举右：`j = {S.j}`，`x = {S.x}`。==紫色格子== = 已存进哈希表的「左边」'
                                       if S.j < 2 else f'枚举右：`j = {S.j}`，`x = {S.x}`'),
        'if target - x': lambda S, B, ret: (f'`O(1)` 查 `{S.target - S.x}` 在不在左边 → ==在！=='
                                            if S.target - S.x in S.idx else
                                            f'`O(1)` 查 `{S.target - S.x}` 在不在左边 → 不在，配不成对'),
        'return [idx': '配对成功：`nums[{ret[0]}] + nums[{ret[1]}] = {target}`，一层循环 ==O(n)== 搞定',
        'idx[x] = j': '维护左：`idx[{x}] = {j}`。==先查再存==，保证不会和自己配对',
        'd = defaultdict': '模板② 分组：`d` 把 ==key → 同组字符串列表==，key 不存在时自动建空列表',
        'for s in strs': lambda S, B, ret: (f"取下一个字符串 `'{S.s}'`" if B.get('s') != S.s
                                            else 'for 结束：所有字符串都分好组了'),
        'key = ': "`'{s}'` 排序得 key = =={key}==：异位词的字母相同，排序后必然相同",
        'd[key].append': "`d['{key}']` 加入 `'{s}'` → 这一组现在有 {len(d[key])} 个",
        'return list(d': '哈希表的所有 value 就是答案：共 =={len(d)} 组==',
    },
    cards=dict(
        one_liner='用 `O(1)` 的查找换掉一层循环：空间换时间',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem_heading='什么时候用？',
        problem=['要找「配对」：`a + b = target`、差值、补数——两层循环想降到一层',
                 '要快速判断「某个值出现过没有」或统计出现次数',
                 '要按某种特征 ==分组==（异位词、同频次、同余数）',
                 '题目要求 `O(n)`，而排序是 `O(n log n)`'],
        before=[dict(heading='核心概念：枚举右，维护左', lines=[
            '两个变量的问题：==枚举一个，把它当常量==，另一个交给哈希表查',
            '遍历到 `j` 时，哈希表里恰好是 `nums[0..j-1]` 的信息',
            '==先查再存==：先查 `target - x`，再存 `x`，下标一定不同',
            '分组的关键是 key：排序后的串 / 26 个字母的计数，同组必相同',
            '只问「在不在」用 `set`，要存下标/次数用 `dict` / `Counter`']),
        ],
        idea_heading='两位作者怎么说',
        quote='很多涉及到「两个变量」的题目，都可以枚举其中一个变量，把它当成==常量==看待……代码实现时，通常来说「==枚举右，寻找左==」是更加好写的。',
        quote_src='—— 灵茶山艾府 · 1. 两数之和',
        idea=['灵神用「获取了多少信息」解释：查一次哈希表，花 `O(1)` 就拿到 `O(n)` 个数的信息',
              'yiduobo 在 1 题给的是排序 + 双指针 `O(n log n)`；49 题用 ==字母计数== 当 key',
              '128 题两人对称：灵神只从 ==起点== 往后数，yiduobo 只从 ==最大数== 往前数'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`1` 两数之和：枚举右，查 `target - x`，先查再存',
                 '`49` 字母异位词分组：排序后的串（或字母计数）当 key',
                 '`128` 最长连续序列：哈希集合，只从 `x-1` 不在的起点往后数',
                 '易错：先存后查会和自己配对；128 要遍历 ==集合== 而不是 nums'],
    ),
)
