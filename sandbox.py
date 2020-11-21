import autokeras as ak
import tensorflow as tf
import numpy as np

class SingleDenseLayerBlock(ak.Block):

    def build(self, hp, inputs=None):
        # Get the input_node from inputs.
        input_node = tf.python.util.nest.flatten(inputs)[0]
        layer = tf.keras.layers.Dense(hp.Int('num_units', min_value=32, max_value=512, step=32))
        output_node = layer(input_node)
        return output_node


input_node = ak.Input()
output_node = SingleDenseLayerBlock()(input_node)
print(type(output_node))
