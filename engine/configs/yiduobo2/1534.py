ARR = [2, 1, 2, 4]
A, B_, C = 1, 2, 3
VMAX = 6  # 数轴画到的最大值


def _pre(tree, i):
    """树状数组前缀和：值 ≤ i-1 的个数（只读，不改状态）"""
    s = 0
    while i > 0:
        s += tree[i]
        i -= i & -i
    return s


def _counts(S):
    t = S.get('suffix_array')
    if not isinstance(t, list) or len(t) != 1002:
        return None
    cnt = [_pre(t, v + 1) - _pre(t, v) for v in range(VMAX + 1)]
    # 调用 add 的这一步，画面停在刚进入 add 时（还没改）：直接画出 add 之后的结果，和字幕对齐
    if S.get('_line') == 6 and isinstance(S.get('num'), int):
        cnt[S['num']] += 1
    if S.get('_line') == 11 and isinstance(S.get('j'), int):
        cnt[ARR[S['j']]] -= 1
    return cnt


def _range(S):
    """当前 arr[k] 的取值范围（值域，闭区间）"""
    ln = S.get('_line', 0)
    if ln in (17, 18, 19, 21) and isinstance(S.get('l'), int):
        return S['l'] - 1, S['r'] - 1, 'yellow'
    if ln == 15 and 'l2' in S:
        return S['l2'] - 1, S['r2'] - 1, 'pink'
    if ln == 14 and 'l1' in S:
        return S['l1'] - 1, S['r1'] - 1, 'cyan'
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '树状数组里的数（每个点 = 一个 arr[k]，k > j）', 24, T['muted'], bold=True)
    cnt = _counts(S)
    if cnt is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    n = VMAX + 1
    cell = min(110, (x1 - x0 - 80) / n)
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    base = y1 - 50
    rg = _range(S)
    if rg:
        lo, hi, c = rg
        a, b = max(lo, 0), min(hi, VMAX)
        if a <= b:
            col = T[c]
            cv.rect((sx + a * cell + 4, y0 + 44, sx + (b + 1) * cell - 4, base + 4), fill=col, alpha=40, r=10)
            cv.rect((sx + a * cell + 4, y0 + 44, sx + (b + 1) * cell - 4, base + 4), outline=col, width=3, r=10)
            name = {'cyan': '由 |arr[j] − arr[k]| ≤ b', 'pink': '由 |arr[i] − arr[k]| ≤ c', 'yellow': '两个范围的交集'}[c]
            cv.text((sx + a * cell + 16, y0 + 56), f'{name}：[{lo}, {hi}]', 22, col, bold=True)
    for v in range(n):
        X = sx + v * cell + cell / 2
        for k in range(cnt[v]):
            cy = base - 30 - k * 46
            cv.d.ellipse((X - 19, cy - 19, X + 19, cy + 19), fill=T['purple'])
            cv.text((X, cy), v, 22, T['bg'], anchor='mm', bold=True)
        cv.text((X, base + 12), v, 22, T['text'], anchor='mt', mono=True)
    cv.line([(sx, base), (sx + n * cell, base)], T['border'], 2)


def _arr_color(S, i, v):
    j = S.get('j')
    if not isinstance(j, int) or S.get('_line', 0) < 11:
        return None
    if i == j:
        return 'orange'
    if isinstance(S.get('i'), int) and i == S['i'] and S.get('_line', 0) >= 13:
        return 'blue'
    if i > j:
        return 'purple'
    return None


def _ptr_i(S):
    return S.get('i') if S.get('_line', 0) >= 13 and isinstance(S.get('i'), int) else None


def _text(S):
    ln = S.get('_line', 0)
    if ln in (17, 18, 19, 21) and isinstance(S.get('l'), int):
        return f"`arr[k]` 要落在 `[{S['l'] - 1}, {S['r'] - 1}]`：数一数树状数组里有几个"
    if ln >= 13 and isinstance(S.get('i'), int):
        return f"`j = {S['j']}`，`i = {S['i']}`：由 `arr[i]`、`arr[j]` 推出 `arr[k]` 的范围"
    return '树状数组下标 = 值 + 1（从 1 开始）；`sum(x)` = 值 `≤ x−1` 的个数'


def _cap_if_a(S, B, ret):
    i, j = S.i, S.j
    d = abs(ARR[i] - ARR[j])
    if d <= A:
        return f'`|arr[{i}] − arr[{j}]| = |{ARR[i]} − {ARR[j]}| = {d} ≤ a = {A}` → 枚举到一个合法的 `i`'
    return f'`|{ARR[i]} − {ARR[j]}| = {d} > a` → 跳过'


def _cap_l1(S, B, ret):
    y = ARR[S.j]
    return (f'由 `|arr[j] − arr[k]| ≤ b`：`{y - B_} ≤ arr[k] ≤ {y + B_}`'
            f'（截到 `[0, 1000]` 再 +1）→ 下标 `[{S.l1}, {S.r1}]`')


def _cap_l2(S, B, ret):
    x = ARR[S.i]
    return (f'由 `|arr[i] − arr[k]| ≤ c`：`{x - C} ≤ arr[k] ≤ {x + C}` → 下标 `[{S.l2}, {S.r2}]`')


def _cap_sum_r(S, B, ret):
    t, l, r = S.suffix_array, S.l, S.r
    hi, lo = _pre(t, r), _pre(t, l - 1)
    return (f'`sum({r}) − sum({l - 1})` = 值在 `[{l - 1}, {r - 1}]` 的个数 = `{hi} − {lo}` = =={hi - lo}==：'
            f'先加 `sum({r}) = {hi}`')


