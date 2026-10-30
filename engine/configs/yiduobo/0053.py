NUMS = [-2, 1, -3, 4, -1, 2, 1, -5, 4]


def _sim():
    """按 yiduobo 的规则预先算出每一步之后的 (段起点, now, 最优段)，只用于画图"""
    out, now, st, res, best = [], 0, 0, 0, None
    for i, x in enumerate(NUMS):
        if now + x < 0:
            now, st = 0, i + 1
        else:
            now += x
            if now > res:
                res, best = now, (st, i)
        out.append((st, now, res, best))
    return out


SIM = _sim()


def _seg(S):
    """当前 now 对应的子段 [st, ed]（now 为 0 时没有）"""
    i, now = S.get('index'), S.get('now')
    if i is None or not now:
        return None
    for e in (i, i - 1):
        if e >= 0 and SIM[e][1] == now and SIM[e][0] <= e:
            return SIM[e][0], e
    return None


def _best(S):
    i, res = S.get('index'), S.get('res')
    if i is None or not res:
        return None
    for e in (i, i - 1):
        if e >= 0 and SIM[e][2] == res and SIM[e][3]:
            return SIM[e][3]
    return None


def _done(S):
    """已经算出 f[i] 的个数（now 刚变成 f[index] 时算上 index）"""
    i, now = S.get('index'), S.get('now')
    if i is None:
        return 0
    prev = SIM[i - 1][1] if i > 0 else 0
    return i + 1 if now == SIM[i][1] and now != prev else i


def _f(S):
    return [SIM[e][1] for e in range(_done(S))] if 'now' in S else None


def _color(S, i, v):
    b = _best(S)
    return 'green' if b and b[0] <= i <= b[1] else None


def _info(S):
    if 'now' not in S:
        return ''
    seg = _seg(S)
    part = f'`nums[{seg[0]}..{seg[1]}]`' if seg else '空（被截成 0）'
    return f'当前子序和 `now = {S["now"]}`：{part}　　最大 `res = {S.get("res", 0)}`（绿色那段）'


CONFIG = dict(
    num=53, title='最大子数组和', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='动态规划 / 贪心（负数就清零）',
    code='''
class Solution(object):
    def maxSubArray(self, nums):
        if max(nums) < 0:
            return max(nums)

        res = 0
        now = 0
        for index, num in enumerate(nums):
            if now + num < 0:
                now = 0
            else:
                now += num
                res = max(res, now)

        return res
''',
    call=f'Solution().maxSubArray({NUMS})',
    expect=6,
    views=[
        dict(type='text', fn=_info),
        dict(type='array', var='nums', label='nums', pointers={'index': 'pink'},
             window=(lambda S: _seg(S)[0] if _seg(S) else None, lambda S: _seg(S)[1] if _seg(S) else None),
             color=_color, cell=96, h=230),
        dict(type='array', var=_f, label='f[i]：以 nums[i] 结束的最大子序和（清零记为 0）；上方框 = now 对应的子段', min_slots=9, cell=96, h=200,
             color=lambda S, i, v: 'cyan' if i == _done(S) - 1 else None, dim=lambda S, i, v: v == 0),
    ],
    watch=[('index', 'index', 'pink'), 'num', ('now', 'now', 'cyan'), ('res', 'res', 'orange')],
    captions={
        'if max(nums) < 0': lambda S, B, ret: (f'`max(nums) = {max(S.nums)}` < 0：全是负数，答案就是最大的那个数' if max(S.nums) < 0
                                               else f'`max(nums) = {max(S.nums)}` ≥ 0：有非负数，==答案至少是 0==，下面放心从 0 开始'),
        'res = 0': '`res` 记录最大的 `f[i]`，从 0 开始',
        'now = 0': lambda S, B, ret: ('`now` 就是 `f[i-1]`：只用一个变量维护当前的子序和' if 'index' not in S
                                      else f'`now` 清零：从 `nums[{S.index + 1}]` 重新开始'),
        'for index, num': lambda S, B, ret: (f'看 `nums[{S.index}] = {S.num}`' if 'index' not in B or S.index != B.index else '扫描结束'),
        'if now + num < 0': lambda S, B, ret: (
            f'`now + num = {B.now} + ({B.num}) = {B.now + B.num}` < 0：==前面这个子序列还不如不要=='
            if B.now + B.num < 0 else
            f'`now + num = {B.now} + ({B.num}) = {B.now + B.num}` ≥ 0：接在后面'),
        'now += num': '`now = {now}`：以 `nums[{index}]` 结束的最大子序和 `f[{index}]`',
        'res = max': '取最大的 `f[i]`：`res = max({B.res}, {now}) = {res}`',
        'return res': '最大子序和 =={ret}==',
    },
    cards=dict(
        one_liner='前面的子序和一旦变成负数，就整段扔掉，从 0 重新开始',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找出和最大的==连续子数组==（至少含一个元素），返回它的和',
                 '示例：`nums = [-2,1,-3,4,-1,2,1,-5,4]` → `6`（子数组 `[4,-1,2,1]`）'],
        quote='若f[i - 1] + nums[i]小于0，那么说明前面这个子序列还不如不要，直接从0开始，即f[i] = 0；否则有f[i] = f[i - 1] + nums[i]。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案 = 最大的 `f[i]`；`f[i]` 只用到 `f[i-1]` → ==一个变量 now 就够了==',
              '和变负就清零：负数前缀接在任何子数组前面都只会让它变小',
              '全是负数时 `f` 全被清成 0 → ==先特判：答案就是最大的那个数=='],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '特判 `max(nums) < 0` 不能少：否则全负数组会错误地返回 0',
                 '`res` 只在 `now += num` 之后更新，初值 0 是安全的（已保证有非负数）',
                 '原文吐槽进阶的分治法：`O(n log n)`「相比 O(n) 的贪心法，感觉并不见得哪里精妙了」',
                 '原文代码可直接在 Python 3 运行，只删去了 docstring'],
    ),
)
