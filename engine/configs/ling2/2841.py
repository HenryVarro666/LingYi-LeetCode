NUMS = [1, 1, 5, 2, 5, 3]
M, K = 3, 3


def WL(S):
    """窗口左端（不足 k 时从 0 开始）"""
    if 'i' not in S:
        return None
    return max(0, S['i'] - K + 1)


def WR(S):
    return S.get('i')


def _color(S, i, v):
    if 'i' not in S:
        return None
    line = S.get('_line')
    left = S['i'] - K + 1
    if line in (19, 20, 21, 22, 23) and i == left:
        return 'red'  # 正在离开窗口
    if i == S['i'] and line in (7, 8):
        return 'green'  # 刚进入窗口
    return None


def _info(S):
    if 'cnt' not in S or 'i' not in S:
        return f'窗口长度 `k = {K}`，至少要有 `m = {M}` 个不同元素'
    left = S['i'] - K + 1
    tag = ''
    if left >= 0 and S.get('_line') in (15, 16):
        tag = ' → ==几乎唯一==' if len(S['cnt']) >= M else f' → 不足 {M} 个，不算'
    return f"窗口和 `s = {S['s']}`，不同元素 `len(cnt) = {len(S['cnt'])}`{tag}"


def _history(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '已检查过的长度为 k 的窗口', 24, T['muted'], bold=True)
    left = S.get('left')
    if not isinstance(left, int):
        return
    line = S.get('_line')
    upto = left if line in (5, 7, 8, 15, 16, 19, 20, 21, 22, 23, 25) else left - 1
    y = y0 + 44
    for L in range(0, upto + 1):
        w = NUMS[L:L + K]
        d = len(set(w))
        ok = d >= M
        txt = f'[{L},{L + K - 1}]  {w}  不同元素 {d} 个  ' + (f'和 = {sum(w)}' if ok else '不算')
        cv.text((x0 + 30, y), txt, 24, T['green'] if ok else T['dim'], mono=True)
        y += 36


def _for_cap(S, B, ret):
    if S.get('i') is not None and S.get('i') != B.get('i'):
        return f'右端点 `i = {S.i}`，`x = {S.x}` 准备进入窗口'
    return '遍历结束'


def _left_cap(S, B, ret):
    if S.left < 0:
        return f'`left = {S.i} - {K} + 1 = {S.left}` < 0：窗口里只有 {S.i + 1} 个数，大小不足 k'
    return f'`left = {S.i} - {K} + 1 = {S.left}`：窗口 `[{S.left}, {S.i}]` 恰好有 k 个数'


def _len_cap(S, B, ret):
    d = len(S.cnt)
    if d >= M:
        return f'`len(cnt) = {d} ≥ m = {M}`：窗口是==几乎唯一==子数组，可以更新答案'
    return f'`len(cnt) = {d} < m = {M}`：不同元素不够，==不更新=='


def _zero_cap(S, B, ret):
    o = S.out
    if S.cnt.get(o, 0) == 0:
        return f'`cnt[{o}]` 减到 0：`{o}` 已不在窗口里 → 要从哈希表删掉'
    return f'`cnt[{o}] = {S.cnt[o]}`：窗口里还有别的 `{o}`，==不能删=='


