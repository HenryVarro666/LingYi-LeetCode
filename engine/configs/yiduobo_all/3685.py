def _fv(S):
    return [int(b) for b in S['f']] if 'f' in S else None


def _rv(S):
    return ['T' if b else 'F' for b in S['res']] if 'res' in S else None


def _fcol(S, t, v):
    line = S.get('_line')
    if line in (16, 17) and 'index' in S and t == S['index']:
        return 'yellow'
    if line in (24, 25, 27, 28) and 'v' in S and t == S['v'] and 'flag' in S:
        return 'pink'
    return 'green' if v else None


def _txt(S):
    if 'x' not in S or 'p' not in S:
        return '`f[s]` = 用已解禁的数能否凑出和 `s`'
    nums, p, q, x = S['nums'], S['p'], S['q'] if 'q' in S else S['p'], S['x']
    return f'`x = {x}`：已解禁前缀 `nums[:{p}]` = {nums[:p]}，没解禁的 `{len(nums) - p}` 个都被卡成 {x}'


CONFIG = dict(
    num=3685, title='含上限元素的子序列和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='排序前缀 · 解禁元素 · 背包 + 检查 k - t·x',
    tags=['灵神题单', '动态规划', '难度分 2073'],
    code='''
class Solution(object):
    def subsequenceSumAfterCapping(self, nums, k):
        
        nums.sort()
        p = 0
        res = []
        f = [False] * (k + 1)
        f[0] = True
        for x in range(1, len(nums) + 1):
            q = p
            while q < len(nums) and nums[q] < x:
                q += 1
            
            for v in nums[p: q]:
                for index in range(k, v - 1, -1):
                    if f[index - v]:
                        f[index] = True
            p = q

            m = len(nums) - q
            v = k
            flag = False
            for index in range(m + 1):
                if f[v]:
                    flag = True
                    break
                v -= x
                if v < 0:
                    break

            res.append(flag)
        
        return res
''',
    call='Solution().subsequenceSumAfterCapping([4,3,2,4], 5)',
    expect=[False, False, True, True],
    skip=['p = 0', 'res = []', 'f = [False]', 'for index in range(k', 'flag = False', 'for index in range(m + 1)', 'v = k', 'v -= x', 'for v in nums[p: q]'],
    max_steps=90,
    views=[
        dict(type='array', var='nums', label='nums（排序后；p 左边 = 已解禁并入背包的数）', cell=90, h=170,
             pointers={'p': 'blue'}, color=lambda S, t, v: 'green' if 'p' in S and t < S['p'] else None,
             dim=lambda S, t, v: 'p' in S and t >= S['p']),
        dict(type='array', var=_fv, label='f[s]：能否凑出和 s（粉 = 正在查的 v，黄 = 正在更新）', cell=80, h=190, color=_fcol),
        dict(type='array', var=_rv, label='res（每个 x 的结果）', cell=80, h=170,
             color=lambda S, t, v: 'green' if v == 'T' else None),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=['x', 'p', 'q', 'v', ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    captions={
        'nums.sort()': '先排序：x 越大，被解禁的元素越多，可用元素是一个==前缀== → `{nums}`',
        'f[0] = True': '`f[0] = True`：什么都不选，和为 0',
        'for x in range': lambda S, B, r: ('`x` 枚举完了，结束循环' if B.get('x') == S.x else f'枚举上限 `x = {S.x}`'),
        'q = p': '`q = p = {p}`：从上次解禁的位置继续往后找',
        'while q < len': lambda S, B, r: (f'`nums[{S.q}] = {S.nums[S.q]} < x = {S.x}`：比上限小，不会被卡住 → ==解禁==' if S.q < len(S.nums) and S.nums[S.q] < S.x
                                          else f'`q = {S.q}`：后面的数都 ≥ {S.x}，会被卡成 {S.x}（等于 x 的数留到下一轮解禁）'),
        'q += 1': '`q` → {q}',
        'if f[index - v]': '`f[{index} - {v}]` = {f[index - v]}：{"能凑出 " + str(index - v) + "，再加 v 就能凑出 " + str(index) if f[index - v] else "凑不出 " + str(index - v) + "，跳过"}（==倒序==，每个数只用一次）',
        'f[index] = True': '`f[{index}] = True`',
        'p = q': '`p = q = {p}`：前缀 `nums[:{p}]` 都已并入背包',
        'm = len(nums) - q': '还有 `m = {m}` 个数 ≥ x，它们都被卡成 {x}',
        'if f[v]': '剩下要凑 `v = {v}`，已选 `{(k - v) // x}` 个 {x}：`f[{v}]` = {f[v]}',
        'flag = True': '能凑出！`flag = True`，==不用再试== → break',
        'if v < 0': lambda S, B, r: (f'再选一个 {S.x}：`v = {S.v + S.x} - {S.x} = {S.v}` < 0，选太多了 → break' if S.v < 0
                                     else f'再选一个 {S.x}：`v = {S.v + S.x} - {S.x} = {S.v}` ≥ 0，继续试'),
        'res.append(flag)': '`x = {x}` 的结果是 `{flag}` → res = {res}',
        'return res': '全部结果：`{res}`',
    },
    cards=dict(
        one_liner='排序后一个个解禁元素；剩下的被卡成 x，从 k 往下减 x 试',
        complexity='时间 `O(nk + k log n)`，空间 `O(k)`',
        problem=['`nums` 里大于 x 的元素都被替换成 x，对 `x = 1..n` 分别回答',
                 '能否选子序列使和 ==恰好为 k==',
                 '示例：`[4,3,2,4], k=5` → `[F,F,T,T]`'],
        quote='随着x的增大，相当于原始nums中被x卡住的元素重新被解禁了。如果在这里想将nums从小到大进行排序，那么随着x的增大，nums中可用的原始元素就是一个逐渐变长的前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['排好序后，每个 x 只比上一个 x 多解禁一小段 `nums[p:q]`',
              '把这一段做背包更新，==不用重算==整个 f',
              '没解禁的 `m` 个都是 x：从 `k` 开始试 `k, k-x, k-2x, …, k-m·x`，任何一个能凑出就行'],
        summary=['复杂度 `O(nk + k log n)`：试 `k-t·x` 的总次数是调和级数 `k + k/2 + …`',
                 '背包内层必须==倒序==，否则同一个数会被选多次',
                 '`while` 用严格小于 x：等于 x 的数仍会被卡成 x，下一轮才并入背包',
                 '原文变量 `v` 复用：先当背包物品，后当剩余目标，别弄混',
                 '对比灵神：灵神 `nums[i] == x` 时并入背包；这里是 `< x`，早一轮'],
    ),
)
