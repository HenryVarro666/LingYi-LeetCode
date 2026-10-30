def _make_draw(rows, cmp_fn):
    """rows: [(label, var, ptr_var or None, color_name)]"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        rh = (y1 - y0 - 60) / len(rows)
        for r, (lab, var, ptr, cname) in enumerate(rows):
            data = S.get(var)
            top = y0 + 10 + r * rh
            cv.text((x0 + 18, top), lab, 24, T['muted'], bold=True)
            if data is None:
                continue
            cw = min(110, (x1 - x0 - 60) / max(1, len(data)))
            for k, (t, v) in enumerate(data):
                X = x0 + 30 + k * cw
                cur = ptr is not None and S.get(ptr) == k
                fill = (36, 43, 54)
                cv.rect((X + 3, top + 36, X + cw - 3, top + 36 + 56), fill=fill, outline=T[cname] if cur else None, width=4, r=8)
                cv.text((X + cw / 2, top + 36 + 14), str(t), 24, T[cname] if cur else T['text'], anchor='mm', bold=True)
                cv.text((X + cw / 2, top + 36 + 40), str(v), 22, T['muted'], anchor='mm')
            if ptr is not None and ptr in S and 0 <= S[ptr] < len(data):
                X = x0 + 30 + S[ptr] * cw + cw / 2
                cv.tri_up(X, top + 100, 9, T[cname])
                cv.text((X, top + 112), ptr, 20, T[cname], anchor='mt', bold=True)
            elif ptr is not None and ptr in S:
                cv.text((x0 + 30 + len(data) * cw + 6, top + 56), f'{ptr} = {S[ptr]}（已越界）', 20, T[cname], anchor='lm')
    return draw


def _cmp(S):
    if 'i' not in S or 'j' not in S or S['i'] >= S['n'] or S['j'] >= S['m']:
        return ''
    return f"比较 id：`a[{S['i']}][0] = {S['a'][S['i']][0]}` 与 `b[{S['j']}][0] = {S['b'][S['j']][0]}`"


CONFIG = dict(
    num=2570, title='合并两个二维数组 - 求和法', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='归并 · 双指针',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def mergeArrays(self, a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
        ans = []
        i, n = 0, len(a)
        j, m = 0, len(b)
        while True:
            if i == n:
                ans.extend(b[j:])
                return ans
            if j == m:
                ans.extend(a[i:])
                return ans
            if a[i][0] < b[j][0]:
                ans.append(a[i])
                i += 1
            elif a[i][0] > b[j][0]:
                ans.append(b[j])
                j += 1
            else:
                a[i][1] += b[j][1]
                ans.append(a[i])
                i += 1
                j += 1
''',
    call='Solution().mergeArrays([[1,2],[2,3],[4,5]], [[1,4],[3,2],[4,1]])',
    expect=[[1, 6], [2, 3], [3, 2], [4, 6]],
    views=[
        dict(type='custom', draw=_make_draw([('a  （上：id，下：值）', 'a', 'i', 'blue'), ('b', 'b', 'j', 'pink'), ('ans', 'ans', None, 'green')], None), h=420),
        dict(type='text', fn=_cmp),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'ans = []': '和归并排序的合并一样，`ans` 按 id 从小到大收集（格子里写 `id:值`）',
        'i, n = 0': '`i` 指向 `a` 的当前 id，`n = {n}`',
        'j, m = 0': '`j` 指向 `b` 的当前 id，`m = {m}`',
        'while True': '一直合并，直到某个数组用完再返回',
        'if i == n': lambda S, B, r: ('`a` 用完了' if S.i == S.n else '`a` 还有元素'),
        'ans.extend(b[j:])': '`a` 已用完，`b` 剩下的 id 都比已处理的大 → 整段接到答案后面',
        'if j == m': lambda S, B, r: ('`b` 用完了' if S.j == S.m else '`b` 还有元素'),
        'ans.extend(a[i:])': '`b` 已用完，`a` 剩下的整段接到答案后面',
        'if a[i][0] <': lambda S, B, r: (f'id `{S.a[S.i][0]} < {S.b[S.j][0]}`：`a` 的 id 更小 → 它在 b 中没有对应项，直接收下'
                                         if S.a[S.i][0] < S.b[S.j][0] else f'id `{S.a[S.i][0]}` 不小于 `{S.b[S.j][0]}`'),
        'ans.append(a[i])': lambda S, B, r: f'`a[{S.i}] = {S.a[S.i]}` 加入答案',
        'i += 1': '`i` → {i}',
        'elif a[i][0] >': lambda S, B, r: (f'id `{S.a[S.i][0]} > {S.b[S.j][0]}`：`b` 的 id 更小 → 它在 a 中没有对应项，直接收下'
                                           if S.a[S.i][0] > S.b[S.j][0] else f'id 相等 `{S.a[S.i][0]}`：两边都有'),
        'ans.append(b[j])': '`b[{j}] = {b[j]}` 加入答案',
        'j += 1': '`j` → {j}',
        'a[i][1] += b[j][1]': 'id 相同：把 `b` 的值加到 `a` 上 → `{a[i]}`（值求和）',
    },
    cards=dict(
        one_liner='做法和归并排序一样：id 小的先走，id 相同就把值相加',
        complexity='时间 `O(n+m)`，空间 `O(1)`（不计返回值）',
        problem=['两个按 id 递增的数组，每项 `[id, val]`，合并成按 id 递增、相同 id 值求和的数组',
                 '示例：`[[1,2],[2,3],[4,5]]` + `[[1,4],[3,2],[4,1]]` → `[[1,6],[2,3],[3,2],[4,6]]`',
                 '本视频用的就是这组示例'],
        quote='做法和归并排序是一样的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i`、`j` 分别指向 `a`、`b` 当前 id；id 小的先放进 `ans`',
              'id 相同：把 `b[j]` 的值加到 `a[i]` 上再放入答案，两个下标一起右移',
              '一个数组用完后，另一个数组剩下的用 `extend` 直接接上'],
        summary=['时间 `O(n+m)`，空间 `O(1)`（不计返回值）',
                 '先判断 `i == n`、`j == m` 再比较，避免下标越界',
                 '注意代码直接修改了输入 `a[i][1]`，没有新建列表',
                 '同类题：21 合并两个有序链表、88 合并两个有序数组'],
    ),
)
