def _a_txt(S):
    if 'a' not in S:
        return ''
    a = S['a']
    if not a:
        return '`a` = [ ]（空，当前没有候选子数组）'
    return '`a`（[GCD, 右端点]）= ' + '  '.join(f'`[{p[0]}, {p[1]}]`' for p in a) + '　左端点在 `i0` 之后，GCD 从左到右递增'


CONFIG = dict(
    num=2447, title='最大公因数等于 K 的子数组数目', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='GCD LogTrick：按 GCD 分组',
    tags=['GCD', 'LogTrick'],
    code='''
class Solution:
    def subarrayGCD(self, nums: List[int], k: int) -> int:
        ans = 0
        a = []  # [GCD，相同 GCD 区间的右端点]
        i0 = -1
        for i, x in enumerate(nums):
            if x % k:  # 保证后续求的 GCD 都是 k 的倍数
                a = []
                i0 = i
                continue
            a.append([x, i])
            # 原地去重，因为相同的 GCD 都相邻在一起
            j = 0
            for p in a:
                p[0] = gcd(p[0], x)
                if a[j][0] != p[0]:
                    j += 1
                    a[j] = p
                else:
                    a[j][1] = p[1]
            del a[j + 1:]
            if a[0][0] == k:  # a[0][0] >= k
                ans += a[0][1] - i0
        return ans
''',
    call='Solution().subarrayGCD([6,4,3,8,2], 2)',
    expect=3,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'i0': 'pink'}, h=200,
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='text', fn=_a_txt, h=90),
        dict(type='text', fn=lambda S: f"`k = {S['k']}`：`i0` 是最近一个不是 k 倍数的位置，子数组左端点必须在它右边" if 'k' in S else '', h=90),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'blue'), ('i0', 'i0', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'a = []  #': '`a` 里每项是 `[GCD, 该 GCD 的最右端点]`，只存不同的 GCD',
        'i0 = -1': '`i0` 记录最近一个「不是 `k` 的倍数」的位置',
        'if x % k': lambda S, B, r: (f'`{S.x} % {S.k} = {S.x % S.k}` ≠ 0 → ==包含 {S.x} 的子数组 GCD 一定不是 k 的倍数==，整段作废'
                                     if S.x % S.k else f'`{S.x} % {S.k} = 0`，是 k 的倍数，可以参与'),
        'a = []': '清空 `a`：之前的子数组都不能再延伸过 `{x}`',
        'i0 = i': '`i0 = {i0}`：后面子数组的左端点必须 > `i0`',
        'a.append([x, i])': '以 `i={i}` 结尾、只含 `{x}` 的子数组，GCD 就是 `{x}`：加入 `a`',
        'p[0] = gcd(p[0], x)': '把 `x={x}` 并进每个旧 GCD：`gcd` → `{p[0]}`（GCD 只会变小/不变）',
        'if a[j][0] != p[0]': lambda S, B, r: ('GCD `{}` 与前一组 `{}` ' .format(S.p[0], S.a[S.j][0]) + ('不同 → 开新的一组' if S.a[S.j][0] != S.p[0] else '相同 → 合并成一组')),
        'j += 1': '新的一组，写到位置 `j = {j}`',
        'a[j] = p': '把这一项原地放到 `a[{j}]`',
        'a[j][1] = p[1]': '相同 GCD 合并，右端点更新为 `{a[j][1]}`',
        'del a[j + 1:]': '删掉被合并掉的多余项 → `a` 只剩 {len(a)} 组不同 GCD',
        'if a[0][0] == k': lambda S, B, r: (f'`a[0][0] = {S.a[0][0]}`（最长子数组的 GCD，最小）' +
                                            (f' == `{S.k}` → 有答案' if S.a[0][0] == S.k else f' > `{S.k}` → 没有 GCD 恰为 k 的子数组')),
        'ans += a[0][1]': '左端点在 `({i0}, {a[0][1]}]` 之间的子数组 GCD 都是 `k`：共 `{a[0][1]} − ({i0})` = {a[0][1]-i0} 个，`ans` = =={ans}==',
        'return ans': '共 =={ans}== 个子数组的 GCD 等于 `{k}`',
    },
    cards=dict(
        one_liner='GCD 随左端点左移只会变小：相同 GCD 合并成一组',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['数出 `nums` 中有多少个子数组，元素的最大公因数恰好等于 `k`',
                 '示例：`[9,3,1,2,6,3], k=3` → `4`',
                 '本视频：`[6,4,3,8,2], k=2` → `3`'],
        quote='原地去重，因为相同的 GCD 都相邻在一起。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['固定右端点 `i`，左端点越往左 GCD 越小，相同的 GCD 相邻 → 按 GCD 分组，每组只存右端点',
              '不是 `k` 的倍数的元素直接清空 `a`、记下 `i0`，保证 GCD 都是 `k` 的倍数',
              '所以 `a[0][0] >= k`：只要等于 `k`，这一组就贡献 `a[0][1] - i0` 个'],
        summary=['时间 `O(n log U)`：每个数求 GCD 至多减半 `log U` 次',
                 '`a` 里最多 `log U` 组，去重要先把新元素 append 再统一求 GCD',
                 '易错：`a[0][1] - i0` 的 `i0` 是最近不合法位置；计数要用 `a[0]`（最长的）',
                 '另一种写法：方法一暴力枚举，遇到 `g % k` 就 break，`O(n²)`'],
    ),
)
