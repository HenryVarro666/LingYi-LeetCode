NUMS, K = [1, 6, 1], 3
U = max(NUMS) - min(NUMS)
CANDS = list(range(U + 1))


END = set()   # for 循环结束那一步的 nums 快照 id（由字幕回调记录，字幕按步骤顺序各求值一次）


def _counting(S):
    return ('index' in S and 'p' in S and 'cnt' in S and S.get('_line') in (12, 13, 14, 16, 19)
            and id(S.get('nums')) not in END)


def _for_idx(S, B, ret):
    if 'index' not in B or B.index != S.index:
        return f'以 `nums[{S.index}] = {S.nums[S.index]}` 作为较小数'
    END.add(id(S.nums))
    return f'统计完：`cnt = {S.cnt}`'


def _cand_color(S, i, v):
    if 'l' not in S or 'r' not in S:
        return None
    if 'mid' in S and S.get('_line', 0) >= 9 and S.get('_line', 0) <= 19 and v == S['mid']:
        return 'yellow'
    if v < S['l']:
        return 'red'
    if v > S['r']:
        return 'blue'
    return None


def _nums_color(S, k, v):
    if not _counting(S):
        return None
    idx, p = S['index'], S['p']
    if k == idx:
        return 'blue'
    if idx < k < p:
        return 'cyan'
    return None


def _text(S):
    if 'l' not in S or 'r' not in S:
        return ''
    if _counting(S):
        idx, p = S['index'], S['p']
        return (f"二分到 `mid = {S['mid']}`：以 `nums[{idx}]` 为较小数、差 `≤ mid` 的有 `p − index − 1 = {max(0, p - idx - 1)}` 组，"
                f"`cnt = {S['cnt']}`")
    return f"答案在闭区间 `[{S['l']}, {S['r']}]` 里；红 = 已排除（太小），蓝 = 已排除（不是最小）"


def _while_p(S, B, ret):
    p, idx, n, mid = B.p, B.index, B.n, B.mid
    if p >= n:
        return '`p` 已经到末尾了'
    d = B.nums[p] - B.nums[idx]
    if d <= mid:
        return f'`nums[{p}] − nums[{idx}] = {d} ≤ mid = {mid}` → `p` 右移'
    return f'`nums[{p}] − nums[{idx}] = {d} > mid`：`p` 是第一个超出的'


def _if_p(S, B, ret):
    if S.p == S.index + 1:
        return (f'`p == index + 1`：以 `nums[{S.index}]` 为较小数的数对==一组都没有==；'
                f'下一轮 `p` 至少要从 `index + 2` 开始')
    return f'`p = {S.p}`：`nums[{S.index + 1}..{S.p - 1}]` 和 `nums[{S.index}]` 的差都 `≤ mid`'


CONFIG = dict(
    num=719, title='找出第 K 小的数对距离', difficulty='Hard', category='二分查找',
    author='yiduobo', technique='二分答案 + 双指针计数',
    tags=['字节30天'],
    code='''
class Solution(object):
    def smallestDistancePair(self, nums, k):
        nums = sorted(nums)
        n = len(nums)

        l = 0
        r = nums[-1] - nums[0]
        while l < r:
            mid = (l + r) >> 1
            p = 1
            cnt = 0
            for index in range(n - 1):
                while p < n and nums[p] - nums[index] <= mid:
                    p += 1

                if p == index + 1:
                    p += 1
                else:
                    cnt += p - index - 1

            if cnt >= k:
                r = mid
            else:
                l = mid + 1

        return l
''',
    call=f'Solution().smallestDistancePair({NUMS}, {K})',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=90),
        dict(type='array', var=lambda S: CANDS, label='答案候选（闭区间 [l, r]，黄 = mid）', cell=90, h=245,
             window=('l', 'r'), pointers={'l': 'red', 'r': 'blue', 'mid': 'yellow'}, color=_cand_color),
        dict(type='array', var='nums', label='nums（排序后；蓝 = index，青 = 和它差 ≤ mid 的 nums[index+1..p−1]）',
             cell=100, h=220, pointers={'index': 'blue', 'p': 'pink'}, color=_nums_color),
    ],
    watch=[('l', 'l', 'red'), ('r', 'r', 'blue'), ('mid', 'mid', 'yellow'), 'cnt', 'k'],
    captions={
        'nums = sorted(nums)': '先排序：`nums = {nums}`',
        'l = 0': '距离的下界是 `0`',
        'r = nums[-1] - nums[0]': '上界是最大差 `r = {r}`：答案在 `[l, r]` 里，==二分答案==',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}` → 继续二分' if B.l < B.r else f'`l == r = {B.l}`：答案确定'),
        'mid = (l + r) >> 1': '`mid = ({l} + {r}) >> 1 = {mid}`：数一数距离 `≤ {mid}` 的数对有多少',
        'p = 1': '`p`：第一个满足 `nums[p] − nums[index] > mid` 的位置',
        'cnt = 0': '`cnt` 统计距离 `≤ mid` 的数对',
        'for index in range(n - 1)': _for_idx,
        'while p < n and': _while_p,
        14: '`p` → `{p}`',
        'if p == index + 1': _if_p,
        17: '`p += 1` → `{p}`',
        'cnt += p - index - 1': '`cnt += {p} − {index} − 1` → `{cnt}`；下一个 index ==p 不用回退==',
        'if cnt >= k': lambda S, B, r: (f'`cnt = {S.cnt} ≥ k = {S.k}` → 答案 `≤ mid`' if S.cnt >= S.k
                                        else f'`cnt = {S.cnt} < k = {S.k}` → 距离 `≤ mid` 的不够 k 个，答案 `> mid`'),
        'r = mid': '`r = mid = {r}`',
        'l = mid + 1': '`l = mid + 1 = {l}`',
        'return l': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='二分答案 mid，数一数距离 ≤ mid 的数对是否够 k 个',
        complexity='时间 `O(n log n + n log(max_diff))`，空间 `O(1)`',
        problem=['数对 `(nums[i], nums[j])`（`i < j`）的距离 = 两数之差的绝对值',
                 '返回所有数对距离中==第 k 小==的那个',
                 '示例：`nums = [1,3,1], k = 1` → `0`',
                 '示例（本视频）：`nums = [1,6,1], k = 3` → `5`'],
        quote='因此我们可以==二分答案==，对于当前二分到的mid，检查所有距离对中有多少个小于等于mid，这一步在对nums排序后，可以在O(n)的时间复杂度完成。',
        quote_src='—— yiduobo 题解',
        idea=['`p` = 第一个差 `> mid` 的位置 → 以 `nums[index]` 为较小数的有 `p − index − 1` 组',
              '`nums[index+1] ≥ nums[index]`：对 index 满足的，对 index+1 也满足 → ==p 只往后走==',
              '`cnt ≥ k` 则 `r = mid`，否则 `l = mid + 1`'],
        summary=['时间 `O(n log n + n log(max_diff))`：`index` 和 `p` 每轮都只遍历一次',
                 '易错：`p == index + 1` 时要 `p += 1`，保证 `p` 在 `index` 的右边',
                 '最朴素是 `O(n²)` 枚举所有数对，会超时',
                 '对比灵神：灵神枚举右端点 `j`、开区间二分；yiduobo 枚举较小数、闭区间 `[l, r]`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（`>> 1` 本身就是整除）'],
    ),
)
