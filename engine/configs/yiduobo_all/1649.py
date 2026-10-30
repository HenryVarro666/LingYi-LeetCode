def _nz(S):
    a = S.get('index_array')
    return {i: v for i, v in enumerate(a) if v} if a else {}


def _txt(S):
    if 'smaller' not in S or 'same' not in S:
        return '每个数 `num`：`smaller` = 前面比它小的个数，`bigger` = 前面比它大的个数，代价取较小者'
    return f"前面共 `{S['index']}` 个数：`bigger = {S['index']} − same({S['same']}) − smaller({S['smaller']})` = =={S['index'] - S['same'] - S['smaller']}=="


def _path(x):
    r = []
    while x <= 100001:
        r.append(x)
        x += x & -x
    return r


def _forcap(S, B, ret):
    if 'num' not in B or 'num' not in S and False:
        return f"取第一个数 `num = {S.num}`，数组还是空的"
    pre = f"上一个数 `{B.num}` 已插入：从节点 `{B.num}` 沿 `lowbit` 向上，每个节点 +1（{'→'.join(str(v) for v in _path(B.num)[:5])}…共 {len(_path(B.num))} 个）。"
    if 'num' in S and S['_inner'].get('index') != B.index:
        return pre + f"下一个 `num = {S.num}`"
    return pre + '没有更多指令了'


CONFIG = dict(
    num=1649, title='通过指令创建有序数组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='树状数组 · 只求小于，大于用减法',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def createSortedArray(self, instructions):

        index_array = [0] * 100001
        cnt_dict = {}
        res = 0
        mod = 10 ** 9 + 7
        for index, num in enumerate(instructions):
            tmp = num - 1
            smaller = 0
            while tmp > 0:
                smaller += index_array[tmp]
                tmp -= tmp & -tmp
            
            same = cnt_dict.get(num, 0)
            bigger = index - same - smaller
            res += min(smaller, bigger)
            if res >= mod:
                res -= mod

            cnt_dict[num] = same + 1
            tmp = num
            while tmp <= 100001:
                index_array[tmp] += 1
                tmp += tmp & -tmp

        return res
''',
    call='Solution().createSortedArray([3,1,3,2])',
    expect=1,
    views=[
        dict(type='array', var='instructions', label='instructions（依次插入，当前处理的数高亮）', cell=90, h=230,
             pointers={'index': 'blue'}),
        dict(type='map', var=_nz, label='树状数组 index_array（只显示非 0 的节点：下标 → 计数）', fmt=lambda k, v: f'[{k}] = {v}', h=250, font=28),
        dict(type='map', var='cnt_dict', label='cnt_dict（之前每个数出现的次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=30),
        dict(type='text', fn=_txt, h=90, size=28),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num', 'cyan'), ('tmp', 'tmp', 'orange'), ('smaller', 'smaller', 'pink'),
           ('same', 'same', 'purple'), ('res', 'res', 'green')],
    skip=['while tmp', 'tmp -= tmp & -tmp', 'tmp += tmp & -tmp', 'index_array[tmp] += 1', 'index_array = [0]', 'mod = ', 'res = 0', 'smaller = 0', 22],
    max_steps=90,
    captions={
        'cnt_dict = {}': '哈希表记录“前面每个数出现过几次”，用来得到 `same`',
        'tmp = num - 1': '先查“比 `{num}` 小的个数”= 前缀和 `[1..{num-1}]`：从 `tmp = {tmp}` 开始，每次去掉最低位',
        'smaller += index_array[tmp]': '树状数组前缀和：累加节点 `{B.tmp}` 的计数 `{index_array[B.tmp]}` → `smaller = {smaller}`，然后 `tmp` 去掉最低位',
        'same = cnt_dict.get': '前面和 `{num}` 相等的有 `same = {same}` 个',
        'bigger = index': '前面一共 `{index}` 个数，去掉相等和更小的，剩下的都更大：`bigger = {bigger}`',
        'res += min': '代价取两侧较小者：`min({smaller}, {bigger})` = {min(smaller, bigger)} → `res = {res}`',
        'res -= mod': '超过模数就减一次 `mod`',
        'cnt_dict[num] = same + 1': '记下 `{num}` 又出现一次：`cnt_dict[{num}] = {same + 1}`；接着把 `{num}` 插入树状数组（沿 `tmp += lowbit` 逐级向上，每级加一）',
        'for index, num in enumerate': _forcap,
        'return res': '全部插入完，总代价 `{res}`',
    },
    cards=dict(
        one_liner='只求“比它小的个数”，“比它大的”靠减法得到',
        complexity='时间 `O(n log U)`，空间 `O(U)`（U = 值域 10^5）',
        problem=['按顺序把 `instructions` 的每个数插入一个有序数组，插入代价 = ==min(比它小的个数, 比它大的个数)==（只数已在数组里的）',
                 '返回总代价对 `10^9+7` 取模',
                 '本视频：`instructions = [3,1,3,2]` → `1`'],
        quote='对于当前处理的数num，不妨设这个数是数组中的第k个数，那么其前方一共就有k - 1个数。这些数可以分成三个部分，分别是大于num的，小于num的，以及等于num的。',
        quote_src='—— yiduobo 题解原文',
        idea=['“等于”最好求：哈希表计数 → `same`',
              '“小于 num”用树状数组前缀和 → `smaller`',
              '“大于” = `index − same − smaller`，不必再查一次，一个树状数组就够'],
        summary=['时间 `O(n log U)`，空间 `O(U)`',
                 '易错：查询的是 `num - 1` 的前缀和，不含等于 `num` 的',
                 '易错：`bigger = index - same - smaller`，`index` 是插入前已有的个数',
                 '树状数组下标从 1 开始，所以值域数组开 `100001`',
                 '原文本身可直接在 Python 3 运行，没有改动'],
    ),
)
