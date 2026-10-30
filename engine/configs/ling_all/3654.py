def _idx(S):
    if 'x' in S and S['x'] in S['nums']:
        return S['nums'].index(S['x'])
    return None


def _mf(S):
    return S['min_f'] if 'min_f' in S else [0] * 4


def _mfcolor(S, i, v):
    if 's' in S and 'f' in S and i == S['s'] and S.get('x') is not None and S.get('_line', 0) >= 16:
        return 'green'
    if 's' in S and i == S['s']:
        return 'yellow'
    return None


def _text(S):
    if 'x' not in S or 'f' not in S:
        return '`f` = 当前前缀删完后的最小和；`min_f[s]` = 前缀和模 k 为 s 的所有位置里，最小的 f'
    k = len(S['min_f'])
    return f"当前 `x = {S['x']}`，前缀和模 k 得 ==s {S['s']}==；`f = min(不删, 删到 min_f[{S['s']}])`"


CONFIG = dict(
    num=3654, title='删除可整除和后的最小数组和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前缀和模 k + 线性 DP（数组实现）',
    tags=['灵神题单', '动态规划', '难度分 2039'],
    code='''
# 手写 min 更快
min = lambda a, b: b if b < a else a

class Solution:
    def minArraySum(self, nums: list[int], k: int) -> int:
        min_f = [inf] * k
        min_f[0] = 0  # s[0] = 0，对应的 f[0] = 0
        f = s = 0
        for x in nums:
            s = (s + x) % k
            # 不删除 x，那么转移来源为 f + x
            # 删除以 x 结尾的子数组，问题变成剩余前缀的最小和
            # 其中剩余前缀的元素和模 k 等于 s，对应的 f 值的最小值记录在 min_f[s] 中
            f = min(f + x, min_f[s])
            # 维护前缀和 s 对应的最小和，由于上面计算了 min，这里无需再计算 min
            min_f[s] = f
        return f
''',
    call='Solution().minArraySum([3,1,4,2,5], 4)',
    expect=3,
    skip=['min = lambda'],
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='array', var='nums', pointers={'nums.index(x)': 'blue'}, label='nums', h=190,
             color=lambda S, i, v: 'blue' if _idx(S) == i else None,
             dim=lambda S, i, v: _idx(S) is not None and i < _idx(S)),
        dict(type='array', var='min_f', label='min_f[s]：模 k 为 s 的最小 f', h=190,
             pointers={'s': 'pink'}, color=_mfcolor),
    ],
    watch=[('x', 'x', 'blue'), ('s', 's', 'pink'), ('f', 'f', 'green')],
    captions={
        'min_f = [inf]': '`min_f` 长 `k = {k}`，每个余数先记为 `inf`（还没出现过）',
        'min_f[0] = 0': '空前缀：和为 0、模 k 余 0、`f[0] = 0`，所以 `min_f[0] = 0`',
        'f = s = 0': '`f` 是当前前缀的最小和，`s` 是前缀和模 k',
        'for x in nums': lambda S, B, r: ('数组处理完了，退出循环' if B.get('x') == S.get('x') else f"依次处理 `x = {S['x']}`"),
        's = (s + x)': '前缀和边加边取模：`s = ({B.s} + {x}) % {k}` = =={s}==',
        'f = min(': '不删 `x`：`{B.f} + {x} = {B.f + x}`；删以 `x` 结尾的子数组：转移到 `min_f[{s}] = {min_f[s]}`。取小 → `f` = =={f}==',
        'min_f[s] = f': '余数 `{s}` 的最小 f 更新为 `{f}`（上一行已取过 min，直接赋值即可）',
        'return f': '整个数组的最小和 `{f}`',
    },
    cards=dict(
        one_liner='和为 k 的倍数 = 前缀和模 k 相同，用 min_f 记下每个余数的最优 f',
        complexity='时间 `O(n + k)`，空间 `O(k)`',
        problem=['每次可删一段和为 `k` 的倍数的连续子数组，删后两边接上',
                 '求任意次删除后，数组剩余元素和的最小值',
                 '示例：`[1,1,1], k=2` → `1`；本视频：`[3,1,4,2,5], k=4` → `3`'],
        quote='如果 a 的元素和是 k 的倍数，且删除的更内部的子数组元素和也是 k 的倍数，那么删除更内部元素后，a 的剩余元素之和是不变的，仍然为 k 的倍数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先证明：内层先删不影响外层能删，所以只需==考虑最右边的那段删除==',
              '`f[i+1] = min(f[i] + nums[i], min_f[sum[i+1]])`：不删，或删到余数相同的某个前缀',
              '`sum` 和 `f` 都只用上一个值，压成变量，只留 `min_f` 数组'],
        summary=['时间 `O(n + k)`，空间 `O(k)`',
                 '易错：贪心地删最近/最远相同前缀和是错的，两段相交时无法判断删谁，必须 DP',
                 '边加边取模没问题，`min_f[0] = 0` 对应空前缀',
                 '灵神还给了哈希表写法 `defaultdict(lambda: inf)`，k 很大时更省空间'],
    ),
)
