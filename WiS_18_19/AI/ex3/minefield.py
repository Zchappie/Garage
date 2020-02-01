import random

class Minefield:
    def __init__(self, dim_x=10, dim_y=10, mine_count=15, mine_map=None):
        assert mine_count <= dim_x*dim_y

        self._bot_pos = 0, 0
        self.known_pos = [(0,0)]

        if mine_map == None:
            self._goal_pos = dim_x - 1, dim_y - 1
            
            self._mine_map = [[False]*dim_y for x in range(dim_x)]
            for i in range(mine_count):
                rx = random.randint(0, dim_x-1)
                ry = random.randint(0, dim_y-1)
                while self._mine_map[rx][ry] or (rx, ry) in (self.bot_pos, self.goal_pos):
                    rx = random.randint(0, dim_x-1)
                    ry = random.randint(0, dim_y-1)
                self._mine_map[rx][ry] = True
        else:
            self._mine_map = [[bool(bm) for bm in col] for col in mine_map]
            assert len(self._mine_map) > 0
            assert all(map(lambda col: len(col)==self.dim_y, self._mine_map))

            self._goal_pos = self.dim_x - 1, self.dim_y - 1

    @property
    def dim_x(self):
        return len(self._mine_map)
    @property
    def dim_y(self):
        return len(self._mine_map[0])
    @property
    def bot_pos(self):
        return self._bot_pos
    @property
    def goal_pos(self):
        return self._goal_pos

    def valid_pos(self, x, y):
        return 0<=x<self.dim_x and 0<=y<self.dim_y

    def surrounding_positions(self, x, y):
        for tx, ty in (x+1, y), (x-1, y), (x, y+1), (x, y-1):
            if self.valid_pos(tx, ty):
                yield tx, ty

    def state_in_view(self):
        return self._state_at(*self._bot_pos)

    def apply_move(self, mx, my):
        assert mx in (-1,0,1)
        assert my in (-1,0,1)
        assert mx+my in (-1,1)

        self._bot_pos = self._bot_pos[0]+mx, self._bot_pos[1]+my
    
    def add_known_pos(self, mx, my):
        for pos in self.known_pos:
            if pos[0] == mx and pos[1] == my:
                return
        self.known_pos.append((mx,my))

    def draw(self, canvas):
        assert canvas.width%self.dim_x == 0
        assert canvas.height%self.dim_y == 0
        assert canvas.width//self.dim_x == canvas.height//self.dim_y

        def sw_iy(y): return self.dim_y-1-y

        canvas.fill(255, 255, 255)
        canvas.stroke(0, 0, 0)
        canvas.strokeWidth(round(canvas.width / self.dim_x / 20))
        canvas.font("%ipx Arial" % round((canvas.height//self.dim_y) * 0.8))

        canvas.clear()

        for pos in self.known_pos:
            canvas.fill(0, 0, 255)
            goal_rect_path = [
                (pos[0]/self.dim_x, sw_iy(pos[1])/self.dim_y),
                ((pos[0]+1)/self.dim_x, sw_iy(pos[1])/self.dim_y),
                ((pos[0]+1)/self.dim_x, (sw_iy(pos[1])+1)/self.dim_y),
                (pos[0]/self.dim_x, (sw_iy(pos[1])+1)/self.dim_y),
            ]
            self._fill_polygon_n(canvas, goal_rect_path)
        
        canvas.fill(0, 255, 0)
        goal_rect_path = [
            (self.goal_pos[0]/self.dim_x, sw_iy(self.goal_pos[1])/self.dim_y),
            ((self.goal_pos[0]+1)/self.dim_x, sw_iy(self.goal_pos[1])/self.dim_y),
            ((self.goal_pos[0]+1)/self.dim_x, (sw_iy(self.goal_pos[1])+1)/self.dim_y),
            (self.goal_pos[0]/self.dim_x, (sw_iy(self.goal_pos[1])+1)/self.dim_y),
        ]
        self._fill_polygon_n(canvas, goal_rect_path)
        
        canvas.fill(255, 0, 0)
        bot_rect_path = [
            (self.bot_pos[0]/self.dim_x, (sw_iy(self.bot_pos[1])+0.5)/self.dim_y),
            ((self.bot_pos[0]+0.5)/self.dim_x, sw_iy(self.bot_pos[1])/self.dim_y),
            ((self.bot_pos[0]+1)/self.dim_x, (sw_iy(self.bot_pos[1])+0.5)/self.dim_y),
            ((self.bot_pos[0]+0.5)/self.dim_x, (sw_iy(self.bot_pos[1])+1)/self.dim_y),
        ]
        self._fill_polygon_n(canvas, bot_rect_path)

        for x in range(1, self.dim_x):
            canvas.line_n(x/self.dim_x, 0, x/self.dim_x, 1)
        for y in range(1, self.dim_y):
            canvas.line_n(0, y/self.dim_y, 1, y/self.dim_y)

        canvas.fill(0, 0, 0)
        for x in range(self.dim_x):
            for y in range(self.dim_y):
                state = self._state_at(x, y)
                if state == -1:
                    path = [
                        ((x+0.5)/self.dim_x, (sw_iy(y)+0.1)/self.dim_y),
                        ((x+0.61)/self.dim_x, (sw_iy(y)+0.22)/self.dim_y),
                        ((x+0.78)/self.dim_x, (sw_iy(y)+0.22)/self.dim_y),
                        ((x+0.78)/self.dim_x, (sw_iy(y)+0.39)/self.dim_y),
                        ((x+0.9)/self.dim_x, (sw_iy(y)+0.5)/self.dim_y),
                        ((x+0.78)/self.dim_x, (sw_iy(y)+0.61)/self.dim_y),
                        ((x+0.78)/self.dim_x, (sw_iy(y)+0.78)/self.dim_y),
                        ((x+0.61)/self.dim_x, (sw_iy(y)+0.78)/self.dim_y),
                        ((x+0.5)/self.dim_x, (sw_iy(y)+0.9)/self.dim_y),
                        ((x+0.39)/self.dim_x, (sw_iy(y)+0.78)/self.dim_y),
                        ((x+0.22)/self.dim_x, (sw_iy(y)+0.78)/self.dim_y),
                        ((x+0.22)/self.dim_x, (sw_iy(y)+0.61)/self.dim_y),
                        ((x+0.1)/self.dim_x, (sw_iy(y)+0.5)/self.dim_y),
                        ((x+0.22)/self.dim_x, (sw_iy(y)+0.39)/self.dim_y),
                        ((x+0.22)/self.dim_x, (sw_iy(y)+0.22)/self.dim_y),
                        ((x+0.39)/self.dim_x, (sw_iy(y)+0.22)/self.dim_y),
                    ]
                    self._fill_polygon_n(canvas, path)
                else:
                    canvas.text_n(str(state), (x+0.2)/self.dim_x, (sw_iy(y)+0.8)/self.dim_y)

    def _state_at(self, x, y):
        if self._mine_map[x][y]:
            return -1 # mine
        else:
            neighbouring_mines = 0
            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= nx < self.dim_x and 0 <= ny < self.dim_y:
                    if self._mine_map[nx][ny]:
                        neighbouring_mines += 1
            return neighbouring_mines
    def _fill_polygon_n(self, canvas, path):
        js_move = "path.moveTo(%i,%i);" %\
            (round(path[0][0] * canvas.width), round(path[0][1] * canvas.height))
        for px, py in path[1:]:
            js_move += "\npath.lineTo(%i,%i);" % (round(px * canvas.width), round(py * canvas.height))

        canvas.exec_list.append("""{
            var path=new Path2D();
            %s
            %s_canvas_object.ctx.fill(path);
        }""" % (js_move, canvas.cid))
