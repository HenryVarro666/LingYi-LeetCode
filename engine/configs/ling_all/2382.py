def _present(S, idx):
    i = S.get('i')
    if i is None:
        return False
    return idx in S['removeQueries'][i:]


def _txt(S):
    if 'i' not in S or 'to' not in S:
        return '倒着看：==删除变添加==，每次把 `removeQueries[i]` 加回来，合并相邻子段'
    return f'加回下标 `{S["removeQueries"][S["i"]]}`：并入链根 `{S["to"]}`，该子段和 `sum[{S["to"]}] = ` ==`{S["sum"][S["to"]]}`=='


CONFIG = dict(
    num=2382, title='删除操作后的最大子段和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='倒序 + 并查集合并子段',
    tags=['灵神题单', '常用数据结构', '难度分 2136'],
    code='''
class Solution:
    def maximumSegmentSum(self, nums: List[int], removeQueries: List[int]) -> List[int]:
        n = len(nums)
        fa = list(range(n + 1))
        sum = [0] * (n + 1)
        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        ans = [0] * n
        for i in range(n - 1, 0, -1):
            x = removeQueries[i]
            to = find(x + 1)
            fa[x] = to  # 合并 x 和 x+1
            sum[to] += sum[x] + nums[x]
            ans[i - 1] = max(ans[i], sum[to])
        return ans
''',
    call='Solution().maximumSegmentSum([1,2,5,6,1], [0,3,2,4,1])',
    expect=[14, 7, 2, 2, 0],
    views=[
        dict(type='text', fn=_txt, h=50),
        dict(type='array', var='nums', label='nums（绿 = 已加回；灰 = 仍被删除）', h=170,
             color=lambda S, i, v: 'blue' if S.get('i') is not None and i == S['removeQueries'][S['i']] else ('green' if _present(S, i) else None),
             dim=lambda S, i, v: not _present(S, i)),
        dict(type='array', var='fa', pointers={'to': 'pink'}, label='fa[x]：x 并向右边（链根 = 幽灵火车头）', h=160,
             color=lambda S, i, v: 'pink' if i == S.get('to') else None),
        dict(type='array', var=lambda S: S['sum'] if 'sum' in S else None, label='sum[根]：该链（子段）的元素和', h=140,
             color=lambda S, i, v: 'yellow' if i == S.get('to') else None),
        dict(type='array', var='ans', label='ans：第 i 次删除后的最大子段和', h=140,
             color=lambda S, i, v: 'green' if i == S.get('i', -9) - 1 else None),
    ],
    watch=['i', 'x', 'to', ('ans', 'ans', 'green')],
    captions={
        'fa = list': '并查集：`fa[x] = x` 表示 x 是链根。数组多开一位，当作最右边的「幽灵火车头」',
        'sum = [0]': '`sum[根]` 记录这条链上的元素和',
        'ans = [0] * n': '最后一次删除后一切都被删光，`ans[n-1] = 0`',
        'for i in range': '倒序：把第 `i` 次删除的元素加回来。`i` 只到 1，因为 `ans[i-1]` 才是加回后的答案',
        'x = removeQueries': '加回下标 `x = {x}`（值 `nums[{x}] = {nums[x]}`）',
        'to = find': '`find({removeQueries[i] + 1})`：找右邻居 `{removeQueries[i] + 1}` 所在链的根。右边还没加回的话，根就是它自己',
        'fa[x] = to': '==合并 x 和 x+1==：`fa[{x}] = {to}`。不用合并 `x-1`：左边的链会在它自己加回时往右连过来',
        'sum[to] += sum[x]': '子段和 += 左边并过来的 `sum[{x}]`（若有）+ 新加回的 `nums[{x}] = {nums[x]}`',
        'ans[i - 1] = max': '`ans[{i - 1}] = max(ans[{i}], sum[{to}])` = max(`{ans[i]}`, `{sum[to]}`)：最大子段要么是上一个，要么是刚合并出来的',
        'return ans': '结果 `{ans}`',
    },
    cards=dict(
        one_liner='删除不好做，倒着加回来：并查集合并相邻子段',
        complexity='时间 `O(n α(n))`，空间 `O(n)`',
        problem=['每次删除 `nums[removeQueries[i]]`，把数组切成若干连续正数子段',
                 '求每次删除后的最大子段和',
                 '示例：`nums=[1,2,5,6,1]`，`removeQueries=[0,3,2,4,1]` → `[14,7,2,2,0]`'],
        quote='删除不好做，添加比较好做。不妨倒着思考，删除变成了添加。添加时可能会合并两个子段。',
        quote_src='—— 灵茶山艾府题解提示 1、2',
        idea=['倒序遍历，下标 `x` 加回时只合并 `x` 和 `x+1`',
              '合并形成「链」，每条链去掉最右元素就是真实的子段；这个多出来的右端点是「幽灵火车头」',
              '`ans[i-1]` = max(`ans[i]`，新合并子段的和)'],
        summary=['时间 `O(n α(n))`，空间 `O(n)`',
                 '易错：并查集开 `n+1` 个点，不然 `find(x+1)` 越界；`ans[n-1]` 恒为 0',
                 '易错：循环到 `i=1`，`ans[i-1]` 才覆盖 `ans[0]`',
                 '变量 `sum` 覆盖了内置函数名，原文如此，仅在函数内使用',
                 '相似题：1562 查找大小为 M 的最新分组'],
    ),
)
