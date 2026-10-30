def _txt(S):
    I = S.get('_inner', S)
    if 'num_list' in I and 'used' in I:
        used = {k: v for k, v in I['used'].items() if v}
        return f"待配对的“需要 2x”：`{used}`" if used else '当前没有悬着的“需要 2x”'
    if 'pos_list' in S:
        return f"正数 `{S['pos_list']}`　负数取反 `{S['neg_list']}`　零 `{S.get('zero_cnt', 0)}` 个"
    return '把数组拆成 正数 / 负数(取反) / 零 三部分'


CONFIG = dict(
    num=954, title='二倍数对数组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='分正负 + 最小堆贪心配对',
    tags=['灵神题单'],
    code='''
import heapq

class Solution(object):
    def canReorderDoubled(self, arr):

        pos_list = []
        neg_list = []
        zero_cnt = 0
        for num in arr:
            if num > 0:
                pos_list.append(num)
            elif num < 0:
                neg_list.append(-num)
            else:
                zero_cnt += 1
        
        if zero_cnt % 2 == 1:
            return False

        if len(pos_list) % 2 == 1:
            return False

        if len(neg_list) % 2 == 1:
            return False

        return self.check(pos_list) and self.check(neg_list)

    def check(self, num_list):
        heapq.heapify(num_list)
        used = {}
        while num_list:
            min_num = heapq.heappop(num_list)
            if used.get(min_num, 0) > 0:
                used[min_num] -= 1
            else:
                used[min_num * 2] = used.get(min_num * 2, 0) + 1
        
        return sum(used.values()) == 0
''',
    call='Solution().canReorderDoubled([8,1,-4,4,2,-2])',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='arr', h=150, label='arr'),
        dict(type='heap', var='num_list', h=220, label='num_list（最小堆，每次取最小）'),
        dict(type='map', var='used', h=220, label='used：放在奇数位、等待配对的数 → 次数',
             fmt=lambda k, v: f'{k} ×{v}'),
    ],
    watch=[('min_num', 'min_num', 'blue'), ('zero_cnt', 'zero_cnt', 'cyan')],
    captions={
        'for num in arr': '逐个看 `arr` 的数，按正负零分开',
        'pos_list.append': '`{num} > 0`：放进正数部分',
        'neg_list.append': '`{num} < 0`：取相反数 `{-num}` 放进负数部分（两边都变成正数问题）',
        'zero_cnt += 1': '`0` 的二倍还是 `0`，只能和 0 配对：`zero_cnt = {zero_cnt}`',
        'if zero_cnt % 2': lambda S, B, r: f'`zero_cnt = {S.zero_cnt}`：' + ('奇数，落单的 0 无法配对 → `False`' if S.zero_cnt % 2 else '偶数，0 自己能配好'),
        'if len(pos_list) % 2': lambda S, B, r: f'正数个数 `{len(S.pos_list)}`：' + ('奇数，必有落单 → `False`' if len(S.pos_list) % 2 else '偶数，继续'),
        'if len(neg_list) % 2': lambda S, B, r: f'负数个数 `{len(S.neg_list)}`：' + ('奇数，必有落单 → `False`' if len(S.neg_list) % 2 else '偶数，继续'),
        'return self.check': '正数和负数两部分，各自检查能否配成 “x 与 2x”',
        'heapq.heapify': '建成最小堆：堆顶永远是剩下的最小数 `{num_list[0]}`',
        'used = {}': '`used` 记录“已经有人在等 2x”的数',
        'while num_list': lambda S, B, r: (f'堆里还有 `{len(S.num_list)}` 个数，继续' if S.num_list else '堆空了，所有数都处理完'),
        'min_num = heapq.heappop': '取出当前最小的 `x = {min_num}`',
        'if used.get(min_num': lambda S, B, r: (f'`used[{S.min_num}] = {S.used.get(S.min_num, 0)} > 0`：之前有数在等它 → ==x 放在奇数位=='
                                               if S.used.get(S.min_num, 0) > 0 else
                                               f'`{S.min_num}` 没人等：它比后面的数都小，不可能是别人的二倍 → ==x 放偶数位，需要一个 {S.min_num * 2}=='),
        'used[min_num] -= 1': '配对成功：`used[{min_num}]` 减 1 → `{used[min_num]}`',
        'used[min_num * 2] =': '登记：还需要 1 个 `{min_num * 2}` → `used[{min_num * 2}] = {used[min_num * 2]}`',
        'return sum(used.values())': lambda S, B, r: f'`used` 里还欠 `{sum(S.used.values())}` 个 → ' + ('全部配齐，`True`' if sum(S.used.values()) == 0 else '有数没配上，`False`'),
    },
    cards=dict(
        one_liner='先分正负零，再从最小的数开始配 x 与 2x',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `arr` 长度为偶数，能否重排成 `arr[2i+1] = 2 * arr[2i]`',
                 '就是问：能否把所有数两两配成 “x 和 2x”',
                 '示例：`[8,1,-4,4,2,-2]` → `True`（1-2、2-4、4-8 取绝对值后配对）'],
        quote='设当前剩下数中最小的数为x，如果x没有通过之前处理的数放在奇数位上，由于x不可能是之后剩下数的两倍，因此当前的x必然要放在偶数位上，同时还需要一个2x放在x对应的奇数位上。',
        quote_src='—— yiduobo 题解原文',
        idea=['正数的二倍是正数、负数的二倍是负数、0 的二倍是 0 → 拆成三部分',
              '负数取相反数后，和正数是同一个问题',
              '最小的数只能当“x”，必须找一个 `2x`；用 dict 记录欠了几个'],
        summary=['时间 `O(n log n)`（堆），空间 `O(n)`',
                 '三部分各自个数必须是偶数，先剪枝',
                 '`used` 为空（全为 0）才算成功，不是只看堆空',
                 '原文本身可直接在 Python 3 运行，未做修改'],
    ),
)
