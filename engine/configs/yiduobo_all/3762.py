NUMS = [6, 3, 9, 5]
K = 3
QUERIES = [[0, 2], [1, 3]]

CODE = '''
class Solution(object):
    def minOperations(self, nums, k, queries):
        
        sorted_nums = sorted(nums)

        p2 = 1
        height = 1
        while p2 < len(nums):
            p2 += p2
            height += 1
        
        t = [[0] * len(nums) for _ in range(height)]
        s = [[0] * len(nums) for _ in range(height)]
        left_cnt = [[0] * len(nums) for _ in range(height)]
        left_s = [[0] * len(nums) for _ in range(height)]
        t[0] = nums[:]

        def build(level, left, right):
            if left == right:
                return
            
            mid = (left + right) // 2
            mid_v = sorted_nums[mid]
            same = mid - left + 1
            for v in t[level - 1][left: right + 1]:
                if v < mid_v:
                    same -= 1
            
            p, q = left, mid + 1
            for index, v in enumerate(t[level - 1][left: right + 1], left):
                if index > left:
                    s[level - 1][index] = s[level - 1][index - 1]
                    left_cnt[level - 1][index] = left_cnt[level - 1][index - 1]
                    left_s[level - 1][index] = left_s[level - 1][index - 1]

                s[level - 1][index] += v
                if v < mid_v or (v == mid_v and same > 0):
                    t[level][p] = v
                    left_cnt[level - 1][index] += 1
                    left_s[level - 1][index] += v
                    p += 1
                    if v == mid_v:
                        same -= 1
                else:
                    t[level][q] = v
                    q += 1
            
            build(level + 1, left, mid)
            build(level + 1, mid + 1, right)
        
        def find(level, left, right, start, end, k):
            if start == end:
                return t[level][start], 0
            
            mid = (left + right) // 2

            prefix_in_left = 0
            interval_s = s[level][end]
            interval_left_s = left_s[level][end]
            if start > left:
                prefix_in_left = left_cnt[level][start - 1]
                interval_s -= s[level][start - 1]
                interval_left_s -= left_s[level][start - 1]

            interval_in_left = left_cnt[level][end] - prefix_in_left
            interval_in_right = end - start + 1 - interval_in_left

            if interval_in_left >= k:
                nxt_start = left + prefix_in_left
                nxt_end = nxt_start + interval_in_left - 1
                kth, v = find(level + 1, left, mid, nxt_start, nxt_end, k)
                return kth, v + interval_s - interval_left_s - kth * interval_in_right
            else:
                prefix_in_right = start - left - prefix_in_left
                interval_in_right = end - start + 1 - interval_in_left
                nxt_start = mid + 1 + prefix_in_right
                nxt_end = nxt_start + interval_in_right - 1
                kth, v = find(level + 1, mid + 1, right, nxt_start, nxt_end, k - interval_in_left)
                return kth, v + kth * interval_in_left - interval_left_s

        build(1, 0, len(nums) - 1)

        belong = []
        parts = 0
        pre = None
        for v in nums:
            if pre is None or v % k != pre % k:
                parts += 1
            belong.append(parts)
            pre = v
        
        res = []
        for left, right in queries:
            if belong[left] != belong[right]:
                res.append(-1)
            else:
                kth, v = find(0, 0, len(nums) - 1, left, right, (right - left + 1) // 2 + 1)
                res.append(v // k)
        
        return res
'''
_L = CODE.split('\n')


def _ln(sub, after=0):
    return next(i for i, s in enumerate(_L) if i >= after and sub in s)   # 引擎的行号 = 去掉开头空行后的 1 起算


_p = _ln('p, q = left, mid + 1')
_b = _ln('build(level + 1, left, mid)')
SKIP = list(range(_p + 1, _b)) + [_ln('for v in t[level - 1][left: right + 1]:'), _ln('if v < mid_v:'), _ln('same -= 1'), 'p2 = 1', 'height = 1',
                              'p2 += p2', 'height += 1', 'while p2 < len', 's = [[0]', 'left_cnt = [[0]', 'left_s = [[0]', 'parts = 0', 'pre = None', 'parts += 1', 'belong.append', 'pre = v', 20, 55, 'interval_s = s[level][end]', 'interval_left_s = left_s[level][end]', 'interval_s -= ', 'interval_left_s -= ', 'nxt_start = ', 'nxt_end = ', 75, 60, 66, 22, 'res = []', 'for v in nums']


