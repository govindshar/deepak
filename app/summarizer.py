
import pandas as pd
from io import BytesIO

def read_excel(file_bytes) -> str:
    df = pd.read_excel(BytesIO(file_bytes))
    return df.to_markdown(index=False)
