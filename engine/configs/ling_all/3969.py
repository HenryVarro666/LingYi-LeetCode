_IN_FOR = '_line in (12, 14, 15, 16, 17, 18, 19, 20)'
_SP = f'pre.index(s) if {_IN_FOR} else None'


def _k(S):
    return len(str(S['low'])) - 1


def _pcolor(S, i, v):
    if S.get('_line') in (12, 14, 15, 16, 17, 18, 19, 20) and 's' in S and v == S['s']:
        return 'orange'
    return None


def _cnt_color(S, i, v):
    if v < 0:
        return 'red'
    if S.get('_line') in (14, 15, 16, 17, 18, 19, 20) and 's' in S and i == (S['s'] - S['x']) % 10:
        return 'green'
    return 'cyan' if v > 0 else None


def _txt(S):
    if 'low' not in S:
        return '子数组 `[ℓ, r)` 的和 = `pre[r] − pre[ℓ]`；首位和末位都要等于 `x`'
    low, high, x = S['low'], S['high'], S['x']
    k = _k(S)
    head = f'本轮：和 ∈ `[{low}, {high - 1}]`（首位是 {x} 的 {k + 1} 位数）'
    ln = S['_line']
    if ln < 12 or ln > 20 or 's' not in S:
        return head
    s = S['s']
    if ln == 20:
        t = (s - x) % 10
        return f'末位：`pre[ℓ] % 10 = ({s} − {x}) % 10 = ` =={t}==；窗口里这样的有 ==`{S["cnt"][t]}`== 个'
    return head + f'；`s = {s}`：窗口内 `{s - high} < pre[ℓ] ≤ {s - low}`'


def _w1(S, B, ret):
    if B.pre[B.left1] <= B.s - B.high:
        return f'`pre[{B.left1}] = {B.pre[B.left1]} ≤ s − high = {B.s - B.high}`：位数超了 → ==踢出窗口=='
    return f'`pre[{B.left1}] = {B.pre[B.left1]} > s − high = {B.s - B.high}`：不用踢'


def _w2(S, B, ret):
    if B.pre[B.left2] <= B.s - B.low:
        return f'`pre[{B.left2}] = {B.pre[B.left2]} ≤ s − low = {B.s - B.low}`：够大 → ==进入窗口=='
    return f'`pre[{B.left2}] = {B.pre[B.left2]} > s − low = {B.s - B.low}`：还不够大'


def _out(S, B, ret):
    d = B.pre[B.left1] % 10
    base = f'末位 {d}：`cnt[{d}]` −1 → `{S.cnt[d]}`，`left1` 右移'
    if S.cnt[d] < 0:
        base = f'`cnt[{d}]` −1 → `{S.cnt[d]}`：还没加入过，先欠着，之后抵消'
    return base


def _in(S, B, ret):
    d = B.pre[B.left2] % 10
    return f'末位 {d}：`cnt[{d}]` +1 → `{S.cnt[d]}`，`left2` 右移'


def _while_low(S, B, ret):
    if S.low <= S.pre[-1]:
        return f'`low = {S.low} ≤ 总和 {S.pre[-1]}`：可能还有 {len(str(S.low))} 位的和 → 继续'
    return f'`low = {S.low} > 总和 {S.pre[-1]}`：不会再有更长的和 → 结束'


