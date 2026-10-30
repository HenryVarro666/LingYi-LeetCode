def _fen_pic(cv, T, box, tree, old, vals, cur, title, vlabel='值'):
    """树状数组：上排 = 位置 1..m 的值，下面每根条 = tree[i] 管的关键区间 [i-lowbit+1, i]（按 lowbit 分层）；
    黄色 = 当前正在访问的 tree[i]，蓝色 = 它覆盖的位置，黄边 = 这一步刚改过"""
    x0, y0, x1, y1 = box
    m = len(tree) - 1
    cv.text((x0 + 18, y0), title, 22, T['muted'], bold=True)
    if m < 1:
        return
    cell = min(120, (x1 - x0 - 60) / m)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * m) / 2
    ty = y0 + 34
    nlev = max(i & -i for i in range(1, m + 1)).bit_length()
    rowh = min(60, (y1 - (ty + 76)) / nlev)
    lo = hi = None
    if cur is not None and 1 <= cur <= m:
        hi = cur
        lo = cur - (cur & -cur) + 1
    for i in range(1, m + 1):
        X = sx + (i - 1) * cell
        covered = lo is not None and lo <= i <= hi
        cv.rect((X + 2, ty, X + cell - 2, ty + 42), fill=T['blue'] if covered else T['panel2'], r=6, alpha=200 if covered else 255)
        v = vals[i - 1] if i - 1 < len(vals) else ''
        cv.text((X + cell / 2, ty + 21), v, 24, T['bg'] if covered else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ty + 48), i, 18, T['dim'], anchor='mt', mono=True)
    by = ty + 72
    for i in range(1, m + 1):
        lb = i & -i
        lv = lb.bit_length() - 1
        xa, xb = sx + (i - lb) * cell + 3, sx + i * cell - 3
        ya = by + lv * rowh
        changed = old is not None and len(old) == len(tree) and old[i] != tree[i]
        if i == cur:
            fill, tc = T['yellow'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((xa, ya, xb, ya + rowh - 5), fill=fill, outline=T['yellow'] if changed else T['border'], width=3 if changed else 1, r=6)
        lab = f't{i}={tree[i]}' if cell * lb > 150 else f'{tree[i]}'
        if lb > 1:
            lab = f't{i}={tree[i]}  [{i - lb + 1},{i}]' if cell * lb > 260 else f't{i}={tree[i]}'
        cv.text(((xa + xb) / 2, ya + (rowh - 5) / 2), lab, 20, tc, anchor='mm', bold=True)


def _lb_text(i):
    return f'`{i}` = `{i:b}`（二进制），lowbit = `{i & -i}`'
def _mk(name, title):
    def draw(cv, S, B, box, T):
        t = S.get(name)
        mp = S.get('mapping')
        if t is None or mp is None:
            cv.text((box[0] + 18, box[1]), f'{name}（还没建）', 22, T['dim'])
            return
        f, x = S.get('f'), S.get('x')
        cur = x if (f is not None and f is t and x is not None and x >= 1) else None
        _fen_pic(cv, T, box, t, B.get(name), sorted(mp), cur, title)
    return draw


def _info(S):
    if 'v' in S and 'cnt1' not in S and 'mapping' in S and 'arr1' not in S:
        return ''
    if 'cnt1' in S and 'cnt2' in S:
        return f"大于 `{S['v']}` 的个数：`arr1` 有 `{S['cnt1']}` 个，`arr2` 有 `{S['cnt2']}` 个（长度减去 ≤ 它的个数）"
    if 'mapping' in S and 'arr1' not in S:
        return f"离散化：数字 → 名次 `mapping = {S['mapping']}`"
    return ''


CONFIG = dict(
    num=3072, title='将元素分配到两个数组中 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='离散化 + 两个树状数组',
    tags=['常用数据结构', '树状数组和线段树', '难度分 2053'],
    code='''
class Solution(object):
    def resultArray(self, nums):

        mapping = {}
        rank = 1
        for v in sorted(nums):
            if v not in mapping:
                mapping[v] = rank
                rank += 1
        
        def add(f, x):
            while x < rank:
                f[x] += 1
                x += x & -x
        
        def get(f, x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s
        
        arr1 = [nums[0]]
        f1 = [0] * rank
        add(f1, mapping[nums[0]])
        arr2 = [nums[1]]
        f2 = [0] * rank
        add(f2, mapping[nums[1]])
        for v in nums[2:]:
            cnt1 = len(arr1) - get(f1, mapping[v])
            cnt2 = len(arr2) - get(f2, mapping[v])
            if cnt1 > cnt2 or (cnt1 == cnt2 and len(arr1) <= len(arr2)):
                arr1.append(v)
                add(f1, mapping[v])
            else:
                arr2.append(v)
                add(f2, mapping[v])
        
        return arr1 + arr2
''',
    call='Solution().resultArray([5, 14, 3, 1])',
    expect=[5, 3, 1, 14],
    max_steps=62,
    skip=['mapping = {}', 'rank = 1', 'f1 = [0] * rank', 'f2 = [0] * rank', 's = 0', 'rank += 1', 'if v not in mapping', 'while x < rank', 'while x > 0'],
    views=[
        dict(type='custom', draw=_mk('f1', 'f1（arr1 的树）：上排 = 数字（按名次 1,2,3… 排）；黄 = 当前下标'), h=250),
        dict(type='custom', draw=_mk('f2', 'f2（arr2 的树）'), h=250),
        dict(type='array', var='arr1', label='arr1', cell=64, h=100),
        dict(type='array', var='arr2', label='arr2', cell=64, h=100),
    ],
    watch=[('v', 'v', 'yellow'), ('cnt1', 'cnt1', 'blue'), ('cnt2', 'cnt2', 'pink'), ('x', 'x', 'blue'), ('s', 's', 'green')],
    captions={
        'for v in sorted(nums)': lambda S, B, r: (f'从小到大看 `{S.v}`：' + ('已有名次，跳过' if S.v in B['mapping'] else '新数字 → 发给下一个名次')),
        'if v not in mapping': lambda S, B, r: (f'`{S.v}` 还没有名次 → 给它' if S.v not in S.mapping else f'`{S.v}` 已有名次，跳过'),
        'mapping[v] = rank': '`mapping[{v}] = {rank}`：数值再大也只占一个名次',
        'rank += 1': '下一个名次 `{rank}`；最后 `rank` = 不同数字个数 + 1，也是树的长度',
        'arr1 = [nums[0]]': '第 1 次操作：`nums[0]` = {nums[0]} 放进 `arr1`',
        'add(f1, mapping[nums[0]])': '`arr1` 的树 `f1`：在名次 `{mapping[nums[0]]}` 上加 1',
        'arr2 = [nums[1]]': '第 2 次操作：`nums[1]` = {nums[1]} 放进 `arr2`',
        'add(f2, mapping[nums[1]])': '`arr2` 的树 `f2`：在名次 `{mapping[nums[1]]}` 上加 1',
        'for v in nums[2:]': '从第 3 个数开始，比较两边大于 `v` 的个数',
        'cnt1 = len(arr1)': '`arr1` 里大于 `{v}` 的个数 = 长度 `{len(arr1)}` − 前缀（≤ 名次 {mapping[v]}）的个数 = =={cnt1}==',
        'cnt2 = len(arr2)': '`arr2` 里大于 `{v}` 的个数 = 长度 `{len(arr2)}` − 前缀个数 = =={cnt2}==',
        'if cnt1 > cnt2 or': lambda S, B, r: (f'`cnt1 = {S.cnt1}` > `cnt2 = {S.cnt2}` → 放 `arr1`' if S.cnt1 > S.cnt2 else
                                                (f'`cnt1 = cnt2 = {S.cnt1}`，`len(arr1) = {len(S.arr1)} ≤ len(arr2) = {len(S.arr2)}` → 放 `arr1`'
                                                 if S.cnt1 == S.cnt2 and len(S.arr1) <= len(S.arr2) else
                                                 (f'`cnt1 = {S.cnt1}` < `cnt2 = {S.cnt2}` → 放 `arr2`' if S.cnt1 < S.cnt2 else
                                                  f'`cnt1 = cnt2`，但 `arr1` 更长（{len(S.arr1)} > {len(S.arr2)}）→ 放 `arr2`'))),
        'arr1.append(v)': '`{v}` 放进 `arr1`：`arr1 = {arr1}`',
        'arr2.append(v)': '`{v}` 放进 `arr2`：`arr2 = {arr2}`',
        'add(f1, mapping[v])': '同步更新 `f1`：名次 `{mapping[v]}` 加 1',
        'add(f2, mapping[v])': '同步更新 `f2`：名次 `{mapping[v]}` 加 1',
        'while x < rank': lambda S, B, r: (f'`x = {S.x}` < `rank = {S.rank}`：`f[{S.x}]` 管的区间含这个名次 → 加 1' if S.x < S.rank else f'`x = {S.x}` ≥ `rank`：越界，加完了'),
        'f[x] += 1': '`f[{x}]` 管 [{x - (x & -x) + 1}, {x}]，加 1 → =={f[x]}==',
        'x += x & -x': '`x += lowbit` → `{x}`：下一个包含该名次的区间',
        'while x > 0': lambda S, B, r: (f'`x = {S.x}` > 0：前缀还没数完' if S.x > 0 else '`x = 0`：前缀数完了'),
        's += f[x]': '`f[{x}]` 管 [{x - (x & -x) + 1}, {x}]，加进 `s` → =={s}==',
        'x -= x & -x': '去掉最低位的 1：`{B.x}` → `{x}`',
        'return s': lambda S, B, r: (lambda nm: f'前缀里 ≤ `{S.v}` 的个数 = `{r}`；`{nm}` 共 {len(S[nm])} 个，大于的个数 = {len(S[nm])} − {r} = =={len(S[nm]) - r}==')
                                      ('arr1' if S.f is S.f1 else 'arr2'),
        'return arr1 + arr2': '`arr1 + arr2` = `{arr1}` + `{arr2}` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='把大于变成「长度减去 ≤ 的个数」，数值压成名次后用树状数组数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把 `nums` 依次分配到 `arr1`、`arr2`：前两个数各放一个',
                 '之后看两边「严格大于 v」的个数：多的那边得到 `v`；一样多放较短的，再一样放 `arr1`',
                 '返回 `arr1 + arr2`；示例 `[5,14,3,1,2]` → `[5,3,1,2,14]`；本视频：`[5,14,3,1]`'],
        quote='可以先将其转化为当前数组的长度减去数组中小于等于待添加的元素的数量。……本题只需要关注数值的相对大小，于是可以先将数组排序，然后建立数字到序的映射',
        quote_src='—— yiduobo 题解原文',
        idea=['严格大于 `v` 的个数 = ==当前长度 − 小于等于 `v` 的个数==，后者就是前缀和',
              '数值范围很大，不能直接当树状数组下标 → 排序去重，建立 `数字 → 名次` 的映射',
              '`arr1`、`arr2` 各配一棵树状数组：放入元素就在名次位置加 1，查询就是前缀和'],
        summary=['时间 `O(n log n)`，空间 `O(n)`：每个数两次查询 + 一次更新',
                 '易错：树状数组下标从 1 开始，所以名次从 1 起；`rank` 最后比名次总数大 1，正好是数组长度',
                 '比较的是「严格大于」：长度减去「小于等于」，不能漏掉等于的那些',
                 '对比灵神：灵神把两棵树合并成一棵存「差值」，这里是两棵独立的树，更直白'],
    ),
)
