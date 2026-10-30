NUMS = [18, 43, 36, 13, 7]

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _color(S, i, v):
    k = _k(S)
    if k is None:
        return None
    if i == k:
        return 'blue'
    mn = S.get('max_num') or {}
    if i < k and v in mn.values():
        return 'green'
    return None


def _dim(S, i, v):
    k = _k(S)
    return k is not None and i > k


def _txt(S):
    if 'tmp' not in S:
        return '按数位和分类，每一类只记==最大==的数'
    if S['tmp']:
        return f"拆数位：`tmp = {S['tmp']}`，已累加 `digit_s = {S['digit_s']}`"
    return f"`{S['num']}` 的数位和 `digit_s = {S['digit_s']}`"


def _in(S, B, r):
    d = S.digit_s
    if d not in S.max_num:
        return f'数位和 {d} ==第一次出现==：还没有能配对的数'
    return f'数位和 {d} 已出现过（最大 `{S.max_num[d]}`）→ 可以配对'


CONFIG = dict(
    num=2342, title='数位和相等数对的最大和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按数位和分类 · 哈希表记最大值',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1309'],
    code='''
class Solution(object):
    def maximumSum(self, nums):

        res = -1
        max_num = {}
        for num in nums:
            digit_s = 0
            tmp = num
            while tmp:
                digit_s += tmp % 10
                tmp //= 10

            if digit_s not in max_num:
                max_num[digit_s] = num
            else:
                res = max(res, max_num[digit_s] + num)
                if num > max_num[digit_s]:
                    max_num[digit_s] = num

        return res
''',
    setup=TRACK,
    call=f'Solution().maximumSum(TList({NUMS}))',
    expect=54,
    skip=['digit_s = 0', 'tmp //= 10', 'while tmp'],
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var='nums', h=260, cell=120, pointers={_k: 'blue'}, pointer_labels={_k: 'num'},
             color=_color, dim=_dim, label='nums（蓝 = 当前 num，绿 = 某类数位和的当前最大值）'),
        dict(type='map', var='max_num', label='max_num（数位和 → 已遍历的最大数）',
             fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
    ],
    watch=[('num', 'num', 'blue'), 'tmp', 'digit_s', ('res', 'res', 'green')],
    captions={
        'res = -1': '`res = -1`：找不到数对就返回它',
        'max_num = {}': '`max_num[d]`：已遍历的数中，数位和为 `d` 的==最大值==',
        'for num in nums': lambda S, B, r: (f'遍历到 `num = {S.num}`' if _k(S) is not None else '遍历结束'),
        'tmp = num': '用 `tmp` 拆 `{num}` 的每一位',
        'digit_s += tmp % 10': lambda S, B, r: (f'取末位 `{B.tmp} % 10 = {B.tmp % 10}`，`digit_s = {S.digit_s}`；'
                                                f'再 `tmp //= 10`'),
        'if digit_s not in max_num': _in,
        'max_num[digit_s] = num': '`max_num[{digit_s}] = {num}`',
        'res = max': lambda S, B, r: (f'这一类目前最大的 `{S.max_num[S.digit_s]}` 与 `{S.num}` 配对：和 '
                                      f'`{S.max_num[S.digit_s] + S.num}`，'
                                      + (f'==更新== `res = {S.res}`' if S.res != B.res else f'不超过 `{S.res}`')),
        'if num > max_num': lambda S, B, r: (f'`{S.num} > {S.max_num[S.digit_s]}`：它成为这一类的新最大值'
                                             if S.num > S.max_num[S.digit_s]
                                             else f'`{S.num}` 不比 `{S.max_num[S.digit_s]}` 大，不用更新'),
        'return res': '返回最大和 =={res}==',
    },
    cards=dict(
        one_liner='按数位和分类，每类只要最大的两个数',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['选 `i ≠ j`，要求 `nums[i]` 与 `nums[j]` 的==数位和相等==',
                 '求 `nums[i] + nums[j]` 的最大值，不存在返回 `-1`',
                 '示例：`[18,43,36,13,7]` → `54`（18 + 36，数位和都是 9）'],
        quote='由于这里只需要知道每种数位和中最大的两个数，那么也可以从左向右一趟遍历，只记录下当前遍历过的数中==每种数位和的最大值==。',
        quote_src='—— yiduobo 题解原文',
        idea=['自然的想法：按数位和分好类，每类取==最大的两个数==相加',
              '一趟遍历即可：`max_num` 只存每类当前最大值',
              '数位和出现过就用 `max_num[d] + num` 更新答案，再视情况更新最大值'],
        summary=['时间 `O(n log U)`，空间 `O(n)`（哈希表）',
                 '先用旧的最大值配对，再更新：避免和自己配对',
                 '用 `% 10` 和整除拆数位，比转字符串更快',
                 '原文为 Python 2 写法，`tmp /= 10` 已改为 `tmp //= 10`'],
    ),
)
