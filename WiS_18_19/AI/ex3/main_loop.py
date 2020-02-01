from notebook import Canvas
from path_planning import PathPlanner
from utils import expr
import time

def main_loop(minefield, kb, stop_on_risk = False, loop_delay = 1):
    canvas = Canvas("testcanvas", minefield.dim_x*50, minefield.dim_y*50)
    minefield.draw(canvas)
    canvas.update()

    pp = PathPlanner(minefield, kb, stop_on_risk = stop_on_risk)

    while True:
        #print("pos:", minefield.bot_pos)
        if minefield.bot_pos == minefield.goal_pos:
            print("Victory!!!")
            break

        siv = minefield.state_in_view()
        if siv == -1:
            kb.tell(expr("B%i%i"%minefield.bot_pos))
            print("KaBoom")
            break
        elif siv == 0:
            kb.tell(expr("Z%i%i"%minefield.bot_pos))
        elif siv == 1:
            kb.tell(expr("O%i%i"%minefield.bot_pos))
        elif siv == 2:
            kb.tell(expr("TW%i%i"%minefield.bot_pos))
        elif siv == 3:
            kb.tell(expr("TH%i%i"%minefield.bot_pos))
        elif siv == 4:
            kb.tell(expr("F%i%i"%minefield.bot_pos))
        kb.tell(expr("~B%i%i"%minefield.bot_pos))

        nm = pp.next_move()
        if nm == None: return
        minefield.apply_move(*nm)

        minefield.draw(canvas)
        canvas.update()

        time.sleep(loop_delay)
