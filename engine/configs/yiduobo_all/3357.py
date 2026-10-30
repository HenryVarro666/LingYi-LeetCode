def _col(S, i, v):
    if v == -1:
        return 'orange'
    if 'p' in S and 'q' in S and S.get('_line', 0) >= 33 and i in (S['p'] - 1, S['q']):
        return 'cyan'
    return None


def _txt(S):
    if 'mid' not in S:
        if 'ma' in S and S['ma'] is not None and 'mi' in S and S['mi'] is not None:
            return f"空位邻居的最大值 ma = =={S['ma']}==，最小值 mi = =={S['mi']}==；二分范围 `[{S['left']}, {S['right']}]`" if 'right' in S else ''
        return ''
    return f"二分 [{S['left']}, {S['right']}]　mid = =={S['mid']}==　x = `{S['x']}`　y = `{S['y']}`"


def _fail(S, k):
    """四种填法是否不合法（k=1 全x, 2 全y, 3 前x后y, 4 前y后x）；单个空位只看 1、2"""
    nums, p, q, n, mid, x, y = S['nums'], S['p'], S['q'], S['n'], S['mid'], S['x'], S['y']
    a = lambda z: (p > 0 and abs(z - nums[p - 1]) > mid)
    b = lambda z: (q < n and abs(z - nums[q]) > mid)
    return {1: a(x) or b(x), 2: a(y) or b(y), 3: a(x) or b(y) or abs(x - y) > mid, 4: a(y) or b(x) or abs(x - y) > mid}[k]


def _plan(S, k, name):
    f = _fail(S, k)
    return f'方案：{name} → ' + ('==不合法==' if f else '==合法==，这一段可以填')


