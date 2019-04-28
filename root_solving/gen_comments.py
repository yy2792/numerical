import pandas as pd

if __name__ == '__main__':

    df = pd.read_csv('grading.csv')

    cols = [col for col in df.columns if col != 'comment']
    df_temp = df[cols]

    df['comments'] = df_temp.apply(lambda x: ','.join(x.index[x == 1]), axis=1)

    df.to_csv('grading.csv')