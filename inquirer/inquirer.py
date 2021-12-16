from cryptography.fernet import Fernet

# Generate Key and Store

# key = Fernet.generate_key()
# with open("fernet_key.key", "wb") as f:
#     f.write(key)


# Get the key
with open("fernet_key.key", "rb") as f:
    key = f.read()


#Encrypt File
with open("Kıbrıs Çağrı Açma.PNG","rb") as f:
    data = f.read()
    fernet = Fernet(key)   
    encrypted = fernet.encrypt(data)
    with open("Kıbrıs Çağrı Açma.PNG","wb") as g:
        g.write(encrypted)


#Decrypt File
with open("Kıbrıs Çağrı Açma.PNG","rb") as f:
    data = f.read() 
    decrypted = fernet.decrypt(data)
    with open("Kıbrıs Çağrı Açma.PNG","wb") as g:
        g.write(decrypted)


