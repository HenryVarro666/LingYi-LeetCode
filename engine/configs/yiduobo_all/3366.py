def _fml(S):
    k = S.get('k')
    return f'part1 `>= {2*k-1}` 先除再减；part2 `[{k}, {2*k-2}]` 先减再除；part3 `< {k}` 只能除'


CONFIG = dict(
    num=3366, title='最小数组和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='分三段贪心 + 奇偶修正',
    tags=['其他线性 DP', '难度分 2040'],
    code='''
class Solution(object):
    def minArraySum(self, nums, k, op1, op2):
        
        part1 = []
        part2 = []
        part3 = []

        for v in nums:
            if v >= k * 2 - 1:
                part1.append(v)
            elif v >= k:
                part2.append(v)
            else:
                part3.append(v)

        res = 0

        part1.sort(reverse=True)
        for v in part1:
            if op1:
                v = (v + 1) // 2
                op1 -= 1
            if op2:
                v -= k
                op2 -= 1
            res += v
        
        part2.sort()
        mk_dict = {}
        rest_odd = 0
        for index, v in enumerate(part2):
            if op2:
                if v % 2 == 0 and k % 2 == 1:
                    mk_dict[v - k] = mk_dict.get(v - k, 0) + 1
                part2[index] -= k
                op2 -= 1
            elif v % 2 == 1:
                rest_odd += 1

        part3.extend(part2)
        part3.sort(reverse=True)
        for v in part3:
            if op1:
                if mk_dict.get(v, 0) > 0 and rest_odd > 0:
                    mk_dict[v] -= 1
                    rest_odd -= 1
                    res -= 1
                v = (v + 1) // 2
                op1 -= 1
            res += v
        
        return res
''',
    call='Solution().minArraySum([6, 7, 12], 5, 3, 2)',
    expect=5,
    skip=['part1 = []', 'part2 = []', 'part3 = []', 'part1.append', 'part2.append', 'part3.append', 'mk_dict = {}'],
    max_steps=70,
    views=[
        dict(type='text', fn=_fml, size=22, h=70),
        dict(type='array', var='part1', label='part1（大 → 先除再减，从大到小）', h=130, cell=70),
        dict(type='array', var='part2', label='part2（减法给小的，除法给大的）', h=130, cell=70),
        dict(type='array', var='part3', label='part3（并入 part2 后从大到小做除法）', h=130, cell=70),
        dict(type='map', var='mk_dict', label='mk_dict：偶数−奇数 k 得到的值 → 次数', h=110, font=26),
    ],
    watch=[('v', 'v', 'yellow'), ('op1', 'op1', 'blue'), ('op2', 'op2', 'pink'), ('rest_odd', 'rest_odd', 'cyan'), ('res', 'res', 'green')],
    captions={
        8: '先按大小把数分成三段',
        9: lambda S, B, r: f'`{S.v} >= 2k-1 = {S.k*2-1}`？' + ('是 → part1：先除再减也还能减' if S.v >= S.k * 2 - 1 else '否'),
        11: lambda S, B, r: f'`{S.v} >= k = {S.k}`？' + ('是 → part2：只能先减再除' if S.v >= S.k else '否'),
        13: '剩下的 `< k` → part3：减不了，只能除',
        16: '`res = 0`：累计最终的数',
        18: 'part1 从大到小：除法给最大的数收益最大',
        20: lambda S, B, r: (f'`op1 = {S.op1}` 还有除法：`{S.v}` 先除以 2 上取整' if S.op1 else '没有除法次数了，跳过'),
        21: '`v = (v + 1) // 2` = =={v}==',
        23: lambda S, B, r: (f'`op2 = {S.op2}` 还有减法：再减 `k`（先除后减更优）' if S.op2 else '没有减法次数了，跳过'),
        24: '`v -= k` → =={v}==',
        26: '`res += {v}` → =={res}==',
        28: 'part2 从小到大排：减法给小的数（减法对任何数收益都是 k），把大的留给除法',
        29: '`mk_dict` 记「偶数减去奇数 k」得到的值；`rest_odd` 记没减的奇数个数',
        32: lambda S, B, r: (f'`op2 = {S.op2}`：剩余减法给 `{S.v}`' if S.op2 else f'减法用完，`{S.v}` 不减'),
        33: lambda S, B, r: (f'`{S.v}` 是偶数且 `k = {S.k}` 是奇数 → 减完变成奇数，除 2 时会多向上取整一次，要登记' if S.v % 2 == 0 and S.k % 2 == 1
                             else f'`{S.v}` 是奇数，或 `k` 是偶数：奇偶不会出问题，不登记'),
        34: '`mk_dict[{v - k}]` 加 1：值 `{v-k}` 是偶数 `{v}` 减 `{k}` 得来的',
        35: '`part2[{index}]` 减 `k` → =={part2[index]}==',
        37: lambda S, B, r: f'没减的 `{S.v}` 是奇数 → `rest_odd` 加 1' if S.v % 2 == 1 else f'没减的 `{S.v}` 是偶数，不用管',
        38: '`rest_odd` = =={rest_odd}==',
        40: 'part2 减完后并入 part3，一起做除法',
        41: '从大到小排序：除法给大的',
        43: lambda S, B, r: (f'`op1 = {S.op1}`：`{S.v}` 做除法' if S.op1 else f'除法用完，`{S.v}` 保持不变'),
        44: lambda S, B, r: (f'`{S.v}` 在 `mk_dict` 里，且还有没减的奇数 → 把减法换给那个奇数更划算' if (S.mk_dict.get(S.v, 0) > 0 and S.rest_odd > 0)
                             else f'`{S.v}` 不需要修正'),
        47: '修正：把减法换到奇数上，除法向上取整少浪费 1 → `res` 减 1，现在 `res = {res}`',
        48: '`v = (v + 1) // 2` = =={v}==',
        50: '`res += {v}` → =={res}==',
        52: '三段处理完，最小和 = =={ret}==',
    },
    cards=dict(
        one_liner='除法给大数、减法给小数，再用奇偶性修正一次',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['操作 1：`nums[i]` 除以 2 上取整，最多 `op1` 次；操作 2：`nums[i] >= k` 时减 `k`，最多 `op2` 次',
                 '每个下标每种操作至多一次，两种可叠加；求最小和',
                 '本视频：`[6,7,12], k=5, op1=3, op2=2` → `5`'],
        quote='应该尽量先执行除法操作再执行减法操作，因为先执行减法操作的话除法操作的效果会打折扣。……应该让除法操作应用在尽量大的数字上。',
        quote_src='—— yiduobo 题解原文',
        idea=['分三段：`>= 2k-1` 先除再减；`[k, 2k-2]` 先减再除；`< k` 只能除',
              'part1 从大到小全做；剩下的减法给 part2 里较小的，剩下的除法给较大的',
              'k 为奇数时 part2 里奇偶不同会差 1：用 `mk_dict` 和 `rest_odd` 做一次修正'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '修正条件：`k` 为奇数、被减的数是偶数、且存在没减的奇数',
                 '修正后答案恰好减 1：`(v+1)//2 + (y+1)//2 - 1`',
                 '示例 `[6,7], k=5` 不修正得 5，修正后得 4',
                 '原文已是 Python 3 兼容写法（`//` 整数除法），无需修改'],
    ),
)
