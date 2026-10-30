CONFIG = dict(
    num=1053, title='交换一次的先前排列', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='从后找逆序 · 交换一次',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def prevPermOpt1(self, arr):

        p1 = len(arr) - 2
        while p1 >= 0 and arr[p1] <= arr[p1 + 1]:
            p1 -= 1
        
        if p1 < 0:
            return arr
        
        p2 = None
        for index in range(p1 + 1, len(arr)):
            if arr[index] >= arr[p1]:
                break
            
            if p2 is None or arr[p2] < arr[index]:
                p2 = index

        arr[p1], arr[p2] = arr[p2], arr[p1]

        return arr
''',
    call='Solution().prevPermOpt1([5, 3, 1, 1, 4])',
    expect=[5, 1, 3, 1, 4],
    views=[
        dict(type='text', size=26, fn=lambda S: (
            f"逆序位置 `p1 = {S['p1']}`：`arr[p1] = {S['arr'][S['p1']]}`" if S.get('p1', -1) >= 0 and 'p2' not in S
            else ('' if 'p1' not in S else (
                f"候选 `p2 = {S['p2']}`（值 {S['arr'][S['p2']]}）：比 `arr[p1]` 小里最大的" if S.get('p2') is not None
                else '还没有候选 p2'))) if 'p1' in S else ''),
        dict(type='array', var='arr', label='arr（蓝 = p1，粉 = 当前最优 q，黄 = 正在看的 index）', h=260,
             pointers={'p1': 'blue', 'p2': 'pink', 'index': 'yellow'},
             color=lambda S, i, v: ('blue' if i == S.get('p1') else 'pink' if i == S.get('p2') else None)
             if S.get('p1', -1) >= 0 else None,
             dim=lambda S, i, v: S.get('p1', -1) >= 0 and i < S['p1']),
        dict(type='text', size=24, fn=lambda S: '`p1` 右边（p1+1 到末尾）是单调不减的最小排列' if S.get('p1', -1) >= 0 else ''),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), ('index', 'index', 'yellow')],
    skip=['p2 = None'],
    captions={
        'p1 = len': '从后向前扫描，`p1 = len(arr) - 2 = {p1}`，找第一次出现逆序的位置',
        'while p1 >= 0': lambda S, B, r: (
            f"`arr[{S.p1}] = {S.arr[S.p1]} <= arr[{S.p1 + 1}] = {S.arr[S.p1 + 1]}` → 还是不降，继续往左" if S.p1 >= 0 and S.arr[S.p1] <= S.arr[S.p1 + 1]
            else (f"`arr[{S.p1}] = {S.arr[S.p1]} > arr[{S.p1 + 1}] = {S.arr[S.p1 + 1]}` → ==第一次逆序==，`p1` 就是它" if S.p1 >= 0
                  else '`p1 < 0`：整个数组不降，已是最小排列')),
        'p1 -= 1': '`arr[p1] <= arr[p1+1]` 不是逆序 → `p1` 左移到 {p1}',
        'if p1 < 0': lambda S, B, r: ('`p1 < 0`：找不到逆序，已是最小排列，无法变小' if S.p1 < 0
                                      else f'`p1 = {S.p1}` 存在，可以交换出更小的排列'),
        'for index': '在 p1 右边找 `q`：`index = {index}`，值 `{arr[index]}`',
        'if arr[index] >= arr[p1]': lambda S, B, r: (
            f"`arr[{S.index}] = {S.arr[S.index]} >= arr[p1] = {S.arr[S.p1]}` → 不再比它小，后面更大，==停止=="
            if S.arr[S.index] >= S.arr[S.p1]
            else f"`arr[{S.index}] = {S.arr[S.index]} < arr[p1] = {S.arr[S.p1]}` → 可以和它换，继续"),
        'if p2 is None': lambda S, B, r: (
            '还没有候选，当前位置直接作为 `p2`' if S.get('p2') is None
            else (f"`arr[p2] = {S.arr[S.p2]} < arr[{S.index}] = {S.arr[S.index]}` → 这个更大，换掉候选" if S.arr[S.p2] < S.arr[S.index]
                  else f"`arr[p2] = {S.arr[S.p2]}` 不小于 `arr[{S.index}] = {S.arr[S.index]}` → ==相等也不更新==，保留靠前的")),
        'p2 = index': '候选 `p2 = {p2}`：目前是比 `arr[p1]` 小的里面最大的',
        'arr[p1], arr[p2]': '交换 `arr[{p1}]` 与 `arr[{p2}]`：大数放到靠后位置，得到 `{arr}`',
        'return arr': lambda S, B, r: f'返回 `{S.arr}`',
    },
    cards=dict(
        one_liner='从后找第一个逆序位 p，再和右边「比它小的最大数」交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `arr`，==恰好交换一次==两个数，得到字典序比原数组小的最大排列',
                 '如果原数组已是最小排列，就原样返回',
                 '示例：`[3,2,1]` → `[3,1,2]`；本视频：`[5,3,1,1,4]` → `[5,1,3,1,4]`'],
        quote='需要找出第一次出现逆序的位置p。若找不到，则说明当前arr已经是最小的排列，那么直接返回即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['和「下一个排列」类似，从后向前扫，找第一个 `arr[p] > arr[p+1]` 的 `p`',
              '`p` 右边已不降，是最小排列；要让结果尽量大，就换成右边==小于 arr[p] 的最大值==',
              '有相同的最大值时，代码用严格 `<` 更新，留下的是靠前的那个'],
        result='`arr[1] = 3` 与 `arr[2] = 1` 交换 → `[5,1,3,1,4]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`，原地交换',
                 '找不到逆序（`p1 < 0`）就直接返回，不能再变小',
                 '循环遇到 `arr[index] >= arr[p1]` 要立刻 break，右边不降，后面只会更大',
                 '有多个相同的候选值时，==取最靠前的那个==才能让结果最大（代码里严格 `<` 保证了这点）'],
    ),
)
