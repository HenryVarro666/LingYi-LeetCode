def _partner(S):
    if 'target' not in S or 'v' not in S:
        return None
    return S['pos'].get(S['target'] - S['v'])


def _cond(S):
    v, t, pos, res, nums = S.v, S.target, S.pos, S.res, S.nums
    w = t - v
    if w not in pos:
        return f'搭档 `{w}` 还没出现过 → 条件不成立，跳过'
    if v == w:
        return f'`{v} = {w}`：两数相等，不满足 `nums[i] > nums[j]` → 跳过'
    if res[0] == -1:
        return f'搭档 `{w}` 在 `pos` 里，`{v} ≠ {w}`，还没有答案 → ==成立，更新=='
    cur = nums[res[0]] * nums[res[1]]
    if cur < v * w:
        return f'乘积 `{v} × {w} = {v * w}` 比当前最优 `{cur}` 大 → ==成立，更新=='
    return f'乘积 `{v} × {w} = {v * w}` 不比当前最优 `{cur}` 大 → 不更新'


def _cell(S, i, v):
    r = S.get('res')
    if r and r[0] != -1 and i in r:
        return 'green'
    return None


def _txt(S):
    nums, res = S['nums'], S['res']
    if res[0] == -1:
        return '目前答案 `[-1, -1]`：还没有有效二元组'
    a, b = nums[res[0]], nums[res[1]]
    return f'目前最优 `res = {res}`：`{a} + {b} = {S["target"]}`，乘积 ==`{a} × {b} = {a * b}`=='


CONFIG = dict(
    num=4074, title='和为目标值的最大乘积对', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 一趟遍历',
    tags=[],
    code='''
class Solution(object):
    def maxProductPair(self, nums, target):
        
        pos = {}
        res = [-1, -1]
        for index, v in enumerate(nums):
            if (target - v) in pos and v != target - v and (res[0] == -1 or nums[res[0]] * nums[res[1]] < v * (target - v)):
                if v > target - v:
                    res = [index, pos[target - v]]
                else:
                    res = [pos[target - v], index]
            
            pos[v] = index
        
        return res
''',
    call='Solution().maxProductPair([2, 3, 6, 5, 4, 4, 7, 1], 8)',
    expect=[3, 1],
    views=[
        dict(type='array', var='nums', label='nums（绿 = 当前最优二元组的下标）', cell=90, h=200,
             pointers={'index': 'blue', 'pos[target - v]': 'pink'}, color=_cell),
        dict(type='map', var='pos', label='pos（值 → 最近出现的下标）', fmt=lambda k, v: f'{k} → {v}', h=170, font=30),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=['index', 'v', ('target - v', 'target - v', 'pink'), ('res', 'res', 'green')],
    skip=['pos = {}', 'res = [-1, -1]'],
    captions={
        'for index, v in enumerate': lambda S, B, r: ('遍历结束' if 'index' in B and B.index == S.index and 'pos' in B and S.v in B.pos and B.pos[S.v] == S.index
                                                      else f'看 `nums[{S.index}] = {S.v}`，需要的搭档是 `{S.target} − {S.v} = {S.target - S.v}`'),
        'if (target - v) in pos': lambda S, B, r: _cond(S),
        'if v > target - v': '`{v}` 和 `{target - v}` 谁大谁当 `i`：`{v} > {target - v}`？ → {"是，当前下标做 i" if v > target - v else "否，旧下标做 i"}',
        'res = [index, pos': '当前较大 → `i = index`，`j = pos[{target - v}]`：`res = {res}`',
        'res = [pos': '搭档较大 → `i = pos[{target - v}]`，`j = index`：`res = {res}`',
        'pos[v] = index': '把 `{v}` 的位置记下：`pos[{v}] = {index}`',
        'return res': '遍历完，返回乘积最大的有效二元组 `{res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='哈希表记位置，边扫边找“和为 target”的搭档',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找下标对 `(i, j)`，满足 `nums[i] + nums[j] = target` 且 `nums[i] > nums[j]`',
                 '返回乘积最大的一对，没有就返回 `[-1, -1]`',
                 '本视频：`nums = [2,3,6,5,4,4,7,1]`，`target = 8` → `[3, 1]`（`5 × 3 = 15`）'],
        quote='nums[i] > nums[j]这一条实际上可以理解成只要这两个元素不相等就行了，这样一来就一定有一个较小另一个较大，此时让较大的这一方作为nums[i]就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['“> ” 等价于“两数不相等”：相等的一对直接排除',
              '用 `pos` 记录前缀里每个值的位置，扫到 `v` 就查 `target − v`',
              '找到就比乘积，更大才更新；较大的数的下标放前面当 `i`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`v == target − v` 必须排除（如 `4 + 4`）',
                 '易错：下标顺序由数值大小决定，不是出现先后',
                 '`pos[v]` 在判断之后才写入，同值出现多次时保留最近的位置',
                 '原文为 Python 2 风格的类，逻辑可直接在 Python 3 运行，代码未改动'],
    ),
)
