def _rng(S):
    """(sweep_lo, sweep_hi, jit_lo, jit_hi) 半开区间，None 表示没有"""
    if 'qs' not in S or 'block_size' not in S:
        return None
    if 'bid' in S and 'qr' in S and 'l0' in S:
        sweep = (S['l0'], S['r']) if 'r' in S and isinstance(S['r'], int) and S['r'] >= S['l0'] else (S['l0'], S['l0'])
        ln = S.get('_line', 0)
        if ln < 46:
            return (0, 0), (0, 0)
        return sweep, ((S['ql'], S['l0']) if 51 <= ln <= 58 else (0, 0))
    if 'l' in S and 'r' in S and 'threshold' in S and 'bid' not in S:
        return (S['l'], S['r']), (0, 0)
    return None


def _color(S, i, v):
    g = _rng(S)
    if not g:
        return None
    (a, b), (c, d) = g
    if c <= i < d:
        return 'orange'
    if a <= i < b:
        return 'blue'
    return None


def _cnt_txt(S):
    if 'cnt' not in S or 'a' not in S:
        return ''
    items = [f'{S["a"][k]}:{c}' for k, c in enumerate(S['cnt'][:len(S['a'])]) if c]
    return f'cnt（值:次数）= `{{{", ".join(items)}}}`　`max_cnt = {S.get("max_cnt", 0)}`　`min_val = {S.get("min_val", 0)}`'


def _qtxt(S):
    if 'qs' not in S or not S.get('qs') or 'threshold' not in S:
        return ''
    if 'qid' in S:
        return f'离线询问 `[{S["ql"]}, {S["qr"]})`，阈值 {S["threshold"]}，块 {S["bid"]}，`l0 = {S["l0"]}`'
    return ''


