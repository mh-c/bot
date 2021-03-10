from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Define session variable
position = [0,0]
horizontal = True
positive = True
started = False

@app.route('/')
def mindex():
	return render_template('index.html')

# Robot command execution
@socketio.on('cmd')
def exe(x):
	global position,horizontal,positive,started
	emit('cmd', x, broadcast=True)
	if x.startswith('PLACE'):
		ini = x.split(' ')[1].split(',')
		if 0 <= int(ini[0]) <= 4 or 0 <= int(ini[0]) <= 4:
			position[0] = int(ini[0])
			position[1] = int(ini[1])
			horizontal = True if ini[2] == 'EAST' or ini[2] == 'WEST' else False
			positive = True if ini[2] == 'EAST' or ini[2] == 'NORTH' else False
			started = True
	elif x == 'MOVE' and started:
		if horizontal:
			position[0] += 1 if positive else -1
			position[0] = resetFail(position[0])
		else:
			position[1] += 1 if positive else -1
			position[1] = resetFail(position[1])
	elif x == 'LEFT' and started:
		positive = positive if horizontal else not positive
		horizontal = not horizontal
	elif x == 'RIGHT' and started:
		positive = not positive if horizontal else positive
		horizontal = not horizontal
	elif x == 'REPORT' and started:
		emit('output', ','.join([str(position[0]),str(position[1]),getDirection(horizontal, positive)]), broadcast=True)

# Helper
def resetFail(x):
	if x < 0:
		return 0
	elif x > 4:
		return 4
	return x

def getDirection(x,y):
	if x:
		if y:
			return 'EAST'
		else:
			return 'WEST'
	else:
		if y:
			return 'NORTH'
		else:
			return 'SOUTH'

if __name__ == '__main__':
	(app.run(host='127.0.0.1', port=5000, debug=True))