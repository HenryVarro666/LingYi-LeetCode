CONFIG = dict(
    num=1570, title='两个稀疏向量的点积', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='只存非零项 + 双指针合并',
    tags=['灵神题单'],
    code='''
class SparseVector:
    def __init__(self, nums):

        self.digit_list = []
        for index, num in enumerate(nums):
            if num > 0:
                self.digit_list.append([index, num])

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec):
        p1 = p2 = 0
        res = 0
        while p1 < len(self.digit_list) and p2 < len(vec.digit_list):
            if self.digit_list[p1][0] == vec.digit_list[p2][0]:
                res += self.digit_list[p1][1] * vec.digit_list[p2][1]
                p1 += 1
                p2 += 1
            elif self.digit_list[p1][0] < vec.digit_list[p2][0]:
                p1 += 1
            else:
                p2 += 1

        return res
''',
    call='''v1 = SparseVector([0, 1, 0, 0, 2, 0, 0])
v2 = SparseVector([1, 0, 0, 0, 3, 0, 4])
v1.dotProduct(v2)''',
    expect=6,
    views=[
        dict(type='table', var='self.digit_list', label='self（向量 1）：只存 [下标, 值]；蓝 = p1 所指', h=190, cols=['下标', '值'],
             color=lambda S, i, j, v: 'blue' if 'p1' in S and i == S['p1'] else None),
        dict(type='table', var='vec.digit_list', label='vec（向量 2）：粉 = p2 所指', h=230, cols=['下标', '值'],
             color=lambda S, i, j, v: 'pink' if 'p2' in S and i == S['p2'] else None),
        dict(type='text', size=30, h=80, fn=lambda S: (
            (lambda a, b: f"下标比较：`{a}` 与 `{b}`，累计 res = =={S['res']}==")(S['self'].digit_list[S['p1']][0], S['vec'].digit_list[S['p2']][0])
            if 'p1' in S and 'res' in S and S['p1'] < len(S['self'].digit_list) and S['p2'] < len(S['vec'].digit_list) else '')),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), ('res', 'res', 'green')],
    captions={
        'self.digit_list = []': '只存非零项，每项是 `[下标, 值]`，零不会影响点积',
        'if num > 0': '`{num} > 0` → ' + '{"非零，记下来" if num > 0 else "是 0，跳过"}',
        'self.digit_list.append': '记下 `[{index}, {num}]`',
        'p1 = p2 = 0': '`p1`、`p2` 分别指向两个向量的非零项列表开头',
        'res = 0': '`res` 累加点积',
        'while p1 < len': lambda S, B, r: ('两边都还有非零项，继续对齐' if S.p1 < len(S['self'].digit_list) and S.p2 < len(S['vec'].digit_list) else '有一边走完了：后面的下标另一边都是 0 → 结束'),
        'if self.digit_list[p1][0] == vec': '两边下标相同吗？`{self.digit_list[p1][0]}` vs `{vec.digit_list[p2][0]}`',
        'res += ': '同一个下标上两边都非零：`{self.digit_list[p1][1]} × {vec.digit_list[p2][1]}` 加进答案 → res = =={res}==',
        'p1 += 1': lambda S, B, r: (f'`p1` → {S.p1}' ),
        'p2 += 1': lambda S, B, r: (f'`p2` → {S.p2}'),
        'elif self.digit_list[p1][0] <': lambda S, B, r: f"`{S['self'].digit_list[S.p1][0]} < {S['vec'].digit_list[S.p2][0]}`？" + ('是：p1 这个下标在另一边是 0，对点积没贡献，p1 后移' if S['self'].digit_list[S.p1][0] < S['vec'].digit_list[S.p2][0] else '否：p2 的下标更小，p2 后移'),
        'return res': '点积 = `{res}`',
    },
    cards=dict(
        one_liner='零不贡献点积：只存非零项，双指针按下标对齐',
        complexity='构造 `O(n)`，点积 `O(k1 + k2)`，k 为非零个数',
        problem=['设计 `SparseVector`：大部分元素为 0 的向量',
                 '`dotProduct(vec)` 返回两个向量的点积',
                 '示例：`[0,1,0,0,2,0,0]` · `[1,0,0,0,3,0,4]` → `6`'],
        quote='0是不会对向量点积产生影响的，因此稀疏向量只需要储存非0列的下标以及数值。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个向量存成 `[下标, 值]` 的有序列表，下标天然递增',
              '`p1`、`p2` 各指一边：下标相同才相乘累加，否则下标小的那边后移',
              '任何一边走完就结束，剩下的另一边乘 0'],
        summary=['点积 `O(k1 + k2)`，空间 `O(k)`',
                 '原文用 `num > 0` 判断非零，题目元素非负所以没问题；有负数应写 `num != 0`',
                 '下标不等时只移动下标小的一边，不能两边一起动',
                 '本题代码是 Python 3 风格，无需修改'],
    ),
)
