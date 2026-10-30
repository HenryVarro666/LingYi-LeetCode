def _pre(S):
    return S.get('i') if 'pre_sum' in S else None


CONFIG = dict(
    num=3811, title='交替按位异或分割的数目', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前缀异或 + 两个哈希表 DP',
    tags=['灵神题单', '动态规划', '难度分 2006'],
    code='''
class Solution:
    def alternatingXOR(self, nums: List[int], target1: int, target2: int) -> int:
        MOD = 1_000_000_007
        f1 = defaultdict(int)
        f2 = defaultdict(int)
        f2[0] = 1
        pre_sum = 0
        for i, x in enumerate(nums):
            pre_sum ^= x
            last1 = f2[pre_sum ^ target1]  # [0,i] 的最后一段的异或和是 target1 的方案数
            last2 = f1[pre_sum ^ target2]  # [0,i] 的最后一段的异或和是 target2 的方案数
            if i == len(nums) - 1:
                return (last1 + last2) % MOD
            f1[pre_sum] = (f1[pre_sum] + last1) % MOD
            f2[pre_sum] = (f2[pre_sum] + last2) % MOD
''',
    call='Solution().alternatingXOR([1,0,0,1,1], 1, 0)',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', cell=96, h=190, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else None,
             dim=lambda S, k, v: S.get('i') is not None and k > S['i']),
        dict(type='map', var='f1', label='f1[s]：前缀异或和为 s，最后一段是 target1 的方案数', h=190, font=30,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='map', var='f2', label='f2[s]：前缀异或和为 s，最后一段是 target2 的方案数', h=190, font=30,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', h=70, size=28,
             fn=lambda S: (f"`pre_sum = {S['pre_sum']}`，找 f2[`{S['pre_sum']} ^ {S['target1']}`] 和 f1[`{S['pre_sum']} ^ {S['target2']}`]"
                           if 'pre_sum' in S else '`f2[0] = 1`：第一段前面有一个异或和为 0 的空前缀')),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('pre_sum', 'pre_sum', 'cyan'), ('last1', 'last1', 'green'), ('last2', 'last2', 'orange')],
    captions={
        'MOD =': '答案要取模；中途取模不影响结果',
        'f1 = defaultdict': '`f1[s]`：异或和为 `s` 的前缀，且最后一段异或和是 ==target1==，有几种分割',
        'f2 = defaultdict': '`f2[s]`：同样的前缀，但最后一段异或和是 ==target2==',
        'f2[0] = 1': '空前缀异或和为 0，算 `f2[0] = 1`：这样第一段（要求 target1）就能从它转移，方案数是 1',
        'pre_sum = 0': '`pre_sum` 是前缀异或和',
        'for i, x in enumerate': lambda S, B, r: (f'看 `nums[{S.i}] = {S.x}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        'pre_sum ^= x': '`pre_sum ^= {x}` → `{pre_sum}`：前缀 `[0,{i}]` 的异或和',
        'last1 =': '最后一段是 target1：前面那个前缀异或和必须是 `{pre_sum} ^ {target1} = {pre_sum ^ target1}`，且它的最后一段是 target2 → 取 `f2` → ==`{last1}`==',
        'last2 =': '最后一段是 target2：前缀异或和是 `{pre_sum} ^ {target2} = {pre_sum ^ target2}`，且最后一段是 target1 → 取 `f1` → ==`{last2}`==',
        'if i == len(nums) - 1': lambda S, B, r: ('到最后一个数了：答案就是此刻的 `last1 + last2`，先别写进表里' if S.i == len(S.nums) - 1
                                                  else f'`i = {S.i}` 不是最后一个数，继续记录'),
        'return (last1': '整个数组的分割数 = `{last1} + {last2}` = =={ret}==（不能从 f1、f2 里取，会混入异或和相同的更短前缀）',
        'f1[pre_sum] =': '`f1[{pre_sum}]` += `last1` → ==`{f1[pre_sum]}`==：以后别的前缀可以接在它后面',
        'f2[pre_sum] =': '`f2[{pre_sum}]` += `last2` → ==`{f2[pre_sum]}`==；注意两个式子用的是同一轮的旧值',
    },
    cards=dict(
        one_liner='借鉴 560：用前缀异或和当键，哈希表记录分割方案数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `nums` 分成若干连续非空块，各块异或和按 `target1, target2, target1, ...` 交替',
                 '返回有效分割的方案数，对 `10^9 + 7` 取模',
                 '本视频：`nums = [1,0,0,1,1]`，`target1 = 1`，`target2 = 0`'],
        quote='用两个哈希表记录每个前缀和对应的划分方案数：f1[s] 表示分割异或和为 s 的前缀，满足交替要求，且最后一段的异或和是 target1 的方案数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['想一想，==最后一步==发生了什么：切下最后一段，剩下是更小的前缀',
              '最后一段是 target1，前缀异或和就是 `s ^ target1`，且它的最后一段必须是 target2',
              '`f1[s] += f2[s ^ target1]`，`f2[s] += f1[s ^ target2]`，初值 `f2[0] = 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '两个式子要==同时算==：先取 last1、last2，再一起写入表',
                 '答案取最后一轮写入前的 `last1 + last2`，不能遍历完再从表里取',
                 '另有利用前缀异或周期为 4 的状态机 DP；若改成加法就失效，本写法仍可用',
                 '前置题：560. 和为 K 的子数组'],
    ),
)
