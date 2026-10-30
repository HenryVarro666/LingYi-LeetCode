def _suf(S):
    """当前后缀长度（index），未进入第二个循环时为 0"""
    return S['index'] if 'index' in S else 0


def _card_color(S, i, v):
    if 'res' not in S:
        return None
    k, n = S['k'], len(S['cardPoints'])
    t = _suf(S)
    if i < k - t:
        return 'blue'
    if i >= n - t:
        return 'green'
    return None


def _card_dim(S, i, v):
    if 'res' not in S:
        return False
    return _card_color(S, i, v) is None


def _pre_ptr(S):
    if 'res' not in S:
        return None
    return len(S['left']) - _suf(S) - 1


def _txt(S):
    if 'res' not in S:
        return '先求前 k 个数的前缀和 `left[j]` = 前 j 张的和'
    t = _suf(S)
    p = S['k'] - t
    return (f"前 =={p}== 张 `left[{p}] = {S['left'][p]}` + 后 =={t}== 张 `right = {S['right']}` "
            f"= `{S['left'][p] + S['right']}`")


CONFIG = dict(
    num=1423, title='可获得的最大点数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='前缀和 + 从后往前扫后缀',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1574'],
    code='''
class Solution(object):
    def maxScore(self, cardPoints, k):

        left = [0]
        for point in cardPoints[:k]:
            left.append(left[-1] + point)

        res = left[-1]
        right = 0
        for index in range(1, k + 1):
            right += cardPoints[-index]
            res = max(res, right + left[-index - 1])

        return res
''',
    call='Solution().maxScore([5,2,1,7,3,1,6], 3)',
    expect=13,
    views=[
        dict(type='array', var='cardPoints', label='cardPoints（蓝 = 取的前缀，绿 = 取的后缀）', h=230, cell=100,
             color=_card_color, dim=_card_dim),
        dict(type='array', var='left', label='left：前缀和（left[j] = 前 j 张之和）', h=230, cell=100,
             pointers={_pre_ptr: 'blue'}, pointer_labels={_pre_ptr: '前缀长度'}),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('index', 'index', 'green'), ('right', 'right', 'green'), ('res', 'res', 'orange')],
    captions={
        'left = [0]': '`left[0] = 0`：取 0 张前缀，和为 0',
        'for point in cardPoints[:k]': lambda S, B, ret: ('前 k 张的前缀和算完了' if len(S.left) == S.k + 1
                                                          else f'只需要前 `k = {S.k}` 张的前缀和：取 `point = {S.point}`'),
        'left.append': '`left` 末尾加入 `{left[-2]} + {point}` = `{left[-1]}`',
        'res = left[-1]': '后缀长度为 0：==全拿前 {k} 张==，`res = {res}`（别漏了这种情况）',
        'right = 0': '`right`：当前后缀的和，从 0 开始',
        'for index in range': lambda S, B, ret: (f'后缀长度 `index = {S.index}`，对应前缀长度 `{S.k} − {S.index} = {S.k - S.index}`'
                                                if 'index' not in B or S.index != B.index else '前后缀的所有组合都试过了'),
        'right += cardPoints[-index]': '后缀多拿一张 `cardPoints[-{index}] = {cardPoints[-index]}` → `right = {right}`',
        'res = max': lambda S, B, ret: (f'`{S.right} + left[{S.k - S.index}]` = `{S.right + S.left[-S.index - 1]}` > `{B.res}`：更新 `res = {S.res}`'
                                        if S.res > B.res else
                                        f'`{S.right} + left[{S.k - S.index}]` = `{S.right + S.left[-S.index - 1]}` ≤ `{B.res}`：不更新'),
        'return res': '最大点数 =={res}==',
    },
    cards=dict(
        one_liner='拿到的一定是一段前缀 + 一段后缀，长度加起来是 k',
        complexity='时间 `O(k)`，空间 `O(k)`',
        problem=['每次从 `cardPoints` 的==开头或末尾==拿一张，恰好拿 `k` 张',
                 '求拿到的点数和的最大值',
                 '本视频：`[5,2,1,7,3,1,6], k = 3` → `13`（前 2 张 + 最后 1 张）'],
        quote='如果每一步都只能从当前剩下数字的两端来取，那么最后拿到的答案必然是==一个前缀与一个后缀==。',
        quote_src='—— yiduobo 题解原文',
        idea=['预处理前 k 个数的前缀和 `left`',
              '从后往前扫：后缀长度为 `index`，前缀长度就是 `k − index`',
              '`left[-index - 1]` 正好是前 `k − index` 张的和'],
        summary=['时间 `O(k)`，空间 `O(k)`',
                 '易错：==后缀长度为 0== 的情况，用 `res = left[-1]` 初始化',
                 '`left` 长度是 `k + 1`，所以 `left[-index - 1] = left[k - index]`',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神反过来求中间剩下 `n − k` 张的最小和'],
    ),
)
