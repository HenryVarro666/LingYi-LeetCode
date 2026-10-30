CONFIG = dict(
    num=3020, title='子集中元素的最大数量', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 枚举 x 并连续平方',
    code='''
class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        cnt = Counter(nums)

        ans = (cnt[1] - 1) | 1  # 保证 ans 是奇数（奇数不变，偶数减一）
        del cnt[1]

        for x in cnt:
            res = 0
            while cnt.get(x, 0) >= 2:  # 用 get 而不是 []，避免把不在 nums 中的数插入 cnt
                res += 2
                x *= x
            ans = max(ans, res + (1 if x in cnt else -1))

        return ans
''',
    call='Solution().maximumLength([1,1,1,2,2,4,4,16,5])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=190),
        dict(type='map', var='cnt', label='cnt（1 已删除）', fmt=lambda k, v: f'{k}: {v}', h=250, font=30),
        dict(type='text', h=90, size=28,
             fn=lambda S: (f"`x = {S['x']}`，已配对 `res = {S['res']}`" if 'res' in S and 'x' in S else '')),
    ],
    watch=['x', 'res', ('ans', 'ans', 'green')],
    captions={
        'ans = (cnt[1]': '全 1 序列：奇数个就全选，偶数个去掉一个 → `ans = {ans}`',
        'del cnt[1]': '1 的平方还是 1，已单独处理，从 `cnt` 里删掉',
        'for x in cnt': '枚举 `x = {x}` 作为序列最小的数',
        'res = 0': '`res` 统计两侧成对的个数，从 0 开始',
        'while cnt.get': '`cnt[{x}] = {cnt.get(x, 0)}`：{"至少有 2 个，能放在两侧 → 继续" if cnt.get(x, 0) >= 2 else "不足 2 个，停止"}',
        'res += 2': '两侧各放一个 `{B.x}`：`res` → {res}',
        'x *= x': '往中间走一步：`x` 平方为 `{x}`',
        'ans = max': '中间放 `{x}`：{"它在 nums 中，+1" if x in cnt else "它不在 nums 中，去掉一个 x^(k/2)，-1"} → `ans = max({B.ans}, {res + (1 if x in cnt else -1)})` = =={ans}==',
        'return ans': '最大子集大小 =={ans}==',
    },
    cards=dict(
        one_liner='枚举 x，沿着 x、x^2、x^4 一路平方，看哪一层不足 2 个',
        complexity='时间 `O(n log log U)`，空间 `O(n)`',
        problem=['从 `nums` 选子集，排成 `[x, x^2, x^4, …, x^k, …, x^4, x^2, x]`，`k` 是 2 的幂',
                 '求这样的子集最大有多少个元素',
                 '本视频：`[1,1,1,2,2,4,4,16,5]` → `5`（`2,4,16,4,2`）'],
        quote='暴力枚举 nums 中的数，作为 x，然后看 x^2,x^4,… 在 nums 中的个数，直到 x^k 的个数不足 2 个为止。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x ≥ 2` 时平方增长极快，`10^9` 以内至多平方 4 次，所以直接暴力枚举',
              '个数 ≥ 2 才能放在两侧；不足 2 个时，若该数还在 nums 里，放正中间 +1，否则去掉一个 -1',
              '`x = 1` 要特判：奇数个全选，偶数个少选一个'],
        summary=['时间 `O(n log log U)`，空间 `O(n)`',
                 '易错：用 `cnt.get` 而不是 `cnt[]`，避免往 `cnt` 里插入新键',
                 '易错：`x = 1` 平方永远是 1，必须特判，否则死循环',
                 '另有 `O(n)` 写法：若 `sqrt(x)` 已有 2 个，就跳过 `x`，不重复计算'],
    ),
)
