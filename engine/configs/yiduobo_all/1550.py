CONFIG = dict(
    num=1550, title='存在连续三个奇数的数组', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟扫描 · 连续奇数计数',
    code='''
class Solution(object):
    def threeConsecutiveOdds(self, arr):

        cnt = 0
        for num in arr:
            if num & 1:
                cnt += 1
                if cnt == 3:
                    return True
            else:
                cnt = 0
        
        return False
''',
    call='Solution().threeConsecutiveOdds([1,2,34,3,4,5,7,23,12])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"以当前数结尾的连续奇数个数 `cnt` = =={S['cnt']}==" if 'cnt' in S else ''),
        dict(type='array', var='arr', h=300,
             color=lambda S, i, v: ('green' if v % 2 else None),
             label='arr（绿色 = 奇数）'),
    ],
    watch=[('num', 'num', 'blue'), ('cnt', 'cnt', 'yellow')],
    captions={
        4: '`cnt` 记录以当前位置为结尾的连续奇数个数',
        'for num in arr': '取下一个数 `num = {num}`',
        'if num & 1': lambda S, B, r: (f'`{S.num} & 1 = 1`：是奇数 → 成立' if S.num & 1 else f'`{S.num} & 1 = 0`：是偶数 → 不成立，连续奇数被打断'),
        'cnt += 1': '连续奇数 +1：`cnt = {cnt}`',
        'if cnt == 3': lambda S, B, r: (f'`cnt = 3` → 成立，三连奇出现' if S.cnt == 3 else f'`cnt = {S.cnt}` 还不到 3 → 继续'),
        'return True': '`cnt` 到了 3，返回 `True`',
        11: '遇到偶数，连续奇数中断：`cnt` 清零',
        'return False': '正常退出循环，说明 `cnt` 从没到过 3，返回 `False`',
    },
    cards=dict(
        one_liner='数连续奇数，数到 3 就赢，遇偶数清零',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['判断数组里是否存在连续三个元素都是奇数',
                 '示例：`[2,6,4,1]` → `false`',
                 '本视频：`[1,2,34,3,4,5,7,23,12]` → `true`'],
        quote='一趟扫描，记录以当前位置为结尾的连续奇数个数cnt。若当前数为奇数，那么将cnt加上1，当cnt等于3时返回true。若当前数为偶数，则将cnt置0。',
        quote_src='—— yiduobo 题解原文',
        idea=['用计数器代替窗口：奇数 `cnt += 1`，偶数 `cnt = 0`',
              '`num & 1` 取最低位，等价于判断奇数',
              '`cnt` 一到 `3` 立刻返回，否则扫完返回 `false`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：遇到偶数必须清零，否则会把不相邻的奇数算在一起',
                 '原文已是 Python 3 可运行，代码未做改动',
                 '对比灵神：灵神每次回看前两个数；这里只记一个计数，可直接推广到 `k` 个'],
    ),
)
