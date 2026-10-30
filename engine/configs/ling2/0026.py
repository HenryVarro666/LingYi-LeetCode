NUMS = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]


def _color(S, i, v):
    if 'k' not in S:
        return None
    if i < S['k']:
        return 'green'
    return None


def _dim(S, i, v):
    return 'i' in S and 'k' in S and S['k'] <= i < S['i']


def _table(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '跟着灵神过一遍示例 2：', 24, T['muted'], bold=True)
    cols = [('i', 70), ('a[i]', 90), ('与 a[i-1]', 140), ('去重后', 330)]
    rh = min(36, (y1 - y0 - 44) / 10)
    X = x0 + 30
    y = y0 + 38
    xs = []
    for name, w in cols:
        xs.append((X, w))
        cv.text((X + w / 2, y + rh / 2), name, 21, T['muted'], anchor='mm', bold=True)
        X += w
    cv.line([(x0 + 30, y + rh), (X, y + rh)], T['border'], 2)
    if 'i' not in S:
        return
    cur = S['i']
    done = 'i' in B and B['i'] == cur and S['_line'] == 4
    for r in range(1, len(NUMS)):
        if r > cur:
            break
        yy = y + rh * r
        live = r == cur and not done
        if live:
            cv.rect((x0 + 26, yy + 2, X + 4, yy + rh - 2), fill=T['panel2'], outline=T['blue'], width=2, r=6)
        eq = NUMS[r] == NUMS[r - 1]
        known = not (live and S['_line'] == 4)
        vals = [str(r), str(NUMS[r]), ('=' if eq else '≠') if known else '?',
                str(sorted(set(NUMS[:r + 1]))) if known else '']
        for (cx, w), v, c in zip(xs, vals, [T['dim'], T['text'], T['muted'] if eq else T['green'], T['text']]):
            if c is T['green'] and not known:
                c = T['muted']
            cv.text((cx + w / 2, yy + rh / 2), v, 22, c, anchor='mm', mono=True, bold=v in ('≠',))


def _for(S, B, ret):
    if 'i' in B and B.i == S.i:
        return f'遍历结束：前 `k = {S.k}` 个位置就是去重后的数组'
    i = S.i
    return f'`i = {i}`：比较 `nums[{i}]` 和它左边的 `nums[{i - 1}]`'


def _if(S, B, ret):
    i, a = S.i, S.nums
    if a[i] != a[i - 1]:
        return f'`nums[{i}] = {a[i]}` ≠ `nums[{i - 1}] = {a[i - 1]}` → ==不是重复项==，保留'
    return f'`nums[{i}] = {a[i]}` = `nums[{i - 1}]` → 是重复项，==不保留==，看下一个'


CONFIG = dict(
    num=26, title='删除有序数组中的重复项', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='同向双指针 · 原地修改',
    tags=['热题173', '面试经典150'],
    code='''
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:  # nums[i] 不是重复项
                nums[k] = nums[i]  # 保留 nums[i]
                k += 1
        return k
''',
    call=f'''nums = {NUMS}
k = Solution().removeDuplicates(nums)
k, nums[:k]''',
    expect=(5, [0, 1, 2, 3, 4]),
    views=[
        dict(type='text', fn=lambda S: (f"去重后：`{S['nums'][:S['k']]}`（长度 `k = {S['k']}`）" if 'k' in S else
                                        '`nums[i] != nums[i-1]` 就保留，填到 `nums[k]`'), size=30),
        dict(type='array', var='nums', pointers={'k': 'pink', 'i': 'blue'}, color=_color, dim=_dim, h=200, cell=90,
             label='nums（绿 = 已保留的唯一元素，暗 = 跳过的重复项）'),
        dict(type='custom', draw=_table, h=400),
    ],
    watch=[('i', 'i', 'blue'), ('k', 'k', 'pink'), ('nums[i]', 'nums[i]'), ('nums[i-1]', 'nums[i - 1]')],
    captions={
        'k = 1': '`nums[0]` 肯定要保留；`k = 1` 表示==保留的元素要填入的下标==',
        'for i in range': _for,
        'if nums[i] != nums[i - 1]': _if,
        'nums[k] = nums[i]': '把 `{nums[i]}` 填入 `nums[{k}]`：`k ≤ i`，==覆盖的位置已经看过了==，不会丢数据',
        'k += 1': '保留了一个元素，`k` → {k}',
        'return k': '返回唯一元素的个数 `k = {ret}`',
    },
    cards=dict(
        one_liner='和左边的数不同就保留，依次填到 nums[k]',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 非严格递增，==原地==删除重复元素，使每个元素只出现一次',
                 '返回唯一元素个数 `k`，`nums` 前 `k` 个就是去重结果',
                 '示例 2：`[0,0,1,1,1,2,2,3,3,4]` → `5`，`nums = [0,1,2,3,4,…]`'],
        quote='如果 nums[i]=nums[i−1]，那么 nums[i] 是重复项，不保留。如果 nums[i]≠nums[i−1]，那么 nums[i] 不是重复项，==保留，填入 nums[k] 中，然后把 k 加一==。',
        quote_src='—— 灵茶山艾府题解（跟着我过一遍示例 2）',
        idea=['首先 `nums[0]` 肯定要保留，所以 `k` 从 1 开始',
              '有序数组里重复项是挨着的：只需==和左边的数比较==',
              '`k` 是写指针，`i` 是读指针，`k ≤ i` 永远成立'],
        result='`k = 5`，`nums` 前 5 个是 `[0,1,2,3,4]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`nums[i-1]` 不会被改坏：写入位置 `k ≤ i`，写到 `i-1` 时只能是自己写自己',
                 '`k` 从 1 开始：题目保证 `n ≥ 1`，第一个数一定保留',
                 '另有 `pairwise` 写法；库函数 `sorted(set(nums))` 需要额外空间',
                 '同类：80 题（最多保留两个）、27 题移除元素'],
    ),
)
