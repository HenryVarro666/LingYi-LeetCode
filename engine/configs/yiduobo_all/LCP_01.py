CONFIG = dict(
    num='LCP 01', title='猜数字', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 数相同下标',
    code='''
class Solution(object):
    def game(self, guess, answer):

        res = 0
        for index in range(3):
            if guess[index] == answer[index]:
                res += 1
        
        return res
''',
    call='Solution().game([2,2,3],[3,2,1])',
    expect=1,
    views=[
        dict(type='array', var='guess', label='guess（小明猜的）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: ('green' if v == S['answer'][i] else 'red') if 'index' in S and i <= S['index'] else None),
        dict(type='array', var='answer', label='answer（小 A 的答案）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: ('green' if v == S['guess'][i] else 'red') if 'index' in S and i <= S['index'] else None),
        dict(type='text', fn=lambda S: f"已经猜对 ==`{S['res']}`== 次" if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 用来数猜对的次数，先记 0',
        'for index in range(3)': '一共只有 3 次，一趟遍历：这次看第 `{index}` 个位置',
        'if guess[index] == answer[index]': '比较 `guess[{index}] = {guess[index]}` 和 `answer[{index}] = {answer[index]}`：{"相同，猜对了" if guess[index] == answer[index] else "不同，没猜对"}',
        'res += 1': '这个位置猜对了，`res` 加一 → =={res}==',
        'return res': '三个位置都比完了，猜对 `{res}` 次',
    },
    cards=dict(
        one_liner='一趟遍历，数两个数组里相同的下标',
        complexity='时间 `O(1)`（固定 3 次），空间 `O(1)`',
        problem=['小 A 和小 B 玩猜数字，各出 3 次，每次从 1、2、3 里选一个',
                 '给定 `guess`（小 A 猜的）和 `answer`（小 B 的选择），求小 A 猜对了几次',
                 '本视频：`[2,2,3]` 对 `[3,2,1]` → `1`'],
        quote='比较基础的题目，一趟遍历，统计两个数组中值相同的下标数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['每一轮只和同一位置比较：`guess[i] == answer[i]` 就算猜对',
              '长度固定为 3，循环 3 次，用 `res` 累计'],
        summary=['时间、空间都是 `O(1)`',
                 '比较的是==同一下标==的两个值，不是看数字是否出现过',
                 '原文是 Python 2 风格的类写法，这里原样使用（`range` 在 Python 3 同样可用）'],
    ),
)
