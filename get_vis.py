# ------------------------------------------------------------------------------
# Import
# ------------------------------------------------------------------------------
from time import time
import datetime
import plotly.express as px
import pandas as pd
from croniter import croniter
# ------------------------------------------------------------------------------
# Init
# ------------------------------------------------------------------------------
STARTDATE = datetime.datetime(2021,12,6)
ENDDATE   = STARTDATE + datetime.timedelta(7)
INFILE    = 'crondat.csv'
# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
    # --------------------------------------------------------------------------
    # Start
    # --------------------------------------------------------------------------
    print('Starting...')
    # --------------------------------------------------------------------------
    # Read the dataframe
    # --------------------------------------------------------------------------
    print('Manipulating the data...')
    inpdf = pd.read_csv(INFILE,delimiter='\t')
    # --------------------------------------------------------------------------
    # Get the relevant fields
    # --------------------------------------------------------------------------
    inpdf = inpdf[['Source','Name','CRON(UTC)','Runtime(m)']].copy()
    inpdf['Name'] = inpdf['Source'] + '|' + inpdf['Name']
    # --------------------------------------------------------------------------
    # Create the time series data
    # --------------------------------------------------------------------------
    print('Building the timeseries...')
    df = create_timeseries(inpdf)
    # --------------------------------------------------------------------------
    # Create the timeline
    # --------------------------------------------------------------------------
    print('Exporting the image...')
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Name", color="Source")
    fig.write_image('timeline.png',width = 2500,height=1000)
    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return

def create_timeseries(df):
    """
    Intake the dataframe and figure out how to create a time-series
    """
    data = []
    # --------------------------------------------------------------------------
    # Start
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # Go through the listed rows
    # --------------------------------------------------------------------------
    for idx,row in df.iterrows():
        citer = croniter(row['CRON(UTC)'],STARTDATE)
        curr = citer.get_next(datetime.datetime)
        while curr <= ENDDATE:
            start = curr
            stop  = curr + datetime.timedelta(minutes=float(row['Runtime']))
            data.append([row['Source'],row['Name'],start,stop])
            curr = citer.get_next(datetime.datetime)
    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return pd.DataFrame(data,columns=['Source','Name','Start','Finish'])
# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    start = time()
    main()
    stop = time()
    print(f'{stop-start}s elapsed')