def _cap_sum_l(S, B, ret):
    t, l = S.suffix_array, S.l
    lo = _pre(t, l - 1)
    return f'再减 `sum({l - 1}) = {lo}`：`res` = `{B.res} − {lo}` = =={B.res - lo}=='


CONFIG = dict(
    num=1534, title='统计好三元组', difficulty='Easy', category='普通数组',
    author='yiduobo', technique='枚举 j、i 推出 arr[k] 的范围 + 树状数组计数',
    tags=['List.md'],
    code='''
class Solution(object):
    def countGoodTriplets(self, arr, a, b, c):
        suffix_array = [0] * 1002

        for num in arr:
            self.add(num + 1, 1001, suffix_array, 1)

        n = len(arr)
        res = 0
        for j in range(n):
            self.add(arr[j] + 1, 1001, suffix_array, -1)
            for i in range(j):
                if abs(arr[i] - arr[j]) <= a:
                    l1, r1 = max(arr[j] - b, 0) + 1, min(arr[j] + b, 1000) + 1
                    l2, r2 = max(arr[i] - c, 0) + 1, min(arr[i] + c, 1000) + 1

                    l, r = max(l1, l2), min(r1, r2)
                    if l <= r:
                        res += self.sum(r, suffix_array)
                        if l > 0:
                            res -= self.sum(l - 1, suffix_array)

        return res

    def add(self, now, max_n, suffix_array, delta):
        while now <= max_n:
            suffix_array[now] += delta
            now += now & -now

    def sum(self, now, suffix_array):
        res = 0
        while now:
            res += suffix_array[now]
            now -= now & -now

        return res
''',
    call=f'Solution().countGoodTriplets({ARR}, {A}, {B_}, {C})',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='arr', label='arr（橙 = j，蓝 = i，紫 = 还在树状数组里的 k > j）', cell=72,
             pointers={'j': 'orange', _ptr_i: 'blue'}, pointer_labels={_ptr_i: 'i'}, color=_arr_color),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('j', 'j', 'orange'), ('i', _ptr_i, 'blue'), ('[l, r]', lambda S: f"[{S['l']}, {S['r']}]" if S.get('_line', 0) in (17, 18, 19, 21) else None, 'yellow'),
           ('res', lambda S: S['_inner'].get('res', S.get('res')) if S.get('_line') != 19 and S.get('_line') != 21 else S.get('res'), 'green')],
    skip=['for num in arr', 'suffix_array = [0] * 1002', 'n = len(arr)', 'res = 0', 'for j in range(n)', 'for i in range(j)', 'if l > 0',
          26, 27, 28, 32, 33, 34, 36],
    captions={
        'self.add(num + 1, 1001, suffix_array, 1)': '先把所有数放进树状数组：`add({num} + 1, +1)`（下标 = 值 + 1）',
        'self.add(arr[j] + 1, 1001, suffix_array, -1)': '枚举中间的 `j = {j}`：把 `arr[{j}] = {arr[j]}` 删掉 → 树状数组里只剩 ==`arr[j+1:]`==',
        'if abs(arr[i] - arr[j]) <= a': _cap_if_a,
        'l1, r1 = ': _cap_l1,
        'l2, r2 = ': _cap_l2,
        'l, r = max(l1, l2)': '两个范围取交集：下标 `[l, r] = [{l}, {r}]`，即 `arr[k]` 的值在 `[{l - 1}, {r - 1}]`',
        'if l <= r': lambda S, B, ret: ('交集非空 → 去树状数组里数' if B.l <= B.r else '交集为空 → 没有合法的 k'),
        'res += self.sum(r, suffix_array)': _cap_sum_r,
        'res -= self.sum(l - 1, suffix_array)': _cap_sum_l,
        'return res': '好三元组一共 =={ret}== 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='枚举 j 和 i，推出 arr[k] 的取值范围，用树状数组数后缀里有几个',
        complexity='时间 `O(n² log U)`，空间 `O(U)`（`U = 1000`）',
        problem=['统计满足 `i < j < k` 且 `|arr[i]−arr[j]| ≤ a`、`|arr[j]−arr[k]| ≤ b`、`|arr[i]−arr[k]| ≤ c` 的三元组',
                 '示例：`arr = [3,0,1,1,9,7], a = 7, b = 2, c = 3` → `4`',
                 '本视频：`arr = [2,1,2,4], a = 1, b = 2, c = 3` → `3`',
                 '即 `(2,1,2)`、`(2,2,4)`、`(1,2,4)`'],
        quote='需要先枚举arr[j]，然后从0到j - 1之间枚举符合条件的arr[i]。接下来根据arr[i]与arr[k]的不等式以及arr[j]与arr[k]的不等式，==可以求出arr[k]的取值范围==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`|arr[j] − arr[k]| ≤ b` → `arr[j] − b ≤ arr[k] ≤ arr[j] + b`；同理 `arr[i] ± c`，取交集 `[l, r]`',
              '问题变成：`arr[j+1:]` 中值在 `[l, r]` 的数有几个 → ==动态区间和==',
              '树状数组按值计数：枚举 `j` 时把 `arr[j]` 删掉，里面恰好是 `arr[j+1:]`'],
        summary=['时间 `O(n² log U)`，空间 `O(U)`；`U = 1000` 是值域',
                 '树状数组下标从 1 开始：值 `v` 存在下标 `v + 1`，所以范围都 `+ 1`',
                 '区间计数 = `sum(r) − sum(l − 1)`；`l ≥ 1` 恒成立，`if l > 0` 只是保险',
                 '对比灵神：灵神方法二用值域前缀和，方法三排序 + 三指针做到 `O(n²)`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
