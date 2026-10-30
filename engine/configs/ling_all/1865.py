CONFIG = dict(
    num=1865, title='找出和为指定值的下标对', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='哈希表维护 nums2 的出现次数', tags=[],
    code='''
class FindSumPairs:
    def __init__(self, nums1: List[int], nums2: List[int]):
        self.nums1 = nums1
        self.nums2 = nums2
        self.cnt = Counter(nums2)

    def add(self, index: int, val: int) -> None:
        # 维护 nums2 每个元素的出现次数
        self.cnt[self.nums2[index]] -= 1
        self.nums2[index] += val
        self.cnt[self.nums2[index]] += 1

    def count(self, tot: int) -> int:
        ans = 0
        for x in self.nums1:
            ans += self.cnt[tot - x]
        return ans
''',
    call='''f = FindSumPairs([1, 2, 3], [1, 4, 2, 5])
out = [f.count(7)]
f.add(2, 2)
out.append(f.count(7))
f.add(0, 1)
out.append(f.count(4))
out''',
    expect=[2, 3, 1],
    views=[
        dict(type='array', var='self.nums1', label='nums1（遍历它）', h=200, cell=70),
        dict(type='array', var='self.nums2', label='nums2（会被 add 修改）', h=200, cell=70),
        dict(type='map', var='self.cnt', label='cnt（nums2 中每个数的出现次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=30),
        dict(type='text', fn=lambda S: (f"`tot = {S['tot']}`：累计 `ans = {S['ans']}`" if 'tot' in S and 'ans' in S else ''), size=30),
    ],
    watch=['x', 'tot', ('ans', 'ans', 'green'), 'index', 'val'],
    captions={
        'self.cnt = Counter': '用哈希表统计 nums2 每个数出现几次：`{dict(self.cnt)}`',
        'self.cnt[self.nums2[index]] -= 1': '旧值 `{self.nums2[index]}` 要离开：它的次数减 1',
        'self.nums2[index] += val': '`nums2[{index}]` 加上 `{val}`，变成 `{self.nums2[index]}`',
        'self.cnt[self.nums2[index]] += 1': '新值 `{self.nums2[index]}` 的次数加 1，cnt 与 nums2 保持一致',
        'ans = 0': '统计满足 `nums1[i] + nums2[j] == {tot}` 的对数',
        'ans += self.cnt': '`x = {x}`：需要 nums2 中有 `{tot} − {x} = {tot - x}`，有 `{self.cnt[tot - x]}` 个 → `ans` = =={ans}==',
        'return ans': '遍历完 nums1，共 =={ans}== 对',
    },
    cards=dict(
        one_liner='本质是两数之和：哈希表记 nums2 的出现次数',
        complexity='add `O(1)`，count `O(n)`',
        problem=['实现 `add(index, val)`：`nums2[index] += val`',
                 '实现 `count(tot)`：数出 `nums1[i] + nums2[j] == tot` 的下标对数',
                 '示例：`nums1=[1,2,3]`，`nums2=[1,4,2,5]`，`count(7)` → `2`'],
        quote='本质是 1. 两数之和。遍历 nums1 中的数……计算 nums2 中有多少个数等于 tot - x。用哈希表维护 nums2 中每个元素的出现次数，即可 O(1) 获知。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `x = nums1[i]`，只需要知道 nums2 里有几个 `tot - x`',
              '哈希表 `cnt` 记录 nums2 每个值的次数，查询 `O(1)`',
              '遍历 nums1 而不是 nums2：nums1 最长 1000，比 nums2 的 10^5 小得多',
              'add 时旧值次数减 1、新值次数加 1'],
        summary=['初始化 `O(m)`，add `O(1)`，count `O(n)`，n 是 nums1 长度',
                 'add 要先减旧值再加新值，别忘了同时改 `nums2` 本身',
                 '代码没有删除次数为 0 的键，空间 `O(m+q)`',
                 '写法二：也给 nums1 建 Counter，count 时枚举不同的 x 再乘 `c1`'],
    ),
)
