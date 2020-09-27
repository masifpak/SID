import Gen_Key
import pickle

if __name__ == "__main__":
    client = Gen_Key.DSSEClient()
    client.Gen()
    #client.Enc(["./data/thatcher.txt", "./data/gandhi.txt"])
    pickle.dump(client.exportkeys(), open("keys", "wb"))
