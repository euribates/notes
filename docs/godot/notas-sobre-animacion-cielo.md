Hola, mundo que tal todo. Júpiter es el planeta más masivo de todo el Sistema Solar

n this lesson, we will continue implementing the day-night cycle script that we began work on previously. We will begin by setting up the systems to control the time variable, as this will be integral to the rest of the script. Our first step will be to set the time_rate value, which can be done in the _ready function.
func _ready():
    time_rate = 1.0 / day_length

Here we set the time_rate property to be the amount per second to increase the time value. “1.0 / day_length” means it will take the full day_length value (in seconds), to perform the full day-night cycle. We can also update the time property to match start_time, as _ready will run at the beginning of our game.
func _ready():
    ...
    time = start_time

In the ready function, we also want to store the Sun child node in the sun property.
func _ready():
    ...
    sun = get_node("Sun")

Finally, for our time property, we want to increase it over time in the _process function.
func _process(delta):
    time += time_rate * delta

By multiplying our time_rate value by delta we convert the per frame value to per second, this means that we will increase the time by a full time_rate once per second. However, we currently do not have a way of handling time going over 1, so to fix this we will use an if statement to check whether time is more than 1.0, and if it is, reset it to 0.0.
func _process(delta):
    ...
    if time >= 1.0:
        time = 0.0

This will ensure that our time variable will always loop back around from 1 to 0 as intended.
Rotating the Sun

We can now start to modify the elements of our scene based on the time variable. We will start by rotating the Sun node, as this will have the largest effect on the scene. We can do this by changing the rotation_degrees.x value of the sun to be equal “time x 360“. Because time is a value between 0 and 1, this multiplication will change the Sun’s rotation to match the time position, where 0 is 0% rotated and 1 is 100% rotated. For example, a time value of 0.25 would translate to the Sun rotating 90 degrees, which would be a sunrise.
func _process(delta):
    ...
    sun.rotation_degrees.x = time * 360

If you press play you can see this in action by looking at the skybox, where the sun-visual rises and sets over the horizon. This implementation isn’t perfect, however, as 0 is not at the bottom of the terrain, as would be expected. This means that our start_time isn’t where we would expect it to be, and could cause some further issues down the line. To fix this we will add an offset to our rotation. This can be easily done by adding 90 degrees to our rotation formula.
func _process(delta):
    ...
    sun.rotation_degrees.x = time * 360 + 90
Sun Color and Intensity

Currently, the sun goes up and goes down, but isn’t particularly dynamic. To fix this, we can change the color and intensity of the light coming from our Sun so that the color of the scene is a lot more dynamic. To implement this, we will first need to add two new variables to our script. The first will be called sun_color and have a type of Gradient. This will need to have the export tag so that it can be accessed in the Inspector.
@export var sun_color : Gradient

The next variable will be called sun_intensity and will be of type Curve, this will also be exported to the Inspector window.
@export var sun_intensity : Curve

We can then assign these properties in the Inspector, starting with the Sun Color gradient object.

This gradient can be edited to represent the stages of the sun’s light and Godot will automatically blend between these colors. We can change the colors of the gradient by adding and adjusting color points along the line. We can think about the gradient line as being from time=0 on the left of the line, to time=1 on the right of the line. This means that each far edge will represent midnight, and the center of the gradient will represent midday, so we can adjust the colors accordingly.

Here we use orange instead of black for the midnight points to create a sunset effect as the sun goes down. We won’t need to worry about the orange light affecting our scene at night, as the intensity of the light will be low at this point in the cycle. To make use of this variable we need to update the sun’s color to the latest value. We can do this by sampling the sun_color gradient at the given time and setting the Sun node’s light_color to this.
func _process(delta):
    ...
    sun.light_color = sun_color.sample(time)

You can press play to see this change. Along with the scene’s lighting, the sun’s visual representation will also change to a darker orange during sunrises and sunsets.

In the next lesson, we will make use of our sun_intensity variable, along with implementing the Moon and WorldEnvironment controls.

Day Night Cycle – Part 3

In this lesson, we will begin by taking a quick break from our day-night cycle code to add some trees to our environment. This will be good to make our environment a bit more interesting and make the lighting changes more obvious. To begin with, we will create a new StaticBody3D node.

We can then rename this node to ‘Tree’.

We can then drag the treePine.obj asset into the scene to create a model of it.

We can rename this node to ‘Model’ and make it a child node of the Tree object.

We can then center the new Model node by setting its Position to (0, 0, 0).

To make it slightly larger, we can also set the Scale property to (4, 4, 4).

The Tree will also need a new CollisionShape3D node to specify the object’s collider.

We can set the Shape property, of this node, to a New CylinderShape3D node.

This can then be scaled along the trunk of the Tree model.

Finally, drag the Tree model into the FileSystem window to turn it into a scene. We can save this scene as ‘Tree.tscn’.

We can then duplicate (CTRL+D) this scene around the terrain to create a small forest on our island.

Changing the Sun Intensity

We can now continue work on the day-night cycle systems we were programming. In the previous lesson, we began work on the sun intensity system. To continue this we can add a New Curve object to the new Sun Intensity property on the DayNightCycle node.

This curve will work very similarly to our gradient from the previous lesson, where we add values along the timeline, and Godot automatically blends between the values given. However, instead of colors, a curve specifies float values at the time points. This is represented by a graph in the object editor, where the x-axis represents the time value and the y-axis represents the light’s intensity. To add a point to the graph, right-click and select Add Point.

We can then outline three points along the graph to specify the sun’s intensity across the day. The far edges will be at night time when the sun has an intensity of 0. The center point will be at midday when the sun has its highest intensity.

We can also move the middle point to the early morning, and place another node in mid afternoon at the 1 value. This will spread out the high-intensity light across the full day which would be more realistic. Of course, you can test these values later and try tweaking them to get the effect you would like.

To get more fine control of these values, you can always open the Points section of the Curve object. The next step is to update our Sun’s light intensity to match the values given by our Curve object. This can be done by adding a line to the _process function in the DayNightCycle script.
func _process(delta):
    ...
    sun.light_energy = sun_intensity.sample(time)

This script will update the Sun node’s light_energy property based on the curve we have just created. As we do this in the _process method this will be updated every frame, which means our sun’s intensity will always match the color property that we set up previously. You can then test this by pressing play and watching the sun travel through the sky. You will see that the lighting on the environment changes as the sun sets and goes beneath the terrain.
Moon Lighting Challenge

Currently, the nighttime lighting doesn’t look particularly great, which is because we haven’t implemented the Moon lighting. As a bit of a challenge, try setting this up for the next lesson! The steps needed to do this will involve:

    Creating a new moon variable.
    Creating a moon color gradient.
    Creating a moon intensity curve.
    Updating the Moon node’s values.

It’s important to keep in mind the Moon’s values should always be the opposite of the Sun’s. So when the sun is at midday, the moon should be at midnight and have 0 intensity. You may also need to update the Moon node’s visibility in the Scene window. 
