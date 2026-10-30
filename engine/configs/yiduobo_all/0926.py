CONFIG = dict(
    num=926, title='将字符串翻转到单调递增', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前缀 1 的个数 + 从后往前',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def minFlipsMonoIncr(self, S):

        one = [0]
        for char in S:
            if char == '0':
                one.append(one[-1])
            else:
                one.append(one[-1] + 1)
        
        res = len(S) + 1
        cnt = 0
        for index in range(len(S) - 1, -1, -1):
            if S[index] == '1':
                continue
            res = min(res, cnt + one[index])
            cnt += 1
        
        return min(res, cnt)
''',
    call="Solution().minFlipsMonoIncr('010110')",
    expect=2,
    views=[
        dict(type='string', var='S', pointers={'index': 'blue'}, h=200, label='S（单调递增 = 前面全 0、后面全 1）',
             color=lambda S, i, v: ('yellow' if 'index' in S and i == S['index'] and 'cnt' in S else None)),
        dict(type='array', var='one', pointers={'index': 'pink'}, h=200, label='one[i] = S 前 i 个字符里 1 的个数'),
        dict(type='text', h=90, fn=lambda S: (f"在 `index={S['index']}` 的 0 处切开：左边的 `{S['one'][S['index']]}` 个 1 改成 0，右边已经数过的 `{S['cnt']}` 个 0 改成 1" if 'cnt' in S and 'index' in S and S['index'] < len(S['S']) and S['S'][S['index']] == '0' else '')),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'one = [0]': '`one[i]` 表示前 `i` 个字符中 1 的个数，先放一个 0（空前缀）',
        "if char == '0'": '字符 `{char}`：0 不增加 1 的个数，1 才增加',
        'one.append(one[-1])': '遇到 0，前缀 1 的个数不变：`one` 末尾加 `{one[-1]}`',
        'one.append(one[-1] + 1)': '遇到 1，前缀 1 的个数 +1：`one` 末尾加 `{one[-1]}`',
        'res = len(S) + 1': '`res` 初始为一个不可能达到的大数 `{res}`',
        'cnt = 0': '`cnt` = 从后往前已经遇到的 0 的个数（它们要改成 1）',
        'for index in range(len(S) - 1': '从后往前看第 `{index}` 个字符',
        "if S[index] == '1'": lambda S, B, r: (f"`S[{S.index}] = 1`：1 放在后面不会破坏单调性，直接看前一个" if S.S[S.index] == '1' else f"`S[{S.index}] = 0`：需要决定怎么处理它"),
        'res = min(res': '方案：这个 0 及其前面全改成 0（前面 `{one[index]}` 个 1 改掉），右边 `{cnt}` 个 0 改成 1，共 `{cnt + one[index]}`；`res = {res}`',
        'cnt += 1': '或者把这个 0 也改成 1，以后算作 `cnt` → =={cnt}==',
        'return min(res, cnt)': '还有一种：所有 0 都改成 1，代价 `cnt = {cnt}`；取较小值 `{min(res, cnt)}`',
    },
    cards=dict(
        one_liner='从后往前看：每个 0 要么改成 1，要么把它前面的 1 全改成 0',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一个只含 `0` 和 `1` 的字符串，翻转最少的字符，让它变成 ==单调递增==（先 0 后 1）',
                 '示例：`"00110"` → `1`（把最后的 0 翻成 1）',
                 '本视频：`"010110"` → `2`'],
        quote='对于每个字符，只有当该字符为0的时候才需要考虑如何进行修改，否则都可以直接考虑更前面的字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['倒数第一个 0 之后全是 1，不用管；遇到 0 有两个选择',
              '改成 1，继续往前看，代价 `cnt` 加 1',
              '或者让它前面全变成 0，代价 = 前面所有 1 的个数 = `one[index]`，再加已累计的 `cnt`'],
        summary=['时间 `O(n)`，空间 `O(n)`（前缀数组 `one`）',
                 '最后别忘了 `min(res, cnt)`：全部 0 改成 1 的方案',
                 '`one[index]` 是前 `index` 个字符，不含当前字符',
                 '原文本身就是 Python 3 可运行的写法，未做修改'],
    ),
)
