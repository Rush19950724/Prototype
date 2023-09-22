import os
from deta import Deta
from dotenv import load_dotenv
import pandas as pd

load_dotenv(".env")

deta_key = os.getenv("deta_key")

deta = Deta(deta_key)
