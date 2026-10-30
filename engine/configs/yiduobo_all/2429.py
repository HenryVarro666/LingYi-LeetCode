CONFIG = dict(
    num=2429, title='最小异或', difficulty='Medium', category='位运算',
    author='yiduobo', technique='高位抵消 + 低位补位',
    tags=['灵神题单', '位运算', '难度分 1532'],
    code='''
class Solution(object):
    def minimizeXor(self, num1, num2):

        cnt = 0
        while num2:
            cnt += 1
            num2 -= num2 & -num2

        one_set = set()
        one_list = []
        now = num1
        while now:
            lowbit = now & -now
            one_set.add(lowbit)
            one_list.append(lowbit)
            now -= lowbit

        now = 1
        res = 0
        while cnt > 0:
            if one_list:
                res += one_list[-1]
                one_list.pop()
            else:
                while now in one_set:
                    now += now
                res += now
                now += now

            cnt -= 1
        
        return res
''',
    call='Solution().minimizeXor(22, 15)',
    expect=23,
    views=[
        dict(type='text', fn=lambda S: f"`num1 = 10110`（22）　x 要用 4 个 1　`res = {S['res']:06b}`（{S['res']}）" if 'res' in S else '`num1 = 10110`（22）　x 要用 4 个 1', size=32, h=90),
        dict(type='stack', var='one_list', label='one_list（num1 的各个 1，栈顶 = 最高位）', fmt=lambda x: str(x), h=300),
        dict(type='set', var='one_set', label='one_set（num1 里已占用的位）', fmt=lambda x: str(x), h=170),
    ],
    watch=['cnt', 'now', ('res', 'res', 'green')],
    skip=['one_set.add', 'now -= lowbit', 'now -= lowbit'],
    captions={
        'cnt = 0': '先统计 `num2` 有几个 1，就是 `x` 需要的 1 的个数',
        'cnt += 1': '又发现一个 1，`cnt = {cnt}`',
        'num2 -= num2 & -num2': '`num2 & -num2` 是最低位的 1，减掉它，`num2` 少一个 1',
        'one_set = set()': '`num1` 的所有 1 要记下来：用 set 查是否占用，用 list 按从低到高顺序存',
        'lowbit =': '取出 `now` 的最低位的 1：`lowbit = {lowbit}`',
        'one_set.add': '记入集合 `one_set`，方便之后查哪些位已被占用',
        'one_list.append': '记入列表：越后加入的位越高，列表末尾 = 最高位的 1',
        'now -= lowbit': '去掉这个 1，继续找下一个',
        'now = 1': '之后补多余的 1 时，从最低位 `1` 开始往上找空位',
        'while cnt > 0': lambda S, B, ret: f"判断 `cnt > 0`（{S['cnt']} > 0）→ {'还有 1 没放，继续' if S['cnt'] > 0 else '全部放完'}",
        'if one_list': lambda S, B, ret: f"判断 `one_list` 是否非空 → {'非空：num1 还有 1 没被抵消' if S['one_list'] else '空了：num1 的 1 都被抵消了'}",
        'res += one_list[-1]': '把 `x` 的 1 放在 `num1` 最高位的 1 上（1^1=0 抵消）：`res = {res}`',
        'one_list.pop': '这个最高位已匹配，弹出',
        'while now in one_set': '检查位 `now = {now}`：{"num1 在这一位有 1，放这里会让异或变大，要往更高位找" if now in one_set else "num1 这一位是 0，是空位"}',
        'res += now': '`num1` 的 1 已用完，==在最低的空位放 1==（异或增量最小）：`res = {res}`',
        'now += now': '`now` 翻倍，指向更高的下一位',
        'cnt -= 1': '放好一个 1，还剩 `{cnt}` 个',
        'return res': '`x` 有 4 个 1，且高位的 1 对齐 num1 → x = =={res}==',
    },
    cards=dict(
        one_liner='先抵消 num1 的高位 1，多余的 1 从最低空位放起',
        complexity='时间 `O(log num1 + log num2)`，空间 `O(log num1)`',
        problem=['找正整数 `x`：1 的个数与 `num2` 相同，且 `x ^ num1` 最小',
                 '置位数 = 二进制里 1 的个数',
                 '示例：`num1=3, num2=5` → `3`；`num1=1, num2=12` → `3`'],
        quote='为了使得num1^x最小，就应该先尽量用x中的1来抵消掉num1中1的影响。很明显，这里应该按照从高位到低位的顺序来进行这个抵消操作。',
        quote_src='—— yiduobo 题解',
        idea=['先数 `num2` 的 1：得到 `cnt`，即 `x` 要放几个 1',
              '`1^1=0`：x 的 1 放在 num1 的 1 上会抵消，优先放高位',
              'num1 的 1 抵消完还有剩，就从最低的、还没占用的位往上放'],
        summary=['时间 `O(log num1 + log num2)`，空间 `O(log num1)`',
                 '`n & -n` 取最低位的 1，`n -= n & -n` 去掉它',
                 '不用 bit_count，自己拆位数 1；用列表尾当最高位',
                 '易错：补位时要跳过 num1 已有的 1，否则会把异或结果变大'],
    ),
)
