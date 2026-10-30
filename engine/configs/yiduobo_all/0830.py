CONFIG = dict(
    num=830, title='较大分组的位置', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟扫描 · 记录左边界',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def largeGroupPositions(self, s):

        start_pos = 0
        now = ''
        res = []
        for index, char in enumerate(s):
            if char != now:
                if index - start_pos >= 3:
                    res.append([start_pos, index - 1])
                start_pos = index
                now = char
        
        if index - start_pos >= 2:
            res.append([start_pos, index])
        
        return res
''',
    call="Solution().largeGroupPositions('abbxxxxzzz')",
    expect=[[3, 6], [7, 9]],
    views=[
        dict(type='string', var='s', pointers={'start_pos': 'blue', 'index': 'pink'}, h=210,
             color=lambda S, i, v: ('green' if 'start_pos' in S and 'index' in S and S['start_pos'] <= i < S['index'] and S['index'] - S['start_pos'] >= 3 else None)),
        dict(type='text', h=90, fn=lambda S: f"当前分组 [start_pos, index] = [{S['start_pos']}, {S['index']}]，结果 res = =={S['res']}==" if 'index' in S and 'start_pos' in S else ''),
    ],
    watch=[('start_pos', 'start_pos', 'blue'), ('index', 'index', 'pink'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'start_pos = 0': '`start_pos`：当前连续字符段的左边界',
        5: '`now`：当前这一段的字符',
        'res = []': '`res` 存放长度 >= 3 的分组区间',
        'if char != now': lambda S, B, r: (f'`{S.char}` ≠ `{B.now or "空"}` → 新的一段开始，要结算上一段' if S.char != B.now
                                           else f'`{S.char}` == `{B.now}` → 还在同一段里，继续向后扫'),
        'if index - start_pos >= 3': lambda S, B, r: (f'上一段长度 `{S.index} − {S.start_pos} = {S.index - S.start_pos}`'
                                                      + (' >= 3 → ==是较大分组==' if S.index - S.start_pos >= 3 else ' < 3 → 太短，不记')),
        'res.append([start_pos, index - 1])': '记下区间 `[{start_pos}, {index - 1}]`（右端是 index−1，因为 index 已是新字符）→ res = {res}',
        'start_pos = index': '新一段从这里开始：`start_pos` → {start_pos}',
        'now = char': '`now` → `{now}`',
        'if index - start_pos >= 2': lambda S, B, r: (f'扫描结束后，==最后一段还没结算==：长度 `{S.index} − {S.start_pos} + 1 = {S.index - S.start_pos + 1}`'
                                                      + (' >= 3 → 是较大分组' if S.index - S.start_pos >= 2 else ' < 3 → 不记')),
        'res.append([start_pos, index])': '最后一段的右端就是 `index`：记下 `[{start_pos}, {index}]` → res = {res}',
        'return res': '返回所有较大分组：`{res}`',
    },
    cards=dict(
        one_liner='扫一遍，字符一变就结算上一段；别忘了最后一段',
        complexity='时间 `O(n)`，空间 `O(1)`（不计结果）',
        problem=['连续相同字符组成一个分组，长度 >= 3 的叫较大分组',
                 '按起始下标升序，返回每个较大分组的 `[起点, 终点]`',
                 '示例：`abbxxxxzzy` → `[[3,6]]`；本视频：`abbxxxxzzz` → `[[3,6],[7,9]]`'],
        quote='不要忘记扫描完成后还需要额外判断最后一个区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `start_pos` 记录当前段的左边界，`now` 记录当前段字符',
              '遇到不同字符，说明上一段在 `index − 1` 结束，用 `index − start_pos` 判断长度',
              '最后一段后面没有新字符触发结算，要循环外单独判断'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环内上一段长度是 `index − start_pos`，循环外最后一段长度是 `index − start_pos + 1`，所以阈值分别是 3 和 2',
                 '原文为 Python 2 风格，本题代码无需改动，直接可在 Python 3 运行',
                 '空串会让 `index` 未定义，但题目保证 `s` 非空'],
    ),
)
