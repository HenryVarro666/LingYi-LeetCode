
def _txt(S):
    if 'neg_cnt' not in S or 'left' not in S:
        return '子数组 [left, right] 内的负数，换成子数组外的正数'
    return (f'子数组内负数 `neg_cnt = {S["neg_cnt"]}`　外面的正数 `pos_cnt = {S["pos_cnt"]}`　最多换 `k = {S["k"]}` 次　'
            f'→ `need_swap = min(neg_cnt, pos_cnt, k)`')


def _gain(S):
    if 'delta' not in S or 'sub_sum' not in S or 'need_swap' not in S:
        return ''
    return f'子数组和 `{S["sub_sum"]}` + 交换增量 `{S["delta"]}` = ==​{S["sub_sum"] + S["delta"]}==　（这个子数组交换后的最大和）'


def _col(S, i, v):
    if 'left' not in S or 'right' not in S or 'sub_sum' not in S:
        return None
    if S['left'] <= i <= S['right']:
        return 'blue' if v < 0 else 'green' if v > 0 else None
    return 'orange' if v > 0 else None


CONFIG = dict(
    num=3962, title='至多 K 次交换后最大子数组和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举子数组 · 只换负数与正数 · 值域树状数组',
    tags=['常用数据结构', '难度分 2672'],
    code=r'''
from __future__ import annotations
class FenwickTree:
    def __init__(self, sorted_nums: List[int]):
        self.n = n = len(sorted_nums)
        self.high_bit = 1 << (n.bit_length() - 1)
        self.sorted_nums = sorted_nums
        self.cnt = [0] * (n + 1)
        self.sum = [0] * (n + 1)

    # 添加 num 个 val，其中 val 离散化后的值为 i（i 从 1 开始）
    # 如果 num < 0，表示减少 -num 个 val
    # 注意 val = sorted_nums[i - 1]，无需手动传入
    def update(self, i: int, num: int) -> None:
        val = self.sorted_nums[i - 1]
        while i <= self.n:
            self.cnt[i] += num
            self.sum[i] += num * val
            i += i & -i

    # 返回前 k 小的数之和（k 从 1 开始）
    def pre_sum(self, k: int) -> int:
        s = i = 0
        b = self.high_bit
        while b > 0:
            nxt = i | b
            if nxt <= self.n and self.cnt[nxt] < k:
                k -= self.cnt[nxt]
                s += self.sum[nxt]
                i = nxt
            b >>= 1
        # 加上等于第 k 小的数
        return s + self.sorted_nums[i] * k

    def copy(self) -> FenwickTree:
        t = FenwickTree(self.sorted_nums)
        t.cnt[:] = self.cnt
        t.sum[:] = self.sum
        return t

class Solution:
    def maxSum(self, nums: list[int], k: int) -> int:
        # O(n) 特判：能否把正数都聚在一起
        all_pos_sum = all_pos_cnt = 0
        for x in nums:
            if x > 0:
                all_pos_sum += x
                all_pos_cnt += 1
        if all_pos_cnt == 0:  # 没有正数
            return max(nums)
        # 定长滑动窗口模板，窗口长度为 all_pos_cnt
        cnt = 0
        for i, x in enumerate(nums):
            if x > 0:
                cnt += 1
            left = i - all_pos_cnt + 1
            if left < 0:
                continue
            if cnt + k >= all_pos_cnt:  # 可以把正数都聚在一起
                return all_pos_sum
            if nums[left] > 0:
                cnt -= 1

        # 离散化
        n = len(nums)
        sorted_nums = sorted(set(nums))
        rank = [0] * n  # rank[i] 是 nums[i] 离散化后的值（从 1 开始）
        all_pos_tree = FenwickTree(sorted_nums)  # 包含所有正数的树状数组
        for i, x in enumerate(nums):
            rank[i] = bisect_left(sorted_nums, x) + 1
            if x > 0:
                all_pos_tree.update(rank[i], 1)

        ans = -inf

        # 枚举子数组左端点
        for left in range(n):
            neg_tree = FenwickTree(sorted_nums)
            pos_tree = all_pos_tree.copy()
            pos_sum = all_pos_sum
            pos_cnt = all_pos_cnt
            neg_cnt = 0
            sub_sum = 0

            # 枚举子数组右端点
            for right in range(left, n):
                # x 从子数组外移到子数组内
                x = nums[right]
                rk = rank[right]
                sub_sum += x
                if x > 0:
                    pos_tree.update(rk, -1)
                    pos_sum -= x
                    pos_cnt -= 1
                elif x < 0:
                    neg_tree.update(rk, 1)
                    neg_cnt += 1

                # 计算通过交换导致的元素和的增量
                delta = 0
                need_swap = min(neg_cnt, pos_cnt, k)
                if need_swap > 0:
                    in_sum = neg_tree.pre_sum(need_swap)
                    out_sum = pos_sum - pos_tree.pre_sum(pos_cnt - need_swap)
                    delta = out_sum - in_sum

                ans = max(ans, sub_sum + delta)

        return ans
''',
    call='Solution().maxSum([2, -3, -1, 4, -2, -5, 3], 1)',
    expect=8,
    views=[
        dict(type='array', var='nums', label='nums（框 = 子数组；绿 = 内部正数，蓝 = 内部负数，橙 = 外部正数）', h=230,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_col),
        dict(type='text', fn=_txt, size=24, h=100),
        dict(type='text', fn=_gain, size=26, h=100),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('sub_sum', 'sub_sum', 'green'),
           ('need_swap', 'need_swap', 'orange'), ('delta', 'delta', 'cyan'), ('ans', 'ans', 'green')],
    skip=['self.n = n', 'self.high_bit', 'self.sorted_nums = ', 'self.cnt = [0]', 'self.sum = [0]', 'val = self.sorted_nums[i - 1]', 'while i <= self.n', 'self.cnt[i] += num', 'self.sum[i] += num * val', 'i += i & -i', 's = i = 0', 'b = self.high_bit', 'while b > 0', 'nxt = i | b', 'if nxt <= self.n and self.cnt[nxt] < k', 'k -= self.cnt[nxt]', 's += self.sum[nxt]', 'i = nxt', 'b >>= 1', 'return s + self.sorted_nums', 't = FenwickTree(self.sorted_nums)', 't.cnt[:] = self.cnt', 't.sum[:] = self.sum', 'return t', 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 64, 65, 66, 68, 69, 70, 71, 79, 80, 81, 82, 87, 88, 99, 91, 93, 95, 101],
    captions={
        67: '离散化，建一棵装==所有正数==的值域树状数组（特判已通过，不能一步聚齐）',
        76: '枚举左端点 `left = {left}`',
        77: '`neg_tree`：子数组==内部的负数==，起初为空',
        78: '`pos_tree`：子数组==外部的正数==，起初是全部正数',
        85: '右端点 `right = {right}`：`nums[{right}]` 进入子数组',
        89: '`sub_sum += {x}` → =={sub_sum}==',
        90: lambda S, B, r: (f'`{S.x}` 是正数：不再属于「外部正数」' if S.x > 0 else f'`{S.x}` 不是正数，外部不变'),
        92: '`pos_sum` 减去 `{x}` → {pos_sum}，`pos_cnt` 减一',
        94: lambda S, B, r: (f'`{S.x}` 是负数：加入 `neg_tree`，可被换出去' if S.x < 0 else '`x = 0`，不处理'),
        96: '内部负数 `neg_cnt` → {neg_cnt}',
        100: lambda S, B, r: f'`need_swap = min({S.neg_cnt}, {S.pos_cnt}, {S.k})` = =={S.need_swap}==' + ('，不换' if S.need_swap == 0 else '，值得换'),
        102: '`in_sum`：内部最小的 `need_swap` 个数之和（换出）',
        103: '`out_sum`：外部最大的 `need_swap` 个正数之和（换入）',
        104: '增量 `delta = {out_sum} − ({in_sum})` = =={delta}==',
        106: '`ans = max({B.ans}, {sub_sum} + {delta})` = =={ans}==',
        108: '最大子数组和：`{ans}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='换进来的只会是正数，换出去的只会是负数：枚举子数组，贪心换',
        complexity='时间 `O(n^2 log n)`，空间 `O(n)`',
        problem=['最多交换 `k` 次（可交换任意两个下标），求交换后的最大子数组和',
                 '`n <= 1500`，所以可以枚举子数组的左右端点',
                 '本视频：`[2,-3,-1,4,-2,-5,3]`，`k=1` → `8`'],
        quote='所以我们只需考虑子数组内的负数与子数组外的正数的交换。……needSwap = min(negCnt, posCnt, k)',
        quote_src='—— 灵茶山艾府题解',
        idea=['先特判：能把所有正数聚到一起，答案就是正数之和；没有正数则取最大值',
              '最优子数组的两端 `nums[l-1]`、`nums[r+1]` 必 ≤ 0，两端内侧必 ≥ 0 → ==只需换「内部负数」和「外部正数」==',
              '换最小的 `need_swap` 个负数出去、最大的 `need_swap` 个正数进来，两棵值域树状数组求「前 m 小之和」'],
        summary=['时间 `O(n^2 log n)`，空间 `O(n)`；优化前（枚举交换次数）会超时',
                 '易错点：没有正数时返回 `max(nums)`，子数组不能为空',
                 '`need_swap = min(neg_cnt, pos_cnt, k)`，最大的正数之和 = `pos_sum − 外部最小的 (pos_cnt−need_swap) 个之和`',
                 '树状数组内部（`update` / `pre_sum`）是标准模板，视频里略过，只看调用',
                 '代码开头加了一行 `from __future__ import annotations`，让 `copy` 的返回类型标注在 Python 3.10 下可运行'],
    ),
)
