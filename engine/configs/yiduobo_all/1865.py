CONFIG = dict(
    num=1865, title='找出和为指定值的下标对', difficulty='Medium', category='设计',
    author='yiduobo', technique='哈希表存 nums2 次数 + 保留 nums2', tags=[],
    code='''
class FindSumPairs(object):

    def __init__(self, nums1, nums2):
        self.nums1 = nums1[:]
        self.nums2 = nums2[:]
        self.num_dict = {}
        for num in self.nums2:
            self.num_dict[num] = self.num_dict.get(num, 0) + 1

    def add(self, index, val):
        self.num_dict[self.nums2[index]] -= 1
        self.nums2[index] += val
        self.num_dict[self.nums2[index]] = self.num_dict.get(self.nums2[index], 0) + 1

    def count(self, tot):
        res = 0 
        for num in self.nums1:
            res += self.num_dict.get(tot - num, 0)
        
        return res
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
        dict(type='array', var='self.nums1', label='nums1', h=200, cell=70),
        dict(type='array', var='self.nums2', label='nums2（add 按下标改它）', h=200, cell=70),
        dict(type='map', var='self.num_dict', label='num_dict（数值 → 在 nums2 中出现次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=30),
        dict(type='text', fn=lambda S: (f"`tot = {S['tot']}`：累计 `res = {S['res']}`" if 'tot' in S and 'res' in S else ''), size=30),
    ],
    watch=['num', 'tot', ('res', 'res', 'green'), 'index', 'val'],
    captions={
        'self.nums1 = nums1[:]': '拷贝一份 nums1，不改动外面的数组',
        'self.nums2 = nums2[:]': '拷贝 nums2：add 按下标改它，所以必须自己留一份',
        'self.num_dict[num] = self.num_dict.get(num, 0)': '`{num}` 在 nums2 里又出现一次：`num_dict[{num}]` = =={self.num_dict[num]}==',
        'self.num_dict[self.nums2[index]] -= 1': '旧值 `{self.nums2[index]}` 要被改掉：哈希表里它的次数减 1',
        'self.nums2[index] += val': '`nums2[{index}]` 加 `{val}` → `{self.nums2[index]}`',
        'self.num_dict[self.nums2[index]] = ': '新值 `{self.nums2[index]}` 的次数加 1（可能是新键，所以用 get）',
        'res = 0': '统计满足 `num + nums2[j] == {tot}` 的对数',
        'res += self.num_dict': '`num = {num}`：找 nums2 里等于 `{tot} − {num} = {tot - num}` 的个数 `{self.num_dict.get(tot - num, 0)}` → `res` = =={res}==',
        'return res': '枚举完 nums1，共 =={res}== 对',
    },
    cards=dict(
        one_liner='两数之和的 online 版：哈希表数 nums2，枚举 nums1',
        complexity='add `O(1)`，count `O(n)`',
        problem=['`add(index, val)`：给 `nums2[index]` 加上 `val`',
                 '`count(tot)`：数 `nums1[i] + nums2[j] == tot` 的下标对',
                 '本视频：`nums1=[1,2,3]`，`nums2=[1,4,2,5]`'],
        quote='用哈希表来储存nums2中每个数出现的次数，然后在计算时枚举nums1中每个数num，去哈希表中查找nums2中有多少个数等于tot - num。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想双指针：要一直保持 nums2 有序，要上平衡树，太麻烦',
              '改用哈希表：值 → 次数；count 时枚举 nums1 的 `num`，查 `tot - num`',
              '进哈希表就丢了下标，而 add 按下标改，所以 nums2 本身也要保留',
              'add 时同时更新 nums2 和哈希表'],
        summary=['初始化 `O(m)`，add `O(1)`，count `O(n)`',
                 '`add` 里新值可能是新键，要用 `.get(x, 0) + 1`；旧值一定存在，直接减',
                 '`nums1[:]`、`nums2[:]` 是拷贝，避免改到调用方的数组',
                 '原文为 Python 2 风格，但在 Python 3 下同样可运行，代码未改动'],
    ),
)
