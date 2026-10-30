def _b(x):
    return format(x, '04b')


def _state(S):
    if 'once' not in S:
        return ''
    if '_inner' in S and 'num' not in S['_inner']:
        pass
    lines = []
    if 'num' in S:
        lines.append(f"`num` = `{_b(S['num'])}`")
    lines.append(f"`once` = `{_b(S['once'])}`　`twice` = `{_b(S['twice'])}`")
    return '　　'.join(lines)


def _hit(S):
    if 'hit_once_once' not in S:
        return ''
    return (f"找出现一次的：状态 `{_b(S['hit_once_once'])}` / `{_b(S['hit_once_twice'])}`　"
            f"找出现两次的：状态 `{_b(S['hit_twice_once'])}` / `{_b(S['hit_twice_twice'])}`")


CONFIG = dict(
    num=3595, title='一次或两次', difficulty='Medium', category='位运算',
    author='yiduobo', technique='模 3 计数 · 先求 mask 再筛选',
    tags=['灵神题单·位运算'],
    code='''
class Solution(object):
    def onceTwice(self, nums):
        
        def nxt(once, twice, num):
            return ~twice & (once ^ num), (once ^ twice) & (twice ^ num)

        once, twice = 0, 0
        for num in nums:
            once, twice = nxt(once, twice, num)

        hit_once_once, hit_once_twice = 0, 0
        hit_twice_once, hit_twice_twice = 0, 0
        for num in nums:
            if num & once == once and num & twice == 0:
                hit_once_once, hit_once_twice = nxt(hit_once_once, hit_once_twice, num)
            if num & twice == twice and num & once == 0:
                hit_twice_once, hit_twice_twice = nxt(hit_twice_once, hit_twice_twice, num)

        return hit_once_once, hit_twice_twice
''',
    call='Solution().onceTwice([5, 3, 3, 6, 6, 6])',
    expect=(5, 3),
    views=[
        dict(type='array', var='nums', label='nums：5 出现 1 次，3 出现 2 次，6 出现 3 次', h=170,
             color=lambda S, i, v: ('yellow' if S.get('num') == v else None)),
        dict(type='text', fn=_state, size=24, h=80),
        dict(type='text', fn=_hit, size=24, h=80),
    ],
    watch=[('once', 'once', 'blue'), ('twice', 'twice', 'pink'),
           ('hit_once', "hit_once_once", 'green'), ('hit_twice', "hit_twice_twice", 'orange')],
    captions={
        'once, twice = 0, 0': '`once`、`twice` 按位记录「该位上 1 的个数 mod 3」：余 1 记在 once，余 2 记在 twice',
        'once, twice = nxt(once, twice, num)': '读入 `{num}`（`{num:04b}`），交给 `nxt` 做一次模 3 计数',
        'hit_once_once, hit_once_twice = 0, 0': '第二遍要分别统计两个目标：先准备找「只出现一次」的计数器',
        'hit_twice_once, hit_twice_twice = 0, 0': '再准备找「出现两次」的计数器',
        'if num & once == once': lambda S, B, r: (
            f'`{S.num:04b}` 含 once 掩码 `{S.once:04b}` 且不含 twice 掩码 `{S.twice:04b}` → '
            + ('==成立==，像出现一次的数' if (S.num & S.once == S.once and S.num & S.twice == 0) else '不成立，跳过')),
        'hit_once_once, hit_once_twice = nxt': '只把符合 once 特征的数重新做模 3 计数',
        'if num & twice == twice': lambda S, B, r: (
            f'`{S.num:04b}` 含 twice 掩码 `{S.twice:04b}` 且不含 once 掩码 `{S.once:04b}` → '
            + ('==成立==，像出现两次的数' if (S.num & S.twice == S.twice and S.num & S.once == 0) else '不成立，跳过')),
        'hit_twice_once, hit_twice_twice = nxt': '只把符合 twice 特征的数做模 3 计数',
        'return ~twice': '`nxt` 返回新的 `(once, twice) = ({ret[0]:04b}, {ret[1]:04b})`：各位 1 的个数模 3 的新状态',
        'return hit_once_once': '出现一次的是 `{ret[0]}`，出现两次的是 `{ret[1]}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='先用模 3 求出两个数的特征 mask，再筛出来重算',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组中一个数出现 1 次，一个数出现 2 次，其余都出现 3 次',
                 '要求 `O(n)` 时间、`O(1)` 空间，找出这两个数',
                 '示例：`[5,3,3,6,6,6]` → `(5, 3)`'],
        quote='只能确定特有的mask，但是无法直接定位到这两个数，理由是一个出现一次的元素，配合上另一个出现两次的元素，可以让某些二进制位上刚好达到3次。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 137 题一样，统计每一位上 1 的个数模 3：余 1 记入 `once`，余 2 记入 `twice`',
              '但两个数的某些位会凑成 3 次被抵消，所以得到的只是 ==特有的 mask==',
              '第二遍：挑出符合 mask 的数，再模 3 计数，就能还原出那两个数'],
        summary=['时间 `O(n)`，空间 `O(1)`，只有若干个整数变量',
                 '`nxt` 是模 3 计数器的状态转移：`(once, twice)` 在 00 → 01 → 10 → 00 之间循环',
                 '易错：第一遍结果只是 mask，不能直接当答案；位被抵消时 mask 会缺位',
                 '筛选条件：含 once 的位且不含 twice 的位，才可能是出现一次的数（twice 同理）',
                 '原文可直接在 Python 3 运行，无需修改'],
    ),
)
