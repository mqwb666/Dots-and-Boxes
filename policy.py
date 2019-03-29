'''
仍需改进的地方：
    1、判断短格数目决定是否全吃长链(已解决，但有待测试)
    2、随机走棋需改进
    3、环中让格是否更好
'''
from random import randint, choice

class policy:

    def __init__(self):
        self.state = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.score = [0,0]

    def make_move(self): # 主要函数
        self.move_a_dead_edge_from_all() # 走一个死格
        if self.get_freedom_1s(): # 如果还有死格
            if self.get_safe_edge(): # 是否有安全边
                self.move_all_freedom_1s() # 走所有的死格
                self.move_edge(self.r,self.c) # 走之前得到的安全边
            else:
                self.move_double_cross(self.u,self.v) # 长链补格
            if sum(self.score) == 25:
                print('GAME OVER!')
        elif self.get_safe_edge(): self.move_edge(self.r,self.c) # 如果有安全边
        elif self.get_signle(): self.move_edge(self.r,self.c) # 如果有单格
        elif self.get_double(): self.move_edge(self.r,self.c) # 如果有双格
        else: self.move_random() # 随机走棋

    def set_edge_to_double_node(self, r, c): # 如果没有安全边，则留双交
        self.count = 0
        self.loop = False
        self.search_edge_to_count(0, r, c)
        if not self.loop: 
            while self.check_dead_node_but(r,c):
                self.move_edge(self.r,self.c)
        if self.score[0]+self.score[1]+self.count==25:
            while check_dead_node(): # 获得死边self.u,self.v
                move_edge(self.u,self.v)
        else:
            if self.loop:
                count -= 2
            self.set_count_to_edge(0,r,c)

    def search_edge_to_count(self,d,r,c): # d=1,2,3,4 top,right,down,left
        self.count += 1
        for i,j,k in [(-1,0,1),(0,1,2),(1,0,3),(0,-1,4)]:
            if d != k and self.state[r+i][c+j] == 0:
                if 0 < r+2*i < 10 and 0 < c+2*j < 10:
                    if self.state[r+2*i][c+2*j] <= 1:
                        self.count += 1
                        self.loop = True
                    elif self.state[r+2*i][c+2*j] <= 2:
                        self.search_edge_to_count((k+1)%4+1,r+2*i,c+2*j)
                break

    def move_double_cross(self,u,v):
        self.count = 0
        self.loop = False # 判断是否为环
        self.in_count(0,u,v)
        if not self.loop: self.move_other_long_chain(u,v) # 如果长链被截成两边，则下完长链另一边
        if self.count + sum(self.score) == 25:
            self.move_other_long_chain(-1,-1) # 走完所有的格子
        else:
            if self.loop: self.count -= 2
            self.let_flag = self.get_short_count() % 2 == 0 # 如果现在短链数量为偶数，则需要补格
            self.out_count(0,u,v)
            if not self.let_flag:
                if self.get_signle(): self.move_edge(self.r,self.c)
                elif self.get_double(): self.move_edge(self.r,self.c)
                else: print('Error')

    def move_other_long_chain(self,r,c):
        while self.get_freedom_1s_except(r,c):
            if self.state[self.u-1][self.v] == 0: self.move_edge(self.u-1,self.v)
            elif self.state[self.u][self.v+1] == 0: self.move_edge(self.u,self.v+1)
            elif self.state[self.u+1][self.v] == 0: self.move_edge(self.u+1,self.v)
            else : self.move_edge(self.u,self.v-1)

    def get_freedom_1s_except(self,r,c):
        for i in range(1,10,2):
            for j in range(1,10,2):
                if self.state[i][j] == 1:
                    if i!=r or j!=c:
                        self.u, self.v = i, j
                        return True
        return False

    def in_count(self,d,r,c):
        self.count += 1
        for i,j,k in [(-1,0,1),(0,1,2),(1,0,3),(0,-1,4)]:
            if d != k and self.state[r+i][c+j] == 0:
                if 0 < r+2*i < 10 and 0 < c+2*j < 10:
                    if self.state[r+2*i][c+2*j] <= 1:
                        self.count += 1
                        self.loop = True
                    elif self.state[r+2*i][c+2*j] <= 2:
                        self.in_count((k+1)%4+1,r+2*i,c+2*j)
                break
    
    def out_count(self,d,r,c):
        if self.count > 0:
            for i,j,k in [(-1,0,1),(0,1,2),(1,0,3),(0,-1,4)]:
                if d != k and self.state[r+i][c+j] == 0:
                    if self.let_flag:
                        if self.count != 2: self.move_edge(r+i,c+j)
                    else:
                        self.move_edge(r+i,c+j)
                    self.count -= 1
                    self.out_count((k+1)%4+1,r+2*i,c+2*j)
                    break
    
    def get_short_count(self):
        count = 0
        for r in range(1,10,2):
            for c in range(1,10,2):
                if self.state[r][c] == 2:
                    num = 0
                    for i, j in [(-1,0),(0,1),(1,0),(0,-1)]:
                        if self.state[r+i][c+j] == 0:
                            if not (0<r+2*i<10 and 0<c+2*j<10) or self.state[r+2*i][c+2*j] > 2:
                                num += 1
                            if num > 1:
                                print((r+i, c+j))
                                count += 1
                                break
        for r in range(1,10,2):
            for c in range(1,8,2):
                if self.state[r][c]==self.state[r][c+2]==2 and self.state[r][c+1]==0:
                    if self.left_double(r,c) and self.right_double(r,c+2):
                        print((r, c+1))
                        count += 1
        for r in range(1,8,2):
            for c in range(1,10,2):
                if self.state[r][c]==self.state[r+2][c]==2 and self.state[r+1][c]==0:
                    if self.top_double(r,c) and self.down_double(r+2,c):
                        print((r+1, c))
                        count += 1
        return count

    def get_signle(self):
        for r in range(1,10,2):
            for c in range(1,10,2):
                if self.state[r][c] == 2:
                    num = 0
                    for i, j in [(-1,0),(0,1),(1,0),(0,-1)]:
                        if self.state[r+i][c+j] == 0:
                            if not (0<r+2*i<10 and 0<c+2*j<10) or self.state[r+2*i][c+2*j] > 2:
                                num += 1
                            if num > 1:
                                self.r, self.c = r+i, c+j
                                return True
        return False

    def get_double(self):
        for r in range(1,10,2):
            for c in range(1,8,2):
                if self.state[r][c]==self.state[r][c+2]==2 and self.state[r][c+1]==0:
                    if self.left_double(r,c) and self.right_double(r,c+2):
                        self.r, self.c = r, c+1
                        return True
        for r in range(1,8,2):
            for c in range(1,10,2):
                if self.state[r][c]==self.state[r+2][c]==2 and self.state[r+1][c]==0:
                    if self.top_double(r,c) and self.down_double(r+2,c):
                        self.r, self.c = r+1, c
                        return True
        return False

    def left_double(self,r,c):
        if self.state[r-1][c] == 0: # 上
            if r == 1 or self.state[r-2][c] > 2: return True                
        elif self.state[r+1][c] == 0: # 下
            if r == 9 or self.state[r+2][c] > 2: return True   
        elif self.state[r][c-1] == 0: # 左
            if c == 1 or self.state[r][c-2] > 2: return True
        return False

    def right_double(self,r,c):
        if self.state[r-1][c] == 0: # 上
            if r == 1 or self.state[r-2][c] > 2: return True                
        elif self.state[r+1][c] == 0: # 下
            if r == 9 or self.state[r+2][c] > 2: return True   
        elif self.state[r][c+1] == 0: # 右
            if c == 9 or self.state[r][c+2] > 2: return True
        return False

    def top_double(self,r,c):
        if self.state[r-1][c] == 0: # 上
            if r == 1 or self.state[r-2][c] > 2: return True                
        elif self.state[r][c-1] == 0: # 左
            if c == 1 or self.state[r][c-2] > 2: return True
        elif self.state[r][c+1] == 0: # 右
            if c == 9 or self.state[r][c+2] > 2: return True   

    def down_double(self,r,c):
        if self.state[r+1][c] == 0: # 下
            if r == 9 or self.state[r+2][c] > 2: return True                
        elif self.state[r][c-1] == 0: # 左
            if c == 1 or self.state[r][c-2] > 2: return True
        elif self.state[r][c+1] == 0: # 右
            if c == 9 or self.state[r][c+2] > 2: return True   

    def move_random(self):
        enable_edge = self.get_enable_edge()
        r, c = choice(enable_edge)
        self.move_edge(r,c)

    def move_all_freedom_1s(self):
        while self.get_freedom_1s():
            self.move_dead_node(self.u,self.v)
    
    def move_dead_node(self,r,c):
        if   self.state[r-1][c] == 0: self.move_edge(r-1,c)
        elif self.state[r][c+1] == 0: self.move_edge(r,c+1)
        elif self.state[r+1][c] == 0: self.move_edge(r+1,c)
        elif self.state[r][c-1] == 0: self.move_edge(r,c-1)  

    def get_safe_edge(self):
        enable_edge = self.get_enable_edge()
        size = len(enable_edge)
        if size == 0: return False
        t = randint(0,size-1)
        start_t = t
        self.r, self.c = enable_edge[t]
        while True:
            if self.is_safe_edge(self.r,self.c): return True
            t = (t + 1) % size
            if start_t == t: return False
            self.r, self.c = enable_edge[t]

    def get_enable_edge(self): # 获得所有可行边
        enable_edge = []
        for i in range(0,11,2):
            for j in range(1,10,2):
                for r, c in ((i,j),(j,i)):
                    if self.state[r][c] == 0:
                        enable_edge.append((r,c))
        return enable_edge
                
    def is_safe_edge(self,r,c):
        if r % 2 == 0:
            if r == 0:
                if self.state[r+1][c] > 2: return True
            if r == 10:
                if self.state[r-1][c] > 2: return True
            else: return self.state[r+1][c] > 2 and self.state[r-1][c] > 2
        else:
            if c == 0:
                if self.state[r][c+1] > 2: return True
            if c == 10:
                if self.state[r][c-1] > 2: return True
            else: return self.state[r][c+1] > 2 and self.state[r][c-1] > 2
        return False


    def get_freedom_1s(self):
        for r in range(1,10,2):
            for c in range(1,10,2):
                if self.state[r][c] == 1: # 自由度为1，是死格
                    self.u, self.v = r, c
                    return True
        return False

    def set_either_side(self,r,c,player=0): # 设置边两边的格子自由度减一
        if r%2 == 0: # 横线
            if (r>0):  
                self.state[r-1][c] -= 1
                if self.state[r-1][c] == 0:
                    self.score[player] += 1
            if (r<10):
                self.state[r+1][c] -= 1
                if self.state[r+1][c] == 0:
                    self.score[player] += 1
        else:
            if (c>0):
                self.state[r][c-1] -= 1
                if self.state[r][c-1] == 0:
                    self.score[player] += 1
            if (c<10):
                self.state[r][c+1] -= 1
                if self.state[r][c+1] == 0:
                    self.score[player] += 1
                

    def move_edge(self,r,c,player=0):
        self.state[r][c] = 1
        self.set_either_side(r,c)
    
    def move_a_dead_edge_from_all(self):
        for r in range(1,10,2):
            for c in range(1,10,2):
                if self.state[r][c] == 1: # 自由度为1，是死格
                    if self.state[r-1][c] == 0:
                        if r == 1 or self.state[r-2][c] != 2:
                            self.move_edge(r-1,c)
                    elif self.state[r][c+1] == 0:
                        if c == 9 or self.state[r][c+2] != 2:
                            self.move_edge(r,c+1)
                    elif self.state[r+1][c] == 0:
                        if r == 9 or self.state[r+2][c] != 2:
                            self.move_edge(r+1,c)
                    elif self.state[r][c-1] == 0:
                        if c == 1 or self.state[r][c-2] != 2:
                            self.move_edge(r,c-1)
