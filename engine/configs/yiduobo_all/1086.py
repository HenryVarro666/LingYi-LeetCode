CONFIG = dict(
    num=1086, title='前五科的均分', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表 + 手动维护前五高',
    code='''
class Solution(object):
    def highFive(self, items):

        score_dict = {}
        for id, score in items:
            if id not in score_dict:
                score_dict[id] = [0] * 5
            
            p = 5
            for index in range(5):
                if score_dict[id][index] < score:
                    p = index
                    break
            
            for index in range(4, p, -1):
                score_dict[id][index] = score_dict[id][index - 1]
            
            if p < 5:
                score_dict[id][p] = score
        
        result = []
        for id in score_dict:
            result.append([id, sum(score_dict[id]) // 5])
        
        return sorted(result)
''',
    call='Solution().highFive([[1,91],[1,92],[2,93],[2,97],[1,60],[2,77],[1,65],[1,87],[2,60],[2,80]])',
    expect=[[1, 79], [2, 81]],
    skip=['for index in range(5)', 'break', 'if p < 5', 'for index in range(4, p, -1)', 'score_dict[id][index] = score_dict[id][index - 1]'],
    max_steps=60,
    views=[
        dict(type='text', fn=lambda S: (f"当前记录 `({S['id']}, {S['score']})`，插入位置 `p = {S['p']}`" if 'p' in S and 'score' in S and 'result' not in S else ''), size=34),
        dict(type='map', var='score_dict', h=260, fmt=lambda k, v: f'学生 {k}: {v}'),
        dict(type='array', var='result', h=150, label='result'),
    ],
    watch=['id', 'score', 'p', ('res', 'result', 'green')],
    captions={
        'score_dict = {}': '哈希表：学生 id → 他当前最高的 5 个分数（降序）',
        'for id, score in items': '读到记录：学生 `{id}` 考了 `{score}` 分',
        'if id not in score_dict': lambda S, B, r: (f'学生 `{S.id}` 第一次出现 → 建一个 5 个 0 的数组占位' if S.id not in S.score_dict else f'学生 `{S.id}` 已有记录 → 直接插入'),
        'p = 5': '`p` = 新分数该插入的位置，先假设 5（比前五都小，不插入）',
        'if score_dict[id][index] < score': lambda S, B, r: (f"`{S.score_dict[S.id][S.index]} < {S.score}` 成立 → 新分数比这位高，插入点就是 `{S.index}`"
                                                              if S.score_dict[S.id][S.index] < S.score else
                                                              f"`{S.score_dict[S.id][S.index]} < {S.score}` 不成立 → 这位不比新分数低，继续往后看"),
        'p = index': '记下插入位置 `p = {p}`，退出查找',
        'for index in range(4, p, -1)': '从后往前，把 `p` 之后的分数依次右移一位，最后一名被挤掉',
        'score_dict[id][index] = score_dict[id][index - 1]': '`第 {index} 位 = 第 {index-1} 位`：`{score_dict[id]}`',
        'if p < 5': lambda S, B, r: (f'`p = {S.p} < 5`：新分数进入前五' if S.p < 5 else '`p = 5`：比前五都低，丢弃'),
        'score_dict[id][p] = score': '`p` 之后的分数已整体右移一位；把 `{score}` 放到第 `{p}` 位：`{score_dict[id]}`',
        'result = []': '遍历结束，每个学生手里都是自己的前五高，开始求平均',
        'result.append': '学生 `{id}`：前五之和 `{sum(score_dict[id])}` // 5 = =={sum(score_dict[id]) // 5}==',
        'return sorted': '按 id 升序排序，答案 `{sorted(result)}`',
    },
    cards=dict(
        one_liner='每个学生只留最高的 5 个分数，再求平均',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`items[i] = [id, score]`，每个学生至少有五个分数',
                 '求每个学生前五高分数的平均值（向下取整），按 id 升序返回',
                 '示例：学生 1 → 87，学生 2 → 88，返回 `[[1,87],[2,88]]`（本视频用更小的数据）'],
        quote='以学生的id作为key，使用哈希表将每个学生前5高的分数分别储存起来。遍历完成后，对于每个学生计算其前5高的分数的平均值，排序后即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表里每个学生维护长度 5 的降序数组，不用堆也不用全排序',
              '新分数找到第一个比它小的位置 `p`，后面的整体右移再放入',
              '最后对每个学生求和再除 5，`sorted` 按 id 排序'],
        summary=['时间 `O(n)`（每条记录只做常数 5 次操作），空间 `O(学生数)`',
                 '原文为 Python 2 写法，整数除法 `/ 5` 已改为 `// 5`',
                 '用 0 占位：分数都不小于 0，所以能被任何新分数挤掉',
                 '`p` 初始 5 表示不插入，`if p < 5` 不能漏'],
    ),
)
