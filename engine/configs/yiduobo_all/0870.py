CONFIG = dict(
    num=870, title='优势洗牌', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='下等牌对上等牌 · 排序后双指针',
    tags=['灵神题单', '双序列配对', '难度分 1648'],
    code='''
class Solution(object):
    def advantageCount(self, A, B):

        n = len(A)
        l, r = 0, n - 1
        res = [0] * n
        sorted_B = sorted(zip(B, range(n)), key=lambda d:d[0])
        for num in sorted(A):
            if num > sorted_B[l][0]:
                res[sorted_B[l][1]] = num
                l += 1
            else:
                res[sorted_B[r][1]] = num
                r -= 1
        
        return res
''',
    call='Solution().advantageCount([12,24,8,32], [13,25,32,11])',
    expect=[24, 32, 8, 12],
    views=[
        dict(type='array', var='A', label='A（原顺序）', h=150),
        dict(type='array', var='sorted_B', label='sorted_B：(B 的值, 原下标) 按值排序', h=190, cell=120,
             fmt=lambda v: f'{v[0]}@{v[1]}' if isinstance(v, tuple) else str(v),
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r')),
        dict(type='array', var='res', label='res：A 的新排列', h=160,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=['num', ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        'l, r = 0': '`l` 指 B 的下等牌，`r` 指 B 的上等牌',
        'sorted_B = sorted': 'B 连同原下标一起排序：`{sorted_B}`，这样排完仍知道每张牌原来在哪',
        'for num in sorted': '把 A 从小到大逐张出牌：`num = {num}`',
        'if num > sorted_B': '`num = {num}` 能打过 B 的下等牌 `{sorted_B[l][0]}` 吗？{"能" if num > sorted_B[l][0] else "不能（打不过）"}',
        'res[sorted_B[l][1]] = num': '这张牌能发挥作用：去对 B 的下等牌，放到 `res[{sorted_B[l][1]}]`' ,
        'l += 1': 'B 的下等牌已被击败，`l` → {l}',
        'res[sorted_B[r][1]] = num': '连下等牌都打不过，只能去对上等牌：放到 `res[{sorted_B[r][1]}]`',
        'r -= 1': 'B 的上等牌已安排好对手，`r` → {r}',
        'return res': '排列完成：`res = {res}`',
    },
    cards=dict(
        one_liner='用 A 的下等牌，去对 B 的上等牌',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`A[i] > B[i]` 的个数叫 A 的优势',
                 '重排 A，让优势最大',
                 '示例：A=`[12,24,8,32]`，B=`[13,25,32,11]` → `[24,32,8,12]`'],
        quote='田忌赛马问题，思路就是用A的下等牌去对B的上等牌。',
        quote_src='—— yiduobo 题解原文',
        idea=['A、B 都排序，`l` 指 B 的下等牌，`r` 指 B 的上等牌',
              '`A[index] > B[l]`：这张牌能赢，就去对 `B[l]`，`l` 后移',
              '`A[index] <= B[l]`：连最小的都赢不了，就去对 `B[r]`，`r` 前移'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：B 排序时要带上原下标 `(值, 下标)`，否则无法把牌放回原位',
                 '相等不算赢，要走 else 分支',
                 '与灵神对比：灵神排的是下标数组 idx，yiduobo 排的是 (值, 下标) 二元组'],
    ),
)
