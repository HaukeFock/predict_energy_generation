import os
import pandas as pd


def generate_dataframe(path,timeframe,folder):
    os.chdir(os.path.join(path,timeframe,'data'))
    for path, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if '.csv' in f:
                if 'data' in f:
                    data_df = pd.read_csv(f, index_col=False)
                if 'sdo' in f:
                    sdo_df = pd.read_csv(f, index_col=False)
    sdo_df.rename(columns = {'Geogr_Laenge':'Longitude','Geogr_Breite':'Latitude','Hoehe_ueber_NN':'Height_above_NN'}, inplace = True)
    merged_df = data_df.merge(sdo_df,left_on = 'SDO_ID',right_on = 'SDO_ID')
    merged_df['Zeitstempel'] = pd.to_datetime(merged_df['Zeitstempel'])
    merged_df.rename(columns = {'Zeitstempel':'Date','Wert':folder.capitalize().replace(' ','_'),'Produkt_Code':'Product_Code','Geogr_Laenge':'Longitude','Geogr_Breite':'Latitude','Hoehe_ueber_NN':'Height_above_NN'}, inplace = True)
    merged_df = merged_df.set_index('Date')
    merged_df.drop(columns=['Qualitaet_Byte','Qualitaet_Niveau','Metadata_Link'],inplace=True)
    return merged_df, sdo_df


if __name__ == "__main__":
    df, sdo_df = generate_dataframe('/Users/michael.kuntz/code/HaukeFock/predict_energy_generation/raw_data/Features/Humidity','daily','Humidity')
