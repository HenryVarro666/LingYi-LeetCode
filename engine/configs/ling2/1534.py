ARR = [3, 0, 1, 1]
A, B_, C = 7, 2, 3
IDX = sorted(range(len(ARR)), key=lambda i: ARR[i])


def _j(S):
    j = S.get('j')
    return j if isinstance(j, int) and S.get('_line', 0) >= 6 else None


def _arr_color(S, i, v):
    j = _j(S)
    if j is None:
        return None
    if i == j:
        return 'orange'
    y = ARR[j]
    if S.get('_line', 0) >= 8 and i < j and abs(ARR[i] - y) <= A:
        return 'blue'
    if S.get('_line', 0) >= 9 and i > j and abs(ARR[i] - y) <= B_:
        return 'pink'
    return None


def _idx_strs(S):
    return [f'{i}:{ARR[i]}' for i in IDX] if 'idx' in S else None


def _idx_pos(S):
    j = _j(S)
    return IDX.index(j) if j is not None else None


def _x_color(S, i, v):
    if S.get('_line') in (13, 14, 15, 16, 17) and v == S.get('x'):
        return 'orange'
    return None


def _right_color(S, i, v):
    if S.get('_line') not in (13, 14, 15, 16, 17) or 'x' not in S:
        return None
    k1, k2 = S.get('k1', 0), S.get('k2', 0)
    if k1 <= i < k2:
        return 'green'
    return None


def _text(S):
    j = _j(S)
    if j is None:
        return f'`a = {A}`，`b = {B_}`，`c = {C}`：枚举中间的 `j`（按 `arr[j]` 从小到大）'
    y = ARR[j]
    if 'x' in S and S.get('_line') in (13, 14, 15, 16, 17):
        x = S['x']
        return f"`x = {x}`：数 right 中在 `[x − c, x + c] = [{x - C}, {x + C}]` 的个数 = `k2 − k1`"
    return f"`j = {j}`，`y = {y}`：left 要 `|arr[i] − y| ≤ a`，right 要 `|arr[k] − y| ≤ b`"


def _cap_for(S, B, ret):
    if 'j' in B and S.get('j') == B.get('j'):
        return '所有 `j` 都枚举完了'
    j = S.j
    _FORX['n'] = 0
    return f'枚举中间的 `j = {j}`（`arr[j] = {ARR[j]}`）：按值从小到大，`left`/`right` 自然有序'


def _cap_left(S, B, ret):
    return f'`i < j` 且 `|arr[i] − {S.y}| ≤ {A}` 的值（按值有序）：`left = {S.left}`'


def _cap_right(S, B, ret):
    if not S.right:
        return f'`k > j` 且 `|arr[k] − {S.y}| ≤ {B_}` 的值：`right = []`，这个 `j` 凑不出三元组'
    return f'`k > j` 且 `|arr[k] − {S.y}| ≤ {B_}` 的值：`right = {S.right}` → 问题变成两个有序数组各选一个数'


_FORX = {'j': None, 'n': 0}


def _cap_forx(S, B, ret):
    """for x in left 没有下标：按步骤顺序数第几次进入（每个 j 在 _cap_for 里清零）"""
    _FORX['n'] += 1
    if _FORX['n'] > len(S.left):
        return 'left 遍历完' if S.left else '`left` 为空，没有可选的 `i`'
    return f'遍历 left 中的 `x = {S.x}`'


def _cap_w2(S, B, ret):
    k2, R, x = B.k2, B.right, B.x
    if k2 < len(R) and R[k2] <= x + C:
        return f'`right[{k2}] = {R[k2]} ≤ x + c = {x + C}` → `k2` 右移'
    if k2 >= len(R):
        return f'`k2 = {k2}` 到头了：right 中 `≤ x + c` 的有 {k2} 个'
    return f'`right[{k2}] = {R[k2]} > x + c = {x + C}` → 停：right 中 `≤ {x + C}` 的有 `k2 = {k2}` 个'


def _cap_w1(S, B, ret):
    k1, R, x = B.k1, B.right, B.x
    if k1 < len(R) and R[k1] < x - C:
        return f'`right[{k1}] = {R[k1]} < x − c = {x - C}` → `k1` 右移'
    if k1 >= len(R):
        return f'`k1 = {k1}` 到头了：right 中 `< x − c` 的有 {k1} 个'
    return f'`right[{k1}] = {R[k1]} ≥ x − c = {x - C}` → 停：right 中 `< {x - C}` 的有 `k1 = {k1}` 个'


