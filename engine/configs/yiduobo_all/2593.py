def _order(S):
    if 'nums' not in S:
        return ''
    pr = sorted(enumerate(S['nums']), key=lambda d: (d[1], d[0]))
    cur = (S.get('index'), S.get('v'))
    parts = []
    for idx, v in pr:
        t = f'{v}@{idx}'
        parts.append(f'==[{t}]==' if (idx, v) == cur else t)
    return '按（值，下标）排序：' + '  '.join(parts)


CONFIG = dict(
    num=2593, title='标记所有元素后数组的分数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 标记数组模拟',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def findScore(self, nums):

        n = len(nums)
        vis = [False] * n
        res = 0
        for index, v in sorted(enumerate(nums), key=lambda d:(d[1], d[0])):
            if not vis[index]:
                res += v
                vis[index] = True
                if index > 0:
                    vis[index - 1] = True
                if index < n - 1:
                    vis[index + 1] = True
        
        return res
''',
    call='Solution().findScore([2,1,3,4,5,2])',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, h=200,
             dim=lambda S, i, v: 'vis' in S and S['vis'][i] and i != S.get('index'),
             color=lambda S, i, v: 'yellow' if 'index' in S and i == S['index'] else None),
        dict(type='array', var='vis', label='vis（True = 已标记）', h=180, cell=84,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', h=100, size=26, fn=_order),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'vis = [False]': '`vis` 记录每个位置是否已被标记，先全是 `False`',
        'res = 0': '`res` 累计分数',
        'for index, v in sorted': lambda S, B, r: (f"按（值，下标）从小到大取下一个：`nums[{S.index}] = {S.v}`" if 'index' in S and S.get('_n') is None and not (B.get('index') == S.index and 'res' in B and B.get('v') == S.v) else '排序里没有更多元素了 → 全部处理完'),
        'if not vis[index]': lambda S, B, r: (f"`vis[{S.index}]` 是 `False`：这个位置没被标记，它就是当前最小的未标记数 → 选它" if not S.vis[S.index] else f"`vis[{S.index}]` 是 `True`：已被邻居标记，跳过"),
        'res += v': '选中，分数加上 `{v}`：`res = {B.res} + {v}` = =={res}==',
        'vis[index] = True': '标记自己 `vis[{index}]`',
        'if index > 0': lambda S, B, r: (f"`index = {S.index} > 0`：左边有邻居，要标记它" if S.index > 0 else "`index = 0`：左边没有元素，==不能标记 index-1==（会越界）"),
        'vis[index - 1] = True': '标记左邻居 `vis[{index - 1}]`',
        'if index < n - 1': lambda S, B, r: (f"`index = {S.index} < n - 1 = {S.n - 1}`：右边有邻居，要标记它" if S.index < S.n - 1 else f"`index = {S.index}` 是最后一个：右边没有元素，==不能标记 index+1=="),
        'vis[index + 1] = True': '标记右邻居 `vis[{index + 1}]`',
        'return res': '总分 `{res}`',
    },
    cards=dict(
        one_liner='排好序，从小到大遍历，没被标记就选，并标记左右邻居',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次选最小的未标记数（相等取下标小的）加分，并标记它和左右邻居',
                 '重复到全部被标记，求总分',
                 '示例：`[2,1,3,4,5,2]` → `7`'],
        quote='由于题目中的标记操作最多只需要标记三个位置，可以认为是O(1)的操作，因此可以直接模拟题目描述的操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['按==（数值，下标）==排序，正好对应题目的选择顺序',
              '遍历排序结果：`vis[index]` 为假才选，并标记 `index-1, index, index+1`',
              '标记最多三个位置，每一步 `O(1)`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '标记左右邻居前要判断 `index > 0`、`index < n - 1`，防止越界',
                 '排序的第二关键字是下标，保证相等时取最左边的',
                 '对比灵神：灵神方法二不排序，按严格递减段 `O(n)` 直接算'],
    ),
)
