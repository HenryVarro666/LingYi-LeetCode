def _cnt_txt(S):
    if 'cnt' not in S:
        return ''
    items = [f'{k}:{c}' for k, c in sorted(S['cnt'].items()) if c]
    return f'cnt（值:次数）= `{{{", ".join(items)}}}`　`ma = {S.get("ma", 0)}`　`mi = {S.get("mi", 0)}`'


def _qtxt(S):
    if 'nowb' not in S or 'x' not in S:
        return ''
    be = f'，块边界 `{S["block_end"]}`' if 'block_end' in S else ''
    return f'询问 `[{S["x"]}, {S["y"]}]`，阈值 {S["threshold"]}，b = {S["b"]}{be}'


def _color(S, i, v):
    if 'nowy' not in S or 'x' not in S or 'block_end' not in S:
        return None
    ln = S.get('_line', 0)
    x, be = S['x'], S['block_end']
    if 39 <= ln <= 47 and x <= i <= be:
        return 'orange'
    if be < i <= S['nowy'] and ln >= 29:
        return 'blue'
    return None


CONFIG = dict(
    num=3636, title='查询超过阈值频率最高元素', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='回滚莫队 · 左端点补齐再缩回',
    tags=['灵神题单·常用数据结构', '难度分 2451'],
    code='''
class Solution(object):
    def subarrayMajority(self, nums, queries):
        
        cnt = {}
        ma = 0
        mi = 0
        b = int(len(nums) ** 0.5)
        if b == 0:
            b = 1
        q = sorted([[x, y, threshold, index] for index, (x, y, threshold) in enumerate(queries)], key=lambda d: (d[0] // b, d[1]))
        res = [-1] * len(q)
        
        nowb = -1
        nowy = -1
        for x, y, threshold, index in q:
            if nowb != x // b:
                block_end = (x // b + 1) * b - 1
                if y <= block_end:
                    cnt = {}
                    ma, mi = 0, 0
                    for v in nums[x : y + 1]:
                        cnt[v] = cnt.get(v, 0) + 1
                        if cnt[v] > ma or (cnt[v] == ma and v < mi):
                            ma, mi = cnt[v], v
                    if ma >= threshold:
                        res[index] = mi
                    continue
                
                nowb = x // b
                nowy = block_end
                cnt = {}
                ma, mi = 0, 0
            for v in nums[nowy + 1: y + 1]:
                cnt[v] = cnt.get(v, 0) + 1
                if cnt[v] > ma or (cnt[v] == ma and v < mi):
                    ma, mi = cnt[v], v
            nowy = y
            ori_ma, ori_mi = ma, mi
            for v in nums[x : block_end + 1]:
                cnt[v] = cnt.get(v, 0) + 1
                if cnt[v] > ma or (cnt[v] == ma and v < mi):
                    ma, mi = cnt[v], v
            if ma >= threshold:
                res[index] = mi
            for v in nums[x : block_end + 1]:
                cnt[v] -= 1
            ma, mi = ori_ma, ori_mi
        
        return res
''',
    call='Solution().subarrayMajority([1, 1, 2, 2, 1, 1, 3, 3], [[0, 5, 4], [0, 3, 3], [2, 3, 2]])',
    expect=[1, -1, 2],
    views=[
        dict(type='text', fn=_qtxt),
        dict(type='array', var='nums', label='nums（橙 = 左端点补齐的块内部分，蓝 = 右端点扩展出的部分）', h=190,
             pointers={'nowy': 'pink'}, color=_color),
        dict(type='text', fn=_cnt_txt),
        dict(type='array', var='res', label='res', h=130, cell=70),
    ],
    watch=['b', ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('nowy', 'nowy', 'yellow'), ('ma', 'ma', 'orange'), ('mi', 'mi', 'cyan')],
    captions={
        'b = int(len(nums)': '块长 `b = int(√n) = =={b}==`（`n = {len(nums)}`）；`b == 0` 时取 1 防止除零',
        'q = sorted': '询问排序：先按左端点所在块 `x // b`，同块按右端点 `y` 升序 → 块内右端点只往右走',
        'for x, y, threshold, index in q': '处理询问 `[{x}, {y}]`，阈值 {threshold}，它属于块 `{x // b}`',
        'if nowb != x // b': lambda S, B, r: (f'`nowb = {S.nowb}` ≠ 块 `{S.x // S.b}` → 换了一个新块，要重新确定块边界' if S.nowb != S.x // S.b
                                              else f'还在块 `{S.nowb}`：右端点的计数结果可以接着用'),
        'block_end = (x // b': '块 `{x // b}` 的右边界 `block_end = {block_end}`',
        'if y <= block_end': lambda S, B, r: (f'`y = {S.y} ≤ block_end = {S.block_end}`：整个区间都在块内，==直接暴力==' if S.y <= S.block_end
                                              else f'`y = {S.y} > block_end = {S.block_end}`：右端点越过了块边界，可以用莫队'),
        'nowb = x // b': '记住当前块 `nowb = {nowb}`',
        'nowy = block_end': '右端点从块边界 `block_end = {block_end}` 开始，扩展出的结果不清空 → `nowy = {nowy}`',
        'for v in nums[x : y + 1]': '暴力：逐个统计 `nums[{x}..{y}]`',
        'for v in nums[nowy + 1: y + 1]': '右端点从 `nowy = {nowy}` 往右扩展到 `y = {y}`：只加不删',
        'for v in nums[x : block_end + 1]': lambda S, B, r: ('左端点：从块边界往左补到 `x`，把 `nums[{}..{}]` 加进来（只加不删）'.format(S.x, S.block_end)
                                                           if S.get('_line') == 39 else
                                                           '回缩：把刚才补进来的 `nums[{}..{}]` 在 `cnt` 里逐个减掉'.format(S.x, S.block_end)),
        'cnt[v] -= 1': '`cnt[{v}]` 减回去 → {cnt[v]}',
        'if cnt[v] > ma': lambda S, B, r: (f'`{S.v}` 出现 {S.cnt[S.v]} 次：超过 `ma = {B.ma}` → 新众数' if S.cnt[S.v] > B.ma
                                           else (f'`{S.v}` 出现 {S.cnt[S.v]} 次：与 `ma` 相同，且 `{S.v} < mi = {B.mi}` → 取更小的值' if S.cnt[S.v] == B.ma and S.v < B.mi
                                                 else f'`{S.v}` 出现 {S.cnt[S.v]} 次：没有超过 `ma = {B.ma}`')),
        'ma, mi = cnt[v], v': '更新：`ma = {ma}`，`mi = {mi}`',
        'ma, mi = 0, 0': '重置众数记录：`ma = 0`，`mi = 0`',
        'cnt = {}': '清空 `cnt`',
        'nowy = y': '右端点就位：`nowy = {nowy}`',
        'ori_ma, ori_mi = ma': '==存档==：此时只含右端点扩展的结果，`ori_ma = {ori_ma}`，`ori_mi = {ori_mi}`，缩回时直接用',
        'if ma >= threshold': lambda S, B, r: (f'`ma = {S.ma} ≥ 阈值 {S.threshold}` → 答案是众数 `{S.mi}`' if S.ma >= S.threshold
                                               else f'`ma = {S.ma} < 阈值 {S.threshold}` → 没有达标元素，保持 -1'),
        'res[index] = mi': '`res[{index}] = {mi}`',
        'ma, mi = ori_ma': '缩回后众数无法由删除推出 → 直接==恢复存档==：`ma = {ma}`，`mi = {mi}`',
        'return res': '返回 `{res}`',
    },
    skip=['cnt[v] -= 1', 'cnt[v] = cnt.get', 'continue', 'cnt = {}', 'ma = 0', 'mi = 0', 'nowb = -1', 'nowy = -1', 'if b == 0', 'b = 1', 'res = [-1]'],
    max_steps=80,
    cards=dict(
        one_liner='右端点只扩展不回头，左端点补齐后缩回：回滚莫队',
        complexity='时间 `O((n + q)·√n)`，空间 `O(n)`',
        problem=['每个询问 `[l, r, threshold]`：区间里出现次数 ≥ 阈值的元素中，取频率最高、同频取最小的',
                 '没有达标元素返回 `-1`',
                 '示例：`nums=[1,1,2,2,1,1,3,3]`，三个询问，答案 `[1, -1, 2]`'],
        quote='对于区间众数，当区间缩回时，若当前众数的出现次数因为缩回操作变少时，要确定新的众数就不容易了。……就可以使用两个变量记录当前区间仅扩展完右边界时的众数以及出现的次数，接下来在左边界扩展前先记录一个副本。',
        quote_src='—— yiduobo 题解原文',
        idea=['询问按「左端点所在块、右端点」排序，同块内右端点单调右移',
              '左端点永远从块边界往左补到 `x`；算完答案再把 `cnt` 减回去',
              '`ma`、`mi` 不靠删除推回来，直接用扩展前存的 `ori_ma`、`ori_mi`'],
        summary=['块长 `b = √n`，右端点每块 `O(n)`，左端点每询问 `O(b)`，合计 `O((n + q)·b)`',
                 '区间整个落在块内（`y ≤ block_end`）的询问直接暴力，不影响 `cnt`',
                 '易错：换新块要清空 `cnt`、`ma`、`mi` 并把 `nowy` 重置到块边界',
                 '原文是 Python 2 风格，本题代码无需改动，直接可在 Python 3 运行',
                 '对比灵神：灵神把块大小取 `n/√(2q)` 并先离散化；yiduobo 取 `√n`，用哈希表计数'],
    ),
)
