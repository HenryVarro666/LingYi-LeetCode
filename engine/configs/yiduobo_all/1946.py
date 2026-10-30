CONFIG = dict(
    num=1946, title='子字符串突变后可能得到的最大整数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 找起点替换到不赚为止',
    tags=['灵神题单', '贪心算法', '难度分 1445'],
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
    call='Solution().maximumNumber("02135", [9,4,3,5,7,2,1,9,0,6])',
    expect='93455',
    views=[
        dict(type='text', fn=lambda S: (f"当前数位 `{S['char']}` → 映射 `{S['change'][int(S['char'])]}`：" +
                                        ('==更大，开始/继续替换==' if S['change'][int(S['char'])] > int(S['char'])
                                         else ('==更小，且已在替换中 → 停止==' if S['change'][int(S['char'])] < int(S['char']) and S['flag']
                                               else '没有收益，原样保留')))
             if 'char' in S else '', size=26),
        dict(type='string', var='num', label='num（蓝 = 当前扫描的数位）', cell=84, pointers={'index': 'blue'},
             color=lambda S, k, v: 'blue' if S.get('index') == k else None),
        dict(type='array', var='change', label='change[d]：数字 d 映射到的数字', cell=70,
             pointers={'int(char)': 'pink'}, pointer_labels={'int(char)': 'd'}),
        dict(type='array', var='num_list', label='num_list（已经得到的结果高位）', cell=70,
             color=lambda S, k, v: 'green'),
    ],
    watch=['flag', ('index', 'index', 'blue'), ('char', 'char')],
    captions={
        'flag = False': '`flag` 标记==已经进入替换区间==',
        'num_list = []': '`num_list` 存结果的每一位',
        'for index, char': '扫描高位到低位：`index = {index}`，`char = {char}`',
        'if change[ord(char) - 48] >': lambda S, B, r: (f"`change[{S.char}] = {S.change[int(S.char)]} > {S.char}` → 替换有==正收益==，从这里（或继续）替换"
                                                        if S.change[int(S.char)] > int(S.char)
                                                        else f"`change[{S.char}] = {S.change[int(S.char)]}` 不大于 `{S.char}` → 没有正收益"),
        'flag = True': '进入替换区间：`flag = True`',
        'num_list.append(change': '放入映射后的数字：`num_list = {num_list}`',
        'if change[ord(char) - 48] <': lambda S, B, r: (f"`change[{S.char}] = {S.change[int(S.char)]} < {S.char}` 且 `flag` 为真 → 替换会变小，==到此为止=="
                                                        if S.change[int(S.char)] < int(S.char) and S.flag
                                                        else f"替换收益不为负或还没开始替换 → 不用停（`flag = {S.flag}`）"),
        'return \'\'.join([str(x) for x in num_list]) + num[index:]': '替换区间结束：已替换的部分 + 原串剩余后缀 `num[{index}:]` = `{ret}`',
        'num_list.append(ord(char) - 48)': '这一位不替换（或收益为 0）：保留原数字 `{char}`',
        'return \'\'.join': '整串扫完：`{ret}`',
    },
    cards=dict(
        one_liner='从高位找第一个能变大的位置开始换，换到会变小为止',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`num` 是大整数字符串，`change[d]` 把数字 `d` 映射成另一个数字',
                 '可以选一个连续子串，把其中每位按 `change` 替换，求能得到的最大整数',
                 '示例：`"132"`，`change = [9,8,5,0,3,6,4,2,6,8]` → `"832"`'],
        quote='若当前位置上替换的收益不为负，那么就执行替换，然后继续向后考虑。重复此过程直到替换没有收益了，或者替换完了整个字符串后缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['只能换一个子串，所以要在==高位==上找有收益的地方开始换',
              '`change[d] > d` 才值得作为起点；起点之前的数位保持不变',
              '开始后，收益为 0（相等）也可以继续换；一旦变小就停，后面保持原样'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`ord(char) - 48` 就是字符转数字',
                 '易错：相等（收益为 0）不要停，后面可能还有更大的',
                 '易错：还没开始替换时遇到变小的数位只能跳过，不能停止（靠 `flag` 区分）'],
    ),
)
