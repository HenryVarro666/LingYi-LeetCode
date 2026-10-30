NUMS, K = [3, 1, 3, 4, 3, 2, 3], 6
SORTED = sorted(NUMS)


def _pairs(S):
    """已配成对的下标（由 res 和指针推出：每配一次，两端各收进一个）"""
    if 'res' not in S or 'r' not in S:
        return set()
    out = set()
    l, r, n = 0, len(SORTED) - 1, 0
    need = S['res'] + (S.get('_line') in (11, 12))  # 正在收缩的这一对也算
    while l < r and n < need:
        s = SORTED[l] + SORTED[r]
        if s == K:
            out |= {l, r}
            l, r, n = l + 1, r - 1, n + 1
        elif s > K:
            r -= 1
        else:
            l += 1
    return out


def _live(S):
    return 'l' in S and 'r' in S and isinstance(S.get('nums'), list) and S['nums'] == SORTED


def _color(S, i, v):
    if not _live(S):
        return None
    if i in _pairs(S):
        return 'green'
    if i == S['l']:
        return 'blue'
    if i == S['r']:
        return 'pink'
    return None


def _dim(S, i, v):
    return _live(S) and not (S['l'] <= i <= S['r']) and i not in _pairs(S)


def _txt(S):
    if not _live(S):
        return '先排序，再像两数之和那样==相向双指针=='
    l, r = S['l'], S['r']
    if l >= r:
        return f"`l = {l} ≥ r = {r}`，指针相遇，共配成 `{S['res']}` 对"
    s = SORTED[l] + SORTED[r]
    rel = '==等于==' if s == K else ('大于' if s > K else '小于')
    return f"`nums[l] + nums[r] = {SORTED[l]} + {SORTED[r]} = {s}`，{rel} `k = {K}`"


def _cmp(S, B, r):
    s = S.s
    if s == S.k:
        return f'`s = {s} == k`：==配成一对==，两端同时收缩'
    return f'`s = {s} ≠ k`'


CONFIG = dict(
    num=1679, title='K 和数对的最大数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='排序 · 相向双指针',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1346'],
    code='''
class Solution(object):
    def maxOperations(self, nums, k):

        nums = sorted(nums)
        l = 0
        r = len(nums) - 1
        res = 0
        while l < r:
            s = nums[l] + nums[r]
            if s == k:
                l += 1
                r -= 1
                res += 1
            elif s > k:
                r -= 1
            else:
                l += 1

        return res
''',
    call=f'Solution().maxOperations({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=90, size=28),
        dict(type='array', var='nums', h=320, cell=110, pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'),
             color=_color, dim=_dim, label='nums（排序后；绿 = 已配对移出，暗 = 已丢弃）'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 's', 'k', ('res', 'res', 'green')],
    captions={
        'nums = sorted': '排序：`{nums}`，有序后才能用双指针',
        'l = 0': '`l` 指向最小的数',
        'r = len': '`r = {r}` 指向最大的数',
        'res = 0': '`res`：操作次数',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，继续' if S.l < S.r
                                        else f'`l = {S.l} ≥ r = {S.r}`：没有两个数可选了，结束'),
        's = nums[l] + nums[r]': '`s = {nums[l]} + {nums[r]} = {s}`',
        'if s == k': _cmp,
        11: '`{nums[l - 1]}` 用掉了：`l` → {l}',
        12: '`{nums[r + 1]}` 也用掉了：`r` → {r}',
        'res += 1': '操作次数 `res = {res}`',
        15: '`r` → {r}',
        17: '`{nums[l - 1]}` 和剩下谁配都不够 → ==丢掉它==，`l` → {l}',
        'elif s > k': lambda S, B, r: (f'`s = {S.s} > k`：最大的 `{S.nums[S.r]}` 配最小的都嫌大 → ==丢掉它=='
                                       if S.s > S.k else f'`s = {S.s} < k`：最小的数配最大的都不够'),
        'return res': '最多操作 =={res}== 次',
    },
    cards=dict(
        one_liner='排序后相向双指针：和小了左移，大了右移，相等就配对',
        complexity='时间 `O(n log n)`，空间 `O(n)`（排序副本）',
        problem=['每次从 `nums` 中选出==和为 k== 的两个数移出数组',
                 '求最多能执行多少次操作',
                 '示例：`[1,2,3,4], k = 5` → `2`；本视频 `[3,1,3,4,3,2,3], k = 6` → `3`'],
        quote='不说跟第一题一模一样，那也是大差不差的。直接照搬第一题的做法，==排序后双指针向中间扫描==就好了。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，`nums[l] + nums[r]` 与 `k` 比较',
              '`s > k`：`nums[r]` 和谁配都太大 → `r -= 1`；`s < k`：`nums[l]` 太小 → `l += 1`',
              '`s == k`：配成一对，两端同时收缩，`res += 1`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '`while l < r`：同一个数不能和自己配对',
                 '对比灵神：哈希表一趟 `O(n)`；双指针需要先排序',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未作改动'],
    ),
)
