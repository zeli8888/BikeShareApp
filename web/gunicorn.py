from .bike_share_application import main
import logging
import warnings
import sys
warnings.filterwarnings("ignore")
logging.basicConfig(
    level=logging.ERROR,
    stream=sys.stdout,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)
app = main('EC2')