def _lim(S):
    return S.get('limit')


CONFIG = dict(
    num=1923, title='最长公共子路径', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='后缀数组 + 高度数组 + 二分答案（Go 原文转写）',
    tags=['灵神题单·字符串', '难度分 2661'],
    setup='''
def suffix_array(a):
    # 等价于 Go 的 suffixarray（SA-IS）：返回 a 的所有后缀按字典序排好的起点下标
    return sorted(range(len(a)), key=lambda i: a[i:])
''',
    code='''
class Solution:
    def longestCommonSubpath(self, _: int, paths: List[List[int]]) -> int:
        a = []
        minPathLen = int(1e9)  # 二分右边界
        for p in paths:
            minPathLen = min(minPathLen, len(p))
            a.append(int(1e9))  # 用一个不存在 paths 中的数拼接所有路径
            a.extend(p)
        n, m = len(a), len(paths)

        # 标记每个元素属于哪条路径
        ids = [0] * n
        id = -1
        for i, v in enumerate(a):
            if v == int(1e9):
                id += 1
                ids[i] = m
            else:
                ids[i] = id

        # 构建 a 的后缀数组和高度数组
        sa = suffix_array(a)
        rank = [0] * n
        for i in range(n):
            rank[sa[i]] = i
        height = [0] * n
        h = 0
        for i, rk in enumerate(rank):
            if h > 0:
                h -= 1
            if rk > 0:
                j = sa[rk - 1]
                while i + h < n and j + h < n and a[i + h] == a[j + h]:
                    h += 1
            height[rk] = h

        # 二分求答案
        def check(limit):
            limit += 1
            vis = [0] * m
            i = 1
            while i < n:
                if height[i] < limit:
                    i += 1
                    continue
                cnt = 0
                st = i
                while i < n and height[i] >= limit:
                    # 检查 sa[i] 和 sa[i-1]
                    j = ids[sa[i]]
                    if j < m and vis[j] != st:
                        vis[j] = st
                        cnt += 1
                    j = ids[sa[i - 1]]
                    if j < m and vis[j] != st:
                        vis[j] = st
                        cnt += 1
                    i += 1
                if cnt == m:
                    return False
                i += 1
            return True

        lo, hi = 0, minPathLen
        while lo < hi:
            mid = (lo + hi) // 2
            if not check(mid):
                lo = mid + 1
            else:
                hi = mid
        return lo
''',
    call='Solution().longestCommonSubpath(3, [[1,2],[0,1,2]])',
    expect=2,
    views=[
        dict(type='array', var='a', label='a：路径用 1e9 隔开拼成一条（颜色 = 属于第几条路径）', h=150, cell=64,
             color=lambda S, i, v: (None if 'ids' not in S else ('orange' if S['ids'][i] == S['m'] else ['blue', 'pink', 'green', 'purple'][S['ids'][i] % 4]) if i < len(S['ids']) and 'm' in S else None),
             ),
        dict(type='array', var='sa', label='sa：后缀按字典序排好后的起点', h=130, cell=64, color=lambda S, i, v: None),
        dict(type='array', var='height', label='height[k]：sa[k] 与 sa[k-1] 的最长公共前缀', h=130, cell=64,
             pointers={'i': 'yellow'},
             color=lambda S, i, v: ('green' if 'limit' in S['_inner'] and S['_inner'].get('i') is not None and v >= S['_inner']['limit'] and i > 0 else None)),
        dict(type='text', fn=lambda S: ('二分：`lo = %s`，`hi = %s`，检查长度 `mid + 1`' % (S['lo'], S['hi'])) if 'lo' in S else '', size=28, h=60),
        dict(type='text', fn=lambda S: ('这一段 `height >= %s` 的后缀里，覆盖了 `%s / %s` 条路径' % (S['limit'], S['cnt'], S['m'])) if 'cnt' in S['_inner'] else '', size=28, h=60),
    ],
    watch=['lo', 'hi', 'mid', 'limit', 'i', 'cnt', 'h'],
    captions={
        'minPathLen = min': '公共子路径不会比最短的路径长：`minPathLen` = {minPathLen}（二分的右边界）',
        'a.append(int(1e9))': '拼接前先放一个不会出现在 `paths` 里的数 `1e9` 当分隔符，防止公共前缀跨路径',
        'a.extend(p)': '接上这条路径，`a = {a}`',
        'n, m =': '拼好后 `a` 长 `n = {n}`，共 `m = {m}` 条路径',
        'ids[i] = m': '分隔符不属于任何路径，标成 `m`（以后统计时忽略）',
        'ids[i] = id': '`a[{i}] = {v}` 属于第 `{id}` 条路径',
        'sa = suffix_array(a)': '后缀数组：把 `a` 的所有后缀按字典序排序，`sa = {sa}`',
        'rank[sa[i]] = i': '`rank` 是 `sa` 的反函数：后缀 `{sa[i]}` 排第 `{i}` 名',
        'if h > 0': 'Kasai 算法：`rank` 顺着后缀起点 `i` 走，`h` 只会减少至多 1，保证整体线性',
        'j = sa[rk - 1]': '排在 `i` 前一名的后缀起点是 `j = {j}`，和它比较最长公共前缀',
        'while i + h < n': lambda S, B, r: (f'`a[{S.i + S.h}] = {S.a[S.i + S.h]}` 等于 `a[{S.j + S.h}]` → 公共前缀还能更长' if (S.i + S.h < S.n and S.j + S.h < S.n and S.a[S.i + S.h] == S.a[S.j + S.h]) else '再往后不一样了（或到末尾）→ 公共前缀长度停在 `h`'),
        'h += 1': '`h` 加一 → {h}',
        'height[rk] = h': '`height[{rk}] = {h}`：后缀 `{i}` 与前一名后缀的最长公共前缀长度',
        'limit += 1': '检查长度 `limit = {limit}`：是否存在所有路径都有的公共子路径',
        'vis = [0] * m': '`vis[j]` 记录路径 `j` 在当前这一段里是否出现过',
        'if height[i] < limit': lambda S, B, r: (f'`height[{S.i}] = {S.height[S.i]} < {S.limit}`：前后缀公共前缀不够长，跳过' if S.height[S.i] < S.limit else f'`height[{S.i}] = {S.height[S.i]} >= {S.limit}`：从这里开始是一段公共前缀 >= `limit` 的后缀'),
        'st = i': '这一段的起点 `st = {st}`，同时用它当 `vis` 的标记',
        'while i < n and height[i] >= limit': lambda S, B, r: (f'`height[{S.i}] = {S.height[S.i]} >= {S.limit}`：还在同一段里，继续' if (S.i < S.n and S.height[S.i] >= S.limit) else '这一段结束，数一数覆盖了几条路径'),
        'j = ids[sa[i]]': '后缀 `sa[{i}] = {sa[i]}` 属于路径 `{j}`（`{m}` 表示分隔符）',
        'j = ids[sa[i - 1]]': '前一名后缀 `sa[{i-1}] = {sa[i-1]}` 属于路径 `{j}`',
        'vis[j] = st': '路径 `{j}` 第一次出现在这一段 → `cnt = {cnt+1}`',
        'cnt += 1': '已覆盖 `{cnt}` 条路径，一共要 `{m}` 条',
        'if cnt == m': lambda S, B, r: (f'`cnt = {S.cnt} == m`：这一段覆盖了所有路径 → 长度 `{S.limit}` 可行' if S.cnt == S.m else f'`cnt = {S.cnt} < m = {S.m}`：没覆盖全，看下一段'),
        'return False': '存在覆盖所有路径的一段 → `check` 返回 False（可行，往更长的找）',
        'return True': '没有任何一段覆盖所有路径 → `check` 返回 True（这个长度不可行）',
        'mid = (lo + hi) // 2': '二分区间 `[{lo}, {hi})`，取 `mid = {mid}`',
        'if not check(mid)': '调用 `check({mid})`：长度 `{mid + 1}` 的公共子路径存在吗？',
        'lo = mid + 1': '`check` 为 False：长度 `{mid + 1}` 可行，答案至少是它 → `lo = mid + 1 = {lo}`',
        'hi = mid': '`check` 为 True：长度 `{mid + 1}` 不可行，答案更短 → `hi = mid = {hi}`',
        'return lo': '`lo = hi = {lo}`：第一个不可行的长度减一，就是最长公共子路径长度 =={ret}==',
    },
    skip=['i += 1', 'rank = [0]', 'height = [0]', 'ids = [0]', 'id = -1', 'h = 0', 'lo, hi = 0', 'for i, v in enumerate', 'if v == int', 'id += 1', 'ids[i] = m', 'for i in range(n)', 'rank[sa[i]]', 'if h > 0', 'h -= 1', 'for p in paths', 'a = []', 'if rk > 0', 'vis = [0]', 'i = 1', 'continue', 'h += 1', 'cnt += 1', 'height[rk] = h', 'cnt = 0'],
    max_steps=110,
    cards=dict(
        one_liner='拼成一条串，后缀数组里找「覆盖所有路径」的公共前缀',
        complexity='时间 `O(L log L)`（`L` 为路径总长），空间 `O(L)`',
        problem=['`m` 个朋友各走一条路径（城市编号序列），求所有人都走过的最长公共子路径长度',
                 '子路径是路径中连续的一段',
                 '本视频：`[[1,2],[0,1,2]]` → `2`（公共子路径 `[1,2]`）'],
        quote='用一个不存在 paths 中的数拼接所有路径；构建 a 的后缀数组和高度数组；二分求答案',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['所有路径用不会出现的数隔开拼成 `a`，对 `a` 建后缀数组和高度数组',
              '长度 `limit` 可行 ⇔ 存在一段连续的后缀，两两 `height >= limit`，且覆盖了全部 `m` 条路径',
              '可行性单调（短的一定也行），所以二分答案；`sort.Search` 找第一个不可行的长度'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.Search` 展开成二分循环，`for` 里改 `i` 的写法用 `while`）',
                 'Go 的 `suffixarray` 包 Python 没有，在 setup 里用排序实现 `suffix_array`，作者其余代码未改',
                 '原文用 `unsafe` 取出 Go 内部的 `sa`，这里直接由 `suffix_array(a)` 给出，含义相同',
                 '时间 `O(L log L)`（建后缀数组 `O(L)`，二分 `log L` 次，每次扫一遍），空间 `O(L)`',
                 '易错点：分隔符必须唯一，否则公共前缀会跨过路径边界；`vis[j] != st` 用段起点去重，不用每次清空'],
    ),
)
