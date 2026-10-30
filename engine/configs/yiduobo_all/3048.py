NUMS = [2, 2, 0]
CI = [2, 2, 2, 2, 3, 2, 2, 1]


def _col(S, i, v):
    last = S.get('last')
    if last is None or S.get('mid') is None or i > S['mid']:
        return None
    return 'blue' if last.get(v) == i else None


def _top(S):
    mid = S.get('mid')
    if mid is None:
        return '减 1 可以随时做，标记必须等到归零 → 每个下标的标记放在 ==mid 内最靠后==的一秒，二分 mid'
    if 'r' in S and S.get('flag') is not None and S.get('index_list') is not None:
        return f'按最晚标记时间排序后依次处理，`r = {S["r"]}` 次可用的减 1 机会，`pre = {S["pre"]}`'
    return f'试探 `mid = {mid}`（第 0 到 {mid} 秒，下标从 0 记）：每个下标取最晚出现的位置（蓝格）'


def _cmp(S, B, ret):
    need = S.nums[S.index]
    if S.r < need:
        return f'`r = {S.r}` < `nums[{S.index}] = {need}`：减 1 次数不够 → 这个 mid ==不可行=='
    return f'`r = {S.r}` >= `nums[{S.index}] = {need}`：够用 → 花掉 {need} 次'


def _gain(S, B, ret):
    g = S.last[S.index + 1] - S.pre - 1
    return f'下标 `{S.index + 1}` 的标记在第 `{S.last[S.index + 1]}` 秒，和上一个标记（`pre = {S.pre}`）之间空出 `{g}` 秒 → 可用减 1 次数 `r = {S.r}`'