CONFIG = dict(
    num=3636, title='查询超过阈值频率最高元素', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='回滚莫队（只加不删）',
    tags=['灵神题单·常用数据结构', '难度分 2451'],
    code='''
class Solution:
    def subarrayMajority(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n, m = len(nums), len(queries)
        # 离散化
        a = sorted(set(nums))
        index_to_value = [bisect_left(a, x) for x in nums]
        cnt = [0] * (len(a) + 1)
        max_cnt = min_val = 0
        def add(i: int) -> None:
            nonlocal max_cnt, min_val
            v = index_to_value[i]
            cnt[v] += 1
            c = cnt[v]
            x = nums[i]
            if c > max_cnt:
                max_cnt, min_val = c, x
            elif c == max_cnt:
                min_val = min(min_val, x)
        ans = [-1] * m
        block_size = ceil(n / sqrt(m * 2))
        qs = []  # (bid, ql, qr, threshold, qid) 其中 bid 是块号，qid 是询问的编号
        for i, (l, r, threshold) in enumerate(queries):
            r += 1  # 左闭右开
            # 大区间离线（保证 l 和 r 不在同一个块中）
            if r - l > block_size:
                qs.append((l // block_size, l, r, threshold, i))
                continue
            # 小区间暴力
            for j in range(l, r):
                add(j)
            if max_cnt >= threshold:
                ans[i] = min_val
            # 重置数据
            for v in index_to_value[l: r]:
                cnt[v] -= 1
            max_cnt = 0
        qs.sort(key=lambda q: (q[0], q[2]))
        for i, (bid, ql, qr, threshold, qid) in enumerate(qs):
            l0 = (bid + 1) * block_size
            if i == 0 or bid > qs[i - 1][0]:  # 遍历到一个新的块
                r = l0  # 右端点移动的起点
                # 重置数据
                cnt = [0] * (len(a) + 1)
                max_cnt = 0
            # 右端点从 r 移动到 qr（qr 不计入）
            while r < qr:
                add(r)
                r += 1
            tmp_max_cnt, tmp_min_val = max_cnt, min_val
            # 左端点从 l0 移动到 ql（l0 不计入）
            for j in range(ql, l0):
                add(j)
            if max_cnt >= threshold:
                ans[qid] = min_val
            # 回滚
            max_cnt, min_val = tmp_max_cnt, tmp_min_val
            for v in index_to_value[ql: l0]:
                cnt[v] -= 1
        return ans
''',
    call='Solution().subarrayMajority([1, 1, 2, 2, 1, 1], [[0, 5, 4], [0, 3, 3], [2, 3, 2]])',
    expect=[1, -1, 2],
    setup='from math import ceil, sqrt',
    views=[
        dict(type='text', fn=_qtxt),
        dict(type='array', var='nums', label='nums（橙 = 左端点回滚段，蓝 = 右端点只增不减的部分）', h=190,
             pointers={'l0': 'green', 'r': 'pink'}, color=_color),
        dict(type='text', fn=_cnt_txt),
        dict(type='array', var='ans', label='ans', h=130, cell=70),
    ],
    watch=['block_size', ('l0', 'l0', 'green'), ('r', 'r', 'pink'), ('max_cnt', 'max_cnt', 'orange'), ('min_val', 'min_val', 'cyan')],
    captions={
        'index_to_value =': '离散化：值映射到 `0..{len(a) - 1}`，这样 `cnt` 可以用数组代替哈希表',
        'block_size = ceil': lambda S, B, r: f'块大小 `ceil(n / sqrt(2m)) = ceil({S.n} / sqrt({2 * S.m})) = =={S.block_size}==`：右端点总移动与左端点抖动平衡',
        'qs = []': '`qs` 收集「大区间」询问：(块号, ql, qr, 阈值, 编号)',
        'r += 1  #': '改成左闭右开：`[{l}, {r})`',
        'if r - l > block_size': lambda S, B, r: (f'区间长度 `{S.r - S.l} > {S.block_size}`：l、r 不在同一块 → ==离线==处理' if S.r - S.l > S.block_size
                                                   else f'区间长度 `{S.r - S.l} ≤ {S.block_size}`：很短 → 直接暴力'),
        'qs.append': '记下它：块号 `l // block_size = {l // block_size}`，等会儿按块分组',
        'for j in range(l, r)': '小区间：逐个 `add` 进来',
        'if max_cnt >= threshold:': lambda S, B, r: (f'`max_cnt = {S.max_cnt} ≥ 阈值 {S.threshold}` → 答案是众数 `{S.min_val}`' if S.max_cnt >= S.threshold
                                                      else f'`max_cnt = {S.max_cnt} < 阈值 {S.threshold}` → 没有元素达标，保持 -1'),
        'ans[i] = min_val': '`ans[{i}] = {min_val}`',
        'ans[qid] = min_val': '`ans[{qid}] = {min_val}`',
        'r += 1': '右端点右移：`r = {r}`',
        'qs.sort': '先按块号分组，块内按右端点 `qr` 升序：右端点只会往右走',
        'l0 = (bid + 1)': '`l0 = (bid + 1) * block_size = {l0}`：本块的右边界，右端点从这里开始扫',
        'if i == 0 or bid': lambda S, B, r: ('进入新的一块 → 右端点从 `l0` 重新开始，计数清零' if (S.i == 0 or S.bid > S.qs[S.i - 1][0])
                                              else '还在同一块 → 右端点接着上一个询问继续往右'),
        'while r < qr': lambda S, B, r: (f'`r = {S.r} < qr = {S.qr}`：右端点还没到，继续 add' if S.r < S.qr
                                          else f'`r = {S.r}` 到达 `qr = {S.qr}`，右端点就位'),
        'tmp_max_cnt, tmp_min_val =': '先存档 `max_cnt = {max_cnt}`、`min_val = {min_val}`：下面左端点要「借用」，用完要回滚',
        'for j in range(ql, l0)': '左端点从 `l0` 向左走到 `ql = {ql}`：只加不删，所以不用维护删除',
        'max_cnt, min_val = tmp_max_cnt': '回滚：`max_cnt`、`min_val` 恢复成存档值 `{max_cnt}`、`{min_val}`；随后把左半段的 `cnt` 逐个减回去',
        'cnt[v] -= 1': '回滚计数：把左半段加进去的元素减掉，`cnt` 复原',
        'cnt[v] += 1': 'add 下标 {i}：`nums[{i}] = {nums[i]}` 的次数 → `{cnt[v]}`',
        'if c > max_cnt': lambda S, B, r: (f'次数 `{S.c}` 超过 `max_cnt = {B.max_cnt}` → 它成为新的众数' if S.c > B.max_cnt else '次数没超过最大值'),
        'elif c == max_cnt': lambda S, B, r: (f'次数 `{S.c}` 与 `max_cnt` 相同 → 取较小的值作 `min_val`' if S.c == S.max_cnt else '次数更小，什么都不用做'),
        'max_cnt, min_val = c, x': '更新 `max_cnt = {max_cnt}`，`min_val = {min_val}`',
        'min_val = min(min_val, x)': '`min_val = min(.., {x})` = {min_val}',
        'return ans': '返回 `{ans}`：-1 表示没有元素次数达到阈值',
    },
    skip=['add(j)', 'add(r)', 'for j in range(ql, l0)', 'cnt[v] -= 1', 'qs.sort', 'for j in range(l, r)', 'for v in index_to_value', 'r += 1', 'r = l0', 'n, m = len', 'v = index_to_value[i]', 'c = cnt[v]', 'x = nums[i]', 'continue', 'max_cnt = min_val = 0', 'cnt = [0] * (len(a) + 1)', 'ans = [-1]', 'a = sorted'],
    max_steps=62,
    cards=dict(
        one_liner='改变回答询问的顺序，让区间只增不删：回滚莫队',
        complexity='时间 `O(n log n + q log q + n√q)`，空间 `O(n + q)`',
        problem=['每个询问 `[l, r, threshold]`：区间里出现次数 ≥ 阈值的元素中，选频率最高、同频取最小的',
                 '没有达标元素返回 `-1`',
                 '示例：`nums=[1,1,2,2,1,1]`，询问 `[[0,5,4],[0,3,3],[2,3,2]]` → `[1,-1,2]`'],
        quote='莫队算法的核心思想是：把询问按照左端点所在块分组，左端点在同一个块的询问分到同一组。对于每个块，把右端点排序，使得右端点在数组中一直向右移动，而左端点只在块内「抖动」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删除元素时没法维护「最小的众数」，那就只做「添加」',
              '右端点从块边界 `l0` 一路右移；左端点每次从 `l0` 向左补到 `ql`',
              '回答完把 `max_cnt`、`min_val` 恢复成存档，`cnt` 减回去 → 回滚'],
        summary=['块大小 `ceil(n / sqrt(2q))` 使右端点与左端点的总移动量平衡，总访问 `O(n√q)`',
                 '区间 ≤ 块大小的询问直接暴力，保证大区间的 `l`、`r` 不在同一块',
                 '易错：换新块时要清空 `cnt`、`max_cnt` 并把 `r` 重置为 `l0`',
                 '优化前用哈希表；本视频是离散化 + 数组的优化版'],
    ),
)
