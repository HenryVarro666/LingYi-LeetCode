def _fcol(S, t, v):
    line = S.get('_line')
    if 'index' in S and line in (9, 13, 14):
        if t == S['index']:
            return 'yellow'
        if line in (13, 14) and S['index'] >= S['v'] and t == S['index'] - S['v']:
            return 'pink'
    return None


def _txt(S):
    if 'v' not in S or 'index' not in S or S.get('_line') not in (9, 13, 14):
        return '`f[j]` = 满足「某个子序列 sj 里有和为 j 的子序列」的 sj 的个数'
    i, v = S['index'], S['v']
    s = f'`f[{i}]` 的三类来源：①不进 sj ②进 sj 但不进和为 j 的子序列 → 两个都是旧 `f[{i}]`'
    if i >= v:
        s += f'；③ 进和为 j 的子序列 → 旧 `f[{i - v}]`'
    else:
        s += f'；`{i} < {v}`，没有第③类'
    return s


CONFIG = dict(
    num=3082, title='求出所有子序列的能量和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='一维背包 · 倒序滚动 · 手动取模',
    tags=['灵神题单', '动态规划', '难度分 2242'],
    code='''
class Solution(object):
    def sumOfPower(self, nums, k):

        f = [0] * (k + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for v in nums:
            for index in range(k, -1, -1):
                f[index] += f[index]
                if f[index] >= mod:
                    f[index] -= mod

                if index >= v:
                    f[index] += f[index - v]
                    if f[index] >= mod:
                        f[index] -= mod

        return f[-1]
''',
    call='Solution().sumOfPower([1, 2, 3], 3)',
    expect=6,
    skip=['f = [0]', 'mod = 10', 'for index in range', 'if f[index] >= mod'],
    max_steps=70,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前的 v）', cell=90, h=170,
             color=lambda S, t, x: 'blue' if 'v' in S and x == S['v'] and 'index' in S else None),
        dict(type='array', var='f', label='f[j]：黄 = 正在更新，粉 = 来源 f[j-v]', cell=100, h=210, color=_fcol),
        dict(type='text', fn=_txt, size=24, h=100),
    ],
    watch=['v', 'index', ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f[0] = 1': '`f[0] = 1`：空子序列，和为 0',
        'for v in nums': lambda S, B, r: ('所有数处理完了' if B.get('v') == S.v and S.nums.count(S.v) == 1 else f'依次加入 `v = {S.v}`，`index` 从 `k` ==倒序==到 0，才能用上一轮的旧值'),
        'f[index] += f[index]': '情况 1、2：`v` 不进和为 j 的子序列（进不进 sj 都行）→ `f[{index}]` 翻倍：{B.f[index]} → =={f[index]}==',
        'if index >= v': '`index = {index}`，`v = {v}`：{"够放下 v，可以走情况 3" if index >= v else "放不下 v，只有前两种情况"}',
        'f[index] += f[index - v]': '情况 3：`v` 进了和为 j 的子序列 → 加上旧 `f[{index - v}]` = {B.f[index - v]}：`f[{index}]` = =={f[index]}==',
        'return f[-1]': '`f[k]` = 所有子序列的能量和 = =={f[-1]}=='
    },
    cards=dict(
        one_liner='f[j] 统计「内含和为 j 子序列」的子序列个数，每个数三种用法',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['子序列 s 的「能量」= s 里和恰为 k 的子序列个数',
                 '求 ==所有子序列的能量之和==，答案对 `10^9+7` 取余',
                 '示例：`[1,2,3], k=3` → `6`'],
        quote='加入子序列sj中，但是不加入sj的和为j的子序列中，那么同样是f[i][j] += f[i - 1][j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[j]`：满足「sj 内部有一个子序列和为 j」的 sj 的个数',
              '`nums[i]` 三种用法：不进 sj；进 sj 但不参与凑和；进 sj 且参与凑和',
              '前两种各贡献 `f[j]`，第三种贡献 `f[j - v]` → ==f[j] = 2·f[j] + f[j-v]==，倒序滚动一维'],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '`index` 必须倒序，否则同一个 `v` 会被重复使用',
                 '`index < v` 时只翻倍，不能读 `f[index - v]`',
                 '用 `if f >= mod: f -= mod` 代替取余，每次相加后值都小于 `2·mod`',
                 '原文 `f[-1]` 就是 `f[k]`'],
    ),
)
