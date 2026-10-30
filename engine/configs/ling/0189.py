NUMS, K = [1, 2, 3, 4, 5, 6, 7], 3
N = len(NUMS)
STAGE = {N - 1: ('第 1 次', '反转整个数组', 'A + B → rev(B) + rev(A)'),
         K - 1: ('第 2 次', '反转前 k 个', 'rev(B) → B'),
         K + N - 1: ('第 3 次', '反转后 n − k 个', 'rev(A) → A')}
AFTER = [([7, 6, 5, 4, 3, 2, 1], '第 1 次反转后：`rev(B) + rev(A)`，两段位置已经换好，但各自是反的'),
         ([5, 6, 7, 4, 3, 2, 1], '第 2 次反转后：前 k 个变回 `B`'),
         ([5, 6, 7, 1, 2, 3, 4], '第 3 次反转后：后 n − k 个变回 `A` → ==B + A==')]


SEG = {N - 1: (0, N - 1), K - 1: (0, K - 1), K + N - 1: (K, N - 1)}


def _seg(S, side):
    if 'i' in S and 'j' in S:
        g = SEG.get(S['i'] + S['j'])
        return g[side] if g else None
    return None


def _stage(S):
    if 'i' in S and 'j' in S and 'nums' in S:
        st = STAGE.get(S['i'] + S['j'])   # 反转过程中 i + j = L + R 保持不变
        if st:
            return f'{st[0]}：{st[1]}　`{st[2]}`'
    for arr, txt in AFTER:
        if S.get('nums') == arr and 'k' in S and S['k'] == K:
            return txt
    return '`nums = A + B`：蓝 = A（前 n − k 个），粉 = B（后 k 个）' if 'nums' in S else ''


CONFIG = dict(
    num=189, title='轮转数组', difficulty='Medium', category='普通数组',
    author='灵茶山艾府', technique='三次反转（负负得正）',
    code='''
# 注：请勿使用切片，会产生额外空间
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        def reverse(i: int, j: int) -> None:
            while i < j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        n = len(nums)
        k %= n  # 轮转 k 次等同于轮转 k % n 次
        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)
''',
    call=f'nums = {NUMS}\nSolution().rotate(nums, {K})\nnums',
    expect=[5, 6, 7, 1, 2, 3, 4],
    views=[
        dict(type='text', fn=_stage),
        dict(type='array', var='nums', label='nums', pointers={'i': 'yellow', 'j': 'orange'},
             window=(lambda S: _seg(S, 0), lambda S: _seg(S, 1)), window_color='yellow',
             color=lambda S, i, v: 'pink' if v > N - K else 'blue', cell=100, h=240),
        dict(type='array', var=lambda S: [5, 6, 7, 1, 2, 3, 4], label='目标：B + A　　（上方黄框 = 本次要反转的区间）',
             color=lambda S, i, v: 'pink' if v > N - K else 'blue', cell=100, h=170),
    ],
    skip=['i += 1', 'j -= 1'],
    watch=['n', 'k', ('i', 'i', 'yellow'), ('j', 'j', 'orange'), ('nums', 'nums', 'cyan')],
    captions={
        'n = len(nums)': '`n = {n}`。目标：把 `A + B` 变成 `B + A`',
        'k %= n': '轮转 `n` 次等于没转：`k %= n` → `k = {k}`，保证 `0 ≤ k < n`',
        'reverse(0, n - 1)': '第 1 次：反转==整个数组== `reverse(0, {n - 1})` → 得到 `rev(B) + rev(A)`',
        'reverse(0, k - 1)': '第 2 次：反转前 `k` 个 `reverse(0, {k - 1})` → ==反转两次等于没反转==，得到 `B`',
        'reverse(k, n - 1)': '第 3 次：反转后 `n − k` 个 `reverse({k}, {n - 1})` → 得到 `A`',
        'while i < j': lambda S, B, ret: (f'`i = {B.i} < j = {B.j}`：交换两端，再向中间靠拢' if B.i < B.j
                                          else f'`i = {B.i}` ≥ `j = {B.j}`：这一段反转完成'),
        'nums[i], nums[j]': '交换 `nums[{i}]` 和 `nums[{j}]`：`{B.nums[i]}` ↔ `{B.nums[j]}`',
    },
    cards=dict(
        one_liner='负负得正：整体反转一次，再把两段各反转一次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组元素==向右轮转 k 个位置==（原地修改）',
                 '示例：`nums = [1,2,3,4,5,6,7], k = 3` → `[5,6,7,1,2,3,4]`',
                 '进阶：用 `O(1)` 额外空间原地完成'],
        quote='这用到了「负负得正」的想法：把一个子数组反转两次，子数组不变。……把这两个子数组分别再反转一次，就抵消掉了反转，相当于我们只交换了 [1,2,3,4] 和 [5,6,7]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `nums = A + B`：`A` 是前 `n − k` 个，`B` 是后 `k` 个，目标是 `B + A`',
              '① 整体反转：`A + B` → `rev(B) + rev(A)`，==两段的位置换好了==，只是各自反了',
              '② 反转前 `k` 个得 `B`；③ 反转后 `n − k` 个得 `A` → `B + A`'],
        result='三次反转完成：`nums = [5,6,7,1,2,3,4]`（原地修改，没有返回值）',
        summary=['时间 `O(n)`，空间 `O(1)`：原地交换，==不要用切片==（会产生额外空间）',
                 '先 `k %= n`：`k ≥ n` 时轮转 `k` 次等同于轮转 `k % n` 次',
                 '反转 `[L, R]` 时，下标 `i` 换到 `L + R − i`（题解附正确性证明）',
                 '题解变形题：改成向左轮转；二维版本见 1260. 二维网格迁移'],
    ),
)
