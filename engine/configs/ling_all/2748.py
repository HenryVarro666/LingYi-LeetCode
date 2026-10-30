from math import gcd as _gcd

_P = 'sum(cnt) - (_line == 11) if _line != 12 else None'


def _idx(S):
    if 'cnt' not in S or S.get('_line') == 12:
        return None
    return sum(S['cnt']) - (S.get('_line') == 11)


def _cnt_color(S, i, v):
    j = _idx(S)
    if j is None or j >= len(S['nums']) or S.get('_line') not in (5, 6, 7, 8):
        return 'pink' if S.get('_line') == 11 and i == S.get('x') else None
    d = S['nums'][j] % 10
    if S.get('_line') == 8 and i == S.get('y'):
        return 'orange'
    if i > 0 and _gcd(i, d) == 1:
        return 'green' if v else 'cyan'
    return None


def _txt(S):
    j = _idx(S)
    if j is None or j >= len(S['nums']):
        return '`cnt[y]`：左边最高位为 `y` 的数有几个'
    d = S['nums'][j] % 10
    ys = [y for y in range(1, 10) if _gcd(y, d) == 1]
    if S.get('_line') in (9, 10, 11):
        return f"求 `{S['nums'][j]}` 的最高位：`x = {S['x']}`"
    return f"末位 `{S['nums'][j]} % 10 = {d}`，与它互质的最高位：==" + ','.join(map(str, ys)) + '=='


def _for_cap(S, B, r):
    if _idx(S) >= len(S.nums):
        return '遍历结束'
    d = S.x % 10
    bad = [str(y) for y in range(1, 10) if S.cnt[y] and _gcd(y, d) != 1]
    tail = f'；左边最高位 {"、".join(bad)} 与 {d} ==不互质==，不计' if bad else ''
    return f'枚举 `x = nums[j] = {S.x}`，末位 `{d}`' + tail


CONFIG = dict(
    num=2748, title='美丽下标对的数目', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 统计最高位',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1301'],
    code='''
class Solution:
    def countBeautifulPairs(self, nums: List[int]) -> int:
        ans = 0
        cnt = [0] * 10
        for x in nums:
            for y, c in enumerate(cnt):
                if c and gcd(y, x % 10) == 1:
                    ans += c
            while x >= 10:
                x //= 10
            cnt[x] += 1  # 统计最高位的出现次数
        return ans
''',
    call='Solution().countBeautifulPairs([25,51,13,4,36])',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（x = 当前枚举的 nums[j]）', pointers={_P: 'blue'}, pointer_labels={_P: 'x'}, h=200,
             dim=lambda S, i, v: _idx(S) is not None and i > _idx(S)),
        dict(type='array', var='cnt', label='cnt[y]：左边最高位为 y 的个数（绿/青 = 与末位互质，橙 = 正在累加）', h=200, cell=70,
             color=_cnt_color),
        dict(type='text', fn=_txt, h=90, size=30),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'cyan'), ('c', 'c'), ('ans', 'ans', 'green')],
    skip=['for y, c in enumerate', 'if c and gcd'],
    captions={
        'ans = 0': '`ans` 统计美丽下标对',
        'cnt = [0] * 10': '最高位只有 1~9：用长为 10 的 `cnt` 统计==左边==的最高位',
        'for x in nums': _for_cap,
        'ans += c': '`gcd({y}, {x % 10}) = 1`：左边有 `{c}` 个最高位是 `{y}` 的数都能配 → `ans = {ans}`',
        'while x >= 10': lambda S, B, r: (f'`x = {S.x} ≥ 10`，还不是最高位' if S.x >= 10 else f'`x = {S.x}` 只剩一位，就是最高位'),
        'x //= 10': '去掉末位：`x = {x}`',
        'cnt[x] += 1': '查询完再计入：`cnt[{x}]` → `{cnt[x]}`，供右边的数配对',
        'return ans': '一共 `{ans}` 组美丽下标对',
    },
    cards=dict(
        one_liner='不枚举 nums[i]，只枚举 9 种最高位',
        complexity='时间 `O(n(k + log U))`，空间 `O(k)`，`k = 10`',
        problem=['`i < j` 且 `nums[i]` 的==第一个数字==与 `nums[j]` 的==最后一个数字==互质，就是美丽下标对',
                 '示例：`[2,5,1,4]` → `5`',
                 '本视频：`[25,51,13,4,36]` → `7`'],
        quote='由于 nums[i] 的最高位在 [1,9] 中，我们可以在遍历数组的同时，==统计最高位的出现次数==，这样就只需枚举 [1,9] 中的与 x mod 10 互质的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举右边的 `x = nums[j]`，只关心它的末位 `x % 10`',
              '左边的数只关心最高位，用 `cnt` 计数',
              '对每个 `y` 互质就加 `cnt[y]`：内层循环最多 10 次'],
        summary=['时间 `O(n(k + log U))`，空间 `O(k)`',
                 '先累加答案，再把 `x` 的最高位计入 `cnt`，保证 `i < j`',
                 '`if c and …`：`cnt[y] = 0` 时直接跳过（动画中跳过了不贡献的 y）',
                 '优化：可预处理 9 以内所有数对的 GCD'],
    ),
)
