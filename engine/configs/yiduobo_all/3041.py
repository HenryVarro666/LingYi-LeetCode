def _txt(S):
    if 'v' not in S:
        return '`f[x]` = 以 x 结尾的最大连续数组长度；`cnt` = v 出现次数'
    v, c = S['v'], S['cnt']
    if c == 1:
        return f"`v = {v}` 只出现 1 次：要么变 `{v+1}` 接 `f[{v}]`，要么不变接 `f[{v-1}]`（二选一，先算 v+1）"
    return f"`v = {v}` 出现 {c} 次：一个不变、一个加一，可同时用上：`f[{v+1}]` 可从 `f[{v-1}] + 2` 得来"


CONFIG = dict(
    num=3041, title='修改数组后最大化数组中的连续元素数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按值计数 · f[x] 数组 DP',
    tags=['灵神题单', '难度分 2231'],
    code='''
class Solution(object):
    def maxSelectedElements(self, nums):

        freq = Counter(nums)
        ma = max(freq.keys())
        f = [0] * (ma + 2)

        for v, cnt in sorted(freq.items()):
            if cnt == 1:
                f[v + 1] = f[v] + 1
                f[v] = f[v - 1] + 1
            else:
                f[v] = f[v - 1] + 1
                f[v + 1] = f[v] + 1

        return max(f)
''',
    call='Solution().maxSelectedElements([2,1,5,1,1])',
    expect=3,
    views=[
        dict(type='map', var='freq', label='freq（各数出现次数）', fmt=lambda k, v: f'{k}: ×{v}', h=130, font=28),
        dict(type='array', var='f', label='f[x]：以 x 结尾的最大连续长度（下标 = 数值）', h=230, cell=90,
             pointers={'v': 'pink'}),
        dict(type='text', h=100, size=26, fn=_txt),
    ],
    watch=[('v', 'v', 'pink'), ('cnt', 'cnt', 'cyan')],
    captions={
        'freq = Counter': '数值范围在 `10^6` 内，先统计每个数出现几次，再按数值从小到大处理',
        'f = [0]': '`f` 数组下标就是数值，多开 2 位给 `v + 1`',
        9: lambda S, B, r: f'`v = {S.v}` 出现了 `{S.cnt}` 次' + ('：只有一个，二选一' if S.cnt == 1 else '：两个 `' + str(S.v) + '` 可以一个不变、一个加一'),
        10: '只有一个 `{v}`：变成 `{v+1}` 接在 `f[{v}]` 后面：`f[{v+1}]` = =={f[v+1]}==（==先算它==，再改 f[v]）',
        11: '`{v}` 不变，接在 `f[{v-1}]` 后面：`f[{v}]` = =={f[v]}==',
        13: '`{v}` 先不变，接在 `f[{v-1}]` 后面：`f[{v}]` = =={f[v]}==',
        14: '另一个 `{v}` 加一变 `{v+1}`，接在刚算好的 `f[{v}]` 后：`f[{v+1}]` = =={f[v+1]}==（相当于 `f[{v-1}] + 2`）',
        'return max(f)': '答案是 `f` 里的最大值：=={ret}==',
    },
    cards=dict(
        one_liner='按值统计次数：出现一次二选一，出现多次两个都能用',
        complexity='时间 `O(n log n + U)`，空间 `O(U)`',
        problem=['每个数可以 ==增加至多 1==，然后选若干个数，排序后要 ==值连续==',
                 '求最多能选多少个数',
                 '示例：`[2,1,5,1,1]` → `3`'],
        quote='数值的取值范围在10^6之内，因此可以考虑使用f[x]表示以x结尾的最大连续数组长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['统计每个数的次数，从小到大遍历数值 `v`',
              '次数为 1：先用 `f[v]+1` 更新 `f[v+1]`，再用 `f[v-1]+1` 更新 `f[v]`',
              '次数 >= 2：先 `f[v] = f[v-1]+1`，再 `f[v+1] = f[v]+1`，即用上 `f[v-1]+2`'],
        summary=['时间 `O(n log n + U)`，空间 `O(U)`，`U` 为最大值',
                 '易错：次数为 1 时两行顺序不能反，否则同一个数被用两次',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神排序后逐个元素处理；yiduobo 按「数值 + 次数」分类'],
    ),
)
