NUMS = [3, 1, 1, 2, 5, 1]


def _p2(S):
    return 'index' in S and 'start' in S and 9 <= S.get('_line', 0) <= 12


def _p1(S):
    return 'index' not in S and 'v' in S and 's' in S and S.get('_line') in (4, 5)


ST = lambda S: S['start'] if _p2(S) else None                                  # noqa: E731
IDX = lambda S: S['index'] if 'index' in S and 8 <= S.get('_line', 0) <= 12 else None   # noqa: E731
SM1 = lambda S: S['start'] - 1 if _p2(S) and S['start'] > 0 else None           # noqa: E731


def _cur1(S):
    if not _p1(S):
        return None
    k = len(S['s']) if S['_line'] == 4 else len(S['s']) - 1
    return k if k < len(S['nums']) else None


def _nums_color(S, k, v):
    if _p2(S) and S['start'] <= k <= S['index']:
        return 'cyan'
    if _cur1(S) == k:
        return 'blue'
    return None


def _s_color(S, k, v):
    if _p2(S):
        if k == S['index']:
            return 'green'
        if S['start'] > 0 and k == S['start'] - 1:
            return 'red'
        return None
    if 'index' not in S and 's' in S and k < len(S['s']):
        return 'cyan'
    return None


def _formula(S):
    if 's' not in S:
        return ''
    ln = S.get('_line')
    if 'index' not in S:
        if ln == 3:
            return '`s[k]` = `nums[0..k]` 的和（这里==没有==开头的 0）'
        k = len(S['s']) - 1
        if ln == 5:
            return f"`s[{k}] = s[{k - 1}] + nums[{k}]` = `{S['s'][-2]} + {S['v']}` = =={S['s'][-1]}=="
        return '一趟扫描，把每个前缀和 `nums[0..k]` 存进 `s`'
    i, v, s = S['index'], S['v'], S['s']
    if ln == 7:
        return '`res` 累加每个下标对应的区间和'
    if ln == 8:
        return f"`index = {i}`，`v = nums[{i}] = {v}`：区间 `[index − v, index]`"
    st = S['start']
    if ln == 9:
        return f"`start = max(0, {i} − {v})` = =={st}==，区间 `nums[{st}..{i}]`"
    if ln == 10:
        return f"先加 `s[{i}]` = `nums[0..{i}]` 的和 = =={s[i]}=="
    if ln == 11:
        return f"`start = {st}`：前面{'有' if st > 0 else '没有'}要去掉的前缀"
    if ln == 12:
        return f"`nums[{st}..{i}]` = `s[{i}] − s[{st - 1}]` = `{s[i]} − {s[st - 1]}` = =={s[i] - s[st - 1]}=="
    return f"`res` = =={S['res']}=="


def _for1(S, B, ret):
    if len(S.s) == len(S.nums):
        return f'前缀和算完了：`s = {S.s}`'
    return f'取下一个数 `v = nums[{len(S.s)}] = {S.v}`'


def _for2(S, B, ret):
    if 'index' in B and B.index == S.index:
        return '所有下标都处理完了，循环结束'
    return f'`index = {S.index}`，`v = {S.v}`：子数组向左最多延伸 `v` 个位置'


def _start(S, B, ret):
    d = S.index - S.v
    extra = f'（`{S.index} − {S.v} = {d}` 为负，夹到 ==0==）' if d < 0 else ''
    return f'`start = max(0, {S.index} − {S.v})` = =={S.start}=={extra}'


def _if(S, B, ret):
    if S.start > 0:
        return f'`start = {S.start} > 0`：`s[{S.index}]` 里多算了 `nums[0..{S.start - 1}]`，要减掉'
    if S.index == 0:
        return '`start = 0`：整段 `nums[0..index]` 都要 → ==不减==；不判断的话 `s[start − 1]` 会变成 `s[-1]`（取到末尾）'
    return '`start = 0`：整段 `nums[0..index]` 都要，不用减'


CONFIG = dict(
    num=3427, title='变长子数组求和', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='前缀和 · 区间和 = s[右] − s[左−1]',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def subarraySum(self, nums):
        s = [nums[0]]
        for v in nums[1:]:
            s.append(s[-1] + v)

        res = 0
        for index, v in enumerate(nums):
            start = max(0, index - v)
            res += s[index]
            if start > 0:
                res -= s[start - 1]

        return res
''',
    call=f'Solution().subarraySum({NUMS})',
    expect=31,
    views=[
        dict(type='text', fn=_formula, h=64),
        dict(type='array', var='nums', label='nums（青 = 当前子数组）', cell=96, h=215, window=(ST, IDX),
             pointers={ST: 'red', IDX: 'blue', _cur1: 'blue'}, pointer_labels={ST: 'start', IDX: 'index', _cur1: 'v'},
             color=_nums_color),
        dict(type='array', var='s', label='s（s[k] = nums[0..k] 的和，没有前导 0）', cell=96, h=230, min_slots=len(NUMS),
             pointers={SM1: 'red', IDX: 'green'}, pointer_labels={SM1: 'start-1', IDX: 'index'}, color=_s_color),
    ],
    watch=['index', 'v', 'start', ('res', 'res', 'green')],
    captions={
        's = [nums[0]]': '先放 `s[0] = nums[0] = {s[0]}`：`s[k]` 是 `nums[0..k]` 的和',
        'for v in nums[1:]': _for1,
        's.append(s[-1] + v)': '`s[{len(s) - 1}] = s[{len(s) - 2}] + {v}` = =={s[-1]}==：前一个前缀和再加上 `v`',
        'res = 0': '`res` 累加每个下标对应的区间和',
        'for index, v in enumerate': _for2,
        'start = max': _start,
        'res += s[index]': '先把 `nums[0..{index}]` 的和 `s[{index}] = {s[index]}` 全加上：`res` {B.res} → {res}',
        'if start > 0': _if,
        'res -= s[start - 1]': '减去多出来的前缀 `s[{start - 1}] = {s[start - 1]}`：`res` {B.res} → =={res}==',
        'return res': '所有区间和累加完毕，返回 `{ret}`',
    },
    cards=dict(
        one_liner='先求出每个下标的 start，区间和就交给前缀和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['对每个下标 `index`，子数组是 `nums[start..index]`，`start = max(0, index − nums[index])`',
                 '求所有子数组的元素和之和',
                 '示例：`[3,1,1,2]` → `13`',
                 '本视频：`[3,1,1,2,5,1]` → `31`'],
        quote='对于每个下标index，可以先计算出对应的start，那么问题就转化成了求数组区间和的问题。于是只需先一趟遍历，预处理出数组的前缀和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s[k]` = `nums[0..k]` 的和，一趟扫描就能递推出来',
              '区间 `[start, index]` 的和 = `s[index] − s[start − 1]`',
              '`start = 0` 时前面没有前缀可减，==要特判==，否则 `s[-1]` 取到末尾'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`start = 0` 时不能减 `s[start − 1]`，Python 里 `s[-1]` 不会报错而是取到最后一个',
                 '这里的 `s` 没有垫开头的 0，所以要多一个 `if`',
                 '对比灵神：`accumulate(nums, initial=0)` 垫了 0，直接 `s[i+1] − s[start]`，免特判'],
    ),
)