CONFIG = dict(
    num=3048, title='标记所有下标的最早秒数 I', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 最晚标记 + 贪心排序',
    tags=['灵神题单·二分算法', '难度分 2263'],
    code='''
class Solution(object):
    def earliestSecondToMarkIndices(self, nums, changeIndices):

        m = len(changeIndices)
        n = len(nums)

        left = 0
        right = m
        while left < right:
            mid = (left + right) // 2
            last = {}
            for index in range(mid + 1):
                last[changeIndices[index]] = index
            
            if len(last) != n:
                left = mid + 1
                continue
            
            index_list = sorted(range(n), key=lambda d:last[d + 1])
            r = 0
            pre = -1
            flag = True
            for index in index_list:
                r += last[index + 1] - pre - 1
                if r < nums[index]:
                    flag = False
                    break
                else:
                    r -= nums[index]
                
                pre = last[index + 1]
            
            if flag:
                right = mid
            else:
                left = mid + 1
        
        if left == m:
            return -1
        return left + 1
''',
    call=f'Solution().earliestSecondToMarkIndices({NUMS}, {CI})',
    expect=8,
    views=[
        dict(type='text', fn=_top, size=24, h=100),
        dict(type='array', var='changeIndices', label='changeIndices（蓝 = 该下标在前 mid+1 秒里最晚出现的位置，灰 = 超出 mid）', cell=84, h=230,
             pointers={'mid': 'yellow'}, dim=lambda S, i, v: S.get('mid') is not None and i > S['mid'], color=_col),
        dict(type='array', var='nums', label='nums（需要的减 1 次数）', cell=100, h=150),
        dict(type='map', var=lambda S: S.get('last') if S.get('mid') is not None else {}, label='last：下标(从1) → 最晚标记的秒', h=130,
             fmt=lambda k, v: f'下标{k} → 秒{v}'),
        dict(type='text', fn=lambda S: f"处理顺序 `index_list = {S['index_list']}`" if S.get('index_list') is not None and S.get('mid') is not None else '', size=22, h=60),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('r', 'r', 'cyan'), ('pre', 'pre', 'orange')],
    captions={
        'm = len': '`m = {m}` 秒',
        'n = len': '`n = {n}` 个下标要标记',
        'left = 0': '二分下界 `left = 0`',
        8: '上界 `right = m = {right}`：停在这里表示做不到 → -1',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：继续二分' if S.left < S.right else f'`left = right = {S.left}`：二分结束'),
        'mid = (left + right)': '猜一个时间：`mid = ({left} + {right}) // 2 = {mid}`（前 `mid + 1` 秒内）',
        'last = {}': '`last` 记录每个下标最晚出现的秒数',
        'for index in range(mid + 1)': lambda S, B, r: ('前 mid+1 秒扫完了，每个下标的最晚位置都记下了' if B.get('index') == S.index and 'last' in B
                                                      else f'扫第 `{S.index}` 秒'),
        'last[changeIndices[index]]': '下标 `{changeIndices[index]}` 最晚出现在第 `{index}` 秒（后面的会覆盖前面）',
        'if len(last) != n': '`len(last) = {len(last)}` {"!=" if len(last) != n else "=="} `n = {n}`：{"有下标在 mid 内根本没出现，没法标记 → mid 太小" if len(last) != n else "每个下标都出现过"}',
        'left = mid + 1': '`left = {left}`：`mid` 不够，下界抬到 mid + 1',
        'continue': '跳过后面的检查，回到二分',
        'index_list = sorted': '按最晚标记时间从小到大排序：先标记的下标要先把 nums 减到 0。`index_list = {index_list}`',
        'r = 0': '`r` = 目前攒下的“可用减 1 的秒数”',
        'pre = -1': '`pre` = 上一次标记所在秒，现在还没有',
        'flag = True': '`flag` 先假设可行',
        'for index in index_list': lambda S, B, r: ('所有下标都顺利标记了' if B.get('index') == S.index and 'r' in B and B.get('pre') == S.pre and S.get('flag') else f'处理下标 `{S.index + 1}`（nums = {S.nums[S.index]}）'),
        'r += last[index + 1]': _gain,
        'if r < nums[index]': _cmp,
        'flag = False': '`flag = False`：不可行',
        'break': '不用再看了，直接结束这轮检查',
        'r -= nums[index]': '把 `{nums[index]}` 次减 1 用在这个下标上：`r = {r}`',
        'pre = last[index + 1]': '`pre` 更新为这个标记所在秒 `{pre}`',
        'if flag': '`flag = {flag}`：{"mid 可行 → 答案 <= mid，`right = mid`" if flag else "mid 不可行 → 答案 > mid，`left = mid + 1`"}',
        'right = mid': '`right = {right}`',
        'if left == m': '`left = {left}` {"== m：每个 mid 都不行 → -1" if left == m else "< m：有解"}',
        'return -1': '无法标记所有下标，返回 `-1`',
        'return left + 1': '`left` 是从 0 开始的下标，换成秒数要 +1：`{left} + 1` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='标记放最晚，减 1 放前面：二分 mid，按最晚标记时间排序贪心',
        complexity='时间 `O(m log m + n log n)`，空间 `O(n)`',
        problem=['`nums` 和 `changeIndices` 下标从 1 开始。每秒可以：某个 `nums[i]` 减 1；或标记 `changeIndices[s]`（要求它已为 0）；或不动',
                 '求标记完所有下标的==最早秒数==，做不到返回 `-1`',
                 f'本视频：`nums = {NUMS}`，`changeIndices = {CI}` → `8`'],
        quote='对于单个下标，执行标记操作的最佳时间必然是小于等于mid且最靠后的时间，因为这样才能预留出尽量多的时间来执行减1操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['有“什么都不做”的操作 → 时间越多越容易，满足二分',
              '每个下标的标记放在 `mid` 内最晚出现的那一秒，用哈希表 `last` 记录',
              '按 `last` 从小到大排序，边走边累计空出的秒数 `r`，`r` 够减 `nums[index]` 就扣掉，不够就失败'],
        summary=['时间 `O(m log m + n log n)`（每次二分排序一次），空间 `O(n)`',
                 '`len(last) != n` 说明有下标在 `mid` 内一次都没出现，直接不可行',
                 '代码里秒数从 0 开始计，返回时要 `left + 1`',
                 '上界取 `m`：二分停在 `m` 表示无解，返回 `-1`',
                 '原文已是 Python 3 可运行的写法（`//` 整除），无需改动；对比灵神：灵神倒着扫、不用排序'],
    ),
)
