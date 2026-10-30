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
    if 'p1' not in S or 'p2' not in S or S['p1'] >= len(S['nums1']) or S['p2'] >= len(S['nums2']):
        return ''
    return f"比较 id：`nums1[{S['p1']}][0] = {S['nums1'][S['p1']][0]}` 与 `nums2[{S['p2']}][0] = {S['nums2'][S['p2']][0]}`"


CONFIG = dict(
    num=2570, title='合并两个二维数组 - 求和法', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='二路归并 · 拷贝后累加',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def mergeArrays(self, nums1, nums2):

        p1 = p2 = 0
        res = []
        while p1 < len(nums1) or p2 < len(nums2):
            if p1 == len(nums1):
                res.append(nums2[p2][:])
                p2 += 1
            elif p2 == len(nums2):
                res.append(nums1[p1][:])
                p1 += 1
            elif nums1[p1][0] < nums2[p2][0]:
                res.append(nums1[p1][:])
                p1 += 1
            elif nums1[p1][0] > nums2[p2][0]:
                res.append(nums2[p2][:])
                p2 += 1
            else:
                res.append(nums1[p1][:])
                res[-1][1] += nums2[p2][1]
                p1 += 1
                p2 += 1
        
        return res
''',
    call='Solution().mergeArrays([[1,2],[2,3],[4,5]], [[1,4],[3,2],[4,1]])',
    expect=[[1, 6], [2, 3], [3, 2], [4, 6]],
    views=[
        dict(type='custom', draw=_make_draw([('nums1  （上：id，下：值）', 'nums1', 'p1', 'blue'), ('nums2', 'nums2', 'p2', 'pink'), ('res', 'res', None, 'green')], None), h=420),
        dict(type='text', fn=_cmp),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink')],
    max_steps=80,
    captions={
        'p1 = p2 = 0': '两个指针从各自数组头部出发（格子里写 `id:值`）',
        'res = []': '`res` 保存合并结果',
        'while p1 <': lambda S, B, r: ('至少有一个数组还没处理完，继续' if S.p1 < len(S.nums1) or S.p2 < len(S.nums2) else '两个数组都处理完了'),
        'if p1 == len': lambda S, B, r: ('`nums1` 走完了，只剩 `nums2`' if S.p1 == len(S.nums1) else '`nums1` 还有元素'),
        'elif p2 == len': lambda S, B, r: ('`nums2` 走完了，只剩 `nums1`' if S.p2 == len(S.nums2) else '`nums2` 还有元素，两边都存在'),
        'elif nums1[p1][0] <': lambda S, B, r: (f'id `{S.nums1[S.p1][0]} < {S.nums2[S.p2][0]}`：nums1 的 id 较小 → 先放它' if S.nums1[S.p1][0] < S.nums2[S.p2][0] else f'id `{S.nums1[S.p1][0]}` 不小于 `{S.nums2[S.p2][0]}`'),
        'elif nums1[p1][0] >': lambda S, B, r: (f'id `{S.nums1[S.p1][0]} > {S.nums2[S.p2][0]}`：nums2 的 id 较小 → 先放它' if S.nums1[S.p1][0] > S.nums2[S.p2][0] else f'id 相同 `{S.nums1[S.p1][0]}`：需要把两边的值相加'),
        'res.append(nums2[p2][:])': '拷贝 `nums2[{p2}]` 放入答案：`res = {res}`',
        'res.append(nums1[p1][:])': '拷贝 `nums1[{p1}]` 放入答案：`res = {res}`（`[:]` 拷贝，避免改到原数组）',
        'res[-1][1] +=': 'id 相同：把 `nums2` 的值累加到刚放入的项上 → `{res[-1]}`',
        'p1 += 1': '`p1` → {p1}',
        'p2 += 1': '`p2` → {p2}',
        'return res': '合并完成：`{ret}`',
    },
    cards=dict(
        one_liner='二路归并：id 小的先放，id 相同要特别处理',
        complexity='时间 `O(n+m)`，空间 `O(1)`（不计返回值）',
        problem=['两个按 id 递增的数组，合并时相同 id 的值求和',
                 '示例：`[[2,4],[3,6],[5,5]]` + `[[1,3],[4,3]]` → `[[1,3],[2,4],[3,6],[4,3],[5,5]]`',
                 '本视频：`[[1,2],[2,3],[4,5]]` + `[[1,4],[3,2],[4,1]]` → `[[1,6],[2,3],[3,2],[4,6]]`'],
        quote='使用两个指针从数组头部开始向后走，使用类似二路归并的做法，每次将id较小那一侧指针对应的值添加到答案数组中，并将对应的指针向后移动即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p1`、`p2` 分别扫两个数组，哪边 id 小就把那一项放入 `res`',
              'id 相同：先拷贝 `nums1` 那项，再把 `nums2` 的值加上去，两个指针一起后移',
              '循环条件用 `or`，一边走完后逐项把另一边剩下的放进去'],
        summary=['时间 `O(n+m)`，空间 `O(1)`（不计返回值）',
                 '放入答案时用 `[:]` 拷贝，之后累加不会改动输入',
                 '原文为 Python 2 风格，本题代码无需改动',
                 '对比灵神：灵神循环到一边用完后用 `extend` 整段接上，yiduobo 用 `or` 逐项处理'],
    ),
)
