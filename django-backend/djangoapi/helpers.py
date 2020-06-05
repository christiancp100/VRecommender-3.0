
def _formatDate(date):
    aux = date.split("T")[0].split("-")
    return aux[2] + "/" +  aux[1] + "/" + aux[0]

def _reformatKey(key):
    aux = key.split("-")
    fromValue = int(float(aux[0].strip()))
    toValue = int(float(aux[1].strip()))
    return "(" + str(fromValue) + "," + str(toValue) + ")"