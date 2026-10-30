CONFIG = dict(
    num='LCP 40', title='心算挑战', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='排序取最大 + 奇偶替换', tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def maximumScore(self, cards: List[int], cnt: int) -> int:
        cards.sort(reverse=True)
        s = sum(cards[:cnt])  # 最大的 cnt 个数之和
        if s % 2 == 0:  # s 是偶数
            return s

        def replaced_sum(x: int) -> int:
            for v in cards[cnt:]:
                if v % 2 != x % 2:  # 找到一个最大的奇偶性和 x 不同的数
                    return s - x + v  # 用 v 替换 s
            return 0

        x = cards[cnt - 1]
        ans = replaced_sum(x)  # 替换 x
        for v in cards[cnt - 1::-1]:
            if v % 2 != x % 2:  # 找到一个最小的奇偶性和 x 不同的数
                ans = max(ans, replaced_sum(v))  # 替换
                break
        return ans
''',
    call='Solution().maximumScore([3,6,5,4,1,8], 3)',
    expect=18,
    views=[
        dict(type='array', var='cards', label='cards（从大到小）', h=260, window=('0', 'cnt - 1'),
             color=lambda S, i, v: ('cyan' if v % 2 == 0 else 'orange') if 's' in S else None),
        dict(type='text', fn=lambda S: (f"前 `cnt={S['cnt']}` 个之和 `s` = =={S['s']}== （{'偶数，直接返回' if S['s'] % 2 == 0 else '奇数，要换掉一个奇偶不同的数'}）" if 's' in S else '先从大到小排序（蓝=偶数，橙=奇数）')),
    ],
    watch=['cnt', 's', 'x', ('ans', 'ans', 'green')],
    captions={
        'cards.sort': '从大到小排序：`{cards}`，想拿的当然是最大的数',
        's = sum': '最大的 `cnt={cnt}` 个数：`{cards[:cnt]}`，和 `s` = =={s}==',
        'if s % 2 == 0': '`s % 2 = {s % 2}` → {"偶数，已经是最大的有效得分" if s % 2 == 0 else "奇数，无效，得换一个数"}',
        'x = cards[cnt - 1]': '`x = {x}`：前 cnt 个里最小的数，奇偶性必是「最小的奇数」或「最小的偶数」之一，==必定被替换==',
        'ans = replaced_sum(x)': '方案一：替换 `x={x}` → `ans = {ans}`',
        'if v % 2 != x % 2': '`v={v}` 和 `x={x}` 奇偶{"不同" if v % 2 != x % 2 else "相同"}',
        'return s - x + v': '后面最大的奇偶不同数是 `{v}`：`s - x + v = {s} - {x} + {v}` = =={ret}==',
        'ans = max(ans, replaced_sum(v))': '方案二：换掉最小的异性数 `v={v}`：`ans = max(旧值 {B.ans}, 方案二)` = =={ans}==',
        'return 0': '后面没有奇偶合适的数 → 这个方案不行，返回 0',
        'return ans': '两种替换取较大：=={ret}==',
    },
    cards=dict(
        one_liner='取最大的 cnt 个；和是奇数就换一个奇偶不同的数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['从 `cards` 里选 `cnt` 张，数字和为偶数才有效，得分就是和',
                 '求最大有效得分，没有有效方案返回 `0`',
                 '示例：`[1,2,8,9], cnt=3` → `18`'],
        quote='如果 s 是奇数，那么可以：从前 cnt 个数中去掉一个最小的奇数，从后 n-cnt 个数中加进来一个最大的偶数；或者去掉一个最小的偶数，加进来一个最大的奇数。两种情况取最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先取最大的 `cnt` 个，和为 `s`；是偶数就是最优',
              '奇数时必须改奇偶：==前面去掉一个，后面补一个，奇偶性不同==',
              '`cards[cnt-1]` 是前 cnt 个里最小的，一定要被替换；另一种情况找奇偶不同的最小数'],
        summary=['时间 `O(n log n)`，快速选择可到 `O(n)`；空间 `O(1)`',
                 '易错：只需替换一个数，换多个只会更小',
                 '易错：找不到可替换的数时 `replaced_sum` 返回 0，表示该方案无效',
                 '思考题：和是 3 的倍数 → 1262. 可被三整除的最大和'],
    ),
)