CONFIG = dict(
    num=2841, title='几乎唯一子数组的最大和', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='定长滑动窗口 · 入 / 更新 / 出',
    tags=['字节30天'],
    code='''
class Solution:
    def maxSum(self, nums: List[int], m: int, k: int) -> int:
        ans = s = 0
        cnt = defaultdict(int)
        for i, x in enumerate(nums):
            # 1. 进入窗口
            s += x
            cnt[x] += 1

            left = i - k + 1
            if left < 0:  # 窗口大小不足 k
                continue

            # 2. 更新答案
            if len(cnt) >= m:
                ans = max(ans, s)

            # 3. 离开窗口
            out = nums[left]
            s -= out
            cnt[out] -= 1
            if cnt[out] == 0:
                del cnt[out]  # 保证 len(cnt) 不计入出现 0 次的元素

        return ans
''',
    call=f'Solution().maxSum({NUMS}, {M}, {K})',
    expect=10,
    skip=['continue'],
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口，绿 = 进入，红 = 离开）', cell=90,
             pointers={'i': 'blue'}, window=(WL, WR), color=_color),
        dict(type='text', h=60, fn=_info, size=27),
        dict(type='map', var='cnt', label='cnt（窗口内每个元素的出现次数）', h=130, font=28, fmt=lambda k, v: f'{k}: {v} 次'),
        dict(type='custom', draw=_history, h=190),
    ],
    watch=[('i', 'i', 'blue'), ('left', 'left'), ('s', 's', 'cyan'), ('len(cnt)', 'len(cnt)', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'ans = s = 0': '`s` 是窗口元素和，`ans` 是答案（没有几乎唯一子数组时返回 0）',
        'cnt = defaultdict': '用==哈希表==统计窗口中每个元素的出现次数：`len(cnt)` 就是不同元素个数',
        'for i, x in': _for_cap,
        's += x': '入：`s += {x}` → `{s}`',
        'cnt[x] += 1': '入：`cnt[{x}] = {cnt[x]}`',
        'left = i - k + 1': _left_cap,
        'if left < 0': lambda S, B, ret: ('窗口大小不足 k → `continue`，先不更新答案' if S.left < 0
                                          else '窗口大小等于 k → 往下更新答案'),
        'if len(cnt) >= m': _len_cap,
        'ans = max': '更新：`ans = max({B.ans}, {s}) = {ans}`',
        'out = nums[left]': '出：窗口最左边的 `nums[{left}] = {out}` 要离开',
        's -= out': '出：`s -= {out}` → `{s}`',
        'cnt[out] -= 1': '出：`cnt[{out}]` 减一 → `{cnt[out]}`',
        'if cnt[out] == 0': _zero_cap,
        'del cnt[out]': '`del cnt[{out}]`：保证 `len(cnt)` 不计入出现 0 次的元素',
        'return ans': '最大和为 =={ret}==',
    },
    cards=dict(
        one_liner='定长窗口：入 → 更新 → 出，哈希表的大小就是不同元素个数',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['给你整数数组 `nums` 和正整数 `m`、`k`',
                 '长度为 `k` 且==至少有 `m` 个互不相同元素==的子数组叫“几乎唯一”，求它们的最大和（没有返回 0）',
                 '示例：`[2,6,7,3,1,7], m=3, k=4` → `18`；本视频 `[1,1,5,2,5,3], m=3, k=3` → `10`'],
        before=[dict(heading='为什么用哈希表而不是哈希集合？', lines=[
            '统计不同元素个数：扔进哈希集合，集合大小就是答案',
            '但元素 `x` 离开窗口时，要不要从集合里删掉？==取决于它是不是窗口中的唯一元素==',
            '所以要知道 `x` 在窗口中的出现次数 → 用哈希表 `cnt` 计数'])],
        quote='当 x 离开窗口时，把 x 在窗口中的出现次数减少一。==如果减一后，x 在窗口中的出现次数等于 0，那么从哈希表中删除 x==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['==入==：`x = nums[i]` 进入窗口，`s += x`，`cnt[x] += 1`；`i < k-1` 时继续入',
              '==更新==：如果 `len(cnt) ≥ m`，用 `s` 更新答案的最大值',
              '==出==：`nums[i-k+1]` 离开窗口，`s` 减少它、`cnt` 减一，减到 0 就删除'],
        result='运行结束，返回 `10`：窗口 `[2,5,3]`（`[1,5,2]` 和为 8，另两个窗口不同元素不足 3 个）',
        summary=['时间 `O(n)`，空间 `O(k)`：哈希表大小不超过窗口长度',
                 '易错：出现次数减到 0 ==一定要 `del`==，否则 `len(cnt)` 偏大',
                 '“入-更新-出”是灵神定长滑窗的通用套路（前置题 1456）',
                 '先更新答案再出窗口：更新时窗口恰好是 `[i-k+1, i]` 这 k 个数'],
    ),
)