CONFIG = dict(
    num=3969, title='求和后首尾数字相同的有效子数组 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 三指针滑动窗口',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def countValidSubarrays(self, nums: list[int], x: int) -> int:
        pre = list(accumulate(nums, initial=0))
        ans = 0

        # 枚举子数组和的十进制长度
        low, high = x, x + 1
        while low <= pre[-1]:
            # 计算子数组和在 [low, high-1] 中，且子数组和模 10 为 x 的子数组个数
            cnt = [0] * 10
            left1 = left2 = 0
            for s in pre:
                # 随着 s 的增大，<= s-high 的前缀和离开窗口，<= s-low 的前缀和进入窗口
                while pre[left1] <= s - high:
                    cnt[pre[left1] % 10] -= 1
                    left1 += 1
                while pre[left2] <= s - low:
                    cnt[pre[left2] % 10] += 1
                    left2 += 1
                ans += cnt[(s - x) % 10]
            low *= 10
            high *= 10

        return ans
''',
    call='Solution().countValidSubarrays([1, 10, 1], 1)',
    expect=4,
    views=[
        dict(type='array', var='pre', label='pre 前缀和（框 = 窗口 pre[left1 .. left2-1]，橙 = 当前 s）', cell=96,
             pointers={'left1': 'pink', 'left2': 'blue', _SP: 'orange'}, pointer_labels={_SP: 's'},
             window=('left1', 'left2 - 1'), color=_pcolor, h=255),
        dict(type='array', var='cnt', label='cnt[d]：窗口里 pre[ℓ] % 10 == d 的个数（绿 = 当前要查的 d）', cell=64, min_slots=10,
             color=_cnt_color, h=130),
        dict(type='text', h=120, size=28, fn=_txt),
    ],
    watch=[('low', 'low', 'cyan'), ('high', 'high', 'cyan'), ('s', 's', 'orange'), ('left1', 'left1', 'pink'), ('left2', 'left2', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'pre = list(accumulate': '前缀和 `pre`：子数组 `[ℓ, r)` 的和 = `pre[r] − pre[ℓ]`',
        'ans = 0': '`ans` 累计有效子数组个数',
        'low, high = x, x + 1': '先看 1 位数：和 ∈ `[{low}, {high - 1}]`，首位就是 `x`；之后每轮乘 10',
        'while low <= pre[-1]': _while_low,
        'cnt = [0] * 10': '`cnt[d]`：窗口里末位是 `d` 的前缀和个数',
        'left1 = left2 = 0': '窗口是 `pre[left1 .. left2-1]`，两个指针都从 0 出发',
        'for s in pre': lambda S, B, r_: (f'枚举右端点：`s = pre[r] = {S.s}`' if 's' not in B or S.s != B.s else '这一轮的 s 都枚举完了'),
        'while pre[left1] <= s - high': _w1,
        'cnt[pre[left1] % 10] -= 1': _out,
        'while pre[left2] <= s - low': _w2,
        'cnt[pre[left2] % 10] += 1': _in,
        'ans += cnt': '要找末位 `({s} − {x}) % 10 = {(s - x) % 10}`：窗口里有 `{cnt[(s - x) % 10]}` 个 → `ans` = =={ans}==',
        'low *= 10': '换下一个位数：`low = {low}`',
        'high *= 10': '`high = {high}`',
        'return ans': '返回 =={ans}==',
    },
    skip=['left1 += 1', 'left2 += 1'],
    max_steps=110,
    cards=dict(
        one_liner='按子数组和的位数分层：窗口管首位，cnt 管末位',
        complexity='时间 `O(n log S)`，空间 `O(n + D)`（`D = 10`）',
        problem=['`nums` 都是正整数。若子数组和的 ==首位== 与 ==末位== 数字都等于 `x`，就是有效子数组',
                 '数有效子数组的个数；示例：`[1,100,1], x=1` → `4`',
                 '本视频：`[1,10,1], x=1` → `4`'],
        quote='枚举子数组和的十进制长度。……用一个滑动窗口维护满足 x·10^k ≤ s[r] − s[ℓ] < (x+1)·10^k 的 s[ℓ] mod 10 的个数。',
        quote_src='—— 灵茶山艾府题解（方法二，公式符号为引用时改写）',
        idea=['固定位数 `k`：和落在 `[x·10^k, (x+1)·10^k)`，首位就是 `x`',
              '末位：`(s[r]−s[ℓ]) % 10 = x` ⇔ `s[ℓ] % 10 = (s[r]−x) % 10`，用 `cnt` 数',
              '元素全为正，`pre` 递增，合格的 `ℓ` 是连续一段：`left1`、`left2` 夹出窗口'],
        summary=['时间 `O(n log S)`（S 为元素和）：每个位数跑一遍 `O(n)` 的滑窗；空间 `O(n + D)`',
                 '`(s − x) % 10` 在 Python 里恒非负；其他语言要先 `+ 10` 再取模',
                 '能用滑窗是因为元素非负；有负数就得换有序集合',
                 '`cnt` 可能暂时出现 −1：`left1` 先越过还没加入的位置，之后被 `left2` 补回',
                 '方法一：暴力枚举左右端点，边累加边判断首末位，`O(n^2 log S)`'],
    ),
)
