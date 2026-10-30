def _txt(S):
    if 'c' not in S:
        return '`f[x]` = 以 x 结尾的好子序列元素和；`cnt[x]` = 这类子序列的个数'
    x = S['x']
    return (f"`c = cnt[{x-1}] + cnt[{x+1}] + 1` = ==`{S['c']}`==：新增 {S['c']} 个以 {x} 结尾的子序列；"
            f"每个都多一个 `{x}`")


CONFIG = dict(
    num=3351, title='好子序列的元素之和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='f[x] 元素和 + cnt[x] 个数',
    tags=['灵神题单', '难度分 2086'],
    code='''
class Solution:
    def sumOfGoodSubsequences(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        mx = max(nums) + 2
        f = [0] * mx
        cnt = [0] * mx
        for x in nums:
            c = cnt[x - 1] + cnt[x + 1] + 1
            f[x] = (f[x] + f[x - 1] + f[x + 1] + x * c) % MOD
            cnt[x] = (cnt[x] + c) % MOD
        return sum(f) % MOD
''',
    call='Solution().sumOfGoodSubsequences([1,2,1,2])',
    expect=33,
    views=[
        dict(type='array', var='nums', label='nums（从左到右处理，x = 当前数）', h=170, cell=100,
             color=lambda S, i, v: None),
        dict(type='array', var='f', label='f[x]：以 x 结尾的子序列元素和', h=190, cell=100,
             pointers={'x': 'pink'}),
        dict(type='array', var='cnt', label='cnt[x]：以 x 结尾的子序列个数', h=190, cell=100,
             pointers={'x': 'pink'}),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    watch=[('x', 'x', 'pink'), ('c', 'c', 'cyan')],
    captions={
        'mx = max': '下标要访问 `x+1`，数组开到 `max + 2` = `{mx}`，用数组代替哈希表',
        'c = cnt': '`x = {x}` 可接在 `{x-1}` 或 `{x+1}` 结尾的子序列后，再加上自己单独一个：`{cnt[x-1]} + {cnt[x+1]} + 1` = =={c}==',
        'f[x] = ': '不选 `f[x]`={B.f[x]}；接 `x-1`：`f[{x-1}]`={f[x-1]}；接 `x+1`：`f[{x+1}]`={f[x+1]}；这 {c} 个子序列每个多一个 `{x}`：`{x}×{c}` → `f[{x}]` = =={f[x]}==',
        'cnt[x] = ': '以 `{x}` 结尾的子序列又多了 {c} 个：`cnt[{x}]` = =={cnt[x]}==',
        'return': '答案 = 所有结尾的元素和之和 = =={ret}==',
    },
    cards=dict(
        one_liner='f[x] 记元素和，cnt[x] 记个数，从倒数第二个数转移',
        complexity='时间 `O(n+U)`，空间 `O(n+U)`，`U = max(nums)`',
        problem=['子序列中相邻两数 ==绝对差恰好为 1== 就是好子序列，单个元素也是',
                 '求所有好子序列的 ==元素和==，对 `10^9+7` 取模',
                 '示例：`[1,2,1]` → `14`；本视频：`[1,2,1,2]`'],
        quote='定义 $f[x]$ 表示以元素 $x$ 结尾的子序列的元素之和。子序列的倒数第二个数是 $x-1$ 或者 $x+1$。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新来的 `x` 接在所有以 `x±1` 结尾的子序列后面，再加上单独的 `x`',
              '新增 `c` 个子序列：原有元素和 `f[x±1]`，再额外加上 `c` 个 `x`',
              '同时 `cnt[x] += c`，下一个数要用'],
        summary=['时间 `O(n+U)`，空间 `O(n+U)`',
                 '易错：==先算 c，再更新 f[x]==，f 和 cnt 的更新都要取模',
                 '`x-1`、`x+1` 越界：数组开 `max+2`，且 `x=0` 时 `x-1=-1` 取到末尾恒为 0',
                 '题解首选哈希表写法（defaultdict），数组版效率更高；这里演示数组版'],
    ),
)
