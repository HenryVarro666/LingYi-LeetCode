def _txt(S):
    if 'v' not in S:
        return ''
    out = f"当前 `v = {S['v']}`"
    if 'mi' in S and 'ma' in S:
        out += f"，前一个同奇偶回文数 `mi = {S['mi']}`，后一个 `ma = {S['ma']}`"
    elif 'x' in S and S.get('_line', 0) >= 14:
        out += f"，用前半段拼出的回文数 `x = {S['x']}`"
    return out


CONFIG = dict(
    num=4053, title='使每个元素变为回文数的最少操作次数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='贪心：前半段生成回文 · 找前后同奇偶回文数',
    tags=[],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        res = 0

        for v in nums:
            s = str(v)
            length = len(s)
            half_len = (length + 1) // 2
            half = s[:(length + 1) // 2]
            if int(s[0]) % 2 == v % 2:
                if half_len * 2 == length:
                    x = half + half[::-1]
                else:
                    x = half + half[::-1][1:]
                
                x = int(x)
                if x == v:
                    continue
                
                if x > v:
                    ma = x
                    half = str(int(half) - 1)
                    if len(half) != half_len:
                        mi = int('8' + '9' * (length - 3) + '8')
                    elif int(half[0]) % 2 != v % 2:
                        if half[0] == '1':
                            if length == 2:
                                mi = 8
                            else:
                                mi = int('8' + '9' * (length - 3) + '8')
                        else:
                            h = str(int(half[0]) - 1)
                            mi = int(h + '9' * (length - 2) + h)
                    else:
                        if half_len * 2 == length:
                            x = half + half[::-1]
                        else:
                            x = half + half[::-1][1:]
                        mi = int(x)
                
                else:
                    mi = x
                    half = str(int(half) + 1)
                    if int(half[0]) % 2 != v % 2:
                        if half[0] == '9':
                            ma = int('2' + '0' * (length - 1) + '2')
                        else:
                            h = str(int(half[0]) + 1)
                            ma = int(h + '0' * (length - 2) + h)
                    else:
                        if half_len * 2 == length:
                            x = half + half[::-1]
                        else:
                            x = half + half[::-1][1:]
                        ma = int(x)

            else:
                if half[0] == '1':
                    if length == 2:
                        mi = 8
                    else:
                        mi = int('8' + '9' * (length - 3) + '8')
                else:
                    h = str(int(half[0]) - 1)
                    mi = int(h + '9' * (length - 2) + h)
                
                if half[0] == '9':
                    ma = int('2' + '0' * (length - 1) + '2')
                else:
                    h = str(int(half[0]) + 1)
                    ma = int(h + '0' * (length - 2) + h)

            res += min(ma - v, v - mi) // 2
        
        return res
''',
    call='Solution().minOperations([10, 125, 1211])',
    expect=8,
    views=[
        dict(type='array', var='nums', label='nums', cell=120, h=220,
             color=lambda S, i, v: 'blue' if v == S.get('v') else None),
        dict(type='text', fn=_txt, size=32, h=140),
    ],
    watch=[('v', 'v', 'blue'), ('half', 'half', 'cyan'), ('mi', 'mi', 'pink'), ('ma', 'ma', 'orange'), ('res', 'res', 'green')],
    skip=['length = len(s)', 'half_len = ', 'half = s[:'],
    captions={
        'for v in nums': lambda S, B, r: (f'取出 `v = {S.v}`：要找前一个 `mi`、后一个 `ma` 同奇偶回文数'
                                          if 'v' not in B or B.v != S.v or S.get('res') != B.get('res') else '所有数都处理完了'),
        's = str(v)': '转成字符串 `s = "{s}"`，让后半段去适配前半段 `half`（尽量不改高位）',
        'if int(s[0]) % 2 == v % 2': '`half` 最高位 `{s[0]}` 与 `v` 奇偶{"相同" if int(s[0]) % 2 == v % 2 else "不同"} → {"不改 half 就可能拼出同奇偶回文数" if int(s[0]) % 2 == v % 2 else "必须改最高位，直接算 mi 和 ma"}',
        'x = half + half[::-1][1:]': '奇数长度：`half` 加上反转后去掉首位 → `x = {x}`',
        'x = half + half[::-1]': '偶数长度：`half` 加上它的反转 → `x = {x}`',
        'x = int(x)': '用前半段拼出的回文数 `x = {x}`',
        'if x == v': '`x == v`？{"相等，v 本身就是回文数，不用操作" if x == v else "不相等"}',
        'if x > v': '`x = {x}` {">" if x > v else "<"} `v = {v}` → {"x 是后一个回文数 ma，还要找前一个 mi" if x > v else "x 是前一个回文数 mi，还要找后一个 ma"}',
        'ma = x': '`ma = {ma}`',
        'half = str(int(half) - 1)': '`half` 减 1 → `{half}`：这样拼出的回文数一定小于 v',
        'half = str(int(half) + 1)': '`half` 加 1 → `{half}`：这样拼出的回文数一定大于 v',
        'mi = x': '`mi = {mi}`',
        "mi = int('8' + '9'": '`half` 退位后的最高位要保持偶数 → 取 `8 99..9 8` 形式：`mi = {mi}`',
        'mi = 8': '两位数且高位是 1：前一个同奇偶回文数就是 `8`',
        'mi = int(h + ': '最高位减 1 后补 9：`mi = {mi}`',
        'mi = int(x)': '`half` 减 1 后拼出 `mi = {mi}`',
        "ma = int('2' + ": '`half` 最高位是 9，上一位只能进到 `2 00..0 2`：`ma = {ma}`',
        'ma = int(h + ': '最高位加 1 后补 0：`ma = {ma}`',
        'ma = int(x)': '`half` 加 1 后拼出 `ma = {ma}`',
        'if len(half) != half_len': '`half` 减 1 后位数变了？{"变了：原来是 100..0，只能降到 899..98" if len(half) != half_len else "没变"}',
        'elif int(half[0]) % 2 != v % 2': '减 1 后的最高位 `{half[0]}` 与 `v` 奇偶{"不同" if int(half[0]) % 2 != v % 2 else "相同"} → {"要再调整最高位" if int(half[0]) % 2 != v % 2 else "直接用 half 拼"}',
        'if int(half[0]) % 2 != v % 2': '加 1 后的最高位 `{half[0]}` 与 `v` 奇偶{"不同" if int(half[0]) % 2 != v % 2 else "相同"} → {"要再调整最高位" if int(half[0]) % 2 != v % 2 else "直接用 half 拼"}',
        "if half[0] == '1'": '`half` 最高位是 1 吗？{"是，不能直接减 1，只能降到 8 开头" if half[0] == "1" else "不是，最高位可以直接减 1"}',
        "if half[0] == '9'": '`half` 最高位是 9 吗？{"是，只能升到 2 开头" if half[0] == "9" else "不是，最高位可以直接加 1"}',
        'if length == 2': '`length == 2`？{"是，两位数的最大偶回文是 8" if length == 2 else "不是"}',
        'res += min(': lambda S, B, r: f'`min(ma - v, v - mi) // 2` = `min({S.ma - S.v}, {S.v - S.mi}) // 2` = {min(S.ma - S.v, S.v - S.mi) // 2} → `res = {S.res}`',
        'return res': '全部处理完，最少操作次数 =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='尽量不改高位：用前半段生成回文数，再向两边找同奇偶的邻居',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['一次操作：`nums[i]` 加 2 或减 2，要把每个数都变成正回文数',
                 '不同元素可以变成不同回文数，求最少总操作次数',
                 '示例：`[125]` → 125 减 2 两次变成 121，答案 `2`'],
        quote='为了使得操作的次数最少，那么就应该尽量不去修改高位，也就是让s的后半部分去适配前半部分。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个 `v` 要找同奇偶的前一个 `mi`、后一个 `ma`，代价 `min(ma-v, v-mi) // 2`',
              '前半段 `half` 的最高位奇偶要和 `v` 相同，才能不改 half 直接拼回文数 `x`',
              '`x > v` 时 x 是 ma，half 减 1 求 mi；`x < v` 时 x 是 mi，half 加 1 求 ma'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '易错：减 1 / 加 1 会借位进位，最高位奇偶变了就要重新调整，如 `899..98`、`200..02`',
                 '特判：两位数且高位为 1 时，前一个同奇偶回文数是 `8`',
                 '对比灵神：灵神把候选收敛成至多 5 个取最小；yiduobo 按 half 大小分情况推 mi 和 ma'],
    ),
)
