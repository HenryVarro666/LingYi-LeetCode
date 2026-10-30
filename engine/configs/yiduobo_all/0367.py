def _txt(S):
    if 'mid' not in S or '_line' not in S:
        return f"在 `1 … {S['num']}` 里二分查找平方根，不用 sqrt"
    if S.get('_line', 0) >= 8 and S.get('tmp') is not None:
        t, n = S['tmp'], S['num']
        rel = '==相等==' if t == n else ('太大' if t > n else '太小')
        return f"`mid² = {S['mid']}² = {t}` 对比 `num = {n}` → {rel}"
    return f"`mid = ({S['left']} + {S['right']}) // 2 = {S['mid']}`"


CONFIG = dict(
    num=367, title='有效的完全平方数', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='二分查找平方根',
    tags=[],
    code='''
class Solution(object):
    def isPerfectSquare(self, num):

        left = 1
        right = num
        while left <= right:
            mid = (left + right) // 2
            tmp = mid * mid
            if tmp == num:
                return True
            elif tmp > num:
                right = mid - 1
            else:
                left = mid + 1

        return False
''',
    call='Solution().isPerfectSquare(10)',
    expect=False,
    views=[
        dict(type='text', fn=_txt, size=30),
        dict(type='array', var='list(range(num + 1))', label='候选的 mid（下标 = 数值，0 不用）',
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}, window=('left', 'right'), h=260,
             dim=lambda S, i, v: i == 0 or ('right' in S and not (S['left'] <= i <= S['right']))),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), 'tmp'],
    captions={
        'left = 1': '二分的范围是 `1 … num`：平方根一定落在这里面',
        'right = num': '`right = num = {right}`，`left` 和 `right` 夹住答案的可能区间',
        'while left <= right': lambda S, B, r: (f'`left = {S.left} <= right = {S.right}`：区间还有数，继续' if S.left <= S.right
                                              else f'`left = {S.left} > right = {S.right}`：区间空了，没找到'),
        'mid = (': '取中点 `mid = ({left} + {right}) // 2 = {mid}`，==mid = {mid}==',
        'tmp = mid': '`tmp = mid * mid = {mid} × {mid} = {tmp}`，拿它和 `num = {num}` 比',
        'if tmp == num': lambda S, B, r: (f'`{S.tmp} == {S.num}`：平方正好等于 num → 它是完全平方数' if S.tmp == S.num
                                          else f'`{S.tmp} == {S.num}` 不成立 → 再看大了还是小了'),
        'elif tmp > num': lambda S, B, r: (f'`{S.tmp} > {S.num}`：==mid 太大==，答案只可能在左边 → 收缩右端' if S.tmp > S.num
                                            else f'`{S.tmp} > {S.num}` 不成立：==mid 太小== → 收缩左端'),
        'right = mid - 1': 'mid 自己已经不行了，`right = mid - 1 = {right}`',
        'left = mid + 1': '`{mid}² = {tmp} < {num}`：==mid 太小==，`left = mid + 1 = {left}`',
        'return True': '找到整数 `mid`，`mid * mid == num` → ==True==',
        'return False': '区间用完，没有整数的平方等于 `num` → ==False==',
    },
    cards=dict(
        one_liner='不用 sqrt：在 1 到 num 之间二分找平方根',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['给定正整数 `num`，判断它是不是完全平方数，==不能使用 sqrt== 之类的库函数',
                 '示例：`16` → `True`；`14` → `False`',
                 '本视频：`num = 10` → `False`'],
        quote='题目要求不能使用sqrt，因此在这里使用二分或者筛法做因式分解都是可以的。我在这里用的是二分法',
        quote_src='—— yiduobo 题解原文',
        idea=['`mid * mid` 与 `num` 比大小，太大就收右边，太小就收左边',
              '平方随 `mid` 单调递增，所以可以二分',
              '找到相等的就返回 `True`，区间空了返回 `False`'],
        summary=['时间 `O(log num)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '`while left <= right`：区间只剩一个数时也要检查',
                 '作者还提到另一种思路：筛法做因式分解'],
    ),
)
