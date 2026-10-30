CONFIG = dict(
    num=908, title='最小差值 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='遍历求最大最小值',
    code='''
class Solution(object):
    def smallestRangeI(self, A, K):

        max_num = min_num = A[0]
        for num in A[1:]:
            if num > max_num:
                max_num = num
            if num < min_num:
                min_num = num
                
        return max(max_num - min_num - K - K, 0)
''',
    call='Solution().smallestRangeI([4,1,9,6,3], 2)',
    expect=4,
    views=[
        dict(type='array', var='A', h=260,
             color=lambda S, i, v: ('yellow' if v == S.get('num') and i == (S['A'].index(S['num'], 1) if S.get('num') in S['A'][1:] else -1) else None) if 'num' in S else None,
             pointers={}),
        dict(type='text', size=34, fn=lambda S: f"当前最大 ==`{S['max_num']}`==，最小 ==`{S['min_num']}`==" if 'max_num' in S else ''),
    ],
    watch=[('num', 'num', 'yellow'), ('max_num', 'max_num', 'pink'), ('min_num', 'min_num', 'blue'), 'K'],
    captions={
        'max_num = min_num': '先假设第一个数 `{A[0]}` 既是最大又是最小',
        'for num in': lambda S, B, r: ('`A[1:]` 遍历完，不再有下一个数' if B.get('num') == S['num'] else f'取下一个数 `num = {S["num"]}`'),
        'if num > max_num': '`{num} > {max_num}`？ 比当前最大值大才更新 → {"成立" if num > max_num else "不成立"}',
        'max_num = num': '最大值更新为 `{max_num}`',
        'if num < min_num': '`{num} < {min_num}`？ 比当前最小值小才更新 → {"成立" if num < min_num else "不成立"}',
        'min_num = num': '最小值更新为 `{min_num}`',
        'return max': '差 `{max_num} - {min_num} = {max_num-min_num}`，两头各缩 `K`，一共缩 `{K+K}`：`{max_num-min_num-K-K}`；不能为负 → =={ret}==',
    },
    cards=dict(
        one_liner='先算最大最小的差，再减去两头各能缩的 K',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给数组 `A` 和整数 `K`，每个数可以加上 `[-K, K]` 的任意整数（最多一次）',
                 '求操作后「最大值 − 最小值」的最小值',
                 '本视频：`A = [4,1,9,6,3], K = 2` → `4`'],
        quote='若这个差值小于等于两倍的K，那么就可以抹平这个差距，否则最多只能提供减少2K的差值。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍数组，记下 `max_num` 和 `min_num`',
              '最大的数最多降 `K`，最小的数最多升 `K`，差最多缩小 `2K`',
              '缩不动就剩 `差 − 2K`，缩过头就是 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：差小于 `2K` 时答案是 0，不是负数',
                 '原文是手写循环求最大最小，没用内置 `max/min`'],
    ),
)