def _segs(n, lv):
    segs = [(0, n - 1)]
    for _ in range(lv):
        nxt = []
        for l, r in segs:
            if l == r:
                nxt.append((l, r))
            else:
                m = (l + r) // 2
                nxt += [(l, m), (m + 1, r)]
        segs = nxt
    return segs


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    t, lc = S.get('t'), S.get('left_cnt')
    cv.text((x0 + 18, y0 + 14), '划分树 t[level]；小字 = left_cnt（前缀里去左半的个数）', 20, T['muted'], bold=True)
    if t is None:
        return
    H, n = len(t), len(t[0])
    inn = S.get('_inner') or {}
    lvl = inn.get('level') if 'start' in inn else None
    cw = min(96, (x1 - x0 - 120) / n)
    rh = min(112, (y1 - y0 - 66) / H)
    sx = x0 + 100 + ((x1 - x0 - 120) - cw * n) / 2
    for L in range(H):
        Y = y0 + 64 + L * rh
        cv.text((sx - 12, Y + 24), f'level {L}', 20, T['muted'], anchor='rm', mono=True, bold=True)
        built = L == 0 or any(t[L])
        for a, b in _segs(n, L):
            cv.rect((sx + a * cw + 2, Y - 2, sx + (b + 1) * cw - 2, Y + 66), outline=T['border'], width=2, r=8)
        for i in range(n):
            X = sx + i * cw
            hot = lvl == L and inn['start'] <= i <= inn['end']
            fill = (84, 72, 36) if hot else (T['panel2'] if built else (24, 28, 36))
            cv.rect((X + 5, Y + 4, X + cw - 5, Y + 44), fill=fill, r=6, outline=T['yellow'] if hot else None, width=3)
            cv.text((X + cw / 2, Y + 24), t[L][i] if built else '·', 24, T['text'] if built else T['dim'], anchor='mm', bold=True)
            if L < H - 1 and built and any(lc[L]):
                cv.text((X + cw / 2, Y + 56), lc[L][i], 17, T['cyan'], anchor='mm', mono=True)


def _info(S):
    inn = S.get('_inner') or {}
    if 'start' in inn and inn.get('k') is not None and inn.get('left') is not None:
        return (f'`level {inn["level"]}`：节点 `[{inn["left"]},{inn["right"]}]`，查子区间 `[{inn["start"]},{inn["end"]}]` 第 `{inn["k"]}` 小'
                + (f'；左半有 `{inn["interval_in_left"]}` 个' if 'interval_in_left' in inn else ''))
    if 'level' in inn and 'mid_v' in inn:
        return f'`level {inn["level"]}`：节点 `[{inn["left"]},{inn["right"]}]`，pivot = `sorted_nums[{inn["mid"]}] = {inn["mid_v"]}`'
    return ''


