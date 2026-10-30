def _pf(x):
    r, p = [], 2
    while p * p <= x:
        if x % p == 0:
            r.append(p)
            while x % p == 0:
                x //= p
        p += 1
    if x > 1:
        r.append(x)
    return r


def _wr(S):
    p, i = S.get('p'), S.get('index')
    if p is None or i is None or p - 1 < i:
        return None
    return p - 1


def _wl(S):
    p, i = S.get('p'), S.get('index')
    if p is None or i is None or p - 1 < i:
        return None
    return i


def _txt(S):
    if 'cnt' not in S or 'p' not in S:
        return '先用筛法预处理：`f[v]` = v 的所有质因子'
    return f"窗口内不同质因子 `len(cnt) = {len(S['cnt'])}`，上限 `k = {S['k']}`"


def _f_draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    cv.text((x0 + 18, y0 + 4), 'f[v]：v 的质因子表（筛出来的）', 24, T['muted'], bold=True)
    if not f:
        return
    n = len(f) - 2
    cell = min(130, (x1 - x0 - 40) / max(n, 1))
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    nums, p, v = S.get('nums'), S.get('p'), S.get('v')
    hot = nums[p] if (nums and p is not None and 'index' in S and p < len(nums)) else None
    for j in range(n):
        val = j + 2
        X = sx + j * cell
        on = (v == val and 'index' not in S) or hot == val
        cv.rect((X + 4, y0 + 50, X + cell - 4, y0 + 50 + 96), fill=T['panel2'] if 'panel2' in T else (30, 36, 46),
                outline=T['yellow'] if on else T['border'], width=3 if on else 1, r=8)
        cv.text((X + cell / 2, y0 + 62), f'f[{val}]', 22, T['yellow'] if on else T['muted'], anchor='mt', mono=True)
        txt = ','.join(map(str, f[val])) or '—'
        cv.text((X + cell / 2, y0 + 108), txt, 30, T['text'], anchor='mt', bold=True)


