def _txt(S):
    if 'cnt' not in S:
        return ''
    k = S['k']
    return f"当前右端点 `i = {S.get('i', '-')}`：nums[0..i] 里等于 `k={k}` 的有 ==`{S['cnt']}`== 个 → 以 `i` 结尾、AND 值为 k 的子数组数"


CONFIG = dict(
    num=3209, title='子数组按位与值为 K 的数目', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='LogTrick · 维护等于 k 的个数',
    tags=['灵神题单·位运算', '难度分 2050'],
    code='''
class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        ans = cnt = 0
        for i, x in enumerate(nums):
            if x == k:
                cnt += 1
            for j in range(i - 1, -1, -1):
                if nums[j] & x == nums[j]:
                    break
                if nums[j] == k:
                    cnt -= 1
                nums[j] &= x
                if nums[j] == k:
                    cnt += 1
            ans += cnt
        return ans
''',
    call='Solution().countSubarrays([3,7,3,1,3], 3)',
    expect=6,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='nums', label='nums[j]（原地改成：下标 j 到 i 的 AND 值）', pointers={'j': 'blue', 'i': 'pink'}, h=260,
             color=lambda S, i, v: 'green' if v == S.get('k') and S.get('i', -1) >= i else None,
             dim=lambda S, i, v: S.get('i', 99) < i),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), ('x', 'x'), ('k', 'k'), ('cnt', 'cnt', 'green'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt = 0': '`cnt`：以当前右端点结尾、AND 值恰好为 `k` 的子数组个数；`ans` 累加每个右端点的 `cnt`',
        'for i, x in': lambda S, B, r: ('所有右端点都处理完了' if B.get('i') == S.i and 'i' in B else
                                       f'右端点来到 `i = {S.i}`，新元素 `x = {S.x}`'),
        5: lambda S, B, r: (f'`x = {S.x}` == `k`：单个元素就是一个合法子数组' if S.x == S.k
                            else f'`x = {S.x}` ≠ `k = {S.k}`：自己不算'),
        6: '`cnt` 加 1 → {cnt}（`[i, i]` 本身合法）',
        'for j in range': lambda S, B, r: ('`i = 0` 左边没有元素' if 'j' not in S else
                                          '`j` 已扫到最左端，内层循环结束' if B.get('j') == S.j else
                                          f'往左更新 AND 值，`j = {S.j}`'),
        'if nums[j] & x == nums[j]': lambda S, B, r: (
            f'`{S.nums[S.j]} & {S.x} = {S.nums[S.j] & S.x}` == `nums[j]`：==AND 不会让它变小== → 左边更小的数也不会变，break'
            if S.nums[S.j] & S.x == S.nums[S.j] else
            f'`{S.nums[S.j]} & {S.x} = {S.nums[S.j] & S.x}` < `{S.nums[S.j]}`：x 把某些 1 清掉了 → 要更新'),
        'break': '`break`：再往左的 AND 值也不会变了，等于 k 的个数不用改',
        'cnt -= 1': '旧值 `nums[{j}]` 原本等于 `k` → 马上要变小了，先从 `cnt` 里减掉：`cnt` = {cnt}',
        'nums[j] &= x': '`nums[{j}]` 更新为 `{B.nums[j]} & {x} = {nums[j]}`：现在是 `[{j}, {i}]` 的 AND 值',
        14: '更新后的值恰好等于 `k` → `[{j}, {i}]` 合法，`cnt` 加回来 = {cnt}',
        'ans += cnt': '右端点 `{i}` 下，AND 值等于 k 的子数组有 `{cnt}` 个 → `ans` = =={ans}==',
        'return ans': '总共 `{ans}` 个子数组',
    },
    cards=dict(
        one_liner='把 OR 的 LogTrick 换成 AND，边更新边维护「等于 k 的个数」',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['数出 `nums` 中有多少个子数组，所有元素按位 AND 的结果恰好是 `k`',
                 '示例：`[1,1,2]`，`k=1` → `3`；`[1,2,3]`，`k=2` → `2`',
                 '本视频：`[3,7,3,1,3]`，`k=3` → `6`'],
        quote='在更新 nums[j] 的同时，维护值等于 k 的元素个数，也就是 AND 值为 k 的子数组个数。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['`nums[j]` 原地存「`j` 到 `i` 的 AND 值」，AND 只会让数变小，每个数最多变 29 次',
              '一旦 `nums[j] & x == nums[j]`，更左边的数都是它的超集，不会再变 → `break`',
              '每次改动前后检查是否等于 `k`，增减 `cnt`；`ans += cnt`'],
        summary=['时间 `O(n log U)`，每个数最多减小约 30 次',
                 '改动前如果等于 `k` 要先 `cnt -= 1`，改动后等于 `k` 再 `cnt += 1`',
                 '灵神另给了二分、三指针（`left/right` 滑窗）、恰好型滑窗+栈的写法，这里演示方法三',
                 '同类题：2411（OR 版 LogTrick）、1521、3171'],
    ),
)
