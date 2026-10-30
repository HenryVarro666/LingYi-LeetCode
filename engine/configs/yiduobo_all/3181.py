VALS = [5, 2, 7, 2]


def _fcol(S, i, v):
    return 'yellow' if S.get('v') is not None and i == S['v'] and S.get('_line') and 12 <= S['_line'] <= 35 else None


def _txt(S):
    ln = S.get('_line')
    if 'p' in S and 'v' in S and ln and 12 <= ln <= 35:
        return f'`calc({S["v"]}, {S["p"]})`：只用 `nums[0..{S["p"]}]` 能否凑出和 `{S["v"]}`？'
    return '`f[v]`：已知能凑出 v 的最小前缀下标；`g[v]`：已知凑不出 v 的最大前缀下标'


CONFIG = dict(
    num=3181, title='执行操作可获得的最大总奖励 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='记忆化搜索 + 剪枝 + f/g 前缀记录',
    tags=['难度分 2688'],
    code='''
class Solution(object):
    def maxTotalReward(self, rewardValues):

        nums = sorted(list(set(rewardValues)))
        
        ma = nums[-1]
        nums.pop()
        f = [len(nums)] * ma
        f[0] = -1
        g = [-1] * ma

        def calc(v, p):
            if f[v] <= p:
                return True
            if g[v] >= p:
                return False

            while p >= 0 and nums[p] > v:
                p -= 1

            res = False
            for index in range(p, -1, -1):
                if nums[index] * 2 <= v:
                    break
                
                if calc(v - nums[index], index - 1):
                    res = True
                    break

            if res:
                f[v] = min(f[v], p)
            else:
                g[v] = max(g[v], p)
        
            return res
        
        for v in range(ma - 1, -1, -1):
            if calc(v, len(nums) - 1):
                return v + ma
''',
    call=f'Solution().maxTotalReward({VALS})',
    expect=12,
    skip=['def calc', 'res = False', 'for v in range(ma'],
    views=[
        dict(type='array', var='nums', label='nums（去重排序，最大值 ma 已取出）', h=140, cell=70,
             color=lambda S, i, v: 'blue' if S.get('index') == i and S.get('_line') in (23, 26, 27) else None),
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='array', var='f', label='f[v]：能凑出 v 的最小前缀（越小越早）', h=140, cell=64, color=_fcol),
        dict(type='array', var='g', label='g[v]：凑不出 v 的最大前缀', h=140, cell=64, color=_fcol),
        dict(type='calls', h=210),
    ],
    watch=[('ma', 'ma', 'cyan'), ('v', 'v', 'yellow'), ('p', 'p', 'blue'), ('index', 'index', 'pink')],
    captions={
        'nums = sorted': '去重再排序：`nums = {nums}`（相同的值选不了两次）',
        'ma = nums[-1]': '最大值 `ma = {ma}` 必选：没选它的方案，把最后一个换成 ma 一定更好',
        'nums.pop': '把 `ma` 从 `nums` 里拿掉，问题变成：用 `nums` 凑一个 `≤ ma-1` 的最大和',
        'f = [len(nums)]': '`f[v]`：已知能凑出 v 的最小前缀下标，初始 `len(nums)` 表示还不知道能凑',
        'f[0] = -1': '和 0 什么都不选就能凑出：下标记为 -1',
        'g = [-1]': '`g[v]`：已知凑不出 v 的最大前缀下标，初始 -1',
        'if f[v] <= p': lambda S, B, r: (f'`f[{S.v}] = {S.f[S.v]} ≤ p = {S.p}`：前缀 `nums[0..{S.p}]` 已知能凑出 {S.v}' if S.f[S.v] <= S.p
                                         else f'`f[{S.v}] = {S.f[S.v]} > p = {S.p}`：还不知道这个前缀能不能凑出 {S.v}'),
        'return True': '命中缓存：能凑出，返回 True',
        'if g[v] >= p': lambda S, B, r: (f'`g[{S.v}] = {S.g[S.v]} ≥ p = {S.p}`：已知这个前缀凑不出 {S.v}' if S.g[S.v] >= S.p
                                         else f'`g[{S.v}] = {S.g[S.v]} < p = {S.p}`：没有记录，只能往下搜索'),
        'return False': '命中缓存：凑不出，返回 False',
        'while p >= 0': lambda S, B, r: (f'`nums[{S.p}] = {S.nums[S.p]} > v = {S.v}`，太大选不了，`p` 左移 → {S.p}' if S.p >= 0 and S.nums[S.p] > S.v
                                         else f'从 `p = {S.p}` 开始枚举最后选的数（比 {S.v} 大的已经排除）'),
        'p -= 1': '`p` → {p}',
        'for index in range': lambda S, B, r: (f'枚举最后一个选的数 `nums[{S.index}] = {S.nums[S.index]}`' if S.get('index') is not None and S.index != B.get('index') or B.get('index') is None
                                               else '枚举完了'),
        'if nums[index] * 2 <= v': lambda S, B, r: (f'`{S.nums[S.index]} × 2 = {S.nums[S.index] * 2} ≤ {S.v}`：它不超过 v 的一半，更小的更不行 → 剪枝 break' if S.nums[S.index] * 2 <= S.v
                                                    else f'`{S.nums[S.index]} × 2 > {S.v}`：它超过 v 的一半，比剩下的和大，合法，继续'),
        'break': '剪枝：后面的数都不超过 v 的一半，不用再试',
        'if calc(v - nums[index]': lambda S, B, r: f'选 `{B.nums[B.index]}`，剩下要凑 `{B.v} - {B.nums[B.index]} = {B.v - B.nums[B.index]}`，只能用 `nums[0..{B.index - 1}]`（每个数只选一次）',
        'res = True': '找到一种凑法，`res = True`',
        'if res': lambda S, B, r: ('凑得出 → 更新 `f[v]`（已知可凑的最小前缀）' if S.res else '凑不出 → 更新 `g[v]`（已知不可凑的最大前缀）'),
        'f[v] = min': '`f[{v}] = {f[v]}`',
        'g[v] = max': '`g[{v}] = {g[v]}`',
        'return res': '`calc({v}, {p})` 返回 `{res}`',
        'if calc(v, len(nums) - 1)': lambda S, B, r: f'从大到小试 `v = {S.v}`：`nums` 能否凑出 {S.v}？',
        'return v + ma': '`v = {v}` 是最大的可凑和，答案 `v + ma = {v} + {ma}` = =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='最大值必选，再用带剪枝的记忆化找最大可凑和',
        complexity='时间：作者称不好严格分析，空间 `O(ma)`',
        problem=['总奖励 `x` 从 0 开始，每次选一个未选过、==大于 x== 的值累加',
                 '求最大总奖励；本题 `n`、值都可到 `5×10^4`',
                 '示例：`[1,1,3,3]` → `4`；本视频：`[5,2,7,2]` → `12`'],
        quote='rewardValues中的最大值ma是必然会被选择的，因为如果没有选择ma，那么对于当前的选择方案，使用ma去替代已选择的最大值必然是可行的，同时总奖励值也会更优。',
        quote_src='—— yiduobo 题解原文',
        idea=['去重 + 取出最大值 `ma`：问题变成「用其余数凑 ≤ ma-1 的最大和」',
              '写成记忆化搜索，剪枝一：选的数要大于剩余和 → 比 v 一半小的不用试',
              '剪枝二：排序后前缀有单调性，用 `f[v]`/`g[v]` 记「最小可凑前缀」「最大不可凑前缀」'],
        summary=['作者没有给出严格复杂度，依赖两个剪枝才能通过',
                 '易错：`calc` 的下标 `p` 要先把比 `v` 大的数跳过',
                 '易错：递归时下一个数从 `index - 1` 开始，保证每个数只选一次',
                 '原文可直接在 Python 3 运行，未做修改',
                 '对比灵神：他用 bitset 位运算一步转移，思路更简洁、复杂度可分析'],
    ),
)
