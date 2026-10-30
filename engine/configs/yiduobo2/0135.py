RATINGS = [1, 3, 4, 2, 2, 1]

CODE = '''
class Solution(object):
    def candy(self, ratings):
        if not ratings:
            return 0

        left_level = [1] * len(ratings)
        right_level = [1] * len(ratings)

        for index in range(1, len(ratings)):
            if ratings[index] > ratings[index - 1]:
                left_level[index] = left_level[index - 1] + 1

        for index in range(len(ratings) - 2, -1, -1):
            if ratings[index] > ratings[index + 1]:
                right_level[index] = right_level[index + 1] + 1

        res = 0
        for index in range(len(ratings)):
            res += max(left_level[index], right_level[index])

        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(s, k=0):
    return [i + 1 for i, t in enumerate(_LINES) if s in t][k]


L_F1, L_F2, L_F3 = _ln('for index in range(1,'), _ln('for index in range(len(ratings) - 2'), _ln('for index in range(len(ratings)):')


def _phase(S):
    line = S.get('_line', 0)
    if line >= L_F3 - 1:
        return 3
    if line >= L_F2:
        return 2
    if line >= L_F1:
        return 1
    return 0


def _cell(which):
    def f(S, i, v):
        ph = _phase(S)
        idx = S.get('index')
        if idx is None or ph == 0:
            return None
        if ph == 3 and 'res' in S and idx is not None and i == idx and S.get('_line') != L_F3 - 1:
            l, r = S['left_level'][i], S['right_level'][i]
            return 'green' if (l >= r) == (which == 'L') else None
        if (ph == 1 and which == 'L') or (ph == 2 and which == 'R'):
            if i == idx:
                return 'yellow'
            if (ph == 1 and i == idx - 1) or (ph == 2 and i == idx + 1):
                return 'purple'
        return None
    return f


def _cmp1(S, B, ret):
    i = B.index
    a, b = B.ratings[i], B.ratings[i - 1]
    if a > b:
        return f'`ratings[{i}] = {a} > ratings[{i - 1}] = {b}`：比左边高 → 要比左边多一颗'
    return f'`ratings[{i}] = {a} ≤ {b}`：不比左边高，左边的约束只要求 1 颗'


def _cmp2(S, B, ret):
    i = B.index
    a, b = B.ratings[i], B.ratings[i + 1]
    if a > b:
        return f'`ratings[{i}] = {a} > ratings[{i + 1}] = {b}`：比右边高 → 要比右边多一颗'
    return f'`ratings[{i}] = {a} ≤ {b}`：不比右边高，右边的约束只要求 1 颗'


CONFIG = dict(
    num=135, title='分发糖果', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='左右各扫一趟 · 取较大值',
    tags=['字节30天', '热题173', '面试经典150'],
    code=CODE,
    call=f'Solution().candy({RATINGS})',
    expect=10,
    skip=['if not ratings'],
    views=[
        dict(type='bars', var='ratings', label='ratings', h=270, vmax=4,
             pointers={'index': 'blue'}),
        dict(type='array', var='left_level', label='left_level（只看左边的约束）黄 = 当前，紫 = 依赖的邻居，绿 = 求和时取它', cell=84,
             color=_cell('L')),
        dict(type='array', var='right_level', label='right_level（只看右边的约束）', cell=84,
             color=_cell('R')),
        dict(type='text', fn=lambda S: (f"`res` = {' + '.join(str(max(a, b)) for a, b in zip(S['left_level'][:S['index'] + 1], S['right_level'][:S['index'] + 1]))} = =={S['res']}=="
                                        if _phase(S) == 3 and 'res' in S and S.get('_line') not in (L_F3 - 1, L_F3) else
                                        ('`res` 逐个累加 `max(left_level[i], right_level[i])`' if _phase(S) == 3 else '')), h=60),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'left_level = [1]': '先假设每人拿 1 颗：`left_level` 记录==与左侧比较==所需的最少糖果',
        'right_level = [1]': '`right_level` 记录==与右侧比较==所需的最少糖果',
        'for index in range(1,': lambda S, B, r: (f'从左往右扫：看 `index = {S.index}` 和它左边' if S.index != B.get('index') or 'index' not in B
                                                  else '左边的约束算完了'),
        'if ratings[index] > ratings[index - 1]': _cmp1,
        'left_level[index] = left_level[index - 1] + 1': '`left_level[{index}] = {left_level[index - 1]} + 1 = {left_level[index]}`',
        'for index in range(len(ratings) - 2': lambda S, B, r: (f'从右往左扫：看 `index = {S.index}` 和它右边' if S.index != B.index
                                                                else '右边的约束也算完了'),
        'if ratings[index] > ratings[index + 1]': _cmp2,
        'right_level[index] = right_level[index + 1] + 1': '`right_level[{index}] = {right_level[index + 1]} + 1 = {right_level[index]}`',
        'res = 0': '两边的约束都要满足 → 每人取==较大值==，再求和',
        'for index in range(len(ratings)):': lambda S, B, r: (f'第 `{S.index}` 个小朋友' if S.index != B.index or S.index == 0 else '求和完毕'),
        'res += max(': '`max({left_level[index]}, {right_level[index]}) = {max(left_level[index], right_level[index])}`，`res` → {res}',
        'return res': '最少需要 =={ret}== 颗糖果',
    },
    cards=dict(
        one_liner='左右两个约束分开算：从左扫一趟、从右扫一趟，每人取较大值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个孩子站成一排，`ratings[i]` 是评分',
                 '每人==至少 1 颗==糖果；相邻两人中评分==更高==的糖果更多，求最少总数',
                 '示例：`[1,0,2]` → `5`（分 2,1,2）；`[1,2,2]` → `4`（分 1,2,1）',
                 '本视频：`[1,3,4,2,2,1]` → `10`'],
        quote='先假设每个小朋友拿了一颗糖果，==从左往右扫描一趟==……然后再==从右往左扫描一趟==，计算出与右侧小朋友比较所需的最少糖果数，最后==取其中的较大值==作为最终拿到的糖果数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['评分高于左边 → 比左边多；高于右边 → 比右边多：两个约束互不干扰',
              '左扫：`left_level[i] = left_level[i-1] + 1`；右扫同理',
              '同时满足两个约束且最少：取 `max(left_level[i], right_level[i])`'],
        summary=['时间 `O(n)`，空间 `O(n)`（两个数组）',
                 '右扫要==倒序==：`right_level[i]` 依赖已经算好的 `right_level[i+1]`',
                 '评分相等时没有约束，糖果可以更少（如示例 `[1,2,2]` 第三人只拿 1 颗）',
                 '对比灵神：分组循环一次遍历、`O(1)` 空间，但需要处理谷底共享',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
