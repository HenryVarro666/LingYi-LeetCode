def _cls(S, v):
    return 0 if v < S['a'] else (1 if v <= S['b'] else 2)


def _info(S):
    if 'cnt1' not in S:
        return '把每个数按 `a=4, b=8` 分成 ==0（小于 a）、1（区间内）、2（大于 b）=='
    return f"`cnt1 = {S['cnt1']}`（已遍历的 1），`cnt2 = {S['cnt2']}`（已遍历的 2），逆序对 `ans = {S['ans']}`"


CONFIG = dict(
    num=3994, title='划分数组的最少相邻交换次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='三种元素数逆序对',
    tags=['灵神题单·常用数据结构', '难度分 1705'],
    code='''
class Solution:
    def minAdjacentSwaps(self, nums: list[int], a: int, b: int) -> int:
        ans = cnt1 = cnt2 = 0
        for x in nums:
            if x < a:  # x 视作 0
                ans += cnt1 + cnt2
            elif x <= b:  # x 视作 1
                ans += cnt2
                cnt1 += 1
            else:  # x 视作 2
                cnt2 += 1
        return ans % 1_000_000_007
''',
    call='Solution().minAdjacentSwaps([5, 1, 9, 3, 7, 2, 8], 4, 8)',
    expect=8,
    views=[
        dict(type='text', fn=_info),
        dict(type='array', var='nums', label='nums（蓝 = 视作 0，黄 = 视作 1，粉 = 视作 2）', h=200,
             color=lambda S, i, v: ('blue', 'yellow', 'pink')[_cls(S, v)] if 'a' in S else None),
        dict(type='text', fn=lambda S: f"当前 `x = {S['x']}` 视作 =={_cls(S, S['x'])}==" if 'x' in S and 'cnt1' in S else ''),
    ],
    watch=['x', ('cnt1', 'cnt1', 'yellow'), ('cnt2', 'cnt2', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt1 = cnt2 = 0': '`ans` 累计逆序对，`cnt1` / `cnt2` 记录已经见过多少个 1 和 2',
        'ans += cnt1 + cnt2': '`x = {x}` 视作 0：前面所有的 1 和 2 都比它大 → 新增 `{cnt1} + {cnt2}` 个逆序对，`ans` = =={ans}==',
        'ans += cnt2': '`x = {x}` 视作 1：只有前面的 2 比它大 → 新增 `{cnt2}` 个逆序对，`ans` = =={ans}==',
        'cnt1 += 1': '见过的 1 多了一个：`cnt1` = {cnt1}',
        'cnt2 += 1': '`x = {x}` 视作 2：没有比 2 更大的数，不新增逆序对；`cnt2` = {cnt2}',
        'return ans': '逆序对个数就是最少相邻交换次数：`{ans} % (10^9+7)` = =={ret}==',
    },
    cards=dict(
        one_liner='三种数排序，最少相邻交换次数 = 逆序对个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组变成「小于 a」「在 [a, b]」「大于 b」依次排列的好数组',
                 '每次只能交换相邻两个数，求最少交换次数（模 `10^9+7`）',
                 '本视频：`[5,1,9,3,7,2,8], a=4, b=8`'],
        quote='把小于 a 的数视作 0，在 [a,b] 中的数视作 1，大于 b 的数视作 2。问题等价于：把这个只包含 0,1,2 的数组排成升序，只能交换相邻元素，求最小交换次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定理：相邻交换排成升序，最少次数 ==等于逆序对个数==（一次交换至多减少一个逆序对）',
              '一般要用值域树状数组数逆序对，但这里只有 0/1/2 三种数',
              '遍历时记下 1 和 2 的个数：来个 0 加 `cnt1+cnt2`，来个 1 加 `cnt2`，2 不加'],
        summary=['时间 `O(n)`，空间 `O(1)`，比树状数组更简单',
                 '易错点：最后别忘了模 `10^9 + 7`',
                 '`cnt1` 只在 x 视作 1 时才加；来个 0 不更新计数',
                 '一般数组的逆序对见题单 §8.2（树状数组 / 归并排序）'],
    ),
)
