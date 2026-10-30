def _txt(S):
    if 'index' not in S:
        return ''
    i, nums = S['index'], S['nums']
    a, b = nums[i - 1], nums[i]
    return f'`{a}` 和 `{b}` 之间有 `{b} − {a} − 1` = =={b - a - 1}== 个空位，剩余 `k = {S["k"]}`，已填和 `res = {S["res"]}`'


CONFIG = dict(
    num=2195, title='向数组中追加 K 个整数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='排序去重 · 逐段填补',
    tags=['灵神题单', '数学算法', '难度分 1659'],
    code='''
class Solution(object):
    def minimalKSum(self, nums, k):

        nums.append(0)
        nums = sorted(list(set(nums)))
        res = 0
        for index in range(1, len(nums)):
            if nums[index] - nums[index - 1] - 1 >= k:
                res += (nums[index - 1] + 1 + nums[index - 1] + k) * k // 2
                return res
            else:
                res += (nums[index - 1] + 1 + nums[index] - 1) * (nums[index] - nums[index - 1] - 1) // 2
                k -= nums[index] - nums[index - 1] - 1

        if k > 0:
            res += (nums[-1] + 1 + nums[-1] + k) * k // 2
        
        return res
''',
    call='Solution().minimalKSum([5,6,12], 20)',
    expect=253,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums（头部补 0、去重、排序）', h=260),
        dict(type='text', fn=_txt, size=30, h=130),
    ],
    watch=['index', 'k', ('res', 'res', 'green')],
    captions={
        'nums.append(0)': '在头部加一个 `0`，开头那段空位 `1 … nums[0]-1` 就和中间的空位一样处理',
        'nums = sorted': '去重并从小到大排序：`nums` = =={nums}==',
        'for index': lambda S, B, ret: ('数组遍历完了' if B.get('index') == S.index else
                                        f'看 `nums[{S.index-1}] = {S.nums[S.index-1]}` 与 `nums[{S.index}] = {S.nums[S.index]}` 之间的空位'),
        'if nums[index] - nums[index - 1] - 1 >= k': '空位 `{nums[index] - nums[index-1] - 1}` 个，剩余 `k = {k}`：{"够了 → 只填前 k 个就结束" if nums[index] - nums[index-1] - 1 >= k else "不够 → 整段填满，继续往后"}',
        'res += (nums[index - 1] + 1 + nums[index] - 1)': lambda S, B, ret: (f'中间没有空位，`res` 加 0 → ==' + str(S.res) + '==' if S.nums[S.index] - S.nums[S.index-1] - 1 == 0 else
                                    f'整段 `{S.nums[S.index-1]+1} … {S.nums[S.index]-1}` 求和：首尾相加 × 个数 ÷ 2 → `res` = ==' + str(S.res) + '=='),
        'k -= nums': '用掉 `{nums[index] - nums[index-1] - 1}` 个名额，`k` 剩 =={k}==',
        'res += (nums[index - 1] + 1 + nums[index - 1] + k)': '填 `{nums[index-1]+1} … {nums[index-1]+B.k}` 共 `{B.k}` 个：等差数列求和 → `res` = =={res}==',
        'if k > 0': '遍历完数组 `k` 还剩 `{k}`：{"要从最大值之后继续追加" if k > 0 else "已经填完"}',
        'res += (nums[-1] + 1': '最大值 `{nums[-1]}` 之后追加 `{nums[-1]+1} … {nums[-1]+B.k}`：等差数列求和 → `res` = =={res}==',
        'return res': '追加的数之和 `{res}`',
    },
    cards=dict(
        one_liner='从 1 开始填没出现过的数，数据太大就按段用公式算',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['向 `nums` 追加 `k` 个没出现过、互不相同的正整数，使和最小',
                 '返回追加的 `k` 个数之和',
                 '示例：`[1,4,25,10,25]`，`k=2` → `5`',
                 '本视频：`[5,6,12]`，`k=20`'],
        quote='最优的方案肯定是从1开始，逐个向数组中追加当前数组中没出现过的数。不过由于题目中nums和k的规模都很大，直接模拟这个过程肯定是行不通的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把最小数 m 之前的 `1 … m-1` 填上，`k` 不够就只填前 `k` 个',
              '一般地：排序、头部加 `0`，对相邻两数之间的空位，用空位数和 `k` 比较',
              '遍历完 `k` 还有剩，就从最大值后面接着追加'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`set` + 新列表）',
                 '去重必须做：重复数字会让空位数变成 -1',
                 '原文为 Python 2 写法，求和公式里的 `/ 2` 已改为 `// 2`（乘积一定是偶数）',
                 '对比灵神：灵神加 `inf` 哨兵，末尾不用单独处理；yiduobo 在循环后补一段 `if k > 0`'],
    ),
)
