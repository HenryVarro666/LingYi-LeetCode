def _txt(S):
    if 'cx' not in S or 's' not in S:
        return '把二进制看成集合：`c(x|y) + c(x&y) = c(x) + c(y)`，只需统计 1 的个数'
    cx, k = S['cx'], S['k']
    need = k - cx
    return f"x 有 `{cx}` 个 1 → y 至少要有 `{max(need, 0)}` 个 1；这样的 y 共 ==`{S['s']}`== 种（后缀和 s）"


CONFIG = dict(
    num=2354, title='优质数对的数目', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='恒等式 + 计数 + 后缀和',
    tags=['灵神题单·位运算', '位运算 · 六、恒等式', '难度分 2076'],
    code='''
class Solution:
    def countExcellentPairs(self, nums: List[int], k: int) -> int:
        cnt = [0] * 30
        for x in set(nums):
            cnt[x.bit_count()] += 1
        ans = 0
        s = sum(cnt[k:])
        for cx, ccx in enumerate(cnt):
            ans += ccx * s
            if 0 <= k - 1 - cx < 30:  # 下一轮循环 cx 是 cx+1
                s += cnt[k - 1 - cx]
        return ans
''',
    call='Solution().countExcellentPairs([1, 2, 3, 1], 3)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（先 set 去重，再数每个数的 1）', h=170),
        dict(type='array', var='cnt', label='cnt[c]：二进制里有 c 个 1 的数有几个', h=240,
             pointers={'cx': 'blue'},
             color=lambda S, i, v: 'green' if v else None,
             dim=lambda S, i, v: i > 6 and v == 0),
        dict(type='text', fn=_txt, size=30, h=130),
    ],
    watch=[('cx', 'cx', 'blue'), ('ccx', 'ccx', 'cyan'), ('s', 's', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'cnt[x.bit_count()] += 1': '`{x}` 的二进制有 `{x.bit_count()}` 个 1 → `cnt[{x.bit_count()}]` 变成 =={cnt[x.bit_count()]}==',
        's = sum(cnt[k:])': '`cx = 0` 时 y 至少要有 `k = {k}` 个 1：把 `cnt[{k}:]` 加起来 → `s = {s}`',
        'ans += ccx * s': '选 x：`{ccx}` 个数 × 配对的 y：`{s}` 个 = `{ccx * s}`（乘法原理）→ `ans` = =={ans}==',
        'if 0 <= k - 1 - cx < 30': lambda S, B, r: (f"下一轮 `cx = {S.cx + 1}`，y 的门槛降到 `{S.k - 1 - S.cx}` 个 1：恰有 `{S.k - 1 - S.cx}` 个 1 的数也能当 y，要并入 `s`"
                                                    if 0 <= S.k - 1 - S.cx < 30 else f"`k - 1 - cx = {S.k - 1 - S.cx}` 已出界：没有新的档位并入 `s`"),
        's += cnt[k - 1 - cx]': '恰有 `{k - 1 - cx}` 个 1 的数也能当 y：`s` 增加 `{cnt[k - 1 - cx]}` → =={s}==',
    },
    max_steps=44,
    cards=dict(
        one_liner='|A∪B| + |A∩B| = |A| + |B|：只需比较 1 的个数',
        complexity='时间 `O(n+U)`，空间 `O(n+U)`，`U = 30`',
        problem=['数对 `(x, y)` 都在 `nums` 中，`x|y` 与 `x&y` 的 1 的个数之和 `>= k` 就是优质数对',
                 '`(a,b)` 和 `(b,a)` 算两个，`x == y` 也允许；求不同数对的个数',
                 '示例：`nums = [1,2,3,1]`，`k = 3` → `5`'],
        quote='把二进制数看成集合，根据容斥原理 |A ∪ B| = |A| + |B| - |A ∩ B|，得 |A ∪ B| + |A ∩ B| = |A| + |B|。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一位上都是 1 被数两次，只有一个 1 被数一次，所以总数就是 `c(x) + c(y)`',
              '去重后按 `c(x)` 分组计数，条件变成 `c(x) + c(y) >= k`，用乘法原理累加',
              '`cx` 从小到大时，y 的门槛 `k - cx` 越来越低，用后缀和 `s` 维护'],
        after=[dict(heading='另一种写法', lines=[
            '题解先给了二重循环：枚举 `cnt` 里的两个分组，满足 `cx + cy >= k` 就加 `ccx * ccy`',
            '时间 `O(n + U^2)`；再用前缀和 / 后缀和优化成 `O(n + U)`，即本视频的写法'])],
        summary=['时间 `O(n+U)`，空间 `O(n+U)`',
                 '易错点：必须先对 `nums` 去重，否则重复数会被多算',
                 '`s` 初值是 `sum(cnt[k:])`，对应 `cx = 0`；若 `k > 30` 则为 0',
                 '同类题：用恒等式把位运算变成「数 1 的个数」'],
    ),
)
