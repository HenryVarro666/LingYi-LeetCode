CONFIG = dict(
    num=1946, title='子字符串突变后可能得到的最大整数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历 · flag 标记是否已开始替换',
    tags=['灵神题单', '贪心与思维', '难度分 1445'],
    code='''
class Solution(object):
    def maximumNumber(self, num, change):

        flag = False
        num_list = []
        for index, char in enumerate(num):
            if change[ord(char) - 48] > ord(char) - 48:
                flag = True
                num_list.append(change[ord(char) - 48])
            else:
                if change[ord(char) - 48] < ord(char) - 48 and flag:
                    return ''.join([str(x) for x in num_list]) + num[index:]
                
                num_list.append(ord(char) - 48)
        
        return ''.join([str(x) for x in num_list])
''',
    call='Solution().maximumNumber("3214", [9,8,5,0,3,6,4,2,6,8])',
    expect='3584',
    views=[
        dict(type='text', fn=lambda S: (f"`{S['char']}` → `change = {S['change'][int(S['char'])]}`；已开始替换：`{S['flag']}`" if 'char' in S else '一趟遍历：先找起点，再尽量延伸'), size=28),
        dict(type='string', var='num', pointers={'index': 'pink'}, h=200,
             color=lambda S, i, v: 'green' if 'index' in S and 'num_list' in S and i < len(S['num_list']) and S['num_list'][i] != int(S['num'][i]) else None),
        dict(type='array', var='num_list', h=200, label='num_list（已确定的前缀）'),
        dict(type='array', var='change', h=200, label='change'),
    ],
    watch=[('index', 'index', 'pink'), 'char', ('flag', 'flag', 'blue')],
    captions={
        'flag = False': '`flag` 记录：是否已经遇到起点开始替换',
        'if change[ord(char) - 48] > ord(char) - 48': lambda S, B, r: (f'`change[{S.char}] = {S.change[int(S.char)]} > {S.char}` → ==替换有收益==，开始（或继续）替换' if S.change[int(S.char)] > int(S.char) else f'`change[{S.char}] = {S.change[int(S.char)]}` 不大于 `{S.char}` → 没有收益'),
        'flag = True': '`flag = True`：从这一位起进入替换状态',
        'num_list.append(change': '这一位替换为 `{num_list[-1]}`',
        'if change[ord(char) - 48] < ord(char) - 48 and flag': lambda S, B, r: (f'`change[{S.char}] = {S.change[int(S.char)]} < {S.char}` 且 已在替换：==替换会亏，到此为止，后面原样保留==' if (S.change[int(S.char)] < int(S.char) and S.flag) else ('替换没有变小，但还没开始替换（`flag` 为假）→ 保持原样' if S.change[int(S.char)] < int(S.char) else f'`change[{S.char}] = {S.change[int(S.char)]}` == `{S.char}` → 替换无收益也无损失，原样保留')),
        'num_list.append(ord(char) - 48)': '这一位保持原样 `{num_list[-1]}`',
        "return ''.join([str(x) for x in num_list]) + num[index:]": '替换中遇到会变小的位 → 前缀 `{num_list}` + 剩余原串 `{num[index:]}` = =={ret}==',
    },
    cards=dict(
        one_liner='从高位找第一个能变大的位开始换，遇到变小就停',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`num` 是大整数字符串，`change[d]` 表示数字 `d` 突变后的值',
                 '可以选一个连续子串全部突变（也可以不突变），求能得到的最大整数',
                 '示例：`"132"`，`change = [9,8,5,0,3,6,4,2,6,8]` → `"832"`'],
        quote='由于只能替换一个子字符串，因此必然是选择高位上有收益的地方进行替换，于是可以从高位开始向低位一趟遍历，找到替换的起点。',
        quote_src='—— yiduobo 题解原文',
        idea=['高位决定大小：第一个替换后变大的位就是起点',
              '起点之后，替换收益不为负就继续换（相等也换）',
              '一旦遇到会变小的位，立刻把剩下的原串接上返回'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`flag` 区分"还没起点"和"已在替换"：没起点时遇到变小的位只是保持原样',
                 '易错点：相等的位在替换中要继续换，不能当终止条件',
                 '原文为 Python 2 风格，除代码外没有改动'],
    ),
)
