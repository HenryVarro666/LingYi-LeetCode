NUMS = [1, 4, 5, 2, 6, 7]


def _first_drop(nums):
    """模拟原算法，返回 (第一次非递增的位置 index, 被删的下标)"""
    last = nums[0]
    for i in range(1, len(nums)):
        if nums[i] <= last:
            if i > 1 and nums[i - 2] >= nums[i]:
                return i, i
            return i, i - 1
        last = nums[i]
    return None, None


def _deleted(S):
    if S.get('cnt', 0) < 1 or 'index' not in S:
        return None
    i0, d = _first_drop(S['nums'])
    if i0 is None:
        return None
    if S['index'] > i0 or (S['index'] == i0 and S.get('_line') in (12, 14)):
        return d
    return None


def _color(S, i, v):
    d = _deleted(S)
    if d == i:
        return 'red'
    idx = S.get('index')
    if idx is None:
        return None
    if S.get('_line') == 11 and idx > 1 and i in (idx - 2, idx):
        return 'purple'
    if i == idx:
        return None
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'nums（红 = 被删掉的，紫 = 正在比较 nums[index-2] 与 nums[index]，虚线 = last）', 22, T['muted'], bold=True)
    nums = S['nums']
    n = len(nums)
    cell = min(110, (x1 - x0 - 200) / n)
    sx = x0 + 100 + ((x1 - x0 - 200) - cell * n) / 2
    base, top = y1 - 90, y0 + 80
    scale = (base - top) / max(nums)
    idx = S.get('index')
    for i, v in enumerate(nums):
        X = sx + i * cell
        bw = cell * 0.62
        c = _color(S, i, v)
        fill = T[c] if c else (110, 120, 132)
        if c is None and idx is not None and i == idx:
            fill = T['blue']
        if c is None and idx is not None and i > idx:
            fill = (52, 58, 68)
        cv.rect((X + (cell - bw) / 2, base - v * scale, X + (cell + bw) / 2, base), fill=fill, r=5)
        cv.text((X + cell / 2, base - v * scale - 6), v, 26, T['text'], anchor='mb', bold=True)
        cv.text((X + cell / 2, base + 6), i, 18, T['dim'], anchor='mt', mono=True)
        if c == 'red':
            cv.text((X + cell / 2, base - v * scale / 2), '删', 24, T['bg'], anchor='mm', bold=True)
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    if 'last' in S:
        y = base - S['last'] * scale
        cv.dashed((sx - 10, y), (sx + n * cell + 10, y), T['orange'], 3)
        cv.text((sx + n * cell + 16, y), f"last={S['last']}", 22, T['orange'], anchor='lm', bold=True)
    if idx is not None:
        X = sx + idx * cell + cell / 2
        cv.tri_up(X, base + 36, 10, T['blue'])
        cv.text((X, base + 50), 'index', 22, T['blue'], anchor='mt', bold=True)


def _formula(S):
    if 'last' not in S:
        return '`last`：保留下来的序列的最后一个数，`cnt`：非递增出现的次数'
    d = _deleted(S)
    tail = f'，删掉了下标 `{d}`（值 {S["nums"][d]}）' if d is not None else ''
    return f'`last = {S["last"]}`，`cnt = {S["cnt"]}`{tail}'


def _if_le(S, B, ret):
    v, last = S.nums[S.index], S.last
    if v <= last:
        return f'`nums[{S.index}] = {v}` ≤ `last = {last}`：==出现非递增==，必须删掉一个'
    return f'`nums[{S.index}] = {v}` > `last = {last}`：仍然严格递增'


def _if_special(S, B, ret):
    i = S.index
    if i > 1 and S.nums[i - 2] >= S.nums[i]:
        return (f'`nums[{i - 2}] = {S.nums[i - 2]}` ≥ `nums[{i}] = {S.nums[i]}`：删掉 `nums[{i - 1}]` 后 '
                f'`{S.nums[i - 2]}, {S.nums[i]}` 又会非递增 → ==只能删 nums[{i}]==')
    if i > 1:
        return f'`nums[{i - 2}] = {S.nums[i - 2]}` < `nums[{i}] = {S.nums[i]}` → 贪心：删掉较大的 `nums[{i - 1}]`'
    return '`index = 1`：前面只有一个数 → 删掉 `nums[0]`'


