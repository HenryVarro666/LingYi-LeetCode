CONFIG = dict(
    num=1862, title='向下取整数对和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='计数 + 前缀和 + 枚举分母与商（Go 原文转写）',
    tags=['一、前缀和', '§1.5 进阶', '难度分 2170'],
    code='''
class Solution:
    def sumOfFlooredPairs(self, a: List[int]) -> int:
        ans = 0
        cnt = [0] * 12
        for v in a:
            cnt[v] += 1
        sum = [0] * 13
        for i, v in enumerate(cnt):
            sum[i + 1] = sum[i] + v
        for i, c in enumerate(cnt):
            if c > 0:
                d = 1
                while d * i <= 6:
                    ans += c * d * (sum[(d + 1) * i] - sum[d * i])
                    d += 1
        return ans % (10 ** 9 + 7)
''',
    call='Solution().sumOfFlooredPairs([2, 3, 6])',
    expect=sum(x // y for x in [2, 3, 6] for y in [2, 3, 6]),
    max_steps=110,
    views=[
        dict(type='array', var='cnt', label='cnt：每个数出现次数', pointers={'i': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='array', var=lambda S: S.get('sum'), label='sum：次数的前缀和，sum[x] = 小于 x 的数的个数', h=170,
             color=lambda S, i, v: None),
        dict(type='text', h=80, fn=lambda S: (f"分母 `{S['i']}`（{S['c']} 个），商 `d = {S['d']}`：分子落在 `[{S['d']*S['i']}, {(S['d']+1)*S['i']-1}]`，共 =={S['sum'][(S['d']+1)*S['i']] - S['sum'][S['d']*S['i']]}== 个" if 'd' in S and 'c' in S and 'i' in S and (S['d']+1)*S['i'] < len(S['sum']) else '')),
    ],
    watch=['i', 'c', 'd', ('ans', 'ans', 'green')],
    captions={
        'cnt = [0] * 12': '`cnt[v]`：数值 v 的出现次数。原文数组大小 2e5，为演示缩成 12',
        'for v in a': '统计每个数的出现次数',
        'cnt[v] += 1': '`cnt[{v}]` → {cnt[v]}',
        'sum = [0] * 13': '`sum[i+1]`：`cnt[0..i]` 的和，用来 O(1) 求某个值域区间内有几个数',
        'for i, v in enumerate(cnt)': '累加前缀和',
        'sum[i + 1] = sum[i] + v': '`sum[{i + 1}] = {sum[i + 1]}`',
        'for i, c in enumerate(cnt)': '枚举分母 `i`，`c` 是它的个数',
        'if c > 0': '分母 `{i}` 出现了 {c} 次 → {"需要处理" if c > 0 else "没有这个数，跳过"}',
        'd = 1': '从商 `d = 1` 开始枚举',
        'while d * i <= 6': '`d × i = {d * i}`：{"分子区间还在值域内，继续" if d * i <= 6 else "超过最大值了，该分母处理完"}（原文是 1e5，演示缩成 6）',
        'ans += c * d * ': '分子在 `[{d * i}, {(d + 1) * i - 1}]` 的数有 `sum[{(d + 1) * i}] - sum[{d * i}] = {sum[(d + 1) * i] - sum[d * i]}` 个，每个商都是 `{d}`，分母 `{c}` 个 → `ans` = =={ans}==',
        'd += 1': '商加 1，看下一个区间',
        'return ans % ': '取模后返回 `{ans % (10 ** 9 + 7)}`',
    },
    cards=dict(
        one_liner='枚举分母和商，用前缀和一次数出分子个数',
        complexity='时间 `O(U log U)`，空间 `O(U)`',
        problem=['求所有下标对 `(i, j)` 的 `floor(nums[i] / nums[j])` 之和，结果对 `1e9+7` 取余',
                 '数组长 1e5、值 ≤ 1e5，不能两两枚举',
                 '本视频：`[2,3,6]` → `9`'],
        quote='统计每个数的出现次数 cnt，并计算次数的前缀和 sum。然后枚举分母以及商，用前缀和计算对应的分子个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分母 `i` 固定，商为 `d` 的分子落在 `[d*i, (d+1)*i-1]`',
              '这个区间里的数个数 = `sum` 两端相减',
              '分母个数 `c` × 商 `d` × 分子个数，累加；`d` 只枚举到 `U/i`，总共是调和级数'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；演示时把原文常量 2e5 / 1e5 缩小为 12 / 6，其余不变',
                 '时间 `O(U log U)`（调和级数），空间 `O(U)`',
                 '易错点：`sum` 比 `cnt` 多一位；只对 `cnt[i] > 0` 的分母枚举',
                 '最后才对 `1e9+7` 取余（Python 整数不会溢出）'],
    ),
)
