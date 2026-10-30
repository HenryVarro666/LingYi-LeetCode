CONFIG = dict(
    num=1304, title='和为零的 N 个不同整数', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='对称构造',
    tags=['灵神题单', '难度分 1167'],
    code='''
class Solution:
    def sumZero(self, n: int) -> List[int]:
        a = [0] * n
        m = n // 2
        for i in range(m):
            a[i] = i + 1
            a[i + m] = -i - 1
        return a
''',
    call='Solution().sumZero(7)',
    expect=[1, 2, 3, -1, -2, -3, 0],
    views=[
        dict(type='text', fn=lambda S: (f"已配对：`{S['i']+1}` + `{-S['i']-1}` = ==0==" if 'i' in S and 'a' in S and S['a'][S['i'] + S['m']] != 0 else '成对放 `x` 和 `-x`，和恒为 0；n 为奇数时中间留一个 0')),
        dict(type='array', var='a', pointers={'i': 'blue', 'i+m': 'pink'}, h=300,
             color=lambda S, i, v: 'green' if v != 0 else None),
    ],
    watch=['n', 'm', 'i'],
    captions={
        'a = [0] * n': '先放 `n = {n}` 个 0 当占位',
        'm = n // 2': '`m = n // 2 = {m}`：一共能凑 `{m}` 对相反数；n 是奇数时最后一格保持 ==0==',
        'for i in range': '第 `{i}` 对：正数放前半、负数放后半',
        'a[i] = i + 1': '`a[{i}] = {i} + 1 = {a[i]}`：前半部分放正数 `1 .. m`',
        'a[i + m]': '`a[{i} + {m}] = -{i} - 1 = {a[i+m]}`：后半部分放对应的相反数，和 `{a[i]}` 抵消',
        'return a': '前 `2m` 位两两抵消，剩下的 0 不影响和 → 返回 `{a}`',
    },
    cards=dict(
        one_liner='x 和 -x 成对出现，和恒为 0',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['给定 `n`，返回任意 `n` 个互不相同的整数，和为 `0`',
                 '示例：`n = 5` → `[-7,-1,1,3,4]` 等都行',
                 '本视频：`n = 7`'],
        quote='由于 x + (-x) = 0 恒成立，可以把 1 和 -1，2 和 -2，3 和 -3 等成对添加到答案中。如果 n 是奇数，就再加个 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`m = n // 2` 对：前 `m` 格放 `1..m`，接着 `m` 格放 `-1..-m`',
              '奇数时多出的最后一格是初始的 `0`，不用再处理',
              '数互不相同，因为绝对值各不相同且 0 只出现一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`a[i + m]` 的下标别写成 `a[m - i]`，要和 `a[i]` 配对',
                 '题解还给了写法二 `list(range(-m, m + 1))` 和方法二 `[-S, 1, ..., n-1]`（S 为等差数列和）'],
    ),
)
