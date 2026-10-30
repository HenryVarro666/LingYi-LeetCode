NUMS = [2, -5, 1, -4, 3, -2]


def _k(S):
    """当前枚举到的下标（NUMS 元素互不相同，用 index 反查）"""
    if 'num' not in S:
        return None
    return S['nums'].index(S['num'])


def _starts(nums, up):
    """st[i]：处理完前 i 个数后，当前子数组的起点（归零后起点跳到下一个位置）。up=True 对应 ma，False 对应 mi"""
    st, cur, start = [0], 0, 0
    for i, v in enumerate(nums):
        cur += v
        if (cur < 0) if up else (cur > 0):
            cur, start = 0, i + 1
        st.append(start)
    return st


def _win(S, up):
    k = _k(S)
    if k is None:
        return None
    st = _starts(S['nums'], up)
    ln = S['_line']
    upd, rst = (7, 9) if up else (10, 12)  # 该变量 += num 的行，以及归零之后的第一行
    if ln < upd:
        return (st[k], k - 1)
    if ln < rst:
        return (st[k], k)
    return (st[k + 1], k)


def _wma(S):
    w = _win(S, True)
    return None if w is None else w[0]


def _wma_end(S):
    w = _win(S, True)
    return None if w is None else w[1]


def _wmi(S):
    w = _win(S, False)
    return None if w is None else w[0]


def _wmi_end(S):
    w = _win(S, False)
    return None if w is None else w[1]


def _text(S, B):
    k = _k(S)
    if k is None:
        return '`ma` / `mi`：以当前位置==结束==的子数组和的最大值 / 最小值，小于 0 的就清零'
    ln = S['_line']
    if ln in (7, 8, 9):
        return f'当前位置 `{S["num"]}`：蓝框 = 以它结束、和为 `ma = {S["ma"]}` 的子数组'
    if ln in (10, 11, 12):
        return f'当前位置 `{S["num"]}`：粉框 = 以它结束、和为 `mi = {S["mi"]}` 的子数组'
    return f'`ma = {S["ma"]}`，`mi = {S["mi"]}` → 候选 `ma = {S["ma"]}` 和 `-mi = {-S["mi"]}`'


CONFIG = dict(
    num=1749, title='任意子数组和的绝对值的最大值', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='贪心 · 同时维护最大 / 最小结尾和',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1542'],
    code='''
class Solution(object):
    def maxAbsoluteSum(self, nums):

        ma = mi = 0
        res = 0
        for num in nums:
            ma += num
            if ma < 0:
                ma = 0
            mi += num
            if mi > 0:
                mi = 0
            
            res = max(res, ma, -mi)
        
        return res
''',
    call=f'Solution().maxAbsoluteSum({NUMS})',
    expect=8,
    views=[
        dict(type='text', fn=_text, h=70, size=26),
        dict(type='array', var='nums', label='nums：蓝框 = ma 对应的子数组（和 ≥ 0 才保留）', cell=96,
             window=(_wma, _wma_end), window_color='blue',
             pointers={'nums.index(num)': 'yellow'}, pointer_labels={'nums.index(num)': 'num'},
             color=lambda S, i, v: 'yellow' if i == _k(S) else None, h=200),
        dict(type='array', var='nums', label='nums：粉框 = mi 对应的子数组（和 ≤ 0 才保留）', cell=96,
             window=(_wmi, _wmi_end), window_color='pink',
             color=lambda S, i, v: 'yellow' if i == _k(S) else None, h=170),
    ],
    watch=[('num', 'num', 'yellow'), ('ma', 'ma', 'blue'), ('mi', 'mi', 'pink'), ('res', 'res', 'green')],
    captions={
        'ma = mi = 0': '`ma`：以当前位置结束的子数组和的==最大值==；`mi`：==最小值==。都从 0 开始',
        'res = 0': '`res` 存答案；子数组可以为空，所以从 `0` 起步',
        'for num in nums': lambda S, B, r: ('`nums` 扫描完了，退出循环' if B.get('num') == S.num and 'num' in B
                                            else f'一趟扫描，当前位置 `num = {S.num}`'),
        'ma += num': '`ma` 加上 `{num}` → {ma}：把它接到前一个子数组后面',
        'if ma < 0': lambda S, B, r: (f'`ma = {S.ma} < 0`：接上去反而拖后腿 → ==要清零==' if S.ma < 0
                                      else f'`ma = {S.ma} ≥ 0`：还有用，保留'),
        'ma = 0': '`ma` 清零：前面的和是负的，==从下一个位置重新开始==',
        'mi += num': '`mi` 加上 `{num}` → {mi}：把它接到前一个子数组后面',
        'if mi > 0': lambda S, B, r: (f'`mi = {S.mi} > 0`：越加越大，不可能是最小 → ==要清零==' if S.mi > 0
                                      else f'`mi = {S.mi} ≤ 0`：还有用，保留'),
        'mi = 0': '`mi` 清零：前面的和是正的，==从下一个位置重新开始==',
        'res = max': lambda S, B, r: (f'`res = max({B.res}, ma={S.ma}, -mi={-S.mi}) = {S.res}`：'
                                      + ('负的那边 `-mi` 更大 → ==用 -mi 更新答案==' if -S.mi > S.ma and -S.mi > B.res
                                         else '`ma` 更大 → ==用 ma 更新答案==' if S.ma > B.res
                                         else '没有超过旧答案，保持不变')),
        'return res': '扫描完，`res = {res}` 就是和的绝对值的最大值',
    },
    cards=dict(
        one_liner='和为正 / 为负分开贪心：ma 最大、mi 最小，清零后重新开始',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 是整数数组，求==和的绝对值==最大的子数组（可以为空）',
                 '返回这个最大的绝对值',
                 '示例：`[2,-5,1,-4,3,-2]` → `8`（`[-5,1,-4]`）'],
        quote='子数组和的绝对值最大可以分为子数组和为正数以及子数组和为负数这两种情况。对于第一种情况，就是常规的最大子段和，可以使用贪心法来做。',
        quote_src='—— yiduobo 题解原文',
        idea=['和为正：常规最大子段和 → `ma` 累加，一旦 `< 0` 就清零重来',
              '和为负：同样的贪心，只是把最大换成最小 → `mi`，一旦 `> 0` 就清零',
              '每个位置得到 `ma` 和 `mi` 后，用 `ma` 和 `-mi` 更新答案'],
        result='`ma` 最大到 `3`，`mi` 最小到 `-8` → 答案 `max(3, 8) = 8` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '清零的条件：`ma < 0` 才清零（等于 0 不用），`mi > 0` 才清零',
                 '更新答案要用 `-mi`，不是 `mi`（`mi` 是负数）',
                 '原文是 Python 2 风格写法，但在 Python 3 下可直接运行，代码未做改动',
                 '对比灵神：灵神写成 `f = max(f, 0) + x`，先清零再累加；这里先累加再判断清零'],
    ),
)
