def _bins(S):
    return '  '.join(f'{d}:{b}' for d, b in enumerate(S['bin_list']) if b) or '（空）'


def _txt(S):
    if 'bin_list' not in S:
        return '`rank[t]` = 只看最后 t 位时，下标从小到大的顺序'
    return f'桶（数字:下标）　{_bins(S)}'


CONFIG = dict(
    num=2343, title='裁剪数字后查询第 K 小的数字', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='基数排序预处理 rank',
    tags=['灵神题单·常用数据结构', '难度分 1652'],
    code='''
class Solution(object):
    def smallestTrimmedNumbers(self, nums, queries):

        n = len(nums)
        rank = [list(range(n))]
        order = [list(range(n))]

        m = len(nums[0])

        for rnd in range(1, m + 1):
            bin_list = [[] for _ in range(10)]
            for r in rank[-1]:
                digit = int(nums[r][-rnd])
                bin_list[digit].append(r)
            
            rank.append([])
            for digit in range(0, 10):
                rank[-1].extend(bin_list[digit])

        res = [rank[trim][k - 1] for k, trim in queries]
        
        return res
''',
    call='Solution().smallestTrimmedNumbers(["24","37","96","04"], [[2,1],[2,2]])',
    expect=[3, 0],
    views=[
        dict(type='array', var='nums', label='nums', cell=110, h=170,
             color=lambda S, i, v: ('blue' if 'r' in S and 'digit' in S and i == S['r'] and S.get('_line') in (14, 15) else None)),
        dict(type='table', var='rank', label='rank[t]：只看最后 t 位的从小到大顺序（行 t）', h=210, cell=84, rows=['t=0','t=1','t=2']),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    watch=[('rnd', 'rnd', 'yellow'), ('r', 'r', 'blue'), ('digit', 'digit', 'pink'), ('res', 'res', 'green')],
    captions={
        'rank = [': '`rank[0] = [0..n-1]`：一位都不看时，顺序就是下标顺序',
        'm = len': '每个数 `m = {m}` 位，要做 `m` 轮',
        'for rnd': lambda S, B, r: ('每一位都排完了' if getattr(B, 'rnd', None) == S.rnd else f'第 =={S.rnd}== 轮：加入倒数第 {S.rnd} 位，按这一位分桶'),
        'bin_list = ': '准备 10 个空桶，对应数字 0–9',
        'for r in rank[-1]': lambda S, B, r: ('这一轮的下标都放进桶里了' if getattr(B, 'r', None) == S.r else f'按 `rank[{S.rnd-1}]` 的顺序取下标 `r = {S.r}`（必须按上一轮的顺序遍历）'),
        'digit = int': '`nums[{r}] = {nums[r]}` 的倒数第 {rnd} 位是 =={digit}==',
        'bin_list[digit].append': lambda S, B, r: f'下标 `{S.r}` 放进桶 `{S.digit}`' + ('：同桶里先放进来的，后面的位更小' if S.rnd > 1 else '：第一轮没有更低位，同桶按下标顺序'),
        'rank.append': '开始收集这一轮的结果 `rank[{rnd}]`',
        'rank[-1].extend': lambda S, B, r: (f'桶 `{S.digit}` 是空的，跳过' if not S.bin_list[S.digit] else f'桶 `{S.digit}` 里的下标 `{S.bin_list[S.digit]}` 依次接到 `rank[{S.rnd}]` 后面 → `{S.rank[-1]}`'),
        'res = [': '每个询问 `[k, trim]` 直接查表：`rank[trim][k-1]` → `{res}`',
        'return res': '答案 `{res}`',
    },
    skip=['order = ', 'for digit in range'],
    max_steps=110,
    cards=dict(
        one_liner='裁剪后比大小就是基数排序：每多一位，分桶收集一次',
        complexity='时间 `O(mn + q)`，空间 `O(mn)`',
        problem=['`nums` 是等长数字字符串，询问 `[k, trim]`：只留最右 `trim` 位，求第 `k` 小的下标',
                 '相等时下标小的算小',
                 '本视频：`["24","37","96","04"]`，`[[2,1],[2,2]]` → `[3,0]`'],
        quote='题目中描述的裁剪数字的过程与经典的基数排序非常像，那么当然就应该用基数排序来预处理出数组在每一种裁剪情况下的大小顺序了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`rank[t]` 记录只看最后 `t` 位时的排序结果，`rank[0]` 就是 `0..n-1`',
              '第 `rnd` 轮：按 `rank[rnd-1]` 的顺序，把下标放进“倒数第 `rnd` 位”对应的桶',
              '桶按 0–9 收集：不同数字由桶决定大小，相同数字由遍历顺序（上一轮的顺序）决定'],
        summary=['时间 `O(mn + q)`，空间 `O(mn)`',
                 '易错：必须按 `rank[rnd-1]` 从小到大遍历，桶内才保持稳定',
                 '原文为 Python 2 写法，`range(n)` 在 Python 2 里是列表，已改为 `list(range(n))`',
                 '对比灵神：灵神把询问按 trim 排序，用稳定的 `sort` 增量排；yiduobo 一次性预处理所有 rank'],
    ),
)
