CONFIG = dict(
    num=2585, title='获得分数的方法数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多重背包 · 枚举做几道（方案数）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1910'],
    code='''
class Solution:
    def waysToReachTarget(self, target: int, types: List[List[int]]) -> int:
        MOD = 1_000_000_007
        f = [1] + [0] * target
        for count, marks in types:
            for j in range(target, marks - 1, -1):
                for k in range(1, min(count, j // marks) + 1):
                    f[j] += f[j - k * marks]
                f[j] %= MOD
        return f[-1]
''',
    call='Solution().waysToReachTarget(4, [[2,1],[2,2]])',
    expect=2,
    skip=['for j in range', 'for k in range'],
    max_steps=70,
    views=[
        dict(type='text', size=24, h=50, fn=lambda S: (
            f'当前题型：`{S["count"]}` 道，每道 `{S["marks"]}` 分' if 'count' in S else '`f[j]` = 用已处理的题型恰好得 j 分的方案数')),
        dict(type='array', var='types', label='types = [道数, 每道分数]', h=190, cell=110,
             color=lambda S, k, v: 'blue' if S.get('count') is not None and v == [S['count'], S['marks']] else None),
        dict(type='array', var='f', label='f[j]（pink = 正在更新的 j，blue = 来源）', h=200, cell=80, pointers={'j': 'pink'},
             color=lambda S, k, v: ('blue' if S.get('j') is not None and S.get('k') is not None and S.get('marks') and k == S['j'] - S['k'] * S['marks']
                                    and S.get('_line', 0) == 8 else None)),
    ],
    watch=[('count', 'count', 'cyan'), ('marks', 'marks', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'yellow')],
    captions={
        'MOD =': '答案对 `10^9+7` 取余',
        'f = [1]': '`f[0] = 1`：得 0 分只有一种方法（都不做）',
        'for count, marks in types': lambda S, B, r: ('所有题型都处理完了' if B.get('marks') == S.marks and B.get('count') == S.count and B.get('marks') is not None else f'处理一种题型：`{S.count}` 道，每道 `{S.marks}` 分'),
        'f[j] += f[j - k * marks]': '做 `{k}` 道这种题 = 得 `{k * marks}` 分，剩下 `{j - k * marks}` 分由前面的题型凑：`f[{j}] += f[{j - k * marks}]` → =={f[j]}==',
        'f[j] %= MOD': '`f[{j}]` 加完 k=1..{min(count, j // marks)} 的所有情况（k=0 就是原来的 f[j]），取余 → =={f[j]}==',
        'return f[-1]': '恰好 `target` 分的方案数 = `f[-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举这种题做几道，倒序更新才不会重复用',
        complexity='时间 `O(target·S)`，空间 `O(target)`',
        problem=['有 `n` 种题型，第 `i` 种有 `count_i` 道，每道 `marks_i` 分；同类型题无法区分',
                 '求恰好得 `target` 分的方法数，对 `10^9+7` 取余',
                 '示例：`target=6, types=[[6,1],[3,2],[2,3]]` → `7`；视频用 `target=4, [[2,1],[2,2]]`'],
        quote='f[i][j] = Σ f[i-1][j-k·marks_i]。注意 k 不能超过 count_i，且 j-k·marks_i ≥ 0。',
        quote_src='—— 灵茶山艾府题解（公式）',
        idea=['`f[j]`：前若干种题型恰好得 `j` 分的方案数',
              '枚举这一种题做 `k` 道，剩下的分数交给前面的题型',
              '像 0-1 背包一样压成一维：`j` 倒序，保证 `f[j-k·marks]` 还是上一种题型的值'],
        summary=['时间 `O(target·S)`，`S` 为所有 `count` 之和；空间 `O(target)`',
                 '`k` 上限是 `min(count, j // marks)`，别越界',
                 '`j` 必须倒序：正序会把本种题型重复算进去',
                 '`k=0` 的情况就是原来的 `f[j]`，无需再加',
                 '更快的做法见 2902（二进制优化 / 滑窗前缀和）'],
    ),
)
