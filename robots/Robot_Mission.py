from time import sleep
import motion
import straight_motion

motion.init()
straight_motion.init()

def execute_command(command, count):
  duration = count * 0.1
  kp = 170

  motion.stop()
  sleep(0.2)

  if command == 'F':
    straight_motion.move(duration, kp)
  elif command == 'L':
    motion.left()
    sleep(duration)
    motion.stop()
  elif command == 'R':
    motion.right()
    sleep(duration)
    motion.stop()
  elif command == 'B':
    motion.backward()
    sleep(duration)
    motion.stop()

def run_mission(file_path):
  with open(file_path, 'r') as f:
    f.readline()
    sleep(2)
    current_command = 'S'
    count = 0

    for line in f:
      data = line.strip().split(',')
      F = int(data[1])
      L = int(data[2])
      R = int(data[3])
      B = int(data[4])

      if F == 1:
        command = 'F'
      elif L == 2:
        command = 'L'
      elif R == 3:
        command = 'R'
      elif B == 4:
        command = 'B'
      else:
        command = 'S'

      if command == current_command:
        count += 1
      else:
        execute_command(current_command, count)
        current_command = command
        count = 1

    execute_command(current_command, count)
    motion.stop()
run_mission('/robot_mission.csv')