CONFIG = dict(
    num=3357, title='最小化相邻元素的最大差值', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='二分答案 + 构造检验',
    tags=['贪心与思维', '难度分 3077'],
    code='''
class Solution(object):
    def minDifference(self, nums):
        
        n = len(nums)
        ma = None
        mi = None
        left = 0
        right = 0

        for index, v in enumerate(nums):
            if v == -1:
                if index > 0 and nums[index - 1] != -1:
                    if ma is None or ma < nums[index - 1]:
                        ma = nums[index - 1]
                    if mi is None or mi > nums[index - 1]:
                        mi = nums[index - 1]
                if index + 1 < n and nums[index + 1] != -1:
                    if ma is None or ma < nums[index + 1]:
                        ma = nums[index + 1]
                    if mi is None or mi > nums[index + 1]:
                        mi = nums[index + 1]
            else:
                if index > 0 and nums[index - 1] != -1:
                    left = max(left, abs(nums[index] - nums[index - 1]))
                if index + 1 < n and nums[index + 1] != -1:
                    left = max(left, abs(nums[index] - nums[index + 1]))
        
        if ma is not None:
            right = ma - mi
            while left < right:
                mid = (left + right) // 2
                x = mi + mid
                y = ma - mid
                flag = True

                p = 0
                while p < n:
                    while p < n and nums[p] != -1:
                        p += 1
                    
                    if p == n:
                        break
                    
                    q = p + 1
                    while q < n and nums[q] == -1:
                        q += 1
                    
                    if p + 1 == q:
                        if ((p > 0 and abs(x - nums[p - 1]) > mid) or (q < n and abs(x - nums[q]) > mid)) and \\
                            ((p > 0 and abs(y - nums[p - 1]) > mid) or (q < n and abs(y - nums[q]) > mid)):
                            flag = False
                            break
                    else:
                        if ((p > 0 and abs(x - nums[p - 1]) > mid) or (q < n and abs(x - nums[q]) > mid)) and \\
                            ((p > 0 and abs(y - nums[p - 1]) > mid) or (q < n and abs(y - nums[q]) > mid)) and \\
                            ((p > 0 and abs(x - nums[p - 1]) > mid) or (q < n and abs(y - nums[q]) > mid) or abs(x - y) > mid) and \\
                            ((p > 0 and abs(y - nums[p - 1]) > mid) or (q < n and abs(x - nums[q]) > mid) or abs(x - y) > mid):
                            flag = False
                            break

                    p = q + 1

                if flag:
                    right = mid
                else:
                    left = mid + 1
        
        return left
''',
    call='Solution().minDifference([1,-1,-1,10,8])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='array', var='nums', label='nums（橙色 = 空位 -1，青色 = 当前空位段两侧的数）', pointers={'p': 'blue', 'q': 'pink'}, color=_col, h=230),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', 'x', 'y', 'flag'],
    max_steps=100,
    skip=['if ma is None', 'if mi is None', 'ma = nums', 'mi = nums', 'index > 0 and nums[index - 1] != -1:', 'index + 1 < n and nums[index + 1] != -1:',
          'while p < n and', 'while q < n', 'p += 1', 'q += 1', 'if p == n', 'q = p + 1', 'p = 0', 'flag = True', 'p = q + 1', 'if v == -1', 'break', 'while p < n:', 'left = max('],
    captions={
        'ma = None': '`ma`、`mi`：和空位相邻的最大、最小数；`left` 是二分下界',
        'right = 0': '`right` 先占位，稍后设为 `ma - mi`',
        'for index, v': '{"扫描完毕" if B.get("index") == index else "扫描 `nums[" + str(index) + "] = " + str(v) + "`：找空位的邻居，并更新下界 left"}',
        'right = ma - mi': '`ma = {ma}`，`mi = {mi}`，上界 `right = ma - mi` = =={right}==（下界 left = {left}：已有的相邻数字最大差）',
        'if ma is not None': '{"有空位邻居，开始二分" if ma is not None else "没有空位邻居，直接返回 left"}',
        'while left < right': '`left = {left}`，`right = {right}`：{"答案还在 [left, right] 里，继续二分" if left < right else "区间收拢，答案就是 left"}',
        'mid = (left': '试探最大差值 `mid = ({B.left} + {B.right}) // 2` = =={mid}==',
        'x = mi + mid': '`x = mi + mid = {mi} + {mid}` = =={x}==：尽量贴近最小的邻居',
        'y = ma - mid': '`y = ma - mid = {ma} - {mid}` = =={y}==：尽量贴近最大的邻居',
        'q = p + 1': '找到空位段 `[{p}, {q})`',
        'if p + 1 == q': '{"单个空位" if p + 1 == q else "连续 " + str(q - p) + " 个空位"}：`p = {p}`，`q = {q}`',
        49: lambda S, B, r: _plan(S, 1, '全部填 x'),
        50: lambda S, B, r: _plan(S, 2, '全部填 y'),
        54: lambda S, B, r: _plan(S, 1, '全部填 x'),
        55: lambda S, B, r: _plan(S, 2, '全部填 y'),
        56: lambda S, B, r: _plan(S, 3, '前半段 x、后半段 y（还要 |x−y| ≤ mid）'),
        57: lambda S, B, r: _plan(S, 4, '前半段 y、后半段 x（还要 |x−y| ≤ mid）'),
        58: '四种填法都不合法 → mid 太小，`flag = False`',
        'if flag': '{"这一轮每段空位都能填 → mid 可行" if flag else "有一段填不了 → mid 太小"}',
        'right = mid': '`mid = {mid}` 可行，答案可能更小：`right = {right}`',
        'left = mid + 1': '`mid = {B.mid}` 不可行，答案更大：`left = {left}`',
        'return left': '二分结束，最小的最大差值 `{left}`',
    },
    cards=dict(
        one_liner='二分最大差值 mid：x、y 取在 mi+mid 和 ma−mid',
        complexity='时间 `O(n log C)`，空间 `O(1)`',
        problem=['`nums` 里 `-1` 是空位，选一对正整数 `(x, y)`，每个空位填 `x` 或 `y`',
                 '要让相邻元素绝对差的最大值最小，求这个最小值',
                 '示例：`[1,2,-1,10,8]` → `4`；本视频：`[1,-1,-1,10,8]` → `3`'],
        quote='对于这类使得最大值最小的问题，一种场景的处理方法就是二分答案。具体来说，就是二分这个最大差值，然后检测能否得到一种可行的构造方案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`ma`、`mi` 是和空位相邻的最大、最小数；二分差值 `mid` 时，令 `x = mi + mid`，`y = ma - mid`',
              '下界 `left`：相邻两个非空数的最大差；上界 `right = ma - mi`',
              '检验：单个空位看填 x 或 y 是否合法；连续空位有四种填法（全 x、全 y、前 x 后 y、前 y 后 x），至少一种合法即可'],
        summary=['时间 `O(n log C)`，空间 `O(1)`',
                 '单个空位：`x`、`y` 两者都不合法才失败',
                 '连续空位：四种填法都不合法才失败，混填时还要检查 `abs(x - y) > mid`',
                 '没有任何空位邻居（`ma is None`）时直接返回 `left`',
                 '原文为 Python 2 写法，只删去了类型说明，逻辑未改'],
    ),
)