CONFIG = dict(
    num=4032, title='至多 K 个不同质因数集合的最长子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='滑动窗口 · 筛法预处理质因子',
    tags=['滑动窗口与双指针', '数学算法', '难度分 1759'],
    code='''
class Solution(object):
    def longestSubarray(self, nums, k):
        
        ma = max(nums)
        f = [[] for _ in range(ma + 1)]

        v = 2
        while v <= ma:
            if not f[v]:
                for x in range(v, ma + 1, v):
                    f[x].append(v)
        
            v += 1
        
        cnt = {}
        p = 0
        res = 0
        for index in range(len(nums)):
            if p < index:
                p = index
                cnt = {}

            while p < len(nums):
                for x in f[nums[p]]:
                    cnt[x] = cnt.get(x, 0) + 1
                if len(cnt) > k:
                    for x in f[nums[p]]:
                        cnt[x] -= 1
                        if cnt[x] == 0:
                            cnt.pop(x)
                    break

                p += 1

            res = max(res, p - index)
            if p > index:
                for x in f[nums[index]]:
                    cnt[x] -= 1
                    if cnt[x] == 0:
                        cnt.pop(x)

        return res
''',
    call='Solution().longestSubarray([2,3,6,5], 2)',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [index, p)）', pointers={'index': 'pink', 'p': 'blue'},
             window=(_wl, _wr), h=230, cell=96),
        dict(type='custom', draw=_f_draw, h=170),
        dict(type='map', var='cnt', label='cnt：质因子 → 次数（键数 = 不同质因子数）', fmt=lambda k, v: f"{k}: {v}", h=130, font=30),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('v', 'v', 'yellow'), ('index', 'index', 'pink'), ('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'ma = max(nums)': '最大元素 `ma = {ma}`：只需预处理 2..ma 的质因子',
        'f = [[]': '`f[x]` 存 x 的质因子列表，先全部置空',
        'while v <= ma': '`v = {v}`：{"还在范围内，检查 v 是不是质数" if v <= ma else "筛完了"}',
        'if not f[v]': '`f[{v}]` {"为空 → 前面没有更小质数整除它，==它是质数==" if not f[v] else "非空 → 已被更小的质数筛过，是合数"}',
        'f[x].append(v)': '质数 `{v}` 是 `{x}` 的质因子',
        'v += 1': '`v` → {v}',
        'cnt = {}': '`cnt` 记窗口内每个质因子出现的次数',
        'if p < index': '`p = {p}`，`index = {index}`：{"右边界落到左边界后面了，窗口清空重来" if p < index else "p 没落后，沿用上一轮的窗口"}',
        'while p < len': '`p = {p}`：{"试着把 nums[p] 加进窗口" if p < len(nums) else "已到数组末尾"}',
        'cnt[x] = cnt.get': '`nums[{p}] = {nums[p]}` 的质因子 `{x}` 次数 → {cnt[x]}',
        'if len(cnt) > k': '`len(cnt) = {len(cnt)}`，`k = {k}`：{"质因子种数超标，这个数加不进来 → 撤销" if len(cnt) > k else "没超标，吸收成功"}',
        10: '把质数 `v` 追加到它所有倍数的质因子表里',
        28: '撤销：`{x}` 次数减一 → {cnt[x]}{"，降到 0 就要 pop" if cnt[x] == 0 else ""}',
        38: '移出：`{x}` 次数减一 → {cnt[x]}{"，降到 0 就要 pop" if cnt[x] == 0 else ""}',
        30: '`{x}` 次数为 0，从 `cnt` 删掉',
        40: '`{x}` 次数为 0，从 `cnt` 删掉',
        'break': '`nums[{p}]` 加不进去，右边界停在 `p = {p}`',
        'p += 1': '`p` → {p}',
        'res = max': '窗口长度 `p - index = {p - index}`，`res = max({B.res}, {p - index}) = {res}`',
        'if p > index': '窗口{"非空：把 nums[index] 移出去" if p > index else "是空的：没有可移出的"}',
        'return res': '最长合法子数组长度 `{res}`',
    },
    skip=['for x in f[nums[', 'for x in range(v', 'v += 1', 'p += 1', 'if p < index', 'if p > index', 'if cnt[x] == 0'],
    max_steps=140,
    cards=dict(
        one_liner='先筛出每个数的质因子，窗口里用哈希表记质因子次数',
        complexity='时间 `O(M log log M + n)`，`M = max(nums)`，空间 `O(M)`',
        problem=['给整数数组 `nums` 和 `k`，子数组的“质因数集合”是各元素不同质因子的并集',
                 '求最长的子数组，使质因数集合的大小不超过 `k`',
                 '本视频：`[2,3,6,5]`，`k=2` → `3`'],
        quote='数组中的元素不超过10^5，那么其可能拥有的质因数数量就不会超过6个……只需在最开始利用筛法预处理2到max(nums)中每个元素的质因子集。',
        quote_src='—— yiduobo 题解原文',
        idea=['`10^5` 以内的数最多 6 个质因子，所以加入/移出一个数都是常数次操作',
              '枚举左边界 `index`，右边界 `p` 先试探：加进去超标就撤销并停下',
              '`len(cnt)` 就是窗口里不同质因子数；次数减到 0 要 `pop`',
              '记录 `p - index` 后，再把 `nums[index]` 的质因子移出窗口'],
        summary=['时间 `O(M log log M + n)`，空间 `O(M)`',
                 '试探加入失败时必须把刚加的质因子撤销，再 `break`',
                 '`p < index` 时（单个数就超标）要把 `cnt` 清空、`p` 追到 `index`',
                 '原文已是可直接运行的写法，仅 `class Solution(object)` 保留原样',
                 '对比灵神：灵神是“先加入、超标再收缩”，yiduobo 是“先试探、超标就撤销”'],
    ),
)
