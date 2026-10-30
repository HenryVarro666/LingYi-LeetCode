def _ni(S):
    v = S.get('v')
    nums = S['nums']
    return nums.index(v) if v in nums else None


CONFIG = dict(
    num=3231, title='要删除的递增子序列的最小数量', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='贪心 · 末尾递减 + 二分（最长不增子序列）',
    code='''
class Solution(object):
    def minOperations(self, nums):
        f = [nums[0]]
        for v in nums[1:]:
            if v <= f[-1]:
                f.append(v)
            else:
                left = 0
                right = len(f) - 1
                while left < right:
                    mid = (left + right) // 2
                    if f[mid] >= v:
                        left = mid + 1
                    else:
                        right = mid

                f[left] = v

        return len(f)
''',
    call='Solution().minOperations([5,3,1,4,2,6])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=200, label='nums（蓝 = 正在处理的 v，灰 = 已处理）',
             color=lambda S, i, v: 'blue' if i == _ni(S) else None,
             dim=lambda S, i, v: _ni(S) is not None and i < _ni(S)),
        dict(type='array', var='f', pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}, h=300,
             label='f：每个递增子序列的末尾（始终从大到小）',
             color=lambda S, i, v: 'green' if S['_line'] in (6, 17) and i == (len(S['f']) - 1 if S['_line'] == 6 else S.get('left')) else None),
        dict(type='text', size=30, fn=lambda S: f"`v` = =={S['v']}==，`f` 有 {len(S['f'])} 个末尾 → 目前 =={len(S['f'])}== 个子序列" if 'v' in S else ''),
    ],
    watch=['v', 'left', 'right', 'mid', ('子序列数', 'len(f)', 'green')] if False else ['v', 'left', 'right', 'mid'],
    captions={
        'f = [nums[0]]': '第一个数自己成一个子序列：`f` = {f}（`f` 记各子序列的==最后一个数==）',
        'for v in': '取下一个数（取完则结束循环）：`v` = {v}',
        'if v <= f[-1]': '`v <= f[-1]`（{v} <= {f[-1]}）→ {"成立：比所有末尾都小或相等，接不到任何子序列后面" if v <= f[-1] else "不成立：能接在某个子序列后面"}',
        'f.append(v)': '另起新子序列：`f` 末尾加入 {v} → {f}，共 =={len(f)}== 个',
        'left = 0': '二分找：最后一个数 ==最大且仍小于 v== 的子序列（`f` 递减，找第一个 `< v`）',
        'right = len': '`right = {right}`',
        'while left < right': '`left < right`（{left} < {right}）→ {"继续二分" if left < right else "二分结束，答案位置是 left"}',
        'mid = (left': '`mid = ({left} + {right}) // 2 = {mid}`',
        'if f[mid] >= v': '`f[{mid}] >= v`（{f[mid]} >= {v}）→ {"成立：这个末尾不比 v 小，v 接不上，往右找" if f[mid] >= v else "不成立：这个末尾小于 v，v 能接上，答案在 mid 或更左（左边末尾更大）"}',
        'left = mid + 1': '`left` → {left}',
        'right = mid': '`right` → {right}',
        'f[left] = v': '`v` 接到 `f[{left}]` 后面：末尾 {B.f[left]} 换成 {v}（末尾==变大了一点，但仍保持递减==）→ {f}',
        'return len(f)': '`f` 的长度就是子序列最少个数：=={len(f)}==',
    },
    cards=dict(
        one_liner='子序列的末尾始终从大到小，新数接到最大的可接末尾上',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，每一轮可以删去一个严格递增子序列，求删空数组的最少轮数',
                 '即：`nums` 最少能拆成几个严格递增子序列',
                 '本视频：`[5,3,1,4,2,6]` → `3`'],
        quote='对于nums[p]：若nums[p]小于等于当前已有递增子序列中最小的最后一个数，……应该从nums[p]开始另起一个新的子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['按顺序处理每个数，让每个子序列的==最后一个数尽量小==，后面的数更容易接上',
              '`v` 不超过所有末尾：谁也接不上，自己另起一个新子序列',
              '否则接在==末尾最大的、但仍小于 v==的那个子序列后面',
              '这样 `f` 始终从大到小，可以二分查找，这个过程和求最长不增子序列相同'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：严格递增，所以 `v <= f[-1]` 带等号；二分里 `f[mid] >= v` 也带等号',
                 '`f` 是递减序列，二分方向和普通 LIS 相反',
                 '作者自己说明：与最长不增子序列等价，但没有证明；答案就是 `len(f)`',
                 '原文就是 Python 3 可运行的写法，仅删去了类型说明文档字符串'],
    ),
)
