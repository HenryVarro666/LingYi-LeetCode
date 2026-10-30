CONFIG = dict(
    num=3514, title='不同 XOR 三元组的数目 II', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='先算两数异或集合，再异或第三个数',
    tags=['灵神题单·位运算', '灵神题单·数学算法'],
    code='''
class Solution:
    def uniqueXorTriplets(self, nums: List[int]) -> int:
        nums = list(set(nums))  # 优化：去重，减少循环次数
        st = {x ^ y for x, y in combinations(nums, 2)} | {0}
        return len({xy ^ z for xy in st for z in nums})
''',
    call='Solution().uniqueXorTriplets([6,7,8,9])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（去重后）', h=150),
        dict(type='set', var='st', fmt=lambda x: str(x), label='st：任意两数异或的所有可能值（含 0）', h=300),
        dict(type='text', fn=lambda S: '`i<=j<=k` 可以重复选，异或又满足交换律 → 等价于 ==从 nums 里可重复地选三个数==' if 'st' not in S else
             f"两数异或的值只有 `{len(S['st'])}` 个，远小于 n²；再逐个异或 nums 里的 z 就得到三数异或", size=26),
    ],
    watch=[('nums', 'nums'), ('|st|', "len(st) if 'st' in S else '-'", 'cyan')],
    captions={
        'nums = list(set': '先去重：`nums = {nums}`，相同的数重复选没有新结果，循环更少',
        'st = {': '`x ^ y` 枚举两个不同数的异或，再并上 `{{0}}`（选同一个数两次异或为 0）：`st = {sorted(st)}`',
        'return len': '`st` 里每个值 `xy` 再异或 `nums` 里的 `z`，得到所有三数异或；用集合去重，答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='异或交换律：i<=j<=k 等于可重复地任选三个数',
        complexity='时间 `O(n(n+U))`，空间 `O(U)`',
        problem=['给整数数组 `nums`，三元组 `(i,j,k)` 满足 `i<=j<=k`，值为三数异或',
                 '求所有三元组中不同异或值的个数',
                 '示例：`[6,7,8,9]` → `4`（值为 6、7、8、9）'],
        quote='任意两数异或的所有可能值，在本题的数据范围下 ≤ 2^11-1=2047，远远小于 n^2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i<=j<=k` 是个幌子：异或可交换，等价于从 nums 里可重复选三个数',
              '三重循环太慢：先用二重循环算出两数异或的==所有可能值==，最多 2048 个',
              '再用「两数异或值 × nums」的二重循环得到三数异或，集合去重后数个数'],
        summary=['时间 `O(n(n+U))`，`U = max(nums)`；空间 `O(U)`',
                 '`| {0}` 不能漏：同一个数选两次，异或为 0，相当于只选了一个数',
                 '先 `set` 去重能减少循环次数',
                 '另解：用异或 FWT 求出三数异或恰好为 i 的个数 cnt3，数 cnt3[i] > 0 的个数，时间 `O(n+U log U)`'],
    ),
)
