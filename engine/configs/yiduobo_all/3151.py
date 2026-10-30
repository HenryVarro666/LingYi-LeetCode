CONFIG = dict(
    num=3151, title='特殊数组 I', difficulty='Easy', category='模拟',
    author='yiduobo', technique='相邻转 01 数组 + 前缀和',
    code='''
class Solution(object):
    def isArraySpecial(self, nums, queries):

        s = [0]
        for index in range(1, len(nums)):
            s.append(s[-1])
            if (nums[index] + nums[index - 1]) % 2 == 0:
                s[-1] += 1
        
        return [s[x] == s[y] for x, y in queries]
''',
    call='Solution().isArraySpecial([4, 3, 1, 6, 5], [[0, 1], [1, 3], [0, 4]])',
    expect=[True, False, False],
    views=[
        dict(type='array', var='nums', label='nums', cell=100, h=220, pointers={'index': 'blue'},
             color=lambda S, i, v: 'orange' if v % 2 == 0 else 'blue'),
        dict(type='array', var='s', label='s（前缀和）', cell=100, h=170),
        dict(type='text', h=80, size=28, fn=lambda S: f"`nums[{S['index']}] + nums[{S['index']-1}] = {S['nums'][S['index']] + S['nums'][S['index']-1]}`" + ('，==和为偶数 → 奇偶相同=='  if (S['nums'][S['index']] + S['nums'][S['index']-1]) % 2 == 0 else '，和为奇数 → 奇偶不同') if 'index' in S and 's' in S and S['index'] >= 1 and S['index'] < len(S['nums']) else ''),
    ],
    watch=[('index', 'index', 'blue'), ('s[-1]', 's[-1]', 'green')],
    captions={
        's = [0]': '`s[k]` 记前 k 个相邻对里“奇偶相同”的个数，先放一个 0',
        's.append(s[-1])': '先把上一个前缀和抄过来：`s = {s}`',
        'if (nums[index]': lambda S, B, ret: (f'`{S.nums[S.index]} + {S.nums[S.index-1]}` 是偶数 → 两数奇偶相同，这一对记 1' if (S.nums[S.index] + S.nums[S.index-1]) % 2 == 0
                                              else f'`{S.nums[S.index]} + {S.nums[S.index-1]}` 是奇数 → 奇偶不同，这一对记 0'),
        's[-1] += 1': '这一对不合格，`s[-1]` 加一 → `{s}`',
        'return [': '每个询问 `[x, y]`：区间 `x..y` 内相邻对的个数 = `s[y] − s[x]`，==为 0 才是特殊数组==，即 `s[x] == s[y]`。结果 `{ret}`',
    },
    cards=dict(
        one_liner='相邻对转成 0/1，再用前缀和判断区间和是否为 0',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['相邻元素奇偶都不同的数组是特殊数组',
                 '3151 原题只问整个数组；原文代码是 3152 的通用写法（带 `queries`）',
                 '本视频：`nums = [4,3,1,6,5]`，询问 `[0,1] [1,3] [0,4]`；整个数组即 `[0, n−1]`'],
        quote='先根据相邻元素的具体情况将数组转化为01数组……得到这样一个01数组之后，其符合条件的子数组中的元素必然都为0，即子数组对应的区间和为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻两数和为偶数 ⇔ 奇偶相同，这一对记 1，否则记 0',
              '子数组是特殊数组 ⇔ 它里面的相邻对全是 0 ⇔ 区间和为 0',
              '区间和用前缀和 `s` 求，`s[x] == s[y]` 即为 0'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '`s[k]` 对应前 k 个相邻对，下标比 `nums` 对应的相邻对错开一位，所以区间是 `s[y] − s[x]`',
                 '3151 只需判断整个数组，等价于查询 `[0, n−1]`，答案取第一个',
                 '对比灵神：灵神直接 `all(...)` 遍历一遍；yiduobo 的做法能扩展到 3152 的多次询问',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
