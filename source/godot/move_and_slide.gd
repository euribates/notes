extends CharacterBody2D

var SPEED: float = 150.0
var direction: Vector2 = Vector2(0, 0)

func _ready():
	print('Player _ready starts')
	velocity.x = 0	
	velocity.y = 0
	print('Player _ready ends')
	
func _process(delta):
	print('_process starts')
	direction.x = 0
	direction.y = 0
	if Input.is_key_pressed(KEY_LEFT):
		direction.x = -1
	if Input.is_key_pressed(KEY_RIGHT):
		direction.x = 1
	if Input.is_key_pressed(KEY_UP):
		direction.y = -1
	if Input.is_key_pressed(KEY_DOWN):
		direction.y = 1
	velocity = direction.normalized() * SPEED * delta
 	move_and_slide()
	print(velocity, global_position, delta)
