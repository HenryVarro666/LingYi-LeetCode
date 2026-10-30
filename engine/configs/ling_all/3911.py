CONFIG = dict(
    num=3911, title='移除子数组元素后第 K 小偶数', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='转成 1539 题 · 二分',
    tags=['灵神题单·二分算法', '难度分 2156'],
    code='''
class Solution:
    def kthRemainingInteger(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        # 记录所有偶数的下标
        even_pos = [i for i, x in enumerate(nums) if x % 2 == 0]
        ans = [0] * len(queries)

        for i, (l, r, k) in enumerate(queries):
            # 计算询问对应的 even_pos 的子数组 even_pos[li:ri]
            li = bisect_left(even_pos, l)
            ri = bisect_right(even_pos, r)

            # 推导过程见 1539 题解
            j = bisect_left(range(ri - li), True, key=lambda j: nums[even_pos[li + j]] // 2 - 1 - j >= k)
            ans[i] = (j + k) * 2

        return ans
''',
    call='Solution().kthRemainingInteger([2,5,8], [[0,1,2],[1,2,1],[0,2,4]])',
    expect=[6, 2, 12],
    views=[
        dict(type='array', var='nums', label='nums', h=150,
             color=lambda S, i, v: ('green' if 'l' in S and S['l'] <= i <= S['r'] and v % 2 == 0 else 'blue' if 'l' in S and S['l'] <= i <= S['r'] else None),
             dim=lambda S, i, v: 'l' in S and not (S['l'] <= i <= S['r']),
             window=('l', 'r')),
        dict(type='array', var='even_pos', label='even_pos（偶数的下标）', h=190,
             pointers={'li': 'blue', 'ri': 'pink'}),
        dict(type='text', h=70, fn=lambda S: (f"第 `{S['i']}` 个询问 `l={S['l']}, r={S['r']}, k={S['k']}`：子数组里有 ==`{S['ri']-S['li']}`== 个偶数，答案在第 `{S['k']}` ~ `{S['k']+S['ri']-S['li']}` 个正偶数之间" if 'ri' in S else '')),
        dict(type='array', var='ans', label='ans', h=130),
    ],
    watch=['i', 'l', 'r', 'k', 'li', 'ri', ('j', 'j', 'green')],
    captions={
        'even_pos = [': '只有偶数才可能挡住正偶数序列，先记下所有偶数的下标 ==`{even_pos}`==',
        'ans = [0]': '`ans` 存每个询问的答案',
        'for i, (l, r, k)': lambda S, B, r_: (f'处理第 `{S.i}` 个询问：`[l, r, k] = [{S.l}, {S.r}, {S.k}]`' if not ('i' in B and B['i'] == S.i) else '询问都处理完了，循环结束'),
        'li = bisect_left': '`even_pos` 里第一个 `>= {l}` 的位置：`li = {li}`',
        'ri = bisect_right': '`even_pos` 里第一个 `> {r}` 的位置：`ri = {ri}`，所以子数组里有 `{ri-li}` 个偶数',
        'j = bisect_left': '把偶数除以 2 就是 1539 题：二分最小的 `j`，使得第 `j` 个偶数前面缺失的数 `>= k`。结果 `j` = =={j}==',
        'ans[i] =': '前面有 `{j}` 个偶数被挡住，答案顺延成第 `j + k = {j + k}` 个正偶数 → `({j} + {k}) × 2` = =={ans[i]}==',
        'return ans': '全部询问处理完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='把偶数除以 2，就是 1539 题：第 k 个缺失的正整数',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['`nums` 严格递增；每个询问 `[l, r, k]`：从 `2, 4, 6, ...` 里删掉 `nums[l..r]` 中的数',
                 '求剩下序列的第 `k` 小，返回所有询问的答案',
                 '示例：`nums=[2,5,8]`，`[[0,1,2],[1,2,1],[0,2,4]]` → `[6,2,12]`'],
        quote='换个方式描述问题：找不在子数组中的第 k 个缺失的正偶数。如果把偶数都除以 2，那不就是 1539 题吗？',
        quote_src='—— 灵茶山艾府题解',
        idea=['奇数不会挡住正偶数，只看子数组里的偶数',
              '偶数 `x` 除以 2 后在第 `x/2` 位；它前面缺失 `x/2 - 1 - j` 个数',
              '缺失数随 `j` 单调不减 → 二分第一个 `>= k` 的 `j`，答案是 `(j + k) × 2`'],
        after=[dict(heading='方法一与写法二', lines=['方法一：二分答案套二分，`O(q log^2 n)`，很慢',
                                                   '写法二：预处理 `a[i] = nums[even_pos[i]]//2 - 1 - i`，直接在 `a` 里二分 `k - li`'])],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`',
                 '易错点：二分范围是子数组的偶数 `[li, ri)`，`li/ri` 用 `bisect_left/right` 得到',
                 '答案是 `(j + k) * 2`，别漏了乘 2',
                 '同类题：1539 第 k 个缺失的正整数'],
    ),
)
