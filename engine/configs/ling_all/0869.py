CONFIG = dict(
    num=869, title='重新排序得到 2 的幂', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序后判字母异位词', tags=['难度分 1505'],
    code='''
pow_two_sorted_str_set = {''.join(sorted(str(1 << i))) for i in range(30)}

class Solution:
    def reorderedPowerOf2(self, n: int) -> bool:
        s = ''.join(sorted(str(n)))
        return s in pow_two_sorted_str_set
''',
    call='Solution().reorderedPowerOf2(46)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"n = ==46==，数位排序后 `s` = =={S['s']}==" if 's' in S else 'n = ==46==，先看预处理好的集合', h=60),
        dict(type='string', var='s', h=150, label='s（n 的数位排序后）'),
        dict(type='text', fn=lambda S: '预处理集合（2^0 ~ 2^29 排序后）含：' + ' '.join('==%s==' % x if x == S.get('s') else x for x in sorted({''.join(sorted(str(1 << i))) for i in range(30)}, key=lambda x: (len(x), x))[:36]) + ' …', h=330, size=28),
    ],
    watch=['n', 's'],
    captions={
        'pow_two_sorted_str_set =': '预处理：把 `2^0 ~ 2^29` 各自转成字符串、数位排序，放进集合。`64` 排序后是 `46`',
        's = ': '`n = {n}` 的数位排序得 `s = {s}`：排序后相同 = ==字母异位词==，说明能互相重排',
        'return s in': '`{s}` 在集合里吗？→ ==`{ret}`==（`64` 排序后正是 `46`）',
    },
    cards=dict(
        after=[dict(heading='两个优化（灵神注）', lines=['注 1：用长为 `10` 的数组统计每个数位出现次数，可免去排序', '注 2：位数与 `n` 相同的 2 的幂至多 `4` 个（最高位 `1,2,4,8`）', '所以只需枚举至多 4 个 2 的幂做比较，复杂度与 `10^9` 无关']),],
        one_liner='n 能重排成 2 的幂 = 它和某个 2 的幂是字母异位词',
        complexity='时间 `O(M log M)`（M 为位数），空间 `O(M)`',
        problem=['把正整数 `n` 的数位任意重排（不能有前导零），能否得到 2 的幂',
                 '示例：`n = 1` → `true`；`n = 10` → `false`',
                 '本视频：`n = 46`，重排为 `64 = 2^6` → `true`'],
        quote='换句话说，n 和某个 2^k 是字母异位词。如果 n 的十进制字符串排序后的字符串，等于某个 2^k 的十进制字符串排序后的字符串，那么返回 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数据范围 `n ≤ 10^9`，2 的幂只有 `2^0 ~ 2^29` 共 30 个',
              '把它们的数位排序后存进哈希集合，只预处理一次',
              '查询时把 `n` 也排序，看是否在集合里即可'],
        summary=['时间 `O(M log M)`，空间 `O(M)`，预处理不计入',
                 '排序后字符串即“数位多重集”的标准形，天然去掉了顺序',
                 '前导零不用特判：2 的幂没有前导零，排序结果等价于合法重排',
                 '灵神还提到：用长为 10 的数组计数可免排序；同位数的 2 的幂至多 4 个，可做到与 10^9 无关'],
    ),
)
