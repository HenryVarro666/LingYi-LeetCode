NUMS = [2, 4, 1, 3]
M = 2


def _ncolor(S, i, v):
    # 扫描中：已经扫过的数按所在子数组交替染色，当前 num 黄色
    if 'mid' not in S or 'num' not in S or S['_line'] not in range(11, 18):
        return None
    idx = NUMS.index(S['num'])
    if i > idx:
        return None
    cnt, now, seg = 1, 0, []
    for x in NUMS[:idx + 1]:
        if now + x <= S['mid']:
            now += x
        else:
            cnt += 1
            now = x
        seg.append(cnt)
    if i == idx and S['_line'] in (11, 12):
        return 'yellow'
    return 'cyan' if seg[i] % 2 else 'purple'


def _top(S):
    if 'l' not in S:
        return f'`m = {M}`：二分答案 + 贪心'
    if 'mid' in S and S['_line'] in range(10, 19):
        return f"设答案为 `mid = {S['mid']}`：第 `{S['cnt']}` 个子数组当前和 `now = {S['now']}`"
    if S['l'] < S['r']:
        return f"答案在 `[{S['l']}, {S['r']}]` 里"
    return f"`l == r = {S['l']}`：就是答案"


def _cand(S, i, v):
    if 'l' not in S:
        return None
    if v < S['l']:
        return 'red'
    if v > S['r']:
        return 'green'
    return None


def _add(S, B, ret):
    if S.now + S.num <= S.mid:
        return f'`now + num = {S.now} + {S.num} = {S.now + S.num} ≤ {S.mid}`：==尽可能多地==加入当前子数组'
    return f'`now + num = {S.now} + {S.num} = {S.now + S.num} > {S.mid}`：加不进去 → 另起新的子数组'


def _cmp(S, B, ret):
    if S.cnt <= S.m:
        return f'划分出 `cnt = {S.cnt} ≤ m = {S.m}` 个：最大值 ≤ {S.mid} 可以做到 → 答案 ==≤ {S.mid}=='
    return f'划分出 `cnt = {S.cnt} > m = {S.m}` 个：{S.mid} 太小 → 答案 ==> {S.mid}=='


CONFIG = dict(
    num=410, title='分割数组的最大值', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 + 贪心一趟扫描',
    tags=['labuladong', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def splitArray(self, nums, m):

        l = max(nums)
        r = sum(nums)

        while l < r:
            mid = (l + r) // 2
            cnt = 1
            now = 0
            for num in nums:
                if now + num <= mid:
                    now += num
                else:
                    cnt += 1
                    now = num
            if cnt <= m:
                r = mid
            else:
                l = mid + 1

        return l
''',
    call=f'Solution().splitArray({NUMS}, {M})',
    expect=6,
    views=[
        dict(type='text', fn=_top, size=27, h=80),
        dict(type='array', var=lambda S: list(range(sum(NUMS) + 1)),
             label='候选答案（红 = 已排除，绿 = 可行但更大；暗 = 小于 max(nums)）', cell=72, index=False,
             dim=lambda S, i, v: v < max(NUMS), color=_cand,
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'}, h=240),
        dict(type='array', var='nums', label='nums（黄 = 当前 num；青 / 紫 = 贪心划分出的子数组）',
             cell=110, h=200, color=_ncolor),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'purple'),
           ('now', 'now', 'cyan'), 'num', 'm'],
    captions={
        'l = max': '下界 `l = max(nums) = {l}`：每个子数组至少要装下最大的数',
        'r = sum': '上界 `r = sum(nums) = {r}`：整个数组一段',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，继续二分' if S.l < S.r else f'`l == r = {S.l}`，结束'),
        'mid = (l + r)': '设答案为 `mid = ({l} + {r}) // 2 = {mid}`，从头开始划分',
        'cnt = 1': '`cnt`：子数组个数，先开一个',
        'now = 0': '`now`：当前子数组的和',
        'for num in': lambda S, B, r: ('扫描完毕' if 'num' in B and B.num == S.num else f'`num = {S.num}`'),
        'if now + num <= mid': _add,
        'now += num': '`now = {now}`',
        'cnt += 1': '新子数组：`cnt = {cnt}`',
        'now = num': '新子数组从 `{num}` 开始：`now = {now}`',
        'if cnt <= m': _cmp,
        'r = mid': '`r` → {r}',
        'l = mid + 1': '`l` → {l}',
        'return l': '最小的最大值 =={ret}==',
    },
    cards=dict(
        one_liner='数都非负：和 ≤ k 的一段拆开后每段仍 ≤ k → 二分答案、贪心验证',
        complexity='时间 `O(n log(sum − max))`，空间 `O(1)`',
        problem=['把非负整数数组 `nums` 分成 `m` 个非空连续子数组',
                 '让各子数组和的==最大值最小==',
                 '示例：`[7,2,5,10,8], m = 2` → `18`；本视频 `[2,4,1,3], m = 2` → `6`'],
        quote='设答案为k，然后从数组的头部开始进行划分。每次都==尽可能多地将数加入到当前的子数组中==，如果无法加入则另起新的子数组。这样划分完毕之后，如果划分出来的子数组数量小于等于m，说明存在某种划分方式使得各个子数组最大值小于等于k。',
        quote_src='—— yiduobo 题解原文',
        idea=['直观想法是 DP：`f[i][j]` 前 i 个数分 j 段，`O(n²m)`',
              '数都非负 → 一段和 ≤ k，拆开后每段仍 ≤ k：==段数可以只少不多==',
              '二分 `k ∈ [max, sum]`，贪心划分一趟，段数 ≤ m 就收缩右界'],
        summary=['时间 `O(n log(sum − max))`，空间 `O(1)`',
                 '下界取 `max(nums)`：否则单个数都放不下',
                 '`cnt <= m` 而不是 `== m`：段少了可以再拆',
                 '原文为 Python 2 写法，`(l + r) / 2` 已改为 `(l + r) // 2`'],
    ),
)