CONFIG = dict(
    num=3762, title='使数组元素相等的最小操作次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='同余分段 + 中位数 + 划分树求第 k 小',
    tags=['灵神题单·常用数据结构', '灵神题单·贪心与思维', '难度分 2497'],
    code=CODE,
    call=f'Solution().minOperations({NUMS}, {K}, {QUERIES})',
    expect=[2, -1],
    max_steps=60,
    skip=SKIP,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前查询区间）', cell=70, h=170,
             color=lambda S, i, v: 'blue' if 'left' in S and 'right' in S and 'belong' in S and S['_inner'].get('start') is None and S['left'] <= i <= S['right'] else None),
        dict(type='array', var=lambda S: S.get('belong'), label='belong：同余段编号（段号不同 → 无解）', cell=70, h=140),
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_info, size=22, h=50),
        dict(type='calls', h=100, hide=('start', 'end')),
    ],
    watch=[('kth', "S.get('kth')", 'yellow'), ('v', "S['_inner'].get('v')", 'pink'), ('res', "S.get('res')", 'green')],
    captions={
        'sorted_nums = sorted': '先排序得到 `{sorted_nums}`：划分树每个节点的 pivot 都取排序数组的中点',
        't = [[0]': '划分树是 `height × n` 的二维数组，一共 `{height}` 层',
        't[0] = nums[:]': '第 0 层就是原数组',
        'if left == right': lambda S, B, r: ('区间只剩一个数，不用再分了，返回' if S.left == S.right else f'节点 `[{S.left},{S.right}]` 还要继续划分'),
        'mid = (left + right)': '划分点 `mid = {mid}`',
        'mid_v = sorted_nums[mid]': '划分点 `mid = {mid}`，pivot = `sorted_nums[{mid}] = {mid_v}`：比它小的去左半，大的去右半',
        'same = mid - left + 1': '左半一共 `{same}` 个位置；等于 pivot 的数要按名额分配，所以先减掉严格小于 pivot 的个数',
        'p, q = left, mid + 1': '把本节点的数按 pivot 稳定地分到下一层：`p` 从左半起点放、`q` 从右半起点放，同时记下 `left_cnt`、`left_s`、`s` 三个前缀数组',
        'build(level + 1, left, mid)': '左半继续划分',
        'build(level + 1, mid + 1, right)': '右半继续划分',
        'belong = []': '同余分段：模 `k` 相同的连续元素属于同一段，段号放进 `belong`（从左到右扫一遍）',
        'for v in nums': lambda S, B, r: ('从左到右分段，`belong[i]` = 第几个同余段' if 'v' not in B or B.v != S.v else '分段完成：`belong = {}`'.format(S.belong)),
        'if pre is None or v % k': lambda S, B, r: ('第一个数，开新段' if S.pre is None else (f'`{S.v} % {S.k} = {S.v % S.k}` ≠ `{S.pre} % {S.k} = {S.pre % S.k}`：余数变了 → 开新段' if S.v % S.k != S.pre % S.k else f'余数同为 `{S.v % S.k}` → 同一段')),
        'for left, right in queries': lambda S, B, r: (f'处理查询 `[{S.left}, {S.right}]`' if not ('res' in B and 'kth' in B and B.left == S.left) else '所有查询处理完了'),
        'if belong[left] != belong[right]': lambda S, B, r: (f'`belong[{S.left}] = {S.belong[S.left]} ≠ belong[{S.right}] = {S.belong[S.right]}`：不同段，余数不同 → ==-1==' if S.belong[S.left] != S.belong[S.right]
                                                            else f'`belong` 都是 `{S.belong[S.left]}`：同一段 → 有解，找中位数'),
        'res.append(-1)': '无解 → `-1`',
        'kth, v = find(0, 0': '在划分树里找区间第 `{(right - left + 1) // 2 + 1}` 小（= 中位数），并同时算出所有数到它的距离和',
        'if start == end': lambda S, B, r: (f'区间只剩一个数：`t[{S.level}][{S.start}] = {S.t[S.level][S.start]}` 就是第 k 小；距离和从 0 开始' if S.start == S.end else '区间还有多个数，继续往下'),
        'prefix_in_left = 0': '要在这个节点里查子区间 `[{start},{end}]`：先算它左边（节点内）有多少个数去了左半，再用 `left_cnt` 前缀相减',
        'interval_in_left = left_cnt': '区间 `[{start},{end}]` 一共 `{end - start + 1}` 个数，其中去左半的 `interval_in_left = {interval_in_left}` 个（`left_cnt` 前缀相减），其余去右半',
        'if interval_in_left >= k': lambda S, B, r: (f'`{S.interval_in_left} ≥ k = {S.k}`：第 k 小在==左半==' if S.interval_in_left >= S.k else f'`{S.interval_in_left} < k = {S.k}`：第 k 小在==右半==，要找右半第 `{S.k - S.interval_in_left}` 小'),
        'nxt_start = left + prefix_in_left': '映射到下一层左半：起点 `{nxt_start}`',
        'nxt_end = nxt_start + interval_in_left': '终点 `{nxt_end}`',
        'kth, v = find(level + 1, left, mid': '递归到左半：区间 `[{nxt_start},{nxt_end}]`',
        'return kth, v + interval_s - interval_left_s': '回溯：右半的数都 ≥ kth，贡献 `interval_s − interval_left_s − kth × {interval_in_right}`；累计距离和 `v` = {ret[1]}',
        'prefix_in_right = start': '右半：节点内区间左边有 `{start - left - prefix_in_left}` 个去了右半，这些占掉右半的前几个位置',
        'nxt_start = mid + 1': '映射到下一层右半：起点 `{nxt_start}`',
        'nxt_end = nxt_start + interval_in_right': '终点 `{nxt_end}`',
        'kth, v = find(level + 1, mid + 1': '递归到右半，`k` 减去左半的 `{interval_in_left}` 个',
        'return kth, v + kth * interval_in_left': '回溯：左半的数都 ≤ kth，贡献 `kth × {interval_in_left} − interval_left_s`；累计距离和 `v` = {ret[1]}',
        'res.append(v // k)': '距离和 `{v}` ÷ `k` = =={v // k}== 次操作',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='模 k 分段判无解，划分树一次递归同时求中位数和距离和',
        complexity='时间 `O((n+q) log n)`，空间 `O(n log n)`',
        problem=['一次操作：某个元素 `+k` 或 `−k`；每个查询问 `nums[l..r]` 全部变成相等的最少次数',
                 '无法做到则返回 `-1`',
                 '示例：`nums=[1,4,7], k=3, queries=[[0,1],[0,2]]` → `[1,2]`',
                 '本视频：`[6,3,9,5]`，`k=3`，查询 `[[0,2],[1,3]]` → `[2,-1]`'],
        quote='对于无序的子区间nums[start: end + 1]，问题实际上就是需要找到区间的中位数v，然后计算v与区间中小于v的元素之差的和，再加上区间中大于v的元素与v之差的和，除以k之后即为此次查询的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['模 `k` 余数相同的连续元素分成一段；起止点不在同一段 → `-1`',
              '全部变成中位数最省：把数从两端配对，目标夹在中间时代价最小',
              '划分树 = 把快速排序每一层的结果存下来，再记 `left_cnt` 前缀，可在 `O(log n)` 找区间第 k 小',
              '再加 `s`、`left_s` 两个和的前缀数组：下降时把另一半的数到 `kth` 的距离和累加起来'],
        summary=['时间建树 `O(n log n)`，每个查询 `O(log n)`，空间 `O(n log n)`',
                 '易错：等于 pivot 的数要按名额分到左半（`same`），否则左右半长度对不上',
                 '易错：去右半时 `k` 要减去 `interval_in_left`，起点要加上 `prefix_in_right`',
                 '原文可直接在 Python 3 运行，代码未改',
                 '对比灵神：灵神用可持久化线段树，yiduobo 用划分树，都是 `O(log n)` 求区间第 k 小'],
    ),
)
