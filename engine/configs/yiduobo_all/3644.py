def _txt(S):
    if 'res' not in S:
        return ''
    if 'v' not in S:
        return '`res = None`：还没有遇到错位元素'
    r = S['res']
    return f'`res` = {"None" if r is None else format(r, "04b")}（已 AND 过的错位元素）'


CONFIG = dict(
    num=3644, title='排序排列', difficulty='Medium', category='位运算',
    author='yiduobo', technique='错位元素按位与',
    tags=['位运算', '思维题', '难度分 1775'],
    code='''
class Solution(object):
    def sortPermutation(self, nums):
        
        res = None

        for index, v in enumerate(nums):
            if index != v:
                if res is None:
                    res = v
                else:
                    res &= v
        
        if res is None:
            return 0
        return res
''',
    call='Solution().sortPermutation([0,5,2,3,4,1,6,7])',
    expect=1,
    views=[
        dict(type='text', fn=_txt, size=30, h=60),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=170,
             color=lambda S, i, v: ('red' if i != v else 'green') if 'res' in S else None),
        dict(type='text', fn=lambda S: ('绿 = 已在正确位置，不要动；红 = 不在位置，要参与按位与' if 'res' in S else ''), size=26, h=60),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    captions={
        'res = None': '`res = None`：用 None 表示还没有错位元素',
        'if index != v': lambda S, B, r: (f'`{S.index} != {S.v}`：不在正确位置，需要交换，二进制必须包含 k' if S.index != S.v
                                          else f'`{S.index} == {S.v}`：在正确位置，不要动它'),
        'if res is None': lambda S, B, r: ('`res` 还是 None：这是第一个错位元素' if S.res is None else '`res` 已有值：继续按位与'),
        'res = v': '第一个错位元素：`res = {v}`',
        'res &= v': '`res &= {v}` → `{res}`：k 的二进制位必须同时在这些数里',
        'if res is None:': lambda S, B, r: ('一个错位元素都没有：数组本来有序' if S.res is None else '有错位元素，答案是它们的按位与'),
        'return 0': '已经有序，返回 `0`',
        'return res': '错位元素的按位与就是上限，也一定能取到：返回 ==`{res}`==',
    },
    cards=dict(
        one_liner='不在位置上的数，按位与就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['排列 `nums`，满足 `nums[i] AND nums[j] = k` 才能交换',
                 '求使数组变为递增的最大 `k`；已有序则返回 0',
                 '本视频：`[0,5,2,3,4,1,6,7]` → `1`'],
        quote='这些不在正确位置上的元素的按位与结果就是答案的上限。',
        quote_src='—— yiduobo 题解原文',
        idea=['交换规则只看元素值：==在正确位置的元素不该动==（除非它就是 k）',
              '要交换的元素二进制里都得含 k，所以 AND 结果是上限',
              'AND 越来越小，必在 `0..n-1`，取它作 k 就能完成所有交换'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '用 `None` 区分「没有错位元素」，此时返回 0',
                 '和灵神的区别：灵神用 -1 全 1 当初始值，这里用 None 判断首个元素',
                 '易错：不要把已在原位的元素也 AND 进去'],
    ),
)
