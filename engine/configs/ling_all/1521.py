def _bits(v, w=4):
    return format(v, '0%db' % w)


def _info(S):
    if 'x' not in S:
        return ''
    i, x = S['i'], S['x']
    arr = S['arr']
    if 'j' in S and S['_line'] in (7, 8, 9, 10) and S['j'] < i:
        j = S['j']
        return f"`x = {_bits(x)}`　`arr[{j}] = {_bits(arr[j])}`　AND = `{_bits(arr[j] & x)}`"
    return f"`x = arr[{i}] = {_bits(x)}`（二进制）"


CONFIG = dict(
    num=1521, title='找到最接近目标值的函数值', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='LogTrick · 与值只减不增',
    tags=['灵神题单', '难度分 3171'],
    code='''
class Solution:
    def closestToTarget(self, arr: List[int], k: int) -> int:
        ans = inf
        for i, x in enumerate(arr):
            ans = min(ans, abs(x - k))
            for j in range(i - 1, -1, -1):
                if arr[j] & x == arr[j]:
                    break
                arr[j] &= x
                ans = min(ans, abs(arr[j] - k))
        return ans
''',
    call='Solution().closestToTarget([9,12,3,7,15], 5)',
    expect=2,
    views=[
        dict(type='text', fn=_info, size=30, h=60),
        dict(type='array', var='arr', pointers={'i': 'blue', 'j': 'pink'}, h=240, label='arr（原地改成「以 i 结尾的子数组与值」）',
             color=lambda S, idx, v: ('blue' if idx == S.get('i') else 'pink' if S['_line'] in (7, 8, 9, 10) and idx == S.get('j') else None)),
        dict(type='text', fn=lambda S: f"`k = {S['k']}`　当前最小差 ans = =={S['ans'] if S['ans'] != float('inf') else '∞'}==" if 'ans' in S else '', size=28, h=60),
    ],
    watch=['i', 'x', 'j', ('k', 'k', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '答案先设成无穷大，之后不断取最小',
        'for i, x in enumerate': lambda S, B, r: (f'`i = {S.i}`：计算右端点为 `{S.i}` 的所有子数组的与值' + (f'，`j` 从 `{S.i-1}` 往左并入 `x`' if S.i else '，左边没有元素') if S.get('i') != B.get('i') else '枚举结束'),
        'ans = min(ans, abs(x - k))': '单个元素也是子数组：`|{x} − {k}| = {abs(x-k)}`，`ans` = {ans}',
        'if arr[j] & x == arr[j]': lambda S, B, r: (f'`arr[{S.j}] & x = {S.arr[S.j]}` 等于它自己 → ==arr[j] 已是 x 的子集==，再往左也不会变，退出内层循环' if S.arr[S.j] & S.x == S.arr[S.j]
                                                   else f'`{_bits(S.arr[S.j])} & {_bits(S.x)} = {_bits(S.arr[S.j] & S.x)}` ≠ 原值 → 与值会变小，继续并入'),
        'break': '退出内层循环：`arr[{j}]` 及更左的元素都不用再改了',
        'arr[j] &= x': '`arr[{j}]` 变成 `{arr[j]}`：它现在表示 `[{j}..{i}]` 的与值',
        'ans = min(ans, abs(arr[j] - k))': '`[{j}..{i}]` 的与值 `{arr[j]}`，差 `{abs(arr[j]-k)}`，`ans` = {ans}',
        'return ans': '所有子数组的与值都看过了，最小差 `{ans}`',
    },
    skip=['for j in range'],
    max_steps=90,
    cards=dict(
        one_liner='与值只减不增：arr[j] 已是子集就停，每个数最多变小约 20 次',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['`func(arr, l, r)` 就是 `arr[l]` 到 `arr[r]` 的按位与',
                 '求 `|func(arr, l, r) − target|` 的最小值',
                 '本视频：`[9,12,3,7,15], target=5` → `2`'],
        quote='本题和 3171 几乎一样，仅仅是把 OR 改成了 AND。',
        quote_src='—— 灵茶山艾府题解',
        idea=['与运算是集合的交集：并入 x 后，arr[j] 只会变小',
              '`arr[j] & x == arr[j]` 说明 arr[j] 是 x 的子集 → 左边也不变，==直接 break==',
              '每个数至多从 19 个元素的集合缩到空集，总循环 `O(n log U)`'],
        after=[dict(heading='另一种写法：滑动窗口 + 栈', lines=[
            '与值随窗口变长而变小，可用滑窗',
            '栈里存后缀与值，右部用 `right_and` 维护；初始值取 `-1`（全 1）',
            '本视频演示 LogTrick'])],
        summary=['时间 `O(n log U)`，空间 `O(1)`（原地改 arr）',
                 '易错：单个元素也是子数组，先 `ans = min(ans, abs(x-k))`',
                 '易错：`break` 的条件是 `arr[j] & x == arr[j]`',
                 '同类题：3171（OR）、3097、2411'],
    ),
)
