def _txt(S):
    if 'cnt' not in S:
        return '被 3 整除的偶数 = 被 6 整除的数'
    if S['cnt'] == 0:
        return '还没找到 6 的倍数：`s = 0`，`cnt = 0`'
    return f"已找到 {S['cnt']} 个，总和 `s` = =={S['s']}=="


def _col(S, i, v):
    if 'num' not in S:
        return None
    cur = S['nums'].index(S['num'])
    if i == cur and S['_line'] < 8:
        return 'blue'
    if v % 6 == 0 and (i < cur or (i == cur and S['_line'] >= 8)):
        return 'green'
    return 'blue' if i == cur else None


CONFIG = dict(
    num=2455, title='可被三整除的偶数的平均值', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='被 6 整除 · 一趟遍历求平均',
    tags=[],
    code='''
class Solution(object):
    def averageValue(self, nums):

        s = 0
        cnt = 0
        for num in nums:
            if num % 6 == 0:
                s += num
                cnt += 1
        
        if cnt == 0:
            return 0
        else:
            return s // cnt
''',
    call='Solution().averageValue([2,6,9,12,18,5])',
    expect=12,
    views=[
        dict(type='text', fn=_txt, size=30, h=100),
        dict(type='array', var='nums', label='nums（蓝 = 当前 num，绿 = 被 6 整除）', cell=110, h=200, color=_col),
    ],
    watch=[('num', 'num', 'blue'), ('s', 's', 'green'), ('cnt', 'cnt', 'orange')],
    captions={
        's = 0': '`s` 保存满足条件的数之和',
        'cnt = 0': '`cnt` 保存满足条件的数的个数',
        'for num in nums': lambda S, B, r: ('遍历结束' if S.num == B.get('num') and S.num == S.nums[-1] else f'取下一个数 `num = {S.num}`'),
        'if num % 6 == 0': lambda S, B, r: (f'`{S.num} % 6 = 0` → 被 6 整除，==既是偶数又被 3 整除==' if S.num % 6 == 0
                                             else f'`{S.num} % 6 = {S.num % 6} ≠ 0` → 不满足，跳过'),
        's += num': '`s` 加上 `{num}` → `{s}`',
        'cnt += 1': '`cnt` → `{cnt}`',
        'if cnt == 0': lambda S, B, r: ('`cnt = 0`：一个都没有，不能做除法' if S.cnt == 0 else f'`cnt = {S.cnt}`，不为 0，可以求平均'),
        'return s // cnt': '平均值 `{s} // {cnt}` = =={s // cnt}==',
        'return 0': '没有满足条件的数，返回 `0`',
    },
    cards=dict(
        one_liner='被 3 整除的偶数就是被 6 整除的数，一趟遍历求平均',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `nums` 中能被 3 整除的偶数的平均值，向下取整',
                 '不存在这样的数返回 `0`',
                 '本视频：`[2,6,9,12,18,5]` → 满足的是 `6,12,18` → `36 // 3 = 12`'],
        quote='可以被三整除的偶数，也就是可以被6整除的数。那么只需一趟遍历，找出所有能被6整除的数并求出这些数的平均值即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把条件化简：==偶数 且 被 3 整除 = 被 6 整除==',
              '一趟遍历，分别累计总和 `s` 和个数 `cnt`',
              '最后先判 `cnt == 0`，再用 `s // cnt` 求平均'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`s / cnt` 是整数除法，已改为 `s // cnt`（向下取整）',
                 '易错：个数为 0 必须先返回 0，否则除零',
                 '对比灵神：灵神把判空和除法写成一行三目表达式，yiduobo 用 if/else'],
    ),
)
