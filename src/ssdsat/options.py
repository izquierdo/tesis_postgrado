import sys
import logging

# path of the c2d compiler
c2d = sys.path[0] + "/c2d/c2d_linux"

# path of the model enumerators
models = sys.path[0] + "/models/models"
bestmodel = sys.path[0] + "/models/bestmodel"

# maximum number of models to be displayed
max_models = 50

# logging level and output file
loglevel = logging.DEBUG
logging_output_file = None

# user defined options
user_options = {}
