NUMS = [2, 4, 1, 4, 3, 2]


def _right(S):
    """循环体内（第 11–20 行）窗口是 [l, r]；其余时候 r 指向下一个要加入的数，窗口是 [l, r-1]"""
    r = S.get('r')
    if r is None:
        return None
    return r if 11 <= S.get('_line', 0) <= 20 else r - 1


def _pcolor(S, k, v):
    if 'pos' in S and 12 <= S.get('_line', 0) <= 14 and k == S['pos'] and 'r' in S and k != S['r']:
        return 'red'
    if 'r' in S and k == S['r'] and 11 <= S.get('_line', 0) <= 20:
        return 'pink'
    return None


def _scolor(S, k, v):
    if S.get('_line') not in (16, 17, 19):
        return None
    r, l = len(S['s']) - 1, S['l']
    if k == r:
        return 'green'
    if l > 0 and k == l - 1:
        return 'orange'
    return None


def _text(S):
    if 'r' not in S or 'res' not in S:
        return ''
    l, r, s = S['l'], _right(S), S['s']
    if r >= len(s):
        return ''
    if l > 0:
        return f'窗口 `[{l}, {r}]` 的和 = `s[{r}] − s[{l - 1}]` = {s[r]} − {s[l - 1]} = =={s[r] - s[l - 1]}=='
    return f'窗口 `[0, {r}]` 的和 = `s[{r}]` = =={s[r]}=='


def _cap_pos(S, B, ret):
    if S['pos'] == -1:
        return f'`{S["nums"][S["r"]]}` 之前没出现过：`pos = -1`'
    return f'`{S["nums"][S["r"]]}` 上一次出现在 `pos = {S["pos"]}`'


def _cap_if_pos(S, B, ret):
    pos, l, x = S['pos'], S['l'], S['nums'][S['r']]
    if pos >= l:
        return f'`pos = {pos} >= l = {l}`：l 到 r 之间==已经有了 {x}== → 左边界要移到它后面'
    if pos >= 0:
        return f'`pos = {pos} < l = {l}`：上次的 {x} ==已经在窗口外==，l 可以保持不变'
    return f'`pos = -1 < l = {l}`：l 保持不变'


def _cap_if_l(S, B, ret):
    if S['l'] > 0:
        return f'`l = {S["l"]} > 0`：区间和 = 前缀和相减，要减去 `s[l - 1]`'
    return '`l = 0`：区间和就是前缀和 `s[-1]` 本身'


def _cap_while(S, B, ret):
    r = B['r']
    if r < len(S['nums']):
        return f'`r = {r} < {len(S["nums"])}`：右边界 r 向右移动，加入 `nums[{r}] = {S["nums"][r]}`'
    return f'`r = {r}`：右边界枚举完毕'


CONFIG = dict(
    num=1695, title='删除子数组的最大得分', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='滑动窗口 + 上次出现位置 + 前缀和',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def maximumUniqueSubarray(self, nums):
        last_pos = {}
        s = [nums[0]]
        l = 0
        r = 1
        now = 0
        res = nums[0]
        last_pos[nums[0]] = 0
        while r < len(nums):
            s.append(s[-1] + nums[r])
            pos = last_pos.get(nums[r], -1)
            if pos >= l:
                l = pos + 1

            if l > 0:
                res = max(res, s[-1] - s[l - 1])
            else:
                res = max(res, s[-1])
            last_pos[nums[r]] = r
            r += 1

        return res
''',
    call=f'Solution().maximumUniqueSubarray({NUMS})',
    expect=10,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums（框 = 窗口 [l, r]，红 = 上一次出现的位置）',
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', lambda S: _right(S)), color=_pcolor,
             dim=lambda S, k, v: 'l' in S and k < S['l'], h=240, cell=100),
        dict(type='array', var='s', label='s（前缀和：s[i] = nums[0] + … + nums[i]）', color=_scolor, h=200, cell=100),
        dict(type='map', var='last_pos', label='last_pos（数字 → 上一次出现的位置）', h=120, fmt=lambda k, v: f'{k}→{v}'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('pos', 'pos', 'red'), ('res', 'res', 'green')],
    captions={
        'last_pos = {}': '用一个 dict 记录下==每个数字上一次出现的位置==',
        's = [nums[0]]': '区间和问题转化成前缀和：`s[i]` = `nums[0..i]` 之和',
        'l = 0': '窗口左边界 `l = 0`',
        'r = 1': '从左向右枚举窗口的右边界，`r` 从 1 开始',
        'res = nums[0]': '只含 `nums[0]` 的窗口：`res = {res}`',
        'last_pos[nums[0]] = 0': '`{nums[0]}` 出现在位置 0',
        'while r < len(nums)': _cap_while,
        's.append': '前缀和 `s[{r}] = s[{r - 1}] + nums[{r}] = {s[-2]} + {nums[r]} = {s[-1]}`',
        'pos = last_pos.get': _cap_pos,
        'if pos >= l': _cap_if_pos,
        'l = pos + 1': '左边界==直接跳到== `pos + 1 = {l}`，不用一步步挪',
        'if l > 0': _cap_if_l,
        'res = max(res, s[-1] - s[l - 1])': '区间 `[{l}, {r}]` 和 = `{s[-1]} - {s[l - 1]} = {s[-1] - s[l - 1]}` → `res = {res}`',
        'res = max(res, s[-1])': '区间 `[0, {r}]` 和 = `{s[-1]}` → `res = {res}`',
        'last_pos[nums[r]] = r': '更新 `{nums[r]}` 上一次出现的位置为 `{r}`',
        'return res': '最大得分 =={ret}==',
    },
    skip=['now = 0', 'r += 1'],
    cards=dict(
        one_liner='记下每个数上次出现的位置，左边界一步跳过重复；区间和用前缀和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['正整数数组 `nums`，删除一个==元素互不相同==的子数组，得分 = 子数组元素和',
                 '只删除一个子数组，求==最大得分==',
                 '示例：`[2,4,1,4,3,2]` → `10`（子数组 `[1,4,3,2]`）'],
        quote='设nums[r\']上一次出现的位置为p，若p >= l，说明l到r之间已经有了nums[r\']，此时就需要移动左边界l到p + 1的位置，否则l可以保持不变。',
        quote_src='—— yiduobo 知乎题解',
        idea=['从左向右枚举右边界 r，左边界 l ==只会跟着向右移动==',
              '`last_pos` 记录每个数字上一次出现的位置 p：`p >= l` 就把 l 跳到 `p + 1`',
              '确定 l 后，窗口和 = 前缀和相减 `s[r] − s[l−1]`，用它更新答案'],
        summary=['时间 `O(n)`，空间 `O(n)`（dict + 前缀和数组）',
                 '易错：`p < l` 时==不能==移动 l（例子里最后的 2：上次在 0，早已出窗口）',
                 '`l = 0` 时没有 `s[l-1]`，所以要分情况；代码里的 `now` 没有用到',
                 '对比灵神：集合 + 逐步缩窗口；这里 dict 让 l 一步到位',
                 '原文为 Python 2 风格，已删去类型文档字符串，代码未改'],
    ),
)
