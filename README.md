# Introduction
This is a repository of iToF phase simulator to visualize cyclic phase errors.

Time-of-flight cameras (**ToF cameras**) are imaging systems that can capture 3D information of the world unlike normal 2D RGB cameras. ToF cameras measure distance to an object by analyizng light that is emited from the camera and reflected by the target object. ToF cameras can be classified into two categories: indirect ToF (**iToF**) and direct ToF (dToF). In the case of iToF, periodic signals are generated on the sensor and laser. By evaluating correlation between illumination signal coming back to the sensor (source modulation signal) and sensor signal (sensor demodulation signal), 3D information, called phase, is extracted. In iToF, it has been known that phase error (= difference between ground truth phase and measured phase) shows periodic behavior. This error is called **cyclic error, wiggling error, and harmonic aliasing error**. Knowing the characteristics of the cyclic error is important to test actual iToF cameras and make good calibrations. In this repository, an **iToF phase simulator is provided in order to simulate cyclic error**.

For further detailed and intuitive explanations about iToF principles and cyclic error, you can read, for example, [this blog](https://medium.com/chronoptics-time-of-flight/harmonic-aliasing-wiggle-error-in-indirect-time-of-flight-depth-cameras-efa1632d4d1b) written by Dr. Refael Whyte. 

# Code
You can run [main.py](https://github.com/ksonod/itof_cyclic_error_simulator/blob/main/main.py) or use [main_notebook.ipynb](https://github.com/ksonod/itof_cyclic_error_simulator/blob/main/main_notebook.ipynb). CONFIG dict is the only part user has to specify.
