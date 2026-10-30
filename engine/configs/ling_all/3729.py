NUMS, K = [1, 1, 1, 2, 2, 3], 3


def _win(S):
    return S.get('last_start')


def _txt(S):
    if 'pre_sum' not in S:
        return '`cnt` 存前缀和模 k 的个数；一段相同元素遍历完，才把它的前缀和放进 `cnt`'
    i = S.get('i')
    ps = S['pre_sum']
    return f'前缀和 `{ps}`，模 `{K}` = ==`{ps % K}`==　当前相同段从下标 `{S["last_start"]}` 开始'


def _color(S, i, v):
    ls, cur = S.get('last_start'), S.get('i')
    if cur is None or ls is None:
        return None
    return 'blue' if ls <= i <= cur else None


CONFIG = dict(
    num=3729, title='统计有序数组中可被 K 整除的子数组数量', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='974 题前缀和余数 + 相同段延迟入表',
    tags=['前缀和与哈希表', '难度分 2248'],
    code='''
class Solution:
    def numGoodSubarrays(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)
        cnt[0] = 1  # 见 560 题
        pre_sum = 0  # 前缀和
        last_start = 0  # 上一个连续相同段的起始下标
        ans = 0

        for i, x in enumerate(nums):
            if i and x != nums[i - 1]:
                # 上一个连续相同段结束，可以把上一段对应的前缀和添加到 cnt
                v = nums[i - 1]
                s = pre_sum
                for _ in range(i - last_start):
                    cnt[s % k] += 1
                    s -= v
                last_start = i

            pre_sum += x
            ans += cnt[pre_sum % k]

        return ans
''',
    call=f'Solution().numGoodSubarrays({NUMS}, {K})',
    expect=5,
    skip=['cnt = defaultdict', 'pre_sum = 0', 'last_start = 0', 'ans = 0', 'v = nums[i - 1]', 's = pre_sum',
          's -= v', 'for _ in range'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前连续相同段，只统计左端点在它之前的子数组）', cell=96, h=230,
             pointers={'i': 'blue'}, color=_color),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='map', var='cnt', label='cnt（前缀和 % k → 个数；只含已结束的段）', fmt=lambda k, v: f'{k}: {v}', h=210, font=30),
    ],
    watch=[('i', 'i', 'blue'), ('pre_sum', 'pre_sum', 'orange'), ('last_start', 'last_start', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'cnt[0] = 1': '空前缀的和是 0，余数 0 先记一个（见 560 题）',
        'for i, x in enumerate(nums)': lambda S, B, r: (f'`x = nums[{S.i}] = {S.x}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        'if i and x != nums[i - 1]': lambda S, B, r: (f'`{S.x} ≠ {S.nums[S.i - 1]}`：上一个相同段结束了，==现在才==把它的前缀和放进 `cnt`'
                                                      if S.i and S.x != S.nums[S.i - 1]
                                                      else ('第一个数，没有上一段' if not S.i else f'`{S.x}` 和前一个相同：还在同一段，先不登记')),
        'cnt[s % k] += 1': '补登记上一段每个位置的前缀和：余数 `{s % k}` 个数 → `{cnt[s % k]}`（`s = {s}`）',
        'last_start = i': '新的相同段从下标 `{i}` 开始',
        'pre_sum += x': '`pre_sum` 加上 `{x}` → `{pre_sum}`',
        'ans += cnt[pre_sum % k]': '`pre_sum % k = {pre_sum % k}`，`cnt` 里有 `{cnt[pre_sum % k]}` 个相同余数 → 就有这么多个以 `{i}` 结尾的好子数组 → `ans = {ans}`',
        'return ans': '一共 `{ans}` 个不同的好子数组',
    },
    max_steps=70,
    cards=dict(
        one_liner='只有“全是同一个数”的子数组会重复，所以相同段的前缀和延迟入表',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['非降序数组 `nums` 和正整数 `k`，子数组元素和能被 `k` 整除就是好子数组',
                 '数值序列相同的子数组只算一个，求不同好子数组的个数',
                 '本视频：`nums = [1,1,1,2,2,3]`，`k = 3` → `5`'],
        quote='对于连续相同元素段，我们要保证哈希表暂时不包含这一段对应的前缀和，等遍历完这一段，再把对应的前缀和加到哈希表中。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['非降序 ⇒ 进入窗口的数比离开的大，含多种数的子数组两两不同',
              '重复只来自==同一个数==构成的子数组',
              '遍历相同段时 `cnt` 不含本段前缀和：左端点最多在段首，不会重复数同一种'],
        summary=['时间 `O(n)`，空间 `O(n)`；内层循环总次数不超过 `n`',
                 '974 题的写法：余数相同的两个前缀和之差被 `k` 整除',
                 '易错：段结束时才登记，且要登记整段每个位置的前缀和',
                 '方法一：先按 974 题全数一遍，再对每段减去重复的个数 `size - sz`'],
    ),
)
