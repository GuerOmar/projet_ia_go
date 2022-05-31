import tensorflow.keras
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, BatchNormalization
import tensorflow.keras.optimizers as optimizers
from sklearn.model_selection import train_test_split
import numpy as np
# Import du fichier contenat les données d'entrainement

def get_raw_data_go():
    ''' Returns the set of samples from the local file or download it if it does not exists'''
    import gzip, os.path
    import json

    raw_samples_file = "samples-9x9.json.gz"

    if not os.path.isfile(raw_samples_file):
        print("File", raw_samples_file, "not found, I am downloading it...", end="")
        import urllib.request
        urllib.request.urlretrieve ("https://www.labri.fr/perso/lsimon/ia-inge2/samples-9x9.json.gz", "samples-9x9.json.gz")
        print(" Done")

    with gzip.open("samples-9x9.json.gz") as fz:
        data = json.loads(fz.read().decode("utf-8"))
    return data

def name_to_coord(s):
    assert s != "PASS"
    indexLetters = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'J':8}

    col = indexLetters[s[0]]
    lin = int(s[1:]) - 1
    return col, lin

def data_transform(data):
  """ Cette fonction prend en entrée le fichier Json et elle retourne deux tableaux qui contiennent  respectivement l'état du borad et  les probalibiltés que le noir (black) gagne """
  X=[]
  Y=[]
  for d in data:
    transformed_data = np.zeros((9,9,2), dtype=np.int32)
    for j in range(len(d["black_stones"])):
       x,y = name_to_coord(d["black_stones"][j])
       transformed_data[x][y][0]=1
    for j in range(len(d["white_stones"])):
       x,y = name_to_coord(d["white_stones"][j])
       transformed_data[x][y][1]=1
    board=transformed_data
    X.append(board)
    Y.append(d["black_wins"]/d["rollouts"])
    X.append(np.rot90(board, k=1, axes=(0,1)))
    Y.append(d["black_wins"]/d["rollouts"])
    X.append(np.rot90(board, k=2, axes=(0,1)))
    Y.append(d["black_wins"]/d["rollouts"])
    X.append(np.rot90(board, k=3, axes=(0,1)))
    Y.append(d["black_wins"]/d["rollouts"])
    board = np.flipud(board)
    X.append(board)
    Y.append(d["black_wins"]/d["rollouts"])
    X.append(np.rot90(board, k=1, axes=(0,1)))
    Y.append(d["black_wins"]/d["rollouts"])
    X.append(np.rot90(board, k=2, axes=(0,1)))
    Y.append(d["black_wins"]/d["rollouts"])
    X.append(np.rot90(board, k=3, axes=(0,1)))
    Y.append(d["black_wins"]/d["rollouts"])

  return np.array(X), np.array(Y)


def model_def():
    epochs = 20
    batch_size = 1024

    model = Sequential([
        Conv2D(48, (3, 3), padding='same', activation = 'relu', data_format='channels_last', input_shape=(9,9,2)),
        Dropout(rate=0.5),
        BatchNormalization(),
        Conv2D(32, (3, 3), padding='same', activation = 'relu', data_format='channels_last'),
        Dropout(rate=0.5),
        BatchNormalization(),
        Flatten(),
        Dense(1024, activation = 'relu'),
        Dropout(rate=0.5),
        Dense(81, activation = 'relu'),
        Dropout(rate=0.5),
        Dense(1, activation = 'sigmoid')
    ])

    model.compile(loss='mse', optimizer='adam', metrics=['accuracy','mse', 'mae'])
    model.summary()
    return model
def Entrainer():
    epochs = 20
    batch_size = 1024
    data = get_raw_data_go()
    X_data, Y_data = data_transform(data)
    X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, test_size=0.2)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    Y_train =Y_train.astype('float32')
    Y_test = Y_test.astype('float32')
    model= model_def()
    history = model.fit(X_data,Y_data, batch_size=batch_size, epochs=epochs, verbose=1)
    model.save("my_model.h5")
def transform_data(data):
      X = []
      transformed_data = np.zeros((9,9,2), dtype=np.int32)
      black_stones=[]
      white_stones=[]
      for i in range(len(data)):
        if(data[i]=="PASS"):
          continue
        if(i%2==0):
          black_stones.append(data[i])
        else :
          white_stones.append(data[i])
      for j in range(len(black_stones)):
        x,y = name_to_coord(black_stones[j])
        transformed_data[x][y][0]=1
      for j in range(len(white_stones)):
        x,y = name_to_coord(white_stones[j])
        transformed_data[x][y][1]=1
      board=transformed_data
      X.append(board)

      X_data = np.array(X)
      return X_data

def import_model():
      model = keras.models.load_model("/home/sana/Documents/Intelligence_artificielle/projet_ia_go/go-package/my_model.h5")
      return model
def predection(data,model):
    y_predicted = model.predict(transform_data(data))
    return y_predicted
#Entrainer()