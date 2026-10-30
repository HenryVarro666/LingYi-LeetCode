CONFIG = dict(
    num=3224, title='使差值相等的最少数组改动次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组统计每个 X 的代价',
    tags=['灵神题单', '常用数据结构', '难度分 1996'],
    code='''
class Solution:
    def minChanges(self, nums: List[int], k: int) -> int:
        n = len(nums)
        d = [0] * (k + 2)
        for i in range(n // 2):
            p, q = nums[i], nums[n - 1 - i]
            if p > q:  # 保证 p <= q
                p, q = q, p
            x = q - p
            mx = max(q, k - p)
            # [0, x-1] 全部 +1：把 q-p 改成小于 x 的，只需要改 p 或 q 中的一个数
            d[0] += 1
            d[x] -= 1
            # [x+1, mx] 全部 +1：把 q-p 改成大于 x 小于等于 mx 的，也只需要改 p 或 q 中的一个数
            d[x + 1] += 1
            d[mx + 1] -= 1
            # [mx+1, k] 全部 +2：把 q-p 改成大于 mx 的，p 和 q 都需要改
            d[mx + 1] += 2
        return min(accumulate(d))
''',
    call='Solution().minChanges([1,0,1,2,4,3], 4)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = i，粉 = n-1-i，两端配对）',
             pointers={'i': 'blue', 'n - 1 - i': 'pink'}, h=210),
        dict(type='text', fn=lambda S: ('' if 'p' not in S else f"这一对 `p={S['p']}, q={S['q']}`" + (f"：原差值 `x={S['x']}`" if S.get('_line', 0) >= 9 else '') + (f"，改一个数最大差值 `mx={S['mx']}`" if S.get('_line', 0) >= 10 else '')), h=60),
        dict(type='array', var='d', label='d（差分数组：d 的前缀和 = 把所有差值改成 X 的次数）', h=180, cell=90),
    ],
    watch=['i', 'p', 'q', 'x', 'mx'],
    captions={
        'd = [0]': '`d` 是差分数组，长度 `k+2`：`mx+1` 最大可以到 `k+1`',
        'for i in range': '一共 `n/2` 对 `(nums[i], nums[n-1-i])`，逐对处理',
        'p, q = nums[i]': '取第 `{i}` 对：`p={p}`，`q={q}`',
        'if p > q': '要保证 `p <= q`，这样 `q-p` 才是差值',
        'x = q - p': '这一对原本的差值 `{q} - {p}` 是 =={x}==：把 X 改成它不用动',
        'mx = max': '改一个数能凑出的最大差值：改 p 到 0 得 `q`，改 q 到 k 得 `k-p`，取大的得 `mx` 为 =={mx}==',
        'd[0] += 1': '`[0, x-1]` 这段 X 要改 1 个数：`d[0]` 加 1（区间起点）',
        'd[x] -= 1': '从 `x` 开始这段结束：`d[{x}]` 减 1（区间终点后一位）',
        'd[x + 1] += 1': '`[x+1, mx]` 也只改 1 个数：`d[{x+1}]` 加 1',
        'd[mx + 1] -= 1': '超过 `mx` 就不止改 1 个：`d[{mx+1}]` 减 1',
        'd[mx + 1] += 2': '`[mx+1, k]` 要改 2 个数：`d[{mx+1}]` 再加 2',
        'return': '`accumulate(d)` 求前缀和得到每个 X 的最少改动次数，取最小 = =={ret}==',
    },
    cards=dict(
        one_liner='把每一对「改成各个 X 要改几次」用差分叠加起来',
        complexity='时间 `O(n+k)`，空间 `O(k)`',
        problem=['`n` 为偶数，每次可把任一元素改成 `0..k` 内任意整数',
                 '要让所有 `|a[i] - a[n-1-i]|` 都等于同一个 `X`，求最少改动次数',
                 '示例：`nums=[1,0,1,2,4,3], k=4` → `2`'],
        quote='把这些操作次数加到 minModify 数组中。这可以用差分数组实现。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['每对 `(p,q)` 对不同的 `X`：`X=q-p` 改 0 个，`X<=mx` 改 1 个，更大改 2 个',
              '这三段都是区间加：`[0,x-1]+1`、`[x+1,mx]+1`、`[mx+1,k]+2`',
              '用差分 `d` 累加所有对，前缀和后取最小值'],
        summary=['时间 `O(n+k)`，空间 `O(k)`',
                 '差分数组要开 `k+2`：`mx+1` 可以等于 `k+1`',
                 '`d[x]` 和 `d[x+1]` 两处衔接起来，保证 `X=x` 这一点的代价是 0',
                 '方法一：枚举 X，用 `cnt` 和 `cnt2` 两个计数数组，思路等价'],
    ),
)
