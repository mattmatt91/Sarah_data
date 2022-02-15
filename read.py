import pandas as pd
import os
from pathlib import Path


def mkdir(path, folder):
    path = os.path.join(path, folder)
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def read_identification(path):
    path_identification = os.path.join(path, "peak_idenification.csv")
    df = pd.read_csv(path_identification, delimiter=';')
    df.columns = [i.replace('#', '') for i in df.columns]
    df.columns = [i.replace(' ', '') for i in df.columns]
    df_new = df[df['Hit'] == 1]
    df_new['Name'] = [i[:i.find('$')] for i in df_new['Name']]
    df_new.set_index('Spectrum', inplace=True)
    save_df(df_new, path, 'identification_extracted')
    return df_new
    
    
def save_df(df, path, name):
    path = path + '\\results'
    Path(path).mkdir(parents=True, exist_ok=True)
    path = path + '\\' + name + '.csv'
    print(name + 'saved as ' + path)
    df.to_csv(path, sep=';', decimal=',', index = True)
    
        
def read_peak_spectra(path):
    # read file
    path_peak_spectra = os.path.join(path, "peak_spectra.csv")
    with open(path_peak_spectra) as file:
        lines = file.readlines()
        
        # searching slice index
        start_index = []
        for line, index in zip(lines, range(len(lines))):
            if line.find('[MS Spectrum]') >= 0:
                start_index.append(index)
        
        
        # slicing data to peaks
        for s_index, index in zip(start_index, range(len(start_index))):
            new_list = []
            try:
                new_list = lines[s_index:start_index[index+1]-1]
            except:
                new_list = lines[s_index:]
            
            name = new_list[2][new_list[2].find('\t')+1:]
            name = name[:name.find(' ')].replace('.', '_')
            
            # removing header
            new_list = new_list[6:]
            
            # creating one string for each peak
            new_list_string = ''
            for i in new_list:
                new_list_string +=i
                
            path_peaks = mkdir(path, f'results\\peaks')        
            path_to_peak =os.path.join(path_peaks, name)
            with open(path_to_peak, "w") as text_file:
                text_file.write(new_list_string)
  
      
        
def main(path):

    print(read_identification(path))

    read_peak_spectra(path)
    
    
main('data')