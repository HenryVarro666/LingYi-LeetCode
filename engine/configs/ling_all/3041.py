def _txt(S):
    if 'x' not in S:
        return '`f[x]` = 子序列最后一个数是 x 时的最大长度（排序后是一段连续值）'
    x = S['x']
    return f"当前 `x = {x}`：不加一 → 接在 `f[{x-1}]` 后；加一变 `{x+1}` → 接在 `f[{x}]` 后"


CONFIG = dict(
    num=3041, title='修改数组后最大化数组中的连续元素数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排序 + 子序列 DP（f[x] 哈希表）',
    tags=['灵神题单', '难度分 2231'],
    code='''
class Solution:
    def maxSelectedElements(self, nums: List[int]) -> int:
        nums.sort()
        f = defaultdict(int)
        for x in nums:
            f[x + 1] = f[x] + 1
            f[x] = f[x - 1] + 1
        return max(f.values())
''',
    call='Solution().maxSelectedElements([2,1,5,1,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（排序后，从左到右处理）', h=190, cell=100),
        dict(type='map', var='f', label='f[x]：以 x 结尾的最长连续子序列', fmt=lambda k, v: f'{k}: {v}', h=200, font=30),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    skip=['for x in nums'],
    watch=[('x', 'x', 'pink')],
    captions={
        'nums.sort': '先排序：选出的数排序后相邻差 1，操作前也必然是递增顺序，所以可以当子序列做',
        'f[x + 1] =': '`x` 加一变成 `{x+1}`，接在以 `{x}` 结尾的后面：`f[{x+1}]` = `f[{x}] + 1` = =={f[x+1]}==（==必须先算这行==，否则同一个 x 会被用两次）',
        'f[x] = f[x - 1] + 1': '`x` 不操作，接在以 `{x-1}` 结尾的后面：`f[{x}]` = `f[{x-1}] + 1` = =={f[x]}==',
        'return': '答案是所有 `f` 值里最大的：=={ret}==',
    },
    cards=dict(
        one_liner='先排序，再当成子序列 DP：每个数可加一也可不加',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个数可以 ==增加至多 1==，然后选若干个数，排序后要 ==值连续==',
                 '求最多能选多少个数',
                 '示例：`[2,1,5,1,1]` → `3`（变成 1,2,3）'],
        quote='把数组排序。设我们选的元素在排序后为 b，那么有 b[i] + 1 = b[i+1]，这意味着 b 中元素在操作前，必然有 b[i] <= b[i+1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，选的数是 `nums` 的一个子序列，定义 `f[x]`：以 x 结尾的最大长度',
              '操作：`x+1` 接在 `x` 后：`f[x+1] = f[x] + 1`；不操作：`f[x] = f[x-1] + 1`',
              '同一个数不能既加一又不加一：==先更新 f[x+1]，再更新 f[x]=='],
        summary=['时间 `O(n log n)`（瓶颈是排序），空间 `O(n)`',
                 '易错：更新顺序反了，会让一个数被重复使用（`[1,2,2]` 会算出 3）',
                 '重复的数：每个相同的 x 依次推进 `f[x]`、`f[x+1]`，自然实现「一个不动、一个加一」',
                 '同类：合法子序列 DP（§7.4），用 `f[x]` 按「结尾的值」记状态'],
    ),
)