CONFIG = dict(
    num=1909, title='删除一个元素使数组严格递增', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='一次遍历 · 贪心决定删哪个',
    tags=['字节30天'],
    code='''
class Solution(object):
    def canBeIncreasing(self, nums):
        n = len(nums)
        cnt = 0
        last = nums[0]
        for index in range(1, n):
            if nums[index] <= last:
                cnt += 1
                if cnt == 2:
                    return False
                if index > 1 and nums[index - 2] >= nums[index]:
                    last = nums[index - 1]
                else:
                    last = nums[index]
            else:
                last = nums[index]

        return True
''',
    call=f'Solution().canBeIncreasing({NUMS})',
    expect=True,
    skip=['n = len'],
    views=[
        dict(type='text', fn=_formula),
        dict(type='custom', draw=_draw, h=500),
    ],
    watch=[('index', 'index', 'blue'), ('last', 'last', 'orange'), ('cnt', 'cnt', 'red')],
    captions={
        'cnt = 0': '`cnt` 记录出现非递增的次数：==最多只能删一次==',
        'last = nums[0]': '`last` 是保留序列的末尾，初始为 `nums[0] = {last}`',
        'for index in range': lambda S, B, ret: (f'看 `nums[{S.index}] = {S.nums[S.index]}`' if B.get('index') != S.get('index') or 'index' not in B
                                                 else '遍历结束'),
        'if nums[index] <= last': _if_le,
        'cnt += 1': '用掉唯一一次删除机会：`cnt = {cnt}`',
        'if cnt == 2': lambda S, B, ret: ('`cnt == 2`：第二次非递增 → 删一个不够' if S.cnt == 2 else '`cnt = 1`，还有救'),
        'return False': '返回 `False`',
        'if index > 1 and': _if_special,
        12: '删掉 `nums[{index}]`：保留序列末尾仍是 `last = nums[{index - 1}] = {last}`',
        14: '删掉 `nums[{index - 1}]`：`last = nums[{index}] = {last}`，末尾更小，==更容易接上后面的数==',
        16: '接在后面：`last = {last}`',
        'return True': '走完遍历，最多只删了一个 → `True`',
    },
    cards=dict(
        one_liner='第一次出现非递增时决定删哪个：默认删前一个，除非会造成新的非递增',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['==恰好删除一个==元素后数组能否==严格递增==？本身严格递增也返回 `true`',
                 '示例：`[1,2,10,5,7]` → `true`（删 10）',
                 '示例：`[2,3,1,2]` → `false`',
                 '本视频：`[1,4,5,2,6,7]` → `true`（删 2）'],
        quote='从贪心的角度来说，为了继续适配后面的数字，这里显然就应该删去nums[index]……如果删去nums[index]将导致新的非递增出现，此时就必须删去nums[index + 1]。',
        quote_src='—— yiduobo 知乎题解（原文的 index 对应代码里的 index-1）',
        idea=['第一次非递增：`nums[i-1] ≥ nums[i]`，两者必删其一',
              '贪心：删==较大==的 `nums[i-1]`，末尾更小，对后面更友好',
              '例外：`nums[i-2] ≥ nums[i]` 时删 `nums[i-1]` 会造成新的非递增 → 只能删 `nums[i]`'],
        summary=['时间 `O(n)`，空间 `O(1)`：只维护 `last` 和 `cnt`',
                 '易错：删 `nums[i]` 时 `last` 保持 `nums[i-1]`，删 `nums[i-1]` 时 `last = nums[i]`',
                 '`cnt == 2` 立刻返回 `False`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '灵神题解：遇到非递增，两个元素各尝试删除检查一遍'],
    ),
)
