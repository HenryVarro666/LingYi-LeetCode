NUMS = [9, 5, 12, 3, 8, 4, 7, 6]
SORTED = sorted(NUMS)
N = len(NUMS)


def _ok(k, mid):
    return SORTED[k] + SORTED[k] <= SORTED[k - mid]


def _status(S, B):
    """当前 mid 下每一对 (k, n-mid+k) 的状态：'ok' / 'bad' / None（未检查）"""
    mid = S.get('mid')
    ln = S.get('_line')
    if not isinstance(mid, int) or ln in (9, 10):
        return {}
    idx = S.get('index')
    st = {}
    if ln in (8, 16, 17, 19, 21):
        if S.get('flag'):
            return {k: 'ok' for k in range(mid)}
        for k in range(mid):
            st[k] = 'ok' if k < idx else ('bad' if k == idx else None)
        return st
    if ln == 11:
        if idx == mid - 1 and S.get('index') == B.get('index') and _ok(idx, mid):
            return {k: 'ok' for k in range(mid)}
        return {k: ('ok' if k < idx else None) for k in range(mid)}
    for k in range(mid):  # 12 / 13 / 14
        if k < idx:
            st[k] = 'ok'
        elif k == idx:
            st[k] = 'ok' if _ok(k, mid) else 'bad'
    return st


def draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '排序后的 nums：最小的 mid 个（蓝）与最大的 mid 个（粉）按顺序配对', 24, T['muted'], bold=True)
    nums = S.get('nums')
    if nums is None:
        return
    sorted_now = nums == SORTED and 'left' in S
    cell = min(100, (x1 - x0 - 60) / N)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * N) / 2
    cy = y0 + 200
    ch = cell * 0.8
    mid = S.get('mid') if sorted_now else None
    st = _status(S, B) if sorted_now else {}
    if isinstance(mid, int):
        for k in range(mid):
            a, b = k, N - mid + k
            c = {'ok': T['green'], 'bad': T['red']}.get(st.get(k), T['dim'])
            X1, X2 = sx + a * cell + cell / 2, sx + b * cell + cell / 2
            lift = 20 + (b - a) * 8 + k * 30
            cv.arc_arrow((X1, cy - 4), (X2, cy - 4), lift, c, 4 if st.get(k) else 2, 12, frac=0.98)
            if st.get(k) == 'bad':
                cv.text(((X1 + X2) / 2, cy - 8 - lift / 2 - 8), f'{SORTED[a]}×2 > {SORTED[b]}', 22, T['red'], anchor='mb', bold=True)
    for k, v in enumerate(nums):
        X = sx + k * cell
        fill = T['panel2']
        if isinstance(mid, int) and mid > 0:
            if k < mid:
                fill = T['blue']
            elif k >= N - mid:
                fill = T['pink']
        cv.rect((X + 4, cy, X + cell - 4, cy + ch), fill=fill, r=8, outline=T['border'])
        cv.text((X + cell / 2, cy + ch / 2), str(v), 30, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        lab = str(k) if not (isinstance(mid, int) and k >= N - mid) else f'{k}（{k - N}）'
        cv.text((X + cell / 2, cy + ch + 6), lab, 18, T['dim'], anchor='mt', mono=True)
    idx = S.get('index')
    if isinstance(mid, int) and isinstance(idx, int) and S.get('_line') in (11, 12, 13, 14) and idx < mid:
        X = sx + idx * cell + cell / 2
        cv.tri_up(X, cy + ch + 34, 10, T['yellow'])
        cv.text((X, cy + ch + 50), 'index', 20, T['yellow'], anchor='mt', bold=True)
        X = sx + (N - mid + idx) * cell + cell / 2
        cv.tri_up(X, cy + ch + 34, 10, T['yellow'])
        cv.text((X, cy + ch + 50), 'index - mid', 20, T['yellow'], anchor='mt', bold=True)


def _cap_if(S, B, ret):
    k, mid = S.index, S.mid
    a, b = S.nums[k], S.nums[k - mid]
    if a + a > b:
        return f'`nums[{k}] + nums[{k}] = {a + a} > nums[{k - mid}] = {b}`：==配不上== → 凑不出 {mid} 组'
    return f'`nums[{k}] + nums[{k}] = {a + a} ≤ nums[{k - mid}] = {b}`：这一对能配'


CONFIG = dict(
    num=2576, title='求出最多标记下标', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='二分答案（配对组数）+ 贪心检查',
    tags=['字节30天'],
    code='''
class Solution(object):
    def maxNumOfMarkedIndices(self, nums):
        n = len(nums)
        nums.sort()

        left = 0
        right = n // 2
        while left < right:
            mid = (left + right + 1) // 2
            flag = True
            for index in range(mid):
                if nums[index] + nums[index] > nums[index - mid]:
                    flag = False
                    break

            if flag:
                left = mid
            else:
                right = mid - 1

        return left + left
''',
    call=f'Solution().maxNumOfMarkedIndices({NUMS})',
    expect=6,
    views=[
        dict(type='custom', draw=draw, h=380),
        dict(type='array', var=lambda S: list(range(N // 2 + 1)) if 'right' in S else None,
             label='二分配对组数 res：答案在 [left, right] 里', cell=80, h=200,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}, window=('left', 'right'),
             dim=lambda S, i, v: not (S['left'] <= i <= S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('flag', 'flag', 'green')],
    skip=['                    break'],
    captions={
        'n = len(nums)': '`n = {n}`',
        'nums.sort()': '从小到大排序：`{nums}`',
        'left = 0': '二分答案（配对组数）：下界 `0`',
        'right = n // 2': '上界 `n // 2 = {right}`：n 个数最多 n/2 组（原文 `/` 为 Python 2 整除，已改为 `//`）',
        'while left < right': lambda S, B, ret: (f'`left = {S.left} < right = {S.right}` → 继续二分' if S.left < S.right
                                                 else f'`left == right = {S.left}`：二分结束'),
        'mid = (left + right + 1)': '`mid = ({left} + {right} + 1) // 2 = {mid}`：检查能否凑出 `{mid}` 组',
        'flag = True': lambda S, B, ret: (f'贪心：最小的 `{S.mid}` 个数配最大的 `{S.mid}` 个数，==按从小到大顺序两两配对=='
                                          if B.left == 0 else f'`flag = True`，检查 `{S.mid}` 对'),
        'for index in range(mid)': lambda S, B, ret: (f'`index = {S.index}`：`nums[{S.index}]` 配 `nums[{S.index - S.mid}]`'
                                                      + ('（负下标 = 倒数第 mid 个起）' if S.index == 0 and S.mid == 2 else '')
                                                      if S.index != B.get('index') or B.get('mid') != S.mid else '这 `{}` 对都能配'.format(S.mid)),
        'if nums[index] + nums[index]': _cap_if,
        'flag = False': '`flag = False`，`break` 不用再检查',
        'if flag:': lambda S, B, ret: (f'能凑出 `{S.mid}` 组 → 答案 `≥ {S.mid}`' if S.flag else f'凑不出 `{S.mid}` 组 → 答案 `< {S.mid}`'),
        'left = mid': '更新下界：`left = {left}`',
        'right = mid - 1': '更新上界：`right = mid - 1 = {right}`',
        'return left + left': '最多 `{left}` 组配对，乘以 2 得到 =={ret}== 个下标',
    },
    cards=dict(
        one_liner='二分配对组数；组数确定后，最小的 mid 个配最大的 mid 个',
        complexity='时间 `O(n log n)`，空间 `O(1)`（忽略排序栈开销）',
        problem=['每次选两个==未标记==的下标 `i`、`j`，满足 `2 * nums[i] <= nums[j]`，标记它们',
                 '求最多可以标记多少个下标',
                 '示例：`[9,2,5,4]` → `4`；本视频 `[9,5,12,3,8,4,7,6]` → `6`'],
        before=[dict(heading='直接贪心为什么难', lines=[
            '最小的数一定会当 `nums[i]`，但它该配谁？',
            '配==尽量小==的：`[1,2,3,4]` 里 1 配 2，剩下 3、4 配不上（最优是 1-3、2-4）',
            '配==尽量大==的：后面更大的 `nums[i]` 需要更大的 `nums[j]`，也不优',
        ])],
        quote='题目中的最大配对数显然是符合二分的条件的，因此在这里可以考虑==二分答案res==……在明确了配对的组数后，就可以使用贪心法了。',
        quote_src='—— yiduobo 题解',
        idea=['二分组数 `mid`：能凑 mid 组，就一定能凑更少的组',
              '检查：最小的 mid 个数作 `nums[i]`，最大的 mid 个数作 `nums[j]`，按顺序配',
              '`nums[index]` 配 `nums[index - mid]`：负下标正好从倒数第 mid 个开始'],
        result='运行结束：最多 3 组配对，返回 `6` ✓',
        summary=['时间 `O(n log n)`：排序 + 二分 `O(log n)` 次、每次检查 `O(n)`',
                 '`mid = (left + right + 1) // 2` 向上取整，配合 `left = mid` 才不会死循环',
                 '原文为 Python 2 写法：两处 `/` 整除改为 `//`，并删去 docstring',
                 '对比灵神：灵神进一步把检查变成同向双指针，一趟扫描 `O(n)`'],
    ),
)
