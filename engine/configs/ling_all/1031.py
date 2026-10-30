def _col(a_first):
    def f(S, i, v):
        if 'i' not in S:
            return None
        k = S['i']
        fl, sl = S['firstLen'], S['secondLen']
        if not a_first:
            fl, sl = sl, fl
        # 右边那段：[k - sl, k)；左边新加入的段：[k - sl - fl, k - sl)
        if k - sl <= i < k:
            return 'pink'
        if k - sl - fl <= i < k - sl:
            return 'blue'
        return None
    return f


def _dim(a_first):
    def f(S, i, v):
        if 'i' not in S:
            return False
        fl, sl = S['firstLen'], S['secondLen']
        if not a_first:
            fl, sl = sl, fl
        return i >= S['i']
    return f


def _txt(S):
    if 'i' not in S:
        return '`s[i]` = 前 i 个数的和；区间 `[l, r)` 的和 = `s[r] − s[l]`'
    i, s, fl, sl = S['i'], S['s'], S['firstLen'], S['secondLen']
    a = S['maxSumA'] + s[i] - s[i - sl]
    b = S['maxSumB'] + s[i] - s[i - fl]
    return f'i = {i}：左a右b 候选 `{S["maxSumA"]} + {s[i] - s[i - sl]}` = =={a}==；左b右a 候选 `{S["maxSumB"]} + {s[i] - s[i - fl]}` = =={b}=='


def _ans(S, B, ret):
    i, s, fl, sl = S.i, S.s, S.firstLen, S.secondLen
    a = S.maxSumA + s[i] - s[i - sl]
    b = S.maxSumB + s[i] - s[i - fl]
    if S.ans > B.ans:
        return f'两种候选 `{a}`、`{b}` 中较大的超过了旧答案 `{B.ans}` → `ans` 更新为 =={S.ans}=='
    return f'候选 `{a}`、`{b}` 都不超过 `{B.ans}`，`ans` 不变'


CONFIG = dict(
    num=1031, title='两个无重叠子数组的最大和', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 · 枚举右，维护左',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1680'],
    code='''
class Solution:
    def maxSumTwoNoOverlap(self, nums: List[int], firstLen: int, secondLen: int) -> int:
        s = list(accumulate(nums, initial=0))  # nums 的前缀和
        ans = maxSumA = maxSumB = 0
        for i in range(firstLen + secondLen, len(s)):
            maxSumA = max(maxSumA, s[i - secondLen] - s[i - firstLen - secondLen])
            maxSumB = max(maxSumB, s[i - firstLen] - s[i - firstLen - secondLen])
            ans = max(ans, maxSumA + s[i] - s[i - secondLen], maxSumB + s[i] - s[i - firstLen])
        return ans
''',
    call='Solution().maxSumTwoNoOverlap([0,6,5,2,2,5,1,9,4], 1, 2)',
    expect=20,
    views=[
        dict(type='array', var='nums', label='左 a 右 b：蓝 = 新加入的 a（长 firstLen），粉 = 当前 b（长 secondLen）',
             color=_col(True), dim=_dim(True), h=170),
        dict(type='array', var='nums', label='左 b 右 a：蓝 = 新加入的 b，粉 = 当前 a',
             color=_col(False), dim=_dim(False), h=170),
        dict(type='array', var='s', label='前缀和 s（s[i] 是右段的右开端点）', pointers={'i': 'pink'}, cell=76, h=190),
        dict(type='text', fn=_txt, size=28, h=90),
    ],
    watch=[('i', 'i', 'pink'), ('maxSumA', 'maxSumA', 'blue'), ('maxSumB', 'maxSumB', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        's = list(': '前缀和 `s = {s}`，任意区间和都能 `O(1)` 算出',
        'ans = maxSumA': '`maxSumA`：右段左边==最大的 a 段和==；`maxSumB` 同理',
        'for i in range': lambda S, B, ret: ((f'枚举右段的右开端点 `i = {S.i}`（从 `firstLen + secondLen` 开始，左边要留出空间）' if 'i' not in B
                                              else f'右段右移：`i = {S.i}`') if 'i' not in B or S.i != B.i else '枚举结束'),
        'maxSumA = max': lambda S, B, ret: (f'右段左边多出一个新的 a 段，和为 `{S.s[S.i - S.secondLen] - S.s[S.i - S.firstLen - S.secondLen]}`'
                                            + (f' → `maxSumA` 变成 =={S.maxSumA}==' if S.maxSumA != B.maxSumA else f'，不超过 `{S.maxSumA}`')),
        'maxSumB = max': lambda S, B, ret: (f'换个顺序：新的 b 段和为 `{S.s[S.i - S.firstLen] - S.s[S.i - S.firstLen - S.secondLen]}`'
                                            + (f' → `maxSumB` 变成 =={S.maxSumB}==' if S.maxSumB != B.maxSumB else f'，不超过 `{S.maxSumB}`')),
        'ans = max(ans': _ans,
        'return ans': '两段最大和为 =={ret}==',
    },
    cards=dict(
        one_liner='枚举右边那段，左边那段只需维护历史最大值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `nums` 中选两个==不重叠==的子数组，长度分别为 `firstLen`、`secondLen`',
                 '两段谁在左谁在右都可以，求两段元素和的最大值',
                 '示例：`[0,6,5,2,2,5,1,9,4]`，1 和 2 → `20`（`[9]` + `[6,5]`）'],
        quote='对于有两个变量的题目，通常可以==枚举其中一个变量，把它视作常量==，从而转化成只有一个变量的问题。对于本题来说，就是枚举 b，把问题转化成计算 a 的最大元素和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设右段 b 为 `[i − secondLen, i)`，和为 `s[i] − s[i − secondLen]`',
              '每右移一次 i，b 左边就==多出一个==新的 a 段，用它更新 `maxSumA`',
              '「左 b 右 a」把两个长度交换即可，两种情况合并在同一个循环里'],
        summary=['时间 `O(n)`，空间 `O(n)`（前缀和数组）',
                 '`i` 从 `firstLen + secondLen` 开始，保证左边放得下另一段',
                 '易错：两种左右顺序都要算，不能只算一种',
                 '原写法封装 `f(firstLen, secondLen)` 调用两次，本视频用合并后的简化写法',
                 '同类题：2555. 两个线段获得的最多奖品'],
    ),
)