CONFIG = dict(
    num=1534, title='统计好三元组', difficulty='Easy', category='普通数组',
    author='灵茶山艾府', technique='排序 + 枚举中间 + 三指针',
    tags=['List.md'],
    code='''
class Solution:
    def countGoodTriplets(self, arr: List[int], a: int, b: int, c: int) -> int:
        idx = sorted(range(len(arr)), key=lambda i: arr[i])

        ans = 0
        for j in idx:
            y = arr[j]
            left = [arr[i] for i in idx if i < j and abs(arr[i] - y) <= a]
            right = [arr[k] for k in idx if k > j and abs(arr[k] - y) <= b]

            k1 = k2 = 0
            for x in left:
                while k2 < len(right) and right[k2] <= x + c:
                    k2 += 1
                while k1 < len(right) and right[k1] < x - c:
                    k1 += 1
                ans += k2 - k1
        return ans
''',
    call=f'Solution().countGoodTriplets({ARR}, {A}, {B_}, {C})',
    expect=4,
    views=[
        dict(type='text', fn=_text, h=56),
        dict(type='array', var='arr', label='arr（橙 = j，蓝 = 进 left 的 i，粉 = 进 right 的 k）', cell=64,
             pointers={_j: 'orange'}, pointer_labels={_j: 'j'}, color=_arr_color),
        dict(type='array', var=_idx_strs, label='idx（下标:值，按值排序）', cell=56,
             color=lambda S, i, v: 'orange' if _idx_pos(S) == i else None),
        dict(type='array', var=lambda S: S.get('left') if _j(S) is not None and S.get('_line', 0) >= 8 else None,
             label='left（橙 = 当前 x）', cell=56, color=_x_color),
        dict(type='array', var=lambda S: S.get('right') if _j(S) is not None and S.get('_line', 0) >= 9 else None,
             label='right（绿 = [k1, k2) 落在 [x−c, x+c] 内）', cell=64,
             pointers={'k1': 'blue', 'k2': 'pink'}, color=_right_color),
    ],
    watch=[('j', 'j', 'orange'), ('y', 'y'), ('x', 'x', 'orange'), ('k1', 'k1', 'blue'), ('k2', 'k2', 'pink'), ('ans', 'ans', 'green')],
    skip=['y = arr[j]', 'k1 = k2 = 0', 'k2 += 1', 'k1 += 1'],
    captions={
        'idx = sorted': '不能直接排序 `arr`（要保持 `i<j<k`）→ ==对下标排序==：`idx = {idx}`',
        'ans = 0': '`ans` 统计好三元组个数',
        'for j in idx': _cap_for,
        'left = [': _cap_left,
        'right = [': _cap_right,
        'for x in left': _cap_forx,
        'while k2 <': _cap_w2,
        'while k1 <': _cap_w1,
        'ans += k2 - k1': '`[{x - c}, {x + c}]` 中有 `k2 − k1 = {k2} − {k1} = {k2 - k1}` 个 → `ans` = =={ans}==',
        'return ans': '好三元组一共 =={ret}== 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='枚举中间 j，左右两个有序数组里数绝对差 ≤ c 的数对',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['统计满足 `i < j < k` 且 `|arr[i]−arr[j]| ≤ a`、`|arr[j]−arr[k]| ≤ b`、`|arr[i]−arr[k]| ≤ c` 的三元组',
                 '示例：`arr = [3,0,1,1,9,7], a = 7, b = 2, c = 3` → `4`',
                 '即 `(3,0,1)`、`(3,0,1)`、`(3,1,1)`、`(0,1,1)`',
                 '本视频去掉用不上的 9、7：`arr = [3,0,1,1]`，答案仍是 `4`'],
        quote='直接排序？不行，题目要求 i<j<k，不能打乱顺序。改成创建一个 [0,n-1] 的下标数组 idx，==对下标数组按照 A_i 的值从小到大排序==。然后遍历 idx 的元素，作为下标 j。（枚举中间）',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['按值顺序收集：`left`（`i<j`，`|A_i−A_j|≤a`）和 `right`（`k>j`，`|A_k−A_j|≤b`）都是==有序==的',
              '对每个 `x ∈ left`：数 `right` 中 `[x−c, x+c]` 内的个数 = `≤ x+c` 的个数 − `< x−c` 的个数',
              '`x` 递增 → `k1`、`k2` 只右移：==三指针=='],
        summary=['时间 `O(n²)`：每个 `j` 收集 `O(n)`，`k1`、`k2` 总共右移 `≤ 2n` 次',
                 '`k2` 停在第一个 `> x+c`，`k1` 停在第一个 `≥ x−c`，答案 `k2 − k1`',
                 '`k1`、`k2` 在每个 `j` 开始时要清零',
                 '方法一暴力 `O(n³)` 足够过本题；方法二值域前缀和 `O(n(n+U))`'],
    ),
)
