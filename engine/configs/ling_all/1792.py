def _total(S):
    h = S.get('h')
    if not h:
        return ''
    t = sum(x[1] / x[2] for x in h)
    return f'当前通过率之和 = `{t:.4f}`，平均 = ==`{t / len(h):.5f}`==（堆顶 = 下一个增量最大的班级）'


CONFIG = dict(
    num=1792, title='最大平均通过率', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最大堆 · 增量递减',
    tags=['堆（优先队列）', '难度分 1818'],
    code='''
class Solution:
    def maxAverageRatio(self, classes: List[List[int]], extraStudents: int) -> float:
        # 默认是小根堆，把增量取相反数，变成大根堆
        h = [((a - b) / (b * (b + 1)), a, b) for a, b in classes]
        heapify(h)  # 堆化，只需 O(n) 时间

        for _ in range(extraStudents):
            _, a, b = h[0]
            a += 1
            b += 1
            heapreplace(h, ((a - b) / (b * (b + 1)), a, b))  # 这样写比 pop 再 push 更快

        return sum(a / b for _, a, b in h) / len(h)
''',
    call='Solution().maxAverageRatio([[1,2],[3,5],[2,2]], 2)',
    expect=0.78333,
    result_fn=lambda r: round(r, 5),
    views=[
        dict(type='text', fn=_total, h=70),
        dict(type='heap', var='h', fmt=lambda x: f'{x[1]}/{x[2]}', label='h（格内 = 通过/总数）', h=200),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink')],
    captions={
        'h = [(': '每个班级入堆：`(−增量, a, b)`，增量 = `(b−a) / (b(b+1))`。堆里 ==−增量最小 = 增量最大== 在堆顶',
        'heapify(h)': '堆化，`O(n)`：现在 `h[0]` 是==增加一个学生收益最大==的班级',
        'for _ in range': '一共 `{extraStudents}` 个聪明学生，==每个都送给当前收益最大的班级==（增量递减，所以贪心成立）',
        '_, a, b = h[0]': '看堆顶班级：`{a}/{b}`，先不弹出',
        'a += 1': '送一个学生：通过人数 `a` → {a}',
        'b += 1': '总人数 `b` → {b}，新通过率 `{a}/{b}`',
        'heapreplace': '用 `heapreplace` 一步完成弹出旧堆顶 + 压入新增量：该班下一个增量 `(b−a)/(b(b+1))` 变小，堆自动调整',
        'return sum': '所有班级通过率之和 ÷ 班级数 = =={ret:.5f}==',
    },
    cards=dict(
        one_liner='每个学生都送给「增加后通过率涨得最多」的班级',
        complexity='时间 `O(n + k log n)`，空间 `O(n)`',
        problem=['`classes[i] = [pass, total]`，再来 `extraStudents` 个必过的学生，可分到任意班级',
                 '让所有班级通过率的平均值最大',
                 '示例：`[[1,2],[3,5],[2,2]]`，2 人 → ==0.78333=='],
        quote='随着增加的学生越来越多，通过率的增量是递减（非递增）的。做法类似 23. 合并 K 个升序链表：创建一个最大堆，谁的下一个增量最大，谁就在堆顶。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一个班：第 1 个学生涨得多，第 2 个涨得少…增量只会越来越小',
              '所以每次选当前==增量最大==的班级，等价于从 n 个递减序列里选最大的 k 个数',
              '增量 `(a+1)/(b+1) − a/b = (b−a)/(b(b+1))`，取负数当最大堆用'],
        summary=['时间 `O(n + k log n)`，k = extraStudents；`heapify` 只要 `O(n)`',
                 '已经 100% 的班级增量为 0，永远不会被选到',
                 '`heapreplace` 比 pop 再 push 更快',
                 '浮点数有舍入误差；灵神写法二用 `a*d > b*c` 交叉相乘比较，不用浮点数（视频只演示写法一）'],
    ),
)
