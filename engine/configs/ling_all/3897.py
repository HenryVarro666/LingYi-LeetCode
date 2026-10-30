N1, N0 = [1, 3, 1, 2], [1, 0, 3, 0]


def _segs(S):
    if 'idx' not in S or 'i' not in S:
        return '先把片段按「没 0 → 1 多 → 0 少」排好序'
    done = S['idx'][:S['idx'].index(S['i']) + 1]
    return '已拼接：`' + ' '.join('1' * S['nums1'][j] + '0' * S['nums0'][j] for j in done) + '`'


CONFIG = dict(
    num=3897, title='连接二进制片段得到的最大值', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='排序比较 · 交换论证',
    tags=['灵神题单', '难度分 1998'],
    code='''
class Solution:
    def maxValue(self, nums1: List[int], nums0: List[int]) -> int:
        # 依次判断：没有 0 的排在最前面，1 多的排前面，0 少的排前面
        idx = sorted(range(len(nums1)), key=lambda i: (nums0[i] != 0, -nums1[i], nums0[i]))

        ans = 0
        for i in idx:
            ans = ((ans + 1) * pow2[nums1[i]] - 1) * pow2[nums0[i]] % MOD
        return ans
''',
    setup='''
MOD = 1_000_000_007
MX = 10001
# 预处理 2 的幂
pow2 = [1] * MX
for i in range(1, MX):
    pow2[i] = pow2[i - 1] * 2 % MOD
''',
    call=f'Solution().maxValue({N1}, {N0})',
    expect=2024,
    views=[
        dict(type='array', var='nums1', label='nums1（每个片段 1 的个数）', pointers={'i': 'blue'}, h=170),
        dict(type='array', var='nums0', label='nums0（每个片段 0 的个数）', pointers={'i': 'blue'}, h=170),
        dict(type='array', var='idx', label='idx（排序后的片段下标，从左到右拼接）',
             color=lambda S, k, v: 'blue' if S.get('i') == v else None, h=170),
        dict(type='text', fn=_segs, size=32, h=80),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'idx = sorted': '排序：`没有 0` 的片段最前，其次 ==1 多的在前==，1 一样多则 ==0 少的在前==。得到 `idx = {idx}`',
        'ans = 0': '`ans` 从空串开始',
        'for i in idx': lambda S, B, r: ('按排好的顺序取片段 `%d`：`%d` 个 1 + `%d` 个 0' % (S.i, S.nums1[S.i], S.nums0[S.i]) if S.i != B.get('i') or S.ans == 0 else '片段都拼完了，退出循环'),
        'ans = ((ans': '右边接 `{nums1[i]}` 个 1：`(ans+1)·2^k − 1`；再接 `{nums0[i]}` 个 0：乘 `2^k`；全程取模，`ans` = =={ans}==',
    },
    cards=dict(
        one_liner='和「最大数」一样排序，只是比较的是 1 和 0 的个数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums1[i]` 个 1 后跟 `nums0[i]` 个 0 组成一个片段，可任意重排后拼接',
                 '求拼出的二进制数最大值，对 `10^9+7` 取余',
                 f'示例：`nums1={N1}`，`nums0={N0}`'],
        quote='本题是 179. 最大数 的二进制版本，做法是一样的。无需先生成字符串再比较：S 中的 1 更多，S 在 T 左边；1 一样多，0 更少的在左边。',
        quote_src='—— 灵茶山艾府题解',
        idea=['比较规则直接用个数算：没 0 的最前，1 多的前，0 少的前',
              '右边接 k 个 0 = 乘 `2^k`；接 k 个 1 = `(ans+1)·2^k − 1`',
              '`2^k` 在 setup 里预处理，每步 `O(1)`'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(n)`',
                 '易错：没有 0 的片段要单独排最前（用 `nums0[i] != 0` 作第一关键字）',
                 '接 1 的公式是 `(ans+1)·2^k − 1`，别漏掉减 1',
                 '`pow2` 预处理放在 setup 中执行，类内代码照原文'],
    ),
)
