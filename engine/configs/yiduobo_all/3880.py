NUMS = [1, 0, 2, 0, 0, 1, 2, 1]


def _color(S, i, v):
    if i == S.get('last_one'):
        return 'cyan'
    if i == S.get('last_two'):
        return 'orange'
    if 'index' in S and i == S['index']:
        return 'yellow'
    return None


def _dim(S, i, v):
    return 'index' in S and i > S['index']


def _txt(S):
    a, b = S.get('last_one'), S.get('last_two')
    if a is None or b is None:
        return f"`last_one = {a}`，`last_two = {b}`：两个都出现过才能配对"
    return f"`last_one = {a}`，`last_two = {b}`：当前最优配对距离 `abs({a} − {b}) = {abs(a - b)}`"


def _if2(S, B, r):
    a, b = S.last_one, S.last_two
    if a is not None and b is not None:
        return f'1 和 2 都出现过：最近的一对是 `({a}, {b})`'
    return '还缺 ' + ('1' if a is None else '2') + '，暂时配不成对'


def _better(S, B, r):
    if S.res == -1:
        return f'`res == -1`：第一次得到答案，`res = {S.dis}`'
    if S.res > S.dis:
        return f'`res = {S.res} > dis = {S.dis}`：找到==更近==的一对'
    return f'`dis = {S.dis}` 不比 `res = {S.res}` 小，不更新'


CONFIG = dict(
    num=3880, title='两个值之间的最小绝对差值', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 · last_one / last_two',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1257'],
    code='''
class Solution(object):
    def minAbsoluteDifference(self, nums):

        last_one = None
        last_two = None

        res = -1
        for index, v in enumerate(nums):
            if v == 1 or v == 2:
                if v == 1:
                    last_one = index
                else:
                    last_two = index

                if last_one is not None and last_two is not None:
                    dis = abs(last_one - last_two)
                    if res == -1 or res > dis:
                        res = dis

        return res
''',
    call=f'Solution().minAbsoluteDifference({NUMS})',
    expect=1,
    views=[
        dict(type='text', fn=_txt, h=90, size=28),
        dict(type='array', var='nums', h=330, cell=104,
             pointers={'index': 'yellow', 'last_one': 'cyan', 'last_two': 'orange'},
             color=_color, dim=_dim, label='nums（青 = 最后一个 1，橙 = 最后一个 2）'),
    ],
    watch=[('index', 'index', 'yellow'), 'v', ('last_one', 'last_one', 'cyan'),
           ('last_two', 'last_two', 'orange'), 'dis', ('res', 'res', 'green')],
    captions={
        'last_one = None': '`last_one`：1 最后一次出现的位置，还没出现 → `None`',
        'last_two = None': '`last_two`：2 最后一次出现的位置',
        'res = -1': '`res = -1`：没有有效对就返回它',
        'for index, v in': lambda S, B, r: (f'遍历：`nums[{S.index}] = {S.v}`' if B.get('index') != S.index
                                            else '遍历结束'),
        'if v == 1 or v == 2': lambda S, B, r: (f'`v = {S.v}`：是 1 或 2，要处理' if S.v in (1, 2)
                                                else '`v = 0`：跳过'),
        'if v == 1:': lambda S, B, r: f'`v = {S.v}`：更新 ' + ('`last_one`' if S.v == 1 else '`last_two`'),
        'last_one = index': '`last_one = {index}`：以后的 2 只需要和==这个最近的 1== 配对',
        'last_two = index': '`last_two = {index}`：以后的 1 只需要和==这个最近的 2== 配对',
        'if last_one is not None': _if2,
        'dis = abs': '`dis = abs({last_one} − {last_two}) = {dis}`',
        'if res == -1 or': _better,
        'res = dis': '`res = {res}`',
        'return res': '返回最小绝对差 =={res}==',
    },
    cards=dict(
        one_liner='只和对面那个数最后一次出现的位置配对',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 只含 0、1、2；`nums[p] == 1` 且 `nums[q] == 2` 的 `(p, q)` 是有效的',
                 '求有效对中 `abs(p − q)` 的==最小值==，没有就返回 `-1`',
                 '示例：`[1,0,0,2,0,1]` → `2`；本视频 `[1,0,2,0,0,1,2,1]` → `1`'],
        quote='若p < q，那么q必然是与q左侧==最后一次出现的p==，也就是1上次出现的位置对应的p组队才是最优的。',
        quote_src='—— yiduobo 题解原文',
        idea=['无论 1 在左还是 2 在左，右边那个只需和左侧==最近==的另一个数配对',
              '用 `last_one`、`last_two` 记录 1 和 2 最后一次出现的位置',
              '每遇到 1 或 2 就更新对应位置，再用 `abs(last_one − last_two)` 更新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先更新位置、再算距离：当前元素一定是这一对里的右端',
                 '`res == -1` 表示还没有答案，要单独判断，不能直接取 min',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未作改动'],
    ),
)
