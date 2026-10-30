NUMS = [0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
K = 2


def _phase(S):
    return 'bound' in S


def _ncolor(S, i, v):
    if 'r' in S and 'one' in S:
        if i < S['l'] or i > S['r']:
            return None  # 头尾的 0
        return 'green' if v == 1 else 'orange'
    return 'green' if v == 1 else None


def _ndim(S, i, v):
    if 'r' in S and 'one' in S:
        return i < S['l'] or i > S['r']
    if 'r' in S:
        return i > S['r']
    if 'l' in S:
        return i < S['l']
    return False


def _npointers(S):
    return {} if _phase(S) else {'l': 'blue', 'r': 'pink', 'p': 'yellow'}


def _ocolor(S, i, v):
    if 'bound' not in S:
        return None
    b, idx = S['bound'], S.get('index', 0)
    if b <= i <= idx:
        return 'green'
    return None


def _zcolor(S, i, v):
    if 'bound' not in S:
        return None
    b, idx = S['bound'], S.get('index', 0)
    if b <= i < idx - 1 or (b <= i == idx - 1 and S['_line'] in (54, 59)):
        return 'orange'
    return None


def _top(S):
    if 'one' not in S:
        if 'r' in S:
            return f"去掉头部 `{S['l']}` 个 0、尾部 `{len(NUMS) - 1 - S['r']}` 个 0，中间交替统计各段 1 / 0 的长度"
        return f'`k = {K}`：头尾的 0 先不管，只看中间 ==1 段与 0 段交替==的部分'
    if 'bound' not in S:
        if 's0' in S:
            return f"中间 0 的总数 `s0 = {S['s0']}`，头尾 0 共 `{S['l'] + len(NUMS) - 1 - S['r']}` 个，`k = {S['k']}`"
        return f"one = `{S['one']}`　zero = `{S.get('zero', [])}`"
    b, idx = S['bound'], S.get('index', 0)
    return f"窗口：第 `{b}`..`{idx}` 段 1，共 `now = {S['now']}` 个 1；剩余额度 `k = {S['k']}`；最好 `res1 = {S['res1']}`"


def _while_b(S, B, ret):
    if S.bound < S.index - 1 and S.k < S.zero[S.index - 1]:
        return f'额度 `k = {S.k}` < 要跨过的 `zero[{S.index - 1}] = {S.zero[S.index - 1]}` → ==回收最左边一段=='
    if S.k >= S.zero[S.index - 1]:
        return f'额度 `k = {S.k}` ≥ `zero[{S.index - 1}] = {S.zero[S.index - 1]}`，够用了'
    return f'`bound = {S.bound}` 已紧挨 `index`，没有可回收的段了'


def _if_k(S, B, ret):
    z = S.zero[S.index - 1]
    if S.k >= z:
        return f'`k = {S.k} ≥ {z}`：能把中间这 {z} 个 0 填成 1 → ==r 右移到第 {S.index} 段=='
    return f'`k = {S.k} < {z}`：连这一段 0 都填不满 → 窗口从第 {S.index} 段重新开始'


def _ret(S, B, ret):
    return f'剩下的额度一定能用在窗口两侧的 0 上：答案 `res0 + res1 = {S.res0} + {S.res1}` = =={ret}=='


CONFIG = dict(
    num=1004, title='最大连续1的个数 III', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按段压缩 + 滑动窗口',
    tags=['labuladong', '灵神核心路线', '难度分 1656'],
    code='''
class Solution(object):
    def longestOnes(self, nums, k):

        n = len(nums)
        l = 0
        while l < n and nums[l] == 0:
            l += 1
        
        if l == n:
            return k
        
        r = n - 1
        while r >= 0 and nums[r] == 0:
            r -= 1
        
        p = l
        while p + 1 <= r and nums[p + 1] == 1:
            p += 1
        
        one = [p - l + 1]
        zero = []
        p += 1
        while p <= r:
            last_p = p
            while p + 1 <= r and nums[p + 1] == 0:
                p += 1
            zero.append(p - last_p + 1)
            p += 1

            last_p = p
            while p + 1 <= r and nums[p + 1] == 1:
                p += 1
            one.append(p - last_p + 1)
            p += 1
        
        s0 = sum(zero)
        if s0 + l + n - 1 - r <= k:
            return n
        elif s0 <= k:
            return r - l + 1 + s0 - k
        else:
            bound = 0
            now = one[0]
            res0 = k
            res1 = now

            for index in range(1, len(one)):
                while bound < index - 1 and k < zero[index - 1]:
                    k += zero[bound]
                    now -= one[bound]
                    bound += 1
                if k >= zero[index - 1]:
                    now += one[index]
                    k -= zero[index - 1]
                else:
                    now = one[index]
                    bound = index

                res1 = max(res1, now)
            
            return res0 + res1
''',
    call=f'Solution().longestOnes({NUMS}, {K})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var='nums', label='nums（暗 = 头尾的 0；绿 = 1，橙 = 中间的 0）',
             pointers={'l': 'blue', 'r': 'pink', 'p': 'yellow'}, color=_ncolor, dim=_ndim, h=230),
        dict(type='array', var=lambda S: S.get('one', []), label='one：各段 1 的长度（绿 = 当前窗口里的段）',
             pointers={'bound': 'blue', 'index': 'pink'}, color=_ocolor, cell=80, h=190),
        dict(type='array', var=lambda S: S.get('zero', []), label='zero：相邻两段 1 之间 0 的个数（橙 = 已用额度填上）',
             color=_zcolor, cell=80, h=170),
    ],
    watch=[('k', 'k', 'orange'), ('now', 'now', 'green'), ('res1', 'res1', 'purple'), 's0'],
    captions={
        'n = len': '`n = {n}`',
        'l = 0': '先跳过头部的 0',
        'while l < n and': lambda S, B, r: (f'`nums[{S.l}] = 0`，是头部的 0' if S.l < S.n and S.nums[S.l] == 0
                                            else f'`nums[{S.l}] = 1`：第一个 1 在下标 =={S.l}=='),
        'l += 1': '`l` → {l}',
        'if l == n': '数组里有 1，不是全 0 的特殊情况',
        'r = n - 1': '再从右往左跳过尾部的 0',
        'while r >= 0 and': lambda S, B, r: (f'`nums[{S.r}] = 0`，是尾部的 0' if S.nums[S.r] == 0
                                             else f'`nums[{S.r}] = 1`：最后一个 1 在下标 =={S.r}=='),
        'r -= 1': '`r` → {r}',
        'p = l': '`p` 从第一个 1 出发，数出第一段 1',
        'while p + 1 <= r and nums[p + 1] == 1': lambda S, B, r: (
            f'`nums[{S.p + 1}] = 1`，这一段 1 还没完' if S.p + 1 <= S.r and S.nums[S.p + 1] == 1 else f'这一段 1 到下标 {S.p} 结束'),
        'while p + 1 <= r and nums[p + 1] == 0': lambda S, B, r: (
            f'`nums[{S.p + 1}] = 0`，这一段 0 还没完' if S.p + 1 <= S.r and S.nums[S.p + 1] == 0 else f'这一段 0 到下标 {S.p} 结束'),
        'one = [p - l + 1]': '第一段 1 的长度 `{p} − {l} + 1 = {one[0]}`',
        'zero = []': '`zero` 存相邻两段 1 之间 0 的个数',
        'while p <= r': lambda S, B, r: ('还没扫到 r，继续交替统计 0 段和 1 段' if S.p <= S.r else '中间部分统计完毕'),
        'zero.append': '这一段 0 有 `{zero[-1]}` 个 → `zero = {zero}`',
        'one.append': '这一段 1 有 `{one[-1]}` 个 → `one = {one}`',
        's0 = sum': '中间 0 的总数 `s0 = {s0}`',
        'if s0 + l + n - 1 - r <= k': lambda S, B, r: (
            f'全部 0 共 `{S.s0} + {S.l} + {S.n - 1 - S.r}` 个 > `k = {S.k}`：不能全翻'),
        'elif s0 <= k': '`s0 = {s0} > k = {k}`：中间的 0 都填不完 → ==需要滑动窗口==',
        'bound = 0': '`bound`：窗口里最左边一段 1 的编号',
        'now = one[0]': '窗口先只含第 0 段 1：`now = {now}`',
        'res0 = k': '`res0 = k = {res0}`：额度最终都会用掉，答案 = 窗口里 1 的个数 + k',
        'res1 = now': '`res1`：窗口里 1 的个数的最大值',
        'for index in': lambda S, B, r: ('所有段都试过了' if 'index' in B and B.index == S.index
                                        else f'尝试把窗口右边界扩到第 `{S.index}` 段 1，要跨过 `zero[{S.index - 1}] = {S.zero[S.index - 1]}` 个 0'),
        'while bound < index - 1': _while_b,
        'k += zero[bound]': '退还 `zero[{B.bound}]` 的额度：`k = {k}`',
        'now -= one[bound]': '第 {bound} 段 1 移出窗口：`now = {now}`',
        'p += 1': '`p` → {p}',
        'bound += 1': '`bound` → {bound}',
        'if k >= zero[index - 1]': _if_k,
        'now += one[index]': '连上第 {index} 段：`now = {B.now} + {one[index]} = {now}`',
        'k -= zero[index - 1]': '用掉 `{zero[index - 1]}` 个额度：`k = {k}`',
        'now = one[index]': '`now = {now}`',
        'bound = index': '`bound` → {bound}',
        'res1 = max': '`res1 = max({B.res1}, {now}) = {res1}`',
        'return res0 + res1': _ret,
    },
    skip=['last_p = p'],
    max_steps=80,
    cards=dict(
        one_liner='把数组压缩成「1 段 / 0 段」，在段上滑窗：额度不够就回收最左一段',
        complexity='时间 `O(n)`，空间 `O(n)`（段数组）',
        problem=['二进制数组 `nums`，最多可以把 `k` 个 0 翻成 1',
                 '求翻转后==连续 1 的最长长度==',
                 '示例：`[1,1,1,0,0,0,1,1,1,1,0], k = 2` → `6`',
                 '本视频：`[0,1,1,0,0,1,0,1,1,0], k = 2` → `5`'],
        quote='一个直观的想法就是==优先填满各段1之间的0==，然后再去填充头部和尾部这两段0。于是我们可以先分别求得各段0和1的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['全部 0 都能翻 → `n`；中间的 0 能翻完 → 1 连成一串，余额填头尾',
              '否则在段上滑窗：`r` 每次跨过一段 0；额度不够，==l 右移并回收它后面那段 0==',
              '额度最终都能用掉，答案 = `k` + 窗口里 1 的个数的最大值'],
        summary=['时间 `O(n)`，空间 `O(n)` 存段长',
                 '头尾的 0 不参与滑窗：s0 > k 时额度一定能全部用上',
                 '易错：回收时 `k += zero[bound]` 退还的是 bound 段==后面==那段 0',
                 '更短的写法：直接按下标滑窗，维护窗口内 0 的个数 `cnt0 ≤ k`',
                 '原文为 Python 2 风格，代码无需修改'],
    ),
)
