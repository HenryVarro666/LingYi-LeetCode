def _bits(S):
    t = S.get('target')
    if t is None:
        return ''
    i = S.get('i', 0)
    return f"target = {t} = `{bin(t)[2:]}`　当前看第 =={i}== 位，已累计的小数之和 `s` = =={S.get('s', 0)}=="


CONFIG = dict(
    num=2835, title='使子序列的和等于目标的最少操作次数', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='从低位到高位贪心', tags=['位运算', '贪心与思维', '难度分 2207'],
    code='''
class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        cnt = Counter(nums)
        ans = s = i = 0
        while 1 << i <= target:
            s += cnt[1 << i] << i
            mask = (1 << (i + 1)) - 1
            i += 1
            if s >= target & mask:
                continue
            ans += 1  # 一定要找更大的数操作
            while cnt[1 << i] == 0:
                ans += 1  # 还没找到，继续找更大的数
                i += 1
        return ans
''',
    call='Solution().minOperations([1,32,1,2], 12)',
    expect=2,
    views=[
        dict(type='text', fn=_bits, h=70),
        dict(type='array', var='nums', label='nums', h=150),
        dict(type='map', var='cnt', fmt=lambda k, v: f'{k}: {v}个', h=260),
    ],
    watch=['i', ('s', 's', 'cyan'), 'mask', ('ans', 'ans', 'green')],
    captions={
        'sum(nums) < target': '每个数都能拆成 1，总和不够 `target` 就一定无解：`{sum(nums)} < {target}` → 不成立，有解',
        'cnt = Counter': '统计每个 2 的幂出现几次：`cnt = {dict(cnt)}`',
        'while 1 << i <= target': '`2^i = {1 << i}`，只要不超过 `target = {target}` 就继续看下一位',
        's += cnt': '把恰好等于 `2^{i}` 的数全加进来：`s` = =={s}==（`s` 是所有 ≤ 2^i 的数之和）',
        'mask =': '`mask = {mask}`：只关心 `target` 的低 `{i+1}` 位',
        10: '位数 +1：`i` = {i}',
        16: '往更大的一位找：`i` → =={i}==',
        'if s >= target & mask': '`s = {s}` 与 `target & mask = {target & mask}` 比：' + '{"够，能凑出低位，不用操作" if s >= target & mask else "不够，低位凑不出来"}',
        'continue': '小数之和够凑 → 不用操作，看下一位',
        13: '小数不够 → 必须拆更大的数：`ans` → =={ans}==',
        'while cnt[1 << i] == 0': '看 `{1 << i}` 有没有：`cnt[{1 << i}] = {cnt[1 << i]}` → ' + '{"没有，还要往更大找" if cnt[1 << i] == 0 else "有，拆它"}',
        15: '这一层也没有，再往上找，多拆一次：`ans` → =={ans}==',
        'return ans': '最少操作 `{ans}` 次',
    },
    cards=dict(
        one_liner='低位到高位贪心：小数凑不够，才去拆更大的数',
        complexity='时间 `O(n + log target)`，空间 `O(log target)`',
        problem=['`nums` 全是 2 的幂；一次操作把一个 `>1` 的数拆成两个一半',
                 '求最少操作次数，使某个子序列的和等于 `target`，不可能返回 -1',
                 '示例：`[1,32,1,2]`，`target=12` → `2`'],
        quote='如果 target 的第 i 位是 1，那么先看看所有 ≤ 2^i 的元素和能否 ≥ target&mask。如果能，那么必然可以合并出 target&mask，无需操作。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先判无解：所有数都能拆成 1，总和不够就是 -1',
              '从低位到高位，小数之和 `s` 够凑低位 → 免费',
              '不够就必须拆一个更大的 `2^j`，拆到 `2^i`，中间的 `2^i … 2^(j-1)` 都有了，直接跳到第 j 位'],
        summary=['时间 `O(n + log target)`，空间 `O(log target)`',
                 '易错：拆完后要把 `i` 直接跳到 `j`，中间各位不用再判',
                 '每往上找一层都算一次操作',
                 '先用 `sum(nums) < target` 排除无解'],
    ),
)
