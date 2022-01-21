from multiprocessing import Pipe
from RobotAgent import RobotAgent
from HumanAgent import HumanAgent
from time import sleep

if __name__ == "__main__":
    robot_conn, human_conn = Pipe()
    r = RobotAgent(robot_conn)
    h = HumanAgent(human_conn)
    r.start()
    h.start()
    sleep(5)
    r.stop()
    h.stop()
