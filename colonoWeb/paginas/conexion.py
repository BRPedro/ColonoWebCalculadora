import psycopg2

class BDConexion:
    def __init__(self,dbname,user,password):
        self.conn=None
        try:
            self.conn = psycopg2.connect("dbname='"+dbname+"' user='"+user+"' password='"+password+"'")
        except:
            self.conn = None

    def desconectar(self):
        self.conn.close()

    def insertarTC_COORDENADA(self,fila,columana):
        try:
            cur = self.conn.cursor()
            cur.execute("select insercioncoordenasas("+str(fila)+","+str(columana)+")")
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            print e
            if self.conn:
                self.conn.rollback()

    def borradolimite(self,limite):
        try:
            cur = self.conn.cursor()
            cur.execute("select borradolimite(" + str(limite) +  ")")
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            print e
            if self.conn:
                self.conn.rollback()

    def centroides(self):
        try:
            cur = self.conn.cursor()
            cur.execute("select centroides()")
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            print e
            if self.conn:
                self.conn.rollback()

    def borrarCoordenadas(self):
        cur = self.conn.cursor()
        cur.execute("delete from paginas_tc_coordenada")
        self.conn.commit()

    def seleccionSimpleCoordenadas(self):
        lista=[]
        try:
            cur = self.conn.cursor()
            cur.execute("select * from paginas_tc_coordenada")

            while True:

                row = cur.fetchone()

                if row == None:
                    break

                lista.append([row[1], row[2]])


        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
        return lista


nn=BDConexion('BDAPTECH','colono14','1234')
nn.insertarTC_COORDENADA(2,3)
print nn.seleccionSimpleCoordenadas()

if nn.conn!=None:
    print "Bien"
else:
    print "Error"